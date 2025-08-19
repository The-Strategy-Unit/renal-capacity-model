"""
Module containing Trial class with logic for running multiple model iterations
"""

from turtle import mode
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
            self.df_trial_results.loc[run, "diverted_to_con_care"] = model.results_df[
                "diverted_to_con_care"
            ].sum()
            diverted_to_con_care = model.results_df.groupby("age_group")[
                "diverted_to_con_care"
            ].sum()
            # TODO: instead of denominator being sum of diverted to con_care, it should be total number of patients of that age group which have entered the system
            # for age_group in diverted_to_con_care.index:
            #     self.df_trial_results.loc[run, f"diverted_to_con_care_{age_group}"] = (
            #         diverted_to_con_care.loc[age_group] / diverted_to_con_care.sum()
            #     )
            # We currently only save counts of patients in the system
            for k, v in model.patients_in_system.items():
                self.df_trial_results.loc[run, k] = v

        self.print_trial_results()
