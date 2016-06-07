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

# KH, 2012/06/20

from random import sample
from numpy import mean


class MAPEval:
    """Abstract base class for computing evaluation metrics for given relevance
    labels."""

    def __init__(self):
        self.prev_solution_w = None
        self.prev_score = None

    def evaluate_all(self, solution, queries, cutoff=-1, ties="random"):
        if self.prev_solution_w is not None and (self.prev_solution_w ==
                                             solution.w).all():
            return self.prev_score
        outcomes = []
        for query in queries:
            outcomes.append(self.evaluate_one(solution, query, cutoff, ties))
        score = mean(outcomes)

        self.prev_solution_w = solution.w
        self.prev_score = score

        return score

    def evaluate_one(self, solution, query, cutoff=-1, ties="random"):
        scores = solution.score(query.get_feature_vectors())
        sorted_docs = self._sort_docids_by_score(query.get_docids(), scores,
            ties=ties)
        return self.evaluate_ranking(sorted_docs, query, cutoff)

    def evaluate_ranking(self, ranking, query, cutoff=-1):
        if cutoff == -1:
            cutoff = len(labels)
        stats_by_vert = defaultdict(lambda: {'total': 0, 'rel': 0})
        for d in ranking[:cutoff]:
            vert = d.get_type()
            if vert == 'Web':
                continue
            stats_by_vert[vert]['total'] += 1
            if labels[d.get_id()] > 0:
                stats_by_vert[vert]['rel'] += 1
        precisions = [float(s['rel']) / s['total'] for s in stats_by_vert.itervalues()]
        if len(precisions) == 0:
            return 0.0
        return float(sum(precisions)) / len(precisions)