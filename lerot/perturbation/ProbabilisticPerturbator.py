# This file is part of Lerot.
#
# Lerot is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Lerot is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Lerot.  If not, see <http://www.gnu.org/licenses/>.

import random as rnd


class ProbabilisticPerturbator(object):
    """
    Application system for perturbation on ranker
    """

    # swap_prob 0.25, gives a good result according to papers
    def __init__(self, swap_prob=0.25):
        self.swap_prob = swap_prob

    def perturb(self, ranker, query, max_length=None):
        """
        Get a ranked list from the ranker, perform perturbation on the
        max_length amount of items
        """

        # Create ranked list given query and ranker
        ranker.init_ranking(query)
        if max_length is None:
            max_length = ranker.document_count()
        else:
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

    def get_swap_probability(self):
        """
        Return the current swap probability
        """
        return self.swap_prob
