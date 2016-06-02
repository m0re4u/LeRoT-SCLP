from form_pairs import form_pairs
import random as rnd
"""
Application system for perturbation on ranker
"""
class Perturbator:

        def __init__(self, swap_prob)
            self.swap_prob = swap_prob
        print("Init of Perturbator done")

    """
    Get a ranked list form the ranker, preform perturbation on the max_el amount of items
    """
    def perturb(self, ranker, max_length, query)
        # Create ranked list given query and ranker
        ranked_list = ranker.init_ranking(query)
        max_length = min(ranked_list.document_count(), max_length)
        # Set flag for single start
        single_start = True

        # Start with pair calculation
        if rnd.randint(0, 1):
            new_ranked = []
            single_start = False
        else:
            new_ranked = [ranked_list.next()]

        # Loop for perturbation    
        for i in xrange(len(new_ranked), max_length-1, 2):
            if rnd.random() < swap_prob and i+1 < max_length-1:
                new_ranked[i+1] = ranked_list.next()
                new_ranked[i] = ranked_list.next()
                
        # Add last index if it hasn't been added yet
        if (single_start and max_length % 2 == 0) or
            (not single_start and max_length % 2 != 0):
            new_ranked.append(ranked_list.next())
        return new_ranked, single_start
