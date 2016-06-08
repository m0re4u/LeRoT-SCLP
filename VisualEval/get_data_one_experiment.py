import os
import sys
from lerot.experiment import GenericExperiment
def get_data_one_experiment():
    """
    Get the data of a single experiment with one config file
    """
    try:
        experiment = GenericExperiment()
        # Runs a number of experiments and returns a list of those experiment results
        experiment_list = experiment.run()

        offline_ndcg_eval_list = []
        # Gather ndcg results of all runs
        for experiment in experiment_list:
            offline_ndcg_eval_list.append(experiment["offline_train_evaluation.NdcgEval"][-1])

        return offline_ndcg_eval_list
    except BaseException as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
