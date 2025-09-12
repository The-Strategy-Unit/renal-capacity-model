"""
Module with helper functions
"""


def get_interarrival_times(config):
    """Calculates interarrival times using values in config
    Args:
        config (Config): Config Class containing values to be used for model run

    Returns:
        dict: Dictionary containing different interarrival times for use in model
    """
    iat_dict = {}
    for referral, referral_value in config.referral_dist.items():
        for age_group, age_value in config.age_dist.items():
            iat_dict[f"{age_group}_{referral}"] = config.arrival_rate / (
                age_value * referral_value
            )
    return iat_dict
