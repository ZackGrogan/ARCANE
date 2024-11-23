"""API package initialization."""
from .routes import npc_routes, campaign_routes, encounter_routes

__all__ = ['npc_routes', 'campaign_routes', 'encounter_routes']

def init_api(app):
    """Initialize API blueprints."""
    app.register_blueprint(npc_routes.bp, url_prefix='/api/npcs')
    app.register_blueprint(campaign_routes.bp, url_prefix='/api/campaigns')
    app.register_blueprint(encounter_routes.bp, url_prefix='/api/encounters')
