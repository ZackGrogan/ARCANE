"""Campaign routes for the API."""
from flask import Blueprint, jsonify, request, current_app
from backend.models.campaign import Campaign
from backend.utils.errors import handle_api_error, APIError
import logging

bp = Blueprint('campaign', __name__)

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@bp.before_request
def before_request():
    """Add mongo to request object."""
    request.mongo = current_app.mongo

def validate_campaign_data(data, update=False):
    """Validate campaign request data."""
    logger.debug(f"Validating campaign data: {data}")
    required_fields = ['name', 'description', 'start_date'] if not update else []
    missing_fields = [field for field in required_fields if field not in data]

    if missing_fields:
        error_msg = f"Missing required fields: {', '.join(missing_fields)}"
        logger.error(error_msg)
        raise ValueError(error_msg)

    # Validate data types for fields that are present
    if 'name' in data and not isinstance(data['name'], str):
        raise ValueError("name must be a string")
    if 'description' in data and not isinstance(data['description'], str):
        raise ValueError("description must be a string")
    if 'start_date' in data and not isinstance(data['start_date'], str):
        raise ValueError("start_date must be a string")

    logger.debug("Campaign data validation successful")
    return data

@bp.route('/', methods=['POST'])
@handle_api_error
def create_campaign():
    """Create a new campaign."""
    logger.debug("Processing create campaign request")
    data = request.get_json()
    if not data:
        raise APIError("No data provided", status_code=400)

    try:
        data = validate_campaign_data(data)
        campaign = Campaign.from_dict(current_app.mongo, data)
        campaign_id = campaign.save()
        return jsonify(campaign.to_dict()), 201
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f"Failed to create campaign: {str(e)}")
        return jsonify({'error': f'Failed to create campaign: {str(e)}'}), 400

@bp.route('/', methods=['GET'])
@handle_api_error
def get_campaigns():
    """Get all campaigns."""
    logger.debug("Processing get all campaigns request")
    try:
        campaigns = Campaign.list_campaigns(current_app.mongo)
        return jsonify(campaigns)
    except Exception as e:
        logger.error(f"Failed to retrieve campaigns: {str(e)}")
        return jsonify({'error': f'Failed to retrieve campaigns: {str(e)}'}), 400

@bp.route('/<campaign_name>', methods=['GET'])
@handle_api_error
def get_campaign(campaign_name):
    """Get a specific campaign."""
    logger.debug(f"Processing get campaign request for: {campaign_name}")
    try:
        campaign = Campaign.get_by_name(current_app.mongo, campaign_name)
        if not campaign:
            return jsonify({'error': 'Campaign not found'}), 404
        return jsonify(campaign.to_dict())
    except Exception as e:
        logger.error(f"Failed to retrieve campaign {campaign_name}: {str(e)}")
        return jsonify({'error': f'Failed to retrieve campaign: {str(e)}'}), 400

@bp.route('/<campaign_name>', methods=['PUT'])
@handle_api_error
def update_campaign(campaign_name):
    """Update a specific campaign."""
    logger.debug(f"Processing update campaign request for: {campaign_name}")
    data = request.get_json()
    if not data:
        raise APIError("No data provided", status_code=400)

    try:
        campaign = Campaign.get_by_name(current_app.mongo, campaign_name)
        if not campaign:
            return jsonify({'error': 'Campaign not found'}), 404

        # Validate update data
        if 'name' in data and data['name'] != campaign_name:
            # Check if new name is unique
            existing = Campaign.get_by_name(current_app.mongo, data['name'])
            if existing:
                raise ValueError("Campaign with this name already exists")

        campaign.update(data)
        return jsonify(campaign.to_dict())
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f"Failed to update campaign {campaign_name}: {str(e)}")
        return jsonify({'error': f'Failed to update campaign: {str(e)}'}), 400

@bp.route('/<campaign_name>', methods=['DELETE'])
@handle_api_error
def delete_campaign(campaign_name):
    """Delete a specific campaign."""
    logger.debug(f"Processing delete campaign request for: {campaign_name}")
    try:
        campaign = Campaign.get_by_name(current_app.mongo, campaign_name)
        if not campaign:
            return jsonify({'error': 'Campaign not found'}), 404
        campaign.delete()
        return '', 204
    except Exception as e:
        logger.error(f"Failed to delete campaign {campaign_name}: {str(e)}")
        return jsonify({'error': f'Failed to delete campaign: {str(e)}'}), 400

@bp.route('/<campaign_name>/npcs/<npc_id>', methods=['POST'])
@handle_api_error
def add_npc_to_campaign(campaign_name, npc_id):
    """Add an NPC to a campaign."""
    logger.debug(f"Processing add NPC to campaign request for: {campaign_name}, {npc_id}")
    try:
        campaign = Campaign.get_by_name(current_app.mongo, campaign_name)
        if not campaign:
            return jsonify({'error': 'Campaign not found'}), 404

        campaign.add_npc(npc_id)
        return jsonify(campaign.to_dict())
    except Exception as e:
        logger.error(f"Failed to add NPC to campaign {campaign_name}, {npc_id}: {str(e)}")
        return jsonify({'error': f'Failed to add NPC to campaign: {str(e)}'}), 400

@bp.route('/<campaign_name>/npcs/<npc_id>', methods=['DELETE'])
@handle_api_error
def remove_npc_from_campaign(campaign_name, npc_id):
    """Remove an NPC from a campaign."""
    logger.debug(f"Processing remove NPC from campaign request for: {campaign_name}, {npc_id}")
    try:
        campaign = Campaign.get_by_name(current_app.mongo, campaign_name)
        if not campaign:
            return jsonify({'error': 'Campaign not found'}), 404

        if campaign.remove_npc(npc_id):
            return jsonify(campaign.to_dict())
        else:
            return jsonify({'error': 'NPC not found in campaign'}), 404
    except Exception as e:
        logger.error(f"Failed to remove NPC from campaign {campaign_name}, {npc_id}: {str(e)}")
        return jsonify({'error': f'Failed to remove NPC from campaign: {str(e)}'}), 400

@bp.route('/<campaign_name>/encounters/<encounter_id>', methods=['POST'])
@handle_api_error
def add_encounter_to_campaign(campaign_name, encounter_id):
    """Add an encounter to a campaign."""
    logger.debug(f"Processing add encounter to campaign request for: {campaign_name}, {encounter_id}")
    try:
        campaign = Campaign.get_by_name(current_app.mongo, campaign_name)
        if not campaign:
            return jsonify({'error': 'Campaign not found'}), 404

        campaign.add_encounter(encounter_id)
        return jsonify(campaign.to_dict())
    except Exception as e:
        logger.error(f"Failed to add encounter to campaign {campaign_name}, {encounter_id}: {str(e)}")
        return jsonify({'error': f'Failed to add encounter to campaign: {str(e)}'}), 400

@bp.route('/<campaign_name>/encounters/<encounter_id>', methods=['DELETE'])
@handle_api_error
def remove_encounter_from_campaign(campaign_name, encounter_id):
    """Remove an encounter from a campaign."""
    logger.debug(f"Processing remove encounter from campaign request for: {campaign_name}, {encounter_id}")
    try:
        campaign = Campaign.get_by_name(current_app.mongo, campaign_name)
        if not campaign:
            return jsonify({'error': 'Campaign not found'}), 404

        if campaign.remove_encounter(encounter_id):
            return jsonify(campaign.to_dict())
        else:
            return jsonify({'error': 'Encounter not found in campaign'}), 404
    except Exception as e:
        logger.error(f"Failed to remove encounter from campaign {campaign_name}, {encounter_id}: {str(e)}")
        return jsonify({'error': f'Failed to remove encounter from campaign: {str(e)}'}), 400
