# -*- coding: utf-8 -*-
"""
Created on Mon Jul  8 11:28:38 2019

@author: Emma
"""

if __name__ == "__main__":
    import numpy as np
    
    from model import ebola_model
    
    from ema_workbench import (IntegerParameter, RealParameter, ReplicatorModel,
                               ScalarOutcome, ArrayOutcome, Policy)
    
    model = ReplicatorModel('Ebola', function=ebola_model)
    
    
    N_SCENARIOS = 2
    
    model.replications = 2
    
    model.uncertainties = [IntegerParameter('I4', 1, 8),
                           IntegerParameter('I14', 20, 35),
                           IntegerParameter('I15', 25, 40),
                           RealParameter('beta_i', 0.1, 0.5),
                           RealParameter('travel_rate', 0.04, 0.1)]
    
    model.outcomes = [ScalarOutcome('mean effectiveness', function=np.mean, 
                                   variable_name='Effectiveness'),
                      ScalarOutcome('mean time until containment', function = np.mean,
                                   variable_name='Time until Containment'),
                      ScalarOutcome('mean difference in met demand', function = np.mean,
                                   variable_name='Difference in Met Demand'),
                      ScalarOutcome('mean difference in arrival time', function = np.mean,
                                   variable_name='Difference in Arrival Time'),
                      ScalarOutcome('mean cost per death prevented', function = np.mean,
                                   variable_name='Cost per Death Prevented'),
                      ArrayOutcome('Uncertainty over Time',
                                   variable_name='Uncertainty over Time'),
                      ArrayOutcome('Decision Types over Time', variable_name='Decision Types'),
                      ArrayOutcome('Chosen Regions', variable_name='Chosen Regions')]
    
    
    model.levers = [RealParameter('exploration_ratio', 0.0, 1.0)]
                    
    policies = [Policy("All exploitation", **{'exploration_ratio' : 0.0}),
                Policy("All exploration", **{'exploration_ratio' : 1.0}),
                Policy("50-50", **{'exploration_ratio' : 0.5})]
    
    
    from ema_workbench import SequentialEvaluator, MultiprocessingEvaluator, ema_logging
    
    ema_logging.log_to_stderr(ema_logging.INFO)
    
    import time
    start_time = time.time()
    
    with SequentialEvaluator(model) as evaluator:
    #with MultiprocessingEvaluator(model) as evaluator:
        results = evaluator.perform_experiments(scenarios=N_SCENARIOS, policies = policies)
        
    print("--- %s seconds ---" % (time.time() - start_time))
    
    from ema_workbench import save_results
    save_results(results, r'./constant-policies.tar.gz')
