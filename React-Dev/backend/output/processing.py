import fitz  # PyMuPDF
from dotenv import load_dotenv # Import the function to load .env file
from google import genai
from output.entity_extractor import extract_entities_to_dataframe, clean_dataframe


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

    return full_text


# Load environment variables from .env file

# The genai client will now automatically pick up GEMINI_API_KEY
# if it's correctly set in your .env file
def extract_entities(extracted_text): 
    
    client = genai.Client()

    prompt = (
    f"Extract the following fields from this content:\n{extracted_text}\n\n"
    "Fields to extract:\n"
    "1) Name 2) Institute 3) Company 4) Role 5) Duration 6) Date 7) Cert No 8) Contact 9) Location 10) Subject.\n"
    "Group output by page. Mark missing values as 'N/A'. Flag duplicates if the same company is found on multiple pages.\n\n"
    "Example Input:\n"
    "--- Page 1 ---\n"
    "Date: 15/Sep/2021. Mr. Rohit Sharma completed his internship with JSHINE SOUK PVT. LTD. from 1st July to 31st August 2021. Address: Mohali.\n\n"
    "Example Output:\n"
    "Name - Rohit Sharma\n"
    "Institute - N/A\n"
    "Company - JSHINE SOUK PVT. LTD.\n"
    "Role - N/A\n"
    "Duration - 1 Jul – 31 Aug 2021\n"
    "Date - 15 Sep 2021\n"
    "Cert No - N/A\n"
    "Contact - N/A\n"
    "Location - Mohali\n"
    "Subject - Internship Completion Cert"
)




    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )
    return (response.text)


def pipeline(pdf_path):
    load_dotenv()

        # Example usage
    # 🔍 Replace 'your_file.pdf' with your PDF file path
    # pdf_path = input("Enter path to the PDF file: ").strip()
    extracted_text = extract_text_pymupdf(pdf_path)
    print (    type (extracted_text)) 
    if extracted_text:
        # print(extracted_text)
        processed_text = extract_entities(extracted_text)
        print("Processed Text:\n", processed_text)
        entities = extract_entities_to_dataframe(processed_text)
        cleaned_entities = clean_dataframe(entities)
        if not cleaned_entities.empty :
            print (type(entities))
            print("Entities Extracted:\n", entities)
            return cleaned_entities
        #     print(tabulate(entities, headers="keys", tablefmt="grid"))
        # else :
        #     print("No entities could be extracted from the processed text.")
    else:
        print("No text could be extracted from the PDF file.")