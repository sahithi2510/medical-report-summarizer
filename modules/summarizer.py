from transformers import pipeline
import streamlit as st

@st.cache_resource
def load_summarizer():
    return pipeline("summarization", model="facebook/bart-large-cnn")

summarizer = load_summarizer()

def generate_summary(text):
    if not text.strip():
        return "No content to summarize."

    max_input_len = 1024
    text = text[:max_input_len]

    summary = summarizer(text, max_length=150, min_length=30, do_sample=False)
    return summary[0]["summary_text"]
