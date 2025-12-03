"""
Module with helper functions
"""

from renal_capacity_model.utils import get_logger
import pandas as pd
import numpy as np
from itertools import product
import math
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from renal_capacity_model.config import Config

logger = get_logger(__name__)


def get_yearly_arrival_rate(config: "Config") -> dict[int, dict]:
    """Iteratively calls get_arival_rate over each year of the simulation

    Args:
        config (Config): Config for the model, containing sim_duration in days and
        arrival rates for each year of the sim duration

    Returns:
        dict[int, dict]: Arrival_rate dictionaries to use for each year of the simulation
    """
    mean_arrival_rates = {}
    years = calculate_lookup_year(config.sim_duration)
    for year in range(1, years + 1):
        mean_arrival_rates[year] = get_arrival_rate(
            config.arrival_rate[year], config.referral_dist, config.age_dist
        )
    return mean_arrival_rates


def get_mean_iat_over_time_from_arrival_rate(
    arrival_rate_dict: dict,
) -> dict[str, pd.DataFrame]:
    """Calculates mean interarrival time in each year of the simulation, for each patient type

    Args:
        arrival_rate_dict (dict): Dict containing the arrival rates

    Returns:
        dict: Dict containing the mean inter arrival times and arrival rates for each patient type
    """
    mean_iat_over_time_dfs = {}
    df = pd.DataFrame(arrival_rate_dict)
    for i in df.index:
        mini_df = pd.DataFrame(df.loc[i])
        mini_df = mini_df.rename(columns={"index": "t", i: "arrival_rate"})
        mini_df["mean_iat"] = 1 / mini_df["arrival_rate"]
        mean_iat_over_time_dfs[i] = mini_df
    return mean_iat_over_time_dfs


def get_arrival_rate(arrival_rate, referral_dist, age_dist) -> dict[str, float]:
    """Calculates arrival rates for different patient groups

    Args:
        arrival_rate (float): Arrival rate in a given year
        referral_dist (dict): Distribution of different referral types
        age_dist (dict): Distribution of different age groups

    Returns:
        dict: Dictionary containing different arrival rates for patient groups, given a single arrival rate
    """

    arrival_rate_dict = {}
    for referral, referral_value in referral_dist.items():
        for age_group, age_value in age_dist.items():
            arrival_rate_dict[f"{age_group}_{referral}"] = arrival_rate * (
                age_value * referral_value
            )
    return arrival_rate_dict


def check_config_duration_valid(config: "Config") -> bool:
    """Checks that config values which change over the sim duration are provided

    Args:
        config (Config): Config Class containing values to be used for model run
    """
    config_values_to_check = [
        "arrival_rate",
        "con_care_dist",
        "modality_allocation_distributions",
        "pre_emptive_transplant_live_donor_dist",
        "pre_emptive_transplant_cadaver_donor_dist",
    ]
    sim_years = calculate_lookup_year(config.sim_duration)
    for config_value in config_values_to_check:
        if max(getattr(config, config_value).keys()) < sim_years:
            raise ValueError(
                f"{config_value} does not include enough years for sim duration"
            )
    return True


def calculate_lookup_year(time_units: float) -> int:
    """Calculates which year of the simulation the model is in, so that relevant values can be obtained from config

    Args:
        time_units (float): Current time in model, in days

    Returns:
        int: Which year of the model the model is in. Starts at 1.
    """
    year = year = math.ceil(time_units / 365) or 1
    return year


def calculate_incidence(event_log: pd.DataFrame) -> pd.DataFrame:
    """Calculate incidence from the event log

    Args:
        event_log (pd.DataFrame): Event log recorded in each model iteration

    Returns:
        pd.DataFrame: Dataframe with incidence counts for each year in the model
    """
    incidence = event_log.groupby(["year_start", "patient_flag"])[
        "activity_from"
    ].value_counts()
    incidence = incidence.unstack(level="year_start")
    incidence.index = incidence.index.map(
        lambda idx: "incidence_" + "_".join(map(str, idx))
    )
    return pd.DataFrame(incidence)


def calculate_activity_change(event_log: pd.DataFrame) -> pd.DataFrame:
    """Calculates activity change dataframe for easier debugging and validation

    Args:
        event_log (pd.DataFrame): Event log recorded in each model iteration

    Returns:
        pd.DataFrame: Activity change dataframe showing counts of changes in activity in each year
        of model simulation
    """
    activity_change = event_log.groupby(
        ["year_start", "patient_type", "patient_flag", "activity_from", "activity_to"]
    ).agg(
        {
            "time_starting_activity_from": "count",
            "time_spent_in_activity_from": "mean",
        }
    )
    activity_change = pd.DataFrame(activity_change, index=activity_change.index).rename(
        columns={
            "time_starting_activity_from": "change_counts",
            "time_spent_in_activity_from": "mean_time",
        }
    )
    return activity_change


def calculate_prevalence(event_log: pd.DataFrame) -> pd.DataFrame:
    """Calculate prevalence from the event log

    Args:
        event_log (pd.DataFrame): Event log recorded in each model iteration

    Returns:
        pd.DataFrame: Dataframe with prevalence counts for each year in the model
    """
    years = list(range(0, int(event_log["year_end"].max())))

    rows = []
    for y in years:
        mask = (event_log["year_start"] <= y) & (event_log["year_end"] > y)
        counts = (
            event_log[mask]
            .groupby(["activity_from", "patient_flag"])["patient_id"]
            .nunique()
        )
        counts.name = y
        rows.append(counts)

    prevalence = pd.DataFrame(rows).fillna(0).astype(int)
    prevalence = prevalence.T
    prevalence.index = ["prevalence_" + "_".join(i) for i in prevalence.index]
    return prevalence


def calculate_mortality(event_log: pd.DataFrame) -> pd.DataFrame:
    """Calculate mortality from the event log

    Args:
        event_log (pd.DataFrame): Event log recorded in each model iteration

    Returns:
        pd.DataFrame: Dataframe with mortality counts for each year in the model
    """
    years = list(range(1, int(event_log["year_end"].max())))
    rows = []
    for y in years:
        mask = (event_log["activity_to"] == "death") & (event_log["year_end"] == y)
        counts = (
            event_log[mask]
            .groupby(["activity_from", "patient_flag"])["patient_id"]
            .nunique()
        )
        counts.name = y
        rows.append(counts)
    mortality = pd.DataFrame(rows).fillna(0).astype(int)
    mortality = mortality.T
    mortality.index = ["mortality_" + "_".join(i) for i in mortality.index]
    return mortality


def adjust_next_modality(event_log: pd.DataFrame) -> pd.DataFrame:
    """
    The event_log records how long each patient spent in each modality before moving to
    modality_allocation. It would be more useful to report, instead of "modality_allocation",
    the specific modality they were allocated to.

    Args:
        event_log (pd.DataFrame): Event log

    Returns:
        pd.DataFrame: Event log with the actual modality allocated after
        "modality_allocation" in the "activity_to" column
    """
    event_log_sorted = event_log.sort_values(
        by=["patient_id", "time_starting_activity_from"]
    ).reset_index(drop=True)
    # if modality_allocation is the last activity recorded then leave it as is
    last_idx = event_log_sorted.groupby("patient_id").tail(1).index
    mask = (event_log_sorted["activity_to"].str.contains("modality")) & (
        ~event_log_sorted.index.isin(last_idx)
    )
    adjusted = event_log_sorted.groupby("patient_id")["activity_from"].shift(-1)
    event_log_sorted.loc[mask, "activity_to"] = adjusted[mask]
    return event_log_sorted


def process_event_log(event_log: pd.DataFrame) -> pd.DataFrame:
    """Processes event log for easier validation and debugging

    Args:
        event_log (pd.DataFrame): event log

    Returns:
        pd.DataFrame with additional columns ("year_start", "end_time", "year_end")
        and clearer information on which modality was next
    """
    event_log["year_start"] = event_log["time_starting_activity_from"].apply(
        calculate_lookup_year
    )
    # normally we count 0 as lookup year 1 but we will force to 0 for results calculations
    event_log.loc[event_log["time_starting_activity_from"] == 0, "year_start"] = 0
    event_log["end_time"] = (
        event_log["time_starting_activity_from"]
        + event_log["time_spent_in_activity_from"]
    )
    event_log["year_end"] = event_log["end_time"].apply(calculate_lookup_year)
    event_log = adjust_next_modality(event_log)
    return event_log


def calculate_model_results(
    processed_event_log: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Calculates full model results and activity change dataframes from the event log

    Args:
        processed_event_log (pd.DataFrame): Event log that has been through process_event_log cleaning

    Returns:
        tuple[pd.DataFrame, pd.DataFrame]: Results dataframe and activiy change dataframe
    """
    logger.info("Calculating model run results from event log")
    incidence = calculate_incidence(processed_event_log)
    mortality = calculate_mortality(processed_event_log)
    prevalence = calculate_prevalence(processed_event_log)
    results_df = pd.concat([incidence, mortality, prevalence]).fillna(0)
    activity_change = calculate_activity_change(processed_event_log)
    return results_df, activity_change


def truncate_2dp(x: float) -> float:
    """Truncates randomly sampled numbers to two decimal places,
    so we can use them as lookups in the time to event curves

    Args:
        x (float): Randomly sampled float from 0,1

    Returns:
        float: Number
    """
    truncated = math.trunc(x * 100) / 100
    return min(max(truncated, 0.01), 0.99)


def check_time_to_event_curve_dfs(tte_df_name: str, tte_df: pd.DataFrame):
    """Checks that loaded time to event curve dataframes meet required standards

    Args:
        tte_df (pd.DataFrame): Time to event curve dataframe, loaded from CSV
        tte_df_name (str): Name of time to event curve dataframe
    """
    indices = [float(num) for num in list(np.arange(0.01, 1, 0.01).round(2))]
    age_groups = list(range(1, 7))
    age_groups_str = [str(num) for num in age_groups]
    referral_type = ["early", "late"]
    cols = [
        "_".join(patient_type)
        for patient_type in list(product(age_groups_str, referral_type))
    ]
    try:
        assert list(tte_df.index) == indices
        assert list(tte_df.columns) == cols
    except AssertionError:
        raise ValueError(f"Check {tte_df_name} csv - incorrect indices/columns")
