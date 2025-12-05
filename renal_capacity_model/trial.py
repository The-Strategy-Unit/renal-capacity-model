"""
Module containing Trial class with logic for running multiple model iterations
"""

import pandas as pd
from renal_capacity_model.model import Model
from renal_capacity_model.config import Config
from renal_capacity_model.utils import get_logger
from renal_capacity_model.process_outputs import (
    create_results_folder,
    save_result_files,
)
import numpy as np
from tqdm import tqdm
from typing import Optional

pd.set_option("display.max_columns", 13)

logger = get_logger(__name__)


class Trial:
    """
    Trial class containing logic for running full experiment
    """

    def __init__(self, config: Config, run_start_time: str):
        self.config = config
        self.rng = np.random.default_rng(self.config.random_seed)
        self.df_trial_results: Optional[pd.DataFrame] = None
        self.results_dfs: list[pd.DataFrame] = []
        self.activity_change_dfs = []
        self.run_start_time = run_start_time

    def print_trial_results(self):
        print("Trial Results")
        print(f"Average across {self.config.number_of_runs} runs")
        if self.df_trial_results is not None:
            print(self.df_trial_results)
        else:
            raise TypeError("No trial results available")

    def process_model_results(self, results_dfs: list[pd.DataFrame]) -> pd.DataFrame:
        """Process model results from all model runs to produce one aggregated combined results

        Args:
            results_dfs (list[pd.DataFrame]): List of model results dataframes

        Returns:
            pd.DataFrame: Combined and processed model results
        """
        logger.info("Processing combined results")
        combined_results = pd.concat(results_dfs)
        aggregated_combined_results = pd.DataFrame(
            combined_results.groupby(combined_results.index).mean()
        )
        return aggregated_combined_results

    def process_eventlog_dfs(self, eventlog_dfs: list[pd.DataFrame]) -> pd.DataFrame:
        """Process event logs to produce one aggregated event log

        Args:
            eventlog_dfs (list[pd.DataFrame]): List of event logs

        Returns:
            pd.DataFrame: Combined and aggregasted event log
        """
        combined_df = pd.concat(eventlog_dfs)
        columns_to_groupby = list(combined_df.index.names)
        aggregated_combined_df = pd.DataFrame(
            combined_df.reset_index().groupby(columns_to_groupby).mean()
        )
        return aggregated_combined_df

    def save_trial_results(self, df_to_save: pd.DataFrame, name_of_df_to_save: str):
        """Save trial results dataframes

        Args:
            df_to_save (pd.DataFrame): Trial results dataframe to save
            name_of_df_to_save (str): Name of trial results dataframe to save
        """
        path_to_results = create_results_folder(self.run_start_time)
        save_result_files(df_to_save, name_of_df_to_save, path_to_results)

    def run_trial(self):
        for run in tqdm(range(self.config.number_of_runs)):
            model = Model(run, self.rng, self.config, self.run_start_time)
            model.run()
            self.activity_change_dfs.append(model.activity_change)
            self.results_dfs.append(model.results_df)
        logger.info("✅🥳 Trial complete!")
        self.df_trial_results = self.process_model_results(self.results_dfs)
        logger.info("💾 Saving full trial results")
        self.save_trial_results(
            self.process_eventlog_dfs(self.activity_change_dfs), "activity_change"
        )
        self.save_trial_results(self.df_trial_results, "trial_results")
