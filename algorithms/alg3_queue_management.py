# -*- coding: utf-8 -*-
"""
Created on Thu Jan 20 13:34:06 2022

@author: Mike



P_scheme = "FCFS"

Theta = [{'i': 20, 'q': 10.758166076206798, 'c': ['a', 'b', 'c']},
         {'i': 19, 'q': 10.3790830381034, 'c': ['a', 'b', 'c']}]

"""



def QueueManagement(Case_DB, P_scheme, seed=1337):
    """
    Parameters
    ----------
    Theta : TYPE
        DESCRIPTION.
    P_scheme : TYPE
        DESCRIPTION.

    Returns
    -------
    Theta_ordered

    """
    #import numpy as np
    #np.random.seed(seed)
    #import pandas as pd
    
    #sort case db by arrival time
    #Case_DB = Case_DB.sort_values("arrival_q",ascending=True)
    #Case_DB.index = list(range(0,len(Case_DB)))
    
    #Case_DB["queue_order"] = list(range(0,len(Case_DB)))

    """ Only cases that arrived up until time z + 15 is visible """


    """ First-come first served queue management """
    if P_scheme == "FCFS":    
        
        """ Sort cases by their arrival time q"""
        #Theta_ordered = sorted(Theta.copy(), key=lambda d: d['q']) 
        
        #sort case db by arrival time
        Case_DB = Case_DB.sort_values("arrival_q",ascending=True)
        
        #change the index
        Case_DB.index = list(range(0,len(Case_DB)))
        
        #set the queue order (including cases that are not in the queue)
        Case_DB["queue_order"] = list(range(0,len(Case_DB)))

    """ NPS-based queue management """
    if P_scheme == "NPS":
        
        """ If there is a tie, the one that arrived first will get first served """
        
        #sort case db by arrival time
        Case_DB = Case_DB.sort_values("arrival_q",ascending=True)
        Case_DB.index = list(range(0,len(Case_DB)))
        
        #sort case db by NPS_priority
        Case_DB = Case_DB.sort_values("est_NPS_priority",ascending=True)
        Case_DB.index = list(range(0,len(Case_DB)))
        
        #set the queue order (including cases that are not in the queue)
        Case_DB["queue_order"] = list(range(0,len(Case_DB)))
        
    # id variable for later use in case assignment
    Case_DB["casedb_idx"] = list(range(0,len(Case_DB)))
    
    return Case_DB

