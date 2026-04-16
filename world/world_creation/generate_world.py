from world.grid import Grid
from .biomes import *

class Grid_Superstructure:
    def __init__(self, screen, worldGenParams):
        self.worldGenParams = worldGenParams
        self.foreground_grid = Grid(worldGenParams.grid_width, worldGenParams.grid_depth, worldGenParams.block_width, screen)
        self.background_grid = Grid(worldGenParams.grid_width, worldGenParams.grid_depth, worldGenParams.block_width, screen)

    def generate_world(self):
        # temporary test
        self.foreground_grid.generate_terrain()
        self.background_grid.generate_terrain()

    def get_grids(self):
        return self.foreground_grid, self.background_grid
        