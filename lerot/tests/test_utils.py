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

import unittest
import lerot.utils as utils


class TestUtils(unittest.TestCase):

    def setUp(self):
        pass

    def testSplitArgStr(self):
        split = utils.split_arg_str("--a 10 --b foo --c \"--d bar --e 42\"")
        self.assertEqual(split, ["--a", "10", "--b", "foo", "--c",
            "--d bar --e 42"], "wrong split (1): %s" % ", ".join(split))
        split = utils.split_arg_str("\"--a\" 10 --b foo --c --d bar --e 42")
        self.assertEqual(split, ["--a", "10", "--b", "foo", "--c", "--d",
            "bar", "--e", "42"], "wrong split (2): %s" % ", ".join(split))
        split = utils.split_arg_str("\"--a\"\" 10\"--b foo --c --d bar --e 42")
        self.assertEqual(split, ["--a", " 10", "--b", "foo", "--c", "--d",
            "bar", "--e", "42"], "wrong split (2): %s" % ", ".join(split))

    def testRank(self):
        scores = [2.1, 2.9, 2.3, 2.3, 5.5]
        self.assertIn(utils.rank(scores, ties="random"),
                      [[0, 3, 1, 2, 4], [0, 3, 2, 1, 4]])
        self.assertIn(utils.rank(scores, reverse=True, ties="random"),
                      [[4, 1, 3, 2, 0], [4, 1, 2, 3, 0]])
        self.assertEqual(utils.rank(scores, reverse=True, ties="first"),
                         [4, 1, 2, 3, 0])
        self.assertEqual(utils.rank(scores, reverse=True, ties="last"),
                         [4, 1, 3, 2, 0])

        scores = [2.1, 2.9, 2.3, 2.3, 5.5, 2.9]
        self.assertIn(utils.rank(scores, ties="random"),
                      [[0, 4, 2, 1, 5, 3],
                       [0, 3, 2, 1, 5, 4],
                       [0, 4, 1, 2, 5, 3],
                       [0, 3, 1, 2, 5, 4]])
        self.assertIn(utils.rank(scores, reverse=True, ties="random"),
                      [[5, 1, 3, 4, 0, 2],
                       [5, 2, 3, 4, 0, 1],
                       [5, 1, 4, 3, 0, 2],
                       [5, 2, 4, 3, 0, 1]])
        self.assertEqual(utils.rank(scores, reverse=True, ties="first"),
                         [5, 1, 3, 4, 0, 2])
        self.assertEqual(utils.rank(scores, reverse=True, ties="last"),
                         [5, 2, 4, 3, 0, 1])


if __name__ == '__main__':
    unittest.main()
