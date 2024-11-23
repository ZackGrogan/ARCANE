"""NPC routes for the API."""
from flask import Blueprint, jsonify, request, current_app
from backend.models.npc import NPC
from backend.utils.errors import handle_api_error, APIError

bp = Blueprint('npc', __name__, url_prefix='/api/npcs')

@bp.route('/', methods=['POST'])
@handle_api_error
def create_npc():
    """Create a new NPC."""
    data = request.get_json()
    if not data:
        raise APIError("No data provided", status_code=400)

    required_fields = ['name', 'race', 'npc_class', 'level', 'alignment', 'abilities']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        raise APIError(f"Missing required fields: {', '.join(missing_fields)}", status_code=400)

    npc = NPC.from_dict(current_app.mongo, data)
    npc_id = npc.save()
    return jsonify(npc.to_dict()), 201

@bp.route('/<npc_id>/', methods=['GET'])
@handle_api_error
def get_npc(npc_id):
    """Get a specific NPC."""
    npc = NPC.get_by_id(current_app.mongo, npc_id)
    if not npc:
        raise APIError("NPC not found", status_code=404)
    return jsonify(npc.to_dict())

@bp.route('/', methods=['GET'])
@handle_api_error
def get_npcs():
    """Get all NPCs."""
    npcs = NPC.list_npcs(current_app.mongo)
    return jsonify([{**npc, '_id': str(npc['_id'])} for npc in npcs])

@bp.route('/<npc_id>/', methods=['PUT'])
@handle_api_error
def update_npc(npc_id):
    """Update a specific NPC."""
    data = request.get_json()
    if not data:
        raise APIError("No data provided", status_code=400)

    npc = NPC.get_by_id(current_app.mongo, npc_id)
    if not npc:
        raise APIError("NPC not found", status_code=404)

    npc.update(data)
    return jsonify(npc.to_dict())

@bp.route('/<npc_id>/', methods=['DELETE'])
@handle_api_error
def delete_npc(npc_id):
    """Delete a specific NPC."""
    npc = NPC.get_by_id(current_app.mongo, npc_id)
    if not npc:
        raise APIError("NPC not found", status_code=404)

    npc.delete()
    return '', 204
