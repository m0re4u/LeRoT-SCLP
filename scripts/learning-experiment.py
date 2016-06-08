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
    offline_ndcg_eval_list = []
    online_ndcg_eval_list = []

    # Loop over results of all runs
    # You can call:
    #   single_run["online_" + evaluation_type][-1]
    #   single_run["offline_test_" + evaluation_type][-1]
    #   single_run["offline_train_" + evaluation_type][-1]
    evaluation_type = str(experiment.experiment_args["evaluation"][0])

    for single_run in experiment_list:
        offline_ndcg_eval_list.append(single_run["offline_train_" + evaluation_type][-1])
        online_ndcg_eval_list.append(single_run["online_" + evaluation_type][-1])
    logging.info(" ===== RESULTS: =====")
    # ONLINE
    logging.info(" ----- ONLINE: -----")
    logging.info(evaluation_type + " Mean: " + str(numpy.mean(online_ndcg_eval_list)))
    logging.info(evaluation_type + " Std: " + str(numpy.std(online_ndcg_eval_list)))
    logging.info(evaluation_type + " Max: " + str(max(online_ndcg_eval_list)))
    logging.info(evaluation_type + " Min: " + str(min(online_ndcg_eval_list)))
    # OFFLINE
    logging.info(" ----- OFFLINE: -----")
    logging.info(evaluation_type + " Mean: " + str(numpy.mean(offline_ndcg_eval_list)))
    logging.info(evaluation_type + " Std: " + str(numpy.std(offline_ndcg_eval_list)))
    logging.info(evaluation_type + " Max: " + str(max(offline_ndcg_eval_list)))
    logging.info(evaluation_type + " Min: " + str(min(offline_ndcg_eval_list)))
