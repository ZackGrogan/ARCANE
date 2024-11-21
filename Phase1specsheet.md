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
- [x] **Integrate AI Placeholder Services**
  - [x] Set up a basic AI service (mock or simple algorithm) for generating:
    - [x] Names (with race-specific patterns)
    - [x] Races (integrated with D&D 5e data)
    - [x] Classes (integrated with D&D 5e data)
    - [x] Backstories (template-based generation)
    - [x] Personality Traits (comprehensive trait system)
    - [x] Appearances (detailed physical descriptions)
- [x] **Update Creation Forms**
  - [x] Add options/buttons to generate attributes using AI
  - [x] Allow users to provide prompts for AI generation
  - [x] Handle AI responses and populate form fields accordingly
- [x] **Prepare for Future AI Integration**
  - [x] Design the system to easily integrate with more advanced AI models later
  - [x] Create modular generator services
  - [x] Implement interfaces for AI content generation

## v0.4.0-BETA
### Profile Picture Generation
- [x] **Implement Local Storage Solution**
  - [x] Create local storage service for handling images
  - [x] Remove AWS S3 dependencies
  - [x] Update API endpoints to use local storage
  - [x] Add image upload endpoint
  - [x] Update tests for local storage
- [x] **Integrate Hugging Face API with FLUX Model**
  - [x] Set up an account with Hugging Face and obtain API keys
  - [x] Implement API calls to generate images based on text descriptions
  - [x] Handle authentication and error checking for API calls
- [x] **Implement Prompt Engineering Pipeline**
  - [x] Develop functions to construct prompts with quality modifiers
  - [x] Implement negative prompts to avoid undesired outputs
- [x] **Enhance Profile Pages**
  - [x] Enable users to:
    - [x] Manually input descriptions for image generation
    - [x] Edit AI-generated descriptions
    - [x] Upload custom images
- [x] **Display Generated Images**
  - [x] Update the UI to display profile pictures
  - [x] Handle image storage and retrieval securely

## v0.5.0-BETA
### Random Encounters Generator
- [x] **Develop Encounter Generation Feature**
  - [x] Implement AI functions to generate encounter components:
    - [x] Titles
    - [x] Descriptions
    - [x] Monsters with tactics
    - [x] Biome and environment
    - [x] Weather conditions
    - [x] Environmental hazards
    - [x] Loot suggestions
    - [x] Roleplaying scenarios
    - [x] Difficulty ratings

## v0.6.0-BETA
### Campaign Management
- [ ] **Campaign Organization**
  - [ ] Create campaign dashboard
  - [ ] Implement campaign creation and editing
  - [ ] Add session management
  - [ ] Enable NPC and encounter organization within campaigns
- [ ] **Campaign Timeline**
  - [ ] Develop timeline visualization
  - [ ] Add event creation and management
  - [ ] Enable drag-and-drop organization
- [ ] **Notes System**
  - [ ] Implement rich text campaign notes
  - [ ] Add tagging and categorization
  - [ ] Enable linking to NPCs and encounters

## v0.7.0-BETA
### Combat Tracker
- [ ] **Initiative Tracking**
  - [ ] Create initiative order management
  - [ ] Add automatic initiative rolling
  - [ ] Enable manual initiative adjustment
- [ ] **Combat Management**
  - [ ] Implement HP tracking
  - [ ] Add status effect management
  - [ ] Create turn order automation
- [ ] **Combat Calculations**
  - [ ] Add damage calculation
  - [ ] Implement saving throws
  - [ ] Create critical hit handling

## v0.8.0-BETA
### Maps and Locations
- [ ] **Map Management**
  - [ ] Enable map uploads
  - [ ] Add map annotation tools
  - [ ] Implement fog of war
- [ ] **Location Database**
  - [ ] Create location profiles
  - [ ] Add AI-generated location descriptions
  - [ ] Enable linking NPCs to locations
- [ ] **Interactive Features**
  - [ ] Add distance measurement
  - [ ] Implement token placement
  - [ ] Create dynamic lighting

## v0.9.0-BETA
### Quest Management
- [ ] **Quest System**
  - [ ] Implement quest creation and tracking
  - [ ] Add quest objectives and milestones
  - [ ] Enable quest rewards management
- [ ] **AI Quest Generation**
  - [ ] Create quest premise generation
  - [ ] Add branching narrative options
  - [ ] Implement dynamic quest adaptation
- [ ] **Quest Integration**
  - [ ] Link quests to NPCs and locations
  - [ ] Add quest progress tracking
  - [ ] Enable quest-related note taking

## v0.10.0-BETA
### Inventory and Items
- [ ] **Item Management**
  - [ ] Create item database
  - [ ] Implement inventory tracking
  - [ ] Add item categorization
- [ ] **Magic Item Generation**
  - [ ] Add AI-generated magic items
  - [ ] Implement item history generation
  - [ ] Create custom item properties
- [ ] **Economy System**
  - [ ] Add currency tracking
  - [ ] Implement shop generation
  - [ ] Create price calculation

## v0.11.0-BETA
### Player Tools
- [ ] **Character Sheets**
  - [ ] Create digital character sheets
  - [ ] Add automatic calculations
  - [ ] Enable spell management
- [ ] **Player Dashboard**
  - [ ] Implement session scheduling
  - [ ] Add character progression tracking
  - [ ] Create player notes system
- [ ] **Collaboration Features**
  - [ ] Add real-time chat
  - [ ] Enable file sharing
  - [ ] Implement shared calendars

## v0.12.0-BETA
### Polish and Optimization
- [ ] **Performance Optimization**
  - [ ] Implement caching
  - [ ] Add lazy loading
  - [ ] Optimize database queries
- [ ] **UI/UX Improvements**
  - [ ] Add animations and transitions
  - [ ] Implement dark mode
  - [ ] Create responsive layouts
- [ ] **Quality of Life**
  - [ ] Add keyboard shortcuts
  - [ ] Implement undo/redo
  - [ ] Create data backup system

## v1.0.0-RELEASE
### Final Release Preparation
- [ ] **Testing and Validation**
  - [ ] Conduct comprehensive testing
  - [ ] Fix all critical bugs
  - [ ] Perform security audit
- [ ] **Documentation**
  - [ ] Complete user documentation
  - [ ] Create API documentation
  - [ ] Add tutorial videos
- [ ] **Deployment**
  - [ ] Set up production environment
  - [ ] Configure monitoring
  - [ ] Implement analytics

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
