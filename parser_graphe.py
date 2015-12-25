# -*- coding: utf-8 -*-
"""
Created on Fri Nov 20 00:22:25 2015

@author: Arthur
"""

import networkx as nx

import matplotlib.pyplot  as plt



def draw_bipartite_graph(G,P1,P2,file_name):
    print("Drawing graph")
    plt.figure(figsize=(8,6))
    pos=nx.spring_layout(G)
    nx.draw_networkx_nodes(G,pos,nodelist=P1,node_size=10, node_color='b')
    nx.draw_networkx_nodes(G,pos,nodelist=P2, node_size=10, node_color='r')
    nx.draw_networkx_edges(G,pos,alpha=0.7)
    plt.axis('off')
    plt.savefig(file_name)






def parse_graph(file):
    G = nx.Graph()
    fichier = open(file,"r")

    a = fichier.readline()
    a.replace("\n","")
    nb_nodes = a.split(' ')[0]



    print "Parsing graph"
    G.add_nodes_from(range(1,int(nb_nodes)+1))
    #print G.nodes()

    i=1

    for line in fichier.readlines():
        for node in line.split(' '):
            if node.strip() :
                #print i
                #print int(node)
                G.add_edge(i,int(node))
        i=i+1
    return G





def greedy(G,starting_node):
    print "Launching first bfs in order to find an end point to start greedy algorithm"

    N = starting_node
    T = nx.bfs_tree(G,starting_node)
    last_successors = [starting_node]

    found = False
    starting_point = 0

    while found == False:
        new_succesors = []
        x = 0
        while(x < len(last_successors) and found == False):
        #for x in last_successors:
            #print("Iterating on node : {} ".format(last_successors[x]))
            succesors = T.successors(last_successors[x])
            #print len(succesors)
            if(len(succesors) == 0):
                found = True
                starting_point = last_successors[x]
                print "New starting point : {}".format(starting_point)
            new_succesors.extend(succesors)
            x = x + 1
        last_successors = new_succesors
        x = 0


    print("Launching greedy algorithm")
    T = nx.bfs_tree(G,starting_point)
    P1 = [starting_point]
    last_successors = [starting_point]


    I = 0
    while len(P1) <= (G.number_of_nodes()/2):
        new_succesors = []
        for x in last_successors:
            new_succesors.extend(T.successors(x))

        P1.extend(new_succesors)
        #print len(P1)
        I = I+1
        print("Step {}".format(I))

        last_successors = new_succesors


    print "Reconstructing second partition"
    P2 = G.nodes()
    for x in P1:
        P2.remove(x)

    print "Size of first partition : {}".format(len(P1))
    print "Size of second partition : {}".format(len(P2))
    print "Size of graph : {}".format(G.number_of_nodes())
    print"Number of edges : {}".format(G.number_of_edges())
    return P1,P2



G = parse_graph("uk.graph")
P1,P2 = greedy(G,1)
draw_bipartite_graph(G,P1,P2,"uk_start1.png")




print "fin process"


