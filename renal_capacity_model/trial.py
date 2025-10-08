"""
Module containing Trial class with logic for running multiple model iterations
"""

import pandas as pd
from renal_capacity_model.model import Model
import numpy as np
from tqdm import tqdm
from typing import Optional

pd.set_option("display.max_columns", None)


class Trial:
    """
    Trial class containing logic for running full experiment
    """

    def __init__(self, config):
        self.config = config
        self.rng = np.random.default_rng(self.config.random_seed)
        self.df_trial_results: Optional[pd.DataFrame] = None

    def print_trial_results(self):
        print("Trial Results")
        print(f"Average across {self.config.number_of_runs} runs")
        if self.df_trial_results is not None:
            print(
                self.df_trial_results.infer_objects(copy=False)
                .fillna(0)
                .drop(columns=["run"])
                .groupby(["measure"])
                .mean()
            )
        else:
            raise TypeError("No trial results available")

    def process_model_results(self, results_df):
        # calculate prevalence
        prevalence_columns = [
            col for col in results_df.columns if col.endswith("count")
        ]
        prevalence = (
            results_df[prevalence_columns]
            .sum()
            .rename(lambda x: f"{x.replace('count', 'prevalence')}")
        )
        mortality = (
            results_df["treatment_modality_at_death"]
            .value_counts()
            .rename(lambda x: f"mortality_{x}")
        )
        totals = (
            results_df[["entry_time", "time_of_death"]]
            .rename(
                columns={"entry_time": "total_entries", "time_of_death": "total_deaths"}
            )
            .count()
        )
        df = pd.concat([prevalence, mortality, totals])
        return df

    def process_snapshot_results(self, model, run):
        snapshots = []
        for time in model.snapshot_results_df["snapshot_time"].unique():
            if time > 0:
                snapshot_df = model.snapshot_results_df[
                    model.snapshot_results_df["snapshot_time"] == time
                ]
                processed_snapshot = self.process_model_results(snapshot_df)
                processed_snapshot.name = time
                snapshots.append(processed_snapshot)
        # add final results
        final_snapshot = self.process_model_results(model.results_df)
        final_snapshot.name = model.config.sim_duration
        snapshots.append(final_snapshot)
        all_processed_snapshots = (
            (pd.concat(snapshots, axis=1).assign(run=run))
            .reset_index()
            .rename(columns={"index": "measure"})
        )
        if self.df_trial_results is not None:
            self.df_trial_results = pd.concat(
                [self.df_trial_results, all_processed_snapshots]
            )
        else:
            self.df_trial_results = all_processed_snapshots

    def run_trial(self):
        for run in tqdm(range(self.config.number_of_runs)):
            model = Model(run, self.rng, self.config)
            model.run()
            self.process_snapshot_results(model, run)

        self.print_trial_results()
