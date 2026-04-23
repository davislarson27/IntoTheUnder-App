from .biomes import *

class World_Generation_Settings:
    def __init__(self, version, inventory_height, health_bar_height, grid_width, grid_height, block_width):
        self.version = version
        self.default_inventory_height = inventory_height
        self.default_health_bar_height = inventory_height
        self.default_grid_width = grid_width
        self.default_grid_depth = grid_height

        self.inventory_height = inventory_height
        self.health_bar_height = inventory_height
        self.grid_width = grid_width
        self.grid_depth = grid_height

        self.block_width = block_width

        self.biomes = [Forest, Thin_Forest, Plains, Tundra, Desert, Lake, Glacier]
        self.biome_probabilities = [25, 25, 35, 8, 12, 5, 3]
        self.biome_size_variability = 15

        self.ground_level = 13

    def reset_ground_level(self, ground_level):
        self.ground_level = ground_level

    def reset_biome_chance(self, Biome, weight):
        """resets biome chance to weight (expects whole integer)"""
        for i in range(len(self.biomes)):
            if isinstance(self.biomes[i], Biome):
                self.biome_probabilities[i] = weight
                return

    def set_single_biome(self, Biome):
        """sets single biome for world generation"""
        self.biomes = [Biome]
        self.biome_probabilities = [1]

    def set_grid_width(self, newWidth):
        self.grid_width = newWidth

    def reset_defaults(self):
        self.inventory_height = self.default_inventory_height
        self.health_bar_height = self.default_inventory_height
        self.grid_width = self.default_grid_width
        self.grid_depth = self.default_grid_depth
