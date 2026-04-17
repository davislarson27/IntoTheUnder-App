from world.grid import Grid
from .biomes_noise import *
import random
from world.world_creation.structures.structures import *
from noise import pnoise1, pnoise2
from .ores_noise import Ore
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
        self.bg_hill_seed = make_seed(self.seed, 'bg_hill')
        self.bg_ter_var_seed = make_seed(self.seed, 'bg_ter_var')

        self.layer_1_var_seed = make_seed(self.seed, 'layer1')
        self.layer_2_var_seed = make_seed(self.seed, 'layer2')
        self.layer_3_var_seed = make_seed(self.seed, 'layer3')

        self.biome_priority_order = [Mountain, Ravine, Desert, Tundra, Glacier, Rain_Forest, Forest, Montane_Forest, Plains]

        # amplitutdes of different generators
        self.elevation_amp = 15
        self.mountain_amp = 38
        self.hill_amp = 8
        self.terrain_variation_amp = 2
        self.bg_hill_amp = self.hill_amp
        self.bg_ter_var_amp = self.terrain_variation_amp

        # frequencies
        self.elevation_freq = 300
        self.mountain_freq = 145
        self.hill_freq = 28
        self.terrain_variation_freq = 10
        self.bg_hill_freq = self.hill_freq
        self.bg_ter_var_freq = self.terrain_variation_freq

        self.ores = { # higher scale = smaller veins, higher threshold = less common
            Coal_Ore_Block: Ore(self.seed, Coal_Ore_Block, threshold=0.61, scale=0.11, min_depth=10),
            Iron_Ore_Block: Ore(self.seed, Iron_Ore_Block, threshold=0.62, scale=0.17, min_depth=15),
            Emerald_Ore_Block: Ore(self.seed, Emerald_Ore_Block, threshold=0.8, scale=0.22, min_depth=25),
            Diamond_Ore_Block: Ore(self.seed, Diamond_Ore_Block, threshold=0.85, scale=0.22, min_depth=35),
            Mabelite_Ore_Block: Ore(self.seed, Mabelite_Ore_Block, threshold=0.85, scale=0.3, min_depth=65),
            Sulfur_Flakes_Block: Ore(self.seed, Sulfur_Flakes_Block, threshold=0.8, scale=0.22, min_depth=12),
        }

    def get_grids(self):
        return self.foreground_grid, self.background_grid
        
    def lake_depth_value(self, x):
        # mountain = self.get_mountain_elevation(x)
        mountain = 0

        hill = pnoise1(x * (1 / self.hill_freq), base=(self.hill_seed) % 256) # more rolling hills
        hill *= abs(hill) * self.hill_amp

        return int(mountain + hill)

    def get_terrain_height(self, x):
        # large = pnoise1( x * freq, base=seed % crunch value) * amp
        base_altitude_level = self.get_base_elevation(x)

        mountain = self.get_mountain_elevation(x)

        hill = pnoise1(x * (1 / self.hill_freq), base=(self.hill_seed) % 256) # more rolling hills
        hill *= abs(hill) * self.hill_amp

        terVar  = pnoise1(x * (1 / self.terrain_variation_freq),  base=(self.terrain_variation_seed) % 256) * self.terrain_variation_amp  # micro variation

        return int(self.worldGenParams.ground_level + base_altitude_level + mountain + hill + terVar)
    
    def get_base_elevation(self, x): # includes moutains and base elevation
        elevation  = pnoise1(x * (1 / self.elevation_freq),  base=(self.elev_seed) % 256)
        elevation *= abs(elevation)
        elevation *= self.elevation_amp # amplitutde

        return elevation
    
    def get_mountain_elevation(self, x):
        mountain  = pnoise1(x * (1 / self.mountain_freq),  base=(self.mountain_seed) % 256)
        mountain *= (abs(mountain) * abs(mountain) * abs(mountain)) * abs(mountain)
        mountain *= self.mountain_amp # amplitutde

        return mountain
    
    def get_biome(self, x):
        elevation = self.get_base_elevation(x)
        humidity = self.get_humidity(x)
        temp = pnoise1(x * 0.003,  base=(self.temp_seed) % 256) * 20

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

        return abs(int(pnoise1(x * (1 / layer.variation_freq), base=(seed) % 256) * layer.variation_amp))

    def get_bg_terrain_height(self, x):
        # large = pnoise1( x * freq, base=seed % crunch value) * amp
        base_altitude_level = self.get_base_elevation(x)

        mountain = self.get_mountain_elevation(x) // 3 # keeps some of the mountain noise but stops it from following them  all the way up

        hill = pnoise1(x * (1 / self.bg_hill_freq), base=(self.bg_hill_seed) % 256) # more rolling hills
        hill *= abs(hill) * self.bg_hill_amp

        terVar  = pnoise1(x * (1 / self.bg_ter_var_freq),  base=(self.bg_ter_var_freq) % 256) * self.bg_ter_var_amp  # micro variation

        return int(self.worldGenParams.ground_level + base_altitude_level + mountain + hill + terVar)
    
    def get_humidity(self, x):
        return pnoise1(x * 0.005,  base=(self.humidity_seed) % 256) * 20
            

    def generate_world(self):


        # idea: have lakes spawn when the mountain or hill value drops below a value (because i know it is a short term dip) and the humidity is low and have it spawn water down until the value hops back up)
        # # start at maybe elevation level when the value dips then have each chunk where the value is true look over to its left to find it where the start happened



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

            # generate ores at this level
            i = 1
            for y in range(ground_elevation, self.foreground_grid.height):
                for ore in self.ores:
                    ore_noise = self.ores[ore]
                    if i < ore_noise.min_depth:
                        continue
                    if ore_noise.find(x, y, biome.multiplier[ore] * (i - ore_noise.min_depth)): # returns True if this ore should be here
                        self.foreground_grid.set(x, y, ore)
                i+=1


        # identify water basins pass
        water_basin_anchors = []
        for x in range(self.foreground_grid.width):
            suddenDepthValue = self.lake_depth_value(x)
            humidity = self.get_humidity(x)
            if suddenDepthValue < -(self.hill_amp * 3 / 5) and humidity > 6: # this means conditions are met for water for form
                if len(water_basin_anchors) == 0 or water_basin_anchors[-1] != x - 1:
                    water_basin_anchors.append(x)

        # fill water basins pass
        for x in water_basin_anchors:
            # check for filling left
            water_level = self.get_terrain_height(x)
            start_x = x
            while start_x > 0 and self.get_terrain_height(start_x - 1) > water_level:
                start_x-=1
            end_x = x
            while end_x + 1 < self.foreground_grid.width and self.get_terrain_height(end_x + 1) > water_level:
                end_x+=1
            for fill_x in range(start_x, end_x+1):
                for y in range(water_level, self.get_terrain_height(fill_x)):
                    # print(f'  literally generated water at {fill_x, y}')
                    self.foreground_grid.set(fill_x, y, Water, True)
            # print(f'generated water from x={start_x} to x={end_x}')



        # generate the background
        for x in range(self.background_grid.width): # this will loop through the grid and let me go x by x
            biome = self.get_biome(x)
            ground_elevation = self.get_bg_terrain_height(x)

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
                