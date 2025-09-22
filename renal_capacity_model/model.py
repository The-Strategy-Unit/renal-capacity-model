"""
Module containing the Model class. Contains most of the logic for the simulation.
"""

import simpy
from entity import Patient
import numpy as np
from config import Config
from helpers import get_interarrival_times
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

    def _setup_results_df(self):
        """Sets up DataFrame for recording model results

        Returns:
            pd.DataFrame: Empty DataFrame for recording model results
        """
        results_df = pd.DataFrame(
            columns=[
                "age_group",
                "referral_type",
                "entry_time",
                "diverted_to_con_care",
                "suitable_for_transplant",
                "live_transplant",
                "cadaver_transplant",
                "pre_emptive_transplant",
                "time_of_death",
            ]
        )
        results_df["patient ID"] = [1]
        results_df.set_index("patient ID", inplace=True)

        return results_df

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
            start_time_in_system_patient = self.rng.exponential(
                1 / self.inter_arrival_times[patient_type]
            )  # self.env.now
            self.results_df.loc[p.id, "entry_time"] = start_time_in_system_patient
            self.results_df.loc[p.id, "age_group"] = int(p.age_group)
            self.results_df.loc[p.id, "referral_type"] = p.referral_type

            if self.rng.uniform(0, 1) > self.config.con_care_dist[p.age_group]:
                # If the patient is not diverted to conservative care they start KRT
                self.patients_in_system[patient_type] += 1
                self.env.process(self.start_krt(p))
            else:
                # these patients are diverted to conservative care. We don't need a process here as all these patients do is wait a while before leaving the system
                self.results_df.loc[p.id, "diverted_to_con_care"] = True
                yield self.env.timeout(start_time_in_system_patient)
                sampled_con_care_time = (
                    self.config.ttd_con_care_scale
                    * self.rng.weibull(a=self.config.ttd_con_care_shape, size=1)
                )
                yield self.env.timeout(sampled_con_care_time)
                self.results_df.loc[p.id, "time_of_death"] = sampled_con_care_time
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

            yield self.env.process(self.start_dialysis_only(patient))
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
                self.results_df.loc[patient.id, "live_transplant"] = True
            else:
                patient.transplant_type = "cadaver"
                self.results_df.loc[patient.id, "cadaver_transplant"] = True

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

                    yield self.env.process(self.start_pre_emptive_transplant(patient))
                    if self.config.trace:
                        print(
                            f"Patient {patient.id} of age group {patient.age_group} started pre-emptive transplant pathway with live donor."
                        )
                else:
                    # Patient starts dialysis whilst waiting for transplant
                    self.results_df.loc[patient.id, "pre_emptive_transplant"] = False

                    yield self.env.process(
                        self.start_dialysis_whilst_waiting_for_transplant(patient)
                    )
                    if self.config.trace:
                        print(
                            f"Patient {patient.id} of age group {patient.age_group} started dialysis whilst waiting for transplant pathway with live donor."
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

                    yield self.env.process(self.start_pre_emptive_transplant(patient))
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

    def start_dialysis_only(self, patient):
        """Function containing the logic for the dialysis only pathway

        Args:
            patient (Patient): An instance of the Patient object

        Yields:
            simpy.Environment.Timeout: Simpy Timeout event with a delay of the start time for the specific patient in the system
        """

        # TODO: No current processes - patients just enter system at the moment
        yield self.env.timeout(5)

    def start_pre_emptive_transplant(self, patient):
        """Function containing the logic for the pre-emptive transplant pathway

        Args:
            patient (Patient): An instance of the Patient object

        Yields:
            simpy.Environment.Timeout: Simpy Timeout event with a delay of the start time for the specific patient in the system
        """

        # TODO: No current processes - patients just enter system at the moment
        yield self.env.timeout(5)

    def start_dialysis_whilst_waiting_for_transplant(self, patient):
        """Function containing the logic for the mixed pathway where a patient starts on dialysis and then receives a transplant

        Args:
            patient (Patient): An instance of the Patient object

        Yields:
            simpy.Environment.Timeout: Simpy Timeout event with a delay of the start time for the specific patient in the system
        """

        # TODO: No current processes - patients just enter system at the moment
        yield self.env.timeout(5)

    def calculate_run_results(self):
        # TODO: what do we want to count?
        pass

    def run(self):
        """Runs the model"""
        # We set up a generator for each of the patient types we have an IAT for
        for patient_type in self.inter_arrival_times.keys():
            self.env.process(self.generator_patient_arrivals(self.rng, patient_type))

        self.env.run(until=self.config.sim_duration)

        self.calculate_run_results()

        # Show results (optional - set in config)
        if self.config.trace:
            print(f"Run Number {self.run_number}")
            print(self.patients_in_system)
            print(self.results_df)
            # print(test_arrival_processes(self.results_df,self.config))


if __name__ == "__main__":
    config = Config({"trace": True})
    rng = np.random.default_rng(config.random_seed)
    model = Model(1, rng, config)
    model.run()
