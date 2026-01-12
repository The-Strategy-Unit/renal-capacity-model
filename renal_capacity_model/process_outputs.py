# Module for processing results into output suitable for users

import pandas as pd
from renal_capacity_model.helpers import get_logger
import os
import shutil

logger = get_logger(__name__)


def split_activities_across_years(row: pd.DataFrame) -> pd.DataFrame:
    """Splits activity durations to calulate how much of each activity happened in each year.
    For example, if we have a model run with a single patient entering at time 0 and spending
    465 days in ichd, we want the count of activity for ichd to be 365 in year 1 and 100 in year 2


    Args:
        row (pd.DataFrame): Row of the event log dataframe

    Returns:
        pd.DataFrame: Dataframe with total activity for each modality over the yeaers of the simulation
    """
    segments = []

    start = row["time_starting_activity_from"]
    end = row["end_time"]
    modality = row["activity_from"]
    start_year = int(row.loc["year_start"])
    end_year = int(row.loc["year_end"])

    for year in range(start_year, end_year + 1):
        year_start = (year - 1) * 365
        year_end = year * 365

        overlap = max(0, min(end, year_end) - max(start, year_start))

        if overlap > 0:
            segments.append({"year": year, "activity": modality, "time_spent": overlap})

    return pd.DataFrame(segments)


def create_yearly_activity_duration(df: pd.DataFrame, model_run: int) -> pd.DataFrame:
    """Table with the total yearly activity for each activity for a specific model run

    Args:
        df (pd.DataFrame): Event log dataframe
        model_run (int): Which model run the event log is from

    Returns:
        pd.DataFrame: DataFrame with the total yearly activity for each treatment modality,
        trimmed to 13 years only and with model_run column added.
    """
    df["activity_from"] = df["activity_from"].replace(
        to_replace=["live", "cadaver"], value="transplant"
    )  # We combine both transplant types for cost calculations
    df["year_start"] = df["year_start"].replace(
        0, 1
    )  # Needed for split_activities_across_years to work properly
    yearly_time = pd.DataFrame(
        pd.concat(
            df.apply(split_activities_across_years, axis=1).to_list(), ignore_index=True
        )
        .groupby(["year", "activity"], as_index=False)["time_spent"]
        .sum()
    )
    yearly_time = yearly_time[
        yearly_time["year"] < 14
    ]  # Hard coding to 13 years of sim
    yearly_pivot = (
        yearly_time.pivot(index="year", columns="activity", values="time_spent")
        .fillna(0)
        .reset_index()
    )
    yearly_pivot["model_run"] = model_run
    return yearly_pivot


def calculate_activity_duration_per_year(
    list_of_eventlogs: list[pd.DataFrame],
) -> pd.DataFrame:
    """Converts list of event logs from multiple model runs to a single dataframe
    with counts of activity for each year of model simulation, for each model run

    Args:
        list_of_eventlogs (list[pd.DataFrame]): List of event log dataframes, each from a single model run

    Returns:
        pd.DataFrame: Single dataframe with counts of activity for each year of
        model simulation, for each model run
    """
    event_logs_processed = [
        create_yearly_activity_duration(event_log, model_run + 1)
        for model_run, event_log in enumerate(list_of_eventlogs)
    ]
    yearly_activity_duration = pd.concat(event_logs_processed)
    return yearly_activity_duration


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
    yearly_activity_duration: pd.DataFrame,
):
    """Write combined model results from all model runs to Excel file

    Args:
        path_to_excel_file (str): Path to Excel file
        combined_df (pd.DataFrame): Dataframe of all model results combined and processed
        yearly_activity_duration (pd.DataFrame): Dataframe of counts of activity for each year of
        model simulation, for each model run
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
        for activity in ["ichd", "hhd", "pd", "transplant"]:
            yearly_activity_duration.pivot(
                index="model_run", columns="year", values=activity
            ).sort_index(axis=1).to_excel(writer, sheet_name=f"{activity}_yearly")
    logger.info(
        f"✅ 💾 Excel format model results written to: \n{path_to_results_excel_file}"
    )
