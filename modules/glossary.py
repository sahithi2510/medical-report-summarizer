import json
import re

with open(
    "data/glossary.json",
    encoding="utf-8"
) as f:

    GLOSSARY = json.load(f)


def highlight_medical_terms(text):

    for term in GLOSSARY.keys():

        pattern = re.compile(
            rf"\b({re.escape(term)})\b",
            re.IGNORECASE
        )

        text = pattern.sub(
            r"<mark>\1</mark>",
            text
        )

    return text


def explain_terms(text):

    explanations = []

    for term, definition in GLOSSARY.items():

        if re.search(
            rf"\b{re.escape(term)}\b",
            text,
            re.IGNORECASE
        ):

            explanations.append(
                f"- **{term}**: {definition}"
            )

    if explanations:

        return (
            "### 📚 Medical Glossary\n\n"
            + "\n".join(explanations)
        )

    return ""