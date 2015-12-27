# -*- coding: utf-8 -*-
"""
Created on Fri Nov 20 00:22:25 2015

@author: Arthur
"""

import networkx as nx

import matplotlib.pyplot  as plt
import random as rd


def draw_bipartite_graph(G,P1,P2,file_name,title):
    print("Drawing graph")
    plt.figure(figsize=(8,6))
    plt.title(title)
    pos=nx.spring_layout(G)
    nx.draw_networkx_nodes(G,pos,nodelist=P1,node_size=10, node_color='b')
    nx.draw_networkx_nodes(G,pos,nodelist=P2, node_size=10, node_color='r')

    nx.draw_networkx_edges(G,pos,alpha=0.7)
    #draw labels
    #nx.draw_networkx(G,pos, alpha=0,with_labels = True, font_size = 25)

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
                G.add_edge(i,int(node),weight=rd.random())
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
        Iterated = [starting_node]
        while(x < len(last_successors) and found == False):
        #for x in last_successors:
            #print("Iterating on node : {} ".format(last_successors[x]))
            succesors = T.successors(last_successors[x])
            #print len(succesors)

            #has only one neighboor
            if len(G.edge[last_successors[x]].keys()) == 1:
                found = True
                starting_point = last_successors[x]
                print "New starting point : {}".format(starting_point)
            new_succesors.extend(succesors)
            x = x + 1
        last_successors = new_succesors
        Iterated.extend(last_successors)
        x = 0

        if len(Iterated) >= G.number_of_nodes():
            print("Iterated over all nodes, no node with only one neighboor")





    print("Launching greedy algorithm")
    T = nx.bfs_tree(G,starting_point)
    P1 = [starting_point]
    last_successors = [starting_point]


    I = 0
    while len(P1) <= (G.number_of_nodes()/2):
        new_succesors = []
        #print "Current partition : {}".format(P1)
        for x in last_successors:
            new_succesors.extend(T.successors(x))

        P1.extend(new_succesors)
        #print len(P1)
        I = I+1
        #print("Step {}".format(I))

        last_successors = new_succesors


    print "Reconstructing second partition"
    P2 = G.nodes()
    for x in P1:
        P2.remove(x)

    print "Size of first partition : {}".format(len(P1))
    print "Size of second partition : {}".format(len(P2))
    print "Size of graph : {}".format(G.number_of_nodes())
    print"Number of edges : {}".format(G.number_of_edges())
    return P1,P2,starting_point




#take A and B lists of nodes in partitions and return the cost of the slice in graph G (total sum of wieghts)
def cost_slice(A,B,G):
    L = []
    result = 0
    for x in A:
        for y in B:
            node = G.get_edge_data(x,y)
            if node != None:
                L.append((x,y))
                result += node["weight"]
                #print(result)
    #print("global cost of slice : {}".format(result))
    #print("List : {}".format(L))
    return L,result




G = parse_graph("uk.graph")

P1,P2,starting_point = greedy(G,1)
L, cost = cost_slice(P1,P2,G)
print("Cost of the slice : {}".format(cost))
title = "UK Starting point : {} P1 : {} P2 : {} Cost : {}".format(starting_point, len(P1), len(P2),cost)
draw_bipartite_graph(G,P1,P2,"uk_start_1",title)

P1,P2,starting_point = greedy(G,500)
L, cost = cost_slice(P1,P2,G)
print("Cost of the slice : {}".format(cost))
title = "UK Starting point : {} P1 : {} P2 : {} Cost : {}".format(starting_point, len(P1), len(P2),cost)
draw_bipartite_graph(G,P1,P2,"uk_start_500",title)

P1,P2,starting_point = greedy(G,1000)
L, cost = cost_slice(P1,P2,G)
print("Cost of the slice : {}".format(cost))
title = "UK Starting point : {} P1 : {} P2 : {} Cost : {}".format(starting_point, len(P1), len(P2),cost)
draw_bipartite_graph(G,P1,P2,"uk_start_1000",title)

P1,P2,starting_point = greedy(G,1500)
L, cost = cost_slice(P1,P2,G)
print("Cost of the slice : {}".format(cost))
title = "UK Starting point : {} P1 : {} P2 : {} Cost : {}".format(starting_point, len(P1), len(P2),cost)
draw_bipartite_graph(G,P1,P2,"uk_start_1500",title)


P1,P2,starting_point = greedy(G,2000)
L, cost = cost_slice(P1,P2,G)
print("Cost of the slice : {}".format(cost))
title = "UK Starting point : {} P1 : {} P2 : {} Cost : {}".format(starting_point, len(P1), len(P2),cost)
draw_bipartite_graph(G,P1,P2,"uk_start_2000",title)



print "fin process"


