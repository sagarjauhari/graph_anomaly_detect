# -*- coding: utf-8 -*-
"""
Created on Thu Nov 14 13:53:46 2013
@author: Sagar Jauhari
"""

import scipy.stats as st
import sys
from os import listdir
from os.path import isfile, join
from igraph import *
import scipy.spatial.distance
import matplotlib.pyplot as plt

# import local config: Set you local paths in dev_settings.py
DATA_URL=""
SAVE_URL=""
try:
    from dev_settings import *
except:
    pass

#==============================================================================
# 7 feature functions and their helper functions
# Page 2: Berlingerio, Michele, et al. "NetSimile: a scalable approach to
# size-independent network similarity." arXiv preprint arXiv:1209.2684 (2012).
#==============================================================================
def get_egonet(node, graph):
    """
    A node’s egonet is the induced subgraph formed by the node and its
    neighbors. Returns list of vertices that belong to the egonet
    """
    return graph.neighborhood(node)

def get_di(node, graph):
    """
    Number of neigbors
    """
    return graph.neighborhood_size(node)

def get_ci(node, graph):
    """
    TODO: Define function
    """
    return 3

def get_dni(node, graph):
    """
    Average number of node’s two-hop away neighbors
    """
    return mean([get_di(n, graph) for n in get_egonet(node, graph) \
                                  if n != node])

def get_cni(node, graph):
    """
    TODO: Define function
    """
    return 5

def get_eegoi(node, graph):
    """
    TODO: Define function
    """
    return 6

def get_eoegoi(node, graph):
    """
    TODO: Define function
    """
    return 7

def get_negoi(node, graph):
    """
    TODO: Define function
    """
    return 8

#==============================================================================
# NetSimile Algorithm components
#==============================================================================
def get_features(g):
    return [(get_di(i,g), 
             get_ci(i,g), 
             get_dni(i,g),
             get_cni(i,g),
             get_eegoi(i,g),
             get_eoegoi(i,g),
             get_negoi(i,g)) for i in g.vs]

def get_features_all(graphs):
    return {g: get_features(graphs[g]) for g in graphs}

def get_moments(feat):
    """
    input: feature matrix of a single graph
    output: for each feature, return the 5 moments
    """
    feat_cols = zip(*feat)
    assert (len(feat_cols)==7),"Total columns != 7"
    
    # Calculate the 5 aggregates for each feature
    signature = []
    for f in feat_cols:
        signature = signature + [mean(f),
             median(f),
             std(f),
             st.skew(f),
             st.kurtosis(f)]
    return signature

def aggregator(features_all):
    return {g: get_moments(features_all[g]) for g in features_all}

def canberra_dist(sig1, sig2):
    """
    Returns the Canberra distance between graphs described by the signatures
    sig1 and sig2.
    """
    return scipy.spatial.distance.canberra(sig1, sig2)

def compare(sigs):
    """
    TODO: Define function
    To detect anomalies, compute the Canberra distance between consecutive time
    points (i.e.,between graphs G t and G t+1 ). You should calculate the 
    threshold value for the Canberra distance as explained in the project 
    description. Use the upper threshold to identify anomalies (i.e., two 
    consecutive time points above the threshold). For example, if both d(G1 , 
    G 2 ) and d(G 2 , G 3 ) are found to be above the threshold, then graph G2 
    is an anomalous graph, since it is different to the preceding and 
    succeeding graphs.
    input: 7x5 signature matrices for each graph
    output: Time series comparison of each graph on the basis of signatures
    """
    
    # Verify dimensions
    for g in sigs:
        assert (len(sigs[g])==7*5),"Total features != 7*5"
    
    # Calculate Canberra distance threshold
    
    # Order all the graphs names based on the timestamp
    ordered_graphs = sorted(sigs.keys(), key=lambda k:int(k.split('_',1)[0]))
    dists = [canberra_dist(sigs[ordered_graphs[i]],
                            sigs[ordered_graphs[i-1]])\
                            for i in range(1,len(ordered_graphs))]
    
    # Plot the (N-1) canberra distances comparing each graph with the 
    # previous one
    fig, ax = plt.subplots()
    ax.plot(dists)
    plt.grid(True)
        
    anomalies = []
    # Starting with the 2nd graph, compute the canberra distance of each
    # graph with the previous one. Compare with threshold value. Append
    # the anomalous grpahs to list anomalies[]

def file2igraph(file):
    """
    Coverts graph file into iGraph object, adds artifacts
    """
    with open(file, 'r') as fi:
        v,e = fi.next().split()
        e_list = [(int(i.split()[0]), int(i.split()[1])) for i in list(fi)]
        assert (int(e) == len(e_list)),\
                    "#edges mentioned and # of edges in file differ"
        g = Graph()
        g.add_vertices(int(v))
        g.add_edges(e_list)
        return g
            
#==============================================================================
# NetSimile algorithm
#==============================================================================
def NetSimile(graph_files, dir_path):
    #dict of graphs
    graphs = {f: file2igraph(join(dir_path, f)) for f in graph_files}

    # Get features of all nodes in all graphs
    # Format: {g1:[(f1..f7),(f1..f7),(f1..f7)...#nodes], g2:...}
    features_all = get_features_all(graphs)
    
    #signature of all graphs
    signatures = aggregator(features_all)
    
    compare(signatures)
    return
    
#==============================================================================
# Main
# Command line parameter: name-of-dataset
# Example Usage:$ python netsimile.py "reality_mining_voices"
#==============================================================================
if __name__=="__main__":
    dir_path = join(DATA_URL, sys.argv[1])
    onlyfiles = [f for f in listdir(dir_path) if \
                            isfile(join(dir_path,f)) ]
    NetSimile(onlyfiles, dir_path)
