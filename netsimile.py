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

# import local config: Set you local paths in dev_settings.py
DATA_URL=""
SAVE_URL=""
try:
    from dev_settings import *
except:
    pass

#==============================================================================
# Define the 7 feature functions and their helper functions
#==============================================================================
def get_egonet(node, graph):
    return 1

def get_di(node, graph):
    return 2

def get_ci(node, graph):
    return 3

def get_dni(node, graph):
    return 4

def get_cni(node, graph):
    return 5

def get_eegoi(node, graph):
    return 6

def get_eoegoi(node, graph):
    return 7

def get_negoi(node, graph):
    return 8

#==============================================================================
# NetSimile Algorithm
#==============================================================================
def get_nodes(graph):
    pass
    
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
   
    return [(mean(f),
             median(f),
             std(f),
             st.skew(f),
             st.kurtosis(f)) for f in feat_cols]

def aggregator(features_all):
    return {g: get_moments(features_all[g]) for g in features_all}

def compare(sigs):
    """
    input: 7x5 signature matrices for each graph
    output: pairwise comparison of each graph on the basis of signatures
    """
    for g in sigs:
        assert (len(sigs[g])==7),"Total features != 7"
        assert (len(sigs[g][0])==5),"Total moments != 5"
        print "Signature of "+g, sigs[g]

def file2igraph(file):
    """
    Covert graph file into iGraph object, add artifacts
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
            

def NetSimile(graph_files, dir_path):
    #dict of graphs
    graphs = {f: file2igraph(join(dir_path, f)) for f in graph_files}

    #features of all nodes in all graphs
    #format: {g1:[(f1..f7),(f1..f7),(f1..f7)...#nodes], g2:...}
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
