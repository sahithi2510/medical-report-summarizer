import streamlit as st
from modules.ocr_reader import extract_text_from_file
from modules.summarizer import generate_summary
from gtts import gTTS
import os

st.set_page_config(page_title="Medical Report Summarizer", layout="centered")

st.title("📄 Medical Report Summarizer")
st.markdown("Upload a PDF medical report to generate a simplified summary.")

uploaded_file = st.file_uploader("Choose a file", type=["pdf", "jpg", "png"])

if uploaded_file is not None:
    with st.spinner("🔍 Extracting text..."):
        extracted_text = extract_text_from_file(uploaded_file)

    st.subheader("📜 Extracted Text")
    st.write(extracted_text)

    if extracted_text.strip():
        with st.spinner("✍️ Summarizing..."):
            summary = generate_summary(extracted_text)

        st.subheader("🧾 Summary")
        st.write(summary)

        with st.spinner("🔊 Generating audio..."):
            tts = gTTS(text=summary, lang='en')
            audio_path = "audio_summary.mp3"
            tts.save(audio_path)
            audio_file = open(audio_path, 'rb')
            audio_bytes = audio_file.read()
            st.audio(audio_bytes, format='audio/mp3')
            audio_file.close()
            os.remove(audio_path)
