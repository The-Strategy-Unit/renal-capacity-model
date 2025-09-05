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
            columns=["entry_time", "diverted_to_con_care", "time_of_death"]
        )
        results_df["patient ID"] = [1]
        results_df.set_index("patient ID", inplace=True)
        return results_df

    def generator_patient_arrivals(self, rng, patient_type):
        """Generator function for arriving patients

        Args:
            rng (np.random.Generator): Random Number Generator
            patient_type (str): Type of patient. Used to retrieve correct inter-arrival time.

        Yields:
            simpy.Environment.Timeout: Simpy Timeout event with a delay of the sampled inter-arrival time
        """
        while True:
            self.patient_counter += 1

            p = Patient(self.patient_counter, patient_type)
            start_time_in_system_patient = self.env.now
            self.results_df.loc[p.id, "entry_time"] = start_time_in_system_patient
            self.results_df.loc[p.id, "age_group"] = int(p.age_group)
            self.results_df.loc[p.id, "referral_type"] = p.referral_type

            if rng.uniform(0, 1) > self.config.con_care_dist[p.age_group]:
                # If the patient is not diverted to conservative care they start KRT
                self.patients_in_system[patient_type] += 1
                self.env.process(self.start_krt(p))
            else:
                # these patients are diverted to conservative care. We don't need a process here as all these patients do is wait a while before leaving the system
                self.results_df.loc[p.id, "diverted_to_con_care"] = True
                yield self.env.timeout(start_time_in_system_patient)
                sampled_con_care_time = self.config.ttd_con_care_scale * rng.weibull(
                    a=self.config.ttd_con_care_shape, size=1
                )
                yield self.env.timeout(sampled_con_care_time)
                self.results_df.loc[p.id, "time_of_death"] = sampled_con_care_time
                if self.config.trace:
                    print(
                        f"Patient {p.id} of age group {p.age_group} diverted to conservative care and left the system after {sampled_con_care_time} time units."
                    )
                    print(self.patients_in_system)

            sampled_inter_arrival_time = rng.exponential(
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


if __name__ == "__main__":
    config = Config({"trace": True})
    rng = np.random.default_rng(config.random_seed)
    model = Model(1, rng, config)
    model.run()
