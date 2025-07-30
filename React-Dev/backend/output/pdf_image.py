import fitz
import pytesseract
from PIL import Image
from io import BytesIO

# Set Tesseract path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\TesseractOCR\tesseract.exe"

def extract_text_with_ocr_fitz(pdf_path, page_list, dpi=300):
    ocr_text_by_page = {}

    with fitz.open(pdf_path) as doc:
        for page_num in page_list:
            page = doc.load_page(page_num)
            pix = page.get_pixmap(dpi=dpi)
            img_data = pix.tobytes("png")
            img = Image.open(BytesIO(img_data))
            text = pytesseract.image_to_string(img)
            ocr_text_by_page[page_num] = text.strip()
    
    return ocr_text_by_page

# Example usage
# pdf_path = "React-Dev/backend/output/mba_str_2020-21.pdf"
# scanned_pages = [4, 6, 11, 12, 13, 14, 16, 17, 20, 21, 27, 35, 43, 68, 69, 71, 78, 93, 94, 96, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123]

# ocr_text = extract_text_with_ocr_fitz(pdf_path, scanned_pages)

# # Print to verify
# for page_num, text in ocr_text.items():
#     print(f"\n--- Page {page_num + 1} ---\n{text}")
