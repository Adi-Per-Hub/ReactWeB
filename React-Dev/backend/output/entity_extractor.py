import re
import pandas as pd

def extract_entities_to_dataframe(text):
    rows = []
    pages = re.split(r"Page\s*-\s*(\d+)", text)

    for i in range(1, len(pages), 2):
        page_num = int(pages[i])
        page_text = pages[i + 1].strip()

        fields = {
            "Page": page_num,
            "Name": "N/A",
            "Institute": "N/A",
            "Company": "N/A",
            "Role": "N/A",
            "Duration": "N/A",
            "Date": "N/A",
            "Cert No": "N/A",
            "Contact": "N/A",
            "Location": "N/A",
            "Subject": "N/A"
        }

        for line in page_text.splitlines():
            if "-" not in line:
                continue
            key_part, val_part = line.split("-", 1)
            key = key_part.strip().title()
            val = val_part.strip()
            if key in fields:
                fields[key] = val

        rows.append(fields)

    return pd.DataFrame(rows)

def clean_dataframe(df):
    # Exclude 'Page' column from the check
    cols_to_check = df.columns.difference(['Page'])

    # Drop rows where all fields (except Page) are 'N/A' or empty/whitespace
    df_cleaned = df[~df[cols_to_check].apply(lambda row: all(x in ['N/A', '', None] or str(x).strip() == '' for x in row), axis=1)]
    
    return df_cleaned

# # ==== Sample Usage ====
# text = """Processed Text:
# Page - 1
# Name - Siddhant Pant
# Institute - Army Institute of Management and Technology, Greater Noida
# Company - Brainstorming Canadian Immigration Consulting Services Inc. [BCICS Inc.]
# Role - Immigration Graduate Program, Immigration practices for International Student Recruitment Programs, and PR Programs
# Duration - 03 (three) months 26.07.2021 to 25.10.2021
# Date - October 29th, 2021
# Cert No - N/A
# Contact - Kaustubh Kulkarni
# Location - Saskatchewan, Canada
# Subject - Internship Certificate
# """

# df = extract_entities_to_dataframe(text)

# # === Save to CSV ===
# df.to_csv("internship_entities.csv", index=False)

# # Optional: print it
# print(df)
