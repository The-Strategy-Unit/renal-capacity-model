"""
Contains the Entities to be used in the model
"""


class Patient:
    """Patient entity"""


    def __init__(self, p_id, patient_type, start_time_in_system,patient_flag):
        self.id = p_id
        self.time_in_system = 0
        self.patient_type = patient_type
        self.start_time_in_system = start_time_in_system
        self.patient_flag = patient_flag  # "incident" or "prevalent"
        self.age_group = int(
            patient_type.split("_")[0]
        )  # Extract age group from patient type
        self.referral_type = patient_type.split("_")[1]
        self.transplant_suitable = None  # transplant_suitable
        self.transplant_type = None  # transplant_type  # "live", "cadaver"
        self.pre_emptive_transplant = None
        self.dialysis_modality = None  # dialysis_modality  # none, ichd, hhd, pd
        self.time_on_dialysis = {"ichd": 0, "hhd": 0, "pd": 0}
        self.time_living_with_live_transplant = None
        self.time_living_with_cadaver_transplant = None
        self.transplant_count = 0  # transplant_count
        self.time_on_waiting_list = None
        self.time_enters_waiting_list = None
        self.time_of_transplant = None
