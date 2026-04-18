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

        self.cave_tunnel_seed = make_seed(self.seed, 'cave_tunnel_seed')
        self.cave_cavern_seed = make_seed(self.seed, 'cave_cavern_seed')

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
        self.cave_tunnel_x_freq = 0.02
        self.cave_tunnel_y_freq = 0.12
        self.cave_cavern_x_freq = 0.07
        self.cave_cavern_y_freq = 0.07

        # thresholds
        self.cave_threshold = 0.645

        self.ores = { # higher scale = smaller veins, higher threshold = less common
            Dirt: Ore(self.seed, Dirt, threshold=0.5, scale=0.11, min_depth=10),
            Gravel: Ore(self.seed, Gravel, threshold=0.5, scale=0.11, min_depth=10),
            Coal_Ore_Block: Ore(self.seed, Coal_Ore_Block, threshold=0.61, scale=0.11, min_depth=10),
            Iron_Ore_Block: Ore(self.seed, Iron_Ore_Block, threshold=0.62, scale=0.17, min_depth=15),
            Gold_Ore_Block: Ore(self.seed, Gold_Ore_Block, threshold=0.71, scale=0.18, min_depth=30),
            Emerald_Ore_Block: Ore(self.seed, Emerald_Ore_Block, threshold=0.77, scale=0.18, min_depth=25),
            Diamond_Ore_Block: Ore(self.seed, Diamond_Ore_Block, threshold=0.81, scale=0.18, min_depth=35),
            Mabelite_Ore_Block: Ore(self.seed, Mabelite_Ore_Block, threshold=0.84, scale=0.17, min_depth=65),
            Sulfur_Flakes_Block: Ore(self.seed, Sulfur_Flakes_Block, threshold=0.77, scale=0.18, min_depth=12),
        }

    def get_grids(self):
        return self.foreground_grid, self.background_grid
    
    def get_hash_chance(self, x, y, need):
        hash = int(hashlib.sha256(f"{self.seed}_{need}_{x}_{y}".encode()).hexdigest(), 16)
        return (hash % 1000) / 1000.0  # value 0.0–1.0

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

        def _get_biome(x):
            elevation = self.get_base_elevation(x)
            humidity = self.get_humidity(x)
            temp = pnoise1(x * 0.003,  base=(self.temp_seed) % 256) * 20

            for biome in self.biome_priority_order:
                if biome.claim(elevation, temp, humidity, self.get_mountain_elevation(x)):
                    return biome

            return Plains # default fallback
        
        biome = _get_biome(x)
        if x > 0 and x < self.foreground_grid.width: # prevents 1 block wide biomes in the middle of another biome
            prev_biome = _get_biome(x-1)
            next_biome = _get_biome(x+1)
            if biome is not prev_biome and biome is not next_biome: # prevents one block bimes
                biome = prev_biome
        return biome
        
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
    
    def is_cave(self, x, y):
        tunnel = pnoise2(x * self.cave_tunnel_x_freq, y * self.cave_tunnel_y_freq, base=self.cave_tunnel_seed & 256)
        cavern = pnoise2(x * self.cave_cavern_x_freq, y * self.cave_cavern_y_freq, base=self.cave_cavern_seed & 256)

        if tunnel + cavern > self.cave_threshold:
            return True
        return False
    
    def get_humidity(self, x):
        return pnoise1(x * 0.005,  base=(self.humidity_seed) % 256) * 20
            

    def generate_world(self):
        for _ in self._generate_world():
            pass

    def _generate_world(self):

        yield 'Generating Grid', 0

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
        
        # yield 'generating lakes'

        # # identify water basins pass
        # water_basin_anchors = []
        # for x in range(self.foreground_grid.width):
        #     suddenDepthValue = self.lake_depth_value(x)
        #     humidity = self.get_humidity(x)
        #     # absolute_height = self.get_bg_terrain_height(x)
        #     # elevation = self.get_base_elevation(x)
        #     # if absolute_height < elevation and suddenDepthValue < -(self.hill_amp * 3 / 5) and humidity > 6: # this means conditions are met for water for form
        #     if suddenDepthValue < -(self.hill_amp * 3 / 5) and humidity > 6: # this means conditions are met for water for form
        #         if len(water_basin_anchors) == 0 or water_basin_anchors[-1] != x - 1:
        #             water_basin_anchors.append(x)

        # # fill water basins pass
        # for x in water_basin_anchors:
        #     # check for filling left
        #     water_level = self.get_terrain_height(x)
        #     start_x = x
        #     while start_x > 0 and self.get_terrain_height(start_x - 1) > water_level:
        #         start_x-=1
        #     end_x = x
        #     while end_x + 1 < self.foreground_grid.width and self.get_terrain_height(end_x + 1) > water_level:
        #         end_x+=1
        #     for fill_x in range(start_x, end_x+1):
        #         for y in range(water_level, self.get_terrain_height(fill_x)):
        #             # print(f'  literally generated water at {fill_x, y}')
        #             self.foreground_grid.set(fill_x, y, Water, True)
        #     # print(f'generated water from x={start_x} to x={end_x}')


        yield 'Generating Background', 25

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
                
        yield 'Generating Structures', 40

        for x in range(self.foreground_grid.width):
            saltpeter_chance = 0.035
            for y in range(self.get_terrain_height(x)+1, self.foreground_grid.height):
                if self.is_cave(x, y):
                    block_set = None
                    if self.is_cave(x, y+1) and not self.is_cave(x, y-1): # check if block below is a cave
                        if self.get_hash_chance(x, y, 'saltpeter') < saltpeter_chance:
                            block_set = Saltpeter
                    self.foreground_grid.set(x, y, block_set)

        # generate ground level objects & structures for the background
        # should this be run with the foreground so foreground & background structures don't overlap?
        x = 1 # structures don't generate at x=0
        while x < self.background_grid.width:
            # get biome
            biome = self.get_biome(x)

            # get seed based random number (hashed based on x)
            hash = int(hashlib.sha256(f"{self.seed}_bg_struct_{x}".encode()).hexdigest(), 16)
            structure_odds = (hash % 1000) / 1000.0  # value 0.0–1.0

            subStructure_hash = int(hashlib.sha256(f"{self.seed}_bg_sub_struct_{x}".encode()).hexdigest(), 16)
            instruction_variance_chance = (subStructure_hash % 1000) / 1000.0  # value 0.0–1.0

            # get structure to generate based on biome
            running_odds_total = 0
            for structureIdentifier in biome.bg_structures:
                if structureIdentifier.odds + running_odds_total > structure_odds:
                    # build structure
                    structure = structureIdentifier.structure
                    y = self.get_bg_terrain_height(x + structure.get_x_difference_for_y())
                    foreground_height = self.get_terrain_height(x + structure.get_x_difference_for_y())
                    if y > foreground_height: # no structures can generate in the background if it is below the surface
                        break
                    buildInstructions = structure.getStructureInstructions(x, y, self.background_grid, instruction_variance_chance)
                    for instruction in buildInstructions:
                        instruction.setBlock(self.background_grid)

                    # jump x past the end of the structure
                    x += structure.get_width()

                    break
                running_odds_total += structureIdentifier.odds
            
            x += 1


        # generate ground level objects & structures
        x = 1 # structures don't generate at x=0
        while x < self.foreground_grid.width:
            # get biome
            biome = self.get_biome(x)

            # get seed based random number (hashed based on x)
            hash = int(hashlib.sha256(f"{self.seed}_struct_{x}".encode()).hexdigest(), 16)
            structure_odds = (hash % 1000) / 1000.0  # value 0.0–1.0

            subStructure_hash = int(hashlib.sha256(f"{self.seed}_sub_struct_{x}".encode()).hexdigest(), 16)
            instruction_variance_chance = (subStructure_hash % 1000) / 1000.0  # value 0.0–1.0

            # get structure to generate based on biome
            running_odds_total = 0
            for structureIdentifier in biome.structures:
                if structureIdentifier.odds + running_odds_total > structure_odds:
                    # build structure
                    structure = structureIdentifier.structure
                    y = self.get_terrain_height(x + structure.get_x_difference_for_y())
                    buildInstructions = structure.getStructureInstructions(x, y, self.foreground_grid, instruction_variance_chance)
                    for instruction in buildInstructions:
                        instruction.setBlock(self.foreground_grid)
                    bg_build_instructions = structure.getBgStructureInstructions(x, y, self.foreground_grid, instruction_variance_chance)
                    for instruction in bg_build_instructions:
                        instruction.setBlock(self.background_grid)

                    # jump x past the end of the structure
                    x += structure.get_width()

                    break
                running_odds_total += structureIdentifier.odds
            
            x += 1

        return 'Initializing Inventory', 50