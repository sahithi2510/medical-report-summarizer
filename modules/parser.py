import re
import logging
from typing import Dict, Optional

def extract_lab_values(text: str) -> Optional[Dict[str, float]]:
    """
    Extracts common lab values from unstructured medical report text.
    Returns a dictionary of {Test Name: Value} or None if no tests are found.
    """
    if not text:
        return None
        
    values = {}
    
    # Advanced regex patterns to capture a wide variety of formats and misspellings
    patterns = {
        "Haemoglobin": [
            r"h[ae]+moglobin\s*(?:level|count|of)?\s*[:=]?\s*(\d+\.?\d*)",
            r"hgb\s*[:=]?\s*(\d+\.?\d*)"
        ],
        "WBC": [
            r"w[h]?i?t?e\s*b[l]?o[o]?d\s*c[e]?[l]?ls?\s*(?:count|of)?\s*[:=]?\s*(\d+\.?\d*)",
            r"wbc\s*(?:count|of)?\s*[:=]?\s*(\d+\.?\d*)"
        ],
        "Blood Sugar": [
            r"b[l]?o[o]?d\s*s[u]?g[a]?r\s*(?:level|of)?\s*[:=]?\s*(\d+\.?\d*)",
            r"g[l]?u[c]?o[s]?e\s*(?:level|of)?\s*[:=]?\s*(\d+\.?\d*)"
        ],
        "Creatinine": [
            r"c[r]?e[a]?t[i]?n[i]?n[e]?\s*(?:level|of)?\s*[:=]?\s*(\d+\.?\d*)"
        ],
        "Platelets": [
            r"p[l]?a[t]?e[l]?e[t]?s?\s*(?:count|of)?\s*[:=]?\s*(\d+\.?\d*)",
            r"plt\s*[:=]?\s*(\d+\.?\d*)"
        ],
        "Cholesterol": [
            r"c[h]?o[l]?e[s]?t[e]?[r]?o[l]?\s*(?:level|of)?\s*[:=]?\s*(\d+\.?\d*)"
        ],
        "HbA1c": [
            r"hba1c\s*(?:level|of)?\s*[:=]?\s*(\d+\.?\d*)",
            r"a1c\s*[:=]?\s*(\d+\.?\d*)"
        ]
    }

    text_lower = text.lower()

    for test_name, regex_list in patterns.items():
        for pattern in regex_list:
            try:
                match = re.search(pattern, text_lower)
                if match:
                    values[test_name] = float(match.group(1))
                    break # Stop searching other regex patterns for this test if found
            except Exception as e:
                logging.warning(f"Failed to parse {test_name} with pattern {pattern}: {e}")

    return values if values else None