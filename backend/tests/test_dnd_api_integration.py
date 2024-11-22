import unittest
from unittest.mock import patch
import requests
from backend.app.utils.dnd_api_client import DnDApiClient
from backend.models.npc import NPC
from backend.models.encounter import Encounter

class DnDApiIntegrationTestCase(unittest.TestCase):
    @patch('requests.get')
    def test_get_monster_success(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {'name': 'Orc', 'hit_points': 15}
        client = DnDApiClient()
        result = client.get_monster('orc')
        self.assertEqual(result['name'], 'Orc')

    def test_npc_add_spell(self):
        npc = NPC(name='Gandalf', race='Wizard', class_type='Mage', level=5, background='Sage', personality='Wise', abilities={}, skills=[], equipment=[], description='', portrait_url='')
        with patch.object(DnDApiClient, 'get_spell', return_value={'name': 'Fireball', 'level': 3}):
            npc.add_spell('Fireball')
            self.assertEqual(len(npc.spells), 1)
            self.assertEqual(npc.spells[0]['name'], 'Fireball')

    def test_encounter_add_monster(self):
        encounter = Encounter(title='Battle of Helm', description='Epic battle', difficulty='Hard', npcs=[], monsters=[], environment='Fortress', loot=[], notes='')
        with patch.object(DnDApiClient, 'get_monster', return_value={'name': 'Orc', 'hit_points': 15}):
            encounter.add_monster('Orc')
            self.assertEqual(len(encounter.monster_data), 1)
            self.assertEqual(encounter.monster_data[0]['name'], 'Orc')

if __name__ == '__main__':
    unittest.main()
