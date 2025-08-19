"""
This module contains the configuration for running the model.
It can later be adapted to take inputs from users
"""


class g:
    trace = True
    number_of_runs = 100
    sim_duration = 365
    random_seed = 0
    arrival_rate = 1

    # distributions for calculating interarrival times
    age_dist = {
        1: 0.051024846,
        2: 0.06697011,
        3: 0.098222828,
        4: 0.169019801,
        5: 0.270344708,
        6: 0.344417708,
    }
    referral_dist = {"early": 0.856711916, "late": 0.143288084}

    con_care_dist = {
        1: 0.1,
        2: 0.1,
        3: 0.1,
        4: 0.1,
        5: 0.25,
        6: 0.5,
    }

    ttd_con_care_shape = 0.66
    ttd_con_care_scale = 92.86
