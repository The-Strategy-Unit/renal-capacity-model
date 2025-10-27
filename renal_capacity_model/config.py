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
        self.sim_duration = config_dict.get(
            "sim_duration", int(1) #2 * 365)
        )  # in days, but should be a multiple of 365 i.e. years
        self.random_seed = config_dict.get("random_seed", 0)
        self.arrival_rate = config_dict.get("arrival_rate", 1)
        self.snapshot_interval = config_dict.get(
            "snapshot_interval", int(365)
        )  # how often to take a snapshot of the results_df
        
        # how many people are in each activity at time zero
        self.prevalent_counts = config_dict.get(
            "prevalent_counts",
            {
                "conservative_care" : {
                    "1_early": 1,
                    "2_early": 1,
                    "3_early": 1, 
                    "4_early": 1,
                    "5_early": 1,
                    "6_early": 1,
                    "1_late": 1,
                    "2_late": 1,
                    "3_late": 1,
                    "4_late": 1,
                    "5_late": 1,
                    "6_late": 1,
                },
                "ichd" : {
                    "1_early": 1,
                    "2_early": 1,
                    "3_early": 1, 
                    "4_early": 1,
                    "5_early": 1,
                    "6_early": 1,
                    "1_late": 1,
                    "2_late": 1,
                    "3_late": 1,
                    "4_late": 1,
                    "5_late": 1,
                    "6_late": 1,
                },
                "hhd" : {
                    "1_early": 1,
                    "2_early": 1,
                    "3_early": 1, 
                    "4_early": 1,
                    "5_early": 1,
                    "6_early": 1,
                    "1_late": 1,
                    "2_late": 1,
                    "3_late": 1,
                    "4_late": 1,
                    "5_late": 1,
                    "6_late": 1,
                },
                "pd" : {
                    "1_early": 1,
                    "2_early": 1,
                    "3_early": 1, 
                    "4_early": 1,
                    "5_early": 1,
                    "6_early": 1,
                    "1_late": 1,
                    "2_late": 1,
                    "3_late": 1,
                    "4_late": 1,
                    "5_late": 1,
                    "6_late": 1,
                },
                "live_transplant" : {
                    "1_early": 1,
                    "2_early": 1,
                    "3_early": 1, 
                    "4_early": 1,
                    "5_early": 1,
                    "6_early": 1,
                    "1_late": 1,
                    "2_late": 1,
                    "3_late": 1,
                    "4_late": 1,
                    "5_late": 1,
                    "6_late": 1,
                },
                "cadaver_transplant" : {
                    "1_early": 1,
                    "2_early": 1,
                    "3_early": 1, 
                    "4_early": 1,
                    "5_early": 1,
                    "6_early": 1,
                    "1_late": 1,
                    "2_late": 1,
                    "3_late": 1,
                    "4_late": 1,
                    "5_late": 1,
                    "6_late": 1,
                },
            },
        ) 
        
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

        #routing distributions (to be fed in externally for each geography under study - these are defaults unrelated to any particular geography)
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
            },
        )

        self.modality_allocation_distributions = config_dict.get(
            "modality_allocation_distributions",
            {
                "none": {
                    "ichd": 0.75,
                    "hhd": 0.01,
                    "pd": 0.24,
                },
                "ichd": {
                    "ichd": 0,
                    "hhd": 0.4,
                    "pd": 0.6,
                },
                "hhd": {
                    "ichd": 0.95,
                    "hhd": 0,
                    "pd": 0.05,
                },
                "pd": {
                    "ichd": 0.99,
                    "hhd": 0.01,
                    "pd": 0,
                },
            },
        )

        self.death_post_transplant = config_dict.get(
            "death_post_transplant",
            {
                "live": 0.4,
                "cadaver": 0.5,
            },
        )

        self.death_post_dialysis_modality = config_dict.get(
            "death_post_dialysis_modality",
            {
                "ichd": {
                    1: 0.6,
                    2: 0.7,
                    3: 0.75,
                    4: 0.8,
                    5: 0.9,
                    6: 0.9,
                },
                "hhd": {
                    1: 0.6,
                    2: 0.7,
                    3: 0.75,
                    4: 0.8,
                    5: 0.9,
                    6: 0.9,
                },
                "pd": {
                    1: 0.6,
                    2: 0.7,
                    3: 0.75,
                    4: 0.8,
                    5: 0.9,
                    6: 0.9,
                },
            },
        )

        self.pre_emptive_transplant_live_donor_dist = config_dict.get(
            "pre_emptive_transplant_live_donor_dist",
            {"early": 0.5, "late": 0.1},
        )

        self.pre_emptive_transplant_cadaver_donor_dist = config_dict.get(
            "pre_emptive_transplant_cadaver_donor_dist",
            {"early": 0.2, "late": 0.01},
        )

        #time to event distribution parameters (these are the same regardless of geography).

        ## initialisation input distributions ##
        self.ttma_initial_distribution = config_dict.get(
            "ttma_initial_distribution",
            {
                "ichd" : {
                    1: {
                       "proportion_uncensored":0.86, 
                       "shape":0.86,
                       "scale":647,  
                    },
                    2: {
                       "proportion_uncensored":0.75, 
                       "shape":0.93,
                       "scale":639,  
                    },
                    3: {
                       "proportion_uncensored":0.78,
                       "shape":1.09,
                       "scale":717,  
                    },
                    4: {
                        "proportion_uncensored":0.78,
                       "shape":0.9,
                       "scale":542,  
                    },
                    5: {
                        "proportion_uncensored":0.79,
                       "shape":0.97,
                       "scale":643,  
                    },
                    6: {
                        "proportion_uncensored":0.87,
                       "shape":0.9,
                       "scale":632,  
                    },                    
                },
                "hhd" : {
                    1: {
                        "proportion_uncensored":0.68,
                        "shape":0.92,
                        "scale":794,  
                    },
                    2: {
                        "proportion_uncensored":0.86,
                        "shape":0.92,
                        "scale":794,  
                    },
                    3: {
                        "proportion_uncensored":0.92,
                        "shape":0.92,
                        "scale":794,  
                    },
                    4: {
                        "proportion_uncensored":0.94,
                        "shape":0.92,
                        "scale":794,  
                    },
                    5: {
                        "proportion_uncensored":1.00,
                        "shape":0.92,
                        "scale":794,  
                    },
                    6: {
                        "proportion_uncensored":1.00,
                        "shape":0.92,
                        "scale":794,    
                    },      
                },
                "pd" : {
                    1: {
                        "proportion_uncensored":1.00,
                       "shape":0.98,
                       "scale":675, 
                    },
                    2: {
                        "proportion_uncensored":1.00,
                       "shape":0.97,
                       "scale":696, 
                    },
                    3: {
                        "proportion_uncensored":1.00,
                       "shape":0.92,
                       "scale":655,  
                    },
                    4: {
                        "proportion_uncensored":0.99,
                       "shape":1,
                       "scale":604,
                    },
                    5: {
                        "proportion_uncensored":1.00,
                       "shape":0.96,
                       "scale":694,  
                    },
                    6: {
                        "proportion_uncensored":1.00,
                       "shape":1.09,
                       "scale":619,  
                    },                    
                },
            },
        )

        self.ttd_initial_distribution = config_dict.get(
            "ttd_distribution",
            {
                "ichd": {
                    1: {
                        "proportion_uncensored":0.84,   
                        "shape":1.02,
                        "scale":1123,
                    },
                    2: {
                        "proportion_uncensored":0.85,   
                        "shape":1.03,
                        "scale":1080,
                    },
                    3: {
                        "proportion_uncensored":0.92,   
                        "shape":1.01,
                        "scale":1127,
                    },
                    4: {
                        "proportion_uncensored":0.96,   
                        "shape":1.05,
                        "scale":1192,
                    },
                    5: {
                        "proportion_uncensored":0.99,   
                        "shape":1.06,
                        "scale":1175,
                    },
                    6: {
                        "proportion_uncensored":1.00,   
                        "shape":1.05,
                        "scale":1218,
                    },
                },
                "hhd": {
                    1: {
                        "proportion_uncensored":0.3,   
                        "shape":1.09,
                        "scale":1456,
                    },
                    2: {
                        "proportion_uncensored":0.57,   
                        "shape":1.09,
                        "scale":1456,
                    },
                    3: {
                        "proportion_uncensored":0.83,   
                        "shape":1.09,
                        "scale":1456,
                    },
                    4: {
                        "proportion_uncensored":0.91,   
                        "shape":1.09,
                        "scale":1456,
                    },
                    5: {
                        "proportion_uncensored":1.00,   
                        "shape":1.09,
                        "scale":1456,
                    },
                    6: {
                        "proportion_uncensored":1.00,   
                        "shape":1.09,
                        "scale":1456,
                    },
                },
                "pd": {
                    1: {
                        "proportion_uncensored":1.00,   
                        "shape":1.03,
                        "scale":847,
                    },
                    2: {
                        "proportion_uncensored":1.00,   
                        "shape":1.03,
                        "scale":847,
                    },
                    3: {
                        "proportion_uncensored":0.98,   
                        "shape":1.03,
                        "scale":847,
                    },
                    4: {
                        "proportion_uncensored":0.98,   
                        "shape":1.07,
                        "scale":702,
                    },
                    5: {
                        "proportion_uncensored":1.00,   
                        "shape":1.09,
                        "scale":800,
                    },
                    6: {
                        "proportion_uncensored":1.00,   
                        "shape":1.04,
                        "scale":803,
                    },
                },            
            },
        )

        self.ttd_tx_initial_distribution = config_dict.get(
            "ttd_tx_initial_distribution",
            {
                "live": {
                    1: {
                        "proportion_uncensored":0.08,
                        "lower_bound":0,
                        "upper_bound":self.sim_duration,
                    },
                    2: {
                        "proportion_uncensored":0.16,
                        "lower_bound":0,
                        "upper_bound":self.sim_duration,
                    },
                    3: {
                        "proportion_uncensored":0.27,
                        "lower_bound":0,
                        "upper_bound":self.sim_duration,
                    },
                    4: {
                        "proportion_uncensored":0.43,
                        "lower_bound":0,
                        "upper_bound":self.sim_duration,
                    },
                    5: {
                        "proportion_uncensored":0.73,
                        "lower_bound":0,
                        "upper_bound":self.sim_duration,
                    },
                    6: {
                        "proportion_uncensored":0.95,
                        "lower_bound":0,
                        "upper_bound":self.sim_duration,
                    },                    
                },
                "cadaver": {
                    1: {
                        "proportion_uncensored":0.1,
                        "lower_bound":0,
                        "upper_bound":self.sim_duration,
                    },
                    2: {
                        "proportion_uncensored":0.22,
                        "lower_bound":0,
                        "upper_bound":self.sim_duration,
                    },
                    3: {
                        "proportion_uncensored":0.35,
                        "lower_bound":0,
                        "upper_bound":self.sim_duration,
                    },
                    4: {
                        "proportion_uncensored":0.59,
                        "lower_bound":0,
                        "upper_bound":self.sim_duration,
                    },
                    5: {
                        "proportion_uncensored":0.84,
                        "lower_bound":0,
                        "upper_bound":self.sim_duration,
                    },
                    6: {
                        "proportion_uncensored":0.96,
                        "lower_bound":0,
                        "upper_bound":self.sim_duration,
                    },                    
                },            
            },
        )

        self.ttgf_tx_initial_distribution = config_dict.get(
            "ttgf_tx_initial_distribution",
            {
                "live": {
                    1: {
                        "proportion_uncensored":0.54,
                        "shape":1.18,
                        "scale":1960,
                    },
                    2: {
                        "proportion_uncensored":0.45,
                        "shape":1.15,
                        "scale":1930,
                    },
                    3: {
                        "proportion_uncensored":0.4,
                        "shape":1.21,
                        "scale":2088,
                    },
                    4: {
                        "proportion_uncensored":0.43,
                        "shape":1.12,
                        "scale":1802,
                    },
                    5: {
                        "proportion_uncensored":0.58,
                        "shape":1.2,
                        "scale":1920,
                    },
                    6: {
                        "proportion_uncensored":0.8,
                        "shape":1.2,
                        "scale":1920,
                    },                    
                },
                "cadaver": {
                    1: {
                        "proportion_uncensored":0.54,
                        "shape":1.17,
                        "scale":1892,
                    },
                    2: {
                        "proportion_uncensored":0.5,
                        "shape":1.11,
                        "scale":1864,
                    },
                    3: {
                        "proportion_uncensored":0.48,
                        "shape":1.24,
                        "scale":1934,
                    },
                    4: {
                        "proportion_uncensored":0.53,
                        "shape":1.22,
                        "scale":1868,
                    },
                    5: {
                        "proportion_uncensored":0.69,
                        "shape":1.23,
                        "scale":1881,
                    },
                    6: {
                        "proportion_uncensored":0.83,
                        "shape":1.27,
                        "scale":2021,
                    },                        
                },            
            },
        )

        ## within run input distributions ##
        self.time_on_waiting_list_mean = config_dict.get(
            "time_on_waiting_list_mean",
            {
                "live": 4.5 * 30,  # 3-6 months on average
                "cadaver": 365 * 2.5 * 30,  # 2-3 years on average
            },
        )
        
        self.ttd_con_care = config_dict.get(
            "ttd_con_care",
            {
                "shape" : 0.5,
                "scale" : 100,
            }
        )

        self.tw_before_dialysis =config_dict.get(
            "tw_before_dialysis", 
            {
                "shape": 1,
                "scale": 450,
            }
        )

        self.ttd_distribution = config_dict.get(
            "ttd_distribution",
            {
                "ichd": {
                    1: {   
                        "shape":0.76,
                        "scale":1/0.001,
                    },
                    2: {
                        "shape":0.66,
                        "scale":1/0.0005,
                    },
                    3: {
                        "shape":0.68,
                        "scale":1/0.0005,
                    },
                    4: {
                        "shape":0.67,
                        "scale":1/0.0005,
                    },
                    5: {
                        "shape":0.76,
                        "scale":1/0.001,
                    },
                    6: {
                        "shape":0.67,
                        "scale":1/0.0004,
                    },
                },
                "hhd": {
                    1: {   
                        "shape":0.58,
                        "scale":1/0.000001,
                    },
                    2: {
                        "shape":0.58,
                        "scale":1/0.000001,
                    },
                    3: {
                        "shape":0.58,
                        "scale":1/0.000001,
                    },
                    4: {
                        "shape":0.58,
                        "scale":1/0.000001,
                    },
                    5: {
                        "shape":0.58,
                        "scale":1/0.000001,
                    },
                    6: {
                        "shape":0.58,
                        "scale":1/0.000001,
                    },
                },
                "pd": {
                    1: {   
                        "shape":0.9,
                        "scale":1/0.0008,
                    },
                    2: {
                        "shape":0.85,
                        "scale":1/0.0008,
                    },
                    3: {
                        "shape":0.87,
                        "scale":1/0.0008,
                    },
                    4: {
                        "shape":0.9,
                        "scale":1/0.0009,
                    },
                    5: {
                        "shape":0.92,
                        "scale":1/0.0009,
                    },
                    6: {
                        "shape":0.89,
                        "scale":1/0.0008,
                    },
                },
            }
        )

        self.ttma_distribution = config_dict.get(
            "ttma_distribution",
            {
                "ichd": {
                    1: {   
                        "shape":0.47,
                        "scale":1/0.0009,
                    },
                    2: {
                        "shape":0.51,
                        "scale":1/0.001,
                    },
                    3: {
                        "shape":0.51,
                        "scale":1/0.0009,
                    },
                    4: {
                        "shape":0.55,
                        "scale":1/0.0009,
                    },
                    5: {
                        "shape":0.6,
                        "scale":1/0.0009,
                    },
                    6: {
                        "shape":0.6,
                        "scale":1/0.0009,
                    },
                },
                "hhd": {
                    1: {   
                        "shape":0.56,
                        "scale":1/0.001,
                    },
                    2: {
                        "shape":0.51,
                        "scale":1/0.001,
                    },
                    3: {
                        "shape":0.6,
                        "scale":1/0.001,
                    },
                    4: {
                        "shape":0.57,
                        "scale":1/0.0008,
                    },
                    5: {
                        "shape":0.58,
                        "scale":1/0.001,
                    },
                    6: {
                        "shape":0.54,
                        "scale":1/0.001,
                    },
                },
                "pd": {
                    1: {   
                        "shape":0.86,
                        "scale":1/0.002,
                    },
                    2: {
                        "shape":0.82,
                        "scale":1/0.002,
                    },
                    3: {
                        "shape":0.81,
                        "scale":1/0.002,
                    },
                    4: {
                        "shape":0.89,
                        "scale":1/0.002,
                    },
                    5: {
                        "shape":0.87,
                        "scale":1/0.002,
                    },
                    6: {
                        "shape":0.88,
                        "scale":1/0.002,
                    },
                },
            }
        )

        self.ttd_tx_distribution = config_dict.get(
            "ttd_tx_distribution",
            {
                "live": {
                    1: {
                        "shape":0.99,
                        "scale":25138,
                    },
                    2: {
                        "shape":0.99,
                        "scale":25138,
                    },
                    3: {
                        "shape":0.99,
                        "scale":25138,
                    },
                    4: {
                        "shape":1.21,
                        "scale":7077,
                    },
                    5: {
                        "shape":1.41,
                        "scale":4462,
                    },
                    6: {
                        "shape":1.41,
                        "scale":4462,
                    },                    
                },
                "cadaver": {
                    1: {
                        "shape":0.98,
                        "scale":14777,
                    },
                    2: {
                        "shape":0.98,
                        "scale":14777,
                    },
                    3: {
                        "shape":1.04,
                        "scale":6837,
                    },
                    4: {
                        "shape":1,
                        "scale":4830,
                    },
                    5: {
                        "shape":1.01,
                        "scale":3938,
                    },
                    6: {
                        "shape":0.95,
                        "scale":3521,
                    },                    
                },            
            },
        )

        self.ttgf_tx_distribution = config_dict.get(
            "ttgf_tx_distribution",
            {
                "live": {
                    1: {
                        "break_point" : 365/12,
                        "mode":7,
                        "proportion_below_break":0.2,
                        "shape":0.5,
                        "scale":4977,
                    },
                    2: {
                        "break_point" : 365/12,
                        "mode":7,
                        "proportion_below_break":0.2,
                        "shape":0.5,
                        "scale":4977,
                    },
                    3: {
                        "break_point" : 365/12,
                        "mode":7,
                        "proportion_below_break":0.2,
                        "shape":0.5,
                        "scale":4977,
                    },
                    4: {
                        "break_point" : 365/12,
                        "mode":7,
                        "proportion_below_break":0.2,
                        "shape":0.5,
                        "scale":4977,
                    },
                    5: {
                        "break_point" : 365/12,
                        "mode":7,
                        "proportion_below_break":0.2,
                        "shape":0.5,
                        "scale":4977,
                    },
                    6: {
                        "break_point" : 365/12,
                        "mode":7,
                        "proportion_below_break":0.2,
                        "shape":0.5,
                        "scale":4977,
                    }, 
                },
                "cadaver": {
                    1: {
                        "break_point" : 365/12,
                        "mode":1,
                        "proportion_below_break":0.24,
                        "shape":0.54,
                        "scale":2547,
                    },
                    2: {
                        "break_point" : 365/12,
                        "mode":1,
                        "proportion_below_break":0.24,
                        "shape":0.54,
                        "scale":2547,
                    },
                    3: {
                        "break_point" : 365/12,
                        "mode":1,
                        "proportion_below_break":0.24,
                        "shape":0.54,
                        "scale":2547,
                    },
                    4: {
                        "break_point" : 365/12,
                        "mode":1,
                        "proportion_below_break":0.24,
                        "shape":0.54,
                        "scale":2547,
                    },
                    5: {
                        "break_point" : 365/12,
                        "mode":1,
                        "proportion_below_break":0.24,
                        "shape":0.54,
                        "scale":2547,
                    },
                    6: {
                        "break_point" : 365/12,
                        "mode":1,
                        "proportion_below_break":0.24,
                        "shape":0.54,
                        "scale":2547,
                    },
                     
                },            
            },
        )
