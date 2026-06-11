from modules.analyzer import analyze_results


def test_analyze_results():

    values = {
        "Hemoglobin": 10,
        "Blood Sugar": 150,
        "Creatinine": 1.0
    }

    df = analyze_results(values)

    status_map = {
        row["Test"]: row["Status"]
        for _, row in df.iterrows()
    }

    assert status_map["Hemoglobin"] == "Low"
    assert status_map["Blood Sugar"] == "High"
    assert status_map["Creatinine"] == "Normal"


def test_normal_values():

    values = {
        "Hemoglobin": 14,
        "Blood Sugar": 90
    }

    df = analyze_results(values)

    status_map = {
        row["Test"]: row["Status"]
        for _, row in df.iterrows()
    }

    assert status_map["Hemoglobin"] == "Normal"
    assert status_map["Blood Sugar"] == "Normal"