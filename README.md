# Renal capacity model

<!-- badges: start -->

[![Project Status: WIP – Initial development is in progress, but there has not yet been a stable, usable release suitable for the public.](https://www.repostatus.org/badges/latest/wip.svg)](https://www.repostatus.org/#wip)
[![codecov](https://codecov.io/gh/The-Strategy-Unit/renal-capacity-model/graph/badge.svg?token=lr1OaInPCf)](https://codecov.io/gh/The-Strategy-Unit/renal-capacity-model)

<!-- badges: end -->

Repository with Python code for the Renal Capacity Model, an open source implementation of the Discrete Event Simulation (DES) [Renal Services model created in collaboration with the Midlands Renal Operational Delivery Network (MRODN)](https://github.com/The-Strategy-Unit/renal-services).

⚠️ **Please note that the code in this repository is still in development**

## Installation

This project was created with [uv](https://github.com/astral-sh/uv).
Although not essential, the instructions will assume you have this installed.

To install the package:

1. Clone the repository to your local machine. Open the repository.
2. Run `uv pip install -e .`

## Running the model

Once installed, set the configuration for your model run in `config.py`.

Run the model using `uv run renal_capacity_model/main.py`. This runs a full trial.

To run a single model run, use `uv run renal_capacity_model/model.py`

## Information for developers

### Testing

There are two types of tests for the model:

- Unit tests, which run automatically as part of the pytest testing suite. These check the
behaviour of the individual elements of code to ensure they behave as expected using strict
testing criteria.
- Validation tests, which are excluded from the pytest testing suite. These are manually
run and require users to view results and use their own judgment to check validity.

To run the unit tests:

- `uv run pytest`

Check code unit testing coverage using:

- `uv run coverage run -m pytest`

View the code unit testing coverage report using:

- `uv run coverage report`

To run the validation tests:

- `uv run tests/validation/validation_test_file.py`
