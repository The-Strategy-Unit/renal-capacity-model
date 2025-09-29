import pytest
from renal_capacity_model.model import Model
from renal_capacity_model.config import Config
import numpy as np
from renal_capacity_model.trial import Trial


@pytest.fixture
def config():
    return Config()


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
    assert trial.df_trial_results.shape[0] > 0  # There are results in the dataframe
