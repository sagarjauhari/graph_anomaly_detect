# -*- coding: utf-8 -*-
"""
Created on Thu Nov 14 13:53:46 2013
@author: Sagar Jauhari
"""
import scipy.stats as st

# import local config
DATA_URL=""
SAVE_URL=""
try:
    from dev_settings import *
except:
    pass

#==============================================================================
# Define the 7 feature functions
#==============================================================================
def get_di(node, graph):
    pass

def get_ci(node, graph):
    pass

def get_dni(node, graph):
    pass

def get_cni(node, graph):
    pass

def get_eegoi(node, graph):
    pass

def get_eoegoi(node, graph):
    pass

def get_negoi(node, graph):
    pass

#==============================================================================
# NetSimile Algorithm
#==============================================================================
def get_nodes(graph):
    pass
    
def get_features(g):
    v = get_nodes(g)
    return [(get_di(i,g), 
             get_ci(i,g), 
             get_dni(i,g),
             get_cni(i,g),
             get_eegoi(i,g),
             get_eoegoi(i,g),
             get_negoi(i,g)) for i in v]

def get_features_all(graphs):
    return [get_features(g) for g in graphs]

def get_moments(feat):
    """
    input: feature matrix of a single graph
    output: for each feature, return the 5 moments
    """
    feat_cols = zip(*feat)
    assert (len(feat_cols)==7),"Total columns != 7"
    assert (len(feat_cols[0])==5),"Total moments !=5"
    
    return [(mean(f),
             median(f),
             std(f),
             st.skew(f),
             st.kurtosis(f)) for f in feat_cols]

def aggregator(features_all):
    return [get_moments(feat) for feat in features_all]

def compare(sigs):
    """
    input: 7x5 signature matrices for each graph
    output: pairwise comparison of each graph on the basis of signatures
    """
    pass

def NetSimile(graphs):
    features_all = get_features_all(graphs)#features of all nodes in all graphs
    signatures = aggregator(features_all)  #signature of all graphs
    compare(signatures)
    return
    