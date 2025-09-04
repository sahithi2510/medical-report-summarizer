import streamlit as st
from modules.utils import (
    extract_text_from_file,
    highlight_medical_terms,
    explain_glossary_terms,
    speak_text,
    TESSERACT_AVAILABLE
)

# ---------------------------
# Page setup
# ---------------------------
st.set_page_config(page_title="Medical Report Summarizer", layout="wide")
st.title("📄 Medical Report Summarizer")

# ---------------------------
# File uploader
# ---------------------------
uploaded_file = st.file_uploader(
    "Upload medical report (PDF or Image)", 
    type=["pdf", "png", "jpg", "jpeg"]
)

# ---------------------------
# Warning if Tesseract missing
# ---------------------------
if not TESSERACT_AVAILABLE:
    st.error("⚠️ Tesseract OCR is not installed. Please check `.streamlit/packages.txt`.")

# ---------------------------
# Processing uploaded file
# ---------------------------
if uploaded_file and TESSERACT_AVAILABLE:
    with st.spinner("🔍 Extracting text..."):
        extracted_text = extract_text_from_file(uploaded_file)

    st.subheader("📑 Extracted Text")
    st.write(extracted_text)

    st.subheader("🩺 Highlighted Medical Terms")
    highlighted_text = highlight_medical_terms(extracted_text)
    st.markdown(highlighted_text)

    st.subheader("📘 Glossary Definitions")
    definitions = explain_glossary_terms(extracted_text)
    if definitions:
        for term, definition in definitions.items():
            st.markdown(f"**{term}**: {definition}")
    else:
        st.info("No glossary terms found.")

    if st.button("🔊 Read Out Summary"):
        speak_text(extracted_text)
