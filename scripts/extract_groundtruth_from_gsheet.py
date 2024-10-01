import sys
sys.path.append('src/')
from doctype_groundtruth import extract_and_save_data


# Define paths and Google Sheets parameters
credentials_path = 'funsd-437312-d8e5db921a91.json'
spreadsheet_key_test = "1P-m192sJDAEdfWtN_KZ5jv2XN9PdA-Iracq7repyeVc"
spreadsheet_key_train = "1F3f-qDrwpPJkkePQ12eIZwehZvzLZg-fX3Q36F_Q4iI"
annot_columns = ['doctype_id', 'doctype_label']
dataset_path_test='datasets/FUNSD/testing_data/' 
dataset_path_train='datasets/FUNSD/training_data/'

# FUNSD training data groundtruth
extract_and_save_data(
    credentials_path=credentials_path,
    spreadsheet_key=spreadsheet_key_test,
    annot_columns=annot_columns,
    annot_fname=f"{dataset_path_test}/doctype_annotation.csv",
    counter_fname=f"{dataset_path_test}/doctype_counter.csv"
)

# FUNSD training data groundtruth
extract_and_save_data(
    credentials_path=credentials_path,
    spreadsheet_key=spreadsheet_key_train,
    annot_columns=annot_columns,
    annot_fname=f"{dataset_path_train}/doctype_annotation.csv",
    counter_fname=f"{dataset_path_train}/doctype_counter.csv"
)
