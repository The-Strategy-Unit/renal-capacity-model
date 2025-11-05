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
