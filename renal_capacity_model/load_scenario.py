"""
This module contains the code needed to load in a scenario from an excel file and convert it to
dictionaries as required by the config.

This will be used optionally, triggered by the user passing an excel file path as a parameter.
"""

import pandas as pd


def load_scenario_from_excel(
    filepath: str = "data/Renal_Modelling_Input_file.xlsx", validation: bool = False
) -> dict:
    """Loads config for a model run from input Excel file

    Args:
        filepath (str, optional): Path to input Excel file. Defaults to "data/Renal_Modelling_Input_file.xlsx".
        validation (bool, optional): Whether to load validation or experimental values from Excel file. Defaults to False, which is the experimental values.

    Returns:
        dict: Values to be passed to Config class
    """
    config_from_excel = {}
    input_scenario = pd.read_excel(
        filepath,
        sheet_name="simPy_sheet",
    )

    if validation:
        config_from_excel["arrival_rate"] = {
            1: input_scenario.iat[3, 1],
            2: input_scenario.iat[3, 2],
            3: input_scenario.iat[3, 3],
            4: input_scenario.iat[3, 4],
            5: input_scenario.iat[3, 5],
            6: input_scenario.iat[3, 6],
            7: input_scenario.iat[3, 7],
            8: input_scenario.iat[3, 8],
            9: input_scenario.iat[3, 9],
            10: input_scenario.iat[3, 10],
            11: input_scenario.iat[3, 11],
            12: input_scenario.iat[3, 12],
            13: input_scenario.iat[3, 13],
        }
        config_from_excel["prevalent_counts"] = {
            "conservative_care": {
                "1_early": input_scenario.iat[128, 2],
                "2_early": input_scenario.iat[129, 2],
                "3_early": input_scenario.iat[130, 2],
                "4_early": input_scenario.iat[131, 2],
                "5_early": input_scenario.iat[132, 2],
                "6_early": input_scenario.iat[133, 2],
                "1_late": input_scenario.iat[134, 2],
                "2_late": input_scenario.iat[135, 2],
                "3_late": input_scenario.iat[136, 2],
                "4_late": input_scenario.iat[137, 2],
                "5_late": input_scenario.iat[138, 2],
                "6_late": input_scenario.iat[139, 2],
            },
            "ichd": {
                "1_early": input_scenario.iat[142, 2],
                "2_early": input_scenario.iat[143, 2],
                "3_early": input_scenario.iat[144, 2],
                "4_early": input_scenario.iat[145, 2],
                "5_early": input_scenario.iat[146, 2],
                "6_early": input_scenario.iat[147, 2],
                "1_late": input_scenario.iat[148, 2],
                "2_late": input_scenario.iat[149, 2],
                "3_late": input_scenario.iat[150, 2],
                "4_late": input_scenario.iat[151, 2],
                "5_late": input_scenario.iat[152, 2],
                "6_late": input_scenario.iat[153, 2],
            },
            "hhd": {
                "1_early": input_scenario.iat[156, 2],
                "2_early": input_scenario.iat[157, 2],
                "3_early": input_scenario.iat[158, 2],
                "4_early": input_scenario.iat[159, 2],
                "5_early": input_scenario.iat[160, 2],
                "6_early": input_scenario.iat[161, 2],
                "1_late": input_scenario.iat[162, 2],
                "2_late": input_scenario.iat[163, 2],
                "3_late": input_scenario.iat[164, 2],
                "4_late": input_scenario.iat[165, 2],
                "5_late": input_scenario.iat[166, 2],
                "6_late": input_scenario.iat[167, 2],
            },
            "pd": {
                "1_early": input_scenario.iat[170, 2],
                "2_early": input_scenario.iat[171, 2],
                "3_early": input_scenario.iat[172, 2],
                "4_early": input_scenario.iat[173, 2],
                "5_early": input_scenario.iat[174, 2],
                "6_early": input_scenario.iat[175, 2],
                "1_late": input_scenario.iat[176, 2],
                "2_late": input_scenario.iat[177, 2],
                "3_late": input_scenario.iat[178, 2],
                "4_late": input_scenario.iat[179, 2],
                "5_late": input_scenario.iat[180, 2],
                "6_late": input_scenario.iat[181, 2],
            },
            "live_transplant": {
                "1_early": input_scenario.iat[184, 2],
                "2_early": input_scenario.iat[185, 2],
                "3_early": input_scenario.iat[186, 2],
                "4_early": input_scenario.iat[187, 2],
                "5_early": input_scenario.iat[188, 2],
                "6_early": input_scenario.iat[189, 2],
                "1_late": input_scenario.iat[190, 2],
                "2_late": input_scenario.iat[191, 2],
                "3_late": input_scenario.iat[192, 2],
                "4_late": input_scenario.iat[193, 2],
                "5_late": input_scenario.iat[194, 2],
                "6_late": input_scenario.iat[195, 2],
            },
            "cadaver_transplant": {
                "1_early": input_scenario.iat[198, 2],
                "2_early": input_scenario.iat[199, 2],
                "3_early": input_scenario.iat[200, 2],
                "4_early": input_scenario.iat[201, 2],
                "5_early": input_scenario.iat[202, 2],
                "6_early": input_scenario.iat[203, 2],
                "1_late": input_scenario.iat[204, 2],
                "2_late": input_scenario.iat[205, 2],
                "3_late": input_scenario.iat[206, 2],
                "4_late": input_scenario.iat[207, 2],
                "5_late": input_scenario.iat[208, 2],
                "6_late": input_scenario.iat[209, 2],
            },
        }
    else:
        config_from_excel["arrival_rate"] = {
            1: input_scenario.iat[4, 1],
            2: input_scenario.iat[4, 2],
            3: input_scenario.iat[4, 3],
            4: input_scenario.iat[4, 4],
            5: input_scenario.iat[4, 5],
            6: input_scenario.iat[4, 6],
            7: input_scenario.iat[4, 7],
            8: input_scenario.iat[4, 8],
            9: input_scenario.iat[4, 9],
            10: input_scenario.iat[4, 10],
            11: input_scenario.iat[4, 11],
            12: input_scenario.iat[4, 12],
            13: input_scenario.iat[4, 13],
        }
        config_from_excel["prevalent_counts"] = {
            "conservative_care": {
                "1_early": input_scenario.iat[128, 3],
                "2_early": input_scenario.iat[129, 3],
                "3_early": input_scenario.iat[130, 3],
                "4_early": input_scenario.iat[131, 3],
                "5_early": input_scenario.iat[132, 3],
                "6_early": input_scenario.iat[133, 3],
                "1_late": input_scenario.iat[134, 3],
                "2_late": input_scenario.iat[135, 3],
                "3_late": input_scenario.iat[136, 3],
                "4_late": input_scenario.iat[137, 3],
                "5_late": input_scenario.iat[138, 3],
                "6_late": input_scenario.iat[139, 3],
            },
            "ichd": {
                "1_early": input_scenario.iat[142, 3],
                "2_early": input_scenario.iat[143, 3],
                "3_early": input_scenario.iat[144, 3],
                "4_early": input_scenario.iat[145, 3],
                "5_early": input_scenario.iat[146, 3],
                "6_early": input_scenario.iat[147, 3],
                "1_late": input_scenario.iat[148, 3],
                "2_late": input_scenario.iat[149, 3],
                "3_late": input_scenario.iat[150, 3],
                "4_late": input_scenario.iat[151, 3],
                "5_late": input_scenario.iat[152, 3],
                "6_late": input_scenario.iat[153, 3],
            },
            "hhd": {
                "1_early": input_scenario.iat[156, 3],
                "2_early": input_scenario.iat[157, 3],
                "3_early": input_scenario.iat[158, 3],
                "4_early": input_scenario.iat[159, 3],
                "5_early": input_scenario.iat[160, 3],
                "6_early": input_scenario.iat[161, 3],
                "1_late": input_scenario.iat[162, 3],
                "2_late": input_scenario.iat[163, 3],
                "3_late": input_scenario.iat[164, 3],
                "4_late": input_scenario.iat[165, 3],
                "5_late": input_scenario.iat[166, 3],
                "6_late": input_scenario.iat[167, 3],
            },
            "pd": {
                "1_early": input_scenario.iat[170, 3],
                "2_early": input_scenario.iat[171, 3],
                "3_early": input_scenario.iat[172, 3],
                "4_early": input_scenario.iat[173, 3],
                "5_early": input_scenario.iat[174, 3],
                "6_early": input_scenario.iat[175, 3],
                "1_late": input_scenario.iat[176, 3],
                "2_late": input_scenario.iat[177, 3],
                "3_late": input_scenario.iat[178, 3],
                "4_late": input_scenario.iat[179, 3],
                "5_late": input_scenario.iat[180, 3],
                "6_late": input_scenario.iat[181, 3],
            },
            "live_transplant": {
                "1_early": input_scenario.iat[184, 3],
                "2_early": input_scenario.iat[185, 3],
                "3_early": input_scenario.iat[186, 3],
                "4_early": input_scenario.iat[187, 3],
                "5_early": input_scenario.iat[188, 3],
                "6_early": input_scenario.iat[189, 3],
                "1_late": input_scenario.iat[190, 3],
                "2_late": input_scenario.iat[191, 3],
                "3_late": input_scenario.iat[192, 3],
                "4_late": input_scenario.iat[193, 3],
                "5_late": input_scenario.iat[194, 3],
                "6_late": input_scenario.iat[195, 3],
            },
            "cadaver_transplant": {
                "1_early": input_scenario.iat[198, 3],
                "2_early": input_scenario.iat[199, 3],
                "3_early": input_scenario.iat[200, 3],
                "4_early": input_scenario.iat[201, 3],
                "5_early": input_scenario.iat[202, 3],
                "6_early": input_scenario.iat[203, 3],
                "1_late": input_scenario.iat[204, 3],
                "2_late": input_scenario.iat[205, 3],
                "3_late": input_scenario.iat[206, 3],
                "4_late": input_scenario.iat[207, 3],
                "5_late": input_scenario.iat[208, 3],
                "6_late": input_scenario.iat[209, 3],
            },
        }
    # The config values below this point are not different between validation and experimentation
    config_from_excel["sim_duration"] = input_scenario.iat[0, 1]
    config_from_excel["age_dist"] = {
        1: input_scenario.iat[6, 1],
        2: input_scenario.iat[6, 2],
        3: input_scenario.iat[6, 3],
        4: input_scenario.iat[6, 4],
        5: input_scenario.iat[6, 5],
        6: input_scenario.iat[6, 6],
    }

    config_from_excel["referral_dist"] = {
        "early": input_scenario.iat[9, 1],
        "late": input_scenario.iat[10, 1],
    }

    config_from_excel["con_care_dist"] = {
        1: input_scenario.iat[19, 1],
        2: input_scenario.iat[20, 1],
        3: input_scenario.iat[21, 1],
        4: input_scenario.iat[22, 1],
        5: input_scenario.iat[23, 1],
        6: input_scenario.iat[24, 1],
    }

    config_from_excel["suitable_for_transplant_dist"] = {
        1: input_scenario.iat[47, 1],
        2: input_scenario.iat[48, 1],
        3: input_scenario.iat[49, 1],
        4: input_scenario.iat[50, 1],
        5: input_scenario.iat[51, 1],
        6: input_scenario.iat[52, 1],
    }
    config_from_excel["transplant_type_dist"] = {
        1: input_scenario.iat[95, 1],
        2: input_scenario.iat[96, 1],
        3: input_scenario.iat[97, 1],
        4: input_scenario.iat[98, 1],
        5: input_scenario.iat[99, 1],
        6: input_scenario.iat[100, 1],
    }
    config_from_excel["modality_allocation_distributions"] = {
        "none": {
            "ichd": input_scenario.iat[69, 5],
            "hhd": input_scenario.iat[69, 6],
            "pd": input_scenario.iat[69, 7],
        },
        "ichd": {
            "ichd": input_scenario.iat[75, 2],
            "hhd": input_scenario.iat[75, 3],
            "pd": input_scenario.iat[75, 4],
        },
        "hhd": {
            "ichd": input_scenario.iat[81, 2],
            "hhd": input_scenario.iat[81, 3],
            "pd": input_scenario.iat[81, 4],
        },
        "pd": {
            "ichd": input_scenario.iat[87, 2],
            "hhd": input_scenario.iat[87, 3],
            "pd": input_scenario.iat[87, 4],
        },
    }
    config_from_excel["death_post_transplant"] = {
        "live": {
            1: input_scenario.iat[119, 3],
            2: input_scenario.iat[120, 3],
            3: input_scenario.iat[121, 3],
            4: input_scenario.iat[122, 3],
            5: input_scenario.iat[123, 3],
            6: input_scenario.iat[124, 3],
        },
        "cadaver": {
            1: input_scenario.iat[119, 2],
            2: input_scenario.iat[120, 2],
            3: input_scenario.iat[121, 2],
            4: input_scenario.iat[122, 2],
            5: input_scenario.iat[123, 2],
            6: input_scenario.iat[124, 2],
        },
    }
    config_from_excel["death_post_dialysis_modality"] = {
        "ichd": {
            "early": {
                1: input_scenario.iat[104, 2],
                2: input_scenario.iat[105, 2],
                3: input_scenario.iat[106, 2],
                4: input_scenario.iat[107, 2],
                5: input_scenario.iat[108, 2],
                6: input_scenario.iat[109, 2],
            },
            "late": {
                1: input_scenario.iat[110, 2],
                2: input_scenario.iat[111, 2],
                3: input_scenario.iat[112, 2],
                4: input_scenario.iat[113, 2],
                5: input_scenario.iat[114, 2],
                6: input_scenario.iat[115, 2],
            },
        },
        "hhd": {
            "early": {
                1: input_scenario.iat[104, 3],
                2: input_scenario.iat[105, 3],
                3: input_scenario.iat[106, 3],
                4: input_scenario.iat[107, 3],
                5: input_scenario.iat[108, 3],
                6: input_scenario.iat[109, 3],
            },
            "late": {
                1: input_scenario.iat[110, 3],
                2: input_scenario.iat[111, 3],
                3: input_scenario.iat[112, 3],
                4: input_scenario.iat[113, 3],
                5: input_scenario.iat[114, 3],
                6: input_scenario.iat[115, 3],
            },
        },
        "pd": {
            "early": {
                1: input_scenario.iat[104, 4],
                2: input_scenario.iat[105, 4],
                3: input_scenario.iat[106, 4],
                4: input_scenario.iat[107, 4],
                5: input_scenario.iat[108, 4],
                6: input_scenario.iat[109, 4],
            },
            "late": {
                1: input_scenario.iat[110, 4],
                2: input_scenario.iat[111, 4],
                3: input_scenario.iat[112, 4],
                4: input_scenario.iat[113, 4],
                5: input_scenario.iat[114, 4],
                6: input_scenario.iat[115, 4],
            },
        },
    }
    config_from_excel["pre_emptive_transplant_live_donor_dist"] = {
        "early": input_scenario.iat[55, 18],
        "late": input_scenario.iat[61, 18],
    }
    config_from_excel["pre_emptive_transplant_cadaver_donor_dist"] = {
        "early": input_scenario.iat[55, 2],
        "late": input_scenario.iat[61, 2],
    }
    config_from_excel["time_on_waiting_list_mean"] = {
        "live": input_scenario.iat[29, 2],
        "cadaver": input_scenario.iat[30, 2],
    }
    config_from_excel["daily_costs"] = {
        "ichd": input_scenario.iat[36, 1],
        "hhd": input_scenario.iat[37, 1],
        "pd": input_scenario.iat[38, 1],
        "living_with_transplant": input_scenario.iat[39, 1],
    }

    return config_from_excel
