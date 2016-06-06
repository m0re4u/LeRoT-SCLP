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

import nympy as np

class DynamicProbabilisticPerturbator(ProbabilisticPerturbator):
    """
    Application system for dynamic probabilistic perturbation on ranker
    """

    def __init__(self, delta=0.8):
        self.cum_affirm = 0
        self.delta = delta
        self.max_perturbation = 0
        print("Init of Dynamic Probabilistic Perturbator done")

    def update_affirm(self, weights, perturbed_vec, feedback_vec):
        weights = np.transpose(weights)
        new_affirm = weights * feedback_vec - weights * perturbed_vec
