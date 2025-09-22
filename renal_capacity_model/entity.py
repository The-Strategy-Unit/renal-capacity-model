"""
Contains the Entities to be used in the model
"""


class Patient:
    """Patient entity"""

    def __init__(self, p_id, patient_type):
        self.id = p_id
        self.time_in_system = 0
        self.patient_type = patient_type
        self.age_group = int(patient_type.split('_')[0])  # Extract age group from patient type
        self.referral_type = patient_type.split('_')[1]
        self.transplant_suitable = None
        self.transplant_type = None  # 1 = live, 2 = cadaver
        self.pre_emptive_transplant = None
