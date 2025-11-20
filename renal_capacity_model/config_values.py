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
    "time_on_waiting_list_mean": {
        y: {
            "live": 4.5 * 30,  # 3-6 months on average
            "cadaver": 365 * 2.5 * 30,  # 2-3 years on average
        }
        for y in range(1, 14)
    },
}

# These are used for all the model runs regardless of geography
time_to_event_distribution_parameters = {
    "ttma_initial_distribution": {
        "ichd": {
            1: {
                "proportion_uncensored": 0.86,
                "shape": 0.96,
                "scale": 859,
            },
            2: {
                "proportion_uncensored": 0.75,
                "shape": 1.01,
                "scale": 762,
            },
            3: {
                "proportion_uncensored": 0.78,
                "shape": 0.97,
                "scale": 644,
            },
            4: {
                "proportion_uncensored": 0.78,
                "shape": 0.91,
                "scale": 569,
            },
            5: {
                "proportion_uncensored": 0.79,
                "shape": 0.95,
                "scale": 464,
            },
            6: {
                "proportion_uncensored": 0.87,
                "shape": 1.08,
                "scale": 453,
            },
        },
        "hhd": {
            1: {
                "proportion_uncensored": 0.68,
                "shape": 0.92,
                "scale": 794,
            },
            2: {
                "proportion_uncensored": 0.86,
                "shape": 0.92,
                "scale": 794,
            },
            3: {
                "proportion_uncensored": 0.92,
                "shape": 0.92,
                "scale": 794,
            },
            4: {
                "proportion_uncensored": 0.94,
                "shape": 0.92,
                "scale": 794,
            },
            5: {
                "proportion_uncensored": 1.00,
                "shape": 0.92,
                "scale": 794,
            },
            6: {
                "proportion_uncensored": 1.00,
                "shape": 0.92,
                "scale": 794,
            },
        },
        "pd": {
            1: {
                "proportion_uncensored": 1.00,
                "shape": 0.84,
                "scale": 553,
            },
            2: {
                "proportion_uncensored": 1.00,
                "shape": 0.92,
                "scale": 645,
            },
            3: {
                "proportion_uncensored": 1.00,
                "shape": 0.96,
                "scale": 647,
            },
            4: {
                "proportion_uncensored": 0.99,
                "shape": 0.98,
                "scale": 665,
            },
            5: {
                "proportion_uncensored": 1.00,
                "shape": 1.03,
                "scale": 702,
            },
            6: {
                "proportion_uncensored": 1.00,
                "shape": 1.07,
                "scale": 612,
            },
        },
    },
    "ttd_initial_distribution": {
        "ichd": {
            1: {
                "proportion_uncensored": 0.85,
                "shape": 1.02,
                "scale": 1441,
            },
            2: {
                "proportion_uncensored": 0.85,
                "shape": 1.02,
                "scale": 1441,
            },
            3: {
                "proportion_uncensored": 0.92,
                "shape": 1.04,
                "scale": 1378,
            },
            4: {
                "proportion_uncensored": 0.96,
                "shape": 1.06,
                "scale": 1305,
            },
            5: {
                "proportion_uncensored": 0.99,
                "shape": 1.08,
                "scale": 1241,
            },
            6: {
                "proportion_uncensored": 1.00,
                "shape": 1.10,
                "scale": 1148,
            },
        },
        "hhd": {
            1: {
                "proportion_uncensored": 0.3,
                "shape": 1.09,
                "scale": 1456,
            },
            2: {
                "proportion_uncensored": 0.57,
                "shape": 1.09,
                "scale": 1456,
            },
            3: {
                "proportion_uncensored": 0.83,
                "shape": 1.09,
                "scale": 1456,
            },
            4: {
                "proportion_uncensored": 0.91,
                "shape": 1.09,
                "scale": 1456,
            },
            5: {
                "proportion_uncensored": 1.00,
                "shape": 1.09,
                "scale": 1456,
            },
            6: {
                "proportion_uncensored": 1.00,
                "shape": 1.09,
                "scale": 1456,
            },
        },
        "pd": {
            1: {
                "proportion_uncensored": 1.00,
                "shape": 0.72,
                "scale": 543,
            },
            2: {
                "proportion_uncensored": 1.00,
                "shape": 0.72,
                "scale": 543,
            },
            3: {
                "proportion_uncensored": 0.98,
                "shape": 1.14,
                "scale": 629,
            },
            4: {
                "proportion_uncensored": 0.98,
                "shape": 1.05,
                "scale": 780,
            },
            5: {
                "proportion_uncensored": 1.00,
                "shape": 1.07,
                "scale": 801,
            },
            6: {
                "proportion_uncensored": 1.00,
                "shape": 1.07,
                "scale": 915,
            },
        },
    },
    "ttd_tx_initial_distribution": {
        "live": {
            1: {
                "proportion_uncensored": 0.08,
                "lower_bound": 0,
                "upper_bound": None,  # sim duration
            },
            2: {
                "proportion_uncensored": 0.16,
                "lower_bound": 0,
                "upper_bound": None,
            },
            3: {
                "proportion_uncensored": 0.27,
                "lower_bound": 0,
                "upper_bound": None,
            },
            4: {
                "proportion_uncensored": 0.43,
                "lower_bound": 0,
                "upper_bound": None,
            },
            5: {
                "proportion_uncensored": 0.73,
                "lower_bound": 0,
                "upper_bound": None,
            },
            6: {
                "proportion_uncensored": 0.95,
                "lower_bound": 0,
                "upper_bound": None,
            },
        },
        "cadaver": {
            1: {
                "proportion_uncensored": 0.1,
                "lower_bound": 0,
                "upper_bound": None,
            },
            2: {
                "proportion_uncensored": 0.22,
                "lower_bound": 0,
                "upper_bound": None,
            },
            3: {
                "proportion_uncensored": 0.35,
                "lower_bound": 0,
                "upper_bound": None,
            },
            4: {
                "proportion_uncensored": 0.59,
                "lower_bound": 0,
                "upper_bound": None,
            },
            5: {
                "proportion_uncensored": 0.84,
                "lower_bound": 0,
                "upper_bound": None,
            },
            6: {
                "proportion_uncensored": 0.96,
                "lower_bound": 0,
                "upper_bound": None,
            },
        },
    },
    "ttgf_tx_initial_distribution": {
        "live": {
            1: {
                "proportion_uncensored": 0.54,
                "shape": 1.18,
                "scale": 1960,
            },
            2: {
                "proportion_uncensored": 0.45,
                "shape": 1.15,
                "scale": 1930,
            },
            3: {
                "proportion_uncensored": 0.4,
                "shape": 1.21,
                "scale": 2088,
            },
            4: {
                "proportion_uncensored": 0.43,
                "shape": 1.12,
                "scale": 1802,
            },
            5: {
                "proportion_uncensored": 0.58,
                "shape": 1.2,
                "scale": 1920,
            },
            6: {
                "proportion_uncensored": 0.8,
                "shape": 1.2,
                "scale": 1920,
            },
        },
        "cadaver": {
            1: {
                "proportion_uncensored": 0.54,
                "shape": 1.17,
                "scale": 1892,
            },
            2: {
                "proportion_uncensored": 0.5,
                "shape": 1.11,
                "scale": 1864,
            },
            3: {
                "proportion_uncensored": 0.48,
                "shape": 1.24,
                "scale": 1934,
            },
            4: {
                "proportion_uncensored": 0.53,
                "shape": 1.22,
                "scale": 1868,
            },
            5: {
                "proportion_uncensored": 0.69,
                "shape": 1.23,
                "scale": 1881,
            },
            6: {
                "proportion_uncensored": 0.83,
                "shape": 1.27,
                "scale": 2021,
            },
        },
    },
    "ttd_con_care": {
        "shape": 0.5,
        "scale": 100,
    },
    "tw_before_dialysis": {
        "shape": 1,
        "scale": 90,
    },
    "ttd_distribution": {
        "ichd": {
            1: {
                "shape": 0.76,
                "scale": 1 / 0.001,
            },
            2: {
                "shape": 0.66,
                "scale": 1 / 0.0005,
            },
            3: {
                "shape": 0.68,
                "scale": 1 / 0.0005,
            },
            4: {
                "shape": 0.67,
                "scale": 1 / 0.0005,
            },
            5: {
                "shape": 0.76,
                "scale": 1 / 0.001,
            },
            6: {
                "shape": 0.67,
                "scale": 1 / 0.0004,
            },
        },
        "hhd": {
            1: {
                "shape": 0.58,
                "scale": 1 / 0.000001,
            },
            2: {
                "shape": 0.58,
                "scale": 1 / 0.000001,
            },
            3: {
                "shape": 0.58,
                "scale": 1 / 0.000001,
            },
            4: {
                "shape": 0.58,
                "scale": 1 / 0.000001,
            },
            5: {
                "shape": 0.58,
                "scale": 1 / 0.000001,
            },
            6: {
                "shape": 0.58,
                "scale": 1 / 0.000001,
            },
        },
        "pd": {
            1: {
                "shape": 0.9,
                "scale": 1 / 0.0008,
            },
            2: {
                "shape": 0.85,
                "scale": 1 / 0.0008,
            },
            3: {
                "shape": 0.87,
                "scale": 1 / 0.0008,
            },
            4: {
                "shape": 0.9,
                "scale": 1 / 0.0009,
            },
            5: {
                "shape": 0.92,
                "scale": 1 / 0.0009,
            },
            6: {
                "shape": 0.89,
                "scale": 1 / 0.0008,
            },
        },
    },
    "ttma_distribution": {
        "ichd": {
            1: {
                "shape": 0.47,
                "scale": 1 / 0.0009,
            },
            2: {
                "shape": 0.51,
                "scale": 1 / 0.001,
            },
            3: {
                "shape": 0.51,
                "scale": 1 / 0.0009,
            },
            4: {
                "shape": 0.55,
                "scale": 1 / 0.0009,
            },
            5: {
                "shape": 0.6,
                "scale": 1 / 0.0009,
            },
            6: {
                "shape": 0.6,
                "scale": 1 / 0.0009,
            },
        },
        "hhd": {
            1: {
                "shape": 0.56,
                "scale": 1 / 0.001,
            },
            2: {
                "shape": 0.51,
                "scale": 1 / 0.001,
            },
            3: {
                "shape": 0.6,
                "scale": 1 / 0.001,
            },
            4: {
                "shape": 0.57,
                "scale": 1 / 0.0008,
            },
            5: {
                "shape": 0.58,
                "scale": 1 / 0.001,
            },
            6: {
                "shape": 0.54,
                "scale": 1 / 0.001,
            },
        },
        "pd": {
            1: {
                "shape": 0.86,
                "scale": 1 / 0.002,
            },
            2: {
                "shape": 0.82,
                "scale": 1 / 0.002,
            },
            3: {
                "shape": 0.81,
                "scale": 1 / 0.002,
            },
            4: {
                "shape": 0.89,
                "scale": 1 / 0.002,
            },
            5: {
                "shape": 0.87,
                "scale": 1 / 0.002,
            },
            6: {
                "shape": 0.88,
                "scale": 1 / 0.002,
            },
        },
    },
    "ttd_tx_distribution": {
        "live": {
            1: {
                "shape": 0.99,
                "scale": 25138,
            },
            2: {
                "shape": 0.99,
                "scale": 25138,
            },
            3: {
                "shape": 0.99,
                "scale": 25138,
            },
            4: {
                "shape": 1.21,
                "scale": 7077,
            },
            5: {
                "shape": 1.41,
                "scale": 4462,
            },
            6: {
                "shape": 1.41,
                "scale": 4462,
            },
        },
        "cadaver": {
            1: {
                "shape": 0.98,
                "scale": 14777,
            },
            2: {
                "shape": 0.98,
                "scale": 14777,
            },
            3: {
                "shape": 1.04,
                "scale": 6837,
            },
            4: {
                "shape": 1,
                "scale": 4830,
            },
            5: {
                "shape": 1.01,
                "scale": 3938,
            },
            6: {
                "shape": 0.95,
                "scale": 3521,
            },
        },
    },
    "ttgf_tx_distribution": {
        "live": {
            1: {
                "break_point": 365 / 12,
                "mode": 7,
                "proportion_below_break": 0.2,
                "shape": 0.5,
                "scale": 4977,
            },
            2: {
                "break_point": 365 / 12,
                "mode": 7,
                "proportion_below_break": 0.2,
                "shape": 0.5,
                "scale": 4977,
            },
            3: {
                "break_point": 365 / 12,
                "mode": 7,
                "proportion_below_break": 0.2,
                "shape": 0.5,
                "scale": 4977,
            },
            4: {
                "break_point": 365 / 12,
                "mode": 7,
                "proportion_below_break": 0.2,
                "shape": 0.5,
                "scale": 4977,
            },
            5: {
                "break_point": 365 / 12,
                "mode": 7,
                "proportion_below_break": 0.2,
                "shape": 0.5,
                "scale": 4977,
            },
            6: {
                "break_point": 365 / 12,
                "mode": 7,
                "proportion_below_break": 0.2,
                "shape": 0.5,
                "scale": 4977,
            },
        },
        "cadaver": {
            1: {
                "break_point": 365 / 12,
                "mode": 1,
                "proportion_below_break": 0.24,
                "shape": 0.54,
                "scale": 2547,
            },
            2: {
                "break_point": 365 / 12,
                "mode": 1,
                "proportion_below_break": 0.24,
                "shape": 0.54,
                "scale": 2547,
            },
            3: {
                "break_point": 365 / 12,
                "mode": 1,
                "proportion_below_break": 0.24,
                "shape": 0.54,
                "scale": 2547,
            },
            4: {
                "break_point": 365 / 12,
                "mode": 1,
                "proportion_below_break": 0.24,
                "shape": 0.54,
                "scale": 2547,
            },
            5: {
                "break_point": 365 / 12,
                "mode": 1,
                "proportion_below_break": 0.24,
                "shape": 0.54,
                "scale": 2547,
            },
            6: {
                "break_point": 365 / 12,
                "mode": 1,
                "proportion_below_break": 0.24,
                "shape": 0.54,
                "scale": 2547,
            },
        },
    },
}
