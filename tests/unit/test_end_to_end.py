import pytest
from renal_capacity_model.model import Model
from renal_capacity_model.config import Config
import numpy as np
from renal_capacity_model.trial import Trial


@pytest.fixture
def config():
    return Config(
        {
            "prevalent_counts": {
                "conservative_care": {
                    "1_early": 1,
                    "2_early": 1,
                    "3_early": 1,
                    "4_early": 1,
                    "5_early": 1,
                    "6_early": 1,
                    "1_late": 1,
                    "2_late": 1,
                    "3_late": 1,
                    "4_late": 1,
                    "5_late": 1,
                    "6_late": 1,
                },
                "ichd": {
                    "1_early": 1,
                    "2_early": 1,
                    "3_early": 1,
                    "4_early": 1,
                    "5_early": 1,
                    "6_early": 1,
                    "1_late": 1,
                    "2_late": 1,
                    "3_late": 1,
                    "4_late": 1,
                    "5_late": 1,
                    "6_late": 1,
                },
                "hhd": {
                    "1_early": 1,
                    "2_early": 1,
                    "3_early": 1,
                    "4_early": 1,
                    "5_early": 1,
                    "6_early": 1,
                    "1_late": 1,
                    "2_late": 1,
                    "3_late": 1,
                    "4_late": 1,
                    "5_late": 1,
                    "6_late": 1,
                },
                "pd": {
                    "1_early": 1,
                    "2_early": 1,
                    "3_early": 1,
                    "4_early": 1,
                    "5_early": 1,
                    "6_early": 1,
                    "1_late": 1,
                    "2_late": 1,
                    "3_late": 1,
                    "4_late": 1,
                    "5_late": 1,
                    "6_late": 1,
                },
                "live_transplant": {
                    "1_early": 1,
                    "2_early": 1,
                    "3_early": 1,
                    "4_early": 1,
                    "5_early": 1,
                    "6_early": 1,
                    "1_late": 1,
                    "2_late": 1,
                    "3_late": 1,
                    "4_late": 1,
                    "5_late": 1,
                    "6_late": 1,
                },
                "cadaver_transplant": {
                    "1_early": 1,
                    "2_early": 1,
                    "3_early": 1,
                    "4_early": 1,
                    "5_early": 1,
                    "6_early": 1,
                    "1_late": 1,
                    "2_late": 1,
                    "3_late": 1,
                    "4_late": 1,
                    "5_late": 1,
                    "6_late": 1,
                },
            }
        }
    )


@pytest.fixture
def rng():
    return np.random.default_rng(1)


def test_single_model_run(config, rng):
    model = Model(1, rng, config)
    model.run()
    assert model.results_df.shape[0] > 0  # There are results in the dataframe


def test_full_trial_run(config):
    trial = Trial(config)
    trial.run_trial()
    if trial.df_trial_results is not None:
        assert trial.df_trial_results.shape[0] > 0  # There are results in the dataframe
