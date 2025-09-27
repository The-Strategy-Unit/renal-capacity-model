from renal_capacity_model.model import Model
from renal_capacity_model.config import Config
import numpy as np
import pandas as pd


def test_arrival_processes(results_df, config):

    # Takes in the results dataframe from a model run and checks for each patient type
    # that the number of arrivals is roughly equal to what we would expect
    # TODO: currently only works on single model run - should probably check average across
    # entire trial?
    expected_iat_dict = {}
    for referral, referral_value in config.referral_dist.items():
        for age_group, age_value in config.age_dist.items():
            expected_iat_dict[f"{age_group}_{referral}"] = config.arrival_rate / (
                age_value * referral_value
            )

    observed_iat_dict = {}
    for referral, referral_value in config.referral_dist.items():
        for age_group, age_value in config.age_dist.items():
            inds = results_df.index[
                (results_df["age_group"] == age_group)
                & (results_df["referral_type"] == referral)
            ].tolist()
            observed_iat_dict[f"{age_group}_{referral}"] = float(
                1 / results_df.loc[inds, "entry_time"].mean()
            )
    return pd.DataFrame({"observed": observed_iat_dict, "expected": expected_iat_dict})


if __name__ == "__main__":
    config = Config()
    rng = np.random.default_rng(config.random_seed)
    model = Model(1, rng, config)
    model.run()
    results_df = model.results_df
    print(test_arrival_processes(results_df, config))
