import random as rnd


class ProbabilisticPerturbator:
    """
    Application system for perturbation on ranker
    """

    # swap_prob 0.25, gives a good result according to papers
    def __init__(self, swap_prob=0.25):
        self.swap_prob = swap_prob
        print("Init of Perturbator done")

    def perturb(self, ranker, query, max_length):
        """
        Get a ranked list from the ranker, perform perturbation on the
        max_length amount of items
        """

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

        # Loop for perturbation swap & pairing
        for i in xrange(single_start, max_length-1, 2):
            # Swap with p(swap)
            if rnd.random() < self.swap_prob:
                new_ranked.append(ranker.next())
                new_ranked.insert(i, ranker.next())
            # Don't swap
            else:
                new_ranked.append(ranker.next())
                new_ranked.append(ranker.next())

        # Add last index if it hasn't been added yet
        if len(new_ranked) < max_length:
            new_ranked.append(ranker.next())
        return new_ranked, single_start

    def update_swap_probability(self, swap_prob):
        """
        Update the swap probability of the pertubator
        """
        self.swap_prob = swap_prob
