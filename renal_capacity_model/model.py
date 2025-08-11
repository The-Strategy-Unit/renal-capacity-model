import simpy
from entity import Patient
import numpy as np
import random
from config import g
from distributions import get_interarrival_times


class Model:
    def __init__(self, run_number, rng):
        self.env = simpy.Environment()
        self.patient_counter = 0
        self.run_number = run_number
        self.rng = rng
        self.inter_arrival_times = get_interarrival_times()
        self.patients_in_system = {k: 0 for k in self.inter_arrival_times.keys()}

        # self.results_df = pd.DataFrame()
        # self.results_df["patient ID"] = [1]
        # self.results_df["Queue Time"] = [0.0]
        # self.results_df.set_index("patient ID", inplace=True)

    def generator_patient_arrivals(self, rng, patient_type):

        while True:
            self.patient_counter += 1

            p = Patient(self.patient_counter, patient_type)
            self.patients_in_system[patient_type] += 1

            self.env.process(self.start_krt(p))
            sampled_inter_arrival_time = rng.exponential(
                self.inter_arrival_times[patient_type]
            )

            yield self.env.timeout(sampled_inter_arrival_time)

    def start_krt(self, patient):
        start_time_in_system_patient = self.env.now

        # TODO: No current processes - patients just enter system at the moment
        yield self.env.timeout(start_time_in_system_patient)

    def calculate_run_results(self):
        # TODO: what do we want to count?
        pass

    def run(self):
        for patient_type in self.inter_arrival_times.keys():
            self.env.process(self.generator_patient_arrivals(self.rng, patient_type))

        # Run the model for the duration specified in g class
        self.env.run(until=g.sim_duration)

        # Now the simulation run has finished, call the method that calculates
        # run results
        self.calculate_run_results()

        # Show results (optional - set in config)
        if g.trace:
            print(f"Run Number {self.run_number}")
            print(self.patients_in_system)


if __name__ == "__main__":
    rng = np.random.default_rng(g.random_seed)
    model = Model(1, rng)
    model.run()
