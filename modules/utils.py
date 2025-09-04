import os
import re
import json
import io
import PyPDF2
from pdf2image import convert_from_bytes
import docx
from odf.opendocument import load as load_odt
from odf.text import P, H
from fpdf import FPDF
import streamlit as st
from google.cloud import vision
from striprtf.striprtf import rtf_to_text

# ----------------- Setup Google Vision client -----------------
def setup_vision_client():
    creds_json = st.secrets["google"]["GOOGLE_APPLICATION_CREDENTIALS_JSON"]
    key_path = "/tmp/key.json"
    with open(key_path, "w") as f:
        f.write(creds_json)
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = key_path
    return vision.ImageAnnotatorClient()

vision_client = setup_vision_client()

# ----------------- OCR -----------------
def ocr_image_cloud(file_bytes):
    image = vision.Image(content=file_bytes)
    response = vision_client.text_detection(image=image)
    texts = response.text_annotations
    if texts:
        return texts[0].description
    return ""

def get_bytes(uploaded_file):
    uploaded_file.seek(0)
    return uploaded_file.getvalue()

# ----------------- Text Extraction -----------------
def extract_text_from_file(uploaded_file):
    filename = uploaded_file.name.lower()

    # TXT
    if filename.endswith(".txt"):
        return uploaded_file.read().decode("utf-8", errors="ignore")

    # PDF
    if filename.endswith(".pdf"):
        try:
            reader = PyPDF2.PdfReader(uploaded_file)
            text = "".join([page.extract_text() or "" for page in reader.pages])
            if text.strip():
                return text
        except Exception:
            pass
        images = convert_from_bytes(get_bytes(uploaded_file))
        text_pages = []
        for img in images:
            with io.BytesIO() as buf:
                img.save(buf, format="PNG")
                buf.seek(0)
                text_pages.append(ocr_image_cloud(buf.getvalue()))
        return "\n".join(text_pages)

    # DOCX
    if filename.endswith(".docx"):
        doc = docx.Document(uploaded_file)
        return "\n".join([para.text for para in doc.paragraphs])

    # ODT
    if filename.endswith(".odt"):
        text = ""
        odt_doc = load_odt(uploaded_file)
        for elem in odt_doc.getElementsByType((P, H)):
            text += (elem.firstChild.data if elem.firstChild else "") + "\n"
        return text

    # Images
    if filename.endswith((".png", ".jpg", ".jpeg")):
        return ocr_image_cloud(get_bytes(uploaded_file))

    # RTF
    if filename.endswith(".rtf"):
        raw = uploaded_file.read().decode("utf-8", errors="ignore")
        return rtf_to_text(raw)

    return f"Unsupported or unrecognized file type: {filename}"

# ----------------- Highlight Medical Terms -----------------
def highlight_medical_terms(text):
    glossary_file = os.path.join(os.path.dirname(__file__), "glossary.json")
    with open(glossary_file, "r") as f:
        glossary = json.load(f)
    for term in glossary.keys():
        pattern = re.compile(fr"\b({term})\b", re.IGNORECASE)
        text = pattern.sub(r"<mark>\1</mark>", text)
    return text

# ----------------- Glossary -----------------
def explain_glossary_terms(summary):
    glossary_file = os.path.join(os.path.dirname(__file__), "glossary.json")
    with open(glossary_file, "r") as f:
        glossary = json.load(f)
    explanations = [
        f"**{t.capitalize()}**: {d}"
        for t, d in glossary.items()
        if re.search(fr"\b{t}\b", summary, re.IGNORECASE)
    ]
    return "### 🧾 Glossary\n" + "\n".join(explanations) if explanations else ""

# ----------------- PDF export -----------------
def save_summary_as_pdf(summary):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for line in summary.split("\n"):
        pdf.multi_cell(0, 10, line)
    path = "/mnt/data/summary.pdf"
    pdf.output(path)
    return path
