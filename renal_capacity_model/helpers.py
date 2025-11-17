"""
Module with helper functions
"""

import pandas as pd


def get_yearly_arrival_rate(config):
    mean_arrival_rates = {}
    years = int(config.sim_duration / 365)
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
    sim_years = config.sim_duration / 365
    for config_value in config_values_to_check:
        if len(getattr(config, config_value)) < sim_years:
            raise ValueError(
                f"{config_value} does not include enough years for sim duration"
            )
    return True
