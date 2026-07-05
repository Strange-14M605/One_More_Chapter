from models.popularity import PopularityRecommender
from data.loader import load_dataset

books = load_dataset("books_clean")
ratings = load_dataset("ratings_clean")

model = PopularityRecommender()
model.fit(ratings, books)

model.save("artifacts/popularity.parquet")

print(model.recommend(10))