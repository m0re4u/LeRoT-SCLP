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
    parser.add_argument("-m", "--evaluation_measure",
                        help="the evaluation measure used")
<<<<<<< HEAD
=======
    parser.add_argument("-o", "--output_file",
                        help="the evaluation measure used",
                        default="")
>>>>>>> 6c19531da42cbdfc82de454d64c13289ae66b913
    parser.add_argument("-t", "--type_evaluation",
                        help="online or offline evaluation")
    parser.add_argument("-name", "--output_file_name",
                        help="start of file name")
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

    config_name = os.path.join(os.path.join("VisualEval","config" ),args.output_file) + "_" + \
                str(args.variable_key) + "_" + str(args.variable_minimum)+ \
                "_" + str(args.variable_maximum)+"_"+str(args.step_size)+".yml"
    with open(args.file_name, 'r') as f:
        original_file = f.read()
<<<<<<< HEAD
        experiment_eval_list = [([0], 0)]
        dump_name = "DataDump/" + args.output_file_name + "EvalDump" + "_" + \
                    str(args.variable_key) + "_" + str(args.variable_minimum)+ \
                    "_" + str(args.variable_maximum)+"_"+str(args.step_size)+".txt"
=======
    # HARDE HACK VOOR CONFIG FIX
    # If dir doesnt exist make it
    if not os.path.exists(os.path.join("VisualEval","config")):
        os.mkdir(os.path.join("VisualEval","config"))
    # Past the original config
    with open(config_name, 'w') as f:
        f.write(original_file)

    experiment_eval_list = [([0], 0)]
    dump_name = os.path.join("DataDump", args.output_file) + "EvalDump" + "_" + \
                str(args.variable_key) + "_" + str(args.variable_minimum)+ \
                "_" + str(args.variable_maximum)+"_"+str(args.step_size)+".txt"
>>>>>>> 6c19531da42cbdfc82de454d64c13289ae66b913

    try:
        # Construct datadump with initial value 0,0
        if not os.path.exists("DataDump"):
            os.mkdir("DataDump")
        with open(dump_name, 'w') as f:
            f.write("[([0],0)")
        for i in [args.variable_minimum + args.step_size * i
                  for i in xrange(0, int((args.variable_maximum - args.variable_minimum) / args.step_size))]:
            # update variable in config
            update_config(config_name, args.variable_key, i)
            # Add data to overall eval list as tuple
            experiment_data = (get_data_one_experiment(args.type_evaluation, args.evaluation_measure, '-f '+config_name), i)
            with open(dump_name, 'a') as f:
                f.write(',' + str(experiment_data))
            experiment_eval_list.append(experiment_data)
        # Finish datadump
        with open(dump_name, 'a') as f:
            f.write("]")
        # Visualize data
        # visualize_data(experiment_eval_list)
    finally:
        os.remove(config_name)
