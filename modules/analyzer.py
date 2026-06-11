import json
import pandas as pd

def load_ranges():
    with open("data/reference_ranges.json") as f:
        return json.load(f)

def analyze_results(values):
    RANGES = load_ranges()

    rows = []

    for test, value in values.items():

        range_val = RANGES.get(test)

        if not range_val:
            status = "Unknown"
        else:
            low, high = range_val
            if value < low:
                status = "Low"
            elif value > high:
                status = "High"
            else:
                status = "Normal"

        rows.append([
            test,
            value,
            status
        ])

    return pd.DataFrame(
        rows,
        columns=[
            "Test",
            "Value",
            "Status"
        ]
    )