import simpy
from entity import Patient
import numpy as np
import random
from config import g
from distributions import probabilities_dict


class Model:
    # Constructor to set up the model for a run.  We pass in a run number when
    # we create a new model.
    def __init__(self, run_number, rng):
        self.env = simpy.Environment()
        self.patient_counter = 0
        self.patients_in_system = {k: 0 for k in probabilities_dict.keys()}
        self.run_number = run_number
        self.rng = rng

        # # Create a new Pandas DataFrame that will store some results against
        # # the patient ID (which we'll use as the index).
        # self.results_df = pd.DataFrame()
        # self.results_df["patient ID"] = [1]
        # self.results_df["Queue Time"] = [0.0]
        # self.results_df.set_index("patient ID", inplace=True)

        # Create an attribute to store the mean queuing time for the support agents
        # across this run of the model

    # A generator function that represents the DES generator for patient
    # arrivals
    def generator_patient_arrivals(self, rng):
        # We use an infinite loop here to keep doing this indefinitely whilst
        # the simulation runs
        while True:
            # Increment the patient counter by 1 (this means our first patient
            # will have an ID of 1)
            self.patient_counter += 1

            # type_of_patient = randomly sample from probabilities_dict
            # Compute the total sum
            total = sum(probabilities_dict.values())
            normalized_probabilities = {
                key: value / total for key, value in probabilities_dict.items()
            }
            probabilities_array = np.array(list(normalized_probabilities.values()))
            patient_type_selection = rng.choice(12, None, p=probabilities_array)
            patient_type = list(probabilities_dict.keys())[patient_type_selection]
            self.patients_in_system[patient_type] += 1
            c = Patient(self.patient_counter, patient_type)

            self.env.process(self.start_krt(c))

            # Randomly sample the time to the next patient arriving.  Here, we
            # sample from an exponential distribution (common for inter-arrival
            # times), and pass in a lambda value of 1 / mean.  The mean
            # inter-arrival time is stored in the g class.
            sampled_inter_arrival_time = random.expovariate(g.patient_arrival_rate)

            # Freeze this instance of this function in place until the
            # inter-arrival time we sampled above has elapsed.  Note - time in
            # SimPy progresses in "Time Units", which can represent anything
            # you like (just make sure you're consistent within the model)
            yield self.env.timeout(sampled_inter_arrival_time)

    # A generator function that represents the pathway for a patient entering the system

    # The patient object is passed in to the generator function so we can
    # extract information from / record information to it
    def start_krt(self, patient):
        # Record the time the patient started queuing for a nurse
        start_time_in_system_patient = self.env.now

        # TODO: No current processes - patients just enter system at the moment
        yield self.env.timeout(start_time_in_system_patient)

    # This method calculates results over a single run.  Here we just calculate
    # a mean, but in real world models you'd probably want to calculate more.
    def calculate_run_results(self):
        # TODO: what do we want to count?
        pass

    # The run method starts up the DES entity generators, runs the simulation,
    # and in turns calls anything we need to generate results for the run
    def run(self):
        # Start up our DES entity generators that create new customers.  We've
        # only got one in this model, but we'd need to do this for each one if
        # we had multiple generators.
        self.env.process(self.generator_patient_arrivals(self.rng))

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
