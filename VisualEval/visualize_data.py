import matplotlib.pyplot as plt

def visualize_data(data):
    """
    Assuming we receive a list(tuple(list(eval_measure), iteration))
    make a plot and output it
    """
    plt.plot([sample[1] for sample in data],[numpy.mean(sample[0]) for sample in data])
    print(data)
    plt.xlabel("swap probability")
    plt.ylabel("nDCG")
    plt.show()
        # get mean
