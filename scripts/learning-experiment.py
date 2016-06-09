#!/usr/bin/env python

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
import logging
import numpy
try:
    from include import *
except:
    pass
from lerot.experiment.GenericExperiment import GenericExperiment

if __name__ == "__main__":
    # Creates an experiment that can be iterated over
    experiment = GenericExperiment()
    # Runs a number of experiments and returns a list of those experiment
    # results
    experiment_list = experiment.run()
    offline_eval = {}
    online_eval = {}

    # Loop over results of all runs
    # You can call:
    #   single_run["online_"+experiment.experiment_args["evaluation"][0]]
    #   single_run["offline_test_"+experiment.experiment_args["evaluation"][0]]
    #   single_run["offline_train_"+experiment.experiment_args["evaluation"][0]]
    for evaluation_string in experiment.experiment_args["evaluation"]:
        evaluation_type = str(evaluation_string.split()[0])
        online_eval[evaluation_type] = []
        offline_eval[evaluation_type] = []
        for single_run in experiment_list:
            online_eval[evaluation_type].append(single_run["online_" + evaluation_type][-1])
            offline_eval[evaluation_type].append(single_run["offline_train_" + evaluation_type][-1])

        logging.info(" ===== RESULTS for " + evaluation_type + " : =====")
        # ONLINE
        logging.info(" ----- ONLINE: -----")
        logging.info(evaluation_type + " mean: " + str(numpy.mean(online_eval[evaluation_type])))
        logging.info(evaluation_type + " std: " + str(numpy.std(online_eval[evaluation_type])))
        logging.info(evaluation_type + " Max: " + str(max(online_eval[evaluation_type])))
        logging.info(evaluation_type + " Min: " + str(min(online_eval[evaluation_type])))
        # OFFLINE
        logging.info(" ----- OFFLINE: -----")
        logging.info(evaluation_type + " mean: " + str(numpy.mean(offline_eval[evaluation_type])))
        logging.info(evaluation_type + " std: " + str(numpy.std(offline_eval[evaluation_type])))
        logging.info(evaluation_type + " Max: " + str(max(offline_eval[evaluation_type])))
        logging.info(evaluation_type + " Min: " + str(min(offline_eval[evaluation_type])))
