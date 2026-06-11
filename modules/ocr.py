import streamlit as st
import pdfplumber
import docx
from PIL import Image
import easyocr
import numpy as np

@st.cache_resource
def get_reader():
    reader = easyocr.Reader(
        ['en'],
        gpu=False
    )
    return reader


def extract_text(uploaded_file):

    filename = uploaded_file.name.lower()

    # PDF
    if filename.endswith(".pdf"):

        text = ""

        with pdfplumber.open(uploaded_file) as pdf:

            for page in pdf.pages:

                page_text = page.extract_text()

                if page_text:
                    text += page_text + "\n"

        return text

    # DOCX
    elif filename.endswith(".docx"):

        doc = docx.Document(uploaded_file)

        return "\n".join(
            p.text for p in doc.paragraphs
        )

    # TXT
    elif filename.endswith(".txt"):

        return uploaded_file.read().decode(
            "utf-8",
            errors="ignore"
        )

    # Images
    elif filename.endswith(
        (".png", ".jpg", ".jpeg")
    ):

        image = Image.open(uploaded_file)

        image_np = np.array(image)

        reader = get_reader()

        result = reader.readtext(
            image_np,
            detail=0
        )

        return "\n".join(result)

    return "Unsupported file format."