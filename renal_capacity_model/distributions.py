"""
This module contains distributions used to calculate other values in the model.
These are currently stored as constants but we can adapt to take
"""

age_dist = {
    1: 0.051024846,
    2: 0.06697011,
    3: 0.098222828,
    4: 0.169019801,
    5: 0.270344708,
    6: 0.344417708,
}

referral_dist = {"early": 0.856711916, "late": 0.143288084}


def get_interarrival_times():
    iat_dict = {}
    for stage, stage_value in referral_dist.items():
        for age_group, age_value in age_dist.items():
            iat_dict[f"{age_group}_{stage}"] = 1 / (age_value * stage_value)
    return iat_dict
