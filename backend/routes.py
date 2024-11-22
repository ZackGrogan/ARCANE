from flask import Blueprint, jsonify, request
from .models.npc import NPC
from .models.encounter import Encounter
from .models.campaign import Campaign

# Create Blueprints
npc_blueprint = Blueprint('npcs', __name__)
encounter_blueprint = Blueprint('encounters', __name__)
campaign_blueprint = Blueprint('campaigns', __name__)

# NPC Routes
@npc_blueprint.route('/npcs', methods=['POST'])
def create_npc():
    data = request.json
    npc = NPC(mongo, **data)
    npc.save()
    return jsonify({'message': 'NPC created successfully'}), 201

@npc_blueprint.route('/npcs', methods=['GET'])
def get_npcs():
    npcs = mongo.db.npcs.find()
    return jsonify([npc for npc in npcs]), 200

@npc_blueprint.route('/npcs/edit/<npc_id>', methods=['GET', 'POST'])
def edit_npc(npc_id):
    # Logic for editing an NPC
    pass

@npc_blueprint.route('/npcs/delete/<npc_id>', methods=['POST'])
def delete_npc(npc_id):
    # Logic for deleting an NPC
    pass

# Encounter Routes
@encounter_blueprint.route('/encounters', methods=['POST'])
def create_encounter():
    data = request.json
    encounter = Encounter(mongo, **data)
    encounter.save()
    return jsonify({'message': 'Encounter created successfully'}), 201

@encounter_blueprint.route('/encounters', methods=['GET'])
def get_encounters():
    encounters = mongo.db.encounters.find()
    return jsonify([encounter for encounter in encounters]), 200

@encounter_blueprint.route('/encounters/edit/<encounter_id>', methods=['GET', 'POST'])
def edit_encounter(encounter_id):
    # Logic for editing an encounter
    pass

@encounter_blueprint.route('/encounters/delete/<encounter_id>', methods=['POST'])
def delete_encounter(encounter_id):
    # Logic for deleting an encounter
    pass

# Campaign Routes
@campaign_blueprint.route('/campaigns', methods=['POST'])
def create_campaign():
    data = request.json
    campaign = Campaign(mongo, **data)
    campaign.save()
    return jsonify({'message': 'Campaign created successfully'}), 201

@campaign_blueprint.route('/campaigns', methods=['GET'])
def get_campaigns():
    campaigns = mongo.db.campaigns.find()
    return jsonify([campaign for campaign in campaigns]), 200

@campaign_blueprint.route('/campaigns/edit/<campaign_id>', methods=['GET', 'POST'])
def edit_campaign(campaign_id):
    # Logic for editing a campaign
    pass

@campaign_blueprint.route('/campaigns/delete/<campaign_id>', methods=['POST'])
def delete_campaign(campaign_id):
    # Logic for deleting a campaign
    pass
