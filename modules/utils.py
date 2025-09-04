import streamlit as st
from google.cloud import vision
from google.oauth2 import service_account
from PyPDF2 import PdfReader
from pdf2image import convert_from_bytes
from PIL import Image
import io
import json
import re
from fpdf import FPDF
import pyttsx3

# ---------------------------
# Google Vision Setup
# ---------------------------
@st.cache_resource
def setup_vision_client():
    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"]
    )
    return vision.ImageAnnotatorClient(credentials=credentials)

vision_client = setup_vision_client()

# ---------------------------
# Text Extraction Functions
# ---------------------------
def extract_text_from_pdf(uploaded_file):
    pdf = PdfReader(uploaded_file)
    text = ""
    for page in pdf.pages:
        text += page.extract_text() or ""
    # If no text, fallback to OCR
    if not text.strip():
        images = convert_from_bytes(uploaded_file.read())
        text = "\n".join([extract_text_from_image(img) for img in images])
    return text

def extract_text_from_image(image):
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()

    response = vision_client.document_text_detection({'content': img_byte_arr})
    texts = response.text_annotations
    return texts[0].description if texts else ""

def extract_from_file(uploaded_file):
    """Detect file type and extract text from PDF or image."""
    fname = uploaded_file.name.lower()
    if fname.endswith(".pdf"):
        return extract_text_from_pdf(uploaded_file)
    elif fname.endswith((".png", ".jpg", ".jpeg")):
        image = Image.open(uploaded_file)
        return extract_text_from_image(image)
    else:
        return "Unsupported file type."

# ---------------------------
# Glossary Highlighting
# ---------------------------
def highlight_medical_terms(text):
    glossary_file = "modules/glossary.json"
    with open(glossary_file, "r") as f:
        glossary = json.load(f)
    for term in glossary.keys():
        pattern = re.compile(fr"\b({term})\b", re.IGNORECASE)
        text = pattern.sub(r"<mark>\1</mark>", text)
    return text

def explain_glossary_terms(summary):
    glossary_file = "modules/glossary.json"
    with open(glossary_file, "r") as f:
        glossary = json.load(f)
    explanations = [
        f"**{t.capitalize()}**: {d}"
        for t, d in glossary.items()
        if re.search(fr"\b{t}\b", summary, re.IGNORECASE)
    ]
    return "### 🧾 Glossary\n" + "\n".join(explanations) if explanations else ""

# ---------------------------
# Export PDF
# ---------------------------
def save_summary_as_pdf(summary):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for line in summary.split("\n"):
        pdf.multi_cell(0, 10, line)
    path = "/mnt/data/summary.pdf"
    pdf.output(path)
    return path

# ---------------------------
# Text-to-Speech
# ---------------------------
def speak_summary(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
