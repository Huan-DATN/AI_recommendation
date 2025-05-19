import time
import threading
import schedule
from app.services.recommendation_service import RecommendationService


def refresh_recommendation_model():
    """Refresh the recommendation model with latest data from database"""
    try:
        print("Scheduled task: Refreshing recommendation model...")
        success, message = RecommendationService.refresh_recommendation_model()
        print(f"Recommendation model refresh {'successful' if success else 'failed'}: {message}")
    except Exception as e:
        print(f"Error in scheduled refresh task: {str(e)}")


def run_scheduler():
    """Run the scheduler in a separate thread"""
    # Schedule the refresh task to run daily at 3 AM
    schedule.every().day.at("03:00").do(refresh_recommendation_model)

    while True:
        try:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
        except Exception as e:
            print(f"Error in scheduler loop: {str(e)}")
            time.sleep(300)  # If error occurs, wait 5 minutes before retrying


def start_scheduler():
    """Start the scheduler in a background thread"""
    try:
        scheduler_thread = threading.Thread(target=run_scheduler)
        scheduler_thread.daemon = True
        scheduler_thread.start()
        print("Scheduler started in background thread")

        # Initial training of the model
        print("Initial training of recommendation model...")
        try:
            success, message = RecommendationService.train_content_based_model()
            print(f"Initial model training {'successful' if success else 'failed'}: {message}")
        except Exception as e:
            print(f"Error during initial model training: {str(e)}")
            print("The application will continue without initial model training.")
            print("You can manually train the model later using the /api/train endpoint.")
    except Exception as e:
        print(f"Failed to start scheduler: {str(e)}")
        raise
