from fastapi import FastAPI, HTTPException
from models import Review
from sentiment import predict_rating
from tfidf_cache import build_tfidf_cache, update_tfidf_cache
from recommendation import get_recommendations
from db import movies_collection
from bson import ObjectId

app = FastAPI()

@app.post("/predict-rating")
async def rating_prediction(review: Review):
    return predict_rating(review)

@app.get("/build-tfidf-cache")
async def build_cache():
    return build_tfidf_cache()

@app.get("/update-tfidf-cache/{movie_id}")
async def update_cache(movie_id: str):
    movie = movies_collection.find_one({"_id": ObjectId(movie_id)})
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found.")
    return update_tfidf_cache(movie)

@app.get("/recommend-movies/{user_id}")
async def recommend_movies(user_id: str, top_n: int = 5):
    return get_recommendations(user_id, top_n)
