import matplotlib.pyplot as plt


# 20 RGB colours
COLOURS = [
    (r / 255., g / 255., b / 255.) for r, g, b in
    [
        (31, 119, 180),  # (174, 199, 232),
        (255, 127, 14),  # (255, 187, 120),
        (44, 160, 44),  # (152, 223, 138),
        (214, 39, 40),  # (255, 152, 150),
        (148, 103, 189),  # (197, 176, 213),
        (140, 86, 75),  # (196, 156, 148),
        (227, 119, 194),  # (247, 182, 210),
        (127, 127, 127),  # (199, 199, 199),
        (188, 189, 34),  # (219, 219, 141),
        (23, 190, 207),  # (158, 218, 229)
    ]
]


def multiple_plots(x_data, y_data, y_pos, max_bound, ymin, ymax, title,
                   x_label, y_label, z_label):
    """
    Plot data of multiple files in one graph.
    """

    # Set figure size
    plt.figure(figsize=(15, 10))

    # Set visibility of plot frame lines
    ax = plt.axes()
    ax.spines["top"].set_visible(False)
    ax.spines["bottom"].set_visible(True)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(True)

    # Limit the range of the plot to where the data is
    plt.ylim(ymin, ymax)
    plt.xlim(0, max_bound)

    # Remove the tick marks at top and right
    plt.tick_params(axis="both", which="both", bottom="on", top="off",
                    labelbottom="on", left="on", right="off", labelleft="on",
                    labelsize=20)

    # Add major grid lines
    ax.grid(
        which='major',
        axis='y',
        linestyle='--',
        linewidth=0.5,
        color='black',
        alpha=0.5
    )

    # Plot all data
    for x_datum, y_datum, color, y, z in zip(x_data, y_data, COLOURS, y_pos,
                                             z_label):
        plt.plot(x_datum, y_datum, lw=2, color=color)

        # Add a text label to the right end of every line
        plt.text(max_bound + 5, y, z,
                 fontsize=17, color=color)

    # Add labels to axes
    plt.xlabel(x_label, size=26)
    plt.ylabel(y_label, size=26)

    # Save plot as picture
    plt.savefig(title + ".png", bbox_inches="tight")
