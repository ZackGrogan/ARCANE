import numpy as np
from noise import pnoise2
from PIL import Image

class MapGenerator:
    def __init__(self, width, height, scale=100, octaves=6, persistence=0.5, lacunarity=2.0):
        self.width = width
        self.height = height
        self.scale = scale
        self.octaves = octaves
        self.persistence = persistence
        self.lacunarity = lacunarity

    def generate_height_map(self):
        height_map = np.zeros((self.height, self.width))
        for y in range(self.height):
            for x in range(self.width):
                height_map[y][x] = pnoise2(x / self.scale,
                                            y / self.scale,
                                            octaves=self.octaves,
                                            persistence=self.persistence,
                                            lacunarity=self.lacunarity,
                                            repeatx=self.width,
                                            repeaty=self.height,
                                            base=0)
        return height_map

    terrain_ranges = {
        'water': (-float('inf'), -0.05),
        'plains': (-0.05, 0.2),
        'forest': (0.2, 0.5),
        'mountain': (0.5, float('inf'))
    }

    terrain_colors = {
        'water': (0, 0, 255),
        'plains': (154, 220, 180),  
        'forest': (34, 139, 34),  
        'mountain': (139, 137, 137)
    }

    def classify_terrain(self, height_value):
        for terrain_type, (min_val, max_val) in self.terrain_ranges.items():
            if min_val <= height_value < max_val:
                return terrain_type
        return 'unknown'  

    def generate_map_image(self, height_map):
        image = Image.new('RGB', (self.width, self.height))
        for y in range(self.height):
            for x in range(self.width):
                terrain_type = self.classify_terrain(height_map[y][x])
                image.putpixel((x, y), self.terrain_colors[terrain_type])
        return image
