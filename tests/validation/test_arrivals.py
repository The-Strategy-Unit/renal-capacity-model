from renal_capacity_model.model import Model
from renal_capacity_model.config import Config
import numpy as np
import pandas as pd


def compare_modelled_arrivals_with_expected(event_log, config):
    # only look at arrivals
    arrival_indexes = event_log.groupby("patient_id").head(1).index
    arrivals = event_log.loc[arrival_indexes]
    comparison_df = pd.DataFrame(
        arrivals.groupby("year_start")["patient_type"].value_counts()
    )
    comparison_df["modelled_arrival_rate"] = comparison_df["count"] / 365
    for year, patient_type in comparison_df.index:
        comparison_df.loc[(year, patient_type), "expected_arrival_rate"] = (
            config.mean_iat_over_time_dfs[patient_type].loc[year, "arrival_rate"]
        )
    return comparison_df


if __name__ == "__main__":
    config = Config()
    config.initialise_prevalent_patients = False
    config.trace = True
    rng = np.random.default_rng(config.random_seed)
    model = Model(1, rng, config, "start_time")
    model.run()
    event_log = model.event_log
    compare_modelled_arrivals_with_expected(event_log, config).to_csv(
        "results/test_arrival_rates.csv"
    )
