# Arcane Project

## Setup Instructions

### Backend Setup
1. Ensure Python 3.10 or above is installed.
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment: `source venv/bin/activate` (Linux/Mac) or `venv\Scripts\activate` (Windows)
4. Install dependencies: `pip install -r requirements.txt`

### Running the Project
- Start the Flask development server: `flask run`

## Development Tools Setup

### JavaScript
- **ESLint and Prettier**: Configure for any client-side JS in the `static/js` directory.

### Python
- **Flake8 and Black**: Use for linting and formatting Python code.

### Testing
- **Backend**: Set up `pytest` for backend testing.

## Environment Variables
- Use the `.env` file to manage environment variables.

## Contribution Guidelines
- Fork the repository and create a new branch for your feature or bug fix.
- Ensure code quality by running linting and tests before committing.
- Submit a pull request for review.
