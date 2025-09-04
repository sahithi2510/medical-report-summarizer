import streamlit as st
from modules.utils import (
    extract_text_from_file,
    highlight_medical_terms,
    explain_glossary_terms,
    save_summary_as_pdf,
    speak_summary,
)

st.set_page_config(page_title="Medical Report Summarizer", layout="wide")

st.title("🩺 Medical Report Summarizer")
uploaded_file = st.file_uploader("Upload a medical report", type=["pdf", "docx", "odt", "txt", "zip", "png", "jpg", "jpeg"])

if uploaded_file:
    content = extract_text_from_file(uploaded_file)
    st.subheader("Original Text")
    st.text_area("", content, height=300)

    highlighted = highlight_medical_terms(content)
    st.subheader("Highlighted Medical Terms")
    st.markdown(highlighted, unsafe_allow_html=True)

    glossary = explain_glossary_terms(content)
    if glossary:
        st.subheader("Glossary")
        st.markdown(glossary, unsafe_allow_html=True)

    pdf_path = save_summary_as_pdf(content)
    st.download_button("📄 Download Summary PDF", pdf_path)

    if st.button("🔊 Listen to Summary"):
        speak_summary(content)
