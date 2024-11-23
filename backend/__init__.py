"""Backend package initialization."""
from flask import Flask, jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS
from bson import ObjectId
import json
from backend.utils.db import init_db
from backend.utils.json_encoder import MongoJSONEncoder

class MongoJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return super().default(obj)

def create_app(test_config=None):
    """Create and configure the Flask application."""
    app = Flask(__name__, instance_relative_config=True)

    # Load configuration
    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY='dev',
            MONGO_URI='mongodb://localhost:27017/arcane',
            STRICT_SLASHES=False  # Allow URLs with or without trailing slashes
        )
    elif isinstance(test_config, str) and test_config == 'testing':
        app.config.from_mapping(
            TESTING=True,
            SECRET_KEY='test',
            MONGO_URI='mongodb://localhost:27017/test_db',
            STRICT_SLASHES=False  # Allow URLs with or without trailing slashes
        )
    else:
        app.config.update(test_config)

    # Set up custom JSON encoder
    app.json_encoder = MongoJSONEncoder

    # Initialize extensions
    CORS(app)
    app.mongo = PyMongo(app)  # Make mongo available in app context

    # Initialize MongoDB collections
    with app.app_context():
        init_db()

    # Register blueprints
    from backend.api import npc_routes, campaign_routes, encounter_routes
    app.register_blueprint(npc_routes.bp, url_prefix='/api/npcs')
    app.register_blueprint(campaign_routes.bp, url_prefix='/api/campaigns')
    app.register_blueprint(encounter_routes.bp, url_prefix='/api/encounters')

    # Register error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({'error': 'Resource not found'}), 404

    @app.errorhandler(400)
    def bad_request_error(error):
        return jsonify({'error': 'Bad request'}), 400

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error'}), 500

    return app
