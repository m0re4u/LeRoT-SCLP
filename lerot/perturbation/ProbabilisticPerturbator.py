
import random as rnd
"""
Application system for perturbation on ranker
"""


class ProbabilisticPerturbator:

    # swap_prob 0.25, gives a good result according to papers
    def __init__(self, swap_prob=0.25):
        self.swap_prob = swap_prob
    print("Init of Perturbator done")

    """
    Get a ranked list form the ranker, preform perturbation on the
    max_length amount of items
    """
    def perturb(self, ranker, query, max_length):
        # Create ranked list given query and ranker
        ranker.init_ranking(query)
        max_length = min(ranker.document_count(), max_length)

        # Set flag for single start
        # Start with pair calculation
        if rnd.randint(0, 1):
            new_ranked = []
            single_start = False
        else:
            single_start = True
            new_ranked = [ranker.next()]

        # Loop for perturbation
        for i in xrange(single_start, max_length-1, 2):
            if rnd.random() < self.swap_prob:
                new_ranked.append(ranker.next())
                new_ranked[i:i] = [ranker.next()]
            else:
                new_ranked.append(ranker.next())
                new_ranked.append(ranker.next())

        # Add last index if it hasn't been added yet
        if len(new_ranked) < max_length:
            new_ranked.append(ranker.next())
        return new_ranked, single_start
