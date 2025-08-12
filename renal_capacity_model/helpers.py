"""
Module with helper functions
"""

from config import g


def get_interarrival_times():
    """Calculates interarrival times using values in config

    Returns:
        dict: Dictionary containing different interarrival times for use in model
    """
    iat_dict = {}
    for stage, stage_value in g.referral_dist.items():
        for age_group, age_value in g.age_dist.items():
            iat_dict[f"{age_group}_{stage}"] = 1 / (age_value * stage_value)
    return iat_dict
