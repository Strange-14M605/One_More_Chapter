# DATA PIPELINE
# frequency: daily

# 1. check raw exists
# 2. load raw tables (pandas)
# 3. preprocess/clean
# 4. load cleaned data into DuckDB
# 5. validate data quality using great expectations
# 6. feature engineering
# 7. load features in DuckDB

# Output: 
# DuckDB.books, DuckDB.users, DuckDB.ratings
# DuckDB.book_features, DuckDB.user_features, DuckDB.rating_features

# possible future work:
# Add Great Expectations feature versioning
# Load raw data from a cloud store instead; spark