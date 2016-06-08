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
Runs an online learning experiment. The "environment" logic is located here,
e.g., sampling queries, observing user clicks, external evaluation of result
lists
"""

import logging
from numpy.linalg import norm

from ..utils import get_cosine_similarity
from AbstractLearningExperiment import AbstractLearningExperiment


class LearningExperiment(AbstractLearningExperiment):
    """
    Represents an experiment in which a retrieval system learns from
    implicit user feedback. The experiment is initialized as specified in the
    provided arguments, or config file.
    """

    def run(self):
        """
        A single run of the experiment.
        """
        query_keys = sorted(self.training_queries.keys())
        query_length = len(query_keys)

        # setup evaluation
        online_evaluation = {}
        offline_test_evaluation = {}
        offline_train_evaluation = {}
        for evaluation in self.evaluations:
            online_evaluation[evaluation] = []
            offline_test_evaluation[evaluation] = []
            offline_train_evaluation[evaluation] = []
        similarities = [.0]

        # Process queries
        for query_count in xrange(self.num_queries):
            logging.debug("Query nr: {}".format(query_count))
            previous_solution_w = self.system.get_solution().w
            qid = self._sample_qid(query_keys, query_count, query_length)
            query = self.training_queries[qid]
            # get result list for the current query from the system
            result_list = self.system.get_ranked_list(query)

            # Evaluate list only
            for evaluation in self.evaluations:
                online_evaluation[evaluation].append(
                    float(self.evaluations[evaluation]['eval_class'].evaluate_ranking(
                        result_list, query, min(len(result_list), 10))))

            # generate click feedback
            clicks = self.um.get_clicks(result_list, query.get_labels())
            # send feedback to system
            current_solution = self.system.update_solution(clicks)

            # compute current offline performance (over all documents)
            for evaluation in self.evaluations:
                if (not (previous_solution_w == current_solution.w).all()) or \
                         len(offline_test_evaluation[evaluation]) == 0:
                    e1 = self.evaluations[evaluation]['eval_class'].evaluate_all(
                        current_solution, self.test_queries,
                        self.evaluations[evaluation]['test_cutoff'])
                    e2 = self.evaluations[evaluation]['eval_class'].evaluate_all(
                        current_solution, self.training_queries,
                        self.evaluations[evaluation]['train_cutoff'])
                    offline_test_evaluation[evaluation].append(float(e1))
                    offline_train_evaluation[evaluation].append(float(e2))
                else:
                    offline_test_evaluation[evaluation].append(
                                    offline_test_evaluation[evaluation][-1])
                    offline_train_evaluation[evaluation].append(
                                    offline_train_evaluation[evaluation][-1])

            similarities.append(float(get_cosine_similarity(
                                                        previous_solution_w,
                                                        current_solution.w)))

        for evaluation in self.evaluations:
            logging.info("Final offline %s = %.3f" % (
                evaluation, offline_test_evaluation[evaluation][-1]))
        logging.info("Length of final weight vector = %.3f" % norm(
            current_solution.w))
        summary = {"weight_sim": similarities, "final_weights":
                   previous_solution_w.tolist()}
        for evaluation in self.evaluations:
            summary["online_" + evaluation] = online_evaluation[evaluation]
            summary["offline_test_" + evaluation] = offline_test_evaluation[evaluation]
            summary["offline_train_" + evaluation] = offline_train_evaluation[evaluation]
        return summary
