"""Manual testing script for API endpoints."""
import json
from pprint import pprint
from backend import create_app
import requests

# Create application and test client globally
app = create_app({
    'TESTING': True,
    'MONGO_URI': 'mongodb://localhost:27017/test_db'
})
client = app.test_client()

def print_response(response):
    print(f"Status: {response.status_code}")
    print("Response:")
    try:
        pprint(response.get_json())
    except Exception as e:
        print(f"Error parsing response: {str(e)}")

def test_npc_endpoints():
    """Test NPC endpoints."""
    with app.app_context():
        print("\n=== Testing NPC Endpoints ===\n")

        # Test NPC creation with valid data
        print("1. Creating NPC with valid data")
        valid_npc = {
            'name': 'Test NPC',
            'race': 'Human',
            'npc_class': 'Fighter',
            'level': 5,
            'alignment': 'Lawful Good',
            'abilities': {
                'strength': 16,
                'dexterity': 14,
                'constitution': 15,
                'intelligence': 12,
                'wisdom': 13,
                'charisma': 11
            }
        }
        try:
            response = client.post('/api/npcs/', json=valid_npc)
            print_response(response)
            response_data = response.get_json()
            npc_id = response_data.get('_id')
        except Exception as e:
            print(f"Error parsing response: {str(e)}")
            return

        # Test NPC creation with invalid data
        print("\n2. Creating NPC with invalid data (missing required fields)")
        invalid_npc = {
            'name': 'Invalid NPC'
        }
        try:
            response = client.post('/api/npcs/', json=invalid_npc)
            print_response(response)
        except Exception as e:
            print(f"Error parsing response: {str(e)}")

        # Get all NPCs
        print("\n4. Getting all NPCs")
        try:
            response = client.get('/api/npcs/')
            print_response(response)
        except Exception as e:
            print(f"Error parsing response: {str(e)}")

def test_campaign_endpoints():
    """Test Campaign endpoints."""
    with app.app_context():
        print("\n=== Testing Campaign Endpoints ===\n")

        # Test Campaign creation
        print("1. Creating Campaign")
        campaign_data = {
            'title': 'Test Campaign',
            'description': 'A test campaign',
            'start_date': '2024-01-01',
            'status': 'active',
            'notes': 'Test notes'
        }
        try:
            response = client.post('/api/campaigns/', json=campaign_data)
            print_response(response)
            response_data = response.get_json()
            campaign_id = response_data.get('_id')
        except Exception as e:
            print(f"Error parsing response: {str(e)}")
            return

        # Get all campaigns
        print("\n2. Getting all campaigns")
        try:
            response = client.get('/api/campaigns/')
            print_response(response)
        except Exception as e:
            print(f"Error parsing response: {str(e)}")

def test_encounter_endpoints():
    """Test Encounter endpoints."""
    with app.app_context():
        print("\n=== Testing Encounter Endpoints ===\n")

        # Test Encounter creation
        print("1. Creating Encounter")
        encounter_data = {
            'title': 'Test Encounter',
            'environment': 'Forest',
            'party_level': 5,
            'difficulty': 'Medium',
            'notes': 'A test encounter',
            'monsters': ['Goblin', 'Wolf'],
            'traps': ['Pit Trap']
        }
        try:
            response = client.post('/api/encounters/', json=encounter_data)
            print_response(response)
            response_data = response.get_json()
            encounter_id = response_data.get('_id')
        except Exception as e:
            print(f"Error parsing response: {str(e)}")
            return

        # Get all encounters
        print("\n2. Getting all encounters")
        try:
            response = client.get('/api/encounters/')
            print_response(response)
        except Exception as e:
            print(f"Error parsing response: {str(e)}")

def main():
    """Run all manual tests."""
    test_npc_endpoints()
    test_campaign_endpoints()
    test_encounter_endpoints()

if __name__ == '__main__':
    main()
