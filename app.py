import streamlit as st
from modules.utils import (
    extract_from_file,
    highlight_medical_terms,
    explain_glossary_terms,
    save_summary_as_pdf
)

st.set_page_config(page_title="Medical Report Summarizer", layout="wide")

st.title("🏥 Medical Report Summarizer")
st.markdown(
    "Upload medical reports (PDF, DOCX, TXT, images) to extract and summarize key information."
)

uploaded_file = st.file_uploader(
    "Choose a file", 
    type=["pdf", "docx", "odt", "rtf", "txt", "png", "jpg", "jpeg"]
)

if uploaded_file:
    with st.spinner("Extracting text..."):
        content = extract_text_from_file(uploaded_file)
    
    st.subheader("📄 Extracted Text")
    st.text_area("Extracted content", content, height=250)

    highlighted_text = highlight_medical_terms(content)
    st.subheader("✨ Highlighted Medical Terms")
    st.markdown(highlighted_text, unsafe_allow_html=True)

    glossary = explain_glossary_terms(content)
    if glossary:
        st.subheader("🧾 Glossary")
        st.markdown(glossary, unsafe_allow_html=True)

    if st.button("💾 Download Summary as PDF"):
        pdf_path = save_summary_as_pdf(content)
        with open(pdf_path, "rb") as f:
            st.download_button("Download PDF", f, file_name="summary.pdf")
