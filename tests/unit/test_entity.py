from renal_capacity_model.entity import Patient


def test_entity_initializes_with_values():
    # arrange
    p_id = 1
    patient_type = "0_referraltype"

    # act
    patient = Patient(p_id, patient_type)

    # assert
    assert patient.id == p_id
    assert patient.patient_type == patient_type
    assert patient.age_group == 0
    assert patient.referral_type == "referraltype"
