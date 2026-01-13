# Renal capacity model

<!-- badges: start -->

[![Project Status: WIP – Initial development is in progress, but there has not yet been a stable, usable release suitable for the public.](https://www.repostatus.org/badges/latest/wip.svg)](https://www.repostatus.org/#wip)
[![codecov](https://codecov.io/gh/The-Strategy-Unit/renal-capacity-model/graph/badge.svg?token=lr1OaInPCf)](https://codecov.io/gh/The-Strategy-Unit/renal-capacity-model)

<!-- badges: end -->

This repository contains the Python code for the Renal Capacity Model, an open source implementation of the Discrete Event Simulation (DES) [Renal Services model created in collaboration with the Midlands Renal Operational Delivery Network (MRODN)](https://www.strategyunitwm.nhs.uk/news/planning-rising-renal-demand-simulating-capacity-across-care-system).

The code in this repository has been geared towards working with input Excel files that are adapted for specific regions in England. To obtain an input Excel file for your region, please contact [the Strategy Unit](mailto:strategy.unit@nhs.net).

The default config contains the values for the national version of the model. However this has not yet been validated and documentation is sparse. We will provide further details on how to run the national version of the model, or adapt the model to be used without an input Excel file, in due course.

⚠️ **Please note that the code in this repository is still in development**

## How to use this package using an input Excel file

### Data preparation

1. [Clone a copy](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository) of the repository to your local machine.
1. Create a `data` folder. Put your `Renal_Modelling_Input_File - REGION.xlsx` and `Renal_Modelling_Output_File - REGION.xlsx` in this folder.
1. Optional: Create a results folder for your model results.

Your repository structure should look like the below:

```bash
.
├── data/
│   ├── Renal_Modelling_Input_File - REGION.xlsx
│   └── Renal_Modelling_Output_File - REGION.xlsx
├── reference/
│   ├── ttgf_cadTx_initialisation.csv
│   ├── ttgf_cadTx.csv
│   └── ...
├── renal_capacity_model/
│   ├── __init__.py
│   ├── config_values.py
│   ├── config.py
│   └── ...
├── results/
├── tests/
│   └── ...
├── .gitignore
├── ...
├── README.md
└── uv.lock
```

### Running the model using uv

Our preferred tool for dependency management is [uv](https://github.com/astral-sh/uv). If using this tool:

1. Run the model using `uv run -m renal_capacity_model.main --input_filepath 'data/Renal_Modelling_Input_File - REGION.xlsx'`

### Running the model without uv

1. Open the repository folder. Install the package using `pip install .`
1. Run the model using `python -m renal_capacity_model.main --input_filepath 'data/Renal_Modelling_Input_File - REGION.xlsx'`

### Viewing model results

Your results will be saved in the `results` folder, in a subfolder with the date and time of the model run. For example:

```bash
├── results/
    └── 20260101-1201/
        ├── Input - REGION_20260101-1201.xlsx
        └── Output - REGION_20260101-1201.xlsx
```

### National model

Run the model using `uv run -m renal_capacity_model.main`. This runs a full trial using national values, stored in `config_values.py`. Note that the size of the national model is very large and will take several hours to complete. We also have not yet validated the national version of the model.

## Information for developers

### Running the model (validation version)

Run the full trial with validation values instead of experimental values using `uv run -m renal_capacity_model.main --input_filepath path/to/excel_file --validation`. This compares historical data from the [UK Renal Registry (UKRR)](https://www.ukkidney.org/about-us/who-we-are/uk-renal-registry) from 2010-2023 with modelled results using a baseline year of 2010.

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

### Contributing to this repository

We have set up some linting tools to help maintain good coding practices. To use these:

- `uv sync --all-extras` to install the development-only packages
- `uv run pyright` to run typing checks with pyright
- `uv run ruff check` to run linting checks with ruff
- `uv run ruff format` to run formatting checks with ruff
