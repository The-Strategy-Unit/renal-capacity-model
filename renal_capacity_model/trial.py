"""
Module containing Trial class with logic for running multiple model iterations
"""

import pandas as pd
from model import Model
from config import g
import numpy as np


class Trial:
    def __init__(self):
        self.df_trial_results = self.setup_trial_results()
        self.rng = np.random.default_rng(g.random_seed)

    def print_trial_results(self):
        print("Trial Results")
        print(self.df_trial_results)

    def setup_trial_results(self):
        df_trial_results = pd.DataFrame()
        df_trial_results["Run Number"] = [0]
        df_trial_results.set_index("Run Number", inplace=True)
        return df_trial_results

    def run_trial(self):
        for run in range(g.number_of_runs):
            model = Model(run, self.rng)
            model.run()
            # We currently only save counts of patients in the system
            for k, v in model.patients_in_system.items():
                self.df_trial_results.loc[run, k] = v

        self.print_trial_results()
