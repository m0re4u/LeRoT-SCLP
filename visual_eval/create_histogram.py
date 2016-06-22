import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import argparse
import yaml


def create_histogram(filename, x_label, y_label, max_x, min_y, max_y, title):

    SEAGREEN = (0, 128 / 255., 102 / 255.)

    fig = plt.figure()

    datafile = open(filename,"r").read()
    y_data = [sorted(data, reverse = True) for data in yaml.load(datafile)]
    x_data = list(range(0, len(y_data[0])))

    ani = animation.FuncAnimation(
        fig, animate,
        fargs=[x_data, y_data, fig, min_y, max_y, x_label, y_label, title,
        SEAGREEN], interval=10
    )

    plt.show()


def animate(i, x_data, y_data, fig, min_y, max_y, x_label, y_label, title,
            bar_colour):

    # Reset figure
    fig.clear()

    # Set text for figure and labels
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title("Iteration" + " " + str(i+1))

    # Set axes sizes
    max_x = len(x_data)
    plt.ylim(min_y, max_y)
    plt.xlim(0,max_x)

    plt.bar(x_data, y_data[i], colour=bar_colour)

    # Set visibility of plot frame lines
    ax = plt.subplot(111)
    ax.spines["top"].set_visible(False)
    ax.spines["bottom"].set_visible(True)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(True)

    # Remove the tick marks at top and right
    plt.tick_params(axis="both", which="both", bottom="on", top="off",
                    labelbottom="on", left="on", right="off", labelleft="on")

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
    parser.add_argument("-x", "--x_label", help="label for x-axis")
    parser.add_argument("-y", "--y_label", help="label for y-axis"
                        "(HAS TO BE EVALUATION MEASURE LIKE IN CONFIG)")
    parser.add_argument("-max_x", "--max_bound_x",
                        help="maximum number for x-axis", type=int)
    parser.add_argument("-max_y", "--max_bound_y",
                        help="maximum number for y-axis", type=float)
    parser.add_argument("-min_y", "--min_bound_y",
                        help="minimum number for y-axis", type=float)
    parser.add_argument("-title", help="title for image")

    args = parser.parse_args()

    create_histogram(args.filename, args.x_label, args.y_label,
                   args.max_bound_x, args.min_bound_y, args.max_bound_y,
                   args.title)
