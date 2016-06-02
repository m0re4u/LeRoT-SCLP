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

# KH, 2012/06/14
"""
Retrieval system implementation for use in learning experiments.
"""

import argparse
import logging

from .AbstractLearningSystem import AbstractLearningSystem
from ..utils import get_class, split_arg_str


class PerturbationLearningSystem(AbstractLearningSystem):
    """A retrieval system that learns online from pairwise comparisons. The
    system keeps track of all necessary state variables (current query,
    weights, etc.) so that comparison and learning classes can be stateless
    (implement only static / class methods)."""

    def __init__(self, feature_count, arg_str):
        # parse arguments
        parser = argparse.ArgumentParser(
            description="Initialize retrieval "
            "system with the specified feedback and learning mechanism.",
            prog="PerturbationLearningSystem"
        )
        parser.add_argument("-w", "--init_weights", help="Initialization "
                            "method for weights (random, zero).",
                            required=True)

        # Perturbation arguments
        parser.add_argument("-p", "--perturbator", required=True)
        parser.add_argument("-b", "--swap_prob", default=0.25, type=float)
        # parser.add_argument("-f", "--perturbator_args", nargs="*")

        parser.add_argument("-r", "--ranker", required=True)
        parser.add_argument("-s", "--ranker_args", nargs="*")
        parser.add_argument("-t", "--ranker_tie", default="random")

        parser.add_argument("-l", "--max_results", default=10)

        args = vars(parser.parse_known_args(split_arg_str(arg_str))[0])

        self.ranker_class = get_class(args["ranker"])
        self.ranker_args = args["ranker_args"]
        self.ranker_tie = args["ranker_tie"]
        self.init_weights = args["init_weights"]
        self.feature_count = feature_count
        self.ranker = self.ranker_class(
            self.ranker_args,
            self.ranker_tie,
            self.feature_count,
            sample=None,  # explicitly break sampling
            init=self.init_weights
        )

        self.max_results = args["max_results"]

        # Comparison that should be replaced by perturbation again
        # Perturbator perturbator = new Perturbator(args["swap_prob"])
        # self.perturbator = perturbator
        self.perturbator = get_class(args["perturbator"])(args["swap_prob"])
        # if "perturbator_args" not in args or args["perturbator_args"] is None:
        #     self.perturbator_args = []
        #     " ".join(args["perturbator_args"])
        #     self.perturbator_args = self.perturbator_args.strip("\"")
        # else:
        #     self.perturbator_args = None
        # self.perturbator = self.perturbator_class(*self.perturbator_args)
        # self.query_count = 0

    def get_ranked_list(self, query):  # , getNewCandidate=True):
        (l, context) = self.perturbator.perturb(self.ranker, query,
                                                self.max_results)
        logging.info(l)
        logging.info(context)
        self.current_l = l
        self.current_context = context
        self.current_query = query
        return l

    def update_solution(self, clicks):
        # feedback_ranking = self.perturbater.get_feedback(self.current_l, clicks, pairs)
        outcome = self.perturbator.infer_outcome(self.current_l,
                                                 self.current_context,
                                                 clicks,
                                                 self.current_query)
        # Update weights!

        # if outcome > 0:
        #     self.ranker.update_weights(self.current_u, self.alpha)
        return self.get_solution()

    def get_solution(self):
        return self.ranker
