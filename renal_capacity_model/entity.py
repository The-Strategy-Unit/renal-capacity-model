"""
Contains the Entities to be used in the model
"""


class Patient:
    """Patient entity"""

    def __init__(
        self,
        p_id: int,
        patient_type: str,
        start_time_in_system: float,
        patient_flag: str,
    ):
        """Initialises Patient entity

        Args:
            p_id (int): id of the patient. Unique to each patient
            patient_type (str): Patient type, comprised of age groups 1-6 and referral types early or late. E.g. "1_early", "2_late"
            start_time_in_system (float): Time the patient enters the simulation
            patient_flag (str): Whether or not the patient is an incident or prevalent patient.
        """
        self.id = p_id
        self.time_in_system = 0
        self.patient_type = patient_type
        self.start_time_in_system = start_time_in_system
        self.time_until_death: float | None = None
        self.patient_flag = patient_flag  # "incident" or "prevalent"
        self.age_group = int(
            patient_type.split("_")[0]
        )  # Extract age group from patient type
        self.referral_type: str = patient_type.split("_")[1]
        self.transplant_suitable: bool | None = None
        self.transplant_type: str | None = None  # "live", "cadaver"
        self.pre_emptive_transplant: bool | None = None
        self.dialysis_modality: str = "none"  # "ichd", "hhd", "pd", "none"
        self.time_starts_dialysis: float | None = None
        self.time_on_dialysis = {"ichd": 0.0, "hhd": 0.0, "pd": 0.0}
        self.time_living_with_live_transplant: float | None = None
        self.time_living_with_cadaver_transplant: float | None = None
        self.transplant_count = 0
        self.time_on_waiting_list = 0
        self.time_enters_waiting_list: float | None = None
        self.time_of_transplant: float | None = None
