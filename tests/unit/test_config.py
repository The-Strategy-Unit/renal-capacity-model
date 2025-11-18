import pytest
from renal_capacity_model.config import Config


@pytest.mark.parametrize(
    "config_dict, expected",
    [({}, (365, 0)), ({"snapshot_interval": 100, "random_seed": 99}, (100, 99))],
)
def test_config_initialises_with_values(config_dict, expected):
    # arrange
    # act
    config = Config(config_dict)

    # assert
    assert config.snapshot_interval == expected[0]
    assert config.random_seed == expected[1]
