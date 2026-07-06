# One More Chapter

This repository contains a small ingestion / exploration starter for the Book-Crossing dataset from the Book-Crossing community. The goal is to prepare the dataset for recommendation, analysis, and modeling, while keeping the pipeline simple and reproducible.

## Understanding the Dataset

Source: [Book-Crossing dataset on Kaggle](https://www.kaggle.com/datasets/syedjaferk/book-crossing-dataset?select=BX-Books.csv)

BookCrossing is a platform where books are registered and then passed on from person to person- sometimes after the user gives it a rating. Here, we will deal with 3 tables: Books, Users and Ratings and try to recommend books using different algorithms like popularity based, collaborative filtering, content based filtering and I will even attempt a hybrid model. 

Note: This is real-world data and comes with complexities and lose-ends.

![Database schema](imgs/db_schema.png)

## Data exploration key observations
- `notebooks/exploration.ipynb` verifies raw data quality and schema issues before preprocessing
- Key observations: 
    - Book metadata needs cleanup: missing authors/publishers, bad years
    - Users require age/country normalization
    - Ratings are sparse and long-tailed, with many implicit zeros


## Storage (DuckDB and intermediate parquet files)

- Raw CSVs are loaded from `data/raw/` into DuckDB at `database/books.duckdb` via `src/data/ingest.py`
- Clean tables are built with `src/data/preprocess.py`:
  - `books_clean`
  - `users_clean`
  - `ratings_clean`
- Cleaned tables are exported as Parquet files into `data/processed/`

![Data storage and preprocessing](imgs/data.png)

Resources:
[DuckDB Python installation](https://duckdb.org/install/?platform=macos&environment=python)

## FastAPI endpoint

Serve recommended books on an endpoint by runnign this command:
` uvicorn src.api.app:app --reload ` and then going to `http://127.0.0.1:8000/recommend/popular`


## References and Acknowledgements

The [Book-Crossing dataset on Kaggle](https://www.kaggle.com/datasets/somnambwl/bookcrossing-dataset?select=Books.csv) is collected by Cai-Nicolas Ziegler with kind permission from Ron Hornbaker, CTO of Humankind Systems.


It is stated that the dataset is freely available for research use when acknowledged with the following reference:

> Improving Recommendation Lists Through Topic Diversification,
Cai-Nicolas Ziegler, Sean M. McNee, Joseph A. Konstan, Georg Lausen; Proceedings of the 14th International World Wide Web Conference (WWW '05), May 10-14, 2005, Chiba, Japan. 