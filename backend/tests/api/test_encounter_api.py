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
        response = client.post('/api/encounters/', json=encounter_data)
        assert response.status_code == 201
        encounter_id = response.get_json()['_id']

        # Get the encounter
        get_response = client.get(f'/api/encounters/{encounter_id}/')
        assert get_response.status_code == 200
        data = get_response.get_json()
        assert data['title'] == encounter_data['title']

        # Try to get non-existent encounter
        get_response = client.get('/api/encounters/000000000000000000000000/')
        assert get_response.status_code == 404

def test_get_nonexistent_encounter(app, client, db):
    """Test retrieving a nonexistent encounter."""
    with app.app_context():
        response = client.get('/api/encounters/000000000000000000000000/')
        assert response.status_code == 404
        assert 'error' in response.get_json()

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
        response = client.post('/api/encounters/', json=encounter_data)
        assert response.status_code == 201
        encounter_id = response.get_json()['_id']

        # Update the encounter
        update_data = {'environment': 'Dungeon'}
        update_response = client.put(f'/api/encounters/{encounter_id}/', json=update_data)
        assert update_response.status_code == 200
        data = update_response.get_json()
        assert data['environment'] == 'Dungeon'

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
        response = client.post('/api/encounters/', json=encounter_data)
        assert response.status_code == 201
        encounter_id = response.get_json()['_id']

        # Delete the encounter
        delete_response = client.delete(f'/api/encounters/{encounter_id}/')
        assert delete_response.status_code == 204

        # Try to get the deleted encounter
        get_response = client.get(f'/api/encounters/{encounter_id}/')
        assert get_response.status_code == 404

def test_list_encounters(app, client, db):
    """Test listing all encounters."""
    with app.app_context():
        # Create multiple encounters with unique titles
        titles = [f'Test Encounter {i}_{int(time.time())}' for i in range(3)]
        created_encounters = []

        for title in titles:
            encounter_data = {
                'title': title,
                'environment': 'Forest',
                'party_level': 5,
                'difficulty': 'Medium',
                'description': f'Description for {title}',
                'monsters': [],
                'traps': [],
                'notes': ''
            }
            response = client.post('/api/encounters/', json=encounter_data)
            assert response.status_code == 201
            created_encounters.append(response.get_json())

        # Get all encounters
        list_response = client.get('/api/encounters/')
        assert list_response.status_code == 200
        encounters_list = list_response.get_json()

        # Verify the response
        assert len(encounters_list) == len(titles)
        returned_titles = {enc['title'] for enc in encounters_list}
        for title in titles:
            assert title in returned_titles

def test_add_monster(app, client, db):
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
        response = client.post('/api/encounters/', json=encounter_data)
        assert response.status_code == 201
        encounter_id = response.get_json()['_id']

        # Add a monster
        add_response = client.post(f'/api/encounters/{encounter_id}/monsters/goblin/')
        assert add_response.status_code == 200
        data = add_response.get_json()
        assert 'goblin' in data['monsters']

def test_remove_monster(app, client, db):
    """Test removing a monster from an encounter."""
    with app.app_context():
        # Create an encounter with a monster
        encounter_data = {
            'title': 'Test Encounter',
            'environment': 'Forest',
            'party_level': 5,
            'difficulty': 'Medium',
            'description': 'A test encounter',
            'monsters': ['goblin'],
            'traps': [],
            'notes': ''
        }
        response = client.post('/api/encounters/', json=encounter_data)
        assert response.status_code == 201
        encounter_id = response.get_json()['_id']

        # Remove the monster
        remove_response = client.delete(f'/api/encounters/{encounter_id}/monsters/goblin/')
        assert remove_response.status_code == 200
        data = remove_response.get_json()
        assert 'goblin' not in data['monsters']

def test_add_monster_invalid_monster(client, mock_dnd_api):
    """Test adding an invalid monster to an encounter."""
    # Create an encounter first
    encounter_data = {
        'title': 'Test Encounter',
        'environment': 'dungeon',
        'party_level': 5,
        'difficulty': 'medium'
    }
    response = client.post('/api/encounters/', json=encounter_data)
    encounter_id = response.json['_id']

    # Mock DnD API to return None for invalid monster
    mock_dnd_api.return_value.get_monster.return_value = None

    # Try to add invalid monster
    response = client.post(f'/api/encounters/{encounter_id}/monsters/invalid_monster/')
    assert response.status_code == 400
    assert 'not found in DnD API' in response.json['error']

def test_add_monster_api_error(client, mock_dnd_api):
    """Test handling of DnD API errors."""
    # Create an encounter first
    encounter_data = {
        'title': 'Test Encounter',
        'environment': 'dungeon',
        'party_level': 5,
        'difficulty': 'medium'
    }
    response = client.post('/api/encounters/', json=encounter_data)
    encounter_id = response.json['_id']

    # Mock DnD API to raise an exception
    mock_dnd_api.return_value.get_monster.side_effect = Exception("API connection error")

    # Try to add monster when API fails
    response = client.post(f'/api/encounters/{encounter_id}/monsters/dragon/')
    assert response.status_code == 400
    assert 'Failed to fetch monster details' in response.json['error']

def test_add_duplicate_monster(client, mock_dnd_api):
    """Test adding a duplicate monster to an encounter."""
    # Create an encounter first
    encounter_data = {
        'title': 'Test Encounter',
        'environment': 'dungeon',
        'party_level': 5,
        'difficulty': 'medium'
    }
    response = client.post('/api/encounters/', json=encounter_data)
    encounter_id = response.json['_id']

    # Mock DnD API to return valid monster data
    mock_dnd_api.return_value.get_monster.return_value = {'name': 'dragon', 'type': 'dragon'}

    # Add monster first time
    response = client.post(f'/api/encounters/{encounter_id}/monsters/dragon/')
    assert response.status_code == 200

    # Try to add same monster again
    response = client.post(f'/api/encounters/{encounter_id}/monsters/dragon/')
    assert response.status_code == 400
    assert 'already exists in encounter' in response.json['error']
