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


def overlap(positions, size):
    positions = sorted(positions)
    for pos, next_pos in zip(positions, positions[1:]):
        if pos + size > next_pos:
            return True
    return False


def multiple_plots(x_data, y_data, y_pos, max_bound, ymin, ymax, title,
                   x_label, y_label, z_label, logarithmic):
    """
    Plot data of multiple files in one graph.
    """

    # Set figure size
    plt.figure(figsize=(15, 10))

    # Set visibility of plot frame lines
    kwargs = {"xscale": "log"} if logarithmic else {}
    ax = plt.axes(**kwargs)
    ax.spines["top"].set_visible(False)
    ax.spines["bottom"].set_visible(True)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(True)

    # Add major grid lines
    ax.grid(
        which='major',
        axis='y',
        linestyle='--',
        linewidth=0.5,
        color='black',
        alpha=0.5
    )

    # Limit the range of the plot to where the data is
    plt.ylim(ymin, ymax)
    plt.xlim(1, max_bound)

    # Remove the tick marks at top and right
    plt.tick_params(axis="both", which="both", bottom="on", top="off",
                    labelbottom="on", left="on", right="off", labelleft="on",
                    labelsize=20)

    # Plot all data and apply magic to the labels.
    # I apologise for the following code.
    MAX_LABELS, FONTSIZE, PADDING = 25, 17, 4  # Empirically tested (I'm sorry)
    labelsize = (ymax - ymin) / float(MAX_LABELS)
    paddingsize = labelsize / FONTSIZE * PADDING
    labels = []
    for x_datum, y_datum, color, y, label in zip(x_data, y_data, COLOURS,
                                                 y_pos, z_label):
        plt.plot(x_datum, y_datum, lw=2, color=color, label=label)

        # Add a text label to the right end of every line and centre it
        labels.append({
            'label': label,
            'position': y - labelsize / 2. + paddingsize,
            'color': color
        })

    labels = sorted(labels, key=lambda a: a['position'])

    while overlap([l['position'] for l in labels], labelsize):
        # Calculate the "force" on every label (in distance to be moved)
        forces = [0.0 for _ in labels]
        for this_i, next_pos in enumerate(l['position'] for l in labels[1:]):
            this_pos = labels[this_i]['position']
            force = (labelsize + this_pos - next_pos) / 2.
            if force > 0:
                forces[this_i] -= force
                forces[this_i + 1] += force

        # Apply forces
        for i, force in enumerate(forces):
            labels[i]['position'] += force

    # Plot labels
    for label in labels:
        plt.text(max_bound + 10, label['position'], label['label'],
                 fontsize=FONTSIZE, color=label['color'])

    # Add labels to axes
    plt.xlabel(x_label, size=30)
    plt.ylabel(y_label, size=30)

    # Save plot as picture
    plt.savefig(title + ".png", bbox_inches="tight", transparent=True)
