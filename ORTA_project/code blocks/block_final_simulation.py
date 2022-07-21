# -*- coding: utf-8 -*-

import csv
import pandas as pd
import pickle
import os
import json
from simulator.simulation import final_simulation

# This script, given the real h and T and optimal lambda, observes the behaviour 
# of the network. It returns two DataFrames, one containing the statistics of the
# final simulation, the other the evolution over time of the simulation in order to plot it.

# Get main script path on local machine.
cwd = os.path.dirname(os.path.realpath(__file__))
path = os.path.dirname(cwd)

# The patient zero degree is set to "MEDIUM" by default, it can changes here.
patient_zero_degree = "MEDIUM"
first_node = None

# Reading the saved variables G, which includes the stochastic graph, and 
# pl which is the list of the nodes, each one characterized by its own parameters.
f = open(path +'/instance.pkl', 'rb')
G, pl,= pickle.load(f)
f.close()

# Reading the saved variables real h and T.
f = open(cwd +'/real_h_T.pkl', 'rb')
df_real_h_T, h_real, T_max_real= pickle.load(f)
f.close()

# Reading the saved variable lambda optimal.
f = open(cwd +'/optimal_lambda.pkl', 'rb')
df_opt_lambda, lambd= pickle.load(f)
f.close()

# Reading the settings json file including the simulation parameters.
fp = open(path +'/etc/simulation_setting.json', 'r')
simulation_setting = json.load(fp)
fp.close()


# Create csv file and its header.
csv_file = cwd +"/csv_folder/block_final_network_behaviour.csv"
csv_columns = ["N_nodes", \
               "lambda", \
               "h", \
               "T_max", \
               "total_healthy", \
               "total_contagious", \
               "total_ill", \
               "total_dead", \
               "total_recovered"]

with open(csv_file, 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
    writer.writeheader()
    
# Create a local Dataframe to store the simulation results, in particular,
# the amount of healthy, contagious, ill, dead and recovered nodes.
df_final_results = pd.DataFrame(columns = csv_columns)

# Name of the log file.
log_file = "block_final_network_behaviour_log"

# Launching the final simulation.
pl = pl
results, df_plot = final_simulation(log_file, lambd, h_real, T_max_real, pl, simulation_setting["SIM_LIM"], patient_zero_degree, first_node)
df_final_results = df_final_results.append(results, ignore_index=True)

# Saving the csv file.
try:
    with open(csv_file, 'a') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writerow(results)
except IOError:
    print("I/O error")

# Saving the Dataframe including the results and variable to be used 
# in the final simulation, together with the variables
# h and T previously discovered.
with open('final_simulation.pkl', 'wb') as f:
    pickle.dump([df_final_results], f)
