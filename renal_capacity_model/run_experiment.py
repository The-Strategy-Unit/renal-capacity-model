import simpy
from config import g
from experiment import patient_generator


def single_run(experiment, rep=0, run_length=g.run_length):
    """
    Perform a single run of the model and return the results

    Parameters:
    -----------

    experiment: Experiment
        The experiment/paramaters to use with model

    rep: int
        The replication number.

    rc_period: float, optional (default=g.run_length)
        The run length of the model
    """

    # reset all results variables to zero and empty
    experiment.init_results_variables()

    # set random number set to the replication no.
    # this controls sampling for the run.
    experiment.set_random_no_set(rep)

    # environment is (re)created inside single run
    env = simpy.Environment()

    # we pass all arrival generators to simpy
    for patient_group in experiment.dists.keys():
        env.process(patient_generator(env, patient_group, experiment))

    # run for warm-up + results collection period
    env.run(until=run_length)

    # return the count of the arrivals
    return experiment.results
