"""
Module containing Trial class with logic for running multiple model iterations
"""

import pandas as pd
from renal_capacity_model.model import Model
from renal_capacity_model.utils import get_logger
import numpy as np
from tqdm import tqdm
from typing import Optional
from datetime import datetime
import os

pd.set_option("display.max_columns", 13)

logger = get_logger(__name__)


class Trial:
    """
    Trial class containing logic for running full experiment
    """

    def __init__(self, config):
        self.config = config
        self.rng = np.random.default_rng(self.config.random_seed)
        self.df_trial_results: Optional[pd.DataFrame] = None
        self.results_dfs: list[pd.DataFrame] = []
        self.activity_change_dfs = []

    def print_trial_results(self):
        print("Trial Results")
        print(f"Average across {self.config.number_of_runs} runs")
        if self.df_trial_results is not None:
            print(self.df_trial_results)
        else:
            raise TypeError("No trial results available")

    def process_model_results(self, results_dfs: list[pd.DataFrame]) -> pd.DataFrame:
        logger.info("Processing combined results")
        combined_results = pd.concat(results_dfs)
        aggregated_combined_results = pd.DataFrame(
            combined_results.groupby(combined_results.index).mean()
        )
        return aggregated_combined_results

    def process_eventlog_dfs(self, eventlog_dfs: list[pd.DataFrame]) -> pd.DataFrame:
        combined_df = pd.concat(eventlog_dfs)
        columns_to_groupby = list(combined_df.index.names)
        aggregated_combined_df = pd.DataFrame(
            combined_df.reset_index().groupby(columns_to_groupby).mean()
        )
        return aggregated_combined_df

    def save_dfs(self, df_to_save, name_of_df_to_save):
        today_date = datetime.now().strftime("%Y%m%d-%H%M")
        if not os.path.exists("results"):
            os.makedirs("results")
        filename = f"results/{today_date}_combined_{name_of_df_to_save}.csv"
        df_to_save.to_csv(filename)

    def run_trial(self):
        for run in tqdm(range(self.config.number_of_runs)):
            model = Model(run, self.rng, self.config)
            model.run()
            self.activity_change_dfs.append(model.activity_change)
            self.results_dfs.append(model.results_df)
        logger.info("✅🥳 Trial complete!")
        self.df_trial_results = self.process_model_results(self.results_dfs)
        logger.info("💾 Saving full trial results")
        self.save_dfs(
            self.process_eventlog_dfs(self.activity_change_dfs), "activity_change"
        )
        self.save_dfs((self.df_trial_results), "trial_results")
