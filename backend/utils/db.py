"""Database utility functions for MongoDB operations.

This module provides utility functions for MongoDB database operations,
including initialization and error handling. It ensures that required
collections exist and provides consistent error handling for database
operations.

Functions:
    init_db: Initialize required database collections
    handle_db_error: Decorator for database error handling
"""

from flask import current_app
from pymongo.errors import PyMongoError

def init_db():
    """Initialize required database collections.

    This function checks for the existence of required collections
    in the MongoDB database and creates them if they don't exist.
    The required collections are:
        - npcs: Stores NPC character data
        - campaigns: Stores campaign information
        - encounters: Stores encounter data

    Raises:
        PyMongoError: If database operations fail
    """
    db = current_app.mongo.db
    collections = db.list_collection_names()

    required_collections = ['npcs', 'campaigns', 'encounters']
    for collection in required_collections:
        if collection not in collections:
            db.create_collection(collection)

def handle_db_error(func):
    """Decorator for handling MongoDB database errors.

    This decorator wraps database operations to provide consistent
    error handling and logging. It catches PyMongo errors and returns
    appropriate error responses.

    Args:
        func: The function to wrap

    Returns:
        function: Wrapped function with error handling

    Example:
        @handle_db_error
        def save_user(user_data):
            # Database operation implementation
            pass
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except PyMongoError as e:
            current_app.logger.error(f"Database error in {func.__name__}: {str(e)}")
            return {'error': 'Database error occurred'}, 500
    return wrapper
