#!/usr/bin/env python

import logging
import numpy
import argparse
import os
import sys
import matplotlib.pyplot as plt
try:
    from include import *
except:
    pass
from VisualEval import update_config
from VisualEval import get_data_one_experiment

def visualize_data(data):
    """
    Assuming we recieve a list(tuple(list(eval_measure), iteration))
    make a plot and output it
    """
    plt.plot([sample[1] for sample in data],[numpy.mean(sample[0]) for sample in data])
    print(data)
    plt.xlabel("swap probability")
    plt.ylabel("nDCG")
    plt.show()
        # get mean




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
    try:
        for i in [args.variable_minimum + args.step_size * i
                  for i in xrange(0, int(args.variable_maximum / args.step_size))]:
            # update variable in config
            update_config(args.file_name,args.variable_key,i)
            # Add data to overall eval list as tuple
            experiment_eval_list.append((get_data_one_experiment(), i))
        # Write datadump
        visualize_data(experiment_eval_list)
        with open("DataDump/EvalDump" +"_" + str(args.variable_key) +"_"+ str(args.variable_minimum)
                  +"_"+ str(args.variable_maximum )+"_" + str(args.step_size) + ".txt", 'w') as f:
            f.write(str(experiment_eval_list))
    finally:
        # Restore original config file
        with open(args.file_name, 'w') as f:
            f.write(original_file)
