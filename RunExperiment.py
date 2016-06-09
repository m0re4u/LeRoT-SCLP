#!/usr/bin/env python

import logging
import numpy
import argparse
import os
try:
    from include import *
except:
    pass
from VisualEval import update_config
from lerot.experiment import GenericExperiment


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="""
            Construct and run a set of learning experiments. Provide the
            name of the config file, and which parameter you want to be shifted
            between what range, with what steps""")
    parser.add_argument("-f", "--file_name", help="name of config file")
    parser.add_argument("-k", "--variable_key",
                        help="the name of the variable that has to be changed")
    parser.add_argument("-min", "--variable_minimum",
                        help="the minimum of the traversable variable",
                        type=float)
    parser.add_argument("-max", "--variable_maximum",
                        help="the maximum of the traversable variable",
                        type=float)
    parser.add_argument("-n", "--step_size",
                        help="steps that the range is traversed with",
                        type=float)
    args = parser.parse_args()
    # Creates an experiment that can be iterated over
    with open(args.file_name, 'r') as f:
        original_file = f.read()
        experiment_eval_list = []
    try:
        for i in numpy.arange(args.variable_minimum, args.variable_maximum+args.step_size, args.step_size):
            # update variable in config
            update_config(args.file_name,args.variable_key,i)
            experiment = GenericExperiment()
            # Runs a number of experiments and returns a list of those experiment results
            experiment_list = experiment.run()

            offline_ndcg_eval_list = []

            for experiment in experiment_list:
                offline_ndcg_eval_list.append(experiment["offline_train_evaluation.NdcgEval"][-1])
            logging.info("RESULTS:")
            print("Average NDCG result: "+ str(float(sum(offline_ndcg_eval_list))/len(offline_ndcg_eval_list)))
            print("NDCG mean: " + str(numpy.mean(offline_ndcg_eval_list)))
            print("NDCG Max: " + str(max(offline_ndcg_eval_list)))
            print("NDCG Min: " + str(min(offline_ndcg_eval_list)))
            # Add to overall eval list as tuple
            experiment_eval_list.append((offline_ndcg_eval_list, i ))
        # Write datadump
        with open("EvalDump.txt", 'w') as f:
            f.write(str(experiment_eval_list))
        # Recover original eval
        with open(args.file_name, 'w') as f:
            f.write(original_file)
    # When something goes wrong, print the type and the error and recover original config
    except Exception as err:
            print(type(err))
            print(err)
            with open(args.file_name, 'w') as f:
                f.write(original_file)
