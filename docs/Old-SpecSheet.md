ARCANE (AI-Driven RPG Campaign Assistant & Narrative Engine)

Development Plan - Phase 1

---

Overview

ARCANE is a Python-centric, web-based application designed to assist Dungeon Masters (DMs) and players in creating and managing content for Dungeons & Dragons 5th Edition (D&D 5e) campaigns. The application focuses on providing tools for character creation, encounter generation, campaign management, and integrating advanced features like AI-assisted content creation and fantasy map generation.

This development plan outlines the roadmap for Phase 1, incorporating all the specified features, technology choices, and considerations. The plan prioritizes Python for backend development and includes specific examples where applicable.

---

Table of Contents

1. Project Setup

Technology Stack

Project Structure

Environment Setup

2. Backend Development

Data Models

API Endpoint Development

Integration with External APIs

AI Services Integration

3. Front-End Development

UI Components and Pages

State Management and Routing

API Communication

4. Testing and Quality Assurance

Testing Strategy

Implementing Tests

5. Logging

Integrate Python's logging

Library

Error Analysis

6. Dockerization

Creating Dockerfiles

Docker Compose Setup

Building and Running Containers

7. Additional Considerations

Security

Performance Optimizations

Code Quality and Documentation

8. Roadmap Summary

9. Conclusion

10. Appendices

Appendix A: Environment Variables Example

Appendix B: Useful Commands

Appendix C: Tools and Libraries

---

Project Setup

Technology Stack

Front-End

:

React

(with hooks)

Tailwind CSS

Shadcn/ui

DaisyUI

Back-End

:

Python (Django)

Prioritize Python for all backend services and features.

MongoDB

(with PyMongo or Djongo driver)

RESTful API

architecture

AI Integration

:

Google Gemini Pro API

FLUX.1-dev API

Map Integration

:

Azgaar's Fantasy Map Generator Integration

Deployment

:

Docker

Logging

:

Python's logging

library

Project Structure

Organize the project directories to separate concerns and ensure maintainability.

arcane/

├── backend/

│   ├── manage.py

│   ├── arcane_backend/

│   │   ├── init

.py

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

├── .env.example

└── README.md

Environment Setup

Backend Setup

1. Install Python 3.10 or above

.

2. Create a virtual environment

:

python3 -m venv venv

source venv/bin/activate

3. Install required packages

:

pip install django djangorestframework djongo pymongo requests

4. Create a Django project

:

django-admin startproject arcane_backend

5. Configure settings.py

to include installed apps and database settings.

Frontend Setup

1. Install Node.js v18 and npm

.

2. Initialize React project

:

npx create-react-app frontend

3. Install dependencies

:

npm install tailwindcss postcss autoprefixer axios react-router-dom

4. Configure Tailwind CSS

:

npx tailwindcss init -p

Docker Setup

1. Install Docker and Docker Compose

.

2. Create Dockerfiles

for the backend and frontend.

3. Write docker-compose.yml

to orchestrate containers.

---

Backend Development

Data Models

Define Models using Django ORM

1. NPC Model

:

apps/npcs/models.py

from django.db import models

class NPC(models.Model):

npc_id = models.CharField(max_length=50, primary_key=True)

name = models.CharField(max_length=100)

race = models.CharField(max_length=50)

npc_class = models.CharField(max_length=50)

background = models.TextField()

alignment = models.CharField(max_length=50)

personality_traits = models.JSONField()

backstory = models.TextField()

appearance = models.TextField()

skills = models.JSONField()

equipment = models.JSONField()

roleplaying_traits = models.JSONField()

profile_picture_url = models.URLField()

conversation_history = models.JSONField()

def str

(self):

return self.name

2. Encounter Model

:

apps/encounters/models.py

class Encounter(models.Model):

encounter_id = models.CharField(max_length=50, primary_key=True)

title = models.CharField(max_length=200)

description = models.TextField()

biome = models.CharField(max_length=100)

weather_conditions = models.CharField(max_length=100)

environmental_hazards = models.JSONField()

monsters = models.JSONField()

loot = models.JSONField()

roleplaying_scenarios = models.JSONField()

difficulty = models.CharField(max_length=50)

tags = models.JSONField()

def str

(self):

return self.title

3. Campaign Model

:

apps/campaigns/models.py

class Campaign(models.Model):

campaign_id = models.CharField(max_length=50, primary_key=True)

name = models.CharField(max_length=200)

description = models.TextField()

npcs = models.ManyToManyField('npcs.NPC', related_name='campaigns')

encounters = models.ManyToManyField('encounters.Encounter', related_name='campaigns')

maps = models.ManyToManyField('maps.Map', related_name='campaigns')

def str

(self):

return self.name

4. Map Model

:

apps/maps/models.py

class Map(models.Model):

map_id = models.CharField(max_length=50, primary_key=True)

name = models.CharField(max_length=200)

description = models.TextField()

map_data = models.JSONField()

created_at = models.DateTimeField(auto_now_add=True)

def str

(self):

return self.name

API Endpoint Development

Prioritize Python for All API Endpoints

Set Up Django REST Framework

:

1. Add 'rest_framework'

to INSTALLED_APPS

in settings.py

.

2. Create serializers

for data models.

NPC Serializer

:

apps/npcs/serializers.py

from rest_framework import serializers

from .models import NPC

class NPCSerializer(serializers.ModelSerializer):

class Meta:

model = NPC

fields = 'all

'

NPC ViewSet

:

apps/npcs/views.py

from rest_framework import viewsets

from .models import NPC

from .serializers import NPCSerializer

class NPCViewSet(viewsets.ModelViewSet):

queryset = NPC.objects.all()

serializer_class = NPCSerializer

URL Routing

:

arcane_backend/urls.py

from django.urls import path, include

from rest_framework import routers

from apps.npcs.views import NPCViewSet

from apps.encounters.views import EncounterViewSet

from apps.campaigns.views import CampaignViewSet

from apps.maps.views import MapViewSet

router = routers.DefaultRouter()

router.register(r'npcs', NPCViewSet)

router.register(r'encounters', EncounterViewSet)

router.register(r'campaigns', CampaignViewSet)

router.register(r'maps', MapViewSet)

urlpatterns = [

path('api/', include(router.urls)),

]

Integration with External APIs

D&D 5e API Integration

Utility Function to Fetch Data

:

apps/external_apis/dnd5e.py

import requests

from django.core.cache import cache

def get_monster_data(monster_name):

cache_key = f'monster_{monster_name}'

monster_data = cache.get(cache_key)

if monster_data:

return monster_data

api_url = f'https://www.dnd5eapi.co/api/monsters/{monster_name}'

response = requests.get(api_url)

if response.status_code == 200:

monster_data = response.json()

cache.set(cache_key, monster_data, timeout=86400)  # Cache for 1 day

return monster_data

else:

return None

Azgaar's Fantasy Map Generator Integration

Since Azgaar's Fantasy Map Generator does not offer a direct API, integration involves embedding the generator or importing/exporting map data.

Map Import/Export Functionality

:

Option 1: Embedding the Generator

:

Use an iframe or embedded component to allow users to access the map generator within the application.

Limitations

: May have cross-origin issues or limited functionality.

Option 2: Import/Export Map Data

:

Allow users to upload map files generated by Azgaar's tool.

Provide an interface to display and interact with the uploaded maps.

Map Model with Map Data

:

apps/maps/models.py

class Map(models.Model):

map_id = models.CharField(max_length=50, primary_key=True)

name = models.CharField(max_length=200)

description = models.TextField()

map_file = models.FileField(upload_to='maps/')

created_at = models.DateTimeField(auto_now_add=True)

def str

(self):

return self.name

Map Upload Endpoint

:

apps/maps/views.py

from rest_framework import viewsets

from .models import Map

from .serializers import MapSerializer

class MapViewSet(viewsets.ModelViewSet):

queryset = Map.objects.all()

serializer_class = MapSerializer

Map Serializer

:

apps/maps/serializers.py

from rest_framework import serializers

from .models import Map

class MapSerializer(serializers.ModelSerializer):

class Meta:

model = Map

fields = 'all

'

AI Services Integration

Design an Abstract Base Class for AI Services

AI Service Interface

:

apps/ai_services/base.py

from abc import ABC, abstractmethod

class AIServiceInterface(ABC):

@abstractmethod

def generate_name(self, prompt):

pass

@abstractmethod

def generate_backstory(self, prompt):

pass

@abstractmethod

def generate_profile_picture(self, description):

pass

Implement AI Clients

Google Gemini Pro API Client

:

apps/ai_services/gemini.py

import requests

class GoogleGeminiProClient(AIServiceInterface):

def init

(self, api_key):

self.api_key = api_key

self.endpoint = 'https://gemini.googleapis.com/v1/'

def generate_name(self, prompt):

# Implement API call to Google Gemini Pro

pass

def generate_backstory(self, prompt):

# Implement API call to Google Gemini Pro

pass

def generate_profile_picture(self, description):

# Delegate to FLUXClient if not supported

pass

FLUX.1-dev API Client

:

apps/ai_services/flux.py

class FLUXClient:

def init

(self, api_key):

self.api_key = api_key

def generate_profile_picture(self, description, negative_prompt=None):

# Implement API call to FLUX.1-dev API

pass

Create API Endpoints for AI-Assisted Creation

Generate NPC Endpoint

:

apps/npcs/views.py

from rest_framework.decorators import action

from rest_framework.response import Response

from .models import NPC

from .serializers import NPCSerializer

from apps.ai_services.gemini import GoogleGeminiProClient

class NPCViewSet(viewsets.ModelViewSet):

queryset = NPC.objects.all()

serializer_class = NPCSerializer

@action(detail=False, methods=['post'])

def generate(self, request):

prompt = request.data.get('prompt')

ai_client = GoogleGeminiProClient(api_key='YOUR_GEMINI_API_KEY')

name = ai_client.generate_name(prompt)

backstory = ai_client.generate_backstory(prompt)

# Assemble NPC data

npc_data = {

'name': name,

'backstory': backstory,

# ... other fields

}

serializer = self.get_serializer(data=npc_data)

serializer.is_valid(raise_exception=True)

self.perform_create(serializer)

return Response(serializer.data)

Profile Picture Generation Endpoint

:

apps/npcs/views.py

from apps.ai_services.flux import FLUXClient

class NPCViewSet(viewsets.ModelViewSet):

# ...

@action(detail=True, methods=['post'])

def generate_profile_picture(self, request, pk=None):

npc = self.get_object()

description = request.data.get('description')

flux_client = FLUXClient(api_key='YOUR_FLUX_API_KEY')

image_url = flux_client.generate_profile_picture(description)

npc.profile_picture_url = image_url

npc.save()

return Response({'profile_picture_url': image_url})

---

Front-End Development

UI Components and Pages

1. NPC and Character Creation Forms

Manual Creation Form

:

Fields for all NPC attributes.

Implement form validation using React hooks and form libraries like react-hook-form

.

AI-Assisted Creation Form

:

Text area for user prompts.

Button to trigger AI generation via API call.

Display generated content for user review before saving.

Component Example

:

// src/components/NpcCreationForm.js

import React, { useState } from 'react';

import axios from '../apiClient';

function NpcCreationForm() {

const [formData, setFormData] = useState({

name: '',

race: '',

npc_class: '',

// ... other fields

});

const [aiPrompt, setAiPrompt] = useState('');

const [aiGeneratedData, setAiGeneratedData] = useState(null);

const handleAiGeneration = async () => {

const response = await axios.post('npcs/generate/', { prompt: aiPrompt });

setAiGeneratedData(response.data);

};

const handleChange = (e) => {

setFormData({ ...formData, [e.target.name]: e.target.value });

};

const handleSubmit = async (e) => {

e.preventDefault();

const response = await axios.post('npcs/', formData);

// Handle success or error

};

return (

Create NPC

{/* AI Generation Section */}

setAiPrompt(e.target.value)}

placeholder="Enter prompt for AI generation"

/>

Generate with AI

{/* Display AI Generated Data */}

{aiGeneratedData && (

AI Generated NPC

{/* Display fields */}

)}

{/* Manual Input Form */}

{/* Other form inputs */}

Create NPC

);

}

export default NpcCreationForm;

2. Profile Picture Generation Interface

Input for Description

to generate profile pictures.

Display Generated Image

after API call.

Option to Confirm and Save

the generated image to the NPC profile.

Component Example

:

// src/components/ProfilePictureGenerator.js

import React, { useState } from 'react';

import axios from '../apiClient';

function ProfilePictureGenerator({ npcId }) {

const [description, setDescription] = useState('');

const [imageUrl, setImageUrl] = useState('');

const generateProfilePicture = async () => {

const response = await axios.post(npcs/${npcId}/generate_profile_picture/

, { description });

setImageUrl(response.data.profile_picture_url);

};

return (

Generate Profile Picture

setDescription(e.target.value)}

placeholder="Describe the appearance"

/>

Generate

{imageUrl && (

{/* Optionally save or discard the image */}

)}

);

}

export default ProfilePictureGenerator;

3. Encounter Generation Interface

Form to Input Parameters

:

Party level

Difficulty rating

Thematic elements

Option to Generate Encounters via AI

.

Display Generated Encounter Details

for review and modification.

4. Campaign Management Dashboard

Dashboard Components

:

List of campaigns

Quick links to NPCs, encounters, and maps

Options to create, edit, and delete campaigns

5. Map Integration Interface

Map Upload and Display

:

Interface to upload maps from Azgaar's Fantasy Map Generator.

Display maps within the application using suitable libraries (e.g., Leaflet.js).

Map Editing Features

:

Basic interactions like zooming, panning.

Potentially annotate maps with markers for NPC locations or encounters.

State Management and Routing

Use React Hooks

for local state management.

React Router

for navigation between components.

App Routing

:

// src/App.js

import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

import NpcCreationForm from './components/NpcCreationForm';

import NpcList from './components/NpcList';

import CampaignDashboard from './components/CampaignDashboard';

import MapUpload from './components/MapUpload';

function App() {

return (

} />

} />

} />

} />

{/* Additional routes */}

);

}

export default App;

API Communication

Set Up Axios Instance

:

// src/apiClient.js

import axios from 'axios';

const apiClient = axios.create({

baseURL: 'http://localhost:8000/api/',

});

export default apiClient;

Use Axios for API Calls

:

// src/components/NpcList.js

import React, { useEffect, useState } from 'react';

import axios from '../apiClient';

function NpcList() {

const [npcs, setNpcs] = useState([]);

useEffect(() => {

axios.get('npcs/')

.then(response => setNpcs(response.data))

.catch(error => console.error('Error fetching NPCs:', error));

}, []);

return (

{/* Render NPCs */}

);

}

export default NpcList;

---

Testing and Quality Assurance

Testing Strategy

Backend Testing

:

Use pytest

for unit tests.

Test models, views, serializers, and utility functions.

Use Django's built-in test client for integration tests.

Frontend Testing

:

Use Jest

and React Testing Library

for component tests.

Write tests for critical user interactions.

Implementing Tests

Backend Test Example

apps/npcs/tests/test_models.py

from django.test import TestCase

from apps.npcs.models import NPC

class NPCTestCase(TestCase):

def setUp(self):

NPC.objects.create(

npc_id='npc_0001',

name='Elara',

race='Elf',

npc_class='Wizard'

)

def test_npc_creation(self):

npc = NPC.objects.get(npc_id='npc_0001')

self.assertEqual(npc.name, 'Elara')

self.assertEqual(npc.race, 'Elf')

self.assertEqual(npc.npc_class, 'Wizard')

Frontend Test Example

// src/components/tests

/NpcCreationForm.test.js

import { render, screen, fireEvent } from '@testing-library/react';

import NpcCreationForm from '../NpcCreationForm';

test('renders NPC creation form', () => {

render();

const nameInput = screen.getByPlaceholderText(/Name/i);

expect(nameInput).toBeInTheDocument();

});

test('submits form data', async () => {

render();

const nameInput = screen.getByPlaceholderText(/Name/i);

fireEvent.change(nameInput, { target: { value: 'Elara' } });

// Simulate form submission and assert API call

});

---

Logging

Integrate Python's logging

Library

Configure Logging

arcane_backend/settings.py

import os

import logging

LOGGING = {

'version': 1,

'disable_existing_loggers': False,

'formatters': {

'standard': {

'format': '{levelname} {asctime} {module} {message}',

'style': '{',

},

},

'handlers': {

'file': {

'level': 'DEBUG',

'class': 'logging.handlers.RotatingFileHandler',

'filename': os.path.join(BASE_DIR, 'logs/arcane.log'),

'maxBytes': 1024 * 1024 * 5,  # 5 MB

'backupCount': 5,

'formatter': 'standard',

},

},

'loggers': {

'arcane': {

'handlers': ['file'],

'level': 'DEBUG',

'propagate': True,

},

},

}

Use Logging in Code

apps/npcs/views.py

import logging

logger = logging.getLogger('arcane')

class NPCViewSet(viewsets.ModelViewSet):

# ...

def create(self, request, *args, **kwargs):

try:

response = super().create(request, *args, kwargs)

logger.info(f'NPC created successfully: {response.data["npc_id"]}')

return response

except Exception as e:

logger.error('Error creating NPC', exc_info=True)

return Response({'error': 'Failed to create NPC'}, status=500)

Error Analysis

Enable Detailed Error Logging.

Monitor Log Files regularly to detect patterns and issues.

Implement Custom Error Handlers for meaningful error responses.

---

Dockerization

Creating Dockerfiles

Backend Dockerfile

backend/Dockerfile

FROM python:3.10-slim

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

Frontend Dockerfile

frontend/Dockerfile

FROM node:18-alpine

WORKDIR /app

COPY package.json package-lock.json ./

RUN npm install

COPY . .

EXPOSE 3000

CMD ["npm", "start"]

Docker Compose Setup

docker-compose.yml:

version: '3'

services:

backend:

build: ./backend

ports:

"8000:8000"

volumes:

./backend:/app

depends_on:

mongodb

frontend:

build: ./frontend

ports:

"3000:3000"

volumes:

./frontend:/app

stdin_open: true

tty: true

mongodb:

image: mongo

ports:

"27017:27017"

volumes:

mongo-data:/data/db

volumes:

mongo-data:

Building and Running Containers

Build Docker Images:

docker-compose build

Run Containers:

docker-compose up

Test Services:

Backend API: http://localhost:8000/api/

Frontend: http://localhost:3000

MongoDB: Accessible on port 27017

---

Additional Considerations

Security

Input Validation and Sanitization:

Validate all user inputs on both frontend and backend.

Use Django forms and serializers for validation.

Authentication and Authorization:

Implement user authentication using Django’s built-in authentication system or third-party packages like django-allauth

.

Protect API endpoints and restrict access where necessary.

API Key Management:

Store sensitive information in environment variables.

Do not commit API keys to version control.

HTTPS and Secure Communication:

Use HTTPS in production environments.

Consider using reverse proxies like Nginx for SSL termination.

Performance Optimizations

Database Indexing:

Add indexes to frequently queried fields in MongoDB.

Monitor query performance and optimize accordingly.

Caching:

Implement caching for API responses and static assets.

Utilize Django’s caching frameworks or external tools like Redis.

Asynchronous Tasks:

Offload heavy computations or external API calls to asynchronous tasks using tools like Celery and RabbitMQ.

Load Testing:

Perform load testing using tools like Locust or JMeter to identify bottlenecks.

Code Quality and Documentation

Code Formatting and Linting:

Use flake8

and black

for formatting Python code.

Use eslint

and prettier

for JavaScript code.

Documentation:

Write docstrings for functions and classes.

Maintain an updated README and CONTRIBUTING guide.

Use tools like Sphinx for generating documentation.

Version Control Practices:

Follow a branching strategy (e.g., Gitflow).

Write meaningful commit messages.

Continuous Integration and Deployment (CI/CD):

Set up automated testing using tools like GitHub Actions or Jenkins.

Automate deployment processes where possible.

---

Roadmap Summary

Phase 1 Milestones

1.

Week 1-2: Project Setup

Set up development environment.

Establish project structure.

Configure Docker and initial services.

2.

Week 3-4: Backend Development

Define data models and serializers.

Implement API endpoints for NPCs, encounters, campaigns, and maps.

Integrate with D&D 5e API and Azgaar's Fantasy Map Generator.

3.

Week 5-6: Front-End Development

Build UI components for key features.

Implement state management and routing.

Integrate API communication.

4.

Week 7: Testing and Logging

Write unit and integration tests.

Set up logging mechanisms.

Perform debugging and QA.

5.

Week 8: Dockerization and Finalization

Finalize Docker configuration.

Test containerization and deployment.

Prepare documentation and deployment guides.

---

Conclusion

By following this comprehensive development plan, the ARCANE application will effectively deliver a robust, Python-centric solution for D&D 5e campaign creation and management. Integrating key features like AI-assisted content generation, encounter creation, and fantasy map integration provides users with powerful tools to enhance their campaigns.

Prioritizing Python for backend development ensures consistency, leverages Python's rich ecosystem, and facilitates future feature expansion. The inclusion of detailed steps, technical considerations, and code examples aims to guide the development process efficiently.

---

Appendices

Appendix A: Environment Variables Example

Create a .env

file in the root directory.

Django settings

DEBUG=True

SECRET_KEY=your_secret_key

ALLOWED_HOSTS=localhost,127.0.0.1

Database

MONGODB_HOST=mongodb

MONGODB_PORT=27017

MONGODB_NAME=arcane_db

External APIs

GEMINI_API_KEY=your_gemini_api_key

FLUX_API_KEY=your_flux_api_key

Other settings

Appendix B: Useful Commands

Run Migrations:

docker-compose run backend python manage.py migrate

Create Superuser:

docker-compose run backend python manage.py createsuperuser

Access MongoDB Shell:

docker-compose exec mongodb mongo

Run Tests:

docker-compose run backend pytest

Appendix C: Tools and Libraries

Backend:

Django

Django REST Framework

MongoDB with Djongo or PyMongo

Requests

Pytest

Frontend:

React

Tailwind CSS

Shadcn/ui

DaisyUI

Axios

React Router

AI Integration:

Google Gemini Pro API

FLUX.1-dev API

Testing:

pytest

for Python

Jest

and React Testing Library

for JavaScript

Docker**:

Docker Engine

Docker Compose

---

By adhering to this development plan, the ARCANE application will be well-positioned to offer an innovative and comprehensive tool for D&D enthusiasts, combining manual and AI-assisted content generation, encounter creation, campaign management, and fantasy map integration within a user-friendly platform.

---