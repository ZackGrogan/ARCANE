# ARCANE (AI-Driven RPG Campaign Assistant & Narrative Engine)

## Version

Current Version: `v0.1.0-ALPHA`

## Overview

ARCANE is a full-stack application designed to assist Dungeon Masters (DMs) and players in creating and managing detailed campaigns for Dungeons & Dragons 5th Edition (D&D 5e). The application leverages AI to generate and manage Non-Player Characters (NPCs), characters, encounters, and integrates with the D&D 5e API for comprehensive data access.

## Update Map - Phase 1

### v0.1.0-ALPHA
**NPC and Character Creator: Manual Creation**
- Implement Manual Input Forms
  - Create forms for users to manually input detailed attributes for NPCs and characters:
    - Name
    - Race
    - Class
    - Background
    - Alignment
    - Personality Traits
    - Backstory
    - Appearance
    - Skills
    - Equipment

**Data Storage Setup**
- Initialize MongoDB Collections
  - Set up separate collections for NPCs and characters.
  - Define schemas according to the design document.

**Basic Frontend Development**
- Set Up Next.js Project
  - Initialize a Next.js application.
  - Configure TypeScript support.
- Implement Basic UI with Tailwind CSS
  - Design simple, responsive forms for data input.
  - Ensure accessibility and basic styling.

### v0.2.0-ALPHA
**Individual Pages for NPCs and Characters**
- Develop Profile Pages
  - Create individual pages displaying all attributes of NPCs and characters.
  - Include editable fields and sections:
    - Profile Picture Placeholder
    - Backstory
    - Personality Traits
    - Appearance Details
    - Equipment List

**CRUD Operations**
- Implement Update and Delete Functionality
  - Allow users to edit existing entries.
  - Enable deletion of NPCs and characters.

**Enhance Data Models**
- Refine MongoDB Schemas
  - Add necessary fields and validations.
  - Ensure data integrity and consistency.

### v0.3.0-ALPHA
**AI-Generated Creation for NPCs and Characters**
- Integrate AI Services (Placeholder)
  - Set up architecture for AI integration.
  - Implement functions to:
    - Generate names
    - Assign races and classes
    - Create backstories and personality traits
    - Describe appearance

**User Interface for AI Generation**
- Add AI Generation Options in Forms
  - Provide buttons or toggles to generate attributes using AI.
  - Allow users to input prompts for AI generation.

### v0.4.0-BETA
**Profile Picture Generation**
- Integrate FLUX.1-dev via Hugging Face API
  - Set up API calls to generate images based on text descriptions.
  - Implement prompt engineering for quality outputs.

**User Options for Images**
- Enable Manual Descriptions and Uploads
  - Allow users to input custom descriptions for image generation.
  - Provide the option to upload their own images.
  - Facilitate editing of AI-generated descriptions.

### v0.5.0-BETA
**Random Encounters Generator**
- Develop AI-Generated Encounters
  - Implement features to generate:
    - Encounter Titles
    - Descriptions
    - Monster Selection with Tactics
    - Biome and Environmental Details
    - Weather Conditions and Hazards
    - Loot Suggestions
    - Roleplaying Scenarios
    - Difficulty Ratings

**Encounters Storage and Management**
- Set Up Encounters Collection in MongoDB
  - Define schema for encounters as per the design document.
  - Implement saving and retrieval mechanisms.

### v0.6.0-BETA
**Manual Encounter Creation**
- Create Customizable Encounter Forms
  - Allow users to manually create and modify encounters.
  - Include options to select and customize:
    - Monsters
    - Environmental Factors
    - Loot Items
    - Tactics and Scenarios

**Monster Stat Lookup Integration**
- Integrate D&D 5e API for Monsters
  - Implement calls to /api/monsters endpoint.
  - Display full monster stats within the application.

### v0.7.0-BETA
**Data Storage and Campaign Management**
- Implement Unified Folder Structure
  - Organize all campaign-related data into a single folder per campaign.
  - Facilitate easy saving, loading, and sharing.

**Campaign Management Interface**
- Develop Dashboard for Campaigns
  - Provide tools to manage NPCs, characters, and encounters.
  - Enable organization of elements according to campaign arcs or sessions.

### v0.8.0-BETA
**Advanced D&D 5e API Integration**
- Integrate Additional Endpoints
  - Ability Scores
  - Alignments
  - Backgrounds
  - Classes
  - Races
  - Proficiencies
  - Spells
  - Equipment
  - Feats, Traits, Features
  - Magic Items
  - Skills

**Functionality Enhancement**
- Utilize API Data in Creation Processes
  - Ensure accurate and rule-compliant data for character and encounter creation.
  - Update forms and AI generation to incorporate API data.

### v0.9.0-BETA
**Technical and UI Improvements**
- Database Schema Refinement
  - Update schemas with any new requirements.
  - Include indexing for better performance.

**User Interface Enhancements**
- Improve UI/UX using Shadcn/ui and DaisyUI components.
  - Implement responsive design and accessibility features.

**Search and Filter Functionality**
- Implement Global Search Bar
  - Enable quick searching of NPCs, characters, and encounters.
- Develop Advanced Filters
  - Allow filtering based on attributes (e.g., alignment, class, race).

### v0.10.0-RELEASE CANDIDATE
**AI Integration with Google Gemini Pro API**
- Implement Advanced AI Features
  - Enable AI-driven NPC interactions.
  - Integrate content generation for backstories and scenarios.
  - Set up real-time chat responses with persistent history.

**Enhanced AI Services**
- Develop Prompt Engineering Pipeline
  - Standardize prompts for consistent AI outputs.
  - Apply quality modifiers and style guidelines.

### v0.11.0-RELEASE CANDIDATE
**Containerization and Deployment**
- Set Up Docker Containers
  - Frontend (Next.js)
  - Backend API
  - MongoDB
  - Redis
  - Nginx Reverse Proxy
  - AI Services
- Configure Docker Compose
  - Create development and production configurations.
  - Implement environment variables and health checks.

**Deployment and DevOps**
- Prepare Self-Hosted Deployment
  - Ensure all services run smoothly in a containerized environment.
  - Set up monitoring and logging solutions.

### v0.12.0-RELEASE CANDIDATE
**Authentication and Security**
- Implement Auth.js for Authentication
  - Set up secure user authentication flows.
  - Include session management and multiple provider support.

**Performance Optimization**
- Optimize Performance
  - Implement caching with Redis.
  - Optimize database queries and API calls.
  - Use lazy loading and code splitting on the frontend.

### v1.0.0-STABLE
**Final Testing and Bug Fixes**
- Conduct Comprehensive Testing
  - Perform unit, integration, and E2E tests.
  - Fix bugs and polish features.

**Documentation Completion**
- Finalize Documentation
  - User Guides
  - API Documentation
  - Developer Contribution Guidelines

**Deployment**
- Launch ARCANE v1.0.0-STABLE
  - Deploy the application to the production environment.
  - Monitor for any post-deployment issues.

## Getting Started

### Prerequisites
- Node.js (v16 or higher)
- pnpm package manager
- MongoDB database

### Installation
1. Clone the repository:
```bash
git clone https://github.com/yourusername/ARCANE.git
cd ARCANE
```

2. Install dependencies:
```bash
pnpm install
```

3. Set up environment variables:
Create a `.env.local` file in the root directory with the following content:
```
MONGODB_URI=your_mongodb_connection_string
```

4. Run the development server:
```bash
pnpm dev
```

The application will be available at `http://localhost:3000`.

### Testing
Run the test suite using:
```bash
pnpm test
```

## API Documentation

### NPC Endpoints

#### Create NPC
- **POST** `/api/npcs/create`
- **Body:**
```json
{
  "name": "string",
  "race": "string",
  "class": "string",
  "background": "string",
  "alignment": "string",
  "personalityTraits": "string",
  "backstory": "string",
  "appearance": "string",
  "skills": ["string"],
  "equipment": ["string"]
}
```
- **Response:** Returns the created NPC object with MongoDB _id

#### Get All NPCs
- **GET** `/api/npcs`
- **Response:** Returns an array of all NPCs

## Contributing

Contributions are welcome! Please see `CONTRIBUTING.md` for more information on how to contribute to the project.

## License

This project is licensed under the MIT License - see the `LICENSE.md` file for details.
