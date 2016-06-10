import os
import sys
from lerot.experiment import GenericExperiment

def get_data_one_experiment(evaluation, measure):
    """
    Get the data of a single experiment with one config file
    """
    try:
        experiment = GenericExperiment()
        # Runs a number of experiments and returns a list of those experiment results
        experiment_list = experiment.run()
        offline_eval = {}
        online_eval = {}

        # Loop over results of all runs
        # You can call:
        #   single_run["online_"+experiment.experiment_args["evaluation"][0]]
        #   single_run["offline_test_"+experiment.experiment_args["evaluation"][0]]
        #   single_run["offline_train_"+experiment.experiment_args["evaluation"][0]]

        # Get names for evaluation measures
        eval_names = [eval_name for eval_name in experiment_list[0]]
        for eval_name in eval_names:
            if eval_name == 'weight_sim' or eval_name == 'final_weights':
                continue
            splitted_eval_name = eval_name.split('@')[0]
            online_eval[splitted_eval_name] = []
            offline_eval[splitted_eval_name] = []
            for single_run in experiment_list:
                if 'online' in eval_name:
                    online_eval[splitted_eval_name].append(single_run[eval_name])
                else:
                    offline_eval[splitted_eval_name].append(single_run[eval_name])

        if 'online' in evaluation:
            return online_eval[evaluation + "_evaluation." + measure]
        else:
            return offline_eval[evaluation + "_evaluation." + measure]

    except BaseException as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
