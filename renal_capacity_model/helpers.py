"""
Module with helper functions
"""

import pandas as pd
import math


def get_yearly_arrival_rate(config):
    mean_arrival_rates = {}
    years = calculate_lookup_year(config.sim_duration)
    for year in range(1, years + 1):
        mean_arrival_rates[year] = get_arrival_rate(
            config.arrival_rate[year], config.referral_dist, config.age_dist
        )
    return mean_arrival_rates


def get_mean_iat_over_time_from_arrival_rate(arrival_rate_dict):
    mean_iat_over_time_dfs = {}
    df = pd.DataFrame(arrival_rate_dict)
    df.columns = [(col - 1) * 365 for col in df.columns]
    for i in df.index:
        mini_df = pd.DataFrame(df.loc[i])
        mini_df = mini_df.reset_index().rename(
            columns={"index": "t", i: "arrival_rate"}
        )
        mini_df["mean_iat"] = 1 / mini_df["arrival_rate"]
        mean_iat_over_time_dfs[i] = mini_df
    return mean_iat_over_time_dfs


def get_arrival_rate(arrival_rate, referral_dist, age_dist):
    """Calculates interarrival times for different patient groups

    Args:
        arrival_rate (float): Arrival rate in a given year
        referral_dist (dict): Distribution of different referral types
        age_dist (dict): Distribution of different age groups

    Returns:
        dict: Dictionary containing different interarrival times for patient groups, given a single arrival rate
    """

    arrival_rate_dict = {}
    for referral, referral_value in referral_dist.items():
        for age_group, age_value in age_dist.items():
            arrival_rate_dict[f"{age_group}_{referral}"] = arrival_rate * (
                age_value * referral_value
            )
    return arrival_rate_dict


def check_config_duration_valid(config):
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
        "time_on_waiting_list_mean",
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


def calculate_incidence(event_log):
    incidence = event_log.groupby("year_start")["activity_from"].value_counts()
    incidence = incidence.unstack(level="year_start")
    incidence.index = ["incidence_" + activity for activity in incidence.index]
    return pd.DataFrame(incidence)


def calculate_activity_change(event_log):
    activity_change = event_log.groupby(
        ["year_start", "activity_from", "activity_to"]
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


def calculate_prevalence(event_log):
    years = list(range(1, event_log["year_end"].max()))

    rows = []
    for y in years:
        mask = (event_log["year_start"] <= y) & (event_log["year_end"] > y)
        counts = event_log[mask].groupby("activity_from")["patient_id"].nunique()
        counts.name = y
        rows.append(counts)

    prevalence = pd.DataFrame(rows).fillna(0).astype(int)
    prevalence = prevalence.T
    prevalence.index = ["prevalence_" + activity for activity in prevalence.index]
    return prevalence


def process_event_log(event_log: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Processes event log for easier validation and debugging

    Args:
        event_log (pd.DataFrame): event log

    Returns:
        tuple with two Pandas dataframes: one recording incidence of patients in each
        treatment modality for each year of simulation, and the other recording changes
        in activity for each year of simulation.
    """
    event_log["year_start"] = event_log["time_starting_activity_from"].apply(
        calculate_lookup_year
    )
    event_log["end_time"] = (
        event_log["time_starting_activity_from"]
        + event_log["time_spent_in_activity_from"]
    )
    event_log["year_end"] = event_log["end_time"].apply(calculate_lookup_year)
    incidence = calculate_incidence(event_log)
    activity_change = calculate_activity_change(event_log)
    return incidence, activity_change
