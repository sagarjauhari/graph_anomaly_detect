# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 14:42:34 2013

@author: sagar jauhari
"""
import csv

#==============================================================================
# Utility functions
#==============================================================================
def file2igraph(file):
    """
    Converts graph file into iGraph object, adds artifacts
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
        
def saveDists(graph_names, dists, file_name):
    assert (len(graph_names) - len(dists) == 1),\
                "len(graph_names) - len(dists) != 1"
    data = zip([graph_names[1:],dists])
    with open(file_name, 'w') as fo:
        fr = csv.writer(fo)
        fr.write_lines(data)
        