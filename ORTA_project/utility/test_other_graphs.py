# -*- coding: utf-8 -*-
"""
Created on Sun May  2 20:34:33 2021

@author: Raimondo Gallo
"""

import random
import matplotlib.pyplot as plt
import networkx as nx
from utility.mesh_generator import randomMeshGenerator
from utility.person import Person

if __name__ == '__main__':
    # Lattice of NxM
    nodes = random.randint(80,100)
    m = random.randint(5,8)
    
    G2 = nx.random_internet_as_graph(nodes)
    
    plt.figure(figsize=(8,5))
    nx.draw(G2, node_color='lightblue', 
            with_labels=True, 
            node_size=500)