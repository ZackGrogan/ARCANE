from flask import Flask
from flask_pymongo import PyMongo
from .routes import npc_blueprint, encounter_blueprint, campaign_blueprint

# Initialize Flask app
app = Flask(__name__)

# Load configuration
app.config.from_pyfile('config.py')

# Initialize PyMongo
mongo = PyMongo(app)

# Register Blueprints
app.register_blueprint(npc_blueprint)
app.register_blueprint(encounter_blueprint)
app.register_blueprint(campaign_blueprint)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
