import unittest
import random
import cStringIO
import lerot.query as query
import lerot.ranker.DeterministicRankingFunction as DRF


class TestPerturbation(unittest.TestCase):
    def setUp(self):
        # Seed the random module to be able to predict the outcome of tests
        random.seed(42)

    def test_fixed_perturbation(self):
        """
        Test whether perturbation with a fixed probability works as expected
        """
        test_queries = """
        1 qid:373 1:0.089908 2:0.531250 3:0.500000 4:0.500000 5:0.156538
        0 qid:373 1:0.066055 2:0.171875 3:0.000000 4:0.250000 5:0.084715
        0 qid:373 1:0.148624 2:0.015625 3:0.250000 4:0.250000 5:0.151013
        0 qid:373 1:0.099083 2:0.250000 3:0.500000 4:0.750000 5:0.134438
        0 qid:373 1:0.051376 2:0.078125 3:0.250000 4:0.250000 5:0.060773
        0 qid:373 1:0.045872 2:1.000000 3:0.250000 4:0.250000 5:0.163904
        """
        ranker_args = ['3']
        ranker_tie = 'random'
        init_weights = 'random'
        feature_count = 10
        ranker = DRF(
            ranker_args,
            ranker_tie,
            feature_count,
            sample=None,
            init=init_weights
        )
        query_fh = cStringIO.StringIO(test_queries)
        queries = query.Queries(query_fh, feature_count)
        query_fh.close()


if __name__ == '__main__':
    unittest.main()
