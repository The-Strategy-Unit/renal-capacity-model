"""
Module for running the experiment
"""

import argparse
from renal_capacity_model.trial import Trial
from renal_capacity_model.config import Config
from renal_capacity_model.load_scenario import load_scenario_from_excel


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input_filepath",
        help="Filepath to Renal Modelling Input file. If not provided, default National config values will be used instead",
        type=str,
        default="",
    )
    parser.add_argument(
        "--validation",
        help="Whether to run the model with validation or experimental values. Defaults to experimental",
        action="store_true",
    )
    return parser.parse_args()


def main(config):
    """Main function for running the experiment"""
    trial = Trial(config)
    trial.run_trial()


if __name__ == "__main__":
    args = parse_args()
    config_dict = {}
    if len(args.input_filepath) > 0:
        config_dict = load_scenario_from_excel(args.input_filepath, args.validation)
    config = Config(config_dict)
    main(config)
