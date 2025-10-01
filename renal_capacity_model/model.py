"""
Module containing the Model class. Contains most of the logic for the simulation.
"""

import simpy
from renal_capacity_model.entity import Patient
import numpy as np
from renal_capacity_model.config import Config
from renal_capacity_model.helpers import get_interarrival_times
import pandas as pd


class Model:
    """
    Model class containing the logic for the simulation
    """

    def __init__(self, run_number, rng, config):
        """Initialise the model

        Args:
            run_number (int): Which run number in the Trial this Model is for
            rng (np.random.Generator): Random Number Generator used for the whole experiment
            config (Config): Config Class containing values to be used for model run
        """
        self.env = simpy.Environment()
        self.config = config
        self.patient_counter = 0
        self.run_number = run_number
        self.rng = rng
        self.inter_arrival_times = get_interarrival_times(self.config)
        self.patients_in_system = {k: 0 for k in self.inter_arrival_times.keys()}
        self.results_df = self._setup_results_df()
        self.snapshot_results_df = self._setup_snapshot_df()
        self.snapshot_interval = (
            self.config.snapshot_interval
        )  # how often to take a snapshot of the results_df

    def _setup_results_df(self):
        """Sets up DataFrame for recording model results

        Returns:
            pd.DataFrame: Empty DataFrame for recording model results
        """
        results_df = pd.DataFrame(
            columns=pd.Index(
                [
                    "age_group",
                    "referral_type",
                    "entry_time",
                    "diverted_to_con_care",
                    "suitable_for_transplant",
                    "live_transplant_count",
                    "cadaver_transplant_count",
                    "pre_emptive_transplant",
                    "transplant_count",
                    "ichd_dialysis_count",
                    "hhd_dialysis_count",
                    "pd_dialysis_count",
                    "time_of_death",
                    "death_from_con_care",
                    "death_from_ichd",
                    "death_from_hhd",
                    "death_from_pd",
                    "death_post_live_transplant",
                    "death_post_cadaver_transplant",
                ]
            )
        )
        results_df["patient ID"] = [1]
        results_df.set_index("patient ID", inplace=True)

        return results_df

    def _setup_snapshot_df(self):
        """Sets up DataFrame for recording snapshot model results

        Returns:
            pd.DataFrame: Empty DataFrame for recording model results
        """
        snapshot_results_df = pd.DataFrame(
            columns=pd.Index(
                [
                    "snapshot_time",
                    "age_group",
                    "referral_type",
                    "entry_time",
                    "diverted_to_con_care",
                    "suitable_for_transplant",
                    "live_transplant_count",
                    "cadaver_transplant_count",
                    "pre_emptive_transplant",
                    "transplant_count",
                    "ichd_dialysis_count",
                    "hhd_dialysis_count",
                    "pd_dialysis_count",
                    "time_of_death",
                    "death_from_con_care",
                    "death_from_ichd",
                    "death_from_hhd",
                    "death_from_pd",
                    "death_post_live_transplant",
                    "death_post_cadaver_transplant",
                ]
            )
        )
        snapshot_results_df["patient ID"] = [1]
        snapshot_results_df.set_index("patient ID", inplace=True)

        return snapshot_results_df

    def generator_patient_arrivals(self, patient_type):
        """Generator function for arriving patients

        Args:
            patient_type (str): Type of patient. Used to retrieve correct inter-arrival time.

        Yields:
            simpy.Environment.Timeout: Simpy Timeout event with a delay of the sampled inter-arrival time
        """
        while True:
            self.patient_counter += 1

            p = Patient(self.patient_counter, patient_type)

            if self.patient_counter <= 12:
                start_time_in_system_patient = self.rng.exponential(
                    1 / self.inter_arrival_times[patient_type]
                )
                yield self.env.timeout(start_time_in_system_patient)
            else:
                start_time_in_system_patient = self.env.now

            self.patients_in_system[patient_type] += 1

            self.results_df.loc[p.id, "entry_time"] = start_time_in_system_patient
            self.results_df.loc[p.id, "age_group"] = int(p.age_group)
            self.results_df.loc[p.id, "referral_type"] = p.referral_type
            self.results_df.loc[p.id, "transplant_count"] = 0
            self.results_df.loc[p.id, "live_transplant_count"] = 0
            self.results_df.loc[p.id, "cadaver_transplant_count"] = 0
            self.results_df.loc[p.id, "ichd_dialysis_count"] = 0
            self.results_df.loc[p.id, "hhd_dialysis_count"] = 0
            self.results_df.loc[p.id, "pd_dialysis_count"] = 0

            if self.rng.uniform(0, 1) > self.config.con_care_dist[p.age_group]:
                # If the patient is not diverted to conservative care they start KRT
                self.env.process(self.start_krt(p))
            else:
                # these patients are diverted to conservative care. We don't need a process here as all these patients do is wait a while before leaving the system
                self.results_df.loc[p.id, "diverted_to_con_care"] = True
                sampled_con_care_time = (
                    self.config.ttd_con_care_scale
                    * self.rng.weibull(a=self.config.ttd_con_care_shape, size=1)
                )
                yield self.env.timeout(sampled_con_care_time)
                self.results_df.loc[p.id, "time_of_death"] = self.env.now
                self.patients_in_system[patient_type] -= 1
                self.results_df.loc[p.id, "diverted_to_con_care"] = (
                    False  # as they've left conservative care
                )
                self.results_df.loc[p.id, "death_from_con_care"] = True
                if self.config.trace:
                    print(
                        f"Patient {p.id} of age group {p.age_group} diverted to conservative care and left the system after {sampled_con_care_time} time units."
                    )
                    print(self.patients_in_system)

            sampled_inter_arrival_time = self.rng.exponential(
                1 / self.inter_arrival_times[patient_type]
            )

            yield self.env.timeout(sampled_inter_arrival_time)

    def start_krt(self, patient):
        """Function containing the logic for the Kidney Replacement Therapy pathway

        Args:
            patient (Patient): An instance of the Patient object

        Yields:
            simpy.Environment.Timeout: Simpy Timeout event with a delay of the start time for the specific patient in the system
        """

        if (
            self.rng.uniform(0, 1)
            > self.config.suitable_for_transplant_dist[patient.age_group]
        ):
            # Patient is not suitable for transplant and so starts dialysis only pathway
            patient.suitable_for_transplant = False
            self.results_df.loc[patient.id, "suitable_for_transplant"] = (
                patient.suitable_for_transplant
            )

            yield self.env.process(self.start_dialysis(patient))
            if self.config.trace:
                print(
                    f"Patient {patient.id} of age group {patient.age_group} started dialysis only pathway."
                )
        else:
            # Patient is suitable for transplant and so we need to decide if they start pre-emptive transplant or dialysis whilst waiting for transplant
            patient.suitable_for_transplant = True
            # We first assign a transplant type: live or cadaver as this impacts the probability of starting pre-emptive transplant
            if (
                self.rng.uniform(0, 1)
                < self.config.transplant_type_dist[patient.age_group]
            ):
                patient.transplant_type = "live"
            else:
                patient.transplant_type = "cadaver"

            self.results_df.loc[patient.id, "suitable_for_transplant"] = (
                patient.suitable_for_transplant
            )

            if patient.transplant_type == "live":
                if (
                    self.rng.uniform(0, 1)
                    < self.config.pre_emptive_transplant_live_donor_dist[
                        patient.referral_type
                    ]
                ):
                    # Patient starts pre-emptive transplant
                    self.results_df.loc[patient.id, "pre_emptive_transplant"] = True

                    yield self.env.process(self.start_transplant(patient))
                    if self.config.trace:
                        print(
                            f"Patient {patient.id} of age group {patient.age_group} started pre-emptive transplant pathway with live donor."
                        )
                else:
                    # Patient starts dialysis whilst waiting for transplant
                    self.results_df.loc[patient.id, "pre_emptive_transplant"] = False
                    patient.time_enters_waiting_list = self.env.now
                    if self.config.trace:
                        print(
                            f"Patient {patient.id} of age group {patient.age_group} started dialysis whilst waiting for transplant pathway with live donor."
                        )
                    yield self.env.process(
                        self.start_dialysis_whilst_waiting_for_transplant(patient)
                    )
            else:  # cadaver
                if (
                    self.rng.uniform(0, 1)
                    < self.config.pre_emptive_transplant_cadaver_donor_dist[
                        patient.referral_type
                    ]
                ):
                    # Patient starts pre-emptive transplant
                    self.results_df.loc[patient.id, "pre_emptive_transplant"] = True

                    yield self.env.process(self.start_transplant(patient))
                    if self.config.trace:
                        print(
                            f"Patient {patient.id} of age group {patient.age_group} started pre-emptive transplant pathway with cadaver donor."
                        )
                else:
                    # Patient starts dialysis whilst waiting for transplant
                    self.results_df.loc[patient.id, "pre_emptive_transplant"] = False

                    yield self.env.process(
                        self.start_dialysis_whilst_waiting_for_transplant(patient)
                    )
                    if self.config.trace:
                        print(
                            f"Patient {patient.id} of age group {patient.age_group} started dialysis whilst waiting for transplant pathway with cadaver donor."
                        )

    def start_dialysis(self, patient):
        """Function containing the logic for the dialysis pathway


        Args:
            patient (Patient): An instance of the Patient object

        Yields:
            simpy.Environment.process: starts process of ichd, hhd or pd based on modality allocation distributions
        """

        ## which modality do they start on?
        patient.time_starts_dialysis = self.env.now
        if patient.last_dialysis_modality == "none":
            random_number = self.rng.uniform(0, 1)
            if random_number < self.config.modality_allocation_none_dist["ichd"]:
                patient.dialysis_modality = "ichd"
                self.results_df.loc[patient.id, "ichd_dialysis_count"] += 1
                yield self.env.process(self.start_ichd(patient))
            elif (
                random_number
                < self.config.modality_allocation_none_dist["ichd"]
                + self.config.modality_allocation_none_dist["hhd"]
            ):
                patient.dialysis_modality = "hhd"
                self.results_df.loc[patient.id, "hhd_dialysis_count"] += 1
                yield self.env.process(self.start_hhd(patient))
            else:
                patient.dialysis_modality = "pd"
                self.results_df.loc[patient.id, "pd_dialysis_count"] += 1
                yield self.env.process(self.start_pd(patient))
        elif patient.last_dialysis_modality == "ichd":
            if (
                self.rng.uniform(0, 1)
                < self.config.modality_allocation_ichd_dist["hhd"]
            ):
                patient.dialysis_modality = "hhd"
                self.results_df.loc[patient.id, "hhd_dialysis_count"] += 1
                yield self.env.process(self.start_hhd(patient))
            else:
                patient.dialysis_modality = "pd"
                self.results_df.loc[patient.id, "pd_dialysis_count"] += 1
                yield self.env.process(self.start_pd(patient))
        elif patient.last_dialysis_modality == "hhd":
            if (
                self.rng.uniform(0, 1)
                < self.config.modality_allocation_hhd_dist["ichd"]
            ):
                patient.dialysis_modality = "ichd"
                self.results_df.loc[patient.id, "ichd_dialysis_count"] += 1
                yield self.env.process(self.start_ichd(patient))
            else:
                patient.dialysis_modality = "pd"
                self.results_df.loc[patient.id, "pd_dialysis_count"] += 1
                yield self.env.process(self.start_pd(patient))
        else:  # pd
            if self.rng.uniform(0, 1) < self.config.modality_allocation_pd_dist["ichd"]:
                patient.dialysis_modality = "ichd"
                self.results_df.loc[patient.id, "ichd_dialysis_count"] += 1
                yield self.env.process(self.start_ichd(patient))
            else:
                patient.dialysis_modality = "hhd"
                self.results_df.loc[patient.id, "hhd_dialysis_count"] += 1
                yield self.env.process(self.start_hhd(patient))

    def start_transplant(self, patient):
        """Function containing the logic for the transplant pathway

        Args:
            patient (Patient): An instance of the Patient object

        Yields:
            simpy.Environment.Timeout: Simpy Timeout event with a delay of the start time for the specific patient in the system
        """
        patient.transplant_count += 1
        self.results_df.loc[patient.id, "transplant_count"] += 1
        patient.time_of_transplant = self.env.now
        if patient.transplant_type == "live":
            self.results_df.loc[patient.id, "live_transplant_count"] += 1
            # how long the graft lasts depends on where they go next: death or back to start_krt
            if self.rng.uniform(0, 1) < self.config.death_post_transplant["live"]:
                # patient dies after transplant
                sampled_wait_time = self.config.live_tx_ttd_scale[
                    patient.age_group
                ] * self.rng.weibull(
                    a=self.config.live_tx_ttd_shape[patient.age_group], size=1
                )
                yield self.env.timeout(sampled_wait_time)
                patient.time_living_with_live_transplant = sampled_wait_time
                self.results_df.loc[patient.id, "live_transplant_count"] -= 1
                self.patients_in_system[patient.patient_type] -= 1
                self.results_df.loc[patient.id, "time_of_death"] = self.env.now
                self.results_df.loc[patient.id, "death_post_live_transplant"] = True
                if self.config.trace:
                    print(
                        f"Patient {patient.id} of age group {patient.age_group} died after live transplant at time {self.env.now}."
                    )
                # patient leaves the system
            else:
                # patient goes back to start_krt after graft fails
                sampled_wait_time = self.config.live_tx_ttgf_scale[
                    patient.age_group
                ] * self.rng.weibull(
                    a=self.config.live_tx_ttgf_shape[patient.age_group], size=1
                )
                yield self.env.timeout(sampled_wait_time)
                patient.time_living_with_live_transplant = sampled_wait_time
                self.results_df.loc[patient.id, "live_transplant_count"] -= 1
                if self.config.trace:
                    print(
                        f"Patient {patient.id} of age group {patient.age_group} had graft failure after live transplant at time {self.env.now}."
                    )
                yield self.env.process(self.start_krt(patient))
        else:  # cadaver
            self.results_df.loc[patient.id, "cadaver_transplant_count"] += 1
            # how long the graft lasts depends on where they go next: death or back to start_krt
            if self.rng.uniform(0, 1) < self.config.death_post_transplant["cadaver"]:
                # patient dies after transplant
                sampled_wait_time = self.config.cadaver_tx_ttd_scale[
                    patient.age_group
                ] * self.rng.weibull(
                    a=self.config.cadaver_tx_ttd_shape[patient.age_group], size=1
                )
                yield self.env.timeout(sampled_wait_time)
                patient.time_living_with_cadaver_transplant = sampled_wait_time
                self.results_df.loc[patient.id, "cadaver_transplant_count"] -= 1
                self.patients_in_system[patient.patient_type] -= 1
                self.results_df.loc[patient.id, "time_of_death"] = self.env.now
                self.results_df.loc[patient.id, "death_post_cadaver_transplant"] = True
                if self.config.trace:
                    print(
                        f"Patient {patient.id} of age group {patient.age_group} died after cadaver transplant at time {self.env.now}."
                    )
                # patient leaves the system
            else:
                # patient goes back to start_krt after graft fails
                sampled_wait_time = self.config.cadaver_tx_ttgf_scale[
                    patient.age_group
                ] * self.rng.weibull(
                    a=self.config.cadaver_tx_ttgf_shape[patient.age_group], size=1
                )
                yield self.env.timeout(sampled_wait_time)
                patient.time_living_with_cadaver_transplant = sampled_wait_time
                self.results_df.loc[patient.id, "cadaver_transplant_count"] -= 1
                if self.config.trace:
                    print(
                        f"Patient {patient.id} of age group {patient.age_group} had graft failure after cadaver transplant at time {self.env.now}."
                    )
                yield self.env.process(self.start_krt(patient))

    def start_dialysis_whilst_waiting_for_transplant(self, patient):
        """Function containing the logic for the mixed pathway where a patient starts on dialysis and then receives a transplant

        Args:
            patient (Patient): An instance of the Patient object

        Yields:
            simpy.Environment.Timeout: Simpy Timeout event with a delay of the start time for the specific patient in the system
        """

        # If they're coming down this pathway then they're listed i.e. pre-emptive = FALSE
        # We know if they're having a live Tx they wait on average 3 months on the list before Tx
        # We know if they're having a cadaver Tx they wait on average 2 years on the list before Tx
        # Let's generate a time on the waiting list based on an exponential distribution with these means
        # We'll use this within the starts_dialysis function to work out how long they stay in dialysis before Tx
        if patient.transplant_type == "live":
            patient.time_on_waiting_list = self.rng.exponential(
                scale=self.config.time_on_waiting_list_mean["live"]
            )
        else:  # cadaver
            patient.time_on_waiting_list = self.rng.exponential(
                scale=self.config.time_on_waiting_list_mean["cadaver"]
            )

        ## if this isn't their first Tx then we need to simulate the time they wait before starting dialysis
        if self.results_df.loc[patient.id, "transplant_count"] > 0:
            # we need to check this isn't longer than their time on the waiting list
            # if it is longer than their time on the waiting list they start transplant pre-emptively
            sampled_wait_time = self.config.tw_before_dialysis_scale * self.rng.weibull(
                a=self.config.tw_before_dialysis_shape, size=1
            )
            if sampled_wait_time > patient.time_on_waiting_list:
                # they go to transplant pre-emptively without starting dialysis
                yield self.env.timeout(patient.time_on_waiting_list)
                if self.config.trace:
                    print(
                        f"Patient {patient.id} of age group {patient.age_group} has pre-emptive {patient.transplant_type} transplant at time {self.env.now}."
                    )
                patient.pre_emptive_transplant = True
                self.results_df.loc[patient.id, "pre_emptive_transplant"] = True
                yield self.env.process(self.start_transplant(patient))
            else:
                yield self.env.timeout(sampled_wait_time)
                patient.time_on_waiting_list -= sampled_wait_time  ## remove time waiting from total time on waiting list
                if self.config.trace:
                    print(
                        f"Patient {patient.id} of age group {patient.age_group} started dialysis whilst waiting for transplant at time {self.env.now}."
                    )
                yield self.env.process(self.start_dialysis(patient))
        else:
            # if this is the first time in the model then there should be no wait before starting dialysis as they
            # are assumed to enter the model at the point of starting dialysis
            if self.config.trace:
                print(
                    f"Patient {patient.id} of age group {patient.age_group} started dialysis whilst waiting for transplant at time {self.env.now}."
                )
            yield self.env.process(self.start_dialysis(patient))

    def start_ichd(self, patient):
        """Function containing the logic for the ichd pathway

        Args:
            patient (Patient): An instance of the Patient object

        Yields:
            simpy.Environment.Timeout: Simpy Timeout event with a delay of the start time for the specific patient in the system
        """

        if self.config.trace:
            print(
                f"Patient {patient.id} of age group {patient.age_group} starts ichd at time {self.env.now}."
            )

        # what is the next step modality change, death
        # if they're waiting for transplant we'll compare the time generated to patient.time on waiting list
        if self.rng.uniform(0, 1) < self.config.death_post_ichd[patient.age_group]:
            # death or transplant
            sampled_ichd_time = self.config.ttd_ichd_scale[
                patient.age_group
            ] * self.rng.weibull(self.config.ttd_ichd_shape[patient.age_group])
            if patient.suitable_for_transplant:
                if sampled_ichd_time >= patient.time_on_waiting_list:
                    yield self.env.timeout(patient.time_on_waiting_list)
                    patient.time_on_ichd_dialysis = patient.time_on_waiting_list
                    if self.config.trace:
                        print(
                            f"Patient {patient.id} of age group {patient.age_group} has {patient.transplant_type} transplant at time {self.env.now}."
                        )
                    self.results_df.loc[patient.id, "ichd_dialysis_count"] -= 1
                    yield self.env.process(self.start_transplant(patient))
                else:
                    # death
                    yield self.env.timeout(sampled_ichd_time)
                    patient.time_on_ichd_dialysis = sampled_ichd_time
                    self.patients_in_system[patient.patient_type] -= 1
                    self.results_df.loc[patient.id, "ichd_dialysis_count"] -= 1
                    self.results_df.loc[patient.id, "time_of_death"] = self.env.now
                    self.results_df.loc[patient.id, "death_from_ichd"] = True
                    if self.config.trace:
                        print(
                            f"Patient {patient.id} of age group {patient.age_group} died and left the system at time {self.env.now}."
                        )
                        print(self.patients_in_system)
            else:
                # death
                yield self.env.timeout(sampled_ichd_time)
                patient.time_on_ichd_dialysis = sampled_ichd_time
                self.patients_in_system[patient.patient_type] -= 1
                self.results_df.loc[patient.id, "ichd_dialysis_count"] -= 1
                self.results_df.loc[patient.id, "death_from_ichd"] = True
                self.results_df.loc[patient.id, "time_of_death"] = self.env.now
                if self.config.trace:
                    print(
                        f"Patient {patient.id} of age group {patient.age_group} died and left the system at time {self.env.now}."
                    )
                    print(self.patients_in_system)
        else:
            # modality change or transplant
            sampled_ichd_time = self.config.ttma_ichd_scale[
                patient.age_group
            ] * self.rng.weibull(self.config.ttma_ichd_shape[patient.age_group])
            if patient.suitable_for_transplant:
                if sampled_ichd_time >= patient.time_on_waiting_list:
                    yield self.env.timeout(patient.time_on_waiting_list)
                    patient.time_on_ichd_dialysis = patient.time_on_waiting_list
                    if self.config.trace:
                        print(
                            f"Patient {patient.id} of age group {patient.age_group} has {patient.transplant_type} transplant at time {self.env.now}."
                        )
                    self.results_df.loc[patient.id, "ichd_dialysis_count"] -= 1
                    yield self.env.process(self.start_transplant(patient))
                else:
                    # modality change
                    yield self.env.timeout(sampled_ichd_time)
                    patient.time_on_ichd_dialysis = sampled_ichd_time
                    if self.config.trace:
                        print(
                            f"Patient {patient.id} of age group {patient.age_group} changed dialysis modality at time {self.env.now}s."
                        )
                    self.results_df.loc[patient.id, "ichd_dialysis_count"] -= 1
                    yield self.env.process(self.start_dialysis(patient))
            else:
                # modality change
                yield self.env.timeout(sampled_ichd_time)
                patient.time_on_ichd_dialysis = sampled_ichd_time
                if self.config.trace:
                    print(
                        f"Patient {patient.id} of age group {patient.age_group} changed dialysis modality at time {self.env.now}."
                    )
                self.results_df.loc[patient.id, "ichd_dialysis_count"] -= 1
                yield self.env.process(self.start_dialysis(patient))

        patient.last_dialysis_modality = "ichd"

    def start_hhd(self, patient):
        """Function containing the logic for the hhd pathway

        Args:
            patient (Patient): An instance of the Patient object

        Yields:
            simpy.Environment.Timeout: Simpy Timeout event with a delay of the start time for the specific patient in the system
        """

        if self.config.trace:
            print(
                f"Patient {patient.id} of age group {patient.age_group} starts hhd at time {self.env.now}."
            )
        # TODO: If ICHD okay above then I'll fill this out in a similar way
        yield self.env.timeout(5)
        patient.last_dialysis_modality = "hhd"

    def start_pd(self, patient):
        """Function containing the logic for the pd pathway

        Args:
            patient (Patient): An instance of the Patient object

        Yields:
            simpy.Environment.Timeout: Simpy Timeout event with a delay of the start time for the specific patient in the system
        """
        if self.config.trace:
            print(
                f"Patient {patient.id} of age group {patient.age_group} starts pd at time {self.env.now}."
            )
        # TODO: If ICHD okay above then I'll fill this out in a similar way

        yield self.env.timeout(5)
        patient.last_dialysis_modality = "pd"

    def snapshot_results(self):
        while True:
            self.snapshot_results_df = pd.concat(
                [
                    self.snapshot_results_df,
                    self.results_df.assign(snapshot_time=self.env.now),
                ]
            )
            if self.config.trace:
                print(
                    f"Taking results snapshot of the results_df at time {self.env.now}"
                )
            yield self.env.timeout(self.snapshot_interval)

    def run(self):
        """Runs the model"""
        # We set up a generator for each of the patient types we have an IAT for
        for patient_type in self.inter_arrival_times.keys():
            self.env.process(self.generator_patient_arrivals(patient_type))

        self.env.process(self.snapshot_results())

        self.env.run(until=self.config.sim_duration)

        # self.calculate_run_results()

        # Show results (optional - set in config)
        if self.config.trace:
            print(f"Run Number {self.run_number}")
            print(self.patients_in_system)
            print(self.results_df)
            print(self.snapshot_results_df)


if __name__ == "__main__":
    config = Config({"trace": True})
    rng = np.random.default_rng(config.random_seed)
    model = Model(1, rng, config)
    model.run()
