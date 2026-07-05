from models.popularity import PopularityRecommender
from models.evaluator import Evaluator
from data.loader import load_dataset

books = load_dataset("books_clean")
ratings = load_dataset("ratings_clean")

# TRAINING
# --------
model = PopularityRecommender()
model.fit(ratings, books, min_ratings=20)

model.save("artifacts/popularity.parquet")

# EVALUATION
# ----------
evaluator = Evaluator()

metrics = evaluator.evaluate(
    model.recommendations, 
    books=books
)

evaluator.display(metrics, model.recommendations)
evaluator.save(metrics, "artifacts/baseline_metrics.json")