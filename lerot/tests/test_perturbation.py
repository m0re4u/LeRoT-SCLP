import unittest
import random
import numpy
import cStringIO
import lerot.query as query
import lerot.ranker.DeterministicRankingFunction as DRF
import lerot.perturbation.ProbabilisticPerturbator as ProbabilisticPerturbator


class TestPerturbation(unittest.TestCase):
    def setUp(self):
        # Seed the random modules to be able to predict the outcome of tests
        random.seed(42)
        numpy.random.seed(42)

        # Create ranker to test with
        ranker_args = ['3']
        ranker_tie = 'random'
        init_weights = 'random'
        feature_count = 5
        self.ranker = DRF(
            ranker_args,
            ranker_tie,
            feature_count,
            sample=None,
            init=init_weights
        )

        # Create queries to test with
        test_queries = """
        1 qid:373 1:0.089908 2:0.531250 3:0.500000 4:0.500000 5:0.156538
        0 qid:373 1:0.066055 2:0.171875 3:0.000000 4:0.250000 5:0.084715
        0 qid:373 1:0.148624 2:0.015625 3:0.250000 4:0.250000 5:0.151013
        0 qid:373 1:0.099083 2:0.250000 3:0.500000 4:0.750000 5:0.134438
        0 qid:373 1:0.051376 2:0.078125 3:0.250000 4:0.250000 5:0.060773
        0 qid:373 1:0.045872 2:1.000000 3:0.250000 4:0.250000 5:0.163904
        """
        query_fh = cStringIO.StringIO(test_queries)
        self.query = query.Queries(query_fh, feature_count)['373']
        query_fh.close()

        # Save the original ranking
        self.ranker.init_ranking(self.query)
        self.ranking = [
            self.ranker.next() for _ in range(self.ranker.document_count())
        ]

    def test_prob_0(self):
        """
        Test perturbing with a probability of 0
        """
        new_ranked, single_start = ProbabilisticPerturbator(0).perturb(
            self.ranker,
            self.query
        )
        self.assertEqual(new_ranked, self.ranking)


if __name__ == '__main__':
    unittest.main()
