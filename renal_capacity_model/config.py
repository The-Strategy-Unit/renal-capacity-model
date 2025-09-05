"""
This module contains the configuration for running the model.
It can later be adapted to take inputs from users
"""


class Config:
    """
    Config class for storing values
    """

    def __init__(self, config_dict={}):
        self.trace = config_dict.get("trace", False)
        self.number_of_runs = config_dict.get("number_of_runs", 100)
        self.sim_duration = config_dict.get("sim_duration", 1000)
        self.random_seed = config_dict.get("random_seed", 0)
        self.arrival_rate = config_dict.get("arrival_rate", 1)

        # distributions for calculating interarrival times
        self.age_dist = config_dict.get(
            "age_dist",
            {
                1: 0.051024846,
                2: 0.06697011,
                3: 0.098222828,
                4: 0.169019801,
                5: 0.270344708,
                6: 0.344417708,
            },
        )
        self.referral_dist = config_dict.get(
            "referral_dist", {"early": 0.856711916, "late": 0.143288084}
        )

        self.con_care_dist = config_dict.get(
            "con_care_dist",
            {
                1: 0.1,
                2: 0.1,
                3: 0.1,
                4: 0.1,
                5: 0.25,
                6: 0.5,
            },
        )

        self.ttd_con_care_shape = config_dict.get("ttd_con_care_shape", 0.66)
        self.ttd_con_care_scale = config_dict.get("ttd_con_care_scale", 92.86)
