from lerot.experiment import GenericExperiment

def get_data_one_experiment():
    """
    Get the data of a single experiment with one config file
    """
    experiment = GenericExperiment()
    # Runs a number of experiments and returns a list of those experiment results
    experiment_list = experiment.run()

    offline_ndcg_eval_list = []
    # Gather ndcg results of all runs
    for experiment in experiment_list:
        offline_ndcg_eval_list.append(experiment["offline_train_evaluation.NdcgEval"][-1])

    return offline_ndcg_eval_list
