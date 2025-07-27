import fitz  # PyMuPDF
from pdf2image import convert_from_path
from PIL import Image
import pytesseract
import difflib
import os

# Set path to tesseract executable
pytesseract.pytesseract.tesseract_cmd = r"C:/Program Files/TesseractOCR/tesseract.exe"

def compare_ocr_results(pdf_path, page_number=0, dpi=300):
    results = {}

    # --- Method 1: Using PyMuPDF ---
    doc = fitz.open(pdf_path)
    page = doc.load_page(page_number)
    pix = page.get_pixmap(dpi=dpi)
    img1 = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    text_fitz = pytesseract.image_to_string(img1)
    results["fitz_text"] = text_fitz

    # --- Method 2: Using pdf2image ---
    images = convert_from_path(pdf_path, dpi=dpi, first_page=page_number+1, last_page=page_number+1)
    img2 = images[0]
    text_pdf2image = pytesseract.image_to_string(img2)
    results["pdf2image_text"] = text_pdf2image

    # --- Compare Results ---
    sm = difflib.SequenceMatcher(None, text_fitz, text_pdf2image)
    similarity = sm.ratio() * 100

    print("\n--- 🧠 OCR Comparison on Page", page_number + 1, "---")
    print(f"\n🔷 PyMuPDF (fitz) OCR:\n{text_fitz.strip()}")
    print(f"\n🔶 pdf2image OCR:\n{text_pdf2image.strip()}")
    print(f"\n📊 Similarity: {similarity:.2f}%")
    print(f"📏 Length: fitz = {len(text_fitz)}, pdf2image = {len(text_pdf2image)}")

    return {
        "fitz_text": text_fitz,
        "pdf2image_text": text_pdf2image,
        "similarity_percent": similarity,
        "fitz_length": len(text_fitz),
        "pdf2image_length": len(text_pdf2image)
    }

if __name__ == "__main__":
    pdf_path = "C:/Users/Admin/Documents/GitHub/ReactWeB/React-Dev/backend/output/mba_str_2020-21.pdf"  # Update with your PDF path
    page_number = 4  # Change to the desired page number (0-indexed)
    
    if os.path.exists(pdf_path):
        compare_ocr_results(pdf_path, page_number)
    else:
        print(f"Error: The file {pdf_path} does not exist.")