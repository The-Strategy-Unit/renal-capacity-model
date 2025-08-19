"""
Module containing the Model class. Contains most of the logic for the simulation.
"""

import simpy
from entity import Patient
import numpy as np
from config import g
from helpers import get_interarrival_times
import pandas as pd


class Model:
    """
    Model class containing the logic for the simulation
    """

    def __init__(self, run_number, rng):
        """Initialise the model

        Args:
            run_number (int): Which run number in the Trial this Model is for
            rng (np.random.Generator): Random Number Generator used for the whole experiment
        """
        self.env = simpy.Environment()
        self.patient_counter = 0
        self.run_number = run_number
        self.rng = rng
        self.inter_arrival_times = get_interarrival_times()
        self.patients_in_system = {k: 0 for k in self.inter_arrival_times.keys()}
        self.results_df = self._setup_results_df()

    def _setup_results_df(self):
        """Sets up DataFrame for recording model results

        Returns:
            pd.DataFrame: Empty DataFrame for recording model results
        """
        results_df = pd.DataFrame()
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
            self.patients_in_system[patient_type] += 1

            if rng.uniform(0,1) > g.con_care_dist[p.age_group]:
                # If the patient is not diverted to conservative care they start KRT
                self.env.process(self.start_krt(p))
            else:
                # these patients are diverted to conservative care. We don't need a process here as all these patients do is wait a while before leaving the system
                start_time_in_system_patient = self.env.now
                yield self.env.timeout(start_time_in_system_patient)
                sampled_con_care_time = rng.weibull(
                    a=g.ttd_con_care_shape, size=1
                )
                yield self.env.timeout(g.ttd_con_care_scale*sampled_con_care_time)
                self.patient_counter -= 1
                self.patients_in_system[patient_type] -= 1
                if g.trace:
                    print(f"Patient {p.id} of age group {p.age_group} diverted to conservative care and left the system after {g.ttd_con_care_scale*sampled_con_care_time} time units.")
                    print(self.patients_in_system)
        
            sampled_inter_arrival_time = rng.exponential(
            1/self.inter_arrival_times[patient_type]
            )

            yield self.env.timeout(sampled_inter_arrival_time)
            



    def start_krt(self, patient):
        """Function containing the logic for the Kidney Replacement Therapy pathway

        Args:
            patient (Patient): An instance of the Patient object

        Yields:
            simpy.Environment.Timeout: Simpy Timeout event with a delay of the start time for the specific patient in the system
        """
        start_time_in_system_patient = self.env.now

        # TODO: No current processes - patients just enter system at the moment
        yield self.env.timeout(start_time_in_system_patient)

    def calculate_run_results(self):
        # TODO: what do we want to count?
        pass

    def run(self):
        """Runs the model"""
        # We set up a generator for each of the patient types we have an IAT for
        for patient_type in self.inter_arrival_times.keys():
            self.env.process(self.generator_patient_arrivals(self.rng, patient_type))

        self.env.run(until=g.sim_duration)

        self.calculate_run_results()

        # Show results (optional - set in config)
        if g.trace:
            print(f"Run Number {self.run_number}")
            print(self.patients_in_system)


if __name__ == "__main__":
    rng = np.random.default_rng(g.random_seed)
    model = Model(1, rng)
    model.run()
