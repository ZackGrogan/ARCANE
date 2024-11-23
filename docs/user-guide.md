# ARCANE User Guide

## Introduction
ARCANE is a comprehensive D&D campaign management tool that helps Dungeon Masters create and manage NPCs, encounters, and campaigns with AI assistance.

## Features

### 1. NPC Management
- Create NPCs with AI-generated backstories and descriptions
- Generate profile pictures using FLUX AI
- View and edit NPC details
- Delete NPCs when no longer needed
- List all NPCs in your campaign

### 2. Encounter Management
- Create combat encounters with specified difficulty levels
- Add monsters from the D&D 5e bestiary
- Track encounter environment and party level
- Add custom notes and descriptions
- Remove or modify monsters in encounters

### 3. Campaign Management
- Create and organize campaigns
- Add NPCs and encounters to campaigns
- Track campaign progress and notes
- Manage multiple campaigns simultaneously

### 4. Map Generation
- Generate procedural fantasy maps
- Customize terrain and features
- Download and save generated maps
- Adjust map parameters for different environments

## Getting Started

### Installation
1. Ensure Python 3.10 or above is installed
2. Clone the ARCANE repository
3. Install dependencies: `pip install -r requirements.txt`
4. Set up environment variables (see Configuration section)
5. Run the application: `python main.py`

### Configuration
Required environment variables:
- `MONGODB_URI`: MongoDB connection string
- `GEMINI_API_KEY`: Google Gemini API key for AI content generation
- `FLUX_API_KEY`: FLUX API key for image generation

### Basic Usage

#### Creating an NPC
1. Navigate to the NPCs section
2. Click "Create New NPC"
3. Fill in basic details or use AI generation
4. Click "Generate Profile Picture" for an AI-generated image
5. Save the NPC

#### Creating an Encounter
1. Go to the Encounters section
2. Click "Create New Encounter"
3. Set environment, party level, and difficulty
4. Add monsters from the D&D bestiary
5. Save the encounter

#### Managing Campaigns
1. Access the Campaigns section
2. Create a new campaign
3. Add NPCs and encounters
4. Track progress and notes
5. Update as needed

## Troubleshooting

### Common Issues
1. **API Connection Errors**
   - Check internet connection
   - Verify API keys are correctly set
   - Ensure environment variables are properly configured

2. **Image Generation Issues**
   - Check FLUX API key validity
   - Ensure proper network connectivity
   - Try regenerating the image

3. **Database Connection Issues**
   - Verify MongoDB connection string
   - Check MongoDB service status
   - Ensure proper network access

### Support
For additional support or to report issues:
1. Check the GitHub repository issues section
2. Contact the development team
3. Review the documentation for updates

## Best Practices
1. Regularly backup campaign data
2. Use meaningful names for NPCs and encounters
3. Add detailed descriptions for better organization
4. Keep track of important campaign events
5. Update NPC and encounter details as campaigns progress
