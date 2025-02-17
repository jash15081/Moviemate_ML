import numpy as np
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from db import movies_collection

TFIDF_CACHE_FILE = "tfidf_matrix.npy"
MOVIE_IDS_FILE = "movie_ids.npy"
vectorizer = TfidfVectorizer(stop_words='english')

def build_tfidf_cache():
    """Generates and stores TF-IDF matrix for all movies."""
    movies = list(movies_collection.find({}))

    if not movies:
        return {"error": "No movies found in database."}

    movie_texts = [
        f"{movie['name']} {movie.get('description', '')} {', '.join(movie.get('genre', []))} {', '.join(movie.get('cast', []))} {', '.join(movie.get('directors', []))}"
        for movie in movies
    ]
    movie_ids = [str(movie["_id"]) for movie in movies]

    tfidf_matrix = vectorizer.fit_transform(movie_texts)

    np.save(TFIDF_CACHE_FILE, tfidf_matrix.toarray())
    np.save(MOVIE_IDS_FILE, np.array(movie_ids))

    return {"message": "TF-IDF cache built successfully."}

def update_tfidf_cache(movie):
    """Updates TF-IDF matrix when a new movie is added."""
    if os.path.exists(TFIDF_CACHE_FILE) and os.path.exists(MOVIE_IDS_FILE):
        existing_tfidf = np.load(TFIDF_CACHE_FILE)
        existing_movie_ids = np.load(MOVIE_IDS_FILE, allow_pickle=True).tolist()
    else:
        return build_tfidf_cache()

    new_movie_text = f"{movie['name']} {movie.get('description', '')} {', '.join(movie.get('genre', []))} {', '.join(movie.get('cast', []))} {', '.join(movie.get('directors', []))}"
    new_tfidf = vectorizer.transform([new_movie_text]).toarray()

    updated_tfidf = np.vstack([existing_tfidf, new_tfidf])
    updated_movie_ids = existing_movie_ids + [str(movie["_id"])]

    np.save(TFIDF_CACHE_FILE, updated_tfidf)
    np.save(MOVIE_IDS_FILE, np.array(updated_movie_ids))

    return {"message": "TF-IDF cache updated successfully."}
