from world.grid import Grid
from .biomes_noise import *
import random
from world.world_creation.structures.structures import *
from noise import pnoise1 as noise
import hashlib

class Grid_Superstructure:
    def __init__(self, screen, worldGenParams):
        self.worldGenParams = worldGenParams
        self.foreground_grid = Grid(worldGenParams.grid_width, worldGenParams.grid_depth, worldGenParams.block_width, screen)
        self.background_grid = Grid(worldGenParams.grid_width, worldGenParams.grid_depth, worldGenParams.block_width, screen) 
        
        def make_seed(base, label):
            return int(hashlib.sha256(f"{base}_{label}".encode()).hexdigest(), 16)

        self.seed = int(random.random() * 10000)
        self.elev_seed = make_seed(self.seed, 'elevation')
        self.mountain_seed = make_seed(self.seed, 'moutain')
        self.hill_seed = make_seed(self.seed, 'hill')
        self.terrain_variation_seed = make_seed(self.seed, 'terVar')
        self.humidity_seed = make_seed(self.seed, 'humidity')
        self.temp_seed = make_seed(self.seed, 'temp')

        self.biome_priority_order = [Mountain, Ravine, Desert, Tundra, Glacier, Lake, Forest, Plains]

        # amplitutdes of different generators
        self.elevation_amp = 15
        self.mountain_amp = 38
        self.hill_amp = 8
        self.terrain_variation_amp = 2

        # frequencies
        self.elevation_freq = 300
        self.mountain_freq = 145
        self.hill_freq = 28
        self.terrain_variation_freq = 10

    def get_grids(self):
        return self.foreground_grid, self.background_grid
        
    def get_terrain_height(self, x):
        # large = noise( x * freq, base=seed % crunch value) * amp
        base_altitude_level = self.get_base_elevation(x)

        mountain = self.get_mountain_elevation(x)

        hill = noise(x * (1 / self.hill_freq), base=(self.hill_seed+1) % 256) # more rolling hills
        hill *= abs(hill) * self.hill_amp

        terVar  = noise(x * (1 / self.terrain_variation_freq),  base=(self.terrain_variation_seed+2) % 256) * self.terrain_variation_amp  # micro variation

        return int(self.worldGenParams.ground_level + base_altitude_level + mountain + hill + terVar)
    
    def get_base_elevation(self, x): # includes moutains and base elevation
        elevation  = noise(x * (1 / self.elevation_freq),  base=(self.elev_seed) % 256)
        elevation *= abs(elevation)
        elevation *= self.elevation_amp # amplitutde

        return elevation
    
    def get_mountain_elevation(self, x):
        mountain  = noise(x * (1 / self.mountain_freq),  base=(self.mountain_seed) % 256)
        mountain *= (abs(mountain) * abs(mountain) * abs(mountain)) * abs(mountain)
        mountain *= self.mountain_amp # amplitutde

        return mountain
    
    def get_biome(self, x):
        elevation = self.get_base_elevation(x)
        humidity = noise(x * 0.005,  base=(self.humidity_seed) % 256) * 20
        temp = noise(x * 0.003,  base=(self.temp_seed) % 256) * 20

        for biome in self.biome_priority_order:
            if biome.claim(elevation, temp, humidity, self.get_mountain_elevation(x)):
                return biome
        return Biome # default fallback for testing
        
    def generate_world(self):
        # biome_diagnostics = {Desert: 0, Tundra: 0, Plains: 0, Mountain: 0, Ravine: 0, Glacier: 0, Forest: 0, Montane_Forest: 0, Lake: 0}
        # max_elev = self.get_terrain_height(0)
        # min_elev = self.get_terrain_height(0)
        
        for x in range(self.foreground_grid.width): # this will loop through the grid and let me go x by x
            biome = self.get_biome(x)
            ground_elevation = self.get_terrain_height(x)

            # self.foreground_grid.set(x, ground_elevation, biome.top_layer)
            # self.foreground_grid.set(x, ground_elevation+1, biome.layer_2)

            cur_depth_down = ground_elevation
            for layer in biome.layers:
                for y in range(cur_depth_down, layer.depth+cur_depth_down):
                    self.foreground_grid.set(x, y, layer.block)
                cur_depth_down += layer.depth
            for y in range(cur_depth_down, self.foreground_grid.height):
                self.foreground_grid.set(x, y, biome.sub_layer)
                

            # biome_diagnostics[biome]+=1
            # max_elev = max(max_elev, ground_elevation)
            # min_elev = min(min_elev, ground_elevation)

        # print(biome_diagnostics)
        # print(f'min: {min_elev}')
        # print(f'max: {max_elev}')
