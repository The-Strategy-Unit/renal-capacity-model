"""
Contains the Entities to be used in the model
"""


class Patient:
    """Patient entity"""

    def __init__(self, p_id, patient_type):
        self.id = p_id
        self.time_in_system = 0
        self.patient_type = patient_type
