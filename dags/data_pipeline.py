# DATA PIPELINE
# frequency: daily

# 1. check raw exists
# 2. load raw tables (pandas)
# 3. preprocess/clean
# 4. load cleaned data into DuckDB
# 5. validate data quality using great expectations (todo)
# 6. feature engineering
# 7. load features in DuckDB

# Output: 
# DuckDB.books, DuckDB.users, DuckDB.ratings
# DuckDB.book_features, DuckDB.user_features, DuckDB.rating_features

# possible future work:
# Add Great Expectations feature versioning
# Load raw data from a cloud store instead; spark

import sys
from pathlib import Path
from airflow.sdk import dag, task

project_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_root))

@dag(
    dag_id="data_pipeline",
    schedule = None,
    catchup = False, 
)

def data_pipeline():
    @task
    def load_raw_tables():
        from src.data.ingest import create_table
        create_table("books", project_root / "data/raw/BX-Books.csv")
        create_table("users", project_root / "data/raw/BX-Users.csv")
        create_table("ratings", project_root / "data/raw/BX-Book-Ratings.csv")

    @task
    def clean_tables():
        from src.data.preprocess import preprocess_books, preprocess_users, preprocess_ratings, export_parquet
        preprocess_books()
        preprocess_users()
        preprocess_ratings()

        export_parquet("books_clean")
        export_parquet("users_clean")
        export_parquet("ratings_clean")

    load_raw_tables() >> clean_tables()

data_pipeline()