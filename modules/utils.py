import io, re, json
from PIL import Image
import docx
from odf.opendocument import load as load_odt
from odf.text import P, H
from fpdf import FPDF
from gtts import gTTS
import easyocr

# Initialize EasyOCR reader
OCR_READER = easyocr.Reader(['en'], gpu=False)

# ---------------------------
# File text extraction
# ---------------------------
def extract_text_from_file(uploaded_file):
    """Extract text from TXT, PDF, DOCX, ODT, images, ZIP."""
    filename = uploaded_file.name.lower()
    file_type = uploaded_file.type or ""

    # TXT
    if file_type.startswith("text/") or filename.endswith(".txt"):
        return uploaded_file.read().decode("utf-8", errors="ignore")

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
        img = Image.open(uploaded_file)
        result = OCR_READER.readtext(np.array(img), detail=0)
        return "\n".join(result)

    return "Unsupported file type."

# ---------------------------
# Highlight terms
# ---------------------------
def highlight_medical_terms(text, glossary_file="modules/glossary.json"):
    """Highlight terms based on glossary."""
    with open(glossary_file) as f:
        glossary = json.load(f)
    for term in glossary.keys():
        pattern = re.compile(fr"\b({term})\b", re.IGNORECASE)
        text = pattern.sub(r"<mark>\1</mark>", text)
    return text

def explain_glossary_terms(summary, glossary_file="modules/glossary.json"):
    """Provide glossary explanations for terms present in summary."""
    with open(glossary_file) as f:
        glossary = json.load(f)
    explanations = [
        f"**{t.capitalize()}**: {d}" 
        for t, d in glossary.items() if re.search(fr"\b{t}\b", summary, re.IGNORECASE)
    ]
    return "### 🧾 Glossary\n" + "\n".join(explanations) if explanations else ""

# ---------------------------
# PDF / TXT / Audio
# ---------------------------
def save_summary_as_pdf(summary_text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for line in summary_text.split("\n"):
        pdf.multi_cell(0, 10, line)
    pdf_bytes = io.BytesIO()
    pdf.output(pdf_bytes)
    pdf_bytes.seek(0)
    return pdf_bytes

def save_summary_as_txt(summary_text):
    txt_bytes = io.BytesIO(summary_text.encode("utf-8"))
    return txt_bytes

def speak_summary(summary_text):
    tts = gTTS(summary_text)
    audio_bytes = io.BytesIO()
    tts.write_to_fp(audio_bytes)
    audio_bytes.seek(0)
    return audio_bytes

