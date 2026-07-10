from pathlib import Path
from kaggle.api.kaggle_api_extended import KaggleApi
# requires authentication via `kaggle auth login` command in terminal.

DATASET = "syedjaferk/book-crossing-dataset "
DOWNLOAD_PATH = Path(__file__).resolve().parents[1] / "data" / "raw" 

def get_raw_data():
    # Download the dataset from Kaggle 
    api = KaggleApi()
    api.authenticate()
    api.dataset_download_files(DATASET, path=DOWNLOAD_PATH, quiet=False, unzip=True)