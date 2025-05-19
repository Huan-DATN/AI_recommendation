from app.models.recommendation.content_based import ContentBasedRecommender
from app.models.database import get_all_products, get_product_by_id, get_products_by_category, get_products_by_group


class RecommendationService:
    """Service for handling product recommendations"""

    @staticmethod
    def train_content_based_model():
        """Train content-based recommendation model with product data from database"""
        try:
            # Fetch all products from database
            products = get_all_products()

            if not products:
                return False, "No products found in database"

            success = ContentBasedRecommender.train(products)
            return success, "Content-based recommendation model trained successfully" if success else "Failed to train model"
        except Exception as e:
            error_message = f"Error training recommendation model: {str(e)}"
            print(error_message)
            return False, error_message

    @staticmethod
    def get_content_based_recommendations(product_id, num_recommendations=5):
        """Get content-based recommendations for a product"""
        try:
            # Check if product exists in database
            product = get_product_by_id(product_id)
            if not product:
                return {"error": f"Product with ID {product_id} not found in database"}

            recommendations = ContentBasedRecommender.recommend(product_id, num_recommendations)
            return recommendations
        except Exception as e:
            error_message = f"Error getting recommendations: {str(e)}"
            print(error_message)
            return {"error": error_message}

    @staticmethod
    def get_category_recommendations(category_id, num_recommendations=5):
        """Get recommendations for products in a specific category"""
        try:
            # Get products in the category
            category_products = get_products_by_category(category_id)

            if not category_products:
                return {"error": f"No products found in category ID {category_id}"}

            # Train model if not already trained
            if not ContentBasedRecommender.load_models():
                success, _ = RecommendationService.train_content_based_model()
                if not success:
                    return {"error": "Failed to train recommendation model"}

            # Get recommendations for each product in the category
            all_recommendations = []
            seen_products = set()

            for product in category_products:
                product_id = product['id']
                recommendations = ContentBasedRecommender.recommend(product_id, num_recommendations)

                if isinstance(recommendations, list):
                    for rec in recommendations:
                        rec_id = rec['id']
                        if rec_id not in seen_products:
                            seen_products.add(rec_id)
                            all_recommendations.append(rec)

            # Sort by similarity score and take top N
            all_recommendations.sort(key=lambda x: x.get('similarity_score', 0), reverse=True)
            return all_recommendations[:num_recommendations]

        except Exception as e:
            error_message = f"Error getting category recommendations: {str(e)}"
            print(error_message)
            return {"error": error_message}

    @staticmethod
    def get_group_recommendations(group_id, num_recommendations=5):
        """Get recommendations for products in a specific group"""
        try:
            # Get products in the group
            group_products = get_products_by_group(group_id)

            if not group_products:
                return {"error": f"No products found in group ID {group_id}"}

            # Train model if not already trained
            if not ContentBasedRecommender.load_models():
                success, _ = RecommendationService.train_content_based_model()
                if not success:
                    return {"error": "Failed to train recommendation model"}

            # Get recommendations for each product in the group
            all_recommendations = []
            seen_products = set()

            for product in group_products:
                product_id = product['id']
                recommendations = ContentBasedRecommender.recommend(product_id, num_recommendations)

                if isinstance(recommendations, list):
                    for rec in recommendations:
                        rec_id = rec['id']
                        if rec_id not in seen_products:
                            seen_products.add(rec_id)
                            all_recommendations.append(rec)

            # Sort by similarity score and take top N
            all_recommendations.sort(key=lambda x: x.get('similarity_score', 0), reverse=True)
            return all_recommendations[:num_recommendations]

        except Exception as e:
            error_message = f"Error getting group recommendations: {str(e)}"
            print(error_message)
            return {"error": error_message}

    @staticmethod
    def refresh_recommendation_model():
        """Refresh the recommendation model with latest data from database"""
        try:
            success, message = RecommendationService.train_content_based_model()
            return success, message
        except Exception as e:
            error_message = f"Error refreshing recommendation model: {str(e)}"
            print(error_message)
            return False, error_message
