import os
import re
import io
import json
import zipfile
from PIL import Image
import pytesseract
import docx
from odf.opendocument import load as load_odt
from odf.text import P, H
from fpdf import FPDF
import pyttsx3

# ---------------------------
# Check Tesseract availability
# ---------------------------
def check_tesseract():
    try:
        pytesseract.get_tesseract_version()
        return True
    except Exception:
        return False

TESSERACT_AVAILABLE = check_tesseract()

# ---------------------------
# File extraction
# ---------------------------
def extract_text_from_file(uploaded_file):
    filename = uploaded_file.name.lower()
    file_type = uploaded_file.type or ""

    # TXT
    if file_type.startswith("text/") or filename.endswith(".txt"):
        return uploaded_file.read().decode("utf-8", errors="ignore")

    # PDF
    if filename.endswith(".pdf"):
        try:
            import PyPDF2
            reader = PyPDF2.PdfReader(uploaded_file)
            text = "".join([page.extract_text() or "" for page in reader.pages])
            if text.strip():
                return text
        except Exception:
            pass

        if TESSERACT_AVAILABLE:
            from pdf2image import convert_from_bytes
            images = convert_from_bytes(uploaded_file.getvalue())
            return "\n".join([pytesseract.image_to_string(img) for img in images])
        else:
            return "⚠️ OCR unavailable: Tesseract not installed."

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
    if file_type.startswith("image/") or filename.endswith((".png", ".jpg", ".jpeg")):
        if TESSERACT_AVAILABLE:
            return pytesseract.image_to_string(Image.open(uploaded_file))
        else:
            return "⚠️ OCR unavailable: Tesseract not installed."

    # ZIP
    if filename.endswith(".zip"):
        try:
            with zipfile.ZipFile(io.BytesIO(uploaded_file.getvalue())) as zf:
                texts = []
                for name in zf.namelist():
                    if name.lower().endswith(".txt"):
                        with zf.open(name) as f:
                            texts.append(f.read().decode("utf-8", "ignore"))
                return "\n\n".join(texts) if texts else "No readable files found in ZIP."
        except Exception:
            return "Could not read ZIP file."

    return "Unsupported file type."

# ---------------------------
# Glossary highlighting
# ---------------------------
def highlight_medical_terms(text):
    glossary_file = os.path.join(os.path.dirname(__file__), "glossary.json")
    with open(glossary_file, "r") as f:
        glossary = json.load(f)

    for term in glossary.keys():
        pattern = re.compile(fr"\b({term})\b", re.IGNORECASE)
        text = pattern.sub(r"<mark>\1</mark>", text)
    return text

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

# ---------------------------
# Save as PDF
# ---------------------------
def save_summary_as_pdf(summary, path="/mnt/data/summary.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for line in summary.split("\n"):
        pdf.multi_cell(0, 10, line)
    pdf.output(path)
    return path

# ---------------------------
# Text-to-speech
# ---------------------------
def speak_summary(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

