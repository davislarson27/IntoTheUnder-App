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

        self.layer_1_var_seed = make_seed(self.seed, 'layer1')
        self.layer_2_var_seed = make_seed(self.seed, 'layer2')
        self.layer_3_var_seed = make_seed(self.seed, 'layer3')

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

        hill = noise(x * (1 / self.hill_freq), base=(self.hill_seed) % 256) # more rolling hills
        hill *= abs(hill) * self.hill_amp

        terVar  = noise(x * (1 / self.terrain_variation_freq),  base=(self.terrain_variation_seed) % 256) * self.terrain_variation_amp  # micro variation

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
        return Plains # default fallback
        
    def get_layer_increment(self, x, layerNum, layer): # layer num is which layer we are on (not blocks deep)
        """returns a postive number of how many additional blocks of a layer to add on as variation"""
        if layerNum == 0:
            seed = self.layer_1_var_seed
        elif layerNum == 1:
            seed = self.layer_2_var_seed
        else:
            seed = self.layer_3_var_seed

        return abs(int(noise(x * (1 / layer.variation_freq), base=(seed) % 256) * layer.variation_amp))


    def generate_world(self):
        # generate the foreground
        for x in range(self.foreground_grid.width): # this will loop through the grid and let me go x by x
            biome = self.get_biome(x)
            ground_elevation = self.get_terrain_height(x)

            cur_depth_down = ground_elevation
            layer_num = 0
            for layer in biome.layers:
                for y in range(cur_depth_down, layer.depth+cur_depth_down):
                    self.foreground_grid.set(x, y, layer.block)
                variation = self.get_layer_increment(x, layer_num, layer)
                cur_depth_down += layer.depth
                for y in range(cur_depth_down, cur_depth_down+variation):
                    self.foreground_grid.set(x, y, layer.block)
                cur_depth_down += variation
                layer_num+=1
            for y in range(cur_depth_down, self.foreground_grid.height):
                self.foreground_grid.set(x, y, biome.sub_layer)


        # generate the background
        for x in range(self.background_grid.width): # this will loop through the grid and let me go x by x
            biome = self.get_biome(x)
            ground_elevation = self.get_terrain_height(x)

            cur_depth_down = ground_elevation
            layer_num = 0
            for layer in biome.layers:
                for y in range(cur_depth_down, layer.depth+cur_depth_down):
                    self.background_grid.set(x, y, layer.block)
                variation = self.get_layer_increment(x, layer_num, layer)
                cur_depth_down += layer.depth
                for y in range(cur_depth_down, cur_depth_down+variation):
                    self.background_grid.set(x, y, layer.block)
                cur_depth_down += variation
                layer_num+=1
            for y in range(cur_depth_down, self.background_grid.height):
                self.background_grid.set(x, y, biome.sub_layer)
                