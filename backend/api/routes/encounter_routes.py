"""Encounter routes for the API."""
from flask import Blueprint, jsonify, request, current_app
from bson import ObjectId
from backend.models.encounter import Encounter
from backend.utils.errors import handle_api_error, APIError

bp = Blueprint('encounter', __name__, url_prefix='/api/encounters')

@bp.before_request
def before_request():
    """Add mongo to request object."""
    request.mongo = current_app.mongo

@bp.route('/', methods=['POST'])
@handle_api_error
def create_encounter():
    """Create a new encounter."""
    data = request.get_json()
    encounter = Encounter(
        mongo=request.mongo,
        title=data['title'],
        environment=data['environment'],
        party_level=data['party_level'],
        difficulty=data['difficulty'],
        description=data.get('description', ''),
        monsters=data.get('monsters', []),
        traps=data.get('traps', []),
        notes=data.get('notes', '')
    )
    result = encounter.save()
    return jsonify(result), 201

@bp.route('/', methods=['GET'])
@handle_api_error
def get_encounters():
    """Get all encounters."""
    encounters = Encounter.list_encounters(request.mongo)
    return jsonify(encounters)

@bp.route('/<encounter_id>/', methods=['GET'])
@handle_api_error
def get_encounter(encounter_id):
    """Get a specific encounter."""
    try:
        _id = ObjectId(encounter_id)
    except Exception:
        raise APIError("Invalid encounter ID", 400)

    encounter = Encounter.get_encounter(request.mongo, _id)
    if not encounter:
        raise APIError("Encounter not found", 404)
    return jsonify(encounter.to_dict())

@bp.route('/<encounter_id>/', methods=['PUT'])
@handle_api_error
def update_encounter(encounter_id):
    """Update a specific encounter."""
    try:
        _id = ObjectId(encounter_id)
    except Exception:
        raise APIError("Invalid encounter ID", 400)

    data = request.get_json()
    encounter = Encounter.get_encounter(request.mongo, _id)
    if not encounter:
        raise APIError("Encounter not found", 404)

    # Update fields
    result = encounter.update(data)
    return jsonify(result)

@bp.route('/<encounter_id>/', methods=['DELETE'])
@handle_api_error
def delete_encounter(encounter_id):
    """Delete a specific encounter."""
    try:
        _id = ObjectId(encounter_id)
    except Exception:
        raise APIError("Invalid encounter ID", 400)

    encounter = Encounter.get_encounter(request.mongo, _id)
    if not encounter:
        raise APIError("Encounter not found", 404)

    if encounter.delete():
        return '', 204
    raise APIError("Failed to delete encounter", 500)

@bp.route('/<encounter_id>/monsters/<monster_name>/', methods=['POST'])
def add_monster(encounter_id, monster_name):
    """Add a monster to an encounter."""
    try:
        encounter = Encounter.get_encounter(current_app.mongo, encounter_id)
        if not encounter:
            return jsonify({'error': 'Encounter not found'}), 404

        success, message = encounter.add_monster(monster_name)
        if success:
            return jsonify(encounter.to_dict()), 200
        return jsonify({'error': message}), 400
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except RuntimeError as e:
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        return jsonify({'error': f'Unexpected error: {str(e)}'}), 500

@bp.route('/<encounter_id>/monsters/<monster_name>/', methods=['DELETE'])
@handle_api_error
def remove_monster(encounter_id, monster_name):
    """Remove a monster from an encounter."""
    try:
        _id = ObjectId(encounter_id)
    except Exception:
        raise APIError("Invalid encounter ID", 400)

    encounter = Encounter.get_encounter(request.mongo, _id)
    if not encounter:
        raise APIError("Encounter not found", 404)
    if encounter.remove_monster(monster_name):
        return jsonify(encounter.to_dict())
    raise APIError("Monster not found in encounter", 404)
