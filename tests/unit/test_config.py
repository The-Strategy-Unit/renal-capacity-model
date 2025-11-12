import pytest
from renal_capacity_model.config import Config


@pytest.mark.parametrize(
    "config_dict, expected",
    [({}, (True, 0)), ({"trace": False, "random_seed": 99}, (False, 99))],
)
def test_config_initialises_with_values(config_dict, expected):
    # arrange
    # act
    config = Config(config_dict)

    # assert
    assert config.trace == expected[0]
    assert config.random_seed == expected[1]
