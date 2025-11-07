from renal_capacity_model.model import Model
from renal_capacity_model.config import Config
from sim_tools.time_dependent import nspp_simulation
import numpy as np
import pandas as pd


def test_arrival_processes(patient_type, config):
    # Takes in the results dataframe from a model run and checks for each patient type
    # that the number of arrivals is roughly equal to what we would expect
    data = config.mean_iat_over_time_dfs[patient_type]
    nspp_replications = nspp_simulation(data, n_reps=100)
    nspp_replications.columns = data["t"].values
    results = pd.DataFrame(nspp_replications.mean()).rename(
        columns={0: "sampled_arrivals"}
    )
    results["sampled_arrival_rate"] = results["sampled_arrivals"] / 365
    print(f"** \n Showing results for {patient_type}: \n")
    full_results = data.merge(results, left_on="t", right_index=True)
    print(full_results)
    return full_results


if __name__ == "__main__":
    config = Config({"sim_duration": 13 * 365, "initialise_prevalent_patients": False})
    rng = np.random.default_rng(config.random_seed)
    model = Model(1, rng, config)
    for patient_type in model.patient_types:
        test_arrival_processes(patient_type, config)
