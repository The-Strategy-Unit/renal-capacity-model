import pytest
from renal_capacity_model.config import Config


@pytest.mark.parametrize(
    "config_dict, expected",
    [({}, (False, 0)), ({"trace": True, "random_seed": 99}, (True, 99))],
)
def test_config_initialises_with_values(config_dict, expected):
    # arrange
    # act
    config = Config(config_dict)

    # assert
    config.trace == expected[0]
    config.random_seed == expected[1]
