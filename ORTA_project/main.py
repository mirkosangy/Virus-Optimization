# -*- coding: utf-8 -*-
"""
Created on Sun May  2 17:50:19 2021

@author: Raimondo Gallo
"""
import random
import matplotlib.pyplot as plt
import networkx as nx
import logging
import json
from simulator.instance import Instance

if __name__ == '__main__':
    
    log_name = "./logs/main.log"
    logging.basicConfig(
        filename=log_name,
        format='%(asctime)s %(levelname)s: %(message)s',
        level=logging.INFO, datefmt="%H:%M:%S",
        filemode='w'
        # The format specifies the format of each line of the log, an example is
        # 14:14:27 INFO starting simulation...
    )
    
    # Reading the simulation setting json file.
    fp = open("./etc/sim_setting.json", 'r')
    sim_setting = json.load(fp)
    fp.close()
    
    random.seed(random.randint(1,100))
    #seed = random.randint(1,100)

    # Initializing the instance of the simulation.
    inst = Instance(sim_setting)
        
    # The simulation max duration.
    SIM_LIM = inst.SIM_LIM
    # The list of nodes/people in the graph.
    nodes = inst.person_list
    # The graph.
    G = inst.G
    # Get nodes attributes.
    nodes_attrs = inst.attrs
    # Get nodes positions in the graph.
    pos = inst.pos
    # Plotting the graph.
    color_state_map = {"ILL": 'red', "DEAD": 'black', "RECOVERED": 'blue', "HEALTHY": "green", "CONTAGIOUS": "yellow"}
    # Getting average and std of the graph degree.
    mean_degree, std_degree = inst.getMeanStdGraphDegree()
    
    # To not display the figure.
    plt.ioff()
    fig = plt.figure(figsize=(8,5))
    nx.draw(G, pos=pos, node_color=[color_state_map.get(node.state)
                    for node in nodes], with_labels=True, node_size=500, font_color='white')
    
    # Initializing empty list for contagious and ill nodes.
    contagious_nodes = []
    ill_nodes = []
    dead_nodes = []
    recovered_nodes = []
    
    logging.info(f'{"Starting the simulation..."}')
    # Starting the simulation from t=0.
    for t in range(SIM_LIM):
        
        flag_event = False
        logging.info(f"Timestamp t={t}:")
        # Set the first node as contagious at random, like if we were in t = 0.
        if t == 0:
            contagious_node = random.choice(range(len(nodes)))
            nodes[contagious_node].setState("CONTAGIOUS")
            nodes[contagious_node].addTimestamp()
            nodes[contagious_node].setP()
            nodes[contagious_node].setQ()
            nodes[contagious_node].setViralQuantity()
            contagious_nodes.append(contagious_node)
            
            plt.ioff()
            plt.figure(figsize=(8,5))
            nx.draw(G, pos=pos, node_color=[color_state_map.get(node.state)
                        for node in nodes], with_labels=True, node_size=500, font_color='white')
            plt.savefig(str(t)+'.png')
            
            logging.info(f"Node {contagious_node} is set to CONTAGIOUS.")
            continue
            
        for node in nodes:
            # In case the current node is either healthy, dead or recovered, it cannot infect
            # other nodes, hence we skip this node.
            if node.state == "HEALTHY" or node.state == "DEAD" or node.state == "RECOVERED":
                continue
            # Otherwise, continue.
            elif node.state == "CONTAGIOUS":
                # Updating the p, q, viral quantity and local timestamp of the contagious node/person
                # for the current timestamp.
                node.addTimestamp()
                node.setP()
                node.setQ()
                node.setViralQuantity()
                
                # Once the node is contagious, we have to check whether its neighbors
                # become contagious too or not
                for neighbor in node.neighborhood:
                    # If the node is not already contagious and it gets infected, 
                    # it becomes contagious.
                    if nodes[neighbor].state == "HEALTHY" and random.random() < node.p:
                        # Now that the node/person is contagious its parameters p, q, viral quantity
                        # are initialized
                        nodes[neighbor].setState("CONTAGIOUS")
                        nodes[neighbor].addTimestamp()
                        nodes[neighbor].setP()
                        nodes[neighbor].setQ()
                        nodes[neighbor].setViralQuantity()
                        # We append the new contagious node id to the list.
                        contagious_nodes.append(nodes[neighbor].id)
                        logging.info(f"Node {neighbor} is now CONTAGIOUS, it has been infected by node {node.id}.")
                        flag_event = True
                # If the viral quantity exceedes the threshold, the node becomes ill. We change its
                # state, append its id to the ill list and add a penalty to the timestamps to heal.
                if node.viral_q >= node.h:
                    node.state = "ILL"
                    ill_nodes.append(node.id)
                    node.addPenalty(2)
                    logging.info(f"Node {node.id}'s viral quantity exceeded h, it is now ILL.")
                    flag_event = True
                # if the local timestamp of the node exceeds the threshold T, the node is considered
                # healed, and it's removed from the lists of either contagious or ill nodes.
                elif node.t > node.T_max:
                    node.state = "RECOVERED"
                    recovered_nodes.append(node.id)
                    if node.id in contagious_nodes:
                        contagious_nodes.remove(node.id)
                    if node.id in ill_nodes:
                        ill_nodes.remove(node.id)
                    logging.info(f"Node {node.id} has been countagious for {node.T_max} timestamps, it is now RECOVERED.")
                    flag_event = True
                # Checking if the node can die, if the probability is higher tha its q.
                #elif random.random() < node.q:
                #    node.state = "DEAD"
                #    dead_nodes.append(node.id)
            
            # If the node is ill...
            elif node.state == "ILL":
                node.addTimestamp()
                node.setP()
                node.setQ()
                node.setViralQuantity()
                
                # Checking if the node can die, if the probability is higher tha its q.
                if random.random() < node.q:
                    node.state = "DEAD"
                    dead_nodes.append(node.id)
                    ill_nodes.remove(node.id)
                    contagious_nodes.remove(node.id)
                    logging.info(f"Node {node.id} is DEAD because of the virus.")
                    flag_event = True
                # If the node stays alive for T_max timestamps, it's considered healed and it's removed
                # from the lists of contagious and ill nodes.
                elif node.t > node.T_max:
                    node.state = "RECOVERED"
                    recovered_nodes.append(node.id)
                    if node.id in contagious_nodes:
                        contagious_nodes.remove(node.id)
                    if node.id in ill_nodes:
                        ill_nodes.remove(node.id)
                    logging.info(f"Node {node.id} has been countagious for {node.T_max} timestamps, it is now RECOVERED.")    
                    flag_event = True
        # Just to print something in case of no event occurred during the current timestamp.            
        if flag_event == False:
            logging.info(f'{"No events occurred."}')
        
        

        plt.ioff()
        plt.figure(figsize=(8,5))
        nx.draw(G, pos=pos, node_color=[color_state_map.get(node.state)
                    for node in nodes], with_labels=True, node_size=500, font_color='white')
        plt.savefig(str(t)+'.png')
        
        # If either all the nodes are recovered or all the nodes are dead or all the nodes are 
        # either recovered or dead, stop the simulation; no changes can occur.
        if len(recovered_nodes) == len(nodes) or len(dead_nodes) == len(nodes) or\
            (len(recovered_nodes)+len(dead_nodes)) == len(nodes) or\
                (len(contagious_nodes) == 0 and len(ill_nodes) == 0):
                break
    
    logging.info(f'{"Simulation has ended."}')
    logging.shutdown()
