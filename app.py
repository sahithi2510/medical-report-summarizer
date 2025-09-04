import streamlit as st
from modules.summarizer import generate_summary
from modules.utils import (
    extract_text_from_file,
    highlight_medical_terms,
    save_summary_as_pdf,
    speak_summary,
    explain_glossary_terms,
)
import os
from dotenv import load_dotenv

load_dotenv()
st.set_page_config(page_title="🩺 Medical Report Summarizer", layout="wide")
st.title("🩺 Medical Report Summarizer")

with st.sidebar.expander("⚙️ Settings"):
    model_choice = st.selectbox(
        "Choose summarization model:",
        ("sshleifer/distilbart-cnn-12-6", "facebook/bart-large-cnn"),
        index=0
    )
    if st.button("Apply model choice"):
        os.environ["SUMMARIZER_MODEL"] = model_choice
        st.info("Restart the app to apply the model change.")

uploaded_file = st.file_uploader(
    "Upload Medical Report (PDF, TXT, DOCX, ODT, RTF, JPG, PNG, ZIP)",
    type=["pdf", "txt", "docx", "odt", "rtf", "jpg", "jpeg", "png", "zip"]
)

if uploaded_file:
    with st.expander("📄 Raw Extracted Text"):
        content = extract_text_from_file(uploaded_file)
        st.text_area("Extracted Text", content, height=300)

    if st.button("Summarize Report"):
        with st.spinner("Generating summary..."):
            summary = generate_summary(content)
            highlighted = highlight_medical_terms(summary)

            st.markdown("### 🧠 Layman-Friendly Summary")
            st.markdown(highlighted, unsafe_allow_html=True)

            glossary = explain_glossary_terms(summary)
            if glossary:
                st.markdown(glossary)

            st.download_button("📥 Download TXT", summary, file_name="summary.txt")
            pdf_path = save_summary_as_pdf(summary)
            with open(pdf_path, "rb") as f:
                st.download_button("📥 Download PDF", f, file_name="summary.pdf")

            if st.checkbox("🔊 Listen to Summary"):
                speak_summary(summary)
