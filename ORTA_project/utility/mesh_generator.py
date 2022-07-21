# -*- coding: utf-8 -*-
"""
Created on Sat May  1 17:46:33 2021

@author: Raimondo Gallo
"""

from itertools import combinations, groupby
import networkx as nx
import random
import matplotlib.pyplot as plt

#this generator will be used to initialize an instance
def randomMeshGenerator(n, p, pl):
    #n is the number of nodes, p is the probability to add an edge, pl is the list of Persons
    """
    Generates a random undirected graph, similarly to an Erdős-Rényi 
    graph, but enforcing that the resulting graph is conneted
    """
    # List of nodes' attributes
    attrs = {}
    # edges contains all the possible combiantions between 2 nodes, 1-2, 1-3...
    # without 1-1, 2-2 or the specular ones, if 1-2 is included, 2-1 isn't.
    edges = combinations(range(n), 2)
    G = nx.Graph()
    G.add_nodes_from(range(n))
    
    '''# To create a graph with a "shell" shape.
    lista = list(range(0,n))
    shells = []
    l1 = []
    l2 = []
    for node in range(round(n/4)):
        a = random.choice(lista)
        l1.append(a)
        lista.remove(a)
    for node in range(round(n/4)):
        a = random.choice(lista)
        l2.append(a)
        lista.remove(a)
    shells = [l1,lista,l2]
    pos = nx.shell_layout(G, shells)
    '''
    # Set the circular shape of the nodes.
    pos = nx.circular_layout(G)
    
    # Adding attributed to the nodes in the graph.
    for node in range(n):
        tmp = {node:{"id":node,"status":"healthy", "pos":pos[node]}}
        attrs.update(tmp)
    nx.set_node_attributes(G, attrs)
    
    if p <= 0:
        return G
    if p >= 1:
        return nx.complete_graph(n, create_using=G)
    for _, node_edges in groupby(edges, key=lambda x: x[0]):
        # nodes_edges is a list conatining all the edges for node 0 like 0-1, 0-2, 0-3 etc.
        # At each iteration of this foor loop, a different node i is considered such that all the
        # edges i-0, i-1 etc are considered.
        node_edges = list(node_edges)
        
        # random_edge is one single random element from the above list.
        random_edge = random.choice(node_edges)
        
        # Here we add a single edge as tuple of two nodes. We do this since in the next for loop
        # the random number might always be over the probability, so we add in advance an edge
        # between two nodes to avoid leaving a node isolated and disconnected.
        # NOTE: if i wanna add a weight to an edge, i have to write 
        # add_edge(*random_edge, weight=w), then i should add this info to the Person object too.
        G.add_edge(*random_edge) # The * means that i add the touple edge (i,j), not a single node.
        
        id = node_edges[0][0] #id of the node we're currently looking at
        edge_node = random_edge[1] #id of the node at the other side of the edge
        #check if the two nodes are not already connected (i.e. they're already neighbours)
        #if they aren't, add them in each other's neighbourhood
        if edge_node not in pl[id].neighborhood and id not in pl[edge_node].neighborhood:
            pl[id].addNeighbor(edge_node)
            pl[edge_node].addNeighbor(id)
            
        # After setting the first edge, add the others in the same way, but with a certain probability p
        # Add edges to a node through the following loop according to a probability.
        for e in node_edges:
            if random.random() < p:
                G.add_edge(*e)
                if e[1] not in pl[id].neighborhood and id not in pl[e[1]].neighborhood:
                    pl[id].addNeighbor(e[1])
                    pl[e[1]].addNeighbor(id)
    return G, pl, pos, attrs
