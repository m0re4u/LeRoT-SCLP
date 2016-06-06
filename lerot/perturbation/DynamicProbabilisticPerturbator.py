
import nympy as np

class DynamicProbabilisticPerturbator(ProbabilisticPerturbator):
    """
    Application system for dynamic probabilistic perturbation on ranker
    """

    def __init__(self, delta=0.8):
        self.cum_affirm = 0
        self.delta = delta
        self.max_perturbation = 0
        print("Init of Dynamic Probabilistic Perturbator done")

    def update_affirm(self, weights, perturbed_vec, feedback_vec):
        weights = np.transpose(weights)
        new_affirm = weights * feedback_vec - weights * perturbed_vec
