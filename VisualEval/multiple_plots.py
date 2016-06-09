import argparse
import matplotlib.pyplot as plt
import pandas as pd
import os
import numpy as np
from ast import literal_eval

def multiple_plots(folder, xlabel, ylabel, zlabel, zvalues):

    # Read all data from specified folder
    data = []
    for filename in os.listdir(folder):
        with open(os.path.join(folder, filename), 'r') as file:
            data.append(eval(file.read() + "]"))

    # 20 RGB colours
    colours = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),
                 (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),
                 (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),
                 (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),
                 (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]

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

    # Limit the range of the plot to only where the data is.
    plt.ylim(0, 1)
    plt.xlim(0, 1000)

    # Remove the tick marks at top and right
    plt.tick_params(axis="both", which="both", bottom="on", top="off",
                    labelbottom="on", left="on", right="off", labelleft="on")

    # Make sure your axis ticks are large enough to be
    plt.yticks(fontsize=14)
    plt.xticks(fontsize=14)


    # Now that the plot is prepared, it's time to actually plot the data!
    # Note that I plotted the majors in order of the highest % in the final year.
    majors = ['Health Professions', 'Public Administration', 'Education', 'Psychology',
              'Foreign Languages', 'English', 'Communications\nand Journalism',
              'Art and Performance', 'Biology', 'Agriculture',
              'Social Sciences and History', 'Business', 'Math and Statistics',
              'Architecture', 'Physical Sciences', 'Computer Science',
              'Engineering']

    # Plot all data
    for file in data:
        plt.plot([sample[1] for sample in file],
            [np.mean(sample[0]) for sample in file],
            lw=2, color=colours[1], alpha=1)

    # Add a text label to the right end of every line. Most of the code below
    # is adding specific offsets y position because some labels overlapped.
    y_pos = gender_degree_data[column.replace("\n", " ")].values[-1] - 0.5
    # if column == "Foreign Languages":
    #     y_pos += 0.5
    # elif column == "English":
    #     y_pos -= 0.5
    # elif column == "Communications\nand Journalism":
    #     y_pos += 0.75
    # elif column == "Art and Performance":
    #     y_pos -= 0.25
    # elif column == "Agriculture":
    #     y_pos += 1.25
    # elif column == "Social Sciences and History":
    #     y_pos += 0.25
    # elif column == "Business":
    #     y_pos -= 0.75
    # elif column == "Math and Statistics":
    #     y_pos += 0.75
    # elif column == "Architecture":
    #     y_pos -= 0.75
    # elif column == "Computer Science":
    #     y_pos += 0.75
    # elif column == "Engineering":
    #     y_pos -= 0.25
    # Again, make sure that all labels are large enough to be easily read
    # by the viewer.
    # plt.text(2011.5, y_pos, column, fontsize=14, color=colours[rank])

    # # matplotlib's title() call centers the title on the plot, but not the graph,
    # # so I used the text() call to customize where the title goes.

    # # Make the title big enough so it spans the entire plot, but don't make it
    # # so big that it requires two lines to show.

    # # Note that if the title is descriptive enough, it is unnecessary to include
    # # axis labels; they are self-evident, in this plot's case.
    # plt.text(1995, 93, "Percentage of Bachelor's degrees conferred to women in the U.S.A."
    #        ", by major (1970-2012)", fontsize=17, ha="center")

    # # Always include your data source(s) and copyright notice! And for your
    # # data sources, tell your viewers exactly where the data came from,
    # # preferably with a direct link to the data. Just telling your viewers
    # # that you used data from the "U.S. Census Bureau" is completely useless:
    # # the U.S. Census Bureau provides all kinds of data, so how are your
    # # viewers supposed to know which data set you used?
    # plt.text(1966, -8, "Data source: nces.ed.gov/programs/digest/2013menu_tables.asp"
    #        "\nAuthor: Randy Olson (randalolson.com / @randal_olson)"
    #        "\nNote: Some majors are missing because the historical data "
    #        "is not available for them", fontsize=10)

    # Finally, save the figure as a PNG.
    # You can also save it as a PDF, JPEG, etc.
    # Just change the file extension in this call.
    # bbox_inches="tight" removes all the extra whitespace on the edges of your plot.
    plt.savefig("percent-bachelors-degrees-women-usa.png", bbox_inches="tight")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="""
            Construct and run a set of learning experiments. Provide the
            name of the config file, and which parameter you want to be shifted
            between what range, with what steps""")
    parser.add_argument("-f", "--folder_name", help="name of folder with data")
    parser.add_argument("-x", "--x_label",
                        help="the label of the x-axis")
    parser.add_argument("-y", "--y_label",
                        help="the label of the y-axis")
    parser.add_argument("-z", "--z_label",
                        help="the label of the variable across lines")
    parser.add_argument("-values", "--z_values",
                        help="...")
    args = parser.parse_args()

    multiple_plots(args.folder_name, args.x_label, args.y_label, args.z_label,
        args.z_values)
