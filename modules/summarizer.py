import streamlit as st
import logging
from typing import Tuple
from transformers import (
    AutoTokenizer,
    AutoModelForSeq2SeqLM
)

@st.cache_resource
def load_model() -> Tuple[AutoTokenizer, AutoModelForSeq2SeqLM]:
    """Loads and caches the T5 Summarization model."""
    try:
        tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-small")
        model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-small")
        return tokenizer, model
    except Exception as e:
        logging.error(f"Failed to load summarization model: {e}")
        st.error(f"Model Loading Error: {e}")
        raise e

def generate_summary(text: str) -> str:
    """
    Generates a concise medical summary from the given text using a T5 transformer.
    """
    if not text or not text.strip():
        return "No report content found to summarize."

    try:
        tokenizer, model = load_model()

        # Truncate text to avoid exceeding model's max input length
        text = text[:2000]

        prompt = "Summarize the following medical report concisely:\n\n" + text

        inputs = tokenizer(
            prompt,
            return_tensors="pt",
            truncation=True,
            max_length=512
        )

        outputs = model.generate(
            **inputs,
            max_length=150,
            min_length=30,
            num_beams=4,
            early_stopping=True
        )

        summary = tokenizer.decode(
            outputs[0],
            skip_special_tokens=True
        )

        return summary
    except Exception as e:
        logging.error(f"Failed to generate summary: {e}")
        st.error(f"Summarization Error: {e}")
        return "An error occurred during summarization."