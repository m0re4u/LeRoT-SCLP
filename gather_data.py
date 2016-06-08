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
from VisualEval import get_data_one_experiment

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
        experiment_eval_list = []
    try:
        for i in numpy.arange(args.variable_minimum, args.variable_maximum+args.step_size, args.step_size):
            # update variable in config
            update_config(args.file_name,args.variable_key,i)
            # Add data to overall eval list as tuple
            experiment_eval_list.append((get_data_one_experiment(), i ))
        # Write datadump
        with open("EvalDump.txt", 'w') as f:
            f.write(str(experiment_eval_list))
        # Restore original config file
        with open(args.file_name, 'w') as f:
            f.write(original_file)
    # When something goes wrong, print error
    except BaseException as err:
            print(type(err))
            print(err)
            # Restore original config file
            with open(args.file_name, 'w') as f:
                f.write(original_file)
