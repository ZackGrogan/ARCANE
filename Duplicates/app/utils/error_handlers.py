from functools import wraps
from flask import jsonify
from bson.errors import InvalidId

def handle_exceptions(f):
    """Decorator to handle common exceptions in routes."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        except InvalidId:
            return jsonify({'error': 'Invalid ID format'}), 400
        except Exception as e:
            return jsonify({'error': f'An unexpected error occurred: {str(e)}'}), 500
    return decorated_function
