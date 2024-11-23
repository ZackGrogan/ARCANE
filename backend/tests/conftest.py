"""Test configuration and fixtures."""
import pytest
from flask import Flask
from flask_pymongo import PyMongo
from backend import create_app
from backend.models.npc import NPC

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    app = create_app({
        'TESTING': True,
        'MONGO_URI': 'mongodb://localhost:27017/test_db'
    })

    # Create the application context
    with app.app_context():
        # Initialize PyMongo with the app
        app.mongo = PyMongo(app)

        # Clear test collections before each test
        app.mongo.db.npcs.delete_many({})
        app.mongo.db.campaigns.delete_many({})
        app.mongo.db.encounters.delete_many({})

        yield app

        # Clear test collections after each test
        app.mongo.db.npcs.delete_many({})
        app.mongo.db.campaigns.delete_many({})
        app.mongo.db.encounters.delete_many({})

@pytest.fixture
def client(app):
    """Test client for the app."""
    return app.test_client()

@pytest.fixture
def mongo(app):
    """MongoDB test database."""
    return app.mongo

@pytest.fixture
def db(app):
    """MongoDB test database."""
    return app.mongo.db

@pytest.fixture
def test_npc():
    """Test NPC data."""
    return {
        'name': 'Test NPC',
        'race': 'Human',
        'npc_class': 'Fighter',
        'level': 1,
        'alignment': 'True Neutral',
        'background': 'Soldier',
        'personality': 'Brave and determined',
        'ideals': 'Honor above all',
        'bonds': 'Loyal to their unit',
        'flaws': 'Stubborn',
        'notes': 'Test NPC notes'
    }

@pytest.fixture
def test_campaign():
    """Test Campaign data."""
    return {
        'name': 'Test Campaign',
        'description': 'A test campaign',
        'start_date': '2024-03-14',
        'status': 'active',
        'notes': '',
        'npcs': [],
        'encounters': [],
        'maps': []
    }

@pytest.fixture
def test_encounter():
    """Test Encounter data."""
    return {
        'title': 'Test Encounter',
        'environment': 'Forest',
        'party_level': 5,
        'difficulty': 'Medium',
        'description': 'A test encounter',
        'monsters': [],
        'traps': [],
        'notes': ''
    }
