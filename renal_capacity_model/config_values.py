import pandas as pd
from renal_capacity_model.utils import get_time_to_event_curve_filepaths

national_config_dict = {
    "arrival_rate": {
        1: 23.42,
        2: 24.61,
        3: 25.76,
        4: 26.87,
        5: 27.92,
        6: 28.90,
        7: 29.81,
        8: 30.66,
        9: 31.45,
        10: 32.19,
        11: 32.88,
        12: 33.52,
        13: 34.12,
    },
    "prevalent_counts": {
        "conservative_care": {
            "1_early": 770,
            "2_early": 911,
            "3_early": 1224,
            "4_early": 1101,
            "5_early": 2396,
            "6_early": 3853,
            "1_late": 215,
            "2_late": 193,
            "3_late": 219,
            "4_late": 199,
            "5_late": 429,
            "6_late": 680,
        },
        "ichd": {
            "1_early": 1378,
            "2_early": 1742,
            "3_early": 3126,
            "4_early": 3892,
            "5_early": 4258,
            "6_early": 3215,
            "1_late": 494,
            "2_late": 558,
            "3_late": 751,
            "4_late": 925,
            "5_late": 948,
            "6_late": 616,
        },
        "hhd": {
            "1_early": 166,
            "2_early": 191,
            "3_early": 231,
            "4_early": 173,
            "5_early": 106,
            "6_early": 38,
            "1_late": 37,
            "2_late": 44,
            "3_late": 33,
            "4_late": 23,
            "5_late": 17,
            "6_late": 5,
        },
        "pd": {
            "1_early": 241,
            "2_early": 300,
            "3_early": 423,
            "4_early": 636,
            "5_early": 706,
            "6_early": 475,
            "1_late": 90,
            "2_late": 68,
            "3_late": 75,
            "4_late": 106,
            "5_late": 91,
            "6_late": 52,
        },
        "live_transplant": {
            "1_early": 2182,
            "2_early": 1986,
            "3_early": 2196,
            "4_early": 1432,
            "5_early": 509,
            "6_early": 26,
            "1_late": 544,
            "2_late": 318,
            "3_late": 283,
            "4_late": 203,
            "5_late": 56,
            "6_late": 1,
        },
        "cadaver_transplant": {
            "1_early": 2968,
            "2_early": 3987,
            "3_early": 5048,
            "4_early": 3784,
            "5_early": 1610,
            "6_early": 99,
            "1_late": 777,
            "2_late": 756,
            "3_late": 829,
            "4_late": 537,
            "5_late": 177,
            "6_late": 6,
        },
    },
    "age_dist": {
        1: 0.07,
        2: 0.08,
        3: 0.14,
        4: 0.19,
        5: 0.25,
        6: 0.27,
    },
    "referral_dist": {"early": 0.82, "late": 0.18},
    "con_care_dist": {
        y: {1: 0.1, 2: 0.1, 3: 0.1, 4: 0.1, 5: 0.25, 6: 0.5} for y in range(1, 14)
    },
    "suitable_for_transplant_dist": {
        1: 0.88,
        2: 0.83,
        3: 0.73,
        4: 0.56,
        5: 0.30,
        6: 0.05,
    },
    "transplant_type_dist": {
        1: 0.4,
        2: 0.3,
        3: 0.26,
        4: 0.23,
        5: 0.19,
        6: 0.12,
    },
    "modality_allocation_distributions": {
        y: {
            "none": {
                "ichd": 0.79,
                "hhd": 0.01,
                "pd": 0.20,
            },
            "ichd": {
                "ichd": 0,
                "hhd": 0.46,
                "pd": 0.54,
            },
            "hhd": {
                "ichd": 0.99,
                "hhd": 0,
                "pd": 0.01,
            },
            "pd": {
                "ichd": 0.99,
                "hhd": 0.01,
                "pd": 0,
            },
        }
        for y in range(1, 14)
    },
    "death_post_transplant": {
        "live": {
            1: 0.05,
            2: 0.15,
            3: 0.26,
            4: 0.38,
            5: 0.50,
            6: 0.63,
        },
        "cadaver": {
            1: 0.07,
            2: 0.17,
            3: 0.27,
            4: 0.42,
            5: 0.54,
            6: 0.73,
        },
    },
    "death_post_dialysis_modality": {
        "ichd": {
            "early": {
                1: 0.08,
                2: 0.15,
                3: 0.18,
                4: 0.25,
                5: 0.3,
                6: 0.35,
            },
            "late": {
                1: 0.07,
                2: 0.14,
                3: 0.19,
                4: 0.24,
                5: 0.31,
                6: 0.35,
            },
        },
        "hhd": {
            "early": {
                1: 0.08,
                2: 0.16,
                3: 0.17,
                4: 0.27,
                5: 0.21,
                6: 0.28,
            },
            "late": {
                1: 0.07,
                2: 0.09,
                3: 0.14,
                4: 0.22,
                5: 0.18,
                6: 0.22,
            },
        },
        "pd": {
            "early": {
                1: 0.05,
                2: 0.08,
                3: 0.14,
                4: 0.24,
                5: 0.31,
                6: 0.38,
            },
            "late": {
                1: 0.04,
                2: 0.1,
                3: 0.12,
                4: 0.24,
                5: 0.35,
                6: 0.41,
            },
        },
    },
    "pre_emptive_transplant_live_donor_dist": {
        y: {"early": 0.49, "late": 0.07} for y in range(1, 14)
    },
    "pre_emptive_transplant_cadaver_donor_dist": {
        y: {"early": 0.22, "late": 0.05} for y in range(1, 14)
    },
}


# These are used for all the model runs regardless of geography
def load_time_to_event_curves(filepath):
    time_to_event_filepaths = get_time_to_event_curve_filepaths(filepath)
    time_to_event_curves = {
        filepath.stem: pd.read_csv(filepath, index_col=0)
        for filepath in time_to_event_filepaths
    }
    return time_to_event_curves
