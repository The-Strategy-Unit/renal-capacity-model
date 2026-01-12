import pytest
import pandas as pd
from renal_capacity_model.process_outputs import create_yearly_activity_duration


@pytest.fixture
def event_log():
    event_log = pd.DataFrame(
        {
            "patient_id": {
                0: 1,
                1: 2,
                2: 3,
                3: 4,
                4: 5,
            },
            "patient_flag": {
                0: "prevalent",
                1: "prevalent",
                2: "incident",
                3: "incident",
                4: "incident",
            },
            "activity_from": {
                0: "ichd",
                1: "cadaver",
                2: "ichd",
                3: "ichd",
                4: "live",
            },
            "time_starting_activity_from": {
                0: 0.0,
                1: 0.0,
                2: 165.0,
                3: 165.0,
                4: 165.0,
            },
            "time_spent_in_activity_from": {
                0: 50.0,
                1: 4750.0,
                2: 100.0,
                3: 4750.0,
                4: 100.0,
            },
            "year_start": {
                0: 0,
                1: 0,
                2: 1,
                3: 1,
                4: 1,
            },
            "year_end": {
                0: 1,
                1: 14,
                2: 1,
                3: 14,
                4: 1,
            },
        }
    )
    event_log["end_time"] = (
        event_log["time_starting_activity_from"]
        + event_log["time_spent_in_activity_from"]
    )
    return event_log


def test_create_yearly_activity_duration(event_log):
    # arrange
    expected_ichd = 350
    expected_transplant = 465

    # act
    result = create_yearly_activity_duration(event_log, 0).set_index("year")

    # assert
    assert result.loc[1, "ichd"] == expected_ichd
    assert result.loc[1, "transplant"] == expected_transplant
