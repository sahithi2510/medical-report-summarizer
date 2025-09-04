import streamlit as st
from google.cloud import vision
from google.oauth2 import service_account
from PyPDF2 import PdfReader
from pdf2image import convert_from_bytes
import io

@st.cache_resource
def setup_vision_client():
    # Load credentials from Streamlit secrets
    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"]
    )
    return vision.ImageAnnotatorClient(credentials=credentials)

# Initialize Vision API client
vision_client = setup_vision_client()

def extract_images_from_pdf(uploaded_file):
    images = convert_from_bytes(uploaded_file.read())
    return images

def extract_text_from_image(image):
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()

    response = vision_client.document_text_detection({'content': img_byte_arr})
    texts = response.text_annotations
    return texts[0].description if texts else ""

def extract_text_from_pdf(uploaded_file):
    pdf = PdfReader(uploaded_file)
    text = ""
    for page in pdf.pages:
        text += page.extract_text() or ""
    return text
