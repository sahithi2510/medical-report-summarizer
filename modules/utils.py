import os
import re
import tempfile
import streamlit as st
from PIL import Image
import pytesseract
import docx
from odf.opendocument import load as load_odt
from odf.text import P
from fpdf import FPDF
import pyttsx3
from PyPDF2 import PdfReader
from pdf2image import convert_from_path

# ---------------------------
# OCR Extraction
# ---------------------------

def extract_text_from_image(image_file):
    """Extract text from an image using Tesseract OCR."""
    try:
        image = Image.open(image_file)
        return pytesseract.image_to_string(image)
    except Exception as e:
        return f"❌ OCR extraction failed: {e}"

def extract_text_from_pdf(pdf_file):
    """Extract text from PDF by direct parsing + OCR fallback."""
    text = ""
    try:
        pdf_reader = PdfReader(pdf_file)
        for page in pdf_reader.pages:
            text += page.extract_text() or ""
    except Exception:
        pass

    if not text.strip():
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
                tmp_pdf.write(pdf_file.read())
                tmp_pdf_path = tmp_pdf.name
            images = convert_from_path(tmp_pdf_path)
            for img in images:
                text += pytesseract.image_to_string(img)
            os.remove(tmp_pdf_path)
        except Exception as e:
            return f"❌ PDF OCR failed: {e}"
    return text

def extract_text_from_docx(docx_file):
    """Extract text from .docx file."""
    try:
        doc = docx.Document(docx_file)
        return "\n".join([p.text for p in doc.paragraphs])
    except Exception as e:
        return f"❌ DOCX extraction failed: {e}"

def extract_text_from_odt(odt_file):
    """Extract text from .odt file."""
    try:
        odt_doc = load_odt(odt_file)
        paragraphs = odt_doc.getElementsByType(P)
        return "\n".join([p.firstChild.data if p.firstChild else "" for p in paragraphs])
    except Exception as e:
        return f"❌ ODT extraction failed: {e}"

def extract_text_from_file(uploaded_file):
    """Auto-detect file type and extract text."""
    file_type = uploaded_file.name.lower()
    if file_type.endswith((".png", ".jpg", ".jpeg", ".bmp", ".tiff")):
        return extract_text_from_image(uploaded_file)
    elif file_type.endswith(".pdf"):
        return extract_text_from_pdf(uploaded_file)
    elif file_type.endswith(".docx"):
        return extract_text_from_docx(uploaded_file)
    elif file_type.endswith(".odt"):
        return extract_text_from_odt(uploaded_file)
    else:
        return "❌ Unsupported file type."

# ---------------------------
# Glossary Highlight
# ---------------------------

MEDICAL_TERMS = {
    "hypertension": "A condition in which blood pressure is consistently too high.",
    "diabetes": "A disease that occurs when blood glucose is too high.",
    "anemia": "A condition marked by a deficiency of red blood cells.",
    "asthma": "A condition in which a person's airways become inflamed and narrow."
}

def highlight_medical_terms(text):
    """Highlight medical terms in extracted text."""
    highlighted = text
    for term in MEDICAL_TERMS.keys():
        pattern = re.compile(rf"\b({term})\b", re.IGNORECASE)
        highlighted = pattern.sub(r"**\1**", highlighted)
    return highlighted

def explain_glossary_terms(text):
    """Return glossary explanations for found terms."""
    found_terms = {}
    for term, meaning in MEDICAL_TERMS.items():
        if re.search(rf"\b{term}\b", text, re.IGNORECASE):
            found_terms[term] = meaning
    return found_terms

# ---------------------------
# Text-to-Speech
# ---------------------------

def text_to_speech(text):
    """Convert text to speech and return audio file path."""
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_audio:
            path = tmp_audio.name
        engine = pyttsx3.init()
        engine.save_to_file(text, path)
        engine.runAndWait()
        return path
    except Exception as e:
        return f"❌ TTS failed: {e}"
