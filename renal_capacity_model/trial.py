"""
Module containing Trial class with logic for running multiple model iterations
"""

import pandas as pd
from model import Model
from config import g
import numpy as np

pd.set_option("display.max_columns", None)


class Trial:
    def __init__(self):
        self.df_trial_results = self.setup_trial_results()
        self.rng = np.random.default_rng(g.random_seed)

    def print_trial_results(self):
        print("Trial Results")
        print(self.df_trial_results.mean())

    def setup_trial_results(self):
        df_trial_results = pd.DataFrame()
        df_trial_results["Run Number"] = [0]
        df_trial_results.set_index("Run Number", inplace=True)
        return df_trial_results

    def run_trial(self):
        for run in range(g.number_of_runs):
            model = Model(run, self.rng)
            model.run()
            # Process results. Consider moving to separate function if it gets too complex
            results_grouped_by_age = (
                model.results_df.groupby("age_group")
                .agg({"diverted_to_con_care": "sum", "entry_time": "count"})
                .rename(columns={"entry_time": "total_entries"})
            )
            self.df_trial_results.loc[run, "diverted_to_con_care"] = (
                results_grouped_by_age["diverted_to_con_care"].sum()
            )
            for age_group in results_grouped_by_age.index:
                self.df_trial_results.loc[
                    run, f"diverted_to_con_care_{int(age_group)}"
                ] = (
                    results_grouped_by_age.loc[age_group, "diverted_to_con_care"]
                    / results_grouped_by_age.loc[age_group, "total_entries"]
                )
            for k, v in model.patients_in_system.items():
                self.df_trial_results.loc[run, k] = v

        self.print_trial_results()
