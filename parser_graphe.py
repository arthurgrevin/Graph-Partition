# -*- coding: utf-8 -*-
"""
Created on Fri Nov 20 00:22:25 2015

@author: Arthur
"""

import networkx as nx

import matplotlib.pyplot  as plt
G = nx.Graph()

fichier = open("add20.graph","r")

a = fichier.readline()
a.replace("\n","")
nb_nodes = a.split(' ')[0]


G.add_nodes_from(range(1,int(nb_nodes)+1))
print G.nodes()

i=1

for line in fichier.readlines():
    for node in line.split(' '):
        if node.strip() :
            print i
            print int(node)
            G.add_edge(i,int(node))
    i=i+1
print G.edges()

pos=nx.spring_layout(G)
colors=range(20)
nx.draw(G,pos,node_color='#A0CBE2',edge_color=colors,width=4,edge_cmap=plt.cm.Blues,with_labels=False)

plt.savefig("add20.png")

print "fin process"


