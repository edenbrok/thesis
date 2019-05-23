# -*- coding: utf-8 -*-
"""
Created on Thu May 23 22:21:29 2019

@author: Emma
"""

from scipy.integrate import odeint
import numpy as np
import random

import objective_functions
from compartmental_model import calc_population
import decision_making
from utility import random_travelling
import uncertainty_reduction

from objects import  Region



    
compartments = 6 #no. of compartments in the model
i_index = 1 #when listing the compartments, where the infected compartent is (starting from 0)
    
#THE GRID HAS TO BE SQUARE 
no_regions = 16
regions_list = [i for i in range(no_regions)] #list of the regions
    
    
### RESOURCES AVAILABLE ###
surveillance_capacity = 1
bed_capacity = 40 
    
    
### TIMESTEPS ###
timesteps = 26



def ebola_model(I1 = 0,
                I2 = 0,
                beta_i = 0.33,
                beta_d = 0.68,
                travel_rate = 0.05,
                exploration_ratio = 0.5):
    
    
    #Time vector to feed into odeint, one timestep each iteration
    time_vec = np.linspace(0,1,2)
     
    #Setting up all the region objects      
    regions = []
    
    for entry in regions_list:
        if entry == 0:
            region = Region(entry, (10000-1.5*I1), I1, 0, (0.5*I1), 0, 0, beta_i, beta_d)
        elif entry == 1:
            region = Region(entry, (10000-1.5*I2), I2, 0, (0.5*I2), 0, 0, beta_i, beta_d)
        else:
            region = Region(entry, 10000, 0, 0, 0, 0, 0, beta_i, beta_d)
            
        regions.append(region)
    

    
    y0 = []
    
    for region in regions:
        y0.extend([region.susceptible[0], region.infected[0], region.recovered[0], region.deceased[0], region.funeral[0], region.treated[0]])

        
    no_response_t = np.linspace(0, 10, 10)
    no_response_population = odeint(calc_population, y0, t=no_response_t, args=(regions, travel_rate))
    no_response_results = no_response_population[-1]
    
    
    for x in range (0,timesteps):
        
        #print("Timestep ", x)
        
        for region in regions:
            
            #in some "hidden" regions, the # of patients may be so high we hear about it spontaneously
            if region.hidden == True:
                region.spontaneous_news()
            
            #update uncertainties
            if region.uncertain_I.percentage != uncertainty_reduction.unc_infected(region,x):
                region.uncertain_I.reduce_uncertainty(uncertainty_reduction.unc_infected(region, x))
                
            if region.uncertain_bi.percentage != uncertainty_reduction.unc_transmission(region.cummulative_patients_prev):
                region.uncertain_bi.reduce_uncertainty(uncertainty_reduction.unc_transmission(region.cummulative_patients_prev))
            
            
        
        #make decisions
        decision_type  = random.uniform(0,1)
        if decision_type < exploration_ratio:
            
            #take an explorative action
            decision_making.explorative_decision(regions,x, surveillance_capacity, bed_capacity)

        else:
            #take an exploitative action
            decision_making.exploitative_decision(regions,x, bed_capacity)

        
        #See if any resources can be freed for the next timestep:
        
        #check if any ETCs can be closed down
        decision_making.check_for_removal(regions,x)
        
        #check if any surveillance teams are "done"
        decision_making.check_surveillance_removal(regions,x)
        
        #update the ETC capacity of each region
        for region in regions:
            region.calculate_capacity(x, regions)
            
        
        #Run the compartmental model for 1 timestep                                                                                  
        population = odeint(calc_population, y0, t=time_vec, args=(regions, travel_rate))
        
        #random travelling takes place here. The function returns the new list of the population, regardless of whether random travel occured
        y0 = random_travelling(regions, population.T[:,1], compartments, i_index)

        
        #store the results and update the region objects
        for i in range(0,len(regions)):
            regions[i].update(y0[i*compartments:i*compartments+compartments])
            regions[i].update_cummulative_patients()


    objective_1 = objective_functions.effectiveness(regions, compartments, no_response_results)
    objective_2 = objective_functions.speed(regions,timesteps)
    objective_3 = objective_functions.equity_demand(regions)
    objective_4 = objective_functions.equity_arrival(regions,timesteps)
    objective_5 = objective_functions.efficiency(regions, compartments, no_response_results, timesteps)
    results = [objective_1, objective_2, objective_3, objective_4, objective_5]
       
    return results
