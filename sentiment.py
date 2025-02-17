from transformers import pipeline
from models import Review

sentiment_model = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")

def predict_rating(review: Review):
    """Predicts movie rating (1 to 5) from review text."""
    result = sentiment_model(review.text)[0]
    label = result['label']
    rating_1_to_5 = int(label.split()[0])  
    return {"rating": rating_1_to_5}
