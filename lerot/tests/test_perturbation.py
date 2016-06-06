import unittest
import random


class TestPerturbation(unittest.TestCase):
    def setUp(self):
        # Seed the random module to be able to predict the outcome of tests
        random.seed(42)

    def test_fixed_perturbation(self):
        """
        Test whether perturbation with a fixed probability works as expected
        """
        pass


if __name__ == '__main__':
    unittest.main()
