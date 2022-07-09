# -*- coding: utf-8 -*-
"""
Created on Mon Jan 24 11:43:41 2022

@author: Mike
"""


def simulate_NPS(case_topicidx, y, seed):
    
    import numpy as np
    import pandas as pd
    from mpmath import gamma
    #use step as seed here
    np.random.seed(seed)

    #############################################
    # NPS score prediction:
    
    # get features
    
    log_throughputtime = np.log(1+y)
    
    #get case topic index
    #case_topicidx = c_topic #sigma["c_topic"]
    
    def MatchCategorical(index, levels= ["j_1",
                                           "z_3",
                                           "q_3",
                                           "z_2",
                                           "r_2",
                                           "z_4",
                                           "d_2",
                                           "w_2",
                                           "g_1",
                                           "w_1"]):
                        
            #get value as string
            value = levels[index]
            return value       
    
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
    
    #residuals (exponential regression)
    #residual = -np.log(1-uniform_values[step])
        
    #prediction equation
    NPS = np.exp(intercept + np.dot(X,betas))/gammascale #*float(gamma(1+gammascale))
        
    #add random component
    NPS = np.random.gamma(shape=NPS, scale=gammascale, size=1)[0]-1 #minus the offset added to target
    
    # update weighted NPS_priority:
    NPS_priority = np.abs(NPS-7.5)
    
    return NPS, NPS_priority




def store_evlog(L, P_scheme, agents, filedest, seed):
    import pandas as pd
    import numpy as np
    import datetime
    print("generating eventlog...")

    DF_list = []
    
    #step counter for random values seed
    step = seed
    
    
    for case in L:
        # update step counter used for seed, each case gets its unique seed
        step = step +1
        
        # Generate lists of equal length to be appended
    
        #trace length 
        length = len(case["a"])
        
        #only store closed cases
        #if case["status"] == "closed":
                    
        if length > 0:
            throughput_time = np.max(case["t_end"])-case["q"]
            NPS_actual, NPS_priority_actual = simulate_NPS(case_topicidx=case["c_topic"], y=throughput_time, seed=step)#[0]
        
            res_i = pd.DataFrame({"case_id":[case["i"]]*length,
                                  
                                  "case_arrival":[case["q"]]*length,
                                  #"case_arrival_offset":[case["q_offset"]]*length,
                                  "case_arrival_dt":[case["q_dt"].strftime('%m/%d/%Y %H:%M:%S')]*length,
                                  
                                  "case_assigned":[case["q_assigned"]]*length,
                                  "resource":[case["r"][0]]*length,
                                  "case_topic":[case["c_topic"]]*length,
                                  
                                  "initial_delay":[case["initial_delay"]]*length,
                                  
                                  "est_NPS_priority":[case["est_NPS_priority"]]*length,
                                  "est_NPS":[case["est_NPS"]]*length,
                                  "est_throughput_time":[case["est_throughputtime"]]*length,
                                  
                                  "event_no":case["j"],
                                  "activity":case["a"],
                                  
                                  "activity_start":case["t_start"],
                                  "activity_end":case["t_end"],
                                  
                                  #"activity_start":case["t_start_dt"].strftime('%m/%d/%Y %H:%M:%S'),
                                  #"activity_end":case["t_end_dt"].strftime('%m/%d/%Y %H:%M:%S'),
                                  
                                  "activity_start_dt":[datetime.datetime.strftime(i, '%m/%d/%Y %H:%M:%S') for i in case["t_start_dt"]],
                                  "activity_end_dt":[datetime.datetime.strftime(i, '%m/%d/%Y %H:%M:%S') for i in case["t_end_dt"]],
                                  
                                  "activity_start_delay":case["t_start_delay"],
                                  "activity_end_delay":case["t_end_delay"],
                                  
                                  "duration":case["t"],
                                  "duration_delayed":case["t_delayed"],
                                  
                                  #"delay_type":[case["delay_type"][0]]*length,
                                  "case_status":[case["status"]]*length,
                                  "F_priority_scheme":[P_scheme]*length,
                                  "F_number_of_agents":[agents]*length,
                                  "seed":[seed]*length,
                                  
                                  "actual_NPS":[NPS_actual]*length,
                                  "actual_NPS_priority":[NPS_priority_actual]*length,
                                  "actual_throughput_time":[throughput_time]*length #end of last event and arrival time
                                  },
                                 index=list(range(0,length)))
            DF_list.append(res_i)
     
    Evlog = pd.concat(DF_list, ignore_index=True)
    Evlog = Evlog.sort_values("case_id")
    
    return Evlog 




def sim_generalized_lognormal(n=1):
    import numpy as np
    
    #simulate from normal
    x = np.random.normal(loc=0.2835587,#-3.228792,
                         scale=0.7866424,#2.0041058,
                         size=n)[0]
    
    #generalized lognormal
    shape = 0.0302774
    
    if shape > 0:
        #transform into generalized lognormal
        x = (np.power(x,shape)-1)/shape
    else:
        #alternative transformation
        x = np.log(x)
    
    return x

def fullfact_corrected(levels):
    import numpy as np
    import pandas as pd
    """
    Create a general full-factorial design
    
    Parameters
    ----------
    levels : array-like
        An array of integers that indicate the number of levels of each input
        design factor.
    
    Returns
    -------
    mat : 2d-array
        The design matrix with coded levels 0 to k-1 for a k-level factor
    
    Example
    -------
    ::
    
        >>> fullfact([2, 4, 3])
        array([[ 0.,  0.,  0.],
               [ 1.,  0.,  0.],
               [ 0.,  1.,  0.],
               [ 1.,  1.,  0.],
               [ 0.,  2.,  0.],
               [ 1.,  2.,  0.],
               [ 0.,  3.,  0.],
               [ 1.,  3.,  0.],
               [ 0.,  0.,  1.],
               [ 1.,  0.,  1.],
               [ 0.,  1.,  1.],
               [ 1.,  1.,  1.],
               [ 0.,  2.,  1.],
               [ 1.,  2.,  1.],
               [ 0.,  3.,  1.],
               [ 1.,  3.,  1.],
               [ 0.,  0.,  2.],
               [ 1.,  0.,  2.],
               [ 0.,  1.,  2.],
               [ 1.,  1.,  2.],
               [ 0.,  2.,  2.],
               [ 1.,  2.,  2.],
               [ 0.,  3.,  2.],
               [ 1.,  3.,  2.]])
               
    """
    n = len(levels)  # number of factors
    nb_lines = np.prod(levels)  # number of trial conditions
    H = np.zeros((nb_lines, n))
    
    level_repeat = 1
    range_repeat = np.prod(levels)
    for i in range(n):
        range_repeat //= levels[i]
        lvl = []
        for j in range(levels[i]):
            lvl += [j]*level_repeat
        rng = lvl*range_repeat
        level_repeat *= levels[i]
        H[:, i] = rng
     
    return H

def construct_df(x,r):
    import numpy as np
    import pandas as pd
    df=pd.DataFrame(data=x,dtype='float32')
    for i in df.index:
        for j in range(len(list(df.iloc[i]))):
            df.iloc[i][j]=r[j][int(df.iloc[i][j])]
    return df

def build_full_fact(factor_level_ranges):
    import numpy as np
    import pandas as pd
    """
    Builds a full factorial design dataframe from a dictionary of factor/level ranges
    Example of the process variable dictionary:
    {'Pressure':[50,60,70],'Temperature':[290, 320, 350],'Flow rate':[0.9,1.0]}
    """
    
    factor_lvl_count=[]
    factor_lists=[]
    
    for key in factor_level_ranges:
        factor_lvl_count.append(len(factor_level_ranges[key]))
        factor_lists.append(factor_level_ranges[key])
    
    x = fullfact_corrected(factor_lvl_count)
    df=construct_df(x,factor_lists)
    df.columns=factor_level_ranges.keys()
    
    return df