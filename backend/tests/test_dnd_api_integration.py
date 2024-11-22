import os
import unittest
from unittest.mock import patch
import http.client
import json

from backend.app.utils.dnd_api_client import DnDApiClient
from backend.app.models.npc import NPC
from backend.app.models.encounter import Encounter

class TestDnDApiIntegration(unittest.TestCase):
    @patch('http.client.HTTPConnection')
    def test_get_monster_success(self, mock_http_conn):
        mock_response = mock_http_conn.return_value.getresponse.return_value
        mock_response.status = 200
        mock_response.read.return_value = b'{"name": "Orc", "hit_points": 15}'
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
