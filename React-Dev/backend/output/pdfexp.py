import pdfplumber
import os

# === Function to Open PDF with pdfplumber and Display Text === #
def open_pdf_with_pdfplumber(file_path):
    extracted_text = " "
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")

    if not file_path.lower().endswith(".pdf"):
        raise ValueError("Please provide a valid PDF file.")
    no_text_pages = []

    with pdfplumber.open(file_path) as pdf:
        total_pages = len(pdf.pages)
        print(f"Total Pages: {total_pages}\n")

        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            if text:
                snippet = text.strip()[:200]
                extracted_text += f"--- Page {i + 1} Preview ---"+snippet + "\n\n" 
            else :
                print(f"Page {i + 1} has no extractable text.")
                no_text_pages.append(i + 1)
                extracted_text +=f"--- Page {i + 1} Preview ---\n No extractable text."+ "\n\n"
        print(f"Pages with no extractable text: {no_text_pages if no_text_pages else 'All pages have content.'}"    ,len (no_text_pages))
    return extracted_text

# === Entry Point === #
if __name__ == "__main__":
    path = input("Enter path to the PDF file: ").strip()
    extract_text=open_pdf_with_pdfplumber(path)
    if extract_text:
        print(extract_text)
    else:
        print("No text could be extracted from the PDF file.")
