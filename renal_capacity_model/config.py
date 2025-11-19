"""
This module contains the configuration for running the model.
It can later be adapted to take inputs from users
"""

from renal_capacity_model.helpers import (
    get_yearly_arrival_rate,
    get_mean_iat_over_time_from_arrival_rate,
)
from renal_capacity_model.config_values import (
    national_config_dict,
    time_to_event_distribution_parameters,
)


class Config:
    """
    Config class for storing values
    """

    def __init__(self, config_dict=national_config_dict):
        self.trace = config_dict.get("trace", True)
        self.initialise_prevalent_patients = config_dict.get(
            "initialise_prevalent_patients", True
        )  # whether to initialise model with prevalent counts (takes a long time using default national values)
        self.number_of_runs = config_dict.get("number_of_runs", 1)
        self.sim_duration = config_dict.get(
            "sim_duration", int(1 * 365)
        )  # in days, but should be a multiple of 365 i.e. years.
        self.random_seed = config_dict.get("random_seed", 0)
        self.arrival_rate = config_dict["arrival_rate"]
        # how often to take a snapshot of the results_df
        self.snapshot_interval = config_dict.get("snapshot_interval", int(365))
        # how many people are in each activity at time zero
        if self.initialise_prevalent_patients:
            self.prevalent_counts = config_dict["prevalent_counts"]
        # distributions for calculating interarrival times
        self.age_dist = config_dict["age_dist"]
        self.referral_dist = config_dict["referral_dist"]
        yearly_arrival_rate = get_yearly_arrival_rate(self)
        self.mean_iat_over_time_dfs: dict = get_mean_iat_over_time_from_arrival_rate(
            yearly_arrival_rate
        )
        # routing distributions
        self.con_care_dist = config_dict["con_care_dist"]
        self.suitable_for_transplant_dist = config_dict["suitable_for_transplant_dist"]
        self.transplant_type_dist = config_dict["transplant_type_dist"]
        self.modality_allocation_distributions = config_dict[
            "modality_allocation_distributions"
        ]
        self.death_post_transplant = config_dict["death_post_transplant"]
        self.death_post_dialysis_modality = config_dict["death_post_dialysis_modality"]

        self.pre_emptive_transplant_live_donor_dist = config_dict[
            "pre_emptive_transplant_live_donor_dist"
        ]

        self.pre_emptive_transplant_cadaver_donor_dist = config_dict[
            "pre_emptive_transplant_cadaver_donor_dist"
        ]
        self.time_on_waiting_list_mean = config_dict["time_on_waiting_list_mean"]
        # time to event distribution parameters (these are the same regardless of geography)
        ## initialisation input distributions ##
        self.ttma_initial_distribution = time_to_event_distribution_parameters[
            "ttma_initial_distribution"
        ]
        self.ttd_initial_distribution = time_to_event_distribution_parameters[
            "ttd_initial_distribution"
        ]
        self.ttd_tx_initial_distribution = time_to_event_distribution_parameters[
            "ttd_tx_initial_distribution"
        ]
        # fix upper_bound
        for tx_type in ["live", "cadaver"]:
            for i in range(1, 7):
                self.ttd_tx_initial_distribution[tx_type][i][
                    "upper_bound"
                ] = self.sim_duration
        self.ttgf_tx_initial_distribution = time_to_event_distribution_parameters[
            "ttgf_tx_initial_distribution"
        ]
        self.ttd_con_care = time_to_event_distribution_parameters["ttd_con_care"]

        self.tw_before_dialysis = time_to_event_distribution_parameters[
            "tw_before_dialysis"
        ]

        self.ttd_distribution = time_to_event_distribution_parameters[
            "ttd_distribution"
        ]
        self.ttma_distribution = time_to_event_distribution_parameters[
            "ttma_distribution"
        ]
        self.ttd_tx_distribution = time_to_event_distribution_parameters[
            "ttd_tx_distribution"
        ]
        self.ttgf_tx_distribution = time_to_event_distribution_parameters[
            "ttgf_tx_distribution"
        ]
