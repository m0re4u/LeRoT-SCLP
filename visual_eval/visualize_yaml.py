#!/usr/bin/env python

import argparse
import numpy as np
import gzip
import os
import yaml
from multiple_plots import multiple_plots

global _CACHE
_CACHE = {}


def visualize_yaml(folder_name, measures, y_labels, x_label, max_bound_x,
                   output, max_bound_y=None, min_bound_y=None, run_mean=1,
                   logarithmic=False):
    """
    Visualize the specified evaluation from the folder given.
    Setting the mean flag will assume each file is one run, and take the
    average over runs.
    """

    for measure, y_label in zip(measures, y_labels):
        x_data, y_data, z_labels = (list(x) for x in zip(*[
            open_file(measure, filename, folder_name)
            for filename in os.listdir(folder_name)
        ]))

        y_pos = []
        for i in range(len(y_data)):
            x_data[i] = x_data[i][:-run_mean]
            y_data[i] = running_mean(y_data[i], run_mean)[:-run_mean]
            if measure == "online":
                y_data[i] = calc_cumulative(y_data[i])
            if max_bound_y is None or max(y_data[i]) > max_bound_y:
                max_bound_y = max(y_data[i])
            if min_bound_y is None or min(y_data[i]) < min_bound_y:
                min_bound_y = min(y_data[i])
            y_pos.append(y_data[i][-1])

        if max_bound_x is None:
            max_bound_x = len(x_data[0])
        else:
            max_bound_x-run_mean

        multiple_plots(
            x_data=x_data,
            y_data=y_data,
            y_pos=y_pos,
            max_bound=max_bound_x,
            ymin=min_bound_y,
            ymax=max_bound_y,
            output=output + measure,
            x_label=x_label,
            y_label=y_label,
            z_label=z_labels,
            logarithmic=logarithmic
        )


def running_mean(x, N):
    return np.convolve(x, np.ones((N,))/N)[(N-1):]


def open_file(evaluation, filename, folder):
    """
    Open a file or folder

    When opening a folder, calculate the median of all files.
    Otherwise just read the numbers into a list and append that list to the
    current data collection.
    """
    new_folder = os.path.join(folder, filename)
    z_labels = filename.split('@')[0]
    if os.path.isdir(new_folder):
        _, temp_y, _ = zip(*[
            open_file(evaluation, file, new_folder)
            for file in os.listdir(new_folder)
        ])

        y_data = np.median(temp_y, axis=0)
    else:
        data = None
        _, ext = os.path.splitext(filename)
        # Exclude some standard files that are normally in the folder generated
        # by an experiment(particularly LearningExperiment)
        if ext == '.gz' and not filename.startswith('_'):
            name = os.path.join(folder, filename)
            global _CACHE
            if name not in _CACHE:
                with gzip.open(name, 'r') as data_file:
                    print("Reading " + str(filename))
                    _CACHE[name] = yaml.load(data_file.read())
            data = _CACHE[name]
            for measure in data:
                if evaluation.lower() == measure.lower():
                    y_data = data[measure]
                    break
            else:
                raise KeyError("The measure {} couldn't be found.".format(
                    evaluation
                ))

    x_data = list(range(1, len(y_data)+1))
    return (x_data, y_data, z_labels)


def calc_cumulative(y_data):
    """
    Turn data into cumulative vector.
    """

    summed = 0
    for i in range(len(y_data)):
        summed += y_data[i]
        y_data[i] = summed / (i + 1)

    return y_data

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Create many plots",
        fromfile_prefix_chars='@'
    )
    parser.add_argument("-f", "--folder_name", help="name of folder with data",
                        required=True)
    parser.add_argument("-m", "--measures", help="Evaluations to use",
                        required=True, nargs='*')
    parser.add_argument("-y", "--y_labels", help="labels for y-axis",
                        nargs='*', required=True)
    parser.add_argument("-x", "--x_label", help="label for x-axis",
                        required=True)
    parser.add_argument("-max_x", "--max_bound_x",
                        help="maximum number for x-axis", type=int)
    parser.add_argument("-max_y", "--max_bound_y",
                        help="maximum number for y-axis", type=float)
    parser.add_argument("-min_y", "--min_bound_y",
                        help="minimum number for y-axis", type=float)
    parser.add_argument("-o", "--output", help="output file for image")
    parser.add_argument("--run_mean", help="parameter for running mean",
                        type=int, default=1)
    parser.add_argument("-l", "--logarithmic", help="flag for log",
                        action='store_true')
    # parser.add_argument("-cum", "--cumulative",
    #                     help="boolean for want cumulative evaluation",
    #                     action=storetrue)
    args = parser.parse_args()

    visualize_yaml(**vars(args))
