import streamlit as st
from modules.utils import (
    extract_text_from_file,
    highlight_medical_terms,
    explain_glossary_terms,
    save_summary_as_pdf,
    save_summary_as_txt,
    speak_summary
)

st.set_page_config(page_title="Medical Report Summarizer", layout="wide")

st.title("📄 Medical Report Summarizer")

uploaded_file = st.file_uploader("Upload your medical report", type=["txt","pdf","docx","odt","png","jpg","jpeg"])
if uploaded_file:
    content = extract_text_from_file(uploaded_file)
    st.subheader("Extracted Text")
    st.write(content)

    # Highlight terms
    highlighted = highlight_medical_terms(content)
    st.markdown("### Highlighted Terms")
    st.markdown(highlighted, unsafe_allow_html=True)

    # Glossary
    glossary_text = explain_glossary_terms(content)
    if glossary_text:
        st.markdown(glossary_text, unsafe_allow_html=True)

    # Download PDF
    pdf_file = save_summary_as_pdf(content)
    st.download_button("Download Summary as PDF", pdf_file, file_name="summary.pdf", mime="application/pdf")

    # Download TXT
    txt_file = save_summary_as_txt(content)
    st.download_button("Download Summary as TXT", txt_file, file_name="summary.txt", mime="text/plain")

    # Audio
    audio_file = speak_summary(content)
    st.audio(audio_file, format="audio/mp3")

