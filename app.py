import streamlit as st
import pymupdf
import pytesseract
import numpy as np
import cv2
import pandas as pd
import json
from io import BytesIO
from PIL import Image


# (Change if installed somewhere else)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


# ----------------------------------------------------------
# Extract PDF Data
# ----------------------------------------------------------
def extract_pdf_advanced(file_bytes):
    doc = pymupdf.open(stream=file_bytes, filetype="pdf")
    output = []

    for page_num in range(len(doc)):
        page = doc[page_num]

        # ---------------- Page Image ----------------
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
        img_bytes = pix.tobytes("png")
        img = Image.open(BytesIO(img_bytes))

        # Convert for CV2
        img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

        # ---------------- OCR ----------------
        try:
            ocr_text = pytesseract.image_to_string(img_cv).strip()
        except:
            ocr_text = "OCR Error — Install Tesseract"

        # ---------------- Vector Text ----------------
        vector_text = page.get_text("text")

        # ---------------- Text Blocks ----------------
        blocks = [b[4] for b in page.get_text("blocks")]

        # ---------------- Table Extraction (heuristic) ----------------
        table_data = []
        tables = page.find_tables()

        if tables:
            for table in tables.tables:
                df = pd.DataFrame(table.extract())
                table_data.append(df.to_dict(orient="records"))

        # ---------------- Line / Shape Detection ----------------
        edges = cv2.Canny(img_cv, 100, 200)
        lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=80,
                                minLineLength=80, maxLineGap=10)
        detected_lines = []
        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line[0]
                detected_lines.append([int(x1), int(y1), int(x2), int(y2)])

        # ---------------- Build Page Output ----------------
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


# ----------------------------------------------------------
# Streamlit UI
# ----------------------------------------------------------
st.set_page_config(page_title="Advanced PDF Extractor", layout="wide")
st.title("📄 AI-Powered PDF Extractor – Advanced Version")

st.sidebar.header("Options")
show_images = st.sidebar.checkbox("Show Page Images", True)
show_ocr = st.sidebar.checkbox("Show OCR Text", True)
show_vector = st.sidebar.checkbox("Show Vector Text", False)
show_tables = st.sidebar.checkbox("Show Tables", True)
show_lines = st.sidebar.checkbox("Show Line Detection", False)

uploaded_file = st.file_uploader("Upload PDF", type="pdf")

if uploaded_file:
    st.success("PDF Uploaded Successfully")

    with st.spinner("Extracting PDF..."):
        data = extract_pdf_advanced(uploaded_file.read())

    st.subheader("📂 Extracted Data")

    # ---------------- SHOW PAGE OUTPUT ----------------
    for page in data:
        with st.expander(f"📄 Page {page['page_number']}", expanded=False):

            # Show image preview
            if show_images:
                st.image(page["image_bytes"], caption=f"Page {page['page_number']}")

            # OCR result
            if show_ocr:
                st.write("📝 **OCR Text:**")
                st.text(page["ocr_text"])

            # Vector text (PDF-drawn text)
            if show_vector:
                st.write("📌 **Vector Text:**")
                st.text(page["vector_text"])

            # Tables
            if show_tables:
                if len(page["tables"]) > 0:
                    st.write("📊 **Extracted Tables:**")
                    for t in page["tables"]:
                        df = pd.DataFrame(t)
                        st.dataframe(df)
                else:
                    st.info("No tables found on this page.")

            # Shape lines
            if show_lines:
                st.write("📐 **Detected Lines:**")
                st.write(page["lines_detected"])

    # ----------------------------------------------------
    # Downloads
    # ----------------------------------------------------
    st.subheader("⬇ Download Options")

    # JSON Download
    json_data = json.dumps(data, indent=2)
    st.download_button("Download JSON", data=json_data,
                       file_name="advanced_output.json",
                       mime="application/json")

    # TXT Download
    txt = ""
    for page in data:
        txt += f"--- Page {page['page_number']} ---\n"
        txt += page["ocr_text"] + "\n\n"

    st.download_button("Download Full Text",
                       data=txt.encode("utf-8"),
                       file_name="pdf_text.txt",
                       mime="text/plain")

    st.success("Processing Completed!")

