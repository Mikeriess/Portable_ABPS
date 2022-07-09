from helper_functions import *
import numpy as np
import pandas as pd


#Simple setup for testing purposes:
Settings = {'F_priority_scheme':["FCFS","NPS"],#,"NPS"],     #
            "days":[365],#,365],
            'F_number_of_agents':[#1,
                                  #3,
                                  3, 
                                  5, 
                                  10, 
                                  15], 
                                  #25, 
                                  #30, 
                                  #35], 
                                  #40],   #
            'Repetition':list(range(0,10))}                #

# Generate a full factorial:
df=build_full_fact(Settings)  


# Constants affecting the experiments:
df["Done"] = 0 #Flag if the final model has been trained
#df["Simulation_duration_sec"] = 0.0


df["RUN"] = df.index + 1
#df["Done"] = 0

print(df)

# Save the settings to a file
np.save('C:/Users/Mike/Norwegian University of Life Sciences\Joachim Scholderer - Teaching/PhD Mike/Papers/CRM process improvement paper (In progress)/Data/Simulation_results/Experiment_Settings.npy', Settings) 
#np.save('E:/CRM_paper/Experiment_Settings.npy', Settings) 
np.save('Experiment_Settings.npy', Settings) 

#store the new experimental design
df.to_csv("Experiments.csv", index=False)
#df.to_csv("E:/CRM_paper/Experiments.csv", index=False)
df.to_csv("C:/Users/Mike/Norwegian University of Life Sciences\Joachim Scholderer - Teaching/PhD Mike/Papers/CRM process improvement paper (In progress)/Data/Simulation_results/Experiments.csv", index=False)