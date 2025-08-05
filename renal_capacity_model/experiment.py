from distributions import (
    IAT_1_EARLY,
    IAT_2_EARLY,
    IAT_3_EARLY,
    IAT_4_EARLY,
    IAT_5_EARLY,
    IAT_6_EARLY,
    IAT_1_LATE,
    IAT_2_LATE,
    IAT_3_LATE,
    IAT_4_LATE,
    IAT_5_LATE,
    IAT_6_LATE,
)
from config import g
import numpy as np
from distributions import Exponential
import itertools
from helpers import trace


class Experiment:
    """
    Manages parameters, PRNG streams and results.
    """

    def __init__(
        self,
        random_number_set=g.default_rnd_set,
        n_streams=g.n_streams,
        iat_1_Early=IAT_1_EARLY,
        iat_2_Early=IAT_2_EARLY,
        iat_3_Early=IAT_3_EARLY,
        iat_4_Early=IAT_4_EARLY,
        iat_5_Early=IAT_5_EARLY,
        iat_6_Early=IAT_6_EARLY,
        iat_1_Late=IAT_1_LATE,
        iat_2_Late=IAT_2_LATE,
        iat_3_Late=IAT_3_LATE,
        iat_4_Late=IAT_4_LATE,
        iat_5_Late=IAT_5_LATE,
        iat_6_Late=IAT_6_LATE,
    ):
        """
        The init method sets up our defaults.
        """
        # sampling
        self.random_number_set = random_number_set
        self.n_streams = n_streams

        # store parameters for the run of the model
        self.iat_1_Early = iat_1_Early
        self.iat_2_Early = iat_2_Early
        self.iat_3_Early = iat_3_Early
        self.iat_4_Early = iat_4_Early
        self.iat_5_Early = iat_5_Early
        self.iat_6_Early = iat_6_Early
        self.iat_1_Late = iat_1_Late
        self.iat_2_Late = iat_2_Late
        self.iat_3_Late = iat_3_Late
        self.iat_4_Late = iat_4_Late
        self.iat_5_Late = iat_5_Late
        self.iat_6_Late = iat_6_Late

        # we will store all code in distributions
        self.dists = {}

        # initialise results to zero
        self.init_results_variables()

        # initialise sampling objects
        self.init_sampling()

    def set_random_no_set(self, random_number_set):
        """
        Controls the random sampling
        Parameters:
        ----------
        random_number_set: int
            Used to control the set of pseudo random numbers used by
            the distributions in the simulation.
        """
        self.random_number_set = random_number_set
        self.init_sampling()

    def init_sampling(self):
        """
        Create the distributions used by the model and initialise
        the random seeds of each.
        """
        # produce n non-overlapping streams
        seed_sequence = np.random.SeedSequence(self.random_number_set)
        self.seeds = seed_sequence.spawn(self.n_streams)

        # create distributions

        # inter-arrival time distributions
        self.dists["iat_1_Early"] = Exponential(
            self.iat_1_Early, random_seed=self.seeds[0]
        )

        self.dists["iat_2_Early"] = Exponential(
            self.iat_2_Early, random_seed=self.seeds[0]
        )

        self.dists["iat_3_Early"] = Exponential(
            self.iat_3_Early, random_seed=self.seeds[0]
        )

        self.dists["iat_4_Early"] = Exponential(
            self.iat_4_Early, random_seed=self.seeds[0]
        )

        self.dists["iat_5_Early"] = Exponential(
            self.iat_5_Early, random_seed=self.seeds[0]
        )

        self.dists["iat_6_Early"] = Exponential(
            self.iat_6_Early, random_seed=self.seeds[0]
        )

        self.dists["iat_1_Late"] = Exponential(
            self.iat_1_Late, random_seed=self.seeds[0]
        )

        self.dists["iat_2_Late"] = Exponential(
            self.iat_2_Late, random_seed=self.seeds[0]
        )

        self.dists["iat_3_Late"] = Exponential(
            self.iat_3_Late, random_seed=self.seeds[0]
        )

        self.dists["iat_4_Late"] = Exponential(
            self.iat_4_Late, random_seed=self.seeds[0]
        )

        self.dists["iat_5_Late"] = Exponential(
            self.iat_5_Late, random_seed=self.seeds[0]
        )

        self.dists["iat_6_Late"] = Exponential(
            self.iat_6_Late, random_seed=self.seeds[0]
        )

    def init_results_variables(self):
        """
        Initialise all of the experiment variables used in results
        collection.  This method is called at the start of each run
        of the model
        """
        # variable used to store results of experiment
        self.results = {}
        self.results["number in system"] = 0


def patient_generator(env, patient_group, args):
    """
    Modified generator for arrivals.
    Now works across all patient group types.

    Parameters:
    ------
    env: simpy.Environment
        The simpy environment for the simulation

    patient_group: str
        string representing the type of patient e.g. age group x and referral status y

    args: Experiment
        The settings and input parameters for the simulation.
    """
    # use itertools as it provides an infinite loop
    # with a counter variable that we can use for unique Ids
    for patient_count in itertools.count(start=1):
        # the sample distribution is defined by the experiment.
        inter_arrival_time = args.dists[patient_group].sample()
        yield env.timeout(inter_arrival_time)

        args.results[f"n_{patient_group}s"] = patient_count
        args.results["number in system"] = args.results["number in system"] + 1
        trace(f"{env.now:.2f}: {patient_group.upper()} arrival.")
