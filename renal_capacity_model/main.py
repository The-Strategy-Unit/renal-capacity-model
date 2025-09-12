"""
Module for running the experiment
"""

from trial import Trial
from config import Config


def main(config):
    """Main function for running the experiment"""
    trial = Trial(config)
    trial.run_trial()


if __name__ == "__main__":
    config = Config()
    main(config)
