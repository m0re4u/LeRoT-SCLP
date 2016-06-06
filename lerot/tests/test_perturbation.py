import os
import sys
import unittest

sys.path.insert(0, os.path.abspath('..'))


class TestQuery(unittest.TestCase):
    def test_fixed_perturbation(self):
        """
        Test whether perturbation with a fixed probability works as expected
        """
        pass


if __name__ == '__main__':
    unittest.main()
