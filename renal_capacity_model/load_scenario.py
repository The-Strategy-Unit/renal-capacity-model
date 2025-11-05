"""
This module contains the code needed to load in a scenario from an excel file and convert it to
dictionaries as required by the config.

This will be used optionally, triggered by the user passing an excel file path as a parameter.
"""

import pandas as pd

input_scenario = pd.read_excel(
    "C:\\Users\\Lucy.Morgan\\Desktop\\Renal Modelling\\simPy model\\renal-capacity-model\\data\\Renal_Modelling_Input_File.xlsx",
    sheet_name="simPy_sheet",
)


class Scenario:
    """
    Scenario class for loading values
    """

    def __init__(self, scenario_dict={}):
        self.sim_duration = input_scenario.iat[0, 1]
        self.validation_arrival_rate = scenario_dict.get(
            "arrival_rate",
            {
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
            },
        )
        self.arrival_rate = scenario_dict.get(
            "arrival_rate",
            {
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
            },
        )
        self.prevalent_counts = scenario_dict.get(
            "prevalent_counts",
            {
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
            },
        )

        self.validation_config = scenario_dict.get(
            "prevalent_counts",
            {
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
            },
        )

        self.age_dist = scenario_dict.get(
            "age_dist",
            {
                1: input_scenario.iat[6, 1],
                2: input_scenario.iat[6, 2],
                3: input_scenario.iat[6, 3],
                4: input_scenario.iat[6, 4],
                5: input_scenario.iat[6, 5],
                6: input_scenario.iat[6, 6],
            },
        )
        self.referral_dist = scenario_dict.get(
            "referral_dist",
            {"early": input_scenario.iat[9, 1], "late": input_scenario.iat[9, 2]},
        )
        self.con_care_dist = scenario_dict.get(
            "con_care_dist",
            {
                1: {
                    1: input_scenario.iat[19, 1],
                    2: input_scenario.iat[20, 1],
                    3: input_scenario.iat[21, 1],
                    4: input_scenario.iat[22, 1],
                    5: input_scenario.iat[23, 1],
                    6: input_scenario.iat[24, 1],
                },
                2: {
                    1: input_scenario.iat[19, 2],
                    2: input_scenario.iat[20, 2],
                    3: input_scenario.iat[21, 2],
                    4: input_scenario.iat[22, 2],
                    5: input_scenario.iat[23, 2],
                    6: input_scenario.iat[24, 2],
                },
                3: {
                    1: input_scenario.iat[19, 3],
                    2: input_scenario.iat[20, 3],
                    3: input_scenario.iat[21, 3],
                    4: input_scenario.iat[22, 3],
                    5: input_scenario.iat[23, 3],
                    6: input_scenario.iat[24, 3],
                },
                4: {
                    1: input_scenario.iat[19, 4],
                    2: input_scenario.iat[20, 4],
                    3: input_scenario.iat[21, 4],
                    4: input_scenario.iat[22, 4],
                    5: input_scenario.iat[23, 4],
                    6: input_scenario.iat[24, 4],
                },
                5: {
                    1: input_scenario.iat[19, 5],
                    2: input_scenario.iat[20, 5],
                    3: input_scenario.iat[21, 5],
                    4: input_scenario.iat[22, 5],
                    5: input_scenario.iat[23, 5],
                    6: input_scenario.iat[24, 5],
                },
                6: {
                    1: input_scenario.iat[19, 6],
                    2: input_scenario.iat[20, 6],
                    3: input_scenario.iat[21, 6],
                    4: input_scenario.iat[22, 6],
                    5: input_scenario.iat[23, 6],
                    6: input_scenario.iat[24, 6],
                },
                7: {
                    1: input_scenario.iat[19, 7],
                    2: input_scenario.iat[20, 7],
                    3: input_scenario.iat[21, 7],
                    4: input_scenario.iat[22, 7],
                    5: input_scenario.iat[23, 7],
                    6: input_scenario.iat[24, 7],
                },
                8: {
                    1: input_scenario.iat[19, 8],
                    2: input_scenario.iat[20, 8],
                    3: input_scenario.iat[21, 8],
                    4: input_scenario.iat[22, 8],
                    5: input_scenario.iat[23, 8],
                    6: input_scenario.iat[24, 8],
                },
                9: {
                    1: input_scenario.iat[19, 9],
                    2: input_scenario.iat[20, 9],
                    3: input_scenario.iat[21, 9],
                    4: input_scenario.iat[22, 9],
                    5: input_scenario.iat[23, 9],
                    6: input_scenario.iat[24, 9],
                },
                10: {
                    1: input_scenario.iat[19, 10],
                    2: input_scenario.iat[20, 10],
                    3: input_scenario.iat[21, 10],
                    4: input_scenario.iat[22, 10],
                    5: input_scenario.iat[23, 10],
                    6: input_scenario.iat[24, 10],
                },
                11: {
                    1: input_scenario.iat[19, 11],
                    2: input_scenario.iat[20, 11],
                    3: input_scenario.iat[21, 11],
                    4: input_scenario.iat[22, 11],
                    5: input_scenario.iat[23, 11],
                    6: input_scenario.iat[24, 11],
                },
                12: {
                    1: input_scenario.iat[19, 12],
                    2: input_scenario.iat[20, 12],
                    3: input_scenario.iat[21, 12],
                    4: input_scenario.iat[22, 12],
                    5: input_scenario.iat[23, 12],
                    6: input_scenario.iat[24, 12],
                },
                13: {
                    1: input_scenario.iat[19, 13],
                    2: input_scenario.iat[20, 13],
                    3: input_scenario.iat[21, 13],
                    4: input_scenario.iat[22, 13],
                    5: input_scenario.iat[23, 13],
                    6: input_scenario.iat[24, 13],
                },
            },
        )
        self.suitable_for_transplant_dist = scenario_dict.get(
            "suitable_for_transplant_dist",
            {
                1: input_scenario.iat[47, 1],
                2: input_scenario.iat[48, 1],
                3: input_scenario.iat[49, 1],
                4: input_scenario.iat[50, 1],
                5: input_scenario.iat[51, 1],
                6: input_scenario.iat[52, 1],
            },
        )
        self.transplant_type_dist = scenario_dict.get(
            "transplant_type_dist",
            {
                1: input_scenario.iat[95, 1],
                2: input_scenario.iat[96, 1],
                3: input_scenario.iat[97, 1],
                4: input_scenario.iat[98, 1],
                5: input_scenario.iat[99, 1],
                6: input_scenario.iat[100, 1],
            },
        )
        self.modality_allocation_distributions = scenario_dict.get(
            "modality_allocation_distributions",
            {
                1: {  # year
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
                },
                2: {  # year
                    "none": {
                        "ichd": input_scenario.iat[69, 8],
                        "hhd": input_scenario.iat[69, 9],
                        "pd": input_scenario.iat[69, 10],
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
                },
                3: {  # year
                    "none": {
                        "ichd": input_scenario.iat[69, 11],
                        "hhd": input_scenario.iat[69, 12],
                        "pd": input_scenario.iat[69, 13],
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
                    4: {  # year
                        "none": {
                            "ichd": input_scenario.iat[69, 14],
                            "hhd": input_scenario.iat[69, 15],
                            "pd": input_scenario.iat[69, 16],
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
                    },
                    5: {  # year
                        "none": {
                            "ichd": input_scenario.iat[69, 17],
                            "hhd": input_scenario.iat[69, 18],
                            "pd": input_scenario.iat[69, 19],
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
                    },
                    6: {  # year
                        "none": {
                            "ichd": input_scenario.iat[69, 20],
                            "hhd": input_scenario.iat[69, 21],
                            "pd": input_scenario.iat[69, 22],
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
                    },
                    7: {  # year
                        "none": {
                            "ichd": input_scenario.iat[69, 23],
                            "hhd": input_scenario.iat[69, 24],
                            "pd": input_scenario.iat[69, 25],
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
                    },
                    8: {  # year
                        "none": {
                            "ichd": input_scenario.iat[69, 26],
                            "hhd": input_scenario.iat[69, 27],
                            "pd": input_scenario.iat[69, 28],
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
                    },
                    9: {  # year
                        "none": {
                            "ichd": input_scenario.iat[69, 29],
                            "hhd": input_scenario.iat[69, 30],
                            "pd": input_scenario.iat[69, 31],
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
                    },
                    10: {  # year
                        "none": {
                            "ichd": input_scenario.iat[69, 32],
                            "hhd": input_scenario.iat[69, 33],
                            "pd": input_scenario.iat[69, 34],
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
                    },
                    11: {  # year
                        "none": {
                            "ichd": input_scenario.iat[69, 35],
                            "hhd": input_scenario.iat[69, 36],
                            "pd": input_scenario.iat[69, 37],
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
                    },
                    12: {  # year
                        "none": {
                            "ichd": input_scenario.iat[69, 38],
                            "hhd": input_scenario.iat[69, 39],
                            "pd": input_scenario.iat[69, 40],
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
                    },
                    13: {  # year
                        "none": {
                            "ichd": input_scenario.iat[69, 41],
                            "hhd": input_scenario.iat[69, 42],
                            "pd": input_scenario.iat[69, 43],
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
                    },
                },
            },
        )
        self.death_post_transplant = scenario_dict.get(
            "death_post_transplant",
            {
                "live": input_scenario.iat[119, 3],
                "cadaver": input_scenario.iat[119, 2],
            },
        )
        self.death_post_dialysis_modality = scenario_dict.get(
            "death_post_dialysis_modality",
            {
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
            },
        )
        self.pre_emptive_transplant_live_donor_dist = scenario_dict.get(
            "pre_emptive_transplant_live_donor_dist",
            {
                1: {
                    "early": input_scenario.iat[55, 18],
                    "late": input_scenario.iat[61, 18],
                },
                2: {
                    "early": input_scenario.iat[55, 19],
                    "late": input_scenario.iat[61, 18],
                },
                3: {
                    "early": input_scenario.iat[55, 20],
                    "late": input_scenario.iat[61, 18],
                },
                4: {
                    "early": input_scenario.iat[55, 21],
                    "late": input_scenario.iat[61, 18],
                },
                5: {
                    "early": input_scenario.iat[55, 22],
                    "late": input_scenario.iat[61, 18],
                },
                6: {
                    "early": input_scenario.iat[55, 23],
                    "late": input_scenario.iat[61, 18],
                },
                7: {
                    "early": input_scenario.iat[55, 24],
                    "late": input_scenario.iat[61, 18],
                },
                8: {
                    "early": input_scenario.iat[55, 25],
                    "late": input_scenario.iat[61, 18],
                },
                9: {
                    "early": input_scenario.iat[55, 26],
                    "late": input_scenario.iat[61, 18],
                },
                10: {
                    "early": input_scenario.iat[55, 27],
                    "late": input_scenario.iat[61, 18],
                },
                11: {
                    "early": input_scenario.iat[55, 28],
                    "late": input_scenario.iat[61, 18],
                },
                12: {
                    "early": input_scenario.iat[55, 29],
                    "late": input_scenario.iat[61, 18],
                },
                13: {
                    "early": input_scenario.iat[55, 30],
                    "late": input_scenario.iat[61, 18],
                },
            },
        )
        self.pre_emptive_transplant_cadaver_donor_dist = scenario_dict.get(
            "pre_emptive_transplant_live_donor_dist",
            {
                1: {
                    "early": input_scenario.iat[55, 2],
                    "late": input_scenario.iat[61, 2],
                },
                2: {
                    "early": input_scenario.iat[55, 3],
                    "late": input_scenario.iat[61, 2],
                },
                3: {
                    "early": input_scenario.iat[55, 4],
                    "late": input_scenario.iat[61, 2],
                },
                4: {
                    "early": input_scenario.iat[55, 5],
                    "late": input_scenario.iat[61, 2],
                },
                5: {
                    "early": input_scenario.iat[55, 6],
                    "late": input_scenario.iat[61, 2],
                },
                6: {
                    "early": input_scenario.iat[55, 7],
                    "late": input_scenario.iat[61, 2],
                },
                7: {
                    "early": input_scenario.iat[55, 8],
                    "late": input_scenario.iat[61, 2],
                },
                8: {
                    "early": input_scenario.iat[55, 9],
                    "late": input_scenario.iat[61, 2],
                },
                9: {
                    "early": input_scenario.iat[55, 10],
                    "late": input_scenario.iat[61, 2],
                },
                10: {
                    "early": input_scenario.iat[55, 11],
                    "late": input_scenario.iat[61, 2],
                },
                11: {
                    "early": input_scenario.iat[55, 12],
                    "late": input_scenario.iat[61, 2],
                },
                12: {
                    "early": input_scenario.iat[55, 13],
                    "late": input_scenario.iat[61, 2],
                },
                13: {
                    "early": input_scenario.iat[55, 14],
                    "late": input_scenario.iat[61, 2],
                },
            },
        )
        self.time_on_waiting_list_mean = scenario_dict.get(
            "time_on_waiting_list_mean",
            {
                1: {
                    "live": input_scenario.iat[29, 2],
                    "cadaver": input_scenario.iat[30, 2],
                },
                2: {
                    "live": input_scenario.iat[29, 3],
                    "cadaver": input_scenario.iat[30, 3],
                },
                3: {
                    "live": input_scenario.iat[29, 4],
                    "cadaver": input_scenario.iat[30, 4],
                },
                4: {
                    "live": input_scenario.iat[29, 5],
                    "cadaver": input_scenario.iat[30, 5],
                },
                5: {
                    "live": input_scenario.iat[29, 6],
                    "cadaver": input_scenario.iat[30, 6],
                },
                6: {
                    "live": input_scenario.iat[29, 7],
                    "cadaver": input_scenario.iat[30, 7],
                },
                7: {
                    "live": input_scenario.iat[29, 8],
                    "cadaver": input_scenario.iat[30, 8],
                },
                8: {
                    "live": input_scenario.iat[29, 9],
                    "cadaver": input_scenario.iat[30, 9],
                },
                9: {
                    "live": input_scenario.iat[29, 10],
                    "cadaver": input_scenario.iat[30, 10],
                },
                10: {
                    "live": input_scenario.iat[29, 11],
                    "cadaver": input_scenario.iat[30, 11],
                },
                11: {
                    "live": input_scenario.iat[29, 12],
                    "cadaver": input_scenario.iat[30, 12],
                },
                12: {
                    "live": input_scenario.iat[29, 13],
                    "cadaver": input_scenario.iat[30, 13],
                },
                13: {
                    "live": input_scenario.iat[29, 14],
                    "cadaver": input_scenario.iat[30, 14],
                },
            },
        )
        self.daily_costs = scenario_dict.get(
            "daily_costs",
            {
                "ichd": input_scenario.iat[36, 1],
                "hhd": input_scenario.iat[37, 1],
                "pd": input_scenario.iat[38, 1],
                "living_with_transplant": input_scenario.iat[39, 1],
            },
        )


scenario = Scenario()

print(scenario.daily_costs)
