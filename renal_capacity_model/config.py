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

        self.death_post_transplant  = config_dict.get(
            "death_post_transplant", 
            {
                "live": 0.4,
                "cadaver": 0.5,
            },
        )

        self.time_on_waiting_list_mean = config_dict.get(
            "time_on_waiting_list_mean", 
            {
                "live": 4.5*30,             # 3-6 months on average
                "cadaver": 365*2.5*30,      # 2-3 years on average
            },
        )

        self.pre_emptive_transplant_live_donor_dist = config_dict.get(
            "pre_emptive_transplant_live_donor_dist", {"early": 0.5, "late": 0.1},
        )
        
        self.pre_emptive_transplant_cadaver_donor_dist = config_dict.get(
            "pre_emptive_transplant_cadaver_donor_dist", {"early": 0.2, "late": 0.01},
        )

        self.ttd_con_care_shape = config_dict.get("ttd_con_care_shape", 0.5)
        self.ttd_con_care_scale = config_dict.get("ttd_con_care_scale", 100)

        self.tw_before_dialysis_shape = config_dict.get("tw_before_dialysis_shape", 1)
        self.tw_before_dialysis_scale = config_dict.get("tw_before_dialysis_scale", 450)

        self.live_tx_ttd_shape = config_dict.get(
            "live_tx_ttd_shape",
             {   
                1: 1,
                2: 0.5,
                3: 1,
                4: 1,
                5: 1.5,
                6: 1.5,
             },
        )

        self.live_tx_ttd_scale = config_dict.get(
            "live_tx_ttd_scale",
             {   
                1: 47000,
                2: 100000,
                3: 5000,
                4: 5000,
                5: 2500,
                6: 2500,
             },
        )

        self.live_tx_ttgf_shape = config_dict.get(
            "live_tx_ttgf_shape",
             {   
                1: 1.,
                2: 1,
                3: 1,
                4: 2,
                5: 2,
                6: 2,
             },
        )

        self.live_tx_ttgf_scale = config_dict.get(
            "live_tx_ttgf_scale",
             {   
                1: 1500,
                2: 1500,
                3: 1500,
                4: 2000,
                5: 2000,
                6: 2000,
             },
        )

        self.cadaver_tx_ttd_shape = config_dict.get(
            "cadaver_tx_ttd_shape",
             {   
                1: 1.5,
                2: 1,
                3: 1,
                4: 1,
                5: 1.25,
                6: 1.25,
             },
        )

        self.cadaver_tx_ttd_scale = config_dict.get(
            "cadaver_tx_ttd_scale",
             {   
                1: 10000,
                2: 15000,
                3: 8000,
                4: 4000,
                5: 2500,
                6: 2500,
             },
        )

        self.cadaver_tx_ttgf_shape = config_dict.get(
            "cadaver_tx_ttgf_shape",
             {   
                1: 1,
                2: 1,
                3: 1,
                4: 2,
                5: 2,
                6: 2,
             },
        )

        self.cadaver_tx_ttgf_scale = config_dict.get(
            "cadaver_tx_ttgf_scale",
             {   
                1: 1500,
                2: 1500,
                3: 1500,
                4: 2000,
                5: 2000,
                6: 2000,
             },
        )

        self.death_post_ichd = config_dict.get(
            "live_tx_ttd_scale",
             {   
                1: 0.6,
                2: 0.7,
                3: 0.75,
                4: 0.8,
                5: 0.9,
                6: 0.9,
             },
        )

        self.death_post_hhd = config_dict.get(
            "live_tx_ttd_scale",
             {   
                1: 0.4,
                2: 0.4,
                3: 0.4,
                4: 0.4,
                5: 0.4,
                6: 0.4,
             },
        )

        self.death_post_pd = config_dict.get(
            "live_tx_ttd_scale",
             {   
                1: 0.45,
                2: 0.45,
                3: 0.45,
                4: 0.45,
                5: 0.45,
                6: 0.45,
             },
        )

        self.ttd_ichd_shape = config_dict.get(
            "ttd_ichd_shape",
            {
                1: 0.9,
                2: 0.9,
                3: 0.9,
                4: 0.9,
                5: 0.9,
                6: 0.9,
            },
        )
        
        self.ttd_ichd_scale = config_dict.get(
            "ttd_ichd_scale",
            {
                1: 1500,
                2: 1500,
                3: 1500,
                4: 1250,
                5: 1000,
                6: 1000,
            },
        )

        self.ttma_ichd_shape = config_dict.get(
            "ttma_ichd_shape",
            {
                1: 0.5,
                2: 0.5,
                3: 0.5,
                4: 0.5,
                5: 0.5,
                6: 0.5,
            },
        )
        
        self.ttma_ichd_scale = config_dict.get(
            "ttma_ichd_scale",
            {
                1: 1500,
                2: 1000,
                3: 750,
                4: 500,
                5: 500,
                6: 250,
            },
        )