import matplotlib.pyplot as plt
import numpy
import argparse
import pandas as pd
import os
import numpy as np
from multiple_plots import multiple_plots

def visualize_gathered_data(folder, max_bound, plot_title, x_label, y_label):
    """
    Plot data of multiple files in one graph
    """

    # Read all data from specified folder
    data = []
    z_label = []
    for filename in os.listdir(folder):
        with open(os.path.join(folder, filename), 'r') as file:
            z_label.append(filename.split('#')[0])
            data.append(eval(file.read()))

    # Gather data from files along with the positions for the labels
    x_data = []
    y_data = []
    y_pos = []
    for i, file in enumerate(data):
        x_data.append([sample[1] for sample in file])
        y_data.append([np.mean(sample[0]) for sample in file])
        y_pos.append(float(np.mean(file[-1][0])))

    # Create multiple plots
    multiple_plots(x_data, y_data, y_pos,
        max_bound, plot_title, x_label, y_label, z_label)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="""
            Construct and run a set of learning experiments. Provide the
            name of the config file, and which parameter you want to be shifted
            between what range, with what steps""")
    parser.add_argument("-f", "--folder_name", help="name of folder with data")
    parser.add_argument("-max", "--max_bound",
                        help="maximum number for x-axis", type=int)
    parser.add_argument("-title", help="title for plot")
    parser.add_argument("-x", "--x_label",
                        help="the label of the x-axis")
    parser.add_argument("-y", "--y_label",
                        help="the label of the y-axis")
    args = parser.parse_args()

    visualize_gathered_data(args.folder_name, args.max_bound, args.title,
        args.x_label, args.y_label)
