from flask import Blueprint, request, jsonify
from app.services.recommendation_service import RecommendationService
from app.models.database import execute_query

recommendation_bp = Blueprint("recommendation", __name__)


@recommendation_bp.route("/train", methods=["POST"])
def train_model():
    """Endpoint to train the recommendation model with products from database"""
    try:
        success, message = RecommendationService.train_content_based_model()

        if success:
            return jsonify({"message": message}), 200
        else:
            return jsonify({"error": message}), 500

    except Exception as e:
        return jsonify({"error": f"Error training model: {str(e)}"}), 500


@recommendation_bp.route("/refresh", methods=["POST"])
def refresh_model():
    """Endpoint to refresh the recommendation model with latest data"""
    try:
        success, message = RecommendationService.refresh_recommendation_model()

        if success:
            return jsonify({"message": message}), 200
        else:
            return jsonify({"error": message}), 500

    except Exception as e:
        return jsonify({"error": f"Error refreshing model: {str(e)}"}), 500


@recommendation_bp.route("/recommend", methods=["GET"])
def recommend():
    """Endpoint to get content-based recommendations for a product"""
    try:
        product_id = request.args.get("product_id")
        num_recommendations = int(request.args.get("num", 5))

        if not product_id:
            return jsonify({"error": "Product ID is required"}), 400

        recommendations = RecommendationService.get_content_based_recommendations(
            product_id, num_recommendations
        )

        if isinstance(recommendations, dict) and "error" in recommendations:
            return jsonify(recommendations), 404

        return jsonify({"data": recommendations}), 200

    except Exception as e:
        return jsonify({"error": f"Error generating recommendations: {str(e)}"}), 500


@recommendation_bp.route("/recommend/category", methods=["GET"])
def recommend_by_category():
    """Endpoint to get recommendations for products in a specific category"""
    try:
        category_id = request.args.get("category_id")
        num_recommendations = int(request.args.get("num", 5))

        if not category_id:
            return jsonify({"error": "Category ID is required"}), 400

        recommendations = RecommendationService.get_category_recommendations(
            category_id, num_recommendations
        )

        if isinstance(recommendations, dict) and "error" in recommendations:
            return jsonify(recommendations), 404

        return jsonify({"recommendations": recommendations}), 200

    except Exception as e:
        return jsonify({"error": f"Error generating category recommendations: {str(e)}"}), 500


@recommendation_bp.route("/recommend/group", methods=["GET"])
def recommend_by_group():
    """Endpoint to get recommendations for products in a specific group"""
    try:
        group_id = request.args.get("group_id")
        num_recommendations = int(request.args.get("num", 5))

        if not group_id:
            return jsonify({"error": "Group ID is required"}), 400

        recommendations = RecommendationService.get_group_recommendations(
            group_id, num_recommendations
        )

        if isinstance(recommendations, dict) and "error" in recommendations:
            return jsonify(recommendations), 404

        return jsonify({"recommendations": recommendations}), 200

    except Exception as e:
        return jsonify({"error": f"Error generating group recommendations: {str(e)}"}), 500


@recommendation_bp.route("/debug/db", methods=["GET"])
def debug_db():
    """Debug endpoint to check database connection and schema"""
    try:
        # Check if Product table exists and get its structure
        product_info = execute_query("""
        SELECT column_name, data_type, is_nullable
        FROM information_schema.columns
        WHERE table_name = 'Product'
        ORDER BY ordinal_position
        """)

        # Get count of products
        product_count = execute_query("SELECT COUNT(*) as count FROM \"Product\"")

        # Get sample product if any exists
        sample_product = execute_query("""
        SELECT * FROM "Product" LIMIT 1
        """)

        # Check related tables
        tables = execute_query("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
        """)

        return jsonify({
            "status": "success",
            "product_schema": product_info,
            "product_count": product_count[0]["count"] if product_count else 0,
            "sample_product": sample_product[0] if sample_product else None,
            "tables": [t["table_name"] for t in tables]
        }), 200

    except Exception as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500
