"""Frontend routes for NPCs."""
from flask import render_template, Blueprint

bp = Blueprint('npcs', __name__)

@bp.route('/npcs/')
def list():
    """Display the list of NPCs."""
    return render_template('npcs/list.html')

@bp.route('/npcs/create/')
def create():
    """Display the NPC creation form."""
    return render_template('npcs/create.html')

@bp.route('/npcs/<npc_id>/')
def view(npc_id):
    """Display a specific NPC."""
    return render_template('npcs/view.html', npc_id=npc_id)
