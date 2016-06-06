
import numpy as np
from .ProbabilisticPerturbator import ProbabilisticPerturbator
from ..utils import create_ranking_vector

class DynamicProbabilisticPerturbator(ProbabilisticPerturbator):
    """
    Application system for dynamic probabilistic perturbation on ranker
    """

    def __init__(self, delta=0.8):
        self.cum_affirm = 0
        self.delta = delta
        self.t = 1
        print("Init of Dynamic Probabilistic Perturbator done")

    def update_affirm(self, query, weights, perturbed_vec, feedback_vec):
        """
        Update the cumulative affirmativeness with the affirmativeness of
        the last iteration
        """
        perturbed_feature_vec = create_ranking_vector(query, perturbed_vec)
        feedback_feature_vec = create_ranking_vector(query, feedback_vec)

        weights = np.transpose(weights)
        new_affirm = weights * feedback_feature_vec - weights * perturbed_feature_vec
        self.cum_affirm += new_affirm

    def _calc_max_perturbation(self, ranker, query, weights):
        """
        Calculate the maximum perturbation for the original
        ranking of this iteration
        """
        # Calculate feature vector for original ranking
        ranking = ranker_to_list(ranker.init_ranking(query))
        org_feature_vec = create_ranking_vector(query, ranking)

        # Calculate feature vector for maximum swap ranking
        self.update_swap_probability(2.0)
        max_ranking = self.perturb(self, ranker, query, max_length)
        max_feature_vec = create_ranking_vector(query, max_ranking)

        weights = np.transpose(weights)
        return weights * original_vec - weights * max_vec

    def perturb_dynamically(self, weights, ranker, query, max_length):
        """
        Calculate perturbed ranking with swap probability
        based on maximum perturbation and the cumulative affirmativeness
        """

        # Calc the maximum perturbation
        max_perturbation = self._calc_max_perturbation(self, ranker,
            query, weights)

        # Calculate swap probability and ranking
        swap_prob = max(0,(delta*t - cum_affirm) / max_perturbation)
        self.update_swap_probability(swap_prob)
        return self.perturb(self, ranker, query, max_length)

    def ranker_to_list(ranker):
        new_ranked = []

        for i in range(0,len(ranker.docids)):
            new_ranked.append(ranker.next())
        return new_ranked
