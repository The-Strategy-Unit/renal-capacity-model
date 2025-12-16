# Module for processing results into output suitable for users

import pandas as pd
from renal_capacity_model.helpers import get_logger
import os
import shutil

logger = get_logger(__name__)


def create_results_folder(run_start_time: str) -> str:
    """Creates folder results/run_start_time to save results files to

    Args:
        run_start_time (str): Start time of model run

    Returns:
        path_to_results (str): Folder to save model run results
    """
    path_to_results = os.path.join("results", run_start_time)
    if not os.path.exists(path_to_results):
        os.makedirs(path_to_results)
    return path_to_results


def save_result_files(df_to_save: pd.DataFrame, filename: str, path_to_results: str):
    """Saves results files in CSV and parquet formats

    Args:
        df_to_save (pd.DataFrame): Dataframe to save
        filename (str): Name of Dataframe to save
        path_to_results (str): Folder to save results to
    """
    logger.info(f"💾 Saving {filename}")
    df_to_save.to_parquet(os.path.join(path_to_results, filename + ".parquet"))
    df_to_save.to_csv(os.path.join(path_to_results, filename + ".csv"))


def combine_incident_and_prevalent_counts(df: pd.DataFrame) -> pd.DataFrame:
    """The results dataframes separate out counts of prevalence, mortality, and incidence
    by incident and prevalent patients, for easier debugging. We undo this aggregation
    and combine the counts of both incident and prevalent patients, for model results aimed at users.

    Args:
        df (pd.DataFrame): Results dataframe from a model run

    Returns:
        pd.DataFrame: Results dataframe from a model run with the counts for incident and prevalent patients combined
    """
    processed_dfs = []
    for metric in ["prevalence", "mortality", "incidence"]:
        df_filtered = df[df.index.str.contains(metric, case=False, na=False)].copy()
        df_filtered.loc[:, "index"] = df_filtered.index.str.replace(
            r"_?(incident|prevalent)", "", regex=True
        )
        processed_dfs.append(df_filtered.groupby("index").sum())
    return pd.concat(processed_dfs).fillna(0)


def produce_combined_results_for_all_model_runs(
    results_dfs: list[pd.DataFrame],
) -> pd.DataFrame:
    """Combine processed results for all model runs into one dataframe

    Args:
        results_dfs (list[pd.DataFrame]): List of model results dataframes

    Returns:
        pd.DataFrame: DataFrame of all model results combined and processed
    """
    dfs_processed = [combine_incident_and_prevalent_counts(df) for df in results_dfs]
    combined = pd.concat(
        [df.reset_index().assign(model_run=i + 1) for i, df in enumerate(dfs_processed)]
    )
    return (
        combined.set_index(["index", "model_run"])
        .sort_index(axis=0)
        .sort_index(axis=1)
        .fillna(0)
    )


def copy_excel_files(path_to_file: str, run_start_time: str) -> str:
    """Creates a copy of the Renal Modelling Input File in the results folder for the trial run

    Args:
        path_to_file (str): Path to the Excel File to copy
        run_start_time (str): Start time of experimment

    Returns:
        str: Filepath to the copied Excel file, in the results folder
    """
    results_folder = create_results_folder(run_start_time)
    new_filename = (
        os.path.basename(path_to_file)
        .replace(".xlsx", f"_{run_start_time}.xlsx")
        .replace("Renal_Modelling_", "")
        .replace("_File", "")
    )
    results_filepath = os.path.join(results_folder, new_filename)
    shutil.copy2(path_to_file, results_filepath)
    return results_filepath


def write_results_to_excel(
    path_to_results_excel_file: str,
    combined_df: pd.DataFrame,
):
    """Write combined model results from all model runs to Excel file

    Args:
        path_to_excel_file (str): Path to Excel file
        combined_df (pd.DataFrame): Dataframe of all model results combined and processed
    """
    with pd.ExcelWriter(
        path_to_results_excel_file,
        engine="openpyxl",
        mode="a",
        if_sheet_exists="replace",
    ) as writer:
        for outcome in combined_df.index.get_level_values(0).drop_duplicates():
            combined_df.loc[outcome].to_excel(
                writer, sheet_name=outcome.replace("waiting_for_transplant", "wft")
            )
    logger.info(
        f"✅ 💾 Excel format model results written to: \n{path_to_results_excel_file}"
    )
