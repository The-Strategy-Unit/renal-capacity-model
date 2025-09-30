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
        output_means = self.df_trial_results.mean().to_frame()
        output_means['Time']=output_means.index.str.split('_').str[-1]
        output_means.index = output_means.index.str.rsplit('_', n=1).str[0]
        reshaped_trial_results = output_means.pivot(columns='Time', values=0)
        print(reshaped_trial_results)
        print(reshaped_trial_results.diff(axis=1))   ### could use for plotting mortality over time instead of cumulative mortality

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

    def process_snapshot_results(self,model,run):
        ## this groups the results by the time the snapshot was taken, so we can see how prevalence and mortality change over time
        results_grouped_by_time = (
            model.snapshot_results_df.groupby("snapshot_time")
            .agg(
                {
                    "entry_time": "count",
                    "diverted_to_con_care": "sum",
                    "ichd_dialysis_count": "sum",
                    "hhd_dialysis_count": "sum",
                    "pd_dialysis_count": "sum",
                    "live_transplant_count": "sum",
                    "cadaver_transplant_count": "sum",
                    "time_of_death": "count",
                    "death_from_con_care": "sum",
                    "death_from_ichd": "sum",
                    "death_from_hhd": "sum",
                    "death_from_pd": "sum",
                    "death_post_live_transplant": "count",
                    "death_post_cadaver_transplant": "count",
                }
            )
            .rename(columns={"entry_time": "total_entries","time_of_death": "total_deaths"})
        )

        for snapshot_time in results_grouped_by_time.index:
            self.df_trial_results.loc[run, f"total_entries_{snapshot_time}"] = results_grouped_by_time.loc[snapshot_time, "total_entries"]
            self.df_trial_results.loc[run, f"prevalence_con_care_{snapshot_time}"] = results_grouped_by_time.loc[snapshot_time, "diverted_to_con_care"]
            self.df_trial_results.loc[run, f"prevalence_ichd_{snapshot_time}"] = results_grouped_by_time.loc[snapshot_time, "ichd_dialysis_count"]
            self.df_trial_results.loc[run, f"prevalence_hhd_{snapshot_time}"] = results_grouped_by_time.loc[snapshot_time, "hhd_dialysis_count"]
            self.df_trial_results.loc[run, f"prevalence_pd_{snapshot_time}"] = results_grouped_by_time.loc[snapshot_time, "pd_dialysis_count"]
            self.df_trial_results.loc[run, f"prevalence_live_Tx_{snapshot_time}"] = results_grouped_by_time.loc[snapshot_time, "live_transplant_count"]
            self.df_trial_results.loc[run, f"prevalence_cadaver_Tx_{snapshot_time}"] = results_grouped_by_time.loc[snapshot_time, "cadaver_transplant_count"]
            self.df_trial_results.loc[run, f"total_deaths_{snapshot_time}"] = results_grouped_by_time.loc[snapshot_time, "total_deaths"]
            self.df_trial_results.loc[run, f"mortality_con_care_{snapshot_time}"] = results_grouped_by_time.loc[snapshot_time, "death_from_con_care"]
            self.df_trial_results.loc[run, f"mortality_ichd_{snapshot_time}"] = results_grouped_by_time.loc[snapshot_time, "death_from_ichd"]
            self.df_trial_results.loc[run, f"mortality_hhd_{snapshot_time}"] = results_grouped_by_time.loc[snapshot_time, "death_from_hhd"]
            self.df_trial_results.loc[run, f"mortality_pd_{snapshot_time}"] = results_grouped_by_time.loc[snapshot_time, "death_from_pd"]
            self.df_trial_results.loc[run, f"mortality_live_Tx_{snapshot_time}"] = results_grouped_by_time.loc[snapshot_time, "death_post_live_transplant"]
            self.df_trial_results.loc[run, f"mortality_cadaver_Tx_{snapshot_time}"] = results_grouped_by_time.loc[snapshot_time, "death_post_cadaver_transplant"]

    def run_trial(self):
        for run in range(self.config.number_of_runs):
            model = Model(run, self.rng, self.config)
            model.run()
            
            model.snapshot_results_df = pd.concat([model.snapshot_results_df, model.results_df.assign(snapshot_time=model.config.sim_duration)])
            self.process_snapshot_results(model,run)

        self.print_trial_results()
