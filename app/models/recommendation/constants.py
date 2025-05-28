import os

# Path to save/load model files
MODEL_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "models")
os.makedirs(MODEL_DIR, exist_ok=True)
TFIDF_MODEL_PATH = os.path.join(MODEL_DIR, "tfidf_vectorizer.pkl")
MATRIX_PATH = os.path.join(MODEL_DIR, "tfidf_matrix.pkl")
ITEMS_PATH = os.path.join(MODEL_DIR, "items.pkl")

# Price range categories
PRICE_RANGES = {
    "very_low": 50000,
    "low": 100000,
    "medium": 200000,
    "high": 500000,
    "very_high": float('inf')
}

# TF-IDF parameters
TFIDF_PARAMS = {
    "analyzer": "word",
    "stop_words": None,  # Removed English stopwords for Vietnamese text
    "min_df": 0.01,
    "max_df": 0.95,
    "ngram_range": (1, 2)  # Include bigrams for better feature extraction
}

# Content features to extract from products
CONTENT_FEATURES = [
    "name",
    "description",
    "price",
    "groupName",
    "cityName",
    "star",
    "categories",
    "images"
]
