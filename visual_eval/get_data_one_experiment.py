import os
import sys
from lerot.experiment import GenericExperiment


def get_data_one_experiment(evaluation, measure, arg_string):
    """
    Get the data of a single experiment with one config file
    """
    print(arg_string)
    experiment = GenericExperiment(arg_string)
    # Runs a number of experiments and returns a list of those experiment
    # results
    experiment_list = experiment.run()
    offline_eval = {}
    online_eval = {}

    # Loop over results of all runs
    # You can call:
    #   single_run["online_"+experiment.experiment_args["evaluation"][0]]
    #   single_run["offline_test_"+experiment.experiment_args["evaluation"][0]]
    #   single_run["offline_train_"+experiment.experiment_args["evaluation"][0]]

    # Get names for evaluation measures
    eval_names = [eval_name for eval_name in experiment_list[0]]
    for eval_name in eval_names:
        if eval_name == 'weight_sim' or eval_name == 'final_weights':
            continue
        splitted_eval_name = eval_name.split('@')[0]
        online_eval[splitted_eval_name] = []
        offline_eval[splitted_eval_name] = []
        for single_run in experiment_list:
            if 'online' in eval_name:
                online_eval[splitted_eval_name].append(
                    single_run[eval_name][-1])
            else:
                offline_eval[splitted_eval_name].append(
                    single_run[eval_name][-1])

    if 'online' in evaluation:
        return online_eval[evaluation + "_evaluation." + measure]
    else:
        return offline_eval[evaluation + "_evaluation." + measure]
