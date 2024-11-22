class NPC:
    def __init__(self, name, race, class_type, level, background, personality, abilities, skills, equipment, description, portrait_url):
        self.name = name
        self.race = race
        self.class_type = class_type
        self.level = level
        self.background = background
        self.personality = personality
        self.abilities = abilities
        self.skills = skills
        self.equipment = equipment
        self.description = description
        self.portrait_url = portrait_url
        self.spells = []  # Initialize spells as an empty list

    def add_spell(self, spell_name):
        # Add a spell to the NPC
        self.spells.append({'name': spell_name})
