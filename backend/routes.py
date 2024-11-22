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
