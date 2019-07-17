# -*- coding: utf-8 -*-
"""
Created on Mon Jul  8 11:03:29 2019

@author: Emma
"""

if __name__ == "__main__":
    from model_with_policy import borg_ebola

    import numpy as np
    
    from ema_workbench import (IntegerParameter, RealParameter, ReplicatorModel,
                               ScalarOutcome, ArrayOutcome, Policy)
    
    
    model = ReplicatorModel('Ebola', function=borg_ebola)
    
    
    N_SCENARIOS = 2
    
    model.replications = 2
    
    
    
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
    
    model.uncertainties = [IntegerParameter('I4', 1, 8),
                           IntegerParameter('I14', 20, 35),
                           IntegerParameter('I15', 25, 40),
                           RealParameter('beta_i', 0.1, 0.5),
                           RealParameter('travel_rate', 0.04, 0.1)]
    
    
    model.levers = [RealParameter('c1', -1.0, 1.0),
                   RealParameter('c2', -1.0, 1.0),
                   RealParameter('r1', 0.000001, 1.0),
                   RealParameter('r2', 0.000001, 1.0),
                   RealParameter('w', 0, 1.0)]
                    
    
    policies = [Policy("141", **{'c1' : 0.189347,
                                 'c2' : 0.297782,
                                 'r1' : 0.663825,
                                 'r2' : 0.677523,
                                 'w' : 0.470387}),
               Policy("148", **{'c1' : 0.356111,
                                'c2' : 0.476011,
                                'r1' : 0.888042,  
                                'r2' : 0.827078,
                                'w' : 0.851858}),
               Policy("390", **{'c1' : 0.960692,
                                'c2' : 0.851394,
                                'r1' : 0.374287,
                                'r2' : 0.139462,
                                'w' : 0.992082}),
               Policy("185", **{'c1' : 0.310568,
                                'c2' : 0.006200,
                                'r1' : 0.539050,
                                'r2' : 0.604281,
                                'w' : 0.624870}),
               Policy("661", **{'c1' : 0.760093,
                                'c2' : 0.356904,
                                'r1' : 0.816285,  
                                'r2' : 1.000000,
                                'w' : 0.661981})]
    
    
    
    
    from ema_workbench import SequentialEvaluator, MultiprocessingEvaluator, ema_logging
    
    ema_logging.log_to_stderr(ema_logging.INFO)
    
    
    import time
    start_time = time.time()
    
    
    with SequentialEvaluator(model) as evaluator:
        results = evaluator.perform_experiments(scenarios=N_SCENARIOS, policies = policies)
        
    print("--- %s seconds ---" % (time.time() - start_time))
    
    from ema_workbench import save_results
    save_results(results, r'./policies-functions.tar.gz')