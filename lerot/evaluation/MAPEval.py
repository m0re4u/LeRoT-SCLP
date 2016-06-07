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

import numpy as np

from collections import defaultdict
from .AbstractEval import AbstractEval

TOP_DOCUMENTS_CHECKED = 10

class MAPEval(AbstractEval):
    
    def evaluate_ranking(self, ranking, query, cutoff=-1):
        # print(cutoff)
        # print(ranking)
        # print(len(ranking))
        # print(query.get_labels())
        # print('=======================')
        if cutoff == -1 or cutoff > len(ranking):
            cutoff = len(ranking)
        stats_by_vert = defaultdict(lambda: {'total': 0, 'rel': 0})
        for d in ranking[:cutoff]:
            # print(d.get_id())
            # print(len(ranking))
            # print("==========")
            vert = d.get_type()
            stats_by_vert[vert]['total'] += 1
            if query.get_labels()[d.get_id()] == 1:
                stats_by_vert[vert]['rel'] += 1
        precisions = [float(s['rel']) / s['total'] for s in stats_by_vert.itervalues()]
        if len(precisions) == 0:
            return 0.0
        return float(sum(precisions)) / len(precisions)