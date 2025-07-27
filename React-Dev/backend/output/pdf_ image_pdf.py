import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io

# Set this if Tesseract is not in PATH
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\TesseractOCR\tesseract.exe"

def extract_text_with_fitz_and_ocr(pdf_path):
    extracted_text_by_page = {}

    with fitz.open(pdf_path) as doc:
        for i, page in enumerate(doc):
            text = page.get_text().strip()
            if text:
                # extracted_text_by_page[i] = text
                pass
            else:
                # Render page as image using fitz
                pix = page.get_pixmap(dpi=300)
                img_data = pix.tobytes("png")
                img = Image.open(io.BytesIO(img_data))
                ocr_text = pytesseract.image_to_string(img).strip()
                extracted_text_by_page[i] = ocr_text or "[No text found even with OCR]"

    return extracted_text_by_page

# --- Main block ---
if __name__ == "__main__":
    pdf_path = "React-Dev/backend/output/mba_str_2020-21.pdf"
    pagewise_text = extract_text_with_fitz_and_ocr(pdf_path)

    for page_num, text in pagewise_text.items():
        print(f"\n--- Page {page_num + 1} ---\n{text}")
