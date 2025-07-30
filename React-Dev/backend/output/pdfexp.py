import fitz
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


from output.pdf_image import extract_text_with_ocr_fitz
def extract_text_pymupdf(file_path):
    full_text = ""
    no_text_pages = []
    # Open the PDF
    with fitz.open(file_path) as doc:
        for i, page in enumerate(doc):
            text = page.get_text()
            if not text:
                full_text+=f"Page {i + 1} has no extractable text."
                no_text_pages.append(i)
                continue
            # print(f"\n--- Page {i + 1} ---\n")
            # print(text)
            full_text += text.strip() + "\n"
        print(len(no_text_pages))

    return full_text,no_text_pages


text, no_text_pages = extract_text_pymupdf("React-Dev/backend/output/mba_str_2020-21.pdf")
print(text)
print("No text pages:", no_text_pages)
text_no_text_pages = extract_text_with_ocr_fitz("React-Dev/backend/output/mba_str_2020-21.pdf", no_text_pages)