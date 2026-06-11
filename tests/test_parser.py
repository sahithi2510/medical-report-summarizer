from modules.parser import extract_lab_values


def test_extract_lab_values():

    sample_text = """
    Hemoglobin: 10.5
    WBC: 12000
    Blood Sugar: 145
    Platelets: 250000
    Creatinine: 1.2
    """

    values = extract_lab_values(sample_text)

    assert values["Hemoglobin"] == 10.5
    assert values["WBC"] == 12000
    assert values["Blood Sugar"] == 145
    assert values["Platelets"] == 250000
    assert values["Creatinine"] == 1.2


def test_empty_text():

    values = extract_lab_values("")

    assert values == {}