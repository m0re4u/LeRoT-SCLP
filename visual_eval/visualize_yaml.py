import argparse
import numpy
import gzip
import os
import yaml
from multiple_plots import multiple_plots


def visualize_yaml(evaluation, folder, x, y, z, max_bound, title, mean=False):
    """
    Visualize the specified evaluation from the folder given.
    Setting the mean flag will assume each file is one run, and take the
    average over runs.
    """

    x_data = []
    y_data = []
    y_pos = []
    z_labels = []

    if evaluation == "offline":
        evaluation = "offline_test"

    for filename in os.listdir(folder):
        x_data, y_data, y_pos, z_labels = open_file(evaluation, filename,
            folder, x_data, y, y_data, y_pos, z, z_labels, mean)

    # if mean:
    #     x_mean = numpy.mean(x_data, axis=0)
    #     y_mean = numpy.mean(y_data, axis=0)
    #     multiple_plots([x_mean], [y_mean], y_pos, max_bound, title, x,
    #                    y, z_labels)
    # else:
    multiple_plots(x_data, y_data, y_pos, max_bound, title, x, y, z_labels)

def open_file(evaluation, filename, folder, x_data, y, y_data, y_pos, z, z_labels, mean):

    if os.path.isdir(os.path.join(folder,filename)):
        new_folder = os.path.join(folder,filename)
        temp_x = []
        temp_y = []
        temp_y_pos = []
        temp_z = []
        for file in os.listdir(new_folder):
            temp_x, temp_y, temp_y_pos, temp_z = open_file(evaluation, file,
                new_folder, temp_x, y, temp_y, temp_y_pos, z, temp_z, mean)
        if mean:
            x_data.append(numpy.mean(temp_x, axis=0))
            y_data.append(numpy.mean(temp_y, axis=0))
            y_pos.append(numpy.mean(temp_y_pos, axis=0))
            z_labels.append(filename.split('@')[0])
    else:
        data = None
        _, ext = os.path.splitext(filename)
        # Exclude some standard files that are normally in the folder generated
        # by an experiment(particularly LearningExperiment)
        if ext == '.gz' and not filename.startswith('_'):

            with gzip.open(os.path.join(folder, filename), 'r') as data_file:
                print("Reading " + str(filename))
                data = yaml.load(data_file.read())

            z_labels.append(z + " " + filename.split("@")[0])

            for measure in data:
                if evaluation in measure and y in measure:
                   data = data[measure]

            y_data.append(data)
            x_data.append(list(range(1, len(data)+1)))
            y_pos.append(data[-1])

    return (x_data, y_data, y_pos, z_labels)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="""
            Construct and run a set of learning experiments. Provide the
            name of the config file, and which parameter you want to be shifted
            between what range, with what steps""")
    parser.add_argument("-f", "--folder_name", help="name of folder with data")
    parser.add_argument("-m", "--measure", help="offline or online evaluation")
    parser.add_argument("-x", "--x_label", help="label for x-axis")
    parser.add_argument("-y", "--y_label", help="label for y-axis")
    parser.add_argument("-z", "--z_label", help="label for z-axis")
    parser.add_argument("-max", "--max_bound",
                        help="maximum number for x-axis", type=int)
    parser.add_argument("-title", help="title for plot")
    parser.add_argument("-mean", help="take the average of all evals",
                        type=bool)
    args = parser.parse_args()

    visualize_yaml(args.measure, args.folder_name, args.x_label, args.y_label,
                   args.z_label, args.max_bound, args.title, args.mean)
