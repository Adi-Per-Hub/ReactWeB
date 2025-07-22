import fitz  # PyMuPDF
from dotenv import load_dotenv # Import the function to load .env file
from google import genai

def extract_text_pymupdf(file_path):
    full_text = ""
    no_text_pages = []
    # Open the PDF
    with fitz.open(file_path) as doc:
        for i, page in enumerate(doc):
            text = page.get_text()
            if not text:
                full_text+=f"Page {i + 1} has no extractable text."
                no_text_pages.append(i + 1)
                continue
            # print(f"\n--- Page {i + 1} ---\n")
            # print(text)
            full_text += text.strip() + "\n"
        print(len(no_text_pages))

    return full_text


# Load environment variables from .env file
load_dotenv()

# The genai client will now automatically pick up GEMINI_API_KEY
# if it's correctly set in your .env file
def extract_entities(extracted_text):
    client = genai.Client()

    prompt = """
    Analyze the following internship certificate excerpts and identify recurring entities across the documents. Specifically, extract and normalize (where needed) the following types of entities:
    1. Candidate Name
    2. Institute/College Name
    3. Company/Organization Name
    4. Internship Role or Department
    5. Internship Duration (Start Date – End Date or total duration)
    6. Certificate Date
    7. Certificate Number (if any)
    8. Email/Contact Details (optional but extract if present)
    9. Location of the organization (if mentioned)
    10. Subject or Title of Certificate (e.g., Internship Completion Certificate)

    Output the results in a structured table, grouped by page number. If a page contains too little information, mark it as 'Insufficient Data'. If multiple certificates are from the same organization (e.g., 'Careerdomain.org'), flag them as duplicates for potential grouping.

    ### Example Input:
    --- Page X ---
    Date: 15/Sep/2021  
    TO WHOMSOEVER IT MAY CONCERN  
    Subject: Internship Completion Certificate  
    This is to certify that Mr. Rohit Sharma has successfully completed his internship with JSHINE SOUK PVT. LTD. from 1st July 2021 to 31st August 2021.  
    CIN: U52601PB2017PTC046630  
    Company address: A-709, Level 7, Bestech Business Tower, Sector 66, Mohali 160066  
    www.jshine.in

    ### Example Output:
    | Page | Candidate Name | Institute Name | Company Name           | Role/Department | Duration                | Certificate Date | Cert. No. | Contact Info | Location               | Subject                      |
    |------|----------------|----------------|------------------------|------------------|--------------------------|------------------|-----------|---------------|------------------------|------------------------------|
    | X    | Rohit Sharma   | Not Mentioned  | JSHINE SOUK PVT. LTD. | Not Mentioned   | 1st Jul – 31st Aug 2021 | 15 Sep 2021      | N/A       | N/A           | Mohali, Punjab         | Internship Completion Cert. |

    Now begin extracting structured data for the provided pages below:
    """


    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )
    print(response.text)

if __name__ == "__main__":
    # Example usage
    # 🔍 Replace 'your_file.pdf' with your PDF file path
    pdf_path = input("Enter path to the PDF file: ").strip()
    extracted_text = extract_text_pymupdf(pdf_path)
    
    if extracted_text:
        # print(extracted_text)
        extract_entities(extracted_text)
    else:
        print("No text could be extracted from the PDF file.")