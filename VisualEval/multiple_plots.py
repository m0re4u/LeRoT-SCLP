import argparse
import matplotlib.pyplot as plt
import pandas as pd
import os
import numpy as np
from ast import literal_eval

def multiple_plots(folder, plot_title, xlabel, ylabel, zlabel, zvalues):

    # Read all data from specified folder
    data = []
    for filename in os.listdir(folder):
        with open(os.path.join(folder, filename), 'r') as file:
            data.append(eval(file.read() + "]"))

    # 20 RGB colours
    colours = [
        (31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),
        (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),
        (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),
        (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),
        (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)
    ]

    # Scale the RGB values to the [0, 1] range
    for i in range(len(colours)):
        r, g, b = colours[i]
        colours[i] = (r / 255., g / 255., b / 255.)

    # Set figure size
    plt.figure(figsize=(15, 10))

    # Set visibility of plot frame lines
    ax = plt.subplot(111)
    ax.spines["top"].set_visible(False)
    ax.spines["bottom"].set_visible(True)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(True)

    # Limit the range of the plot to where the data is
    plt.ylim(0, 1)
    plt.xlim(0, 1000)

    # Remove the tick marks at top and right
    plt.tick_params(axis="both", which="both", bottom="on", top="off",
                    labelbottom="on", left="on", right="off", labelleft="on")

    # Add hardly visible lines at every +0.1
    for y in np.arange(0, 1, 0.1):
        plt.plot(range(0,1000), [y] * len(range(0,1000)),
            "--", lw=0.5, color="black", alpha=0.5)

    # # Make sure your axis ticks are large enough to be
    # plt.yticks(fontsize=14)
    # plt.xticks(fontsize=14)

    # Plot all data
    for i, file in enumerate(data):
        plt.plot([sample[1] for sample in file],
            [np.mean(sample[0]) for sample in file],
            lw=2, color=colours[1], alpha=1)

        # Add a text label to the right end of every line. Most of the code below
        # is adding specific offsets y position because some labels overlapped.
        y_pos = float(np.mean(file[-1][0]) + 0.1)
        plt.text(1001, y_pos, zlabel + str(zvalues[i]), fontsize=14, color=colours[i])

    # Add title to plot
    plt.title(plot_title, size=17)

    # Save plot as picture
    plt.savefig(plot_title + ".png", bbox_inches="tight")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="""
            Construct and run a set of learning experiments. Provide the
            name of the config file, and which parameter you want to be shifted
            between what range, with what steps""")
    parser.add_argument("-f", "--folder_name", help="name of folder with data")
    parser.add_argument("-title", help="title for plot")
    parser.add_argument("-x", "--x_label",
                        help="the label of the x-axis")
    parser.add_argument("-y", "--y_label",
                        help="the label of the y-axis")
    parser.add_argument("-z", "--z_label",
                        help="the label of the variable across lines")
    parser.add_argument("-values", "--z_values",
                        help="...")
    args = parser.parse_args()

    multiple_plots(args.folder_name, args.title, args.x_label, args.y_label,
        args.z_label, eval(args.z_values))
