from pathlib import Path
import pandas as pd
from src.deployment.config import MODEL_PATH

def recommend(n=10):
    return load_recommendations(MODEL_PATH).head(n)

def load_recommendations(path: str):
    return pd.read_parquet(Path(path))