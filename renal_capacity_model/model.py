"""
Module containing the Model class. Contains most of the logic for the simulation.
"""

import simpy
from renal_capacity_model.entity import Patient
import numpy as np
from renal_capacity_model.config import Config
from renal_capacity_model.helpers import (
    check_config_duration_valid,
    calculate_lookup_year,
    process_event_log,
    calculate_model_results,
    truncate_2dp,
)
from renal_capacity_model.utils import get_logger
import pandas as pd
from datetime import datetime
import os
from typing import Generator

logger = get_logger(__name__)


class Model:
    """
    Model class containing the logic for the simulation
    """

    def __init__(
        self,
        run_number: int,
        rng: np.random.Generator,
        config: Config,
        run_start_time: str,
    ):
        """Initialise the model

        Args:
            run_number (int): Which run number in the Trial this Model is for
            rng (np.random.Generator): Random Number Generator used for the whole experiment
            config (Config): Config Class containing values to be used for model run
        """
        self.env = simpy.Environment()
        if check_config_duration_valid(config):
            self.config = config
        self.patient_counter: int = 0
        self.run_number = run_number
        self.rng = rng
        self.patient_types = self.config.mean_iat_over_time_dfs.keys()
        self.patients_in_system: dict = {k: 0 for k in self.patient_types}
        self.event_log: pd.DataFrame = self._setup_event_log()
        self.run_start_time = run_start_time

    def _setup_event_log(self) -> pd.DataFrame:
        """Sets up DataFrame for recording model events

        Returns:
            pd.DataFrame: Empty DataFrame for recording model events
        """
        event_log = pd.DataFrame(
            columns=pd.Index(
                [
                    "patient_id",
                    "patient_type",
                    "patient_flag",
                    "activity_from",
                    "activity_to",
                    "time_starting_activity_from",
                    "time_spent_in_activity_from",
                ]
            )
        )
        return event_log

    def generator_prevalent_patient_arrivals(self, patient_type: str, location: str):
        """Generator function for prevalent patients at time zero

        Args:
            patient_type (str): Type of patient. Used to retrieve correct inter-arrival time
            location (str): Where the prevalent patient is initialised to

        Yields:
            simpy.Environment.process: starts process based on location of the patient at time t=0.
        """
        self.patient_counter += 1

        p = Patient(self.patient_counter, patient_type, 0, patient_flag="prevalent")

        self.patients_in_system[patient_type] += 1

        if location == "conservative_care":
            # these patients are diverted to conservative care. We don't need a process here as all these patients do is wait a while before leaving the system
            if self.config.trace:
                print(
                    f"Patient {p.id} of age group {p.age_group} is in conservative care at time {self.env.now}."
                )
            sampled_con_care_time = self.config.ttd_con_care[
                "scale"
            ] * self.rng.weibull(a=self.config.ttd_con_care["shape"], size=None)
            self._update_event_log(
                p,
                "conservative_care",
                "death",
                0.0,
                sampled_con_care_time,
            )
            yield self.env.timeout(sampled_con_care_time)
            self.patients_in_system[patient_type] -= 1
            if self.config.trace:
                print(
                    f"Prevalent Patient {p.id} of age group {p.age_group} diverted to conservative care and left the system after {sampled_con_care_time} time units."
                )
                # print(self.patients_in_system)
        elif location == "ichd":
            p.dialysis_modality = "ichd"
            if (
                self.rng.uniform(0, 1)
                > self.config.suitable_for_transplant_dist[p.age_group]
            ):
                p.transplant_suitable = False
                if self.config.trace:
                    print(
                        f"Patient {p.id} of age group {p.age_group} is in ICHD dialysis at time {self.env.now}."
                    )
            else:
                p.transplant_suitable = True
                p.time_enters_waiting_list = self.env.now
                if self.config.trace:
                    print(
                        f"Patient {p.id} of age group {p.age_group} is in ICHD dialysis whilst waiting for transplant at time {self.env.now}."
                    )
                if (
                    self.rng.uniform(0, 1)
                    < self.config.transplant_type_dist[p.age_group]
                ):
                    p.transplant_type = "live"
                    random_number = truncate_2dp(self.rng.uniform(0, 1))
                    p.time_on_waiting_list = self.config.time_to_event_curves[
                        "tw_liveTx_England"
                    ].loc[random_number, p.patient_type]

                else:
                    p.transplant_type = "cadaver"
                    random_number = truncate_2dp(self.rng.uniform(0, 1))
                    p.time_on_waiting_list = self.config.time_to_event_curves[
                        "tw_cadTx_England"
                    ].loc[random_number, p.patient_type]
                p.pre_emptive_transplant = False
            self.env.process(self.start_dialysis_modality(p))
        elif location == "hhd":
            p.dialysis_modality = "hhd"
            if (
                self.rng.uniform(0, 1)
                > self.config.suitable_for_transplant_dist[p.age_group]
            ):
                p.transplant_suitable = False
                if self.config.trace:
                    print(
                        f"Patient {p.id} of age group {p.age_group} is in HHD dialysis at time {self.env.now}."
                    )
            else:
                p.transplant_suitable = True
                p.time_enters_waiting_list = self.env.now
                if self.config.trace:
                    print(
                        f"Patient {p.id} of age group {p.age_group} is in HHD dialysis whilst waiting for transplant at time {self.env.now}."
                    )
                if (
                    self.rng.uniform(0, 1)
                    < self.config.transplant_type_dist[p.age_group]
                ):
                    p.transplant_type = "live"
                    random_number = truncate_2dp(self.rng.uniform(0, 1))
                    p.time_on_waiting_list = self.config.time_to_event_curves[
                        "tw_liveTx_England"
                    ].loc[random_number, p.patient_type]
                else:
                    p.transplant_type = "cadaver"
                    random_number = truncate_2dp(self.rng.uniform(0, 1))
                    p.time_on_waiting_list = self.config.time_to_event_curves[
                        "tw_cadTx_England"
                    ].loc[random_number, p.patient_type]
                p.pre_emptive_transplant = False
            self.env.process(self.start_dialysis_modality(p))
        elif location == "pd":
            p.dialysis_modality = "pd"
            if (
                self.rng.uniform(0, 1)
                > self.config.suitable_for_transplant_dist[p.age_group]
            ):
                p.transplant_suitable = False
                if self.config.trace:
                    print(
                        f"Patient {p.id} of age group {p.age_group} is in PD dialysis at time {self.env.now}."
                    )
            else:
                p.transplant_suitable = True
                p.time_enters_waiting_list = self.env.now
                if self.config.trace:
                    print(
                        f"Patient {p.id} of age group {p.age_group} is in PD dialysis whilst waiting for transplant at time {self.env.now}."
                    )
                if (
                    self.rng.uniform(0, 1)
                    < self.config.transplant_type_dist[p.age_group]
                ):
                    p.transplant_type = "live"
                    random_number = truncate_2dp(self.rng.uniform(0, 1))
                    p.time_on_waiting_list = self.config.time_to_event_curves[
                        "tw_liveTx_England"
                    ].loc[random_number, p.patient_type]
                else:
                    p.transplant_type = "cadaver"
                    random_number = truncate_2dp(self.rng.uniform(0, 1))
                    p.time_on_waiting_list = self.config.time_to_event_curves[
                        "tw_cadTx_England"
                    ].loc[random_number, p.patient_type]
                p.pre_emptive_transplant = False
            self.env.process(self.start_dialysis_modality(p))
        elif location == "live_transplant":
            p.transplant_suitable = True
            p.pre_emptive_transplant = None  # Unknown for prevalent patients
            p.time_of_transplant = self.env.now
            p.transplant_type = "live"

            if self.config.trace:
                print(
                    f"Patient {p.id} of age group {p.age_group} is living with live donor transplant at time {self.env.now}."
                )
            self.env.process(self.start_transplant(p))
        elif location == "cadaver_transplant":
            p.transplant_suitable = True
            p.pre_emptive_transplant = None  # Unknown for prevalent patients
            p.time_of_transplant = self.env.now
            p.transplant_type = "cadaver"

            if self.config.trace:
                print(
                    f"Patient {p.id} of age group {p.age_group} is living with cadaver donor transplant at time {self.env.now}."
                )
            self.env.process(self.start_transplant(p))

    def _update_event_log(
        self,
        patient: Patient,
        activity_from: str | None,
        activity_to: str | None,
        time_starting_activity_from: float | None,
        time_spent_in_activity_from: float | None,
    ) -> None:
        """Updates the event log with a change in activity for a specific simulated patient

        Args:
            patient (Patient): Patient entity undergong activity change
            activity_from (str | None): Activity that the patient is currently in
            activity_to (str | None): Activity the patient is moving to
            time_starting_activity_from (float | None): Timestamp of time starting current activity
            time_spent_in_activity_from (float | None): Timestamp of time moving to the next activity
        """
        self.event_log.loc[len(self.event_log)] = [
            patient.id,
            patient.patient_type,
            patient.patient_flag,
            activity_from,
            activity_to,
            time_starting_activity_from,
            time_spent_in_activity_from,
        ]

    def generator_patient_arrivals(self, patient_type: str) -> Generator:
        """Generator function for arriving patients

        Args:
            patient_type (str): Type of patient. Used to retrieve correct inter-arrival time.

        Yields:
            simpy.Environment.Timeout: Simpy Timeout event with a delay of the sampled inter-arrival time
        """
        while True:
            year = calculate_lookup_year(self.env.now)
            mean_iat = self.config.mean_iat_over_time_dfs[patient_type].loc[
                year, "mean_iat"
            ]
            sampled_iat = self.rng.exponential(mean_iat)
            yield self.env.timeout(sampled_iat)
            self.patient_counter += (
                1  # we use the patient_counter for the ID so this must come first
            )
            p = Patient(
                self.patient_counter,
                patient_type,
                self.env.now,
                patient_flag="incident",
            )
            if self.config.trace:
                print(
                    f"Patient {p.id} of age group {p.age_group} entered the system at {self.env.now}."
                )
            self.patients_in_system[patient_type] += 1

            year = calculate_lookup_year(self.env.now)
            if self.rng.uniform(0, 1) > self.config.con_care_dist[year][p.age_group]:
                # If the patient is not diverted to conservative care they start KRT
                self.env.process(self.start_krt(p))
            else:
                self.env.process(self.start_conservative_care(p))

    def start_conservative_care(self, p: Patient) -> Generator:
        """Generator function for patients entering conservative care

        Args:
            p (Patient): Patient entity

        Yields:
            simpy.Environment.Timeout: Simpy Timeout event with a delay of the sampled inter-arrival time
        """
        sampled_con_care_time = self.config.ttd_con_care["scale"] * self.rng.weibull(
            a=self.config.ttd_con_care["shape"], size=None
        )
        self._update_event_log(
            p,
            "conservative_care",
            "death",
            self.env.now,
            sampled_con_care_time,
        )
        self.patients_in_system[p.patient_type] -= 1
        if self.config.trace:
            print(
                f"Patient {p.id} of age group {p.age_group} diverted to conservative care and left the system after {sampled_con_care_time} time units."
            )
        yield self.env.timeout(sampled_con_care_time)

    def start_krt(self, patient: Patient) -> Generator:
        """Function containing the logic for the Kidney Replacement Therapy pathway

        Args:
            patient (Patient): An instance of the Patient object

        Yields:
            simpy.Environment.Timeout: Simpy Timeout event with a delay of the start time for the specific patient in the system
        """
        year = calculate_lookup_year(self.env.now)
        if (
            self.rng.uniform(0, 1)
            > self.config.suitable_for_transplant_dist[patient.age_group]
        ):
            # Patient is not suitable for transplant and so starts dialysis only pathway
            patient.transplant_suitable = False

            if self.config.trace:
                print(
                    f"Patient {patient.id} of age group {patient.age_group} started dialysis only pathway at time {self.env.now}."
                )
            self.env.process(self.start_dialysis_modality_allocation(patient))
            yield self.env.timeout(0)

        else:
            # Patient is suitable for transplant and so we need to decide if they start pre-emptive transplant or dialysis whilst waiting for transplant
            patient.transplant_suitable = True
            # We first assign a transplant type: live or cadaver as this impacts the probability of starting pre-emptive transplant
            if (
                self.rng.uniform(0, 1)
                < self.config.transplant_type_dist[patient.age_group]
            ):
                patient.transplant_type = "live"
            else:
                patient.transplant_type = "cadaver"

            if patient.transplant_type == "live":
                if (
                    self.rng.uniform(0, 1)
                    < self.config.pre_emptive_transplant_live_donor_dist[year][
                        patient.referral_type
                    ]
                ):
                    # Patient starts pre-emptive transplant

                    patient.pre_emptive_transplant = True
                    patient.time_enters_waiting_list = self.env.now
                    if self.config.trace:
                        print(
                            f"Patient {patient.id} of age group {patient.age_group} started pre-emptive transplant pathway with live donor at time {self.env.now}."
                        )
                    self.env.process(self.start_transplant(patient))
                else:
                    # Patient starts dialysis whilst waiting for transplant

                    patient.pre_emptive_transplant = False
                    patient.time_enters_waiting_list = self.env.now
                    if self.config.trace:
                        print(
                            f"Patient {patient.id} of age group {patient.age_group} started dialysis whilst waiting for transplant pathway with live donor at time {self.env.now}."
                        )
                    self.env.process(
                        self.start_dialysis_whilst_waiting_for_transplant(patient)
                    )
            else:  # cadaver
                if (
                    self.rng.uniform(0, 1)
                    < self.config.pre_emptive_transplant_cadaver_donor_dist[year][
                        patient.referral_type
                    ]
                ):
                    # Patient starts pre-emptive transplant

                    patient.pre_emptive_transplant = True
                    patient.time_enters_waiting_list = self.env.now
                    if self.config.trace:
                        print(
                            f"Patient {patient.id} of age group {patient.age_group} started pre-emptive transplant pathway with cadaver donor at time {self.env.now}."
                        )
                    self.env.process(self.start_transplant(patient))

                else:
                    # Patient starts dialysis whilst waiting for transplant
                    patient.pre_emptive_transplant = False
                    patient.time_enters_waiting_list = self.env.now

                    if self.config.trace:
                        print(
                            f"Patient {patient.id} of age group {patient.age_group} started dialysis whilst waiting for transplant pathway with cadaver donor at time {self.env.now}."
                        )
                    self.env.process(
                        self.start_dialysis_whilst_waiting_for_transplant(patient)
                    )

    def start_dialysis_modality_allocation(self, patient: Patient) -> Generator:
        """Function containing the logic for the dialysis pathway


        Args:
            patient (Patient): An instance of the Patient object

        Yields:
            simpy.Environment.process: starts process of ichd, hhd or pd based on modality allocation distributions
        """

        ## which modality do they start on?
        patient.time_starts_dialysis = self.env.now
        year = calculate_lookup_year(self.env.now)
        modality_allocation_distributions = (
            self.config.modality_allocation_distributions[year]
        )
        random_number = self.rng.uniform(0, 1)
        current_modality = patient.dialysis_modality
        if current_modality == "none":
            if (
                random_number
                < modality_allocation_distributions[current_modality]["ichd"]
            ):
                patient.dialysis_modality = "ichd"

            elif (
                random_number
                < modality_allocation_distributions[current_modality]["ichd"]
                + modality_allocation_distributions[current_modality]["hhd"]
            ):
                patient.dialysis_modality = "hhd"
            else:
                patient.dialysis_modality = "pd"
        elif current_modality == "ichd":
            if (
                self.rng.uniform(0, 1)
                < modality_allocation_distributions[current_modality]["hhd"]
            ):
                patient.dialysis_modality = "hhd"
            else:
                patient.dialysis_modality = "pd"
        elif current_modality == "hhd":
            if (
                self.rng.uniform(0, 1)
                < modality_allocation_distributions[current_modality]["ichd"]
            ):
                patient.dialysis_modality = "ichd"
            else:
                patient.dialysis_modality = "pd"
        elif current_modality == "pd":
            if (
                self.rng.uniform(0, 1)
                < modality_allocation_distributions[current_modality]["ichd"]
            ):
                patient.dialysis_modality = "ichd"
            else:
                patient.dialysis_modality = "hhd"

        self.env.process(self.start_dialysis_modality(patient))
        yield self.env.timeout(0)

    def start_transplant(self, patient: Patient) -> Generator:
        """Function containing the logic for the transplant pathway

        Args:
            patient (Patient): An instance of the Patient object

        Yields:
            simpy.Environment.Timeout: Simpy Timeout event with a delay of the start time for the specific patient in the system
        """
        patient.transplant_count += 1

        patient.time_of_transplant = self.env.now
        if patient.transplant_type == "live":
            # how long the graft lasts depends on where they go next: death or back to start_krt
            if (
                self.rng.uniform(0, 1)
                < self.config.death_post_transplant["live"][patient.age_group]
            ):
                # patient dies after transplant

                ## sampled_wait_time depends on whether patient is incident or not
                if patient.patient_flag == "incident":
                    random_number = truncate_2dp(self.rng.uniform(0, 1))
                    sampled_wait_time = self.config.time_to_event_curves[
                        "ttd_liveTx"
                    ].loc[random_number, patient.patient_type]
                else:  # prevalent patient
                    random_number = truncate_2dp(self.rng.uniform(0, 1))
                    sampled_wait_time = self.config.time_to_event_curves[
                        "ttd_liveTx_initialisation"
                    ].loc[random_number, patient.patient_type]
                self._update_event_log(
                    patient,
                    patient.transplant_type,
                    "death",
                    float(self.env.now),
                    sampled_wait_time,
                )

                yield self.env.timeout(sampled_wait_time)
                patient.time_living_with_live_transplant = sampled_wait_time

                self.patients_in_system[patient.patient_type] -= 1

                if self.config.trace:
                    print(
                        f"Patient {patient.id} of age group {patient.age_group} died after live transplant at time {self.env.now}."
                    )
                # patient leaves the system
            else:
                # patient goes back to start_krt after graft fails
                ## sampled_wait_time depends on whether patient is incident or not
                if patient.patient_flag == "incident":
                    random_number = truncate_2dp(self.rng.uniform(0, 1))
                    sampled_wait_time = self.config.time_to_event_curves[
                        "ttgf_liveTx"
                    ].loc[random_number, patient.patient_type]
                else:  # prevalent patient
                    random_number = truncate_2dp(self.rng.uniform(0, 1))
                    sampled_wait_time = self.config.time_to_event_curves[
                        "ttgf_liveTx_initialisation"
                    ].loc[random_number, patient.patient_type]

                self._update_event_log(
                    patient,
                    patient.transplant_type,
                    "graft_failure",
                    float(self.env.now),
                    sampled_wait_time,
                )
                patient.patient_flag = "incident"  # if they were prevalent then after the patient has a graft failure we treat them as incident again
                yield self.env.timeout(sampled_wait_time)
                patient.time_living_with_live_transplant = sampled_wait_time
                if self.config.trace:
                    print(
                        f"Patient {patient.id} of age group {patient.age_group} had graft failure after live transplant at time {self.env.now}."
                    )
                ## they're returning to start_krt so we want to reset a bunch of starting variables
                patient.transplant_suitable = None
                patient.transplant_type = None
                patient.pre_emptive_transplant = None
                patient.dialysis_modality = "none"
                patient.time_starts_dialysis = None
                patient.time_on_dialysis = {"ichd": 0.0, "hhd": 0.0, "pd": 0.0}
                patient.time_living_with_live_transplant = None
                patient.time_living_with_cadaver_transplant = None
                patient.time_on_waiting_list = 0
                patient.time_enters_waiting_list = None
                patient.time_of_transplant = None

                self.env.process(self.start_krt(patient))
        else:  # cadaver
            # how long the graft lasts depends on where they go next: death or back to start_krt
            if (
                self.rng.uniform(0, 1)
                < self.config.death_post_transplant["cadaver"][patient.age_group]
            ):
                # patient dies after transplant

                ## sampled_wait_time depends on whether patient is incident or not
                if patient.patient_flag == "incident":
                    random_number = truncate_2dp(self.rng.uniform(0, 1))
                    sampled_wait_time = self.config.time_to_event_curves[
                        "ttgf_cadTx"
                    ].loc[random_number, patient.patient_type]
                else:  # prevalent patient
                    random_number = truncate_2dp(self.rng.uniform(0, 1))
                    sampled_wait_time = self.config.time_to_event_curves[
                        "ttgf_liveTx_initialisation"
                    ].loc[random_number, patient.patient_type]
                self._update_event_log(
                    patient,
                    patient.transplant_type,
                    "death",
                    float(self.env.now),
                    sampled_wait_time,
                )

                yield self.env.timeout(sampled_wait_time)
                patient.time_living_with_cadaver_transplant = sampled_wait_time

                self.patients_in_system[patient.patient_type] -= 1

                if self.config.trace:
                    print(
                        f"Patient {patient.id} of age group {patient.age_group} died after cadaver transplant at time {self.env.now}."
                    )
                # patient leaves the system
            else:
                # patient goes back to start_krt after graft fails

                ## sampled_wait_time depends on whether patitent is inicident or not
                if patient.patient_flag == "incident":
                    random_number = truncate_2dp(self.rng.uniform(0, 1))
                    sampled_wait_time = self.config.time_to_event_curves[
                        "ttgf_cadTx"
                    ].loc[random_number, patient.patient_type]
                else:  # prevalent patient
                    random_number = truncate_2dp(self.rng.uniform(0, 1))
                    sampled_wait_time = self.config.time_to_event_curves[
                        "ttgf_cadTx_initialisation"
                    ].loc[random_number, patient.patient_type]

                self._update_event_log(
                    patient,
                    patient.transplant_type,
                    "graft_failure_modality_allocation",
                    float(self.env.now),
                    sampled_wait_time,
                )
                patient.patient_flag = "incident"  # if they were prevalent then after the patient has a graft failure we treat them as incident again
                yield self.env.timeout(sampled_wait_time)
                patient.time_living_with_cadaver_transplant = sampled_wait_time
                if self.config.trace:
                    print(
                        f"Patient {patient.id} of age group {patient.age_group} had graft failure after cadaver transplant at time {self.env.now}."
                    )
                ## they're returning to start_krt so we want to reset a bunch of starting variables
                patient.transplant_suitable = None
                patient.transplant_type = None
                patient.pre_emptive_transplant = None
                patient.dialysis_modality = "none"
                patient.time_starts_dialysis = None
                patient.time_on_dialysis = {"ichd": 0.0, "hhd": 0.0, "pd": 0.0}
                patient.time_living_with_live_transplant = None
                patient.time_living_with_cadaver_transplant = None
                patient.time_on_waiting_list = 0
                patient.time_enters_waiting_list = None
                patient.time_of_transplant = None

                self.env.process(self.start_krt(patient))

    def start_dialysis_whilst_waiting_for_transplant(
        self, patient: Patient
    ) -> Generator:
        """Function containing the logic for the mixed pathway where a patient starts on dialysis and then receives a transplant

        Args:
            patient (Patient): An instance of the Patient object

        Yields:
            simpy.Environment.Timeout: Simpy Timeout event with a delay of the start time for the specific patient in the system
        """

        # If they're coming down this pathway then they're listed i.e. pre-emptive = FALSE

        # Let's generate a time on the waiting list
        # We'll use this within the starts_dialysis function to work out how long they stay in dialysis before Tx
        if patient.transplant_type == "live":
            random_number = truncate_2dp(self.rng.uniform(0, 1))
            patient.time_on_waiting_list = self.config.time_to_event_curves[
                "tw_liveTx_England"
            ].loc[random_number, patient.patient_type]
        else:  # cadaver
            random_number = truncate_2dp(self.rng.uniform(0, 1))
            patient.time_on_waiting_list = self.config.time_to_event_curves[
                "tw_cadTx_England"
            ].loc[random_number, patient.patient_type]
        ## if this isn't their first Tx then we also need to simulate the time they wait before starting dialysis
        if patient.transplant_count > 0:
            # we need to check this isn't longer than their time on the waiting list
            # if it is longer than their time on the waiting list they start transplant pre-emptively
            sampled_wait_time = self.config.tw_before_dialysis[
                "scale"
            ] * self.rng.weibull(a=self.config.tw_before_dialysis["shape"], size=None)
            if sampled_wait_time > patient.time_on_waiting_list:
                # they go to transplant pre-emptively without starting dialysis
                self._update_event_log(
                    patient,
                    "waiting_for_transplant",
                    patient.transplant_type,
                    float(self.env.now),
                    patient.time_on_waiting_list,
                )
                yield self.env.timeout(patient.time_on_waiting_list)
                if self.config.trace:
                    print(
                        f"Patient {patient.id} of age group {patient.age_group} has pre-emptive {patient.transplant_type} transplant at time {self.env.now}."
                    )
                patient.pre_emptive_transplant = True
                self.env.process(self.start_transplant(patient))
            else:
                self._update_event_log(
                    patient,
                    "waiting_for_transplant",
                    "dialysis_modality_allocation",
                    float(self.env.now),
                    sampled_wait_time,
                )
                yield self.env.timeout(sampled_wait_time)
                patient.time_on_waiting_list -= sampled_wait_time  ## remove time waiting from total time on waiting list
                if self.config.trace:
                    print(
                        f"Patient {patient.id} of age group {patient.age_group} started dialysis whilst waiting for transplant at time {self.env.now}."
                    )
                self.env.process(self.start_dialysis_modality_allocation(patient))
        else:
            # if this is the first time in the model then there should be no wait before starting dialysis as they
            # are assumed to enter the model at the point of starting dialysis
            if self.config.trace:
                print(
                    f"Patient {patient.id} of age group {patient.age_group} started dialysis whilst waiting for transplant at time {self.env.now}."
                )
            yield self.env.timeout(0)
            self.env.process(self.start_dialysis_modality_allocation(patient))

    def start_dialysis_modality(self, patient: Patient) -> Generator:
        """Function containing the logic for all dialysis pathways

        Args:
            patient (Patient): An instance of the Patient object

        Yields:
            simpy.Environment.Timeout: Simpy Timeout event with a delay of the start time for the specific patient in the system
        """

        if self.config.trace:
            print(
                f"Patient {patient.id} of age group {patient.age_group} starts {patient.dialysis_modality} at time {self.env.now}."
            )

        # what is the next step modality change, death
        # if they're waiting for transplant we'll compare the time generated to patient.time on waiting list
        if (
            self.rng.uniform(0, 1)
            < self.config.death_post_dialysis_modality[patient.dialysis_modality][
                patient.referral_type
            ][patient.age_group]
        ):
            # death or transplant
            ## sampled_time depends on whether patitent is inicident or not
            if patient.patient_flag == "incident":
                random_number = truncate_2dp(self.rng.uniform(0, 1))
                sampled_time = self.config.time_to_event_curves[
                    f"ttd_{patient.dialysis_modality}"
                ].loc[random_number, patient.patient_type]
            else:  ## prevalent patient
                random_number = truncate_2dp(self.rng.uniform(0, 1))
                sampled_time = self.config.time_to_event_curves[
                    f"ttd_{patient.dialysis_modality}_initialisation"
                ].loc[random_number, patient.patient_type]
            if (
                patient.transplant_suitable
                and sampled_time >= patient.time_on_waiting_list
            ):
                self._update_event_log(
                    patient,
                    patient.dialysis_modality,
                    patient.transplant_type,
                    float(self.env.now),
                    patient.time_on_waiting_list,
                )
                patient.patient_flag = "incident"  # after prevalent patient ends their dialysis episode we treat them as incident again if they're going to transplant (no need to do this if next step is death)
                patient.pre_emptive_transplant = False
                yield self.env.timeout(patient.time_on_waiting_list)
                patient.time_on_dialysis[patient.dialysis_modality] = (
                    patient.time_on_waiting_list
                )
                if self.config.trace:
                    print(
                        f"Patient {patient.id} of age group {patient.age_group} has {patient.transplant_type} transplant at time {self.env.now}."
                    )
                yield self.env.timeout(0)
                self.env.process(self.start_transplant(patient))
            else:
                # death
                self._update_event_log(
                    patient,
                    patient.dialysis_modality,
                    "death",
                    float(self.env.now),
                    sampled_time,
                )
                yield self.env.timeout(sampled_time)
                patient.time_on_dialysis[patient.dialysis_modality] = sampled_time
                self.patients_in_system[patient.patient_type] -= 1
                if self.config.trace:
                    print(
                        f"Patient {patient.id} of age group {patient.age_group} died and left the system at time {self.env.now}."
                    )
                    print(self.patients_in_system)
        else:
            # modality change or transplant

            ## sampled_time depends on whether patient is incident or not
            if patient.patient_flag == "incident":
                random_number = truncate_2dp(self.rng.uniform(0, 1))
                sampled_time = self.config.time_to_event_curves[
                    f"ttma_{patient.dialysis_modality}"
                ].loc[random_number, patient.patient_type]
            else:  ## prevalent patient
                random_number = truncate_2dp(self.rng.uniform(0, 1))
                sampled_time = self.config.time_to_event_curves[
                    f"ttma_{patient.dialysis_modality}_initialisation"
                ].loc[random_number, patient.patient_type]
            if (
                patient.transplant_suitable
                and sampled_time >= patient.time_on_waiting_list
            ):
                self._update_event_log(
                    patient,
                    patient.dialysis_modality,
                    patient.transplant_type,
                    float(self.env.now),
                    patient.time_on_waiting_list,
                )
                patient.patient_flag = "incident"  # after prevalent patient ends their dialysis episode we treat them as incident again
                patient.pre_emptive_transplant = False
                yield self.env.timeout(patient.time_on_waiting_list)
                patient.time_on_dialysis[patient.dialysis_modality] = (
                    patient.time_on_waiting_list
                )
                if self.config.trace:
                    print(
                        f"Patient {patient.id} of age group {patient.age_group} has {patient.transplant_type} transplant at time {self.env.now}."
                    )
                self.env.process(self.start_transplant(patient))
            else:
                # modality change
                self._update_event_log(
                    patient,
                    patient.dialysis_modality,
                    "modality_allocation",
                    float(self.env.now),
                    sampled_time,
                )
                patient.patient_flag = "incident"  # after prevalent patient ends their dialysis episode we treat them as incident again
                yield self.env.timeout(sampled_time)
                patient.time_on_waiting_list -= sampled_time
                patient.time_on_dialysis[patient.dialysis_modality] = sampled_time
                if self.config.trace:
                    print(
                        f"Patient {patient.id} of age group {patient.age_group} changed dialysis modality at time {self.env.now}."
                    )

                self.env.process(self.start_dialysis_modality_allocation(patient))

    def time_tracker(self) -> Generator:
        """Function for logging time passing in the simulation, for user information

        Yields:
            simpy.Environment.Timeout: Simpy Timeout event with a delay of each year of simulation
        """
        years = calculate_lookup_year(self.config.sim_duration)
        for i in range(1, years + 1):
            yield (self.env.timeout(365))
            logger.info(f"{i} year(s) of simulation complete")

    def save_result_files(self, data_to_save):
        logger.info(f"💾 Saving {data_to_save}")
        folder_path = "results"
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        today_date = datetime.now().strftime("%Y%m%d-%H%M")
        filename = f"results/{today_date}_{data_to_save}_{self.run_number}"
        df_to_save = getattr(self, data_to_save).copy()
        df_to_save.to_parquet(filename + ".parquet")
        df_to_save.to_csv(filename + ".csv")

    def run(self):
        """Runs the model"""
        if self.config.initialise_prevalent_patients:
            logger.info("Initialising prevalent patients...")
            # We first initialize the model with patients that were in the system at time zero - we look at each location in turn (conservative care, ichd, hhd, pd, live transplant, cadaver transplant)
            for patient_type in self.patient_types:
                for _ in range(
                    self.config.prevalent_counts["conservative_care"][patient_type]
                ):
                    self.env.process(
                        self.generator_prevalent_patient_arrivals(
                            patient_type, "conservative_care"
                        )
                    )
                for _ in range(self.config.prevalent_counts["ichd"][patient_type]):
                    self.env.process(
                        self.generator_prevalent_patient_arrivals(patient_type, "ichd")
                    )
                for _ in range(self.config.prevalent_counts["hhd"][patient_type]):
                    self.env.process(
                        self.generator_prevalent_patient_arrivals(patient_type, "hhd")
                    )
                for _ in range(self.config.prevalent_counts["pd"][patient_type]):
                    self.env.process(
                        self.generator_prevalent_patient_arrivals(patient_type, "pd")
                    )
                for _ in range(
                    self.config.prevalent_counts["live_transplant"][patient_type]
                ):
                    self.env.process(
                        self.generator_prevalent_patient_arrivals(
                            patient_type, "live_transplant"
                        )
                    )
                for _ in range(
                    self.config.prevalent_counts["cadaver_transplant"][patient_type]
                ):
                    self.env.process(
                        self.generator_prevalent_patient_arrivals(
                            patient_type, "cadaver_transplant"
                        )
                    )
        logger.info("🏃‍➡️ Beginning simulation with incident patients")
        # We set up a generator for each of the patient types we have an IAT for
        self.env.process(self.time_tracker())
        for patient_type in self.patient_types:
            self.env.process(self.generator_patient_arrivals(patient_type))
        self.env.run(until=self.config.sim_duration)
        logger.info("✅ Model run complete!")
        self.event_log = process_event_log(self.event_log)
        results_df, activity_change = calculate_model_results(self.event_log)
        self.results_df = results_df
        self.activity_change = activity_change
        self.save_result_files("event_log")
        self.save_result_files("results_df")
        # Show results (optional - set in config)
        if self.config.trace:
            print(f"Run Number {self.run_number}")
            print(self.patients_in_system)


if __name__ == "__main__":
    config = Config()
    config.trace = False
    config.initialise_prevalent_patients = False
    rng = np.random.default_rng(config.random_seed)
    model = Model(1, rng, config, "20250101_1200")
    model.run()
