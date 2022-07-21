# -*- coding: utf-8 -*-
"""
Created on Sun May  2 16:58:09 2021

@author: Raimondo Gallo
"""
import numpy as np
import math

#each node will be a Person
#this class will be used to initialize the instance
class Person:

    def __init__(self, id, a_infect, b_infect, a_death, b_death, lambd, T_max, h):
        #Identifier of the Node/Person in the graph.
        self.id = id
        # Starting state of the Node/Person.
        self.state = "HEALTHY"
        ''' Possible states of a node/Person:
            "HEALTHY"
            "CONTAGIOUS"
            "ILL"
            "RECOVERED"
            "DEAD"
        '''
        # Setting alpha and beta which influence, respectively, the probability to infect p 
        # and probabilitiy to die q.
        self.alpha = np.random.beta(a_infect, b_infect, size=None)
        self.beta = np.random.beta(a_death, b_death, size=None)
        # Probability p to infect neighbors, zero when the person is healthy.
        self.p = 0
        # Probability q to die because of the virus, zero when the person is healthy.
        self.q = 0
        # Lambda for the probabilities p and q.
        self.lambd = lambd
        # Start with an empty neighbourhood.
        self.neighborhood = []
        # Local timestamps to heal.
        self.t = -1
        # Timestamps threshold to heal. 
        self.T_max = T_max
        # Threshold h for viral quantity.
        self.h = h
        # Current viral quantity for the person.
        self.viral_q = 0
    
    # Setting T = 0 when the node/person becomes contagious.
    def setTimestamp(self):
        self.t = 0
        
    # Setting T = 0 when the node/person becomes contagious.
    def addTimestamp(self):
        self.t = self.t + 1
        
    # To change/set the probability p to infect.
    def setP(self):
        self.p = self.alpha*(1 - math.exp(-self.lambd*self.t))
    
    # To change/set the probability q to die because of the virus.
    def setQ(self):
        self.q = self.beta*(1 - math.exp(-self.lambd*self.t))
        
    # To change/set the alpha.
    def setAlpha(self, mean, std):
        self.alpha = np.random.normal(loc=mean, scale=std, size=1)
        
    # To change/set the beta.
    def setBeta(self, mean, std):
        self.beta = np.random.normal(loc=mean, scale=std, size=1)
    
    # To change/set the state that varies according to the situation.
    def setState(self, new_state):
        self.state = new_state
    
    # To set/change the viral quantity of a node/person in a given timestamp.
    def setViralQuantity(self):
        self.viral_q = 1 - math.exp(-self.lambd*self.t)
    
    # To add a neighbour to the Node/Person.
    def addNeighbor(self, neighbour):
        self.neighborhood.append(neighbour)
    
    # To add a penalty to the threshold in case the person goes from contagious to ill.
    def addPenalty(self, penalty):
        self.T_max = self.T_max + penalty
