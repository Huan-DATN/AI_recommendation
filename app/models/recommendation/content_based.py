import pickle
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from app.models.recommendation.constants import (
    TFIDF_MODEL_PATH, MATRIX_PATH, ITEMS_PATH,
    PRICE_RANGES, TFIDF_PARAMS, CONTENT_FEATURES
)
from app.models.text_preprocessing import preprocess_text

# Global variables to store models
tfidf_vectorizer = None
tfidf_matrix = None
items_df = None


def load_models():
    """Load pre-trained models if they exist"""
    global tfidf_vectorizer, tfidf_matrix, items_df

    try:
        with open(TFIDF_MODEL_PATH, 'rb') as f:
            tfidf_vectorizer = pickle.load(f)
        with open(MATRIX_PATH, 'rb') as f:
            tfidf_matrix = pickle.load(f)
        with open(ITEMS_PATH, 'rb') as f:
            items_df = pickle.load(f)
        return True
    except (FileNotFoundError, EOFError):
        return False


def get_price_range(price):
    """Convert price to a categorical range for better recommendation"""
    for range_name, threshold in PRICE_RANGES.items():
        if price < threshold:
            return range_name
    return "very_high"  # Default case


def prepare_content_features(products_df):
    """Prepare content features from product data"""
    products_df['content'] = products_df.apply(
        lambda x: ' '.join(filter(None, [
            preprocess_text(str(x.get('name', ''))),
            preprocess_text(str(x.get('description', ''))),
            f"price_{get_price_range(x.get('price', 0))}",
            f"group_{preprocess_text(str(x.get('groupName', '')))}",
            f"city_{preprocess_text(str(x.get('cityName', '')))}",
            f"star_{str(x.get('star', 2))}",
            ' '.join([f"category_{preprocess_text(cat)}" for cat in x.get('categories', []) if cat]) if x.get('categories') else '',
        ])),
        axis=1
    )
    return products_df


class ContentBasedRecommender:
    """Content-based recommendation model using TF-IDF and cosine similarity"""

    @staticmethod
    def load_models():
        """Load pre-trained models if they exist"""
        return load_models()

    @staticmethod
    def train(products):
        """Train a content-based recommendation model"""
        global tfidf_vectorizer, tfidf_matrix, items_df

        # Convert products to DataFrame if it's not already
        if not isinstance(products, pd.DataFrame):
            items_df = pd.DataFrame(products)
        else:
            items_df = products

        # Prepare content features
        items_df = prepare_content_features(items_df)

        # Create TF-IDF matrix
        tfidf_vectorizer = TfidfVectorizer(**TFIDF_PARAMS)

        tfidf_matrix = tfidf_vectorizer.fit_transform(items_df['content'])

        # Save models
        with open(TFIDF_MODEL_PATH, 'wb') as f:
            pickle.dump(tfidf_vectorizer, f)
        with open(MATRIX_PATH, 'wb') as f:
            pickle.dump(tfidf_matrix, f)
        with open(ITEMS_PATH, 'wb') as f:
            pickle.dump(items_df, f)

        return True

    @staticmethod
    def recommend(product_id, num_recommendations=5):
        """Generate recommendations for a given product"""
        global tfidf_matrix, items_df

        if tfidf_matrix is None or items_df is None:
            if not load_models():
                return {"error": "Recommendation model not trained yet"}

        # Find the index of the product in the dataframe
        try:
            product_id = int(product_id)  # Ensure product_id is an integer
            idx = items_df[items_df['id'] == product_id].index[0]
        except (IndexError, KeyError, ValueError):
            return {"error": f"Product with ID {product_id} not found"}

        # Calculate cosine similarity between the product and all other products
        sim_scores = cosine_similarity(tfidf_matrix[idx], tfidf_matrix).flatten()

        # Get indices of top similar products (excluding the product itself)
        sim_indices = sim_scores.argsort()[::-1]
        sim_indices = sim_indices[sim_indices != idx][:num_recommendations]

        # Get the products with similarity scores
        recommended_products = []
        for i, idx in enumerate(sim_indices):
            product = items_df.iloc[idx].to_dict()
            product['similarity_score'] = float(sim_scores[idx])

            # Remove content field as it's not needed in the response
            if 'content' in product:
                del product['content']

            recommended_products.append(product)

        return recommended_products
