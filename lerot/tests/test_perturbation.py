import os
import sys
import unittest

sys.path.insert(0, os.path.abspath('..'))


class TestQuery(unittest.TestCase):
    def test_join(self):
        """This is an example test function"""
        self.assertEqual("Some string", ' '.join(["Some", "string"]))


if __name__ == '__main__':
    unittest.main()
