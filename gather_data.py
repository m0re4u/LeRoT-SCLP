#!/usr/bin/env python

import logging
import numpy
import argparse
import os
import sys
import yaml
try:
    from include import *
except:
    pass
from visual_eval import update_config
from visual_eval import get_data_one_experiment

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
    parser.add_argument("-o", "--output_file",
                        help="part of tmp config name",
                        default="")
    parser.add_argument("-t", "--type_evaluation",
                        help="online or offline evaluation")
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
    config_path = os.path.join(os.path.join("visual_eval", "tmp"), "config")
    config_name = os.path.join(
        config_path, args.output_file) + "_" + str(args.variable_key) + "_" + \
        str(args.variable_minimum) + "_" + str(args.variable_maximum) + "_" + \
        str(args.step_size) + ".yml"
    base_output_path = args.output_file
    with open(args.file_name, 'r') as original_config:
        original_file = yaml.load(original_config)
    # HARDE HACK VOOR CONFIG FIX
    # If dir doesnt exist make it
    if not os.path.exists(config_path):
        os.makedirs(config_path)
    if not os.path.exists(base_output_path):
        os.makedirs(base_output_path)
    # Past the original config
    with open(config_name, 'w') as tmp_config:
        yaml.dump(original_file, tmp_config)

    try:
        # Construct datadump with initial value 0,0
        for i in [args.variable_minimum + args.step_size * i
                  for i in xrange(0, int(
                    (args.variable_maximum - args.variable_minimum) /
                    args.step_size))]:
            # update variable in config
            update_config(config_name, args.variable_key, i)
            # Add data to overall eval list as tuple
            output_path = os.path.join(base_output_path, args.variable_key +
                                       str(i))
            experiment_data = get_data_one_experiment(
                args.type_evaluation, args.evaluation_measure, '-f ' +
                config_name + ' -o ' + output_path)
    finally:
        os.remove(config_name)
