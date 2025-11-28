import pytest
from renal_capacity_model.helpers import (
    check_config_duration_valid,
    calculate_lookup_year,
)
from renal_capacity_model.config import Config
from renal_capacity_model.config_values import national_config_dict


@pytest.mark.parametrize(
    "time_units, expected",
    [(0.1, 1), (365, 1), (4745, 13)],
)
def test_calculate_lookup_year(time_units, expected):
    assert calculate_lookup_year(time_units) == expected


def test_check_config_duration_valid_passes(
    config_values={
        "sim_duration": 730,
        "pre_emptive_transplant_live_donor_dist": {1: {}, 2: {}},
    },
):
    # arrange
    config_dict = national_config_dict.copy()
    for k, v in config_values.items():
        config_dict[k] = v
    config = Config(config_dict)
    # act, assert
    assert check_config_duration_valid(config)


def test_check_config_duration_valid_raises_error(
    config_values={
        "sim_duration": 730,
        "pre_emptive_transplant_live_donor_dist": {1: {}},
    },
):
    # arrange
    config_dict = national_config_dict.copy()
    for k, v in config_values.items():
        config_dict[k] = v
    config = Config(config_dict)
    # act, assert
    with pytest.raises(ValueError):
        check_config_duration_valid(config)
