import streamlit as st
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine

@st.cache_resource
def get_presidio_engines():
    """Load and cache the Presidio engines."""
    analyzer = AnalyzerEngine()
    anonymizer = AnonymizerEngine()
    return analyzer, anonymizer

def redact_pii(text: str) -> str:
    """
    Analyzes and redacts Personally Identifiable Information (PII) from the given text.
    Replaces entities like PERSON, PHONE_NUMBER, etc., with placeholders.
    """
    if not text:
        return ""
        
    try:
        analyzer, anonymizer = get_presidio_engines()
        
        # Analyze the text for specific PII entities
        results = analyzer.analyze(
            text=text,
            entities=["PERSON", "PHONE_NUMBER", "EMAIL_ADDRESS", "DATE_TIME", "LOCATION"],
            language="en"
        )
        
        # Anonymize the text based on the analysis
        anonymized_result = anonymizer.anonymize(
            text=text,
            analyzer_results=results
        )
        
        return anonymized_result.text
    except Exception as e:
        import logging
        logging.error(f"PII Redaction failed: {e}")
        st.warning(f"Failed to redact PII: {str(e)}")
        return text
