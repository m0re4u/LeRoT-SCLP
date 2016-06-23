from time import sleep
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import argparse
import yaml
import sys

SEAGREEN = (0, 128 / 255., 102 / 255.)
INTERVAL = 500


def create_histogram(filename, iterations, stepsize, x_label, y_label, max_x,
                     min_y, max_y, title):
    fig = plt.figure(facecolor='white')

    datafile = open(filename, "r").read()
    y_data = [sorted(data, reverse=True) for data in yaml.load(datafile)]
    y_data = [y_data[i*stepsize] for i in range(0, len(y_data) // stepsize)]
    x_data = list(range(0, len(y_data[0])))

    fargs = [
        x_data,
        y_data,
        fig,
        min_y,
        max_y,
        x_label,
        y_label,
        title,
        iterations
    ]
    animation.FuncAnimation(
        fig, animate,
        fargs=fargs,
        interval=INTERVAL
    )

    plt.show()


def animate(i, x_data, y_data, fig, min_y, max_y, x_label, y_label,
            iterations):

    if i > iterations:
        sleep(3)
        sys.exit()
    if i == 1:
        sleep(5)
    # Reset figure
    fig.clear()

    # Set text for figure and labels
    plt.xlabel(x_label, size=26)
    plt.ylabel(y_label, size=26)
    plt.title("Iteration" + " " + str(i+1), size=26)

    # Set axes sizes
    max_x = len(x_data)
    plt.ylim(min_y, max_y)
    plt.xlim(0, max_x)

    plt.bar(x_data, y_data[i], color=SEAGREEN)

    # Set visibility of plot frame lines
    ax = plt.axes()
    ax.spines["top"].set_visible(False)
    ax.spines["bottom"].set_visible(True)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(True)

    # Remove the tick marks at top and right
    plt.tick_params(axis="both", which="both", bottom="on", top="off",
                    labelbottom="on", left="on", right="off",
                    labelleft="on")

    # Add hardly visible lines at every +0.1
    for y in np.arange(0, 1, 0.1):
        plt.plot(range(0, max_x+1), [y] * len(range(0, max_x+1)),
                 "--", lw=0.5, color="black", alpha=0.5)

    return plt


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="""
            Construct and run a set of learning experiments. Provide the
            name of the config file, and which parameter you want to be shifted
            between what range, with what steps""")
    parser.add_argument("-f", "--filename", help="name of file with data")
    parser.add_argument("-s", "--stepsize", help="stepsize for the animation",
                        type=int)
    parser.add_argument("-i", "--iterations", type=int,
                        help="number of iterations shown")
    parser.add_argument("-x", "--x_label", help="label for x-axis")
    parser.add_argument("-y", "--y_label", help="label for y-axis"
                        "(HAS TO BE EVALUATION MEASURE LIKE IN CONFIG)")
    parser.add_argument("-max_x", "--max_bound_x",
                        help="maximum number for x-axis", type=int)
    parser.add_argument("-max_y", "--max_bound_y",
                        help="maximum number for y-axis", type=float)
    parser.add_argument("-min_y", "--min_bound_y",
                        help="minimum number for y-axis", type=float)

    args = parser.parse_args()

    create_histogram(args.filename, args.iterations, args.stepsize,
                     args.x_label, args.y_label, args.max_bound_x,
                     args.min_bound_y, args.max_bound_y)
