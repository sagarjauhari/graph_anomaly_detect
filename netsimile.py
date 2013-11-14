# -*- coding: utf-8 -*-
"""
Created on Thu Nov 14 13:53:46 2013

@author: Sagar Jauhari
"""
def get_di(node, graph):
    return

def get_ci(node, graph):
    return

def get_dni(node, graph):
    return

def get_cni(node, graph):
    return

def get_eegoi(node, graph):
    return

def get_eoegoi(node, graph):
    return

def get_negoi(node, graph):
    return

def get_nodes(graph):
    return
    
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

def NetSimile(graphs):
    features = get_features_all(graphs)
    signatures = aggregator(features)
    compare(signatures)
    return