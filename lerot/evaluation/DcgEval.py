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

import numpy as np

from .AbstractEval import AbstractEval


class DcgEval(AbstractEval):
    """Compute DCG (with gain = 2**rel-1 and log2 discount)."""

    def get_dcg(self, ranked_labels, cutoff=-1):
        if (cutoff == -1):
            cutoff = len(ranked_labels)

        rank = np.arange(cutoff)
        return ((np.power(2, np.asarray(ranked_labels[:cutoff])) - 1) /
                np.log2(2 + rank)).sum()

    def evaluate_ranking(self, ranking, query, cutoff=-1):
        """Compute NDCG for the provided ranking. The ranking is expected
        to contain document ids in rank order."""
        if cutoff == -1 or cutoff > len(ranking):
            cutoff = len(ranking)
        if query.has_ideal():
            ideal_dcg = query.get_ideal()
        else:
            ideal_labels = list(reversed(sorted(query.get_labels())))[:cutoff]
            ideal_dcg = self.get_dcg(ideal_labels, cutoff)
            query.set_ideal(ideal_dcg)

        if ideal_dcg == .0:
            # return 0 when there are no relevant documents. This is consistent
            # with letor evaluation tools; an alternative would be to return
            # 0.5 (e.g., used by the yahoo learning to rank challenge tools)
            return 0.0

        # get labels for the sorted docids
        sorted_labels = [0] * cutoff
        for i in range(cutoff):
            sorted_labels[i] = query.get_label(ranking[i])
        dcg = self.get_dcg(sorted_labels, cutoff)
        return dcg / ideal_dcg

    def get_value(self, ranking, labels, orientations, cutoff=-1):
        """
        Compute the value of the metric
        - ranking contains the list of documents to evaluate
        - labels are the relevance labels for all the documents, even those
          that are not in the ranking; labels[doc.get_id()] is the relevance of
          doc
        - orientations contains orientation values for the verticals;
          orientations[doc.get_type()] is the orientation value for the
          doc (from 0 to 1).
        """
        return self.get_dcg([labels[doc.get_id()] for doc in ranking], cutoff)
