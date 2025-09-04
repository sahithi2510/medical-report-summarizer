import io
import os
import re
import tempfile
import streamlit as st
from google.cloud import vision
from google.oauth2 import service_account
from PyPDF2 import PdfReader
from pdf2image import convert_from_bytes
from PIL import Image
import pyttsx3

# -------------------------------
# Setup Google Vision client
# -------------------------------
@st.cache_resource
def setup_vision_client():
    """Initialize Google Vision API client using Streamlit Secrets."""
    creds = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"]
    )
    return vision.ImageAnnotatorClient(credentials=creds)

vision_client = setup_vision_client()


# -------------------------------
# OCR FUNCTIONS
# -------------------------------
def extract_text_from_image(image: Image.Image) -> str:
    """Extract text from a PIL image using Google Vision API."""
    with io.BytesIO() as output:
        image.save(output, format="PNG")
        content = output.getvalue()

    image_obj = vision.Image(content=content)
    response = vision_client.text_detection(image=image_obj)

    if response.error.message:
        raise RuntimeError(f"OCR error: {response.error.message}")

    return response.full_text_annotation.text


def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    """Convert PDF pages to images and extract text via Vision API."""
    images = convert_from_bytes(pdf_bytes)
    text = ""
    for img in images:
        text += extract_text_from_image(img) + "\n"
    return text.strip()


def extract_text_from_file(uploaded_file) -> str:
    """Handle file upload (PDF, image, or text)."""
    file_type = uploaded_file.type

    if file_type == "application/pdf":
        return extract_text_from_pdf(uploaded_file.read())
    elif file_type.startswith("image/"):
        image = Image.open(uploaded_file)
        return extract_text_from_image(image)
    elif file_type.startswith("text/"):
        return uploaded_file.read().decode("utf-8")
    else:
        raise ValueError(f"Unsupported file type: {file_type}")


# -------------------------------
# GLOSSARY HIGHLIGHTING
# -------------------------------
def highlight_medical_terms(text: str, glossary: dict) -> str:
    """Highlight glossary terms inside text with Markdown bold formatting."""
    for term, definition in glossary.items():
        pattern = re.compile(rf"\b({re.escape(term)})\b", flags=re.IGNORECASE)
        text = pattern.sub(r"**\1**", text)
    return text


# -------------------------------
# TEXT TO SPEECH
# -------------------------------
def text_to_speech(text: str) -> str:
    """Convert text to speech and return path to temporary audio file."""
    engine = pyttsx3.init()
    tmp_file = tempfile.NamedTemporaryFile(delete=False,
