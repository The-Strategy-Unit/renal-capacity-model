"""
This module stores National config values and time to event values that are used
regardless of model geography
"""

import pandas as pd
from renal_capacity_model.utils import get_time_to_event_curve_filepaths, get_logger
from renal_capacity_model.helpers import check_time_to_event_curve_dfs

logger = get_logger(__name__)

national_config_dict = {
    "region": {"England"},
    "centre": {"All"},
    "multipliers": {
        "ttd": {
            "inc": 1,
            "prev": 1,
        },
        "ttma": {
            "inc": {
                "ichd": 1,
                "hhd": 1,
                "pd": 1,
            },
            "prev": {
                "ichd": 1,
                "hhd": 1,
                "pd": 1,
            },
        },
        "ttgf": {
            "inc": {
                "live": 1,
                "cadaver": 1,
            },
            "prev": {
                "live": 1,
                "cadaver": 1,
            },
        },
        "tw": {
            "inc": {
                "live": 1,
                "cadaver": 1,
            },
            "prev": {
                "live": 1,
                "cadaver": 1,
            },
        },
    },
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
    "age_dist": {  ## adjusted for con-care patient inflow
        1: 0.05,
        2: 0.06,
        3: 0.11,
        4: 0.15,
        5: 0.24,
        6: 0.39,
    },
    "referral_dist": {"early": 0.82, "late": 0.18},
    "con_care_dist": {
        y: {1: 0.1, 2: 0.1, 3: 0.1, 4: 0.1, 5: 0.25, 6: 0.5} for y in range(1, 14)
    },
    "suitable_for_transplant_dist": {
        "inc": {
            1: 0.88,
            2: 0.83,
            3: 0.73,
            4: 0.56,
            5: 0.30,
            6: 0.05,
        },
        "prev": {
            1: 0.88,
            2: 0.83,
            3: 0.73,
            4: 0.56,
            5: 0.30,
            6: 0.05,
        },
    },
    "receives_transplant_dist": {
        y: {
            "inc": {
                1: 0.88,
                2: 0.83,
                3: 0.73,
                4: 0.56,
                5: 0.30,
                6: 0.05,
            },
            "prev": {
                1: 0.88,
                2: 0.83,
                3: 0.73,
                4: 0.56,
                5: 0.30,
                6: 0.05,
            },
        }
        for y in range(1, 14)
    },
    "transplant_type_dist": {
        "inc": {
            1: 0.4,
            2: 0.3,
            3: 0.26,
            4: 0.23,
            5: 0.19,
            6: 0.12,
        },
        "prev": {
            1: 0.4,
            2: 0.3,
            3: 0.26,
            4: 0.23,
            5: 0.19,
            6: 0.12,
        },
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
    "pre_emptive_transplant_live_donor_dist": {
        y: {"early": 0.49, "late": 0.07} for y in range(1, 14)
    },
    "pre_emptive_transplant_cadaver_donor_dist": {
        y: {"early": 0.22, "late": 0.05} for y in range(1, 14)
    },
    "daily_costs": {
        "ichd": 62842 / 365,
        "hhd": 51122 / 365,
        "pd": 39391 / 365,
        "transplant": 9005 / 365,
    },
}

# Time to death: conservative care
ttd_con_care_values = {
    "shape": 0.5,
    "scale": 100,
}

ttd_krt_values = {  ## weibull shape and scale parameters
    "initialisation": {
        "not_listed": {
            "early": {
                1: {"shape": 0.926963321, "scale": 2127.231053},
                2: {"shape": 1.102888443, "scale": 2360.960064},
                3: {"shape": 1.042024424, "scale": 1757.881403},
                4: {"shape": 1.102673686, "scale": 1641.614239},
                5: {"shape": 1.149855608, "scale": 1561.636782},
                6: {"shape": 1.151814597, "scale": 1190.40286},
            },
            "late": {
                1: {"shape": 1.099732869, "scale": 4314.8445},
                2: {"shape": 1.239811029, "scale": 2204.356655},
                3: {"shape": 1.025879638, "scale": 1940.947327},
                4: {"shape": 1.17279732, "scale": 1700.235305},
                5: {"shape": 1.168619527, "scale": 1512.312581},
                6: {"shape": 1.156286321, "scale": 1253.912137},
            },
        },
        "listed": {
            "early": {
                1: {"shape": 1.426589565, "scale": 13064.21921},
                2: {"shape": 1.501319694, "scale": 8229.734667},
                3: {"shape": 1.475457685, "scale": 6126.819295},
                4: {"shape": 1.388640715, "scale": 4221.17834},
                5: {"shape": 1.381583619, "scale": 2805.868318},
                6: {"shape": 1.262968437, "scale": 1862.925138},
            },
            "late": {
                1: {"shape": 1.403897083, "scale": 13250.96392},
                2: {"shape": 1.359190822, "scale": 8393.578341},
                3: {"shape": 1.435707658, "scale": 5981.108405},
                4: {"shape": 1.326446673, "scale": 4096.723314},
                5: {"shape": 1.469351223, "scale": 2905.94038},
                6: {"shape": 1.244780918, "scale": 1800.673553},
            },
        },
        "received_Tx": {
            "early": {
                1: {"shape": 1.945083614, "scale": 11291.09043},
                2: {"shape": 1.765333669, "scale": 8449.099418},
                3: {"shape": 1.750669869, "scale": 6535.672038},
                4: {"shape": 1.61142907, "scale": 4693.44361},
                5: {"shape": 1.51886545, "scale": 3189.62546},
                6: {"shape": 1.315655704, "scale": 2078.132622},
            },
            "late": {
                1: {"shape": 1.982364823, "scale": 10573.47681},
                2: {"shape": 1.658109448, "scale": 8611.590105},
                3: {"shape": 1.699130074, "scale": 6499.195977},
                4: {"shape": 1.491659213, "scale": 4669.1818},
                5: {"shape": 1.678178577, "scale": 3296.367133},
                6: {"shape": 1.306592647, "scale": 1990.733317},
            },
        },
    },
    "incidence": {
        "not_listed": {
            "early": {
                1: {"shape": 1.021124756, "scale": 1630.450226},
                2: {"shape": 1.033558934, "scale": 1601.726618},
                3: {"shape": 1.175150289, "scale": 1788.324784},
                4: {"shape": 1.171027698, "scale": 1671.61871},
                5: {"shape": 1.182843607, "scale": 1604.030346},
                6: {"shape": 1.111932566, "scale": 1324.708399},
            },
            "late": {
                1: {"shape": 1.025446743, "scale": 2098.5119},
                2: {"shape": 0.86558945, "scale": 2071.301577},
                3: {"shape": 0.787953011, "scale": 1428.187242},
                4: {"shape": 1.093861294, "scale": 1533.652413},
                5: {"shape": 0.817406992, "scale": 1170.501979},
                6: {"shape": 0.829891, "scale": 841.5931435},
            },
        },
        "listed": {
            "early": {
                1: {"shape": 1.76722409, "scale": 7565.454427},
                2: {"shape": 2.071602421, "scale": 5267.578147},
                3: {"shape": 1.842843082, "scale": 5294.787645},
                4: {"shape": 2.276835063, "scale": 3862.063689},
                5: {"shape": 1.990617668, "scale": 3148.737229},
                6: {"shape": 2.435166079, "scale": 2479.412332},
            },
            "late": {
                1: {"shape": 2.732803839, "scale": 5100.306997},
                2: {"shape": 1.7523112, "scale": 6999.685955},
                3: {"shape": 2.667855187, "scale": 3817.522327},
                4: {"shape": 2.39938038, "scale": 3728.91519},
                5: {"shape": 2.195794462, "scale": 2550.374846},
                6: {"shape": 2.435166079, "scale": 2479.412332},
            },
        },
        "received_Tx": {
            "early": {
                1: {"shape": 2.51486622, "scale": 6903.239543},
                2: {"shape": 3.159509376, "scale": 5391.985192},
                3: {"shape": 2.70710626, "scale": 5381.509481},
                4: {"shape": 2.893707823, "scale": 4282.49379},
                5: {"shape": 2.35276178, "scale": 3550.906294},
                6: {"shape": 4.316362639, "scale": 3118.52084},
            },
            "late": {
                1: {"shape": 3.160772244, "scale": 5169.606112},
                2: {"shape": 2.323615011, "scale": 7944.757158},
                3: {"shape": 3.8964386, "scale": 4637.1169},
                4: {"shape": 5.45663996, "scale": 3913.875032},
                5: {"shape": 3.071596253, "scale": 3120.115725},
                6: {"shape": 4.316362639, "scale": 3118.52084},
            },
        },
    },
}

tw_cadTx_values = {
    1: {"shape": 1.12, "scale": 719},
    2: {"shape": 1.23, "scale": 734},
    3: {"shape": 1.31, "scale": 794},
    4: {"shape": 1.31, "scale": 762},
    5: {"shape": 1.23, "scale": 619},
    6: {"shape": 1.02, "scale": 385},
}

tw_liveTx_values = {
    1: {"shape": 1.03, "scale": 399},
    2: {"shape": 1.06, "scale": 464},
    3: {"shape": 1.08, "scale": 417},
    4: {"shape": 1.09, "scale": 420},
    5: {"shape": 1.22, "scale": 391},
    6: {"shape": 1.01, "scale": 342},
}

tw_cadTx_initialisation_values = {
    1: {"shape": 1.12, "scale": 1336},
    2: {"shape": 1.13, "scale": 1163},
    3: {"shape": 1.22, "scale": 1194},
    4: {"shape": 1.26, "scale": 1023},
    5: {"shape": 1.28, "scale": 839},
    6: {"shape": 1.28, "scale": 409},
}

tw_liveTx_initialisation_values = {
    1: {"shape": 0.96, "scale": 752},
    2: {"shape": 1.05, "scale": 1006},
    3: {"shape": 0.96, "scale": 903},
    4: {"shape": 1.01, "scale": 665},
    5: {"shape": 1.27, "scale": 765},
    6: {"shape": 1.27, "scale": 765},
}

# Time waiting before dialysis
tw_before_dialysis_values = {
    "shape": 1,
    "scale": 90,
}


# These are used for all the model runs regardless of geography
def load_time_to_event_curves(filepath: str) -> dict[str, pd.DataFrame]:
    """Loads time to event curves from CSV files stored in a directory

    Args:
        filepath (str): Path to the directory containing the time to event curves

    Returns:
        dict: Dictionary where the keys are the names of the time to event variable,
        and the values are a DataFrame with the time to event distributions for each
        patient type
    """
    logger.info(f"Loading time to event curves from {filepath}")
    time_to_event_filepaths = get_time_to_event_curve_filepaths(filepath)
    time_to_event_curves = {
        filepath.stem: pd.read_csv(filepath, index_col=0)
        for filepath in time_to_event_filepaths
    }
    for name, df in time_to_event_curves.items():
        check_time_to_event_curve_dfs(name, df)
    return time_to_event_curves
