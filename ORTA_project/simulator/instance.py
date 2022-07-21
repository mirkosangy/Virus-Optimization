# -*- coding: utf-8 -*-
import logging
import random
import math
import matplotlib as plt
import networkx as nx
from utility.mesh_generator import randomMeshGenerator
from utility.person import Person

#this class is used to generated a random graph: it is called once before running the simulation
class Instance():
    def __init__(self, sim_setting): #initialization starting from the chosen params
        
        self.nodes = random.randint(sim_setting['min_N_nodes'], sim_setting['max_N_nodes'])
        self.probability = sim_setting['edge_probability']
        self.degree_mean = 0
        self.degree_std = 0
        pl = []
        # Initialize the Person (nodes) objects.
        for node in range(self.nodes):
            pl.append(Person(node, \
                             sim_setting['infecting_P_a'], \
                             sim_setting['infecting_P_b'], \
                             sim_setting['death_P_a'], \
                             sim_setting['death_P_b'], \
                             sim_setting['lambda'], \
                             sim_setting['T_max'], \
                             sim_setting['viral_quantity_max']))
                
        self.G, self.person_list, self.pos, self.attrs = randomMeshGenerator(self.nodes, self.probability, pl) 
        self.SIM_LIM = sim_setting['SIM_LIM']
        
        # Adding the parameters drawn values to the log file of the main.
        logging.info("Parameters of the simulation:")
        logging.info(f"n_nodes: {self.nodes}")
        logging.info(f"edge_probability: {self.probability}")
        logging.info(f"lambda: {sim_setting['lambda']}")
        logging.info(f"T: {sim_setting['T_max']}")
        logging.info(f"h: {sim_setting['viral_quantity_max']}")
        logging.info(f"SIM_LIM: {self.SIM_LIM}")
    
    def getNodesPosition(self): #this method returns the position of all the nodes
        return self.pos
    
    def getGraph(self): #generate graph from the info stores in the logfile
        logging.info("getting graph from instance...")
        return self.G
    
    def getPeople(self):
        logging.info("getting population of the graph from instance...")
        return self.person_list
    
    # To evaluate average and standard deviation of the node degree for the whole graph. 
    def getMeanStdGraphDegree(self):
        logging.info("getting mean and std of the node graph degree from instance...")
        tot = 0
        for person in self.person_list:
            tot = tot + len(person.neighborhood)
        self.degree_mean = round(tot / len(self.person_list),2)
        tot = 0
        for person in self.person_list:
            tot = tot + abs(pow(len(person.neighborhood) - self.degree_mean, 2))
        self.degree_std = round(math.sqrt(tot/self.nodes),2)
        '''
        #(maybe we can test these options with the one implemented to see if they give the same results and, in case, choose what we prefer)
        self.degree_mean = round(sum(self.G.degree().values())/float(len(G)), 2) #average of the node degree
        len(person.neighborhood)=>G.degree(id) #to use when computing standard deviation of the node degree
        '''
        logging.info(f"Graph degree average: {self.degree_mean}")
        logging.info(f"Graph degree std: {self.degree_std}")
        return self.degree_mean, self.degree_std
    
    def getSimulationDuration(self):
        logging.info("getting duration of the simulation from instance...")
        return self.SIM_LIM
    
    def plotGraph(self):
        plt.figure(figsize=(8,5))
        nx.draw(self.G, 
                node_color='lightblue', 
                with_labels=True, 
                node_size=500)
