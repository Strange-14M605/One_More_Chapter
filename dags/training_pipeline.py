# TRAINING PIPELINE
# frequency: manual/weekly

# 1. load features from DuckDB
# 2. fit the model 
# 3. evaluate model perf.
# 4. save recommendations
# 5. save metrics

# Output: 
# a. artifacts/models/{model_type}/{version}/recommendations.json    -> acts as a backup of the recommendations
# b. artifacts/models/{model_type}/{version}/metrics.json            -> to compare across versions

# possible future work:
# multiple recommender algorithms
# automated retraining with MLflow model registry
# hyperparameter tuning

import sys
from pathlib import Path
from airflow.sdk import dag, task

project_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_root))

@dag(
    dag_id="training_pipeline",
    schedule = None,
    catchup = False, 
)

def training_pipeline():
    @task
    def train_model():
        from src.models.popularity import fit
        from src.data.loader import load_dataset
        books = load_dataset("books_clean")
        ratings = load_dataset("ratings_clean")
        fit(ratings, books, min_ratings=20)

    @task
    def evaluate_model():
        from src.models.evaluator import evaluate
        from src.data.loader import load_dataset
        books = load_dataset("books_clean")
        evaluate(books)

    train_model() >> evaluate_model()
training_pipeline()