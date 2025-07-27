import os

import pandas as pd

import os
import pandas as pd

# Get current script directory
script_dir = os.path.dirname(os.path.abspath(__file__))

# Join with your CSV file name
csv_path = os.path.join(script_dir, 'mba_str_2020-21_processed.csv')

df=pd.read_csv(csv_path)

def clean_dataframe(df):
    # Exclude 'Page' column from the check
    cols_to_check = df.columns.difference(['Page'])

    # Drop rows where all fields (except Page) are 'N/A' or empty/whitespace
    df_cleaned = df[~df[cols_to_check].apply(lambda row: all(x in ['N/A', '', None] or str(x).strip() == '' for x in row), axis=1)]
    
    return df_cleaned
result = clean_dataframe(df)
result.to_csv("cleaned_mba_str_2020-21.csv", index=False)
print(result)