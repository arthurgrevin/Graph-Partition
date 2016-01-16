__author__ = 'pascal'

import networkx as nx
import matplotlib.pyplot  as plt
import random as rd
from gurobipy import *


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



G = parse_graph("bigraph")
X = {}
Edges = {}

Arrete = {}
K = 2

m = Model()

print("List des arrêtes : " )
print("Declaration des variables")


for node in G.nodes():
    X[node] = m.addVar(vtype=GRB.BINARY)


for (x,y) in G.edges():
    print("Ajout : {}".format((x,y)))
    #Arrete[(x,y)] = m.addVar(vtype=GRB.BINARY)
    Edges[(x,y)] = m.addVar(vtype=GRB.BINARY)


    print("Ajout : {}".format((y,x)))
    #Arrete[(y,x)] = m.addVar(vtype=GRB.BINARY)
    Edges[(y,x)] = m.addVar(vtype=GRB.BINARY)



'''
for x in G.nodes():
    for y in G.nodes():
        if(x != y and Edges.has_key((x,y)) == False and Edges.has_key((y,x)) == False):
            print("Add {}{}".format(x,y))
            Edges[x,y] =  m.addVar(vtype=GRB.BINARY)

            print("Add {}{}".format(y,x))
            Edges[y,x] =  m.addVar(vtype=GRB.BINARY)
'''
m.update()


m.setObjective(quicksum(Edges.values()),GRB.MAXIMIZE)
#m.setObjective(quicksum(Arrete.values()), GRB.MAXIMIZE)


'''
for key in Arrete.keys():
    m.addConstr(Edges[key] - Arrete[key], "==", 0)
'''


for (x,y) in Edges.keys():
    v1 = Edges[x,y]
    v2 = Edges[y,x]
    m.addConstr(v1 - v2, "==", 0)

print("---")
print("Contrainte triangulaires")
for i in G.nodes():
    for j in G.nodes():
        for k in G.nodes():
            if(Edges.has_key((i,j)) and Edges.has_key((j,k)) and Edges.has_key((i,k))):

                Xij = Edges[i,j]
                Xjk = Edges[j,k]
                Xik = Edges[i,k]

                L1 = LinExpr([1,1,-1],[Xij,Xjk,Xik])
                m.addConstr(L1, ">", 0)
                print("Ajout : X{}{} + X{}{} > X{}{}".format(i,j,j,k,i,k))

                L2 = LinExpr([1,1,-1],[Xjk,Xik,Xij])
                m.addConstr(L2, ">", 0)
                print("Ajout : X{}{} + X{}{} > X{}{}".format(j,k,i,k,i,j))

                L3 = LinExpr([1,1,-1],[Xik,Xij,Xjk])
                m.addConstr(L3, ">", 0)
                print("Ajout : X{}{} + X{}{} > X{}{}".format(i,k,i,j,j,k))
                print(' ')




print("Contrainte d'existence")
for x1 in X:
    #sum = quicksum(Edges[(x,y)] for (x,y) in Edges.keys() if (y < x and x == x1))

    exists_lower = False
    sum = 0
    print("---")
    print("X{} +".format(x1))
    for(x,y) in Edges.keys():
        if(y<x and x1 == x):
            exists_lower = True
            #print("Y : {} X : {} X1 : {}".format(y,x,x1))
            print("X{}{} + ".format(x,y))
            sum += Edges[(x,y)]

    print(">= 1")

    #print("Sum : {}".format(sum))

    if(exists_lower == False):
        m.addConstr(X[x], ">=", 1)
        print("Constraint: {}    >= 1".format(X[x]))

    else:
        #L1 = LinExpr([1,1],[X[x],sum])

        L1 = X[x] + sum
        print("Constraint: {}   >= 1".format(L1))
        m.addConstr(X[x] + sum, ">=", 1)
    #m.addConstr(X[x], ">=",1-sum)
    #print("Ajout : ")
    print("---")


for x1 in X:
    print("---")
    for (x,y) in Edges.keys():
       #print y
        if(x>y and x1 == x):
            print(" X{} + X{}{} <= 1".format(x1,x,y))
            var = Edges[(x,y)]
            #print [X[x],var]
            L1 = LinExpr([1,1],[X[x],var])
            print(L1)
            m.addConstr(L1,"<=",1)
print("---")

m.addConstr(quicksum(X.values()), "==" , 2 )




m.optimize()


