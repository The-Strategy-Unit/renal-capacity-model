import pytest
from renal_capacity_model.helpers import (
    check_config_duration_valid,
    calculate_lookup_year,
)
from renal_capacity_model.config import Config


@pytest.mark.parametrize(
    "time_units, expected",
    [(0.1, 1), (365, 1), (4745, 13)],
)
def test_calculate_lookup_year(time_units, expected):
    assert calculate_lookup_year(time_units) == expected


def test_check_config_duration_valid_passes(
    config_dict={"sim_duration": 730, "time_on_waiting_list_mean": {1: {}, 2: {}}},
):
    # arrange
    config = Config(config_dict)
    # act, assert
    assert check_config_duration_valid(config)


def test_check_config_duration_valid_raises_error(
    config_dict={"sim_duration": 730, "time_on_waiting_list_mean": {1: {}}},
):
    # arrange
    config = Config(config_dict)
    # act, assert
    with pytest.raises(ValueError):
        check_config_duration_valid(config)
