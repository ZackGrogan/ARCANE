# Development Checklist

## Overview
This checklist outlines the development roadmap for the ARCANE project, incorporating the necessary changes from the old system to the new Python-centric stack. Features that have been previously completed but need to be remade are marked with a -. The version numbers and order have been adjusted to reflect a chronological development process that makes sense for the project's evolution.

## Table of Contents

## v0.1.0-ALPHA - Project Restructuring
### Environment Setup v0.1.1-ALPHA
- [x] Update Development Environment
- [x] Remove Node.js and npm dependencies
- [x] Uninstall React and TypeScript packages
- [x] Ensure Python 3.10 or above is installed
- [x] Update virtual environment
- [x] Install Flask and required packages
- [ ] Install frontend dependencies (Bootstrap 5)
- [x] Update requirements.txt

### Project Structure Adjustment v0.1.2-ALPHA
- [x] Adjust Project Structure
- [x] Remove frontend directory related to React
- [x] Organize templates/ and static/ directories for Flask
- [x] Update .gitignore to exclude obsolete files
- [x] Update README.md with new setup instructions
- [x] Ensure all team members are aware of the new structure

## v0.2.0-ALPHA - Backend Conversion to Flask
### Flask App Setup v0.2.1-ALPHA
- [x] Create app.py as the main entry point for the Flask application
- [x] Configure config.py with necessary settings
- [x] Initialize the Flask app instance and any required extensions
- [x] Set up Flask Blueprints for modularizing application components
- [x] Update the Dockerfile to reflect the Flask application setup

### Data Model Conversion v0.2.2-ALPHA
- [x] Rewrite existing Django models as Python classes using PyMongo
- [x] Convert the NPC model
- [x] Convert the Encounter model
- [x] Convert the Campaign model
- [x] Update all database interactions to use PyMongo

### API Endpoint Restructuring v0.2.3-ALPHA
- [x] Rewrite API endpoints using Flask routes and functions
- [x] Update CRUD operations for NPCs
- [x] Update CRUD operations for Encounters
- [x] Update CRUD operations for Campaigns
- [x] Adjust URL routes and handlers to align with Flask's routing conventions
- [x] Implement proper error handling and responses for all API endpoints

## v0.3.0-ALPHA - Frontend Migration to Flask Templates
### Template Implementation v0.3.1-ALPHA
- [x] Create base.html template with common layout components
- [x] Develop Jinja2 templates for various pages (npcs/list.html, npcs/create.html, npcs/view.html)
- [x] Develop Jinja2 templates for encounters and campaigns
- [x] Utilize Jinja2 features for dynamic content rendering

### Form Handling with Flask-WTF v0.3.2-ALPHA
- [x] Set up Flask-WTF for form handling and validation
- [x] Create WTF forms for NPC creation and editing
- [x] Create WTF forms for Encounter creation and editing
- [x] Create WTF forms for Campaign management
- [x] Ensure server-side validation of form data and display appropriate error messages

### Static Files and Asset Management v0.3.3-ALPHA
- [x] Organize CSS, JavaScript, and image files within the static/ directory
- [x] Integrate Bootstrap 5 using CDN
- [x] Ensure static files are properly linked in the templates
- [ ] Optimize asset loading for performance

## v0.4.0-BETA - Map Generation Feature Development
### Procedural Map Generation Logic v0.4.1-BETA
- [x] Implement procedural map generation logic using Perlin noise.
- [x] Use Pillow library for image creation and manipulation.
- [x] Classify terrain types based on height values.
- [x] Assign distinct colors to different terrain types.

### Map Visualization and Interaction v0.4.2-BETA
- [x] Integrate map generation into the Flask frontend.
- [x] Create Flask routes for map generation and display.
- [x] Develop a Jinja2 template for map generation and display.
- [x] Enable user interaction for map parameter adjustments.
- [x] Implement map downloading functionality.
- [x] Save generated maps to the database.
- [x] Use dynamic filenames for generated maps.
- [x] Add input validation for map generation parameters.

## v0.5.0-BETA - AI Services Integration
### AI Service Implementation v0.5.1-BETA
- [ ] Integrate AI Services
- [ ] Update AI service clients for Flask backend
- [ ] Implement abstract base classes for AI services
- [ ] Securely handle API keys and configurations

### Google Gemini Pro Integration v0.5.2-BETA
- [ ] Implement Gemini Pro Client
- [ ] Set up API calls for name and backstory generation
- [ ] Handle API responses and errors gracefully
- [ ] Integrate with NPC creation forms and workflows

### FLUX Integration v0.5.3-BETA
- [ ] Implement FLUX Client
- [ ] Set up API calls for profile picture generation
- [ ] Integrate image generation into NPC profiles
- [ ] Ensure compliance with FLUX API terms of use

## v0.6.0-BETA - Feature Enhancements and UI Improvements
### Advanced Features Remake v0.6.1-BETA
- [ ] Reimplement Advanced Functionalities
- [ ] Update and enhance campaign management features
- [ ] Improve encounter generation tools
- [ ] Integrate AI-assisted content creation throughout the application

### UI Enhancements with Bootstrap v0.6.2-BETA
- [ ] Enhance User Interface
- [ ] Refine layouts and navigation menus
- [ ] Implement responsive design practices
- [ ] Utilize Bootstrap components for better UX
- [ ] Ensure visual consistency across all templates

## v0.7.0-BETA - Testing and Quality Assurance
### Backend Testing v0.7.1-BETA
- [ ] Update and Expand Backend Tests
- [ ] Write unit tests for Flask models and utilities
- [ ] Test all Flask routes and API endpoints
- [ ] Implement integration tests where appropriate

### Frontend Testing v0.7.2-BETA
- [ ] Implement Frontend Testing
- [ ] Use tools like Flask-Testing or Selenium for E2E tests
- [ ] Test form validation, submission, and user flows
- [ ] Verify template rendering and static file serving

## v0.8.0-BETA - Security Enhancements
### Authentication and Authorization v0.8.1-BETA
- [ ] Implement User Authentication
- [ ] Use Flask-Login for session management
- [ ] Create user registration and login functionalities
- [ ] Protect routes with login requirements
- [ ] Implement role-based access control if needed

### Input Validation and Sanitization v0.8.2-BETA
- [ ] Ensure Input Security
- [ ] Validate all user inputs on server-side
- [ ] Sanitize inputs to prevent XSS and injection attacks
- [ ] Implement CSRF protection using Flask-WTF

## v0.9.0-BETA - Optimization and Performance
### Database Indexing and Query Optimization v0.9.1-BETA
- [ ] Optimize Database Performance
- [ ] Analyze and optimize MongoDB queries
- [ ] Add indexes to improve query efficiency
- [ ] Refactor data models if necessary

### Caching Implementation v0.9.2-BETA
- [ ] Implement Caching Strategies
- [ ] Use Flask-Caching for data caching
- [ ] Determine and configure appropriate cache backends
- [ ] Test caching to ensure it improves performance

## v1.0.0-RELEASE - Deployment and Documentation
### Deployment Setup v1.0.1-RELEASE
- [ ] Prepare for Production Deployment
- [ ] Update Docker configurations for production
- [ ] Set up environment variables and secrets securely
- [ ] Configure a production-ready WSGI server (e.g., Gunicorn)

### Comprehensive Documentation v1.0.2-RELEASE
- [ ] Finalize Documentation
- [ ] Update README.md with installation and usage instructions
- [ ] Document API endpoints and data models
- [ ] Provide deployment and maintenance guides

### Final Testing and Launch v1.0.3-RELEASE
- [ ] Conduct Final Testing
- [ ] Perform thorough QA testing across all features
- [ ] Address any remaining bugs or issues
- [ ] Launch the application and monitor for any post-launch issues

## Notes and Future Considerations
### Scalability
- [ ] Plan for application scalability
- [ ] Consider using load balancers
- [ ] Evaluate database sharding or replication

### Internationalization
- [ ] Implement support for multiple languages
- [ ] Prepare templates and content for localization
- [ ] Use appropriate libraries for translation

### Accessibility
- [ ] Ensure compliance with accessibility standards
- [ ] Use semantic HTML elements
- [ ] Provide ARIA labels where necessary
- [ ] Test with screen readers and keyboard navigation

### Push to GitHub
- [ ] Update Version Control
- [ ] Commit all changes to the Git repository
- [ ] Push updates regularly to GitHub
- [ ] Use tags and releases for versioning
- [ ] Update issue tracker and project boards as needed