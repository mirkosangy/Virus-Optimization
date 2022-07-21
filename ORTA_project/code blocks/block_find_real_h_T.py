# -*- coding: utf-8 -*-

import csv
import pandas as pd
import numpy as np
import pickle
import json
import os
from simulator.simulation import Simulation

# This script finds the real h and T which match the most the chosen characteristics
# of the virus. It takes as parameters the instance (including G and the list of nodes
# populating the graph G), the settings and the chosen degree of the patient zero.

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

# Reading the settings json file for the research of the real h and T.
fp = open(path + '/etc/real_h_T_setting.json', 'r')
real_h_T_setting = json.load(fp)
fp.close()

# Reading the settings json file including the simulation parameters.
fp = open(path +'/etc/simulation_setting.json', 'r')
simulation_setting = json.load(fp)
fp.close()

# Creating a csv file and its header. Each line of the csv file is relative
# to a different simulation characterized with a different triplet (h, T, lambda).
csv_file = cwd +"/csv_folder/block_find_real_h_T.csv"
csv_columns = ["N_nodes", \
               "lambda", \
               "h", \
               "T_max", \
               "total_healthy", \
               "total_contagious", \
               "total_ill", \
               "total_dead", \
               "total_recovered", \
               "contagious_percentage", \
               "ill_percentage", \
               "death_percentage", \
               "avg_iterations_to_die", \
               "diff_contage", \
               "diff_deaths", \
               "sum_of_diffs"]

with open(csv_file, 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
    writer.writeheader()
    
# Create a local Dataframe to store the intermediate results and for
# further analysis.
df = pd.DataFrame(columns = csv_columns)

# Name of the log file.
log_file = "block_find_real_h_T_log"
    
# Launching a simulation letting lambda, h and T vary in the ranges specified 
# in the settings. For each triplet (h, T, lambda) a simulation is launched.
for lambd in real_h_T_setting['lambda_range']:
    for h in real_h_T_setting['h_range']:
        for T in real_h_T_setting["T_max"]:
            pl = pl
            results = Simulation(log_file, real_h_T_setting, lambd, h, T, pl, simulation_setting["SIM_LIM"], patient_zero_degree, False, False)            
            # Appending the intermediate results in a local DF.
            df = df.append(results, ignore_index=True)
            
            # Save the intermediate results of each simulation in the csv file.
            try:
                with open(csv_file, 'a') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
                    writer.writerow(results)
            except IOError:
                print("I/O error")

# Finding the h and T that match the most the chosen virus characteristics.
# The rows of the DataFrame, that provide a gap not higher than 500 from the
# infection and death targets jointly, are considered to discover the real h and T.
# h and T values are evaluated by averaging their values in the selected rows.
dfObj = df.sort_values(by='sum_of_diffs').loc[(df['sum_of_diffs'] >= 0) & (df['sum_of_diffs'] <= 500)]
h = dfObj["h"].mean()
T_max = int(np.ceil(dfObj["T_max"].mean()))

# Saving the Dataframe including the results and variables h and T to be used 
# for the optimal lambda research.
with open('real_h_T.pkl', 'wb') as f:
    pickle.dump([df, h, T_max], f)





