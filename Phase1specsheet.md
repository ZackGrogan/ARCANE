# ARCANE (AI-Driven RPG Campaign Assistant & Narrative Engine)

# Development Checklist

## v0.1.0-ALPHA (✅ COMPLETED)
### NPC and Character Creator: Manual Creation
- [x] **Set Up Project Environment**
  - [x] Initialize a Next.js project with TypeScript support
  - [x] Install and configure Tailwind CSS for styling
- [x] **Implement Manual Input Forms**
  - [x] Create forms for users to input NPC attributes:
    - [x] Name
    - [x] Race
    - [x] Class
    - [x] Background
    - [x] Alignment
    - [x] Personality Traits
    - [x] Backstory
    - [x] Appearance
    - [x] Skills
    - [x] Equipment
- [x] **Set Up MongoDB Database**
  - [x] Install MongoDB and set up a local development database
  - [x] Define schemas for NPCs based on the design document
  - [x] Implement Mongoose for schema management
  - [x] Create collections for NPCs
- [x] **Implement Basic CRUD Operations**
  - [x] **Create**
    - [x] Save new NPCs to the database
  - [x] **Read**
    - [x] Fetch and display a list of NPCs
- [x] **Basic Frontend Development**
  - [x] Design a simple and responsive UI for the input forms
  - [x] Ensure accessibility standards are met
  - [x] Implement client-side validation for form inputs
- [x] **Testing and Documentation**
  - [x] Write unit tests for API endpoints
  - [x] Write integration tests for components
  - [x] Create API documentation (OpenAPI/Swagger)
  - [x] Update README with setup instructions
- [x] **Deployment Setup**
  - [x] Configure Vercel deployment
  - [x] Set up environment variables
  - [x] Initialize Git repository

## v0.2.0-ALPHA (🔄 IN PROGRESS)
### Individual Pages for NPCs and Characters
- [x] **Develop Profile Pages**
  - [x] Create a dynamic route for individual NPC and character pages
  - [x] Display all attributes on the profile page
  - [x] Include sections for:
    - [x] Basic Information (name, race, class)
    - [x] Backstory (with rich text editing)
    - [x] Personality Traits (with rich text editing)
    - [x] Appearance (with rich text editing)
    - [x] Skills (with add/remove functionality)
    - [x] Equipment (with add/remove functionality)
- [x] **Enhance Editing Capabilities**
  - [x] Allow inline editing of attributes on the profile page
  - [x] Implement rich-text editors for backstory and appearance
- [x] **Improve Data Models**
  - [x] Refine MongoDB schemas to include any additional fields
  - [x] Add data validation and sanitization

## v0.3.0-ALPHA
### AI-Generated Creation for NPCs and Characters
- [ ] **Integrate AI Placeholder Services**
  - [ ] Set up a basic AI service (mock or simple algorithm) for generating:
    - [ ] Names
    - [ ] Races
    - [ ] Classes
    - [ ] Backstories
    - [ ] Personality Traits
    - [ ] Appearances
- [ ] **Update Creation Forms**
  - [ ] Add options/buttons to generate attributes using AI
  - [ ] Allow users to provide prompts for AI generation
  - [ ] Handle AI responses and populate form fields accordingly
- [ ] **Prepare for Future AI Integration**
  - [ ] Design the system to easily integrate with more advanced AI models later

## v0.4.0-BETA
### Profile Picture Generation
- [ ] **Integrate Hugging Face API with FLUX Model**
  - [ ] Set up an account with Hugging Face and obtain API keys
  - [ ] Implement API calls to generate images based on text descriptions
  - [ ] Handle authentication and error checking for API calls
- [ ] **Implement Prompt Engineering Pipeline**
  - [ ] Develop functions to construct prompts with quality modifiers
  - [ ] Implement negative prompts to avoid undesired outputs
- [ ] **Enhance Profile Pages**
  - [ ] Enable users to:
    - [ ] Manually input descriptions for image generation
    - [ ] Edit AI-generated descriptions
    - [ ] Upload custom images
- [ ] **Display Generated Images**
  - [ ] Update the UI to display profile pictures
  - [ ] Handle image storage and retrieval securely

## v0.5.0-BETA
### Random Encounters Generator
- [ ] **Develop Encounter Generation Feature**
  - [ ] Implement AI functions to generate encounter components:
    - [ ] Titles
    - [ ] Descriptions
    - [ ] Monsters with tactics
    - [ ] Biome and environment
    - [ ] Weather conditions
    - [ ] Environmental hazards
    - [ ] Loot suggestions
    - [ ] Roleplaying scenarios
    - [ ] Difficulty ratings

---

# Design Specification Document

## Overview

ARCANE is a full-stack application designed to assist Dungeon Masters (DMs) and players in creating and managing detailed campaigns for Dungeons & Dragons 5th Edition (D&D 5e). The application leverages AI to generate and manage Non-Player Characters (NPCs), characters, encounters, and integrates with the D&D 5e API for comprehensive data access.

## Table of Contents

1. NPC and Character Creator
2. Random Encounters Generator
3. Data Storage and Campaign Management
4. D&D 5e API Integration
5. Technical and UI Details
6. Future Enhancements
7. Technical Stack

## NPC and Character Creator

### Manual Creation

#### Attributes Input:
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

Users can manually input detailed attributes for both NPCs and characters, allowing full customization to fit their campaign needs.

### AI-Generated Creation

#### AI-Powered Generation:
- Generates Name
- Race
- Class
- Backstory
- Personality Traits
- and Appearance
- based on a user prompt
- Ensures generated content adheres to D&D 5e rules and lore

### Storage and Individual Pages

#### Separate Databases:
- NPC Collection:
  - Stores NPC-specific attributes (Bio, Personality, Backstory, Appearance, Roleplaying Traits)
- Character Collection:
  - Stores character-specific attributes (Class, Race, Skills, Equipment, Personality)

#### Individual Pages:
- Each NPC and character has an editable profile page featuring:
  - Profile Picture
  - Backstory
  - Personality Traits
  - Appearance Details
  - Equipment List
  - AI-Generated Content
- Persistent AI Chat:
  - Integrated chat functionality for roleplaying interactions
  - Conversation history is stored and accessible for continuous storytelling

### Profile Picture Generation

#### FLUX.1-dev Integration:
- AI-generated profile pictures based on text descriptions
- Options for users to:
  - Manually input descriptions for image generation
  - Upload custom images
  - Edit AI-generated descriptions for precise image outputs

## Random Encounters Generator

### AI-Generated Encounters

#### AI-Driven Components:
- Title:
  - Creative encounter names (e.g., "Ambush in the Mist")
- Description:
  - Vivid narratives setting the scene
- Monsters:
  - Selection from D&D 5e API with tactical behaviors
- Biome/Environment:
  - Environmental context (forest, cavern, etc.)
- Weather and Hazards:
  - Dynamic conditions affecting gameplay
- Loot:
  - Suggested rewards
- Roleplaying Scenarios:
  - Potential story developments
- Encounter Difficulty:
  - Rated as easy, medium, hard, or deadly

### Manual Encounter Creation

#### Customizable Options:
- Users can select and modify:
  - Monsters
  - Weather Conditions
  - Loot Items
  - Tactics
  - Roleplaying Scenarios
- Allows DMs to tailor encounters to their specific campaign requirements

### Monster Stat Lookup

#### D&D 5e API Integration:
- Access to full monster stats
- Quick reference during encounter planning and gameplay

### Scaling Encounter Difficulty

#### Difficulty Adjustments:
- Modify:
  - Number of Monsters
  - Challenge Rating (CR)
  - Monster Stats
  - Environmental Factors
- Real-time difficulty recalculations

### Save Encounters

#### Encounter Storage:
- Encounters saved with unique IDs
- Tagging system for categorization
- Search and Filter functionality
- Edit and update capabilities

## Data Storage and Campaign Management

### File Organization

#### Unified Folder Structure:
- All campaign-related files in a single folder
- Simplifies saving, loading, and sharing
- Facilitates future enhancements

### MongoDB Storage

#### Database Collections:
- NPCs Collection
- Characters Collection
- Encounters Collection
- Detailed documents for efficient retrieval

### Campaign Management Interface

#### User-Friendly Tools:
- Dashboard for managing campaigns
- Add or remove components
- Organize by campaign arcs or sessions

## D&D 5e API Integration

### Integrated Endpoints:
- Monsters
- Ability Scores
- Alignments
- Backgrounds
- Classes
- Races
- Proficiencies
- Spells
- Equipment
- Magic Items
- Skills

## Technical Stack

### Frontend
- Next.js 14
- TypeScript
- Tailwind CSS
- Shadcn/ui
- DaisyUI

### Backend
- Node.js
- MongoDB
- Mongoose ORM

### AI Integration
- Google Gemini Pro API
- FLUX.1-dev (Hugging Face)

### Testing
- Jest
- React Testing Library
- Cypress

### Deployment
- Vercel
- MongoDB Atlas

## Future Enhancements

### Planned Features
- Campaign Export/Import
- Advanced AI Integration
- Enhanced Search Capabilities
- Mobile App Development
- Collaborative Campaign Management
