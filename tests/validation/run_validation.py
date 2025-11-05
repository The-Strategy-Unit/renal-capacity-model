from renal_capacity_model.model import Model
from renal_capacity_model.config import Config
import numpy as np
import pandas as pd

validation_config = {
    "prevalent_counts": {
        "conservative_care": {
            "1_early": 396,
            "2_early": 599,
            "3_early": 796,
            "4_early": 846,
            "5_early": 2277,
            "6_early": 2205,
            "1_late": 76,
            "2_late": 124,
            "3_late": 165,
            "4_late": 168,
            "5_late": 470,
            "6_late": 466,
        },
        "ichd": {
            "1_early": 1094,
            "2_early": 1562,
            "3_early": 2456,
            "4_early": 3252,
            "5_early": 4137,
            "6_early": 1704,
            "1_late": 201,
            "2_late": 336,
            "3_late": 529,
            "4_late": 647,
            "5_late": 849,
            "6_late": 381,
        },
        "hhd": {
            "1_early": 39,
            "2_early": 93,
            "3_early": 106,
            "4_early": 103,
            "5_early": 57,
            "6_early": 7,
            "1_late": 6,
            "2_late": 15,
            "3_late": 26,
            "4_late": 16,
            "5_late": 10,
            "6_late": 2,
        },
        "pd": {
            "1_early": 220,
            "2_early": 362,
            "3_early": 516,
            "4_early": 693,
            "5_early": 679,
            "6_early": 226,
            "1_late": 46,
            "2_late": 72,
            "3_late": 110,
            "4_late": 149,
            "5_late": 141,
            "6_late": 39,
        },
        "live_transplant": {
            "1_early": 945,
            "2_early": 1047,
            "3_early": 1061,
            "4_early": 765,
            "5_early": 303,
            "6_early": 18,
            "1_late": 186,
            "2_late": 252,
            "3_late": 229,
            "4_late": 149,
            "5_late": 59,
            "6_late": 3,
        },
        "cadaver_transplant": {
            "1_early": 1268,
            "2_early": 2334,
            "3_early": 3033,
            "4_early": 2809,
            "5_early": 1656,
            "6_early": 250,
            "1_late": 250,
            "2_late": 446,
            "3_late": 595,
            "4_late": 557,
            "5_late": 352,
            "6_late": 41,
        },
    }
}

if __name__ == "__main__":
    config = Config(validation_config)
    rng = np.random.default_rng(config.random_seed)
    model = Model(1, rng, config)
    model.run()
