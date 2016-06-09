#!/usr/bin/env python

import logging
import numpy
import argparse
import os
import sys
try:
    from include import *
except:
    pass
from VisualEval import update_config
from VisualEval import get_data_one_experiment
from VisualEval import visualize_data




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
    # Save original config file
    with open(args.file_name, 'r') as f:
        original_file = f.read()
        experiment_eval_list = [([0],0)]
        dump_name = "DataDump/EvalDump" +"_" + str(args.variable_key) +"_"+ str(args.variable_minimum)
                    +"_"+ str(args.variable_maximum )+"_" + str(args.step_size) + ".txt"
    try:
        # Construct datadump with initial value 0,0
        with open(dump_name, 'w') as f:
            f.write("[([0],0)")
        for i in [args.variable_minimum + args.step_size * i
                  for i in xrange(0, int(args.variable_maximum / args.step_size))]:
            # update variable in config
            update_config(args.file_name,args.variable_key,i)
            # Add data to overall eval list as tuple
            experiment_data = (get_data_one_experiment(),i)
            with open(dump_name, 'a') as f:
                f.write(','str(experiment_data))
            experiment_eval_list.append(experiment_data)
        # Finish datadump
        with open(dump_name, 'a')
            f.write("]")
        # Visualize data
        visualize_data(experiment_eval_list)
    finally:
        # Restore original config file
        with open(args.file_name, 'w') as f:
            f.write(original_file)
