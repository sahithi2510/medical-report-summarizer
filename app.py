import streamlit as st

from modules.ocr import extract_text
from modules.summarizer import generate_summary
from modules.parser import extract_lab_values
from modules.analyzer import analyze_results
from modules.visualization import display_charts
from modules.glossary import highlight_medical_terms, explain_terms
from modules.exporter import export_pdf, export_txt
from modules.tts import generate_audio
from modules.redactor import redact_pii

st.set_page_config(
    page_title="AI Medical Report Analyzer",
    layout="wide"
)

st.title("🩺 AI Medical Report Analyzer")

# Initialize session state
if "current_file" not in st.session_state:
    st.session_state.current_file = None
if "text" not in st.session_state:
    st.session_state.text = None
if "summary" not in st.session_state:
    st.session_state.summary = None
if "glossary_text" not in st.session_state:
    st.session_state.glossary_text = None
if "lab_values" not in st.session_state:
    st.session_state.lab_values = None
if "results" not in st.session_state:
    st.session_state.results = None

uploaded_file = st.file_uploader(
    "Upload Medical Report",
    type=["pdf", "txt", "docx", "png", "jpg", "jpeg"]
)

if uploaded_file:
    file_id = f"{uploaded_file.name}_{uploaded_file.size}"

    if st.session_state.current_file != file_id:
        st.session_state.current_file = file_id
        
        with st.spinner("Extracting text..."):
            raw_text = extract_text(uploaded_file)
            
        with st.spinner("Redacting Personally Identifiable Information..."):
            # Redact PII before storing
            st.session_state.text = redact_pii(raw_text)
            
        with st.spinner("Generating summary..."):
            st.session_state.summary = generate_summary(st.session_state.text)
            
        with st.spinner("Analyzing terms..."):
            st.session_state.glossary_text = explain_terms(st.session_state.summary)
            
        with st.spinner("Extracting lab values..."):
            st.session_state.lab_values = extract_lab_values(st.session_state.text)
            if st.session_state.lab_values:
                st.session_state.results = analyze_results(st.session_state.lab_values)
            else:
                st.session_state.results = None

    text = st.session_state.text
    summary = st.session_state.summary
    glossary_text = st.session_state.glossary_text
    values = st.session_state.lab_values
    results = st.session_state.results

    # Use tabs for a cleaner UI
    tab1, tab2, tab3 = st.tabs(["📄 AI Summary", "📊 Lab Results", "📝 Raw Extracted Text"])

    with tab1:
        st.subheader("AI Summary")
        st.write(summary)

        st.subheader("Medical Terms")
        st.markdown(
            highlight_medical_terms(summary),
            unsafe_allow_html=True
        )

        if glossary_text:
            st.markdown(glossary_text)
            
        # Audio inside an expander
        with st.expander("Listen to Summary"):
            audio = generate_audio(summary)
            if audio:
                st.audio(audio, format="audio/mp3")

        # Downloads inside an expander
        with st.expander("Export Options"):
            col1, col2 = st.columns(2)
            with col1:
                pdf_file = export_pdf(summary)
                st.download_button("Download PDF", pdf_file, file_name="summary.pdf")
            with col2:
                txt_file = export_txt(summary)
                st.download_button("Download TXT", txt_file, file_name="summary.txt")

    with tab2:
        if values and results is not None:
            st.subheader("Detected Lab Values")
            
            # Apply styling to dataframe
            def color_status(val):
                if val in ['High', 'Low']:
                    color = '#ff4b4b' # Red
                else:
                    color = '#00cc66' # Green
                return f'color: {color}'
            
            styled_df = results.style.map(color_status, subset=['Status'])
            st.dataframe(styled_df, use_container_width=True)

            display_charts(results)
        else:
            st.info("No lab values detected in this report.")

    with tab3:
        st.subheader("Extracted Report (PII Redacted)")
        st.text_area("Content", text, height=400)
