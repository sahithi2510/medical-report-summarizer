import streamlit as st

# ---------------------------
# Page configuration (must be first)
# ---------------------------
st.set_page_config(
    page_title="Medical Report Summarizer",
    page_icon="🩺",
    layout="wide"
)

# ---------------------------
# Imports
# ---------------------------
from modules.utils import (
    extract_from_file,
    highlight_medical_terms,
    explain_glossary_terms,
    save_summary_as_pdf,
    speak_summary
)

# ---------------------------
# App UI
# ---------------------------
st.title("🩺 Medical Report Summarizer")

uploaded_file = st.file_uploader(
    "Upload a PDF or image file to extract and summarize text", 
    type=["pdf", "png", "jpg", "jpeg"]
)

if uploaded_file:
    with st.spinner("Extracting text..."):
        content = extract_text_from_file(uploaded_file)

    st.subheader("Extracted Text")
    st.write(content)

    st.subheader("Highlighted Medical Terms")
    highlighted_text = highlight_medical_terms(content)
    st.markdown(highlighted_text, unsafe_allow_html=True)

    st.subheader("Glossary")
    glossary_text = explain_glossary_terms(content)
    st.markdown(glossary_text, unsafe_allow_html=True)

    st.subheader("Export Summary as PDF")
    pdf_path = save_summary_as_pdf(content)
    with open(pdf_path, "rb") as f:
        st.download_button(
            label="Download PDF",
            data=f,
            file_name="summary.pdf",
            mime="application/pdf"
        )

    st.subheader("Text-to-Speech (Disabled on Streamlit Cloud)")
    tts_text = speak_summary(content)
    st.info(tts_text)

