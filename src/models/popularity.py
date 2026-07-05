import pandas as pd
from pathlib import Path

class PopularityRecommender:
    def __init__(self):
        self.recommendations = None

    def fit(self, ratings: pd.DataFrame , books: pd.DataFrame, min_ratings: int = 50):
        
        # here we calculate number and average of ratings for each book
        consider_books = (
            ratings.groupby("ISBN")["Book_Rating"]
            .agg(
                Number_of_Ratings="count",
                Average_Rating="mean"
            )
            .reset_index()
        )

        # filter out books with less than min_ratings ratings to remove noise.
        # e.g. book with (no_rating=100 && avg_rating=4.8) is better than book with (no_rating=1 && avg_rating=5.0)
        consider_books = consider_books[consider_books["Number_of_Ratings"] >= min_ratings]

        # merge with books to get book titles and other info
        consider_books = consider_books.merge(
            books,
            how="left",
            on="ISBN"
        )

        # sort by average rating (highest avg rating is recommended)
        # for books with same averge rating, sort by number of ratings (highest number of ratings is recommended)
        self.recommendations = (
            consider_books.sort_values(
                by=["Average_Rating", "Number_of_Ratings"],
                ascending=[False, False]
            )
            .reset_index(drop=True)
        )

    def recommend(self, n=10):
        return self.recommendations.head(n)

    def save(self, path: str):
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        self.recommendations.to_parquet(path, index=False)

    def load(self, path: str):
        self.recommendations = pd.read_parquet(path)