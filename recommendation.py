import numpy as np
import os
from bson import ObjectId
from db import movies_collection, ratings_collection
from tfidf_cache import build_tfidf_cache

TFIDF_CACHE_FILE = "tfidf_matrix.npy"
MOVIE_IDS_FILE = "movie_ids.npy"

def get_recommendations(user_id, top_n=5):
    """Recommends movies for a user based on liked movies."""
    liked_movies = list(ratings_collection.find({"user_id": ObjectId(user_id), "rate": {"$gte": 4}}, {"movie_id": 1}))
    print(liked_movies)
    print(user_id)
    if not liked_movies:
        return {"error": "No liked movies found."}

    liked_movie_ids = [str(m["movie_id"]) for m in liked_movies]

    if not os.path.exists(TFIDF_CACHE_FILE) or not os.path.exists(MOVIE_IDS_FILE):
        build_tfidf_cache()

    tfidf_matrix = np.load(TFIDF_CACHE_FILE)
    movie_ids = np.load(MOVIE_IDS_FILE, allow_pickle=True).tolist()

    liked_indices = [movie_ids.index(m_id) for m_id in liked_movie_ids if m_id in movie_ids]
    if not liked_indices:
        return {"error": "Liked movies not found in cache."}

    user_preference_vector = np.mean(tfidf_matrix[liked_indices], axis=0)
    similarity_scores = np.dot(tfidf_matrix, user_preference_vector)

    recommended_indices = similarity_scores.argsort()[-top_n:][::-1]
    recommended_movie_ids = [movie_ids[i] for i in recommended_indices if movie_ids[i] not in liked_movie_ids]

    recommended_movies = list(movies_collection.find({"_id": {"$in": [ObjectId(m_id) for m_id in recommended_movie_ids]}}))
    for movie in recommended_movies:
        movie["_id"] = str(movie["_id"]) 
    return {"recommended_movies": recommended_movies}
