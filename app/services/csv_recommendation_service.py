import pickle
import os
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from app.models.csv_data_loader import load_csv_data

# Global variables to store models
csv_tfidf_vectorizer = None
csv_tfidf_matrix = None
csv_items_df = None

# Path to save/load model files
MODEL_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models")
os.makedirs(MODEL_DIR, exist_ok=True)
CSV_TFIDF_MODEL_PATH = os.path.join(MODEL_DIR, "csv_tfidf_vectorizer.pkl")
CSV_MATRIX_PATH = os.path.join(MODEL_DIR, "csv_tfidf_matrix.pkl")
CSV_ITEMS_PATH = os.path.join(MODEL_DIR, "csv_items.pkl")

# TF-IDF parameters
TFIDF_PARAMS = {
    "analyzer": "word",
    "stop_words": None,  # Removed English stopwords for Vietnamese text
    "min_df": 0.01,
    "max_df": 0.95,
    "ngram_range": (1, 2)  # Include bigrams for better feature extraction
}


class CSVRecommendationService:
    """Service for handling product recommendations based on CSV data"""

    @staticmethod
    def load_models():
        """Load pre-trained models if they exist"""
        global csv_tfidf_vectorizer, csv_tfidf_matrix, csv_items_df

        try:
            with open(CSV_TFIDF_MODEL_PATH, 'rb') as f:
                csv_tfidf_vectorizer = pickle.load(f)
            with open(CSV_MATRIX_PATH, 'rb') as f:
                csv_tfidf_matrix = pickle.load(f)
            with open(CSV_ITEMS_PATH, 'rb') as f:
                csv_items_df = pickle.load(f)
            return True
        except (FileNotFoundError, EOFError):
            return False

    @staticmethod
    def train_model():
        """Train a content-based recommendation model using CSV data"""
        global csv_tfidf_vectorizer, csv_tfidf_matrix, csv_items_df

        try:
            # Load CSV data
            csv_items_df = load_csv_data()

            if csv_items_df is None or len(csv_items_df) == 0:
                return False, "No products found in CSV data"

            # Create TF-IDF matrix
            csv_tfidf_vectorizer = TfidfVectorizer(**TFIDF_PARAMS)
            csv_tfidf_matrix = csv_tfidf_vectorizer.fit_transform(csv_items_df['content'])

            # Save models
            with open(CSV_TFIDF_MODEL_PATH, 'wb') as f:
                pickle.dump(csv_tfidf_vectorizer, f)
            with open(CSV_MATRIX_PATH, 'wb') as f:
                pickle.dump(csv_tfidf_matrix, f)
            with open(CSV_ITEMS_PATH, 'wb') as f:
                pickle.dump(csv_items_df, f)

            return True, "CSV-based recommendation model trained successfully"
        except Exception as e:
            error_message = f"Error training CSV recommendation model: {str(e)}"
            print(error_message)
            return False, error_message

    @staticmethod
    def get_recommendations(product_id, num_recommendations=5):
        """Generate recommendations for a given product"""
        global csv_tfidf_matrix, csv_items_df

        if csv_tfidf_matrix is None or csv_items_df is None:
            if not CSVRecommendationService.load_models():
                success, message = CSVRecommendationService.train_model()
                if not success:
                    return {"error": message}

        # Find the index of the product in the dataframe
        try:
            product_id = int(product_id)  # Ensure product_id is an integer
            idx = csv_items_df[csv_items_df['id'] == product_id].index[0]
        except (IndexError, KeyError, ValueError):
            return {"error": f"Product with ID {product_id} not found in CSV data"}

        # Calculate cosine similarity between the product and all other products
        sim_scores = cosine_similarity(csv_tfidf_matrix[idx], csv_tfidf_matrix).flatten()

        # Get indices of top similar products (excluding the product itself)
        sim_indices = sim_scores.argsort()[::-1]
        sim_indices = sim_indices[sim_indices != idx][:num_recommendations]

        # Get the products with similarity scores
        recommended_products = []
        for i, idx in enumerate(sim_indices):
            product = csv_items_df.iloc[idx].to_dict()
            product['similarity_score'] = float(sim_scores[idx])

            # Remove content field as it's not needed in the response
            if 'content' in product:
                del product['content']

            recommended_products.append(product)

        return recommended_products

    @staticmethod
    def get_keyword_recommendations(keywords, num_recommendations=5):
        """Generate recommendations based on keywords"""
        global csv_tfidf_vectorizer, csv_tfidf_matrix, csv_items_df

        if csv_tfidf_vectorizer is None or csv_tfidf_matrix is None or csv_items_df is None:
            if not CSVRecommendationService.load_models():
                success, message = CSVRecommendationService.train_model()
                if not success:
                    return {"error": message}

        try:
            # Transform keywords to TF-IDF vector
            keywords_vector = csv_tfidf_vectorizer.transform([keywords])

            # Calculate cosine similarity between keywords and all products
            sim_scores = cosine_similarity(keywords_vector, csv_tfidf_matrix).flatten()

            # Get indices of top similar products
            sim_indices = sim_scores.argsort()[::-1][:num_recommendations]

            # Get the products with similarity scores
            recommended_products = []
            for i, idx in enumerate(sim_indices):
                product = csv_items_df.iloc[idx].to_dict()
                product['similarity_score'] = float(sim_scores[idx])

                # Remove content field as it's not needed in the response
                if 'content' in product:
                    del product['content']

                recommended_products.append(product)

            return recommended_products
        except Exception as e:
            error_message = f"Error generating keyword recommendations: {str(e)}"
            print(error_message)
            return {"error": error_message}

    @staticmethod
    def get_all_products():
        """Get all products from CSV data"""
        global csv_items_df

        if csv_items_df is None:
            if not CSVRecommendationService.load_models():
                success, message = CSVRecommendationService.train_model()
                if not success:
                    return {"error": message}

        try:
            products = csv_items_df.to_dict(orient="records")

            # Remove content field as it's not needed in the response
            for product in products:
                if 'content' in product:
                    del product['content']

            return products
        except Exception as e:
            error_message = f"Error getting all products: {str(e)}"
            print(error_message)
            return {"error": error_message}
