import pandas as pd
from model import Model
from config import g
import numpy as np


class Trial:
    # The constructor sets up a pandas dataframe that will store the key
    # results from each run (just the mean queuing time for the nurse here)
    # against run number, with run number as the index.
    def __init__(self):
        self.df_trial_results = pd.DataFrame()
        self.df_trial_results["Run Number"] = [0]
        self.df_trial_results["Mean Time in System"] = [0.0]
        self.df_trial_results.set_index("Run Number", inplace=True)
        self.rng = np.random.default_rng(g.random_seed)

    # Method to print out the results from the trial.  In real world models,
    # you'd likely save them as well as (or instead of) printing them
    def print_trial_results(self):
        print("Trial Results")
        print(self.df_trial_results)

    # Method to run a trial
    def run_trial(self):
        # Run the simulation for the number of runs specified in g class.
        # For each run, we create a new instance of the Model class and call its
        # run method, which sets everything else in motion.  Once the run has
        # completed, we grab out the stored run results (just mean queuing time
        # here) and store it against the run number in the trial results
        # dataframe.
        for run in range(g.number_of_runs):
            model = Model(run, self.rng)
            model.run()
            for k, v in model.patients_in_system.items():
                self.df_trial_results.loc[run, k] = v

        # Once the trial (ie all runs) has completed, print the final results
        self.print_trial_results()
