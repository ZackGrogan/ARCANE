"""Custom JSON encoder for MongoDB objects.

This module provides a custom JSON encoder that extends the standard
JSON encoder to handle MongoDB-specific data types, particularly the
ObjectId type which is not natively JSON-serializable.

Classes:
    MongoJSONEncoder: Custom JSON encoder for MongoDB objects
"""

from bson import ObjectId
import json

class MongoJSONEncoder(json.JSONEncoder):
    """Custom JSON encoder that handles MongoDB-specific data types.

    This class extends the standard JSON encoder to properly serialize
    MongoDB ObjectId instances by converting them to strings. This is
    necessary because ObjectId is not natively JSON-serializable.

    Example:
        app.json_encoder = MongoJSONEncoder
        # Now JSON responses will properly handle ObjectId
    """

    def default(self, obj):
        """Convert MongoDB objects to JSON-serializable types.

        Args:
            obj: Object to serialize

        Returns:
            str: String representation of ObjectId if obj is ObjectId,
                 otherwise delegates to parent class

        Example:
            encoder = MongoJSONEncoder()
            json_str = encoder.encode({'_id': ObjectId()})
            # Results in: {"_id": "..."}
        """
        if isinstance(obj, ObjectId):
            return str(obj)
        return super().default(obj)
