# Backend Development

## Data Models

### NPC Model
```python
class NPC:
    name: str
    race: str
    class_type: str
    level: int
    background: str
    personality: str
    abilities: Dict[str, int]
    skills: List[str]
    equipment: List[str]
    description: str
    portrait_url: str
```

### Encounter Model
```python
class Encounter:
    title: str
    description: str
    difficulty: str
    npcs: List[NPC]
    monsters: List[str]
    environment: str
    loot: List[str]
    notes: str
```

### Campaign Model
```python
class Campaign:
    title: str
    description: str
    setting: str
    level_range: Tuple[int, int]
    encounters: List[Encounter]
    npcs: List[NPC]
    maps: List[str]
    notes: str
```

### Map Model
```python
class Map:
    title: str
    description: str
    image_url: str
    markers: List[Dict]
    scale: str
    environment_type: str
    notes: str
```

## API Endpoints

### NPC Endpoints
- GET /api/npcs/ - List all NPCs
- POST /api/npcs/ - Create new NPC
- GET /api/npcs/{id}/ - Get NPC details
- PUT /api/npcs/{id}/ - Update NPC
- DELETE /api/npcs/{id}/ - Delete NPC
- POST /api/npcs/generate/ - Generate NPC using AI

### Map Endpoints
- GET /api/maps/ - List all maps
- POST /api/maps/ - Create new map
- GET /api/maps/{id}/ - Get map details
- PUT /api/maps/{id}/ - Update map
- DELETE /api/maps/{id}/ - Delete map
- POST /api/maps/generate/ - Generate map using AI

## AI Services Integration

### AI Service Interface
```python
class AIService:
    def generate_npc(self, parameters: Dict) -> NPC:
        pass
    
    def generate_map(self, parameters: Dict) -> Map:
        pass
    
    def generate_encounter(self, parameters: Dict) -> Encounter:
        pass
```

### Google Gemini Pro Implementation
```python
class GeminiService(AIService):
    def generate_npc(self, parameters: Dict) -> NPC:
        # Implementation using Google Gemini Pro
        pass
```

### FLUX Implementation
```python
class FLUXService(AIService):
    def generate_portrait(self, npc: NPC) -> str:
        # Implementation using FLUX API
        pass
```
