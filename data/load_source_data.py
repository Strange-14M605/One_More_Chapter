from pathlib import Path
import zipfile
from kaggle.api.kaggle_api_extended import KaggleApi
# requires authentication via `kaggle auth login` command in terminal.

DATASET = "syedjaferk/book-crossing-dataset "
DOWNLOAD_PATH = Path(__file__).resolve().parents[1] / "data" / "raw" 

def main():
    print("Downloading dataset...")

    # Download the dataset from Kaggle 
    api = KaggleApi()
    api.dataset_download_files(DATASET, path=DOWNLOAD_PATH, quiet=False, unzip=True)

    print("Done!")

if __name__ == "__main__":
    main()