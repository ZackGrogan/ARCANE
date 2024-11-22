class Encounter:
    def __init__(self, title, description, difficulty, npcs, monsters, environment, loot, notes):
        self.title = title
        self.description = description
        self.difficulty = difficulty
        self.npcs = npcs
        self.monsters = monsters
        self.environment = environment
        self.loot = loot
        self.notes = notes
        self.monster_data = []  # Initialize monster_data as an empty list

    def add_monster(self, monster_name):
        # Add a monster to the encounter
        self.monster_data.append({'name': monster_name})
