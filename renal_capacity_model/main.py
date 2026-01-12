"""
Module for running the experiment
"""

import argparse
from renal_capacity_model.trial import Trial
from renal_capacity_model.config import Config
from renal_capacity_model.config_values import national_config_dict
from renal_capacity_model.load_scenario import (
    load_scenario_from_excel,
)
from renal_capacity_model.process_outputs import (
    write_results_to_excel,
    copy_excel_files,
    produce_combined_results_for_all_model_runs,
)
from renal_capacity_model.helpers import get_logger
from datetime import datetime
import os

logger = get_logger()


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input_filepath",
        help="Path to the Renal Modelling Input Excel file for regional models. If omitted, defaults to National model",
        type=str,
        default=None,
    )
    parser.add_argument(
        "--validation",
        help="Whether to run the model with validation or experimental values. Defaults to experimental",
        action="store_true",
    )
    return parser.parse_args()


def main(
    config: Config,
    path_to_inputs_file: str | None = None,
    path_to_outputs_file: str | None = None,
):
    """Main function for running the experiment

    Args:
        config (Config): Config entity set up with the desired model run configuration values
        path_to_inputs_file (str | None, optional): Path to inputs file, used for regional model runs. Defaults to None (national values).
        path_to_outputs_file (str | None, optional): Path to outputs file, used for regional model runs. Defaults to None (national values).
    """
    run_start_time = datetime.now().strftime("%Y%m%d-%H%M")
    trial = Trial(config, run_start_time)
    trial.run_trial()
    if path_to_inputs_file:
        filepaths = []
        combined_results = produce_combined_results_for_all_model_runs(
            trial.results_dfs
        )
        for excel_file in [path_to_inputs_file, path_to_outputs_file]:
            filepaths.append(copy_excel_files(excel_file, run_start_time))
        write_results_to_excel(filepaths[1], combined_results, trial.costs_dfs)


if __name__ == "__main__":
    args = parse_args()
    results_filepath = None
    if args.input_filepath:
        config_dict = load_scenario_from_excel(args.input_filepath, args.validation)
        results_filepath = args.input_filepath.replace("Input", "Output")
        if os.path.exists(results_filepath):
            logger.info("✅ Output Excel file exists")
        else:
            raise ValueError("⚠️ Output Excel file does not exist!")
    else:
        logger.info(
            "Running national version of model. ⚠️ Validation and results Excel file currently not available"
        )
        config_dict = national_config_dict
    config = Config(config_dict)
    if results_filepath:
        main(config, args.input_filepath, results_filepath)
    else:
        main(config, args.input_filepath)
