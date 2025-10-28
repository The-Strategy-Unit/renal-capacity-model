from renal_capacity_model.entity import Patient


def test_entity_initializes_with_values():
    # arrange
    p_id = 1
    patient_type = "0_referraltype"
    patient_flag = "incident"

    # act
    patient = Patient(p_id, patient_type, patient_flag)

    # assert
    assert patient.id == p_id
    assert patient.patient_type == patient_type
    assert patient.patient_flag == patient_flag
    assert patient.age_group == 0
    assert patient.referral_type == "referraltype"
