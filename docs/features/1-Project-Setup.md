# Project Setup

## Technology Stack

### Front-End
- React (with hooks)
- Tailwind CSS
- Shadcn/ui
- DaisyUI

### Back-End
- Python (Django)
- MongoDB (with PyMongo or Djongo driver)
- RESTful API architecture

### AI Integration
- Google Gemini Pro API
- FLUX.1-dev API

### Map Integration
- Azgaar's Fantasy Map Generator Integration

### Deployment
- Docker

### Logging
- Python's logging library

## Project Structure
```
arcane/
├── backend/
│   ├── manage.py
│   ├── arcane_backend/
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── apps/
│   │   ├── npcs/
│   │   ├── encounters/
│   │   ├── campaigns/
│   │   ├── maps/
│   │   └── ai_services/
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   ├── tailwind.config.js
│   └── Dockerfile
├── docker-compose.yml
└── .env.example
```

## Environment Setup
1. Python environment setup
2. Node.js and npm setup
3. MongoDB installation
4. Docker installation
5. Development tools configuration
