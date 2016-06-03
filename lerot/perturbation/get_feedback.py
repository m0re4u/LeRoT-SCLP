
def get_feedback(current_ranking, clicks, pairs):
    """
    Get a new ranking, swapped according to user clicks
    """
    
    feedback_ranking = current_ranking
    for pair in pairs:
        if len(pair) == 1:
            continue
        else:
            # lower and upper are indices of elements in current_ranking
            lower, upper = pair
        # if lower is clicked and upper is not, swap the two
        if lower in clicks and upper not in clicks:
            feedback_ranking[upper], feedback_ranking[lower] = \
                feedback_ranking[lower], feedback_ranking[upper]

    return feedback_ranking
