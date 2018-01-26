# -*- coding: utf-8 -*-
"""
Created on Mon Jan  1 19:11:19 2018

@author: berk
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Jan  1 17:05:59 2018

@author: berk
"""
import csv
import sys
from numpy import genfromtxt
import numpy as np

from scipy.optimize import linprog

from time import time

dist = genfromtxt("mesafe_dist.csv",delimiter=",")

#il_dict_csv = pd.read_csv("il_dict.csv",index_col="iladi")
print("Creating il_dict, later will be used for inputting costs to cost matrix.")
il_dict = {}
with open("il_dict.csv") as il:
    csvFileil = csv.reader(il,delimiter=',')
    for row in csvFileil:
        il_dict[row[1]]=row[0]

#inverse il_dict, will be used later for converting LP solution to a meaningful string for output.
inv_il_dict={}
for il, ind in il_dict.items():
    inv_il_dict[int(ind)] = il

KOMSULAR_DOSYASI = 'komsular.csv'

print("Initialise cost matrix with arbitrarily large numbers.")
neigh_cost = np.empty((81,81))
neigh_cost.fill(999999999)

print("Fill out real distances for neighbouring cities.")
with open(KOMSULAR_DOSYASI) as file:
    csvFile = csv.reader(file, delimiter=',')
    for row in csvFile:
        maincity = row[0]
        for komsu in row:
            if komsu == maincity:
                pass
            else:
                neigh_cost[int(il_dict.get(maincity)),int(il_dict.get(komsu))] = dist[int(il_dict.get(maincity)),int(il_dict.get(komsu))]
        
if __name__ == "__main__":
        
    strt = sys.argv[1]
    end = sys.argv[2]
    #Convert LP to standard form for scipy.linprog(http://www.vision.ime.usp.br/~igor/articles/optimization-linprog.html)
    #Cost vector
    tupledict={}
    t = ()
    c=[]
    print("Constructing cost matrix.")
    for i in range(0,81):
        for j in range(0,81):
            c.append(neigh_cost[i,j])
            t = (i,j)
            tupledict[t]=len(c)-1

    #inverse tupledict, will be used later for converting LP solution to a meaningful string for output.
    inv_tupledict={}
    for tup, ind in tupledict.items():
    	inv_tupledict[ind]=tup        
    
    print("Constructing RHS of constraints matrix.")        
    b=[]
    for i in range(0,81):
        b.append(0)
    
    #change start & end nodes
    b[int(il_dict.get(strt))] = 1
    b[int(il_dict.get(end))] = -1
    
    #construct constraints matrix
    print("Constructing LHS of constraints matrix.")
    for i in range(0,81):
        row_n = [0]*len(c)
        ntl = []
        ptl = []
        nt = ()
        pt = ()
        for ti in range(0,81):
            nt = (i,ti)
            pt = (ti,i)
            ntl.append(nt)
            ptl.append(pt)
        for tup in ntl:
            t=int(tupledict.get(tup))
            row_n[t] = -1
        for tup in ptl:
            t=int(tupledict.get(tup))
            row_n[t] = 1
        
        if i == 0:
            cmat = np.array(row_n).reshape(-1,len(row_n))
        else:
            row_n = np.array(row_n).reshape(-1,len(row_n))
            cmat = np.vstack((cmat,row_n))
    
    c = np.array(c).reshape(-1,len(c)).ravel()
    A = cmat
    b = np.array(b).reshape(-1,len(b)).ravel()
    
    print("Starting LP solver with scipy.")
    t0=time()
    res = linprog(c, A_eq=A, b_eq=b, bounds=(0,1))
    print("Found solution! It took %f, secs to run" %(time()-t0))
    print(res)
    resulting_arr = res.x
    res_ind = np.where(resulting_arr == 1)[0]
    res_tuples = []
    for ind in res_ind:
        res_tuples.append(inv_tupledict.get(ind))
    
    #make directed nodes, may not always work, need to test with different from-to pairs.
    search_str = strt
    ordered_nodes = []
    ctr = 1
    while ctr<len(res_tuples)+1:
        for tup in res_tuples:
            if inv_il_dict.get(tup[1])==search_str:
                ordered_nodes.append(tup[1])
                search_str = inv_il_dict.get(tup[0])
                ctr += 1
    
    dir_nodes = ""
    for i in range(0,len(ordered_nodes)):
        if i == 0:
            dir_nodes = inv_il_dict.get(ordered_nodes[i])
        else:
            dir_nodes += " -->  " + inv_il_dict.get(ordered_nodes[i])
    dir_nodes += " -->  " + end
                
    nodes=[]
    for tup in res_tuples:
        t0=tup[0]
        t1=tup[1]
        nodes.append(inv_il_dict.get(t0))
        nodes.append(inv_il_dict.get(t1))
    nodes = list(set(nodes))
    print("Printing Used Nodes in the solution, list is neither ordered nor clarified as start-end:")
    for nd in nodes:
        print(nd)
    
    print("Printing directed nodes(experimental) for the solution:\n ")
    print(dir_nodes)