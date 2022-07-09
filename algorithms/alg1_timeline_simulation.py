# -*- coding: utf-8 -*-
"""
Created on Thu Jan 20 10:25:12 2022

@author: Mike
"""

def Run_simulation(agents, P_scheme, D, seed, filename="Test_log.csv"):
    
    import numpy as np
    np.random.seed(seed)
    import pandas as pd
    
    from helper_functions import store_evlog, sim_generalized_lognormal
    from Alg2_case_arrival import CaseArrival#, pi_arr, pi_attr#, phi_arrival
    from Alg3_queue_management import QueueManagement
    from Alg4_case_assignment import CaseAssignment
    from Alg5_case_activities import CaseActivities
    
    verbose = False
    
    """
    Generate the agents
    """
    
        
    #agents = 20
    
    Psi = []
    
    # Normal distribution
    agent_personalities = np.random.normal(loc=0.2171,
                         scale=0.5196,
                         size=agents)
    
    for a in range(0,agents):
        psi = {"id":a,
                 "i":[],
                 "q":np.round(a*0.1,decimals=1), # debugging only
                 
                 "personality":agent_personalities[a],
                 
                 "status":None}
        
        Psi.append(psi)


    """
    Generate simulated activities using same seed
    """
    
    states = ["Task-Reminder", "Interaction", "Email", "END"]
    
    p_vectors = {"p0":np.random.choice(states, size=1000000, replace=True, p=[0.0, 0.92, 0.08, 0.0]),
                 "p1":np.random.choice(states, size=1000000, replace=True, p=[0.08, 0.00, 0.67, 0.25]),
                 "p2":np.random.choice(states, size=1000000, replace=True, p=[0.00, 0.02, 0.96, 0.02]),
                 "p3":np.random.choice(states, size=1000000, replace=True, p=[0.00, 0.02, 0.45, 0.53]),
                 "p4":np.random.choice(states, size=1000000, replace=True, p=[0.00, 0.00, 0.00, 1.00]),
                 "c_topic":np.random.choice(list(range(0,10)), size=1000000, replace=True, p=[0.318670,
                                                                                                0.243781,
                                                                                                0.138256,
                                                                                                0.066510,
                                                                                                0.064415,
                                                                                                0.063891,
                                                                                                0.039277,
                                                                                                0.037968,
                                                                                                0.014925,
                                                                                                0.012307])}
        

    """
    Days, case-buffer, case identifier
    """    
    
    L = []
    
    
    """
    Simulate case arrivals throughout the full period
    """
    i = 0
    counter = 0
    Theta, i = CaseArrival(i, D, P_scheme,
                       seed=seed)
    
    
    """
    Generate case database: All cases throughout the simulation period
    """
    Case_DB = pd.DataFrame(pd.DataFrame({'theta_idx':list(range(0,len(Theta))), 
                                         'agent_idx':[None]*len(Theta), 
                                         'arrival_q':[v['q'] for v in Theta], 
                                         "est_throughputtime":[v['est_throughputtime'] for v in Theta], 
                                         "est_NPS":[v['est_NPS'] for v in Theta], 
                                         "est_NPS_priority":[v['est_NPS_priority'] for v in Theta],
                                         #FLAGS
                                         "case_currently_arrived":[False]*len(Theta),
                                         "case_currently_assigned":[False]*len(Theta),
                                         "case_queued":[False]*len(Theta),
                                         "status":["open"]*len(Theta)
                                         #"case_temporal_status":["Future_case"]*len(Theta)
                                         }))
    
    
    """ For each day in the simulation period """
    for d in list(range(0,D)):
        
        if verbose == True:
            print("#"*30)
            
        print("day",str(d),"start")
        
        
        if verbose == True:
            """ DEBUG/verbose ONLY: Update status on newly arrived cases """
            Case_DB["case_currently_arrived"] = Case_DB["arrival_q"] <= d+1
             
            """ Print updated information """
            
            all_cases = len(Case_DB)    
            future_cases = len(Case_DB.loc[np.where((Case_DB['case_currently_arrived']==False))])      
            currently_arrived = len(Case_DB.loc[np.where((Case_DB['case_currently_arrived']==True))])
            cases_assigned = len(Case_DB.loc[np.where(Case_DB['agent_idx'].notnull())]) # & Case_DB["case_temporal_status"] != "Future_case"))
            print("Currently arrived cases (until today):",currently_arrived, "cases assigned:",cases_assigned,"future cases:",future_cases,"all cases:",all_cases)
            
        """ Generate 15-minute increments"""
        minute_intervals = 15
        daily_increment = 1/((60*24)/minute_intervals) #### 15 minute intervals 
        daily_intervals = [daily_increment]*int(((60*24)/minute_intervals)) #12
        
        z = d
        
        """ Queue management, case assignment and activities"""
        for interval in daily_intervals:
            
            """ Update time by 15 minutes """
            z = z + interval
            
            """ Update case database with new cases that have arrived """
            # a case has arrived if its arrival time is before the end of the current window
            Case_DB["case_currently_arrived"] = Case_DB["arrival_q"] <= z
            
            # a case is in the queue if it has currently arrived, and no agent is assigned to it
            Case_DB["case_queued"] = Case_DB["case_currently_arrived"] & Case_DB['agent_idx'].isnull()
            
            """ If there are currently any cases in the queue or being processed """
            queue_size = np.sum(Case_DB["case_queued"]*1)
            open_cases = len(Case_DB.loc[np.where(Case_DB['agent_idx'].notnull())])
            
            if queue_size + open_cases > 0:
                
                """ Sort case order, based on queue priority scheme """        
                Case_DB = QueueManagement(Case_DB, P_scheme, seed=seed)
                
                """ Assign idle agents to newly arrived cases """        
                Case_DB, Theta, Psi = CaseAssignment(Case_DB=Case_DB, 
                                                     Theta=Theta,
                                                     Psi=Psi, 
                                                     verbose=verbose, 
                                                     time_interval = z, seed=seed)
                
                """ Perform activities on the active cases """                    
                L, Case_DB, Theta, Psi, counter = CaseActivities(d, 
                                                        Case_DB, 
                                                        Theta, 
                                                        Psi, 
                                                        L, 
                                                        p_vectors=p_vectors,
                                                        seed=seed,
                                                        start_delays=True, 
                                                        end_delays=True, 
                                                        verbose=verbose, 
                                                        counter=counter)
                
            
    
    """
    Save an event-log
    """
    
    arrived_cases = len(Case_DB)
    
    evlog = store_evlog(Theta, P_scheme, agents, filedest=filename, seed=seed)
    
    return evlog, arrived_cases, Case_DB


#evlog.est_NPS_priority