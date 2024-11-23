"""Error handling utilities for the ARCANE backend.

This module provides error handling utilities for the ARCANE backend,
including custom exceptions and decorators for consistent error handling
across the API endpoints.

Classes:
    APIError: Base exception class for API-related errors

Functions:
    handle_api_error: Decorator for consistent API error handling
"""

from flask import current_app, jsonify
from functools import wraps
from bson.errors import InvalidId
from pymongo.errors import DuplicateKeyError

class APIError(Exception):
    """Base exception class for API-related errors.

    This class extends the built-in Exception class to provide structured
    error handling for API endpoints, including status codes and optional
    detailed error information.

    Attributes:
        message (str): Human-readable error message
        status_code (int): HTTP status code for the error
        details (Any, optional): Additional error details
    """

    def __init__(self, message: str, status_code: int = 400, details: any = None):
        """Initialize an API error.

        Args:
            message (str): Human-readable error message
            status_code (int, optional): HTTP status code. Defaults to 400.
            details (Any, optional): Additional error details. Defaults to None.
        """
        super().__init__()
        self.message = message
        self.status_code = status_code
        self.details = details

    def to_dict(self) -> dict:
        """Convert error to dictionary format.

        Returns:
            dict: Dictionary containing error message and optional details
        """
        error_dict = {'error': self.message}
        if self.details:
            error_dict['details'] = self.details
        return error_dict

def handle_api_error(func):
    """Decorator for consistent API error handling.

    This decorator wraps API endpoint functions to provide consistent
    error handling and response formatting. It catches various types
    of exceptions and converts them to appropriate HTTP responses.

    Args:
        func: The function to wrap

    Returns:
        function: Wrapped function with error handling

    Example:
        @handle_api_error
        def get_user(user_id):
            # Function implementation
            pass
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except InvalidId:
            return jsonify({'error': 'Invalid ID format'}), 400
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        except DuplicateKeyError:
            return jsonify({'error': 'Resource already exists'}), 409
        except APIError as e:
            return jsonify(e.to_dict()), e.status_code
        except Exception as e:
            current_app.logger.exception("Unexpected error occurred")
            return jsonify({
                'error': 'Internal server error',
                'details': str(e) if current_app.debug else None
            }), 500
    return wrapper
