# Removed self-referential import to prevent circular import issues
# from ..ai_services.prompts import get_prompt, update_prompt

DEFAULT_PROMPTS = {
    'name_generation': "Generate a unique fantasy name for a character based on the following description: {prompt}",
    'backstory_generation': "Create a detailed backstory for a character with the following traits: {prompt}",
    # Add more default prompts for different NPC types or themes here
}

def get_prompt(template_key, user_prompt=''):
    template = DEFAULT_PROMPTS.get(template_key, '')
    return template.format(prompt=user_prompt)

# Function to update prompts if needed
def update_prompt(template_key, new_template):
    if template_key in DEFAULT_PROMPTS:
        DEFAULT_PROMPTS[template_key] = new_template
    else:
        DEFAULT_PROMPTS[template_key] = new_template

# Example usage
if __name__ == "__main__":
    print(get_prompt('name_generation', 'a brave warrior'))
    update_prompt('new_type', 'A new prompt template for {prompt}')
    print(get_prompt('new_type', 'a cunning rogue'))
