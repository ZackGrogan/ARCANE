from flask import Flask
from flask_assets import Environment, Bundle

def create_app():
    app = Flask(__name__)
    assets = Environment(app)

    # Configure assets
    css = Bundle(
        'css/main.css',
        output='css/main.min.css'
    )
    assets.register('css', css)

    js = Bundle(
        'js/main.js',
        output='js/main.min.js'
    )
    assets.register('js', js)

    # Register blueprints
    from app.main import bp as main_bp
    from app.main.npc_routes import bp as npc_bp
    from app.main.encounter_routes import bp as encounter_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(npc_bp)
    app.register_blueprint(encounter_bp)

    return app
