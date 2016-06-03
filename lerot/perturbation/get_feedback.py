
def get_feedback(clicks, documents, single_start):
    """
    Get a new ranking of documents, swapped according to user clicks
    """

    max_length = len(documents)

    # Check whether new ranking should start with a single start
    if single_start:
        single_start = True
        new_ranked = [documents[0]]
    else:
        new_ranked = []
        single_start = False

    # Loop for swapping pairs of documents according to clicks
    for i in xrange(single_start, max_length-1, 2):
        # Swap if there is a click on the lower item of a pair
        if clicks[i+1]: # ANDERE IF-STATEMENT
            new_ranked.append(documents[i+1])
            new_ranked.append(documents[i])
        # Don't swap
        else:
            new_ranked.append(documents[i])
            new_ranked.append(documents[i+1])


    # Add last index if it hasn't been added yet
    if len(new_ranked) < max_length:
        new_ranked.append(ranker.next())

    return new_ranked
    