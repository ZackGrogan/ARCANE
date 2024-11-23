"""Flask application factory."""
from flask import Flask
from flask_pymongo import PyMongo
from backend.api.routes import npc_routes, campaign_routes, encounter_routes

def create_app(test_config=None):
    """Create and configure the Flask application."""
    app = Flask(__name__)

    # Default configuration
    app.config.from_mapping(
        MONGO_URI='mongodb://localhost:27017/arcane_db'
    )

    if test_config is not None:
        # Load test config if passed in
        app.config.update(test_config)

    # Initialize MongoDB
    app.mongo = PyMongo(app)

    # Register blueprints
    app.register_blueprint(npc_routes.bp)
    app.register_blueprint(campaign_routes.bp)
    app.register_blueprint(encounter_routes.bp)

    return app
