from flask import Blueprint, jsonify, request, redirect, url_for, render_template, flash
from .models.npc import NPC
from .models.encounter import Encounter
from .models.campaign import Campaign
from backend.app.ai_services.gemini_service import GeminiService
from backend.app.ai_services.flux_service import FLUXService
from .forms import NPCForm

# Create Blueprints
npc_blueprint = Blueprint('npcs', __name__)
encounter_blueprint = Blueprint('encounters', __name__)
campaign_blueprint = Blueprint('campaigns', __name__)

# Initialize AI services
gemini_service = GeminiService()
flux_service = FLUXService()

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

@npc_blueprint.route('/npcs/create', methods=['GET', 'POST'])
def create_npc_with_ai():
    form = NPCForm()
    if form.validate_on_submit():
        name_prompt = form.name_prompt.data
        if not name_prompt:
            flash('Please provide a name prompt.', 'error')
            return render_template('npcs/create.html', form=form)

        backstory_prompt = form.backstory_prompt.data
        if not backstory_prompt:
            flash('Please provide a backstory prompt.', 'error')
            return render_template('npcs/create.html', form=form)

        name = gemini_service.generate_name(name_prompt)
        if name is None:
            flash('Error generating name.', 'error')
            return render_template('npcs/create.html', form=form)

        backstory = gemini_service.generate_backstory(backstory_prompt)
        if backstory is None:
            flash('Error generating backstory.', 'error')
            return render_template('npcs/create.html', form=form)

        portrait_prompt = form.portrait_prompt.data
        if not portrait_prompt:
            flash('Please provide a portrait prompt.', 'error')
            return render_template('npcs/create.html', form=form)

        portrait_url = flux_service.generate_profile_picture(portrait_prompt)
        if portrait_url is None:
            flash('Error generating portrait.', 'error')
            return render_template('npcs/create.html', form=form)

        # Create NPC object
        npc = NPC(
            mongo,
            name=name,
            race=form.race.data,
            npc_class=form.npc_class.data,
            alignment=form.alignment.data,
            level=form.level.data,
            background=form.background.data,
            personality=form.personality.data,
            abilities=form.abilities.data,
            skills=form.skills.data,
            equipment=form.equipment.data,
            description=backstory,
            portrait_url=portrait_url
        )
        # Save NPC to the database
        mongo.db.npcs.insert_one(npc.__dict__)
        return redirect(url_for('npcs.list'))
    return render_template('npcs/create.html', form=form)

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
