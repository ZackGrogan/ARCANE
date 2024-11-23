from flask import Flask, jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS
from bson import ObjectId
import json
from utils.db import init_db

class MongoJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return super().default(obj)

def create_app(test_config=None):
    """Create and configure the Flask application."""
    app = Flask(__name__)

    # Load configuration
    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY='dev',
            MONGO_URI='mongodb://localhost:27017/arcane'
        )
    else:
        app.config.update(test_config)

    # Set up custom JSON encoder
    app.json_encoder = MongoJSONEncoder

    # Initialize extensions
    CORS(app)
    mongo = PyMongo(app)
    app.mongo = mongo  # Make mongo available in app context

    # Initialize MongoDB collections
    with app.app_context():
        init_db()

    # Register blueprints
    from api import npc_routes, campaign_routes, encounter_routes
    app.register_blueprint(npc_routes.bp, url_prefix='/api/npcs')
    app.register_blueprint(campaign_routes.bp, url_prefix='/api/campaigns')
    app.register_blueprint(encounter_routes.bp, url_prefix='/api/encounters')

    # Register error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({'error': 'Resource not found'}), 404

    @app.errorhandler(400)
    def bad_request_error(error):
        return jsonify({'error': str(error.description)}), 400

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error'}), 500

    return app
