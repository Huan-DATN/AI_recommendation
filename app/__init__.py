from flask import Flask
from app.routes.recommendation import recommendation_bp
from app.tasks.scheduled_tasks import start_scheduler


def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.Config")

    app.register_blueprint(recommendation_bp, url_prefix="/api")

    # Start the scheduler for periodic tasks
    with app.app_context():
        try:
            start_scheduler()
        except Exception as e:
            app.logger.error(f"Error starting scheduler: {str(e)}")
            app.logger.info("Application will continue without scheduled tasks")

    return app
