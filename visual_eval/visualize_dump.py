import visualize_data

def visualize_dump(file):
    """
    Visualize a datadump file with visualize_data
    """
    data = []
    with open(file, 'r'):
        data = f.read()
    visualize_data(data)
