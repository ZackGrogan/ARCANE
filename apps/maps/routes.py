from flask import Blueprint, render_template, request, redirect, url_for
from backend.app import mongo
from apps.maps.map_generator import MapGenerator
import os
from PIL import Image
import uuid

maps_blueprint = Blueprint('maps', __name__)

@maps_blueprint.route('/maps/generate', methods=['GET', 'POST'])
def generate_map():
    if request.method == 'POST':
        try:
            width = int(request.form['width'])
            height = int(request.form['height'])
            scale = float(request.form['scale'])
            octaves = int(request.form['octaves'])
            persistence = float(request.form['persistence'])
            lacunarity = float(request.form['lacunarity'])

            if not (10 <= width <= 1000 and 10 <= height <= 1000 and 1 <= scale <= 500 and 1 <= octaves <= 10 and 0 <= persistence <= 1 and 0 <= lacunarity <= 5):
                raise ValueError("Invalid input values.")
        except (KeyError, ValueError, TypeError):
            return "Invalid input", 400

        generator = MapGenerator(width, height, scale, octaves, persistence, lacunarity)
        height_map = generator.generate_height_map()
        map_image = generator.generate_map_image(height_map)

        filename = str(uuid.uuid4()) + '.png'
        map_image_path = os.path.join('static', 'maps', filename)
        map_image.save(map_image_path)

        # Save map metadata to the database
        map_data = {
            'width': width,
            'height': height,
            'scale': scale,
            'octaves': octaves,
            'persistence': persistence,
            'lacunarity': lacunarity,
            'image_path': map_image_path
        }
        mongo.db.maps.insert_one(map_data)

        return render_template('maps/generate.html', map_image_url=url_for('static', filename='maps/' + filename))

    return render_template('maps/generate.html')

@maps_blueprint.route('/api/maps/', methods=['GET'])
def list_maps():
    # Logic to list all maps
    pass

@maps_blueprint.route('/api/maps/', methods=['POST'])
def create_map():
    # Logic to create a new map
    pass

@maps_blueprint.route('/api/maps/<map_id>/', methods=['GET'])
def get_map(map_id):
    # Logic to get map details
    pass

@maps_blueprint.route('/api/maps/<map_id>/', methods=['PUT'])
def update_map(map_id):
    # Logic to update map
    pass

@maps_blueprint.route('/api/maps/<map_id>/', methods=['DELETE'])
def delete_map(map_id):
    # Logic to delete map
    pass

@maps_blueprint.route('/api/maps/generate/', methods=['POST'])
def generate_map_api():
    # Logic to generate map using AI (for future integration)
    pass
