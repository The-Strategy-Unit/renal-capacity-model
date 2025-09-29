"""
Module containing Trial class with logic for running multiple model iterations
"""

import pandas as pd
from renal_capacity_model.model import Model
import numpy as np

pd.set_option("display.max_columns", None)


class Trial:
    """
    Trial class containing logic for running full experiment
    """

    def __init__(self, config):
        self.df_trial_results = self.setup_trial_results()
        self.config = config
        self.rng = np.random.default_rng(self.config.random_seed)

    def print_trial_results(self):
        print("Trial Results")
        print(self.df_trial_results.mean())

    def setup_trial_results(self):
        df_trial_results = pd.DataFrame()
        df_trial_results["Run Number"] = [0]
        df_trial_results.set_index("Run Number", inplace=True)
        return df_trial_results
    
    def process_model_results(self,model,run):
 
        self.df_trial_results.loc[run, "total_entries"] = model.results_df["entry_time"].count()   
        self.df_trial_results.loc[run, "prevalence_con_care"] = model.results_df["diverted_to_con_care"].sum()
        self.df_trial_results.loc[run, "prevalence_ichd"] = model.results_df["ichd_dialysis_count"].sum()
        self.df_trial_results.loc[run, "prevalence_hhd"] = model.results_df["hhd_dialysis_count"].sum()
        self.df_trial_results.loc[run, "prevalence_pd"] = model.results_df["pd_dialysis_count"].sum()
        self.df_trial_results.loc[run, "prevalence_live_Tx"] = model.results_df["live_transplant_count"].sum()
        self.df_trial_results.loc[run, "prevalence_cadaver_Tx"] = model.results_df["cadaver_transplant_count"].sum()

        self.df_trial_results.loc[run, "total_deaths"] = model.results_df["time_of_death"].count()   
        self.df_trial_results.loc[run, "mortality_con_care"] = model.results_df["death_from_con_care"].sum()
        self.df_trial_results.loc[run, "mortality_ichd"] = model.results_df["death_from_ichd"].sum()
        self.df_trial_results.loc[run, "mortality_hhd"] = model.results_df["death_from_hhd"].sum()
        self.df_trial_results.loc[run, "mortality_pd"] = model.results_df["death_from_pd"].sum()
        self.df_trial_results.loc[run, "mortality_live_Tx"] = model.results_df["death_post_live_transplant"].sum()
        self.df_trial_results.loc[run, "mortality_cadaver_Tx"] = model.results_df["death_post_cadaver_transplant"].sum()


    def run_trial(self):
        for run in range(self.config.number_of_runs):
            model = Model(run, self.rng, self.config)
            model.run()
            # Process results. Consider moving to separate function if it gets too complex
            self.process_model_results(model,run)

        self.print_trial_results()
