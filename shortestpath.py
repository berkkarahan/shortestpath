# -*- coding: utf-8 -*-
"""
Created on Sat Dec 30 16:24:12 2017

@author: berk
"""
import csv
import sys
from numpy import genfromtxt
import numpy as np

dist = genfromtxt("mesafe_dist.csv",delimiter=",")

#il_dict_csv = pd.read_csv("il_dict.csv",index_col="iladi")
il_dict = {}

with open("il_dict.csv") as il:
    csvFileil = csv.reader(il,delimiter=',')
    for row in csvFileil:
        il_dict[row[1]]=row[0]

graph_dict = {}
sub_dict = {}
KOMSULAR_DOSYASI = 'komsular.csv'

with open(KOMSULAR_DOSYASI) as file:
    csvFile = csv.reader(file, delimiter=',')
    for row in csvFile:
        maincity = row[0]
        sub_dict = {}
        for komsu in row:
            if komsu == maincity:
                pass
            else:
                sub_dict[komsu] = dist[int(il_dict.get(maincity)),int(il_dict.get(komsu))]
        graph_dict[maincity] = sub_dict
        del sub_dict
        
def shortestpath(graph,start,end,visited=[],distances={},predecessors={}):
    """Find the shortest path between start and end nodes in a graph"""
    # we've found our end node, now find the path to it, and return
    if start==end:
        path=[]
        while end != None:
            path.append(end)
            end=predecessors.get(end,None)
        return distances[start], path[::-1]
    # detect if it's the first time through, set current distance to zero
    if not visited: distances[start]=0
    # process neighbors as per algorithm, keep track of predecessors
    for neighbor in graph[start]:
        if neighbor not in visited:
            neighbordist = distances.get(neighbor,np.inf)
            tentativedist = distances[start] + graph[start][neighbor]
            if tentativedist < neighbordist:
                distances[neighbor] = tentativedist
                predecessors[neighbor]=start
    # neighbors processed, now mark the current node as visited
    visited.append(start)
    # finds the closest unvisited node to the start
    unvisiteds = dict((k, distances.get(k,np.inf)) for k in graph if k not in visited)
    closestnode = min(unvisiteds, key=unvisiteds.get)
    # now we can take the closest node and recurse, making it current
    return shortestpath(graph,closestnode,end,visited,distances,predecessors)

if __name__ == "__main__":
    print(shortestpath(graph_dict,sys.argv[1],sys.argv[2]))
    #c, p = SP2(graph_dict,'Isparta','Antalya')
    #print(c, p)