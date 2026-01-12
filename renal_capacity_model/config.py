"""
This module contains the configuration for running the model.
It can be adapted to take inputs from users
"""

from renal_capacity_model.helpers import (
    get_yearly_arrival_rate,
    get_mean_iat_over_time_from_arrival_rate,
)
from renal_capacity_model.config_values import (
    national_config_dict,
    load_time_to_event_curves,
    ttd_con_care_values,
    tw_before_dialysis_values,
    ttd_krt_values,
    tw_cadTx_values,
    tw_liveTx_values,
    tw_cadTx_initialisation_values,
    tw_liveTx_initialisation_values,
)
from renal_capacity_model.utils import get_logger

logger = get_logger(__name__)


class Config:
    """
    Config class for storing values
    """

    def __init__(
        self,
        config_dict: dict = national_config_dict,
        path_to_time_to_event_curves: str = "reference/survival_time_to_event_curves",
    ):
        """Initialises config for running the model

        Args:
            config_dict (dict, optional): Dict containing values to be used to run the model. Defaults to national_config_dict.
            path_to_time_to_event_curves (str, optional): Path to folder containing time to event curves as CSV files. Defaults to "reference/survival_time_to_event_curves".
        """
        self.trace = config_dict.get("trace", False)
        self.initialise_prevalent_patients = config_dict.get(
            "initialise_prevalent_patients", True
        )  # whether to initialise model with prevalent counts (takes a long time using default national values)
        self.number_of_runs = config_dict.get("number_of_runs", 10)
        self.sim_duration = config_dict.get(
            "sim_duration", int(13 * 365)
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
        self.receives_transplant_dist = config_dict["receives_transplant_dist"]
        self.transplant_type_dist = config_dict["transplant_type_dist"]
        self.modality_allocation_distributions = config_dict[
            "modality_allocation_distributions"
        ]
        self.pre_emptive_transplant_live_donor_dist = config_dict[
            "pre_emptive_transplant_live_donor_dist"
        ]

        self.pre_emptive_transplant_cadaver_donor_dist = config_dict[
            "pre_emptive_transplant_cadaver_donor_dist"
        ]
        # time to event distribution parameters (these are the same regardless of geography)
        self.ttd_con_care = ttd_con_care_values
        self.ttd_krt = ttd_krt_values
        self.tw_cadTx = tw_cadTx_values
        self.tw_liveTx = tw_liveTx_values
        self.tw_cadTx_initialisation = tw_cadTx_initialisation_values
        self.tw_liveTx_initialisation = tw_liveTx_initialisation_values
        self.tw_before_dialysis = tw_before_dialysis_values
        self.multipliers = config_dict["multipliers"]
        self.time_to_event_curves = load_time_to_event_curves(
            path_to_time_to_event_curves
        )
        self.daily_costs = config_dict["daily_costs"]
        logger.info("🔧 Config loaded successfully")
