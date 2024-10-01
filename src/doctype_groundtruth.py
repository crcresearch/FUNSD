import gspread
from urllib.parse import urlparse
from google.oauth2.service_account import Credentials
import pandas as pd
import os

def extract_and_save_data(credentials_path, spreadsheet_key, annot_columns, annot_fname, counter_fname):
    """
    Extracts data from the Google Sheets document and saves specific sheets to CSV files.

    Args:
    - credentials_path (str): Path to the Google service account JSON credentials file.
    - spreadsheet_key (str): The key or ID of the Google Spreadsheet.
    - annot_columns (list): List of columns to be extracted from the 'annotation' sheet.
    - annot_fname (str): Path to save the annotation CSV file.
    - counter_fname (str): Path to save the counter CSV file.
    """
    # Define the scope and credentials
    SCOPE = ['https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive']
    credentials = Credentials.from_service_account_file(credentials_path, scopes=SCOPE)

    # Authorize and connect to Google Sheets
    client = gspread.authorize(credentials)
    spreadsheet = client.open_by_key(spreadsheet_key)

    def extract_sheet_data(spreadsheet, sheet_name):
        """Extract sheet data and convert it to a pandas DataFrame."""
        sheet = spreadsheet.worksheet(sheet_name)  # Access specific sheet by name
        sheet_data = sheet.get_all_values()         # Extract all values from the sheet
        df = pd.DataFrame(sheet_data)               # Convert to DataFrame
        df.columns = df.iloc[0]                     # Set the first row as column headers
        df = df.drop(0).reset_index(drop=True)      # Drop the header row and reset index
        return df

    # Extract and save annotation data
    annotation_df = extract_sheet_data(spreadsheet, "annotation")
    # Check if the required columns exist
    if set(annot_columns).issubset(annotation_df.columns):
        # Extract the filename from 'image_path' URL
        if 'image_path' in annotation_df.columns:
            annotation_df['image_filename'] = annotation_df['image_path'].apply(
                lambda x: os.path.basename(urlparse(x).path) if pd.notnull(x) else None
            )

        # Reorder columns to place 'image_filename' as the first column
        cols = ['image_filename'] + [col for col in annotation_df.columns if col != 'image_filename']
        annot_data = annotation_df[cols].copy()
        
        # Select only image_filename and annot_columns for saving
        columns_to_save = ['image_filename'] + [col for col in annot_columns if col in annotation_df.columns]
        annot_data = annotation_df[columns_to_save].copy()
    
        annot_data.to_csv(annot_fname, index=False)
        print(f'Annotation data saved to: {annot_fname}')
    else:
        print(f"Columns {annot_columns} not found in 'annotation' sheet")

    # Extract and save counter data
    counter_df = extract_sheet_data(spreadsheet, "counter")
    # Select first 4 columns if they exist
    counter_columns = counter_df.columns[:4]
    if len(counter_columns) > 0:
        counter_data = counter_df[counter_columns].copy()
        counter_data.to_csv(counter_fname, index=False)
        print(f'Counter data saved to: {counter_fname}')
    else:
        print("No columns found in 'counter' sheet")

    print('Done!')