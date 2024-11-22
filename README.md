# Arcane Project

## Setup Instructions

### Backend Setup
1. Ensure Python 3.10 or above is installed.
2. Navigate to the `backend` directory.
3. Create a virtual environment: `python -m venv venv`
4. Activate the virtual environment: `source venv/bin/activate` (Linux/Mac) or `venv\Scripts\activate` (Windows)
5. Install dependencies: `pip install -r requirements.txt`

### Frontend Setup
1. Ensure Node.js v18 and npm are installed.
2. Navigate to the `frontend` directory.
3. Install dependencies: `npm install`

### Running the Project
- **Backend**: `python manage.py runserver`
- **Frontend**: `npm start`

## Contribution Guidelines
- Fork the repository and create a new branch for your feature or bug fix.
- Ensure code quality by running linting and tests before committing.
- Submit a pull request for review.

## Testing
- **Backend**: Run tests using `pytest`.
- **Frontend**: Run tests using `npm test`.

## Environment Variables
- Use the `.env` file to manage environment variables.

## Code Quality
- **Backend**: Use `flake8` and `black` for linting and formatting.
- **Frontend**: Use `eslint` and `prettier` for linting and formatting.

## Documentation
- API documentation is generated using Swagger or ReDoc.
