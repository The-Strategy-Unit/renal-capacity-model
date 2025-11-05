from renal_capacity_model.model import Model
from renal_capacity_model.config import Config
from sim_tools.time_dependent import NSPPThinning, nspp_plot, nspp_simulation
import numpy as np
import pandas as pd


# def test_arrival_processes(results_df, config):
#     # Takes in the results dataframe from a model run and checks for each patient type
#     # that the number of arrivals is roughly equal to what we would expect
#     # TODO: currently only works on single model run - should probably check average across
#     # entire trial?
#     observed_iat_dict = {}
#     for referral, referral_value in config.referral_dist.items():
#         for age_group, age_value in config.age_dist.items():
#             inds = results_df.index[
#                 (results_df["age_group"] == age_group)
#                 & (results_df["referral_type"] == referral)
#             ].tolist()
#             observed_iat_dict[f"{age_group}_{referral}"] = float(
#                 1 / results_df.loc[inds, "entry_time"].mean()
#             )
#     return observed_iat_dict


if __name__ == "__main__":
    config = Config({"sim_duration": 13 * 365, "initialise_prevalent_patients": False})
    rng = np.random.default_rng(config.random_seed)
    model = Model(1, rng, config)
    data = config.mean_iat_over_time_dfs["5_early"]
    nspp_replications = nspp_simulation(data, n_reps=1000)
    # re-label columns
    nspp_replications.columns = data["t"].values
    ## banks data converted from arrivals per min to arrivals per hour
    print(data)
    print(nspp_replications)
