# -*- coding: utf-8 -*-
"""
Created on Thu Nov 14 13:53:46 2013
@author: Sagar Jauhari
"""
import time
import numpy as np
import scipy as sp
import matplotlib as mpl
import matplotlib.pyplot as plt
from pylab import *
import scipy.stats as st
import sys
from os import listdir
from os.path import isfile, join
from igraph import *
import scipy.spatial.distance
import matplotlib.pyplot as plt
from util import *

is_debug = True

# import local config: Set your local paths in dev_settings.py
DATA_URL=""
SAVE_URL=""
try:
    from dev_settings import *
except ImportError:
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
    Clustering coefficient of node, defined as the number of triangles
    connected to node over the number of connected triples centered on node
    """
    return graph.transitivity_local_undirected(node, mode="zero")

def get_dni(node, graph):
    """
    Average number of node’s two-hop away neighbors
    """
    return mean([get_di(n, graph) for n in get_egonet(node, graph) \
                                  if n != node])

def get_cni(node, graph):
    """
    Average clustering coefficient of neighbors of node
    """
    return mean([get_ci(n, graph) for n in get_egonet(node, graph) \
                                  if n != node])

def get_eegoi(node, graph):
    """
    Number of edges in node’s egonet;
    """
    edges_to=[]
    vertices = get_egonet(node, graph)

    for n in vertices:
        for i in get_egonet(n, graph):
            if i!=n:
                edges_to.append(i)

    #remove external nodes
    edges2x=[i for i in edges_to if i in vertices]
    assert (len(edges2x)%2==0),"Wrong calculation"
    return len(edges2x)/2


def get_eoegoi(node, graph):
    """
    Number of outgoing edges from node's egonet
    """
    edges_to=[]
    vertices=get_egonet(node, graph)

    for n in vertices:
        for i in get_egonet(n, graph):
            edges_to.append(i)

    return len([i for i in edges_to if i not in vertices])

def get_negoi(node, graph):
    """
    Number of neighbors of node's egonet
    """
    vertices = get_egonet(node, graph)
    all_neighbors = []
    for v in vertices:
        all_neighbors = all_neighbors + get_egonet(v,graph)
    all_neighbors = set(all_neighbors)
    all_neighbors =  [i for i in all_neighbors if i not in vertices]
    return(len(all_neighbors))

#==============================================================================
# NetSimile Algorithm components
#==============================================================================
def get_features(g, name):
    print "Extracting features: %s" % name
    return [(get_di(i,g),
             get_ci(i,g),
             get_dni(i,g),
             get_cni(i,g),
             get_eegoi(i,g),
             get_eoegoi(i,g),
             get_negoi(i,g)) for i in g.vs]

def get_features_all(graphs):
    """
    Returns all features of all graphs.
    Out Format: {g1:[(f1..f7),(f1..f7),(f1..f7)...#nodes], g2:...}
    """
    # Order all the graphs names based on the timestamp
    ordered_names = sorted(graphs.keys(), key=lambda k:int(k.split('_',1)[0]))
    return {g: get_features(graphs[g], g) for g in ordered_names}

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
    print "Aggregating features"
    return {g: get_moments(features_all[g]) for g in features_all}

def canberra_dist(sig1, sig2):
    """
    Returns the Canberra distance between graphs described by the signatures
    sig1 and sig2.
    """
    return scipy.spatial.distance.canberra(sig1, sig2)

def dist_threshold(dists):
    """
    Median + 2*(std dev)
    """
    return dists[len(dists)/2] + 2*std(dists)

def plot_and_save(dists, up_limit):
    """
    Plot the (N-1) canberra distances comparing each graph with the previous
    """
    figure(num=None, figsize=(12, 6), dpi=80, facecolor='w', edgecolor='k')
    plt.plot(dists, "-o")
    axhline(y=up_limit, ls='-', c='r', label='Threshold: $\mu + 2\sigma$',lw=2)
    plt.grid(True)
    plt.legend(loc='best')
    plt.title("Anomaly Detection: "+sys.argv[1])
    plt.xlabel("Time Series Graphs")
    plt.ylabel("Canberra Distance")
    savefig(join('png', sys.argv[1]+"_canberra.png"),bbox_inches='tight')

def get_anomalies(dists, up_limit):
    anomalies = []
    for i in range(1, len(dists)-1):
        if abs(dists[i]-dists[i-1]) >= up_limit and \
        abs(dists[i]-dists[i+1]) >= up_limit:
            anomalies.append(i)

    return anomalies

def compare(sigs, use_old_dists):
    """
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

    if not use_old_dists:
        # Verify dimensions, Order all the graphs names based on the timestamp,
        # and Save dists to file
        for g in sigs:
            assert (len(sigs[g])==7*5),"Total features != 7*5"

        ordered_graphs = sorted(sigs.keys(),
                                key=lambda k:int(k.split('_',1)[0]))

        dists = [canberra_dist(sigs[ordered_graphs[i]],
              sigs[ordered_graphs[i-1]]) for i in range(1,len(ordered_graphs))]

        saveDists(ordered_graphs, dists, sys.argv[1]+"_dists.csv")
    else:
        dists = loadDists(sys.argv[1])

    # Calculate Canberra distance threshold
    up_limit = dist_threshold(dists)

    anomalies = get_anomalies(dists, up_limit)
    plot_and_save(dists, up_limit)

    # Starting with the 2nd graph, compute the canberra distance of each
    # graph with the previous one. Compare with threshold value. Append
    # the anomalous grpahs to list anomalies[]

#==============================================================================
# NetSimile algorithm
#==============================================================================
def NetSimile(graph_files, dir_path, use_old_dists=False):
    """
    use_old_dists - if True, then use previously computed values of distances
    """
    start_time = time.time()
    signatures=None
    if not use_old_dists:
        graphs = {f: file2igraph(join(dir_path, f)) for f in graph_files}
        features_all = get_features_all(graphs)
        signatures = aggregator(features_all)

    compare(signatures, use_old_dists)

    print time.time() - start_time, "seconds"
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
    NetSimile(onlyfiles, dir_path, use_old_dists=is_debug)
