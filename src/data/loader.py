from pathlib import Path
import pandas as pd

DATA_DIR = Path("data/processed")

def load_dataset(name: str):
    return pd.read_parquet(DATA_DIR / f"{name}.parquet")