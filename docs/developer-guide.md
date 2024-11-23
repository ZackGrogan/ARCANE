# ARCANE Developer Guide

## Project Structure

```
ARCANE/
├── backend/
│   ├── api/
│   │   ├── routes/
│   │   │   ├── campaign_routes.py
│   │   │   ├── encounter_routes.py
│   │   │   └── npc_routes.py
│   │   └── __init__.py
│   ├── models/
│   │   ├── campaign.py
│   │   ├── encounter.py
│   │   └── npc.py
│   ├── utils/
│   │   ├── dnd_api_client.py
│   │   ├── flux_client.py
│   │   └── gemini_client.py
│   ├── tests/
│   │   ├── api/
│   │   ├── integration/
│   │   └── unit/
│   └── __init__.py
├── docs/
├── static/
└── templates/
```

## Development Setup

### Prerequisites
- Python 3.10+
- MongoDB
- Git
- Poetry (recommended for dependency management)

### Environment Setup
1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Unix: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Set up environment variables in `.env`

## Architecture

### Backend Components

#### 1. Models
- `Campaign`: Manages campaign data and relationships
- `Encounter`: Handles combat encounters and monster management
- `NPC`: Manages NPC data and AI-generated content

#### 2. API Routes
- RESTful endpoints for all entities
- Consistent error handling
- JSON response format

#### 3. External Services
- DnD 5e API: Monster data and spells
- Google Gemini: AI content generation
- FLUX: Image generation

### Database Schema

#### Campaign Collection
```json
{
  "_id": ObjectId,
  "title": String,
  "description": String,
  "npcs": Array<ObjectId>,
  "encounters": Array<ObjectId>
}
```

#### Encounter Collection
```json
{
  "_id": ObjectId,
  "title": String,
  "environment": String,
  "party_level": Integer,
  "difficulty": String,
  "description": String,
  "monsters": Array<String>,
  "traps": Array<Object>,
  "notes": String
}
```

#### NPC Collection
```json
{
  "_id": ObjectId,
  "name": String,
  "race": String,
  "class": String,
  "backstory": String,
  "description": String,
  "profile_picture_url": String
}
```

## Testing

### Running Tests
- All tests: `pytest`
- Specific test file: `pytest path/to/test.py`
- With coverage: `pytest --cov=backend`

### Test Structure
1. Unit Tests
   - Model functionality
   - Utility functions
   - Individual components

2. Integration Tests
   - API endpoints
   - Database operations
   - External service integration

3. Manual Tests
   - End-to-end workflows
   - UI interactions

## API Documentation

See the API documentation in `docs/New-SpecSheet.md` for detailed endpoint specifications.

## Contributing

### Code Style
- Follow PEP 8 guidelines
- Use type hints
- Add docstrings for classes and functions
- Keep functions focused and modular

### Git Workflow
1. Create feature branch from `main`
2. Make changes and add tests
3. Run full test suite
4. Create pull request
5. Address review comments
6. Merge after approval

### Pull Request Guidelines
- Clear description of changes
- Test coverage for new features
- Documentation updates
- No breaking changes without discussion

## Deployment

### Production Setup
1. Set up MongoDB instance
2. Configure environment variables
3. Install production dependencies
4. Set up WSGI server (e.g., Gunicorn)
5. Configure reverse proxy (e.g., Nginx)

### Environment Variables
```bash
MONGODB_URI=mongodb://[username:password@]host[:port]/database
GEMINI_API_KEY=your_gemini_api_key
FLUX_API_KEY=your_flux_api_key
FLASK_ENV=production
```

### Monitoring
- Set up logging
- Monitor API endpoints
- Track external service usage
- Monitor database performance

## Security

### Best Practices
1. Secure API keys
2. Input validation
3. Error handling
4. Rate limiting
5. Database security

### Known Issues
- None currently

## Performance Optimization

### Guidelines
1. Use database indexes
2. Implement caching
3. Optimize database queries
4. Minimize external API calls
5. Use async operations where appropriate
