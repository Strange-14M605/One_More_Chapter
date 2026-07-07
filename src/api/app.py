from fastapi import FastAPI
from src.deployment.service import recommend

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Welcome to One More Chapter!"}

@app.get("/recommend/popular")
def recommend_popular(top_k: int = 10):
    recommendations = recommend(top_k)
    return recommendations.to_dict(orient="records")