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

import numpy as np
from .ProbabilisticPerturbator import ProbabilisticPerturbator
from ..utils import create_ranking_vector

class DynamicProbabilisticPerturbator(ProbabilisticPerturbator):
    """
    Application system for dynamic probabilistic perturbation on ranker
    """

    def __init__(self, delta=0.8):
        self.cum_affirm = 0
        self.t = 1
        self.swap_prob = 0
        print("Init of Dynamic Probabilistic Perturbator done")

    def update_affirm(self, feedback_vec, perturbed_vec, query, ranker):
        """
        Update the cumulative affirmativeness with the affirmativeness of
        the last iteration
        """
        #perturbed_feature_vec = create_ranking_vector(query, perturbed_vec)
        #feedback_feature_vec = create_ranking_vector(query, feedback_vec)

        weights = np.transpose(ranker.w)
        new_affirm = np.dot(weights,feedback_vec) - np.dot(weights,perturbed_vec)
        print(np.dot(weights,feedback_vec))
        print(np.dot(weights,perturbed_vec))
        self.cum_affirm += new_affirm


    def _calc_max_affirm(self, ranker, query, max_length):
        """
        Calculate the maximum perturbation for the original
        ranking of this iteration
        """
        # Calculate feature vector for original ranking
        ranker.init_ranking(query)
        ranking = self.ranker_to_list(ranker, max_length)
        org_feature_vec = create_ranking_vector(query, ranking)

        # Calculate feature vector for maximum swap ranking
        self.update_swap_probability(2.0)
        max_ranking, single_start = self.perturb(ranker, query, max_length)
        max_feature_vec = create_ranking_vector(query, max_ranking)

        weights = np.transpose(ranker.w)
        return np.dot(weights,org_feature_vec) - np.dot(weights, max_feature_vec)

    def perturb_dynamically(self, ranker, query, max_length):
        """
        Calculate perturbed ranking with swap probability
        based on maximum perturbation and the cumulative affirmativeness
        """

        # Calc the maximum perturbation
        max_affirm = self._calc_max_affirm(ranker,
            query, max_length)

        # Calculate swap probability and ranking
        #print((self.delta*self.t - self.cum_affirm) / max_affirm)
        if self.t > 1:
            delta = self.cum_affirm / self.t - 1
        else:
            delta = 0

        swap_prob = max(0,(delta*self.t - self.cum_affirm) / max_affirm)
        #print(swap_prob)
        self.update_swap_probability(swap_prob)
        self.t += 1
        print(self.get_swap_probability())
        return self.perturb(ranker, query, max_length)

    def ranker_to_list(self, ranker, max_length):
        """
        Extract the ranking from a ranker,
        put it in a list
        """
        new_ranked = []

        if max_length is None:
            max_length = ranker.document_count()
        else:
            max_length = min(ranker.document_count(), max_length)

        for i in range(max_length):
            new_ranked.append(ranker.next())
        return new_ranked
