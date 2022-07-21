# -*- coding: utf-8 -*-

import csv
import pandas as pd
import os
import pickle
import json
from simulator.simulation import Simulation

# This script, given the real h and T, finds the optimal lambda in such way that
# the death rate among ill nodes is maximized. The optimal lambda value is returned.

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

# Reading the saved variables real h and T to further investigate lamnda optimal.
f = open(cwd +'/real_h_T.pkl', 'rb')
df, h_real, T_max_real= pickle.load(f)
f.close()

# Reading the settings json file including the simulation parameters.
fp = open(path +'/etc/simulation_setting.json', 'r')
simulation_setting = json.load(fp)
fp.close()

# Reading the settings json file for the research of the real h and T.
fp = open(path + '/etc/best_lambda_setting.json', 'r')
best_lambda_settings = json.load(fp)
fp.close()

# Create csv file and its header. Each line of the csv file is relative
# to a different simulation characterized with a different triplet (h, T, lambda).
csv_file = cwd +"/csv_folder/block_lambda_search.csv"
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
    
# Create a local Dataframe to store the intermediate results and for
# further analysis.
df = pd.DataFrame(columns = csv_columns)

# Name of the log file.
log_file = "block_lambdasearch_log"

# Given h and T real, the behaviour of the simulation for varying lambda
# (which changes in the range specified in the settings) is studied.
for lambd in best_lambda_settings["lambda_range"]:
    pl = pl
    results = Simulation(log_file, best_lambda_settings, lambd, h_real, T_max_real, pl, simulation_setting["SIM_LIM"], patient_zero_degree, first_node, True, False)
    # Appending the intermediate results in a local DF.
    df = df.append(results, ignore_index=True)
    
    # Save the intermediate results of each simulation in the csv file.
    try:
        with open(csv_file, 'a') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writerow(results)
    except IOError:
        print("I/O error")

# Select the lambda that caused more deaths.
lambda_opt = df[df.total_dead == df.total_dead.max()]["lambda"].to_numpy()[0]

# Saving the Dataframe including the results and variable to be used 
# in the final simulation, together with the variables
# h and T previously discovered.
with open('optimal_lambda.pkl', 'wb') as f:
    pickle.dump([df, lambda_opt], f)

