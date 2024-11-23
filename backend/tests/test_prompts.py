import unittest
from backend.ai_services import prompts

class TestPromptManagement(unittest.TestCase):

    def test_get_prompt_with_default(self):
        result = prompts.get_prompt('name_generation', 'a brave warrior')
        self.assertIn('a brave warrior', result)

    def test_get_prompt_with_nonexistent_key(self):
        result = prompts.get_prompt('nonexistent_key', 'a brave warrior')
        self.assertEqual(result, '')

    def test_update_prompt(self):
        prompts.update_prompt('new_type', 'A new prompt template for {prompt}')
        result = prompts.get_prompt('new_type', 'a cunning rogue')
        self.assertIn('a cunning rogue', result)

if __name__ == '__main__':
    unittest.main()
