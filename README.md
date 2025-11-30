# 📄 PDF Intelligence Extractor -- Advanced Streamlit App

An **AI-powered PDF Extraction App** built with **Streamlit**,
**PyMuPDF**, **Tesseract OCR**, and **OpenCV**.\
This tool extracts:

✔ OCR Text\
✔ Vector Text\
✔ Text Blocks\
✔ Tables (auto-detected)\
✔ Lines / Shapes (diagram detection)\
✔ Page Images\
✔ Downloadable JSON + TXT

------------------------------------------------------------------------

## 🚀 Features

### 🔍 **PDF Intelligence Extraction**

-   OCR extraction using **Tesseract**
-   Vector text extraction using **PyMuPDF**
-   Text blocks detection
-   Auto table detection
-   Diagram / line detection using **OpenCV**
-   Full JSON export

### 🖥️ **Streamlit UI**

-   Page-by-page expandable viewer
-   Optional features (OCR, tables, vector text, line detection)
-   Document previews
-   Download JSON and text summaries

------------------------------------------------------------------------

## 📦 Installation

### 1. Clone the repository

``` bash
git clone https://github.com/your-username/PDF-Intelligence-Extractor.git
cd PDF-Intelligence-Extractor
```

### 2. Install requirements

``` bash
pip install -r requirements.txt
```

### 3. Install Tesseract OCR (Windows)

Download installer:\
➡ https://github.com/UB-Mannheim/tesseract/wiki

Then set the path inside **app.py**:

``` python
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
```

------------------------------------------------------------------------

## ▶️ Run the App

``` bash
streamlit run app.py
```

------------------------------------------------------------------------

## 📁 Folder Structure

    📦 PDF-Intelligence-Extractor
    ├── app.py
    ├── requirements.txt
    ├── README.md
    ├── samples/
    └── screenshots/

------------------------------------------------------------------------

## 🧪 Example Output (JSON)

``` json
{
  "page_number": 1,
  "ocr_text": "...",
  "vector_text": "...",
  "tables": [...],
  "text_blocks": [...],
  "lines_detected": [...]
}
```

------------------------------------------------------------------------

## 📷 Screenshots

(Add your UI screenshot here)

    screenshots/ui_preview.png

------------------------------------------------------------------------

## 🛠️ Tech Stack

-   **Python**
-   **Streamlit**
-   **PyMuPDF (fitz)**
-   **OpenCV**
-   **Tesseract OCR**
-   **Pandas**
-   **Pillow**

------------------------------------------------------------------------

## 🧠 Future Enhancements

-   AI Summaries
-   Chapter-wise notes generator
-   MCQ generator from PDF
-   Text-to-speech for pages
-   File comparison tool

------------------------------------------------------------------------

## 🤝 Contributing

Pull requests are welcome!\
If you like this project, ⭐ star the repo!

------------------------------------------------------------------------

## 📜 License

MIT License --- free for personal & commercial use.
