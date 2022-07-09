# -*- coding: utf-8 -*-
"""
Created on Thu Jan 20 11:06:14 2022

@author: Mike
"""


import numpy as np
#np.random.seed(1337)
import pandas as pd

"""
def pi_arr(z):
    
    features = [1,1,1]
    
    return features

def pi_attr():
    c = ["a","b","c"]
    
    return c

def phi_arrival():
    return
"""

def CaseArrival(i, D, P_scheme, 
                       seed):
    
    def predict_RT_NPS_Notopic(sigma):
         
        import numpy as np
        np.random.seed(seed)
        #import pandas as pd
        #from mpmath import gamma
        
        
        
        """
        ################################################
        Remaining time prediction 
        ################################################
        """
        
        # get features 
    
        dt = sigma["q_dt"]
        
        # #np.mod(z,7)
        day = dt.day
        
        year = dt.year
        month = dt.month
        weekday = dt.weekday()
        hour = dt.hour
        
        # predict throughput time from scoring equation
        
        betas = [-0.02950, #year
                 -0.04149, #month
                 -0.00034, #weekday
                  0.06511] #hour
        
        X = [year,
             month,
             weekday,
             hour]
        
        c = 66.80872
        
        
        #prediction expression (-1 since original target is +1)
        y = np.exp(c + np.dot(X,betas))-1
        
        #simulation expression
        #scale = 2.2944
        # y = np.random.normal(loc=linear_comb,
        #                      scale=scale,
        #                      size=1)[0]
        
        #convert from minutes to days
        y = y/60/24 
        
        # update case with estimated throughput time
        sigma["est_throughputtime"] = y
        
        """
        ################################################
        NPS score prediction 
        ################################################
        """
        
        # get features
        log_throughputtime = np.log(1+y)
   
        # model params
        intercept = 10.221063
        #scale = 1.3378604
        
        #coefficients
        betas = [-0.094867]
        
        #inputs
        X =[log_throughputtime]
        
       
        #prediction equation
        NPS = intercept + np.dot(X, betas)
        
        # update case with estimated throughput time
        sigma["est_NPS"] = NPS
        
        # update weighted NPS_priority:
        NPS_priority = np.abs(NPS-7.5)
        sigma["est_NPS_priority"] = NPS_priority
        
        return sigma
    
    def predict_RT_NPS(sigma):
         
        import numpy as np
        np.random.seed(seed)
        #import pandas as pd
        #from mpmath import gamma
        
        date_and_time = sigma["q_dt"]
        case_topicidx = sigma["c_topic"]
        
         # Inputs for case arrival model
        hour = date_and_time.hour
        weekday = date_and_time.weekday() #np.mod(z,7)
        month = date_and_time.month
        day = date_and_time.day
        year = date_and_time.year
        
         #define list of case topics in indexed order
        case_topics = ["j_1",
                       "z_3",
                       "q_3",
                       "z_2",
                       "r_2",
                       "z_4",
                       "d_2",
                       "w_2",
                       "g_1",
                       "w_1"]
        
        #get casetopic as string
        casetopic = case_topics[case_topicidx]
        
        #case topic conditional coefficients from the model
        
        
        if casetopic == "d_2":
            d_2 = 0
            g_1 = 0
            j_1 = 1
            q_3 = 0
            r_2 = 0
            w_1 = 0
            w_2 = 0
            z_2 = 0
            z_3 = 0
            z_4 = 0
         
        if casetopic == "g_1":
            d_2 = 0
            g_1 = 1
            j_1 = 0
            q_3 = 0
            r_2 = 0
            w_1 = 0
            w_2 = 0
            z_2 = 0
            z_3 = 0
            z_4 = 0
            
        if casetopic == "j_1":
            d_2 = 0
            g_1 = 0
            j_1 = 1
            q_3 = 0
            r_2 = 0
            w_1 = 0
            w_2 = 0
            z_2 = 0
            z_3 = 0
            z_4 = 0
            
        if casetopic == "q_3":
            d_2 = 0
            g_1 = 0
            j_1 = 0
            q_3 = 1
            r_2 = 0
            w_1 = 0
            w_2 = 0
            z_2 = 0
            z_3 = 0
            z_4 = 0
            
        if casetopic == "r_2":
            d_2 = 0
            g_1 = 0
            j_1 = 0
            q_3 = 0
            r_2 =1
            w_1 = 0
            w_2 = 0
            z_2 = 0
            z_3 = 0
            z_4 = 0
            
        if casetopic == "w_1":
            d_2 = 0
            g_1 = 0
            j_1 = 0
            q_3 = 0
            r_2 = 0
            w_1 = 1
            w_2 = 0
            z_2 = 0
            z_3 = 0
            z_4 = 0
            
        if casetopic == "w_2":
            d_2 = 0
            g_1 = 0
            j_1 = 0
            q_3 = 0
            r_2 = 0
            w_1 = 0
            w_2 = 1
            z_2 = 0
            z_3 = 0
            z_4 = 0
            
        if casetopic == "z_2":
            d_2 = 0
            g_1 = 0
            j_1 = 0
            q_3 = 0
            r_2 = 0
            w_1 = 0
            w_2 = 0
            z_2 = 1
            z_3 = 0
            z_4 = 0
            
        if casetopic == "z_3":
            d_2 = 0
            g_1 = 0
            j_1 = 0
            q_3 = 0
            r_2 = 0
            w_1 = 0
            w_2 = 0
            z_2 = 0
            z_3 = 1
            z_4 = 0
            
        if casetopic == "z_4":
            d_2 = 0
            g_1 = 0
            j_1 = 0
            q_3 = 0
            r_2 = 0
            w_1 = 0
            w_2 = 0
            z_2 = 0
            z_3 = 0
            z_4 = 1
            
        
        """
        ################################################
        Remaining time prediction 
        ################################################
        """
            
        # model params
        intercept = 139.3817
      
        #coefficients
        betas = [-0.0654, #year
                 -0.0495, #month
                 0.0077, #day
                 0.0197, #weekday
                 0.0602, #hour   
                 
                 -0.3368, #d2
                 0.0, #g1
                 -1.2246, #j1
                 0.2251, #q3
                 1.1927, #r2
                 -1.1476, #w1
                 0.2342, #w2
                 -0.1040, #z2
                 0.1695, #z3
                 0.0 #z4
                 ]
        
        #inputs
        X = [year,
             month,
             day,
             weekday,
             hour,
                 d_2,
                g_1,
                j_1,
                q_3,
                r_2,
                w_1,
                w_2,
                z_2,
                z_3,
                z_4]
        
        #residuals (exponential regression)
        #residual = -np.log(1-uniform_values[step])
            
        #prediction equation
        y = np.exp(intercept + np.dot(X,betas)) #*residual
            
        
        #convert from minutes to days
        y = y/60/24 
        
        # update case with estimated throughput time
        sigma["est_throughputtime"] = y
        
        
        """
        ################################################
        NPS score prediction 
        ################################################
        """
        
        # get features
        log_throughputtime = np.log(1+y)
   
        # model params
        intercept = 2.300587
        gammascale = 1.300057
        
        #normalscale = 2.3027043599
        
        #coefficients
        betas = [-0.0098232, #log_throughputtime
                 -0.12910, #d2
                 0.100756, #g1
                 0.085297, #j1
                 -0.042748, #q3
                 -0.031668, #r2
                 0.0, #w1
                 0.0, #w2
                 0.09665, #z2
                 -0.00047, #z3
                 0.0 #z4
                 ]
        
        #inputs
        X = [log_throughputtime,
                 d_2,
                g_1,
                j_1,
                q_3,
                r_2,
                w_1,
                w_2,
                z_2,
                z_3,
                z_4]
                    
        #prediction equation
        NPS = np.exp(intercept + np.dot(X,betas))/gammascale
        
        # update case with estimated throughput time
        sigma["est_NPS"] = NPS
        
        # update weighted NPS_priority:
        NPS_priority = np.abs(NPS-7.5)
        sigma["est_NPS_priority"] = NPS_priority
        
        return sigma
    
    
    import datetime
    
    date_and_time  = datetime.datetime(2018, 7, 1, 0, 0, 0)
    print(date_and_time )
    
    q = 0
    z = 0

    M = []
    
    """ simulate all case topics beforehand """
    
    topics = list(range(0,10))
    
    P_topics = [0.318670,
                0.243781,
                0.138256,
                0.066510,
                0.064415,
                0.063891,
                0.039277,
                0.037968,
                0.014925,
                0.012307]
    
    sim_topics = np.random.choice(topics, size=100000, replace=True, p=P_topics)
    
    uniform_values = np.random.uniform(0,1, size=100000)
    
    """ Simulate todays case arrivals """
    
    for step in range(0,10000000000000):
        
        """
        Determine current place in time
        """
        
        time_change = datetime.timedelta(days=q)
        date_and_time = date_and_time + time_change
        #print(date_and_time)
    
        """
        ################################################
        Inter-arrival time prediction 
        ################################################
        """
            
        # Inputs for case arrival model
        #hour = date_and_time.hour
        weekday = date_and_time.weekday() #np.mod(z,7)
        month = date_and_time.month
        day = date_and_time.day
        year = date_and_time.year
                
        
        X = [year,
             month,
             day,
             weekday]
        
        betas = [-0.3589,
                 -0.0881,
                  0.0078,
                  0.2616]
        
        c = 726.6267
        
        #simulated residuals
        residual = -np.log(1-uniform_values[step])
        
        #Simulation equation: exponential regression
        q = residual * np.exp(c + np.dot(X,betas))
        
        #prediction expression is in hours, convert back to days:            
        q = q/24
        
      
        
        """ Simulate a new case arrival at time q in day d, and append it to the set of cases M """
        sigma = {"i":i,
                 "q":z+q, 
                 "q_offset":q,
                 "q_dt":date_and_time + datetime.timedelta(days=q),
                 "q_assigned":0,
                 "r":[],
                 "c_topic":sim_topics[step],
                 'j':[],
                 'a':[],
                 't':[],
                 't_delayed':[],
                 't_start':[],
                 't_end':[],
                 't_start_dt':[],
                 't_end_dt':[],
                 't_start_delay':[],
                 't_end_delay':[],
                 'initial_delay':0,
                 "status":"queue",
                 
                 "est_throughputtime":0,
                 "est_NPS":0,
                 "est_NPS_priority":0}
        
        
        """predict the expected RT and NPS for the given case"""
            
            
        #predict rt and nps
        """sigma = predict_RT_NPS(sigma)"""
        sigma = predict_RT_NPS_Notopic(sigma)
        
        
        if sigma["q"] <= D+1:
            #print(i,sigma["q"])
            M.append(sigma)
        
            """ Update time and counter variables """
            z = z + q
            
            i = i + 1
            
        else:
            break
    
    return M.copy(), i




    