from fastapi import FastAPI
from src.models.popularity import PopularityRecommender

model = PopularityRecommender()
model.load("artifacts/popularity.parquet")

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Welcome to One More Chapter!"}

@app.get("/recommend/popular")
def recommend_popular(top_k: int = 10):
    recommendations = model.recommend(top_k)
    return recommendations.to_dict(orient="records")