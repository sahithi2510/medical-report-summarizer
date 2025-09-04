import os
import json
import re
import tempfile
from PIL import Image
import pytesseract
import pyttsx3
from PyPDF2 import PdfReader

# ---------------------------
# Load glossary terms
# ---------------------------
GLOSSARY_PATH = os.path.join(os.path.dirname(__file__), "glossary.json")
with open(GLOSSARY_PATH, "r", encoding="utf-8") as file:
    GLOSSARY = json.load(file)

# ---------------------------
# Check Tesseract availability
# ---------------------------
def is_tesseract_available():
    try:
        pytesseract.get_tesseract_version()
        return True
    except Exception:
        return False

TESSERACT_AVAILABLE = is_tesseract_available()

# ---------------------------
# Text-to-Speech
# ---------------------------
def speak_text(text: str):
    try:
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    except Exception:
        return "❌ TTS failed. Is pyttsx3 supported in this environment?"

# ---------------------------
# OCR: extract text from image
# ---------------------------
def extract_text_from_image(image):
    if not TESSERACT_AVAILABLE:
        return "❌ Tesseract OCR is not installed."
    try:
        return pytesseract.image_to_string(image)
    except Exception as e:
        return f"❌ OCR error: {str(e)}"

# ---------------------------
# OCR: extract text from PDF
# ---------------------------
def extract_text_from_pdf(pdf_file):
    if not TESSERACT_AVAILABLE:
        return "❌ Tesseract OCR is not installed."

    text = ""
    try:
        with tempfile.TemporaryDirectory() as _:
            reader = PdfReader(pdf_file)
            for page in reader.pages:
                try:
                    text += page.extract_text() or ""
                except Exception:
                    continue
    except Exception as e:
        return f"❌ PDF reading error: {str(e)}"

    return text.strip() if text else "❌ No text found in the PDF."

# ---------------------------
# General extractor
# ---------------------------
def extract_text_from_file(uploaded_file):
    try:
        if uploaded_file.type.startswith("image/"):
            image = Image.open(uploaded_file)
            return extract_text_from_image(image)
        elif uploaded_file.type == "application/pdf":
            return extract_text_from_pdf(uploaded_file)
        else:
            return "❌ Unsupported file format."
    except Exception as e:
        return f"❌ File extraction error: {str(e)}"

# ---------------------------
# Highlight glossary terms
# ---------------------------
def highlight_medical_terms(text: str):
    highlighted = text
    for term in GLOSSARY.keys():
        pattern = re.compile(rf"\b({re.escape(term)})\b", re.IGNORECASE)
        highlighted = pattern.sub(r"**\1**", highlighted)
    return highlighted

# ---------------------------
# Explain glossary terms
# ---------------------------
def explain_glossary_terms(text: str):
    found = {}
    for term, definition in GLOSSARY.items():
        if re.search(rf"\b{re.escape(term)}\b", text, re.IGNORECASE):
            found[term] = definition
    return found
