"""Test Encounter API endpoints."""
import pytest
from flask import url_for
from bson import ObjectId
import time
import random
from unittest.mock import MagicMock, patch
from backend.utils.dnd_api_client import DnDApiClient

@pytest.fixture
def mock_dnd_api():
    """Mock the DnD API client."""
    with patch('backend.models.encounter.DnDApiClient') as mock:
        yield mock

@pytest.fixture(autouse=True)
def clear_db(app, db):
    """Clear database before each test."""
    with app.app_context():
        db.encounters.delete_many({})
        yield

def test_create_encounter(app, client, db):
    """Test creating a new encounter."""
    with app.app_context():
        encounter_data = {
            'title': 'Test Encounter',
            'environment': 'Forest',
            'party_level': 5,
            'difficulty': 'Medium',
            'description': 'A test encounter',
            'monsters': [],
            'traps': [],
            'notes': ''
        }
        response = client.post('/api/encounters/', json=encounter_data)
        assert response.status_code == 201
        data = response.get_json()
        assert data['title'] == encounter_data['title']
        assert data['environment'] == encounter_data['environment']
        assert data['party_level'] == encounter_data['party_level']
        assert data['difficulty'] == encounter_data['difficulty']

def test_get_encounter(app, client, db):
    """Test getting a specific encounter."""
    with app.app_context():
        # Create an encounter
        encounter_data = {
            'title': 'Test Encounter',
            'environment': 'Forest',
            'party_level': 5,
            'difficulty': 'Medium',
            'description': 'A test encounter',
            'monsters': [],
            'traps': [],
            'notes': ''
        }
        create_response = client.post('/api/encounters/', json=encounter_data)
        assert create_response.status_code == 201
        encounter_id = create_response.get_json()['_id']

        # Get the encounter
        response = client.get(f'/api/encounters/{encounter_id}/')
        assert response.status_code == 200
        data = response.get_json()
        assert data['title'] == encounter_data['title']
        assert data['environment'] == encounter_data['environment']
        assert data['party_level'] == encounter_data['party_level']

def test_get_nonexistent_encounter(app, client, db):
    """Test retrieving a nonexistent encounter."""
    with app.app_context():
        response = client.get('/api/encounters/nonexistent/')
        assert response.status_code == 404
        data = response.get_json()
        assert 'error' in data

def test_update_encounter(app, client, db):
    """Test updating an encounter."""
    with app.app_context():
        # Create an encounter
        encounter_data = {
            'title': 'Test Encounter',
            'environment': 'Forest',
            'party_level': 5,
            'difficulty': 'Medium',
            'description': 'A test encounter',
            'monsters': [],
            'traps': [],
            'notes': ''
        }
        create_response = client.post('/api/encounters/', json=encounter_data)
        assert create_response.status_code == 201
        encounter_id = create_response.get_json()['_id']

        # Update the encounter
        update_data = {
            'title': 'Updated Encounter',
            'environment': 'Cave',
            'party_level': 6
        }
        response = client.put(f'/api/encounters/{encounter_id}/', json=update_data)
        assert response.status_code == 200
        data = response.get_json()
        assert data['title'] == update_data['title']
        assert data['environment'] == update_data['environment']
        assert data['party_level'] == update_data['party_level']
        assert data['difficulty'] == encounter_data['difficulty']  # Unchanged field

def test_delete_encounter(app, client, db):
    """Test deleting an encounter."""
    with app.app_context():
        # Create an encounter
        encounter_data = {
            'title': 'Test Encounter',
            'environment': 'Forest',
            'party_level': 5,
            'difficulty': 'Medium',
            'description': 'A test encounter',
            'monsters': [],
            'traps': [],
            'notes': ''
        }
        create_response = client.post('/api/encounters/', json=encounter_data)
        assert create_response.status_code == 201
        encounter_id = create_response.get_json()['_id']

        # Delete the encounter
        response = client.delete(f'/api/encounters/{encounter_id}/')
        assert response.status_code == 204

        # Verify it's gone
        response = client.get(f'/api/encounters/{encounter_id}/')
        assert response.status_code == 404

def test_list_encounters(app, client, db):
    """Test listing all encounters."""
    with app.app_context():
        # Initially there should be no encounters
        response = client.get('/api/encounters/')
        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 0

        # Create a few encounters
        encounters_to_create = [
            {
                'title': 'Forest Ambush',
                'environment': 'Forest',
                'party_level': 5,
                'difficulty': 'Medium',
                'description': 'A forest ambush',
                'monsters': [],
                'traps': [],
                'notes': ''
            },
            {
                'title': 'Cave Exploration',
                'environment': 'Cave',
                'party_level': 6,
                'difficulty': 'Hard',
                'description': 'A cave exploration',
                'monsters': [],
                'traps': [],
                'notes': ''
            }
        ]

        for encounter in encounters_to_create:
            response = client.post('/api/encounters/', json=encounter)
            assert response.status_code == 201

        # List all encounters
        response = client.get('/api/encounters/')
        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == len(encounters_to_create)
        assert all(encounter['title'] in [e['title'] for e in data] for encounter in encounters_to_create)

def test_add_monster(app, client, db, mock_dnd_api):
    """Test adding a monster to an encounter."""
    with app.app_context():
        # Create an encounter
        encounter_data = {
            'title': 'Test Encounter',
            'environment': 'Forest',
            'party_level': 5,
            'difficulty': 'Medium',
            'description': 'A test encounter',
            'monsters': [],
            'traps': [],
            'notes': ''
        }
        create_response = client.post('/api/encounters/', json=encounter_data)
        assert create_response.status_code == 201
        encounter_id = create_response.get_json()['_id']

        # Mock DnD API response
        mock_monster = {
            'name': 'Goblin',
            'challenge_rating': 0.25,
            'hit_points': 7
        }
        mock_dnd_api.return_value.get_monster.return_value = mock_monster

        # Add monster to encounter
        monster_data = {'monster_name': 'goblin', 'quantity': 2}
        response = client.post(f'/api/encounters/{encounter_id}/monsters/', json=monster_data)
        assert response.status_code == 200
        data = response.get_json()
        assert len(data['monsters']) == 1
        assert data['monsters'][0]['name'] == 'Goblin'
        assert data['monsters'][0]['quantity'] == 2

def test_remove_monster(app, client, db, mock_dnd_api):
    """Test removing a monster from an encounter."""
    with app.app_context():
        # Create an encounter with a monster
        encounter_data = {
            'title': 'Test Encounter',
            'environment': 'Forest',
            'party_level': 5,
            'difficulty': 'Medium',
            'description': 'A test encounter',
            'monsters': [{'name': 'Goblin', 'quantity': 2}],
            'traps': [],
            'notes': ''
        }
        create_response = client.post('/api/encounters/', json=encounter_data)
        assert create_response.status_code == 201
        encounter_id = create_response.get_json()['_id']

        # Remove monster from encounter
        response = client.delete(f'/api/encounters/{encounter_id}/monsters/Goblin/')
        assert response.status_code == 200
        data = response.get_json()
        assert len(data['monsters']) == 0

def test_add_monster_invalid_monster(client, mock_dnd_api):
    """Test adding an invalid monster to an encounter."""
    # Mock DnD API to raise an error for invalid monster
    mock_dnd_api.return_value.get_monster.side_effect = Exception("Monster not found")

    # Try to add invalid monster
    monster_data = {'monster_name': 'invalid_monster', 'quantity': 1}
    response = client.post('/api/encounters/some_id/monsters/', json=monster_data)
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data

@patch('backend.models.encounter.DnDApiClient')
def test_add_monster_api_error(mock_dnd_api_class, app, client):
    """Test handling of DnD API errors."""
    with app.app_context():
        # Create an encounter first
        encounter_data = {
            'title': 'Test Encounter',
            'environment': 'Forest',
            'party_level': 5,
            'difficulty': 'Medium',
            'description': 'A test encounter',
            'monsters': [],
            'traps': [],
            'notes': ''
        }
        create_response = client.post('/api/encounters/', json=encounter_data)
        assert create_response.status_code == 201
        encounter_id = create_response.get_json()['_id']

        # Mock DnD API to simulate a connection error
        mock_instance = mock_dnd_api_class.return_value
        mock_instance.get_monster.side_effect = Exception("API connection error")

        # Try to add monster
        monster_data = {'monster_name': 'goblin', 'quantity': 1}
        response = client.post(f'/api/encounters/{encounter_id}/monsters/', json=monster_data)

        assert response.status_code == 500
        assert 'error' in response.get_json()

def test_add_duplicate_monster(client, mock_dnd_api, app):
    """Test adding a duplicate monster to an encounter."""
    with app.app_context():
        # Create an encounter
        encounter_data = {
            'title': 'Test Encounter',
            'environment': 'Forest',
            'party_level': 5,
            'difficulty': 'Medium',
            'description': 'A test encounter',
            'monsters': [],
            'traps': [],
            'notes': ''
        }
        create_response = client.post('/api/encounters/', json=encounter_data)
        assert create_response.status_code == 201
        encounter_id = create_response.get_json()['_id']

        # Mock DnD API response
        mock_monster = {
            'name': 'Goblin',
            'challenge_rating': 0.25,
            'hit_points': 7
        }
        mock_dnd_api.return_value.get_monster.return_value = mock_monster

        # Add monster first time
        monster_data = {'monster_name': 'Goblin', 'quantity': 1}
        response = client.post(f'/api/encounters/{encounter_id}/monsters', json=monster_data)
        assert response.status_code == 200

        # Try to add same monster again
        response = client.post(f'/api/encounters/{encounter_id}/monsters', json=monster_data)
        assert response.status_code == 400
        assert "already exists in encounter" in response.json['error']

def test_add_monster_to_encounter(client, mock_dnd_api, app):
    """Test adding a monster to an encounter."""
    with app.app_context():
        # Create a test encounter
        encounter_data = {
            'title': 'Test Encounter',
            'environment': 'dungeon',
            'party_level': 5,
            'difficulty': 'medium'
        }
        response = client.post('/api/encounters/', json=encounter_data)
        assert response.status_code == 201
        encounter_id = response.json['_id']

        # Mock DnD API response
        mock_monster = {
            'name': 'Goblin',
            'challenge_rating': 0.25,
            'hit_points': 7
        }
        mock_dnd_api.return_value.get_monster.return_value = mock_monster

        # Test adding a valid monster
        monster_data = {
            'monster_name': 'Goblin',
            'quantity': 3
        }
        response = client.post(f'/api/encounters/{encounter_id}/monsters', json=monster_data)
        assert response.status_code == 200
        assert 'Successfully added 3 Goblin(s)' in response.json['message']

def test_remove_monster_from_encounter(client, mock_dnd_api, app):
    """Test removing a monster from an encounter."""
    with app.app_context():
        # Create a test encounter
        encounter_data = {
            'title': 'Test Encounter',
            'environment': 'dungeon',
            'party_level': 5,
            'difficulty': 'medium'
        }
        response = client.post('/api/encounters/', json=encounter_data)
        assert response.status_code == 201
        encounter_id = response.json['_id']

        # Mock DnD API response
        mock_monster = {
            'name': 'Goblin',
            'challenge_rating': 0.25,
            'hit_points': 7
        }
        mock_dnd_api.return_value.get_monster.return_value = mock_monster

        # Add a monster first
        monster_data = {'monster_name': 'Goblin'}
        response = client.post(f'/api/encounters/{encounter_id}/monsters', json=monster_data)
        assert response.status_code == 200

        # Test removing the monster
        response = client.delete(f'/api/encounters/{encounter_id}/monsters/Goblin')
        assert response.status_code == 200
        assert 'Successfully removed monster' in response.json['message']
