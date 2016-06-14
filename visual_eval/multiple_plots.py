import argparse
import matplotlib.pyplot as plt
import os
import numpy as np
from ast import literal_eval


def multiple_plots(x_data, y_data, y_pos, max_bound, plot_title, x_label,
                   y_label, z_label):
    """
    Plot data of multiple files in one graph.
    """

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
    plt.xlim(0, max_bound)

    # Remove the tick marks at top and right
    plt.tick_params(axis="both", which="both", bottom="on", top="off",
                    labelbottom="on", left="on", right="off", labelleft="on")

    # Add hardly visible lines at every +0.1
    for y in np.arange(0, 1, 0.1):
        plt.plot(range(0, 1000), [y] * len(range(0, 1000)),
                 "--", lw=0.5, color="black", alpha=0.5)

    # Plot all data
    for i in range(len(x_data)):
        plt.plot(x_data[i], y_data[i], lw=2, color=colours[i])

        # Add a text label to the right end of every line

        plt.text(max_bound + 5, y_pos[i], z_label[i],
                 fontsize=14, color=colours[i])

    # Add title to plot and labels to axes
    plt.title(plot_title, size=17)
    plt.xlabel(x_label)
    plt.ylabel(y_label)

    # Save plot as picture
    plt.savefig(plot_title + ".png", bbox_inches="tight")
