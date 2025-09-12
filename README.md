# 🏥 Medical Report Summarizer

An offline-first **Streamlit app** that:
- Extracts text from medical **PDFs, DOCX, ODT, and images** (using Tesseract OCR).
- Highlights medical glossary terms.
- Provides simple explanations for complex terms.
- Exports summary as **PDF**.
- Supports **Text-to-Speech** for accessibility.

---

## 🚀 Features
✅ Works **100% offline** – no paid API keys required.  
✅ Multi-file support: PDF, DOCX, ODT, Images (JPG, PNG).  
✅ Export summary as **PDF**.  
✅ **Glossary-based highlighting** for medical terms.  
✅ **Text-to-Speech** integration.  

---

## 📂 Project Structure
```
medical-report-summarizer/
│── app.py
│── modules/utils.py
│── modules/summarizer.py
│── modules/glossary.json
│── requirements.txt
│── packages.txt
│── runtime.txt
│── Procfile
│── Dockerfile
│── README.md
```

---

## 🖥️ Run Locally

```bash
# Clone repo
git clone https://github.com/sahithi2510/medical-report-summarizer.git
cd medical-report-summarizer

# Install dependencies
pip install -r requirements.txt

# Run app
streamlit run app.py
```

---

## 🌐 Deployment Options

### 1️⃣ Streamlit Cloud
- Add `packages.txt` with:
  ```txt
  tesseract-ocr
  libtesseract-dev
  ```
- Push repo to GitHub → Deploy on [Streamlit Cloud](https://streamlit.io/cloud).

⚠️ **Known Issues on Streamlit Cloud**
- Sometimes `tesseract-ocr` fails to install → `⚠️ Tesseract OCR is not installed.`  
- Limited system access → may block some `pyttsx3` functionality.  
- Deployment can fail with `installer returned a non-zero exit code`.  
- Google Vision API integration requires **billing enabled** → not free.  

✅ **Workaround**: If Streamlit fails, use **Render or Railway**.

---

### 2️⃣ Render (Recommended)
- Add `Procfile`:
  ```bash
  web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
  ```
- Add `runtime.txt`:
  ```
  python-3.11
  ```
- Render automatically builds & installs from `requirements.txt` and `packages.txt`.

---

### 3️⃣ Railway
- Same as Render.  
- Connect GitHub repo → it auto-builds with `requirements.txt`.  
- Supports persistent deployments.

---

### 4️⃣ Docker (Universal Option)
```bash
docker build -t medical-report-summarizer .
docker run -p 8501:8501 medical-report-summarizer
```

Works everywhere: local, cloud, or any container platform.

---

## Deployment Notes

### Streamlit Cloud

- **Tesseract OCR** and **pyttsx3** cannot be reliably installed due to system-level dependencies.  
- For Streamlit, only gTTS audio works.  
- Some PDF/TXT files may face encoding issues.

### Alternative Platforms

- **Google Colab**: Works if you install Tesseract using `!apt install tesseract-ocr`.  
- **Local PC**: Fully functional. Recommended for demos.  
- **Docker**: Can create a custom image with all dependencies.  

---

## Contribution Guide

- **Fixing OCR Issues**: Ensure Tesseract path is correctly set in `utils.py`.  
- **Improving TTS**: Replace pyttsx3 with gTTS for web compatibility.  
- **Enhancing Summarization**: Use NLP models for better summaries.  
- **PDF/TXT Generation**: Handle Unicode characters properly to avoid encoding errors.  

---

## Disclaimer

This project is intended for educational purposes and interview demos. It is **not a certified medical tool**. Always consult professionals for medical interpretations.

---

## License

MIT License



## 👨‍💻 Author
Developed by **Dhanakudharam Sahithi** (B.Tech CSE).  
Contact: sahithidhanakudharam25@gmail.com 
