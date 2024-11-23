"""Frontend routes for encounters."""
from flask import render_template, Blueprint

bp = Blueprint('encounters', __name__)

@bp.route('/encounters/')
def list():
    """Display the list of encounters."""
    return render_template('encounters/list.html')

@bp.route('/encounters/create/')
def create():
    """Display the encounter creation form."""
    return render_template('encounters/create.html')

@bp.route('/encounters/<encounter_id>/')
def view(encounter_id):
    """Display a specific encounter."""
    return render_template('encounters/view.html', encounter_id=encounter_id)
