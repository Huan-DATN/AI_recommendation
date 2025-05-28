from flask import Blueprint, request, jsonify
from app.services.csv_recommendation_service import CSVRecommendationService

csv_recommendation_bp = Blueprint("csv_recommendation", __name__)


@csv_recommendation_bp.route("/train", methods=["POST"])
def train_model():
    """Endpoint to train the recommendation model with products from CSV data"""
    try:
        success, message = CSVRecommendationService.train_model()

        if success:
            return jsonify({"message": message}), 200
        else:
            return jsonify({"error": message}), 500

    except Exception as e:
        return jsonify({"error": f"Error training model: {str(e)}"}), 500


@csv_recommendation_bp.route("/products", methods=["GET"])
def get_all_products():
    """Endpoint to get all products from CSV data"""
    try:
        products = CSVRecommendationService.get_all_products()

        if isinstance(products, dict) and "error" in products:
            return jsonify(products), 500

        return jsonify({"data": products}), 200

    except Exception as e:
        return jsonify({"error": f"Error getting products: {str(e)}"}), 500


@csv_recommendation_bp.route("/recommend", methods=["GET"])
def recommend():
    """Endpoint to get content-based recommendations for a product from CSV data"""
    try:
        product_id = request.args.get("product_id")
        num_recommendations = int(request.args.get("num", 5))

        if not product_id:
            return jsonify({"error": "Product ID is required"}), 400

        recommendations = CSVRecommendationService.get_recommendations(
            product_id, num_recommendations
        )

        if isinstance(recommendations, dict) and "error" in recommendations:
            return jsonify(recommendations), 404

        return jsonify({"data": recommendations}), 200

    except Exception as e:
        return jsonify({"error": f"Error generating recommendations: {str(e)}"}), 500


@csv_recommendation_bp.route("/recommend/keywords", methods=["GET"])
def recommend_by_keywords():
    """Endpoint to get recommendations based on keywords"""
    try:
        keywords = request.args.get("keywords")
        num_recommendations = int(request.args.get("num", 5))

        if not keywords:
            return jsonify({"error": "Keywords are required"}), 400

        recommendations = CSVRecommendationService.get_keyword_recommendations(
            keywords, num_recommendations
        )

        if isinstance(recommendations, dict) and "error" in recommendations:
            return jsonify(recommendations), 404

        return jsonify({"data": recommendations}), 200

    except Exception as e:
        return jsonify({"error": f"Error generating keyword recommendations: {str(e)}"}), 500
