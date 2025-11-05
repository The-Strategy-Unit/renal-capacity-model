"""
Module with helper functions
"""

import pandas as pd


def get_yearly_interarrival_times(config):
    mean_iat_over_time = {}
    years = int(config.sim_duration / 365)
    for year in range(1, years + 1):
        mean_iat_over_time[year] = get_interarrival_times(
            config.arrival_rate[year], config.referral_dist, config.age_dist
        )
    return mean_iat_over_time


def transform_mean_iat_over_time(mean_iat_over_time):
    mean_iat_over_time_dfs = {}
    df = pd.DataFrame(mean_iat_over_time)
    df.columns = [(col - 1) * 365 for col in df.columns]
    for i in df.index:
        mini_df = pd.DataFrame(df.loc[i])
        mean_iat_over_time_dfs[i] = mini_df.reset_index().rename(
            columns={"index": "t", i: "mean_iat"}
        )
    return mean_iat_over_time_dfs


def get_interarrival_times(arrival_rate, referral_dist, age_dist):
    """Calculates interarrival times for different patient groups

    Args:
        arrival_rate (float): Arrival rate in a given year
        referral_dist (dict): Distribution of different referral types
        age_dist (dict): Distribution of different age groups

    Returns:
        dict: Dictionary containing different interarrival times for patient groups, given a single arrival rate
    """

    iat_dict = {}
    for referral, referral_value in referral_dist.items():
        for age_group, age_value in age_dist.items():
            iat_dict[f"{age_group}_{referral}"] = arrival_rate / (
                age_value * referral_value
            )
    return iat_dict


def check_config_duration_valid(config):
    """Checks that config values which change over the sim duration are provided

    Args:
        config (Config): Config Class containing values to be used for model run
    """
    config_values_to_check = ["arrival_rate"]  # we'll add more here - see issue #86
    sim_years = config.sim_duration / 365
    for config_value in config_values_to_check:
        if len(getattr(config, config_value)) < sim_years:
            raise ValueError(
                f"{config_value} does not include enough years for sim duration"
            )
    return True
