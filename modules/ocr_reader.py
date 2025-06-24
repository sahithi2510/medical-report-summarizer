from PIL import Image
import pdfplumber

def extract_text_from_file(file):
    if file.type == "application/pdf":
        with pdfplumber.open(file) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text() or ""
            return text if text.strip() else "No extractable text found in PDF."

    elif "image" in file.type:
        return "Image-based reports are not supported unless OCR is enabled."

    else:
        return "Unsupported file format."
