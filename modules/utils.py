import os
import re
import json
import zipfile
import io
import mimetypes
import requests

from pdf2image import convert_from_bytes
from PIL import Image
import PyPDF2
import docx
from odf.opendocument import load as load_odt
from odf.text import P, H
import pypandoc
import pyttsx3
from fpdf import FPDF

# ----------------- Cloud OCR setup -----------------
OCR_SPACE_API_KEY = "YOUR_OCR_SPACE_API_KEY"  # Replace with your key
OCR_SPACE_URL = "https://api.ocr.space/parse/image"

def ocr_image_cloud(file_input):
    """
    Perform OCR using OCR.space cloud API.
    Accepts:
      - bytes
      - file-like object (with .read())
    """
    # Ensure we always have bytes
    if hasattr(file_input, "read"):
        file_input.seek(0)
        file_bytes = file_input.read()
    elif isinstance(file_input, bytes):
        file_bytes = file_input
    else:
        raise ValueError(f"OCR input must be bytes or file-like object, got {type(file_input)}")

    files = {"file": ("file", file_bytes)}
    payload = {"apikey": OCR_SPACE_API_KEY, "language": "eng"}
    try:
        response = requests.post(OCR_SPACE_URL, files=files, data=payload)
        result = response.json()
        if result.get("IsErroredOnProcessing"):
            return "OCR failed: " + result.get("ErrorMessage", ["Unknown error"])[0]
        return result["ParsedResults"][0]["ParsedText"]
    except Exception as e:
        return f"OCR request failed: {e}"

def get_bytes(uploaded_file):
    """Return bytes from a Streamlit UploadedFile safely."""
    uploaded_file.seek(0)
    return uploaded_file.getvalue()

# ----------------- Text Extraction -----------------
def extract_text_from_file(uploaded_file):
    """Extract text from different file formats with robust type detection."""
    filename = uploaded_file.name.lower()
    file_type = uploaded_file.type or mimetypes.guess_type(filename)[0] or ""

    # TXT
    if file_type.startswith("text/") or filename.endswith(".txt"):
        return uploaded_file.read().decode("utf-8", errors="ignore")

    # PDF
    if filename.endswith(".pdf") or "pdf" in file_type:
        try:
            reader = PyPDF2.PdfReader(uploaded_file)
            text = "".join([page.extract_text() or "" for page in reader.pages])
            if text.strip():
                return text
        except Exception:
            pass
        try:
            images = convert_from_bytes(get_bytes(uploaded_file))
            text_pages = []
            for img in images:
                with io.BytesIO() as buf:
                    img.save(buf, format="PNG")
                    buf.seek(0)
                    text_pages.append(ocr_image_cloud(buf))
            return "\n".join(text_pages)
        except Exception:
            return "OCR failed for scanned PDF."

    # DOCX
    if filename.endswith(".docx") or "wordprocessingml.document" in file_type:
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
        return ocr_image_cloud(uploaded_file)

    # RTF
    if filename.endswith(".rtf"):
        raw = uploaded_file.read().decode("utf-8", errors="ignore")
        return pypandoc.convert_text(raw, 'plain', format='rtf')

    # ZIP
    if filename.endswith(".zip"):
        try:
            with zipfile.ZipFile(io.BytesIO(get_bytes(uploaded_file))) as zf:
                texts = []
                for name in zf.namelist():
                    if name.lower().endswith('.txt'):
                        with zf.open(name) as m:
                            texts.append(m.read().decode('utf-8', 'ignore'))
                return "\n\n".join(texts) if texts else "No readable files found in ZIP."
        except Exception:
            return "Could not read ZIP file."

    return f"Unsupported or unrecognized file type: {filename}"

# ----------------- Highlight Medical Terms -----------------
def highlight_medical_terms(text):
    """Highlight medical terms based on glossary.json."""
    glossary_file = os.path.join(os.path.dirname(__file__), "glossary.json")
    with open(glossary_file, "r") as f:
        glossary = json.load(f)
    for term in glossary.keys():
        pattern = re.compile(fr"\b({term})\b", re.IGNORECASE)
        text = pattern.sub(r"<mark>\1</mark>", text)
    return text

# ----------------- Glossary Explanations -----------------
def explain_glossary_terms(summary):
    """Add simple glossary explanations for medical terms in the summary."""
    glossary_file = os.path.join(os.path.dirname(__file__), "glossary.json")
    with open(glossary_file, "r") as f:
        glossary = json.load(f)
    explanations = [
        f"**{t.capitalize()}**: {d}"
        for t, d in glossary.items()
        if re.search(fr"\b{t}\b", summary, re.IGNORECASE)
    ]
    return "### 🧾 Glossary\n" + "\n".join(explanations) if explanations else ""

# ----------------- Save Summary as PDF -----------------
def save_summary_as_pdf(summary):
    """Save the summary as a PDF file and return the path."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for line in summary.split("\n"):
        pdf.multi_cell(0, 10, line)
    path = "/mnt/data/summary.pdf"
    pdf.output(path)
    return path

# ----------------- Text-to-Speech -----------------
def speak_summary(text):
    """Read the summary aloud using text-to-speech."""
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


