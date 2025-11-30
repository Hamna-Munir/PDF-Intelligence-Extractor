import streamlit as st
import fitz   # <-- pymupdf is imported as fitz
import pytesseract
import numpy as np
import cv2
import pandas as pd
import json
from io import BytesIO
from PIL import Image

# REMOVE the Windows-only path
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def extract_pdf_advanced(file_bytes):
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    output = []

    for page_num in range(len(doc)):
        page = doc[page_num]

        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
        img_bytes = pix.tobytes("png")
        img = Image.open(BytesIO(img_bytes))
        img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

        try:
            ocr_text = pytesseract.image_to_string(img_cv).strip()
        except:
            ocr_text = "OCR Error — Tesseract not installed"

        vector_text = page.get_text("text")
        blocks = [b[4] for b in page.get_text("blocks")]

        table_data = []
        tables = page.find_tables()
        if tables:
            for table in tables.tables:
                df = pd.DataFrame(table.extract())
                table_data.append(df.to_dict(orient="records"))

        edges = cv2.Canny(img_cv, 100, 200)
        lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=80,
                                minLineLength=80, maxLineGap=10)
        detected_lines = []
        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line[0]
                detected_lines.append([int(x1), int(y1), int(x2), int(y2)])

        output.append({
            "page_number": page_num + 1,
            "ocr_text": ocr_text,
            "vector_text": vector_text,
            "text_blocks": blocks,
            "tables": table_data,
            "lines_detected": detected_lines,
            "image_bytes": img_bytes
        })

    return output

