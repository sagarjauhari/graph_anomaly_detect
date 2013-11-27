# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 14:42:34 2013

@author: sagar jauhari
"""
import csv
from igraph import *
from os.path import join

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
    data = zip(graph_names[1:],dists)
    with open(join("out",file_name), 'w') as fo:
        fr = csv.writer(fo)
        fr.writerows(data)

def loadDists(name):
    with open(join('out',name+"_dists.csv")) as fi:
        fr = csv.reader(fi, delimiter=',')
        data=list(fr)
    return [float(i[1]) for i in data]

def saveAnomalies(lim_up, lim_down, dists, anomalies):
    """
    Writes to disk the anomalies in the defined format.
    """
    with open(join('out',sys.argv[1]+'_anomalies.txt'), 'w') as fo:
        fo.write(str(lim_up)+' '+str(lim_down)+'\n')
        for a in anomalies:
            fo.write(str(a)+' '+str(dists[a-1]) +' ' + str(dists[a])+'\n')
