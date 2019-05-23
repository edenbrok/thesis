# -*- coding: utf-8 -*-
"""
Created on Thu May 23 22:52:10 2019

@author: Emma
"""

### Functions for the Uncertainty Reduction ###
import math

def unc_infected(region, timestep):
    
    ETC_50 = [1.0,0.95,0.85,0.7,0.5,0.325,0.25,0.225,0.21,0.2]
    ETC_10 = [1.0,0.95,0.7,0.55,0.45,0.375,0.325,0.30]

    perc_reduced = 1.0
    ETCs = region.ETCs
    for ETC in ETCs:
        if ETC.capacity == 50:
            weeks = timestep - ETC.timestep_placed
            
            if weeks >= len(ETC_50):
                percentage = ETC_50[-1]
            else:
                percentage = ETC_50[weeks]
                
            if perc_reduced > percentage:
                perc_reduced = percentage
                
        elif ETC.capacity == 10:
            weeks = timestep - ETC.timestep_placed
            
            if weeks >= len(ETC_10):
                percentage = ETC_10[-1]
            else:
                percentage = ETC_10[weeks]
                
            if perc_reduced > percentage:
                perc_reduced = percentage

    return perc_reduced
        
####CHECK THIS ONE
def unc_transmission(cumm_patients):
    if cumm_patients > 100:
        return 0
    else:
        return math.e**(-cumm_patients/15)