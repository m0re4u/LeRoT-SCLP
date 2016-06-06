
class DynamicProbabilisticPerturbator(ProbabilisticPerturbator):
    """
    Application system for dynamic probabilistic perturbation on ranker
    """

    def __init__(self, delta=0.8):
        self.delta = delta
        print("Init of Dynamic Probabilistic Perturbator done")
