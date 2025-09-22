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
        self.number_of_runs = config_dict.get("number_of_runs", 10)
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

        self.suitable_for_transplant_dist = config_dict.get(
            "suitable_for_transplant_dist",
            {
                1: 0.9,
                2: 0.8,
                3: 0.7,
                4: 0.5,
                5: 0.25,
                6: 0.03,
            },
        )

        self.transplant_type_dist = config_dict.get(
            "transplant_type_dist",
             {   
                1: 0.4,
                2: 0.3,
                3: 0.3,
                4: 0.25,
                5: 0.2,
                6: 0.1,
             }
        )

        self.modality_allocation_none_dist = config_dict.get(
            "modality_allocation_none_dist",
            {
                "ichd": 0.75,
                "hhd": 0.01,
                "pd": 0.24,
            },
        )

        self.modality_allocation_ichd_dist = config_dict.get(
            "modality_allocation_ichd_dist",
            {
                "ichd": 0,
                "hhd": 0.4,
                "pd": 0.6,
            },
        )

        self.modality_allocation_hhd_dist = config_dict.get(
            "modality_allocation_hhd_dist",
            {
                "ichd": 0.95,
                "hhd": 0,
                "pd": 0.05,
            },
        )

        self.modality_allocation_pd_dist = config_dict.get(
            "modality_allocation_pd_dist",
            {
                "ichd": 0.99,
                "hhd": 0.01,
                "pd": 0,
            },
        )

        self.pre_emptive_transplant_live_donor_dist = config_dict.get(
            "pre_emptive_transplant_live_donor_dist", {"early": 0.5, "late": 0.1}
        )
        
        self.pre_emptive_transplant_cadaver_donor_dist = config_dict.get(
            "pre_emptive_transplant_cadaver_donor_dist", {"early": 0.2, "late": 0.01}
        )

        self.ttd_con_care_shape = config_dict.get("ttd_con_care_shape", 0.5)
        self.ttd_con_care_scale = config_dict.get("ttd_con_care_scale", 100)

        self.tw_before_dialysis_shape = config_dict.get("tw_before_dialysis_shape", 1)
        self.tw_before_dialysis_scale = config_dict.get("tw_before_dialysis_scale", 450)
