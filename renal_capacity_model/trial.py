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
        results_grouped_by_age = (
            model.results_df.groupby("age_group")
            .agg(
                {
                    "diverted_to_con_care": "sum",
                    "entry_time": "count",
                    "suitable_for_transplant": "sum",
                    "live_transplant_count": "sum",
                    "cadaver_transplant_count": "sum",
                    "pre_emptive_transplant": "sum",
                    "ichd_dialysis_count": "sum",
                    "hhd_dialysis_count": "sum",
                    "pd_dialysis_count": "sum",
                }
            )
            .rename(columns={"entry_time": "total_entries"})
        )
        self.df_trial_results.loc[run, "total_entries"] = results_grouped_by_age[
                "total_entries"
            ].sum()    
        self.df_trial_results.loc[run, "prevalence_con_care"] = (
                results_grouped_by_age["diverted_to_con_care"].sum()
            )    
        self.df_trial_results.loc[run, "prevalence_ichd"] = (
                results_grouped_by_age["ichd_dialysis_count"].sum()
            )  
        self.df_trial_results.loc[run, "prevalence_hhd"] = (
                results_grouped_by_age["hhd_dialysis_count"].sum()
            )  
        self.df_trial_results.loc[run, "prevalence_pd"] = (
                results_grouped_by_age["pd_dialysis_count"].sum()
            )  
        self.df_trial_results.loc[run, "prevalence_live_Tx"] = (
                results_grouped_by_age["live_transplant_count"].sum()
            ) 
        self.df_trial_results.loc[run, "prevalence_cadaver_Tx"] = (
                results_grouped_by_age["cadaver_transplant_count"].sum()
            ) 

        for age_group in results_grouped_by_age.index:
                self.df_trial_results.loc[
                    run, f"diverted_to_con_care_{int(age_group)}"
                ] = (
                    results_grouped_by_age.loc[age_group, "diverted_to_con_care"]
                    / results_grouped_by_age.loc[age_group, "total_entries"]
                )   ### move to validation test

        self.df_trial_results.loc[run, "suitable_for_transplant"] = (
                results_grouped_by_age["suitable_for_transplant"].sum()
            )    ### move to validation test
        self.df_trial_results.loc[run, "proportion_suitable_for_transplant"] = (
                results_grouped_by_age["suitable_for_transplant"].sum()
                / results_grouped_by_age["total_entries"].sum()
            )    ### move to validation test
        for age_group in results_grouped_by_age.index:
                self.df_trial_results.loc[
                    run, f"suitable_for_transplant_{int(age_group)}"
                ] = (
                    results_grouped_by_age.loc[age_group, "suitable_for_transplant"]
                    / results_grouped_by_age.loc[age_group, "total_entries"]
                )
        self.df_trial_results.loc[run, "proportion_pre_emptive_transplant"] = (
                results_grouped_by_age["pre_emptive_transplant"].sum()
                / results_grouped_by_age["total_entries"].sum()
            )   ### keep
        for age_group in results_grouped_by_age.index:
                self.df_trial_results.loc[
                    run, f"pre_emptive_transplant_{int(age_group)}"
                ] = (
                    results_grouped_by_age.loc[age_group, "pre_emptive_transplant"]
                    / results_grouped_by_age.loc[age_group, "total_entries"]
                )   ### move to validation test
        self.df_trial_results.loc[
                run, "proportion_live_transplant"
            ] = results_grouped_by_age["live_transplant_count"].sum() / (
                results_grouped_by_age["live_transplant_count"].sum()
                + results_grouped_by_age["cadaver_transplant_count"].sum()
            )  ### move to validation test
        for age_group in results_grouped_by_age.index:
                self.df_trial_results.loc[run, f"live_transplants_{int(age_group)}"] = (
                    results_grouped_by_age.loc[age_group, "live_transplant_count"]
                ) ### move to validation test
        for age_group in results_grouped_by_age.index:
                self.df_trial_results.loc[
                    run, f"cadaver_transplants_{int(age_group)}"
                ] = results_grouped_by_age.loc[age_group, "cadaver_transplant_count"]
                ### move to validation test
        for k, v in model.patients_in_system.items():
                self.df_trial_results.loc[run, k] = v
                ### move to validation test

    def run_trial(self):
        for run in range(self.config.number_of_runs):
            model = Model(run, self.rng, self.config)
            model.run()
            # Process results. Consider moving to separate function if it gets too complex
            self.process_model_results(model,run)

        self.print_trial_results()
