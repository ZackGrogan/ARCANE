# ARCANE Backend API

ARCANE (Advanced Role-playing Campaign And NPC Engine) is a D&D 5E campaign management system that helps Dungeon Masters create and manage their campaigns, NPCs, and encounters.

## Version v0.7.0-BETA

### Features

- **NPC Management**
  - Create, read, update, and delete NPCs
  - Generate random NPCs with AI-assisted name and backstory generation
  - Manage NPC equipment, spells, and abilities

- **Campaign Management**
  - Create and manage multiple campaigns
  - Add/remove NPCs from campaigns
  - Track campaign progress and notes

- **Encounter Management**
  - Create and manage combat encounters
  - Add/remove NPCs and monsters from encounters
  - Track initiative and combat state

### API Endpoints

#### NPCs
- `POST /api/npcs/` - Create a new NPC
- `GET /api/npcs/` - List all NPCs
- `GET /api/npcs/<id>` - Get a specific NPC
- `PUT /api/npcs/<id>` - Update an NPC
- `DELETE /api/npcs/<id>` - Delete an NPC

#### Campaigns
- `POST /api/campaigns/` - Create a new campaign
- `GET /api/campaigns/` - List all campaigns
- `GET /api/campaigns/<id>` - Get a specific campaign
- `PUT /api/campaigns/<id>` - Update a campaign
- `DELETE /api/campaigns/<id>` - Delete a campaign
- `POST /api/campaigns/<id>/npcs/<npc_id>` - Add NPC to campaign
- `DELETE /api/campaigns/<id>/npcs/<npc_id>` - Remove NPC from campaign

#### Encounters
- `POST /api/encounters/` - Create a new encounter
- `GET /api/encounters/` - List all encounters
- `GET /api/encounters/<id>` - Get a specific encounter
- `PUT /api/encounters/<id>` - Update an encounter
- `DELETE /api/encounters/<id>` - Delete an encounter
- `POST /api/encounters/<id>/npcs/<npc_id>` - Add NPC to encounter
- `DELETE /api/encounters/<id>/npcs/<npc_id>` - Remove NPC from encounter

### Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -e .
   ```

3. Set up MongoDB:
   - Install MongoDB
   - Start MongoDB service
   - Create a database named 'arcane'

4. Run the development server:
   ```bash
   python -m flask run
   ```

### Testing

Run tests with pytest:
```bash
python -m pytest tests/
```

### Recent Changes (v0.7.0-BETA)

1. Project Structure
   - Cleaned up project structure
   - Removed duplicate files and directories
   - Improved import paths

2. Error Handling
   - Enhanced error handling with proper application context management
   - Added comprehensive error messages
   - Improved error logging

3. API Improvements
   - Added 404 responses for missing resources
   - Standardized API response formats
   - Added NPC management endpoints for campaigns and encounters

### Known Issues

1. MongoDB connection must be configured manually
2. No authentication system in place yet
3. Limited validation on some input fields

### Coming Soon

1. Authentication and authorization
2. Advanced NPC generation with AI
3. Initiative tracking for encounters
4. Campaign timeline management
