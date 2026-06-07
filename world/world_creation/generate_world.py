import hashlib
from noise import pnoise1, pnoise2

from world.grid import Grid
from .biomes import *
from world.world_creation.structures.structures import *
from .ore import Ore
from .lake_pre_fill import LakePreFill

class Grid_Superstructure:
    def __init__(self, screen, world_generation_settings, world_details, directory='', world_seed=0, spawn_x=0):
        self.world_generation_settings = world_generation_settings
        self.foreground_grid = Grid(world_generation_settings.grid_width, world_generation_settings.grid_depth, world_generation_settings.block_width, screen, f'{directory}/foreground_grid')
        self.background_grid = Grid(world_generation_settings.grid_width, world_generation_settings.grid_depth, world_generation_settings.block_width, screen, f'{directory}/background_grid') 
        
        grid_height = self.foreground_grid.height

        # set seeds
        def make_seed(base, label):
            return int(hashlib.sha256(f"{base}_{label}".encode()).hexdigest(), 16)

        self.seed = world_seed
        self.elev_seed = make_seed(self.seed, 'elevation')
        self.mountain_seed = make_seed(self.seed, 'mountain')
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

        self.border_block_seed = make_seed(self.seed, 'border_block_seed')

        self.biome_priority_order = [Volcano, Mountain, Lake, Ravine, Desert, Tundra, Glacier, Rain_Forest, Forest, Montane_Forest, Plains]

        # amplitutdes of different generators
        self.elevation_amp = 15
        self.mountain_amp = 38
        self.hill_amp = 8
        self.terrain_variation_amp = 2
        self.bg_hill_amp = self.hill_amp
        self.bg_ter_var_amp = self.terrain_variation_amp
        self.border_block_amp = 2

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
        self.border_block_freq = 8

        # thresholds
        self.cave_threshold = 0.66

        self.ores = { # higher scale = smaller veins, higher threshold = less common
            Dirt: Ore(self.seed, Dirt, grid_height, 
                scale=0.11,
                min_depth_threshold=0.5,
                min_depth=10,
                max_depth_threshold=0.51,
            ),
            Gravel: Ore(self.seed, Gravel, grid_height,
                scale=0.11,
                min_depth_threshold=0.5,
                min_depth=10,
                max_depth_threshold=0.52
            ),
            Coal_Ore_Block: Ore(self.seed, Coal_Ore_Block, grid_height,
                scale=0.11,
                min_depth_threshold=0.584,
                min_depth=15,
                max_depth_threshold=0.591
            ),
            Iron_Ore_Block: Ore(self.seed, Iron_Ore_Block, grid_height,
                scale=0.17,
                min_depth_threshold=0.599,
                min_depth=45,
                max_depth_threshold=0.592
            ),
            Gold_Ore_Block: Ore(self.seed, Gold_Ore_Block, grid_height,
                scale=0.18,
                min_depth_threshold=0.705,
                min_depth=88,
                max_depth_threshold=0.672
            ),
            Emerald_Ore_Block: Ore(self.seed, Emerald_Ore_Block, grid_height,
                scale=0.18,
                min_depth_threshold=0.742,
                min_depth=25,
                max_depth_threshold=1,
                max_depth=95
            ),
            Diamond_Ore_Block: Ore(self.seed, Diamond_Ore_Block, grid_height,
                scale=0.18,
                min_depth_threshold=0.785,
                min_depth=95,
                max_depth_threshold=0.77
            ),
            Mabelite_Ore_Block: Ore(self.seed, Mabelite_Ore_Block, grid_height,
                scale=0.17,
                min_depth_threshold=0.814,
                min_depth=110,
                max_depth_threshold=0.8
            ),
            Sulfur_Flakes_Block: Ore(self.seed, Sulfur_Flakes_Block, grid_height,
                scale=0.18,
                min_depth_threshold=0.667,
                min_depth=10,
                max_depth_threshold=1,
                max_depth=80
            ),
        }

        self.saltpeter_chance = 0.025

    def get_grids(self):
        return self.foreground_grid, self.background_grid
    
    def get_hash_chance(self, x, y, need):
        hash = int(hashlib.sha256(f"{self.seed}_{need}_{x}_{y}".encode()).hexdigest(), 16)
        return (hash % 1000) / 1000.0  # value 0.0–1.0

    def get_micro_terrain_height_variation(self, x):
        return pnoise1(x * (1 / self.terrain_variation_freq),  base=(self.terrain_variation_seed) % 256) * self.terrain_variation_amp

    def get_terrain_height(self, x):
        # large = pnoise1( x * freq, base=seed % crunch value) * amp
        base_altitude_level = self.get_base_elevation(x)

        mountain = self.get_mountain_elevation(x)

        hill = pnoise1(x * (1 / self.hill_freq), base=(self.hill_seed) % 256) # more rolling hills
        hill *= abs(hill) * self.hill_amp

        terVar  = self.get_micro_terrain_height_variation(x)

        return int(self.world_generation_settings.ground_level + base_altitude_level + mountain + hill + terVar)
    
    def get_bg_terrain_height(self, x):
        # large = pnoise1( x * freq, base=seed % crunch value) * amp
        base_altitude_level = self.get_base_elevation(x)

        mountain = self.get_mountain_elevation(x) // 3 # keeps some of the mountain noise but stops it from following them  all the way up

        hill = pnoise1(x * (1 / self.bg_hill_freq), base=(self.bg_hill_seed) % 256) # more rolling hills
        hill *= abs(hill) * self.bg_hill_amp

        terVar  = pnoise1(x * (1 / self.bg_ter_var_freq),  base=(self.bg_ter_var_freq) % 256) * self.bg_ter_var_amp  # micro variation

        return int(self.world_generation_settings.ground_level + base_altitude_level + mountain + hill + terVar)
    
    def lake_depth_value(self, x):
        # mountain = self.get_mountain_elevation(x)
        mountain = 0

        hill = pnoise1(x * (1 / self.hill_freq), base=(self.hill_seed) % 256) # more rolling hills
        hill *= abs(hill) * self.hill_amp

        return int(mountain + hill)

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

    def is_cave(self, x, y):
        tunnel = pnoise2(x * self.cave_tunnel_x_freq, y * self.cave_tunnel_y_freq, base=self.cave_tunnel_seed % 256)
        cavern = pnoise2(x * self.cave_cavern_x_freq, y * self.cave_cavern_y_freq, base=self.cave_cavern_seed % 256)

        if tunnel + cavern > self.cave_threshold:
            return True
        return False
    
    def get_humidity(self, x):
        return pnoise1(x * 0.005,  base=(self.humidity_seed) % 256) * 20
    
    def get_border_block_depth(self, x):
        depth  = pnoise1(x * (1 / self.border_block_freq),  base=(self.border_block_seed) % 256) * self.border_block_amp
        return abs(int(depth))

    def generate_world(self):
        for _ in self._generate_world():
            pass

    def _generate_world(self):

        yield 'Pre-Scanning Grid', 0

        # identify lakes and create lake objects
        lakes = [] 
        open_lake_obj = None
        for x in range(self.foreground_grid.width):
            if open_lake_obj is not None and self.get_biome(x) is Lake:
                open_lake_obj.extend_x(x, self.get_terrain_height(x))
            elif open_lake_obj is None and self.get_biome(x) is Lake:
                open_lake_obj = LakePreFill(x, self.get_terrain_height(x))
            elif open_lake_obj is not None:
                open_lake_obj.calculate_lake()
                if open_lake_obj.is_valid_lake(): lakes.append(open_lake_obj)
                open_lake_obj = None
        if open_lake_obj is not None:
            open_lake_obj.calculate_lake()
            if open_lake_obj.is_valid_lake(): lakes.append(open_lake_obj)
            open_lake_obj = None

        yield 'Generating Grid', 3

        # generate the foreground
        for x in range(self.foreground_grid.width): # this will loop through the grid and let me go x by x
            if len(lakes) > 0 and lakes[0] is not None and lakes[0].is_lake(x): # checks for if this is a lake
                lake = lakes[0]
                biome = Lake
                ground_elevation = lake.get_floor_height(x) - abs(int(self.get_micro_terrain_height_variation(x)))
                water_level = lake.get_water_level()
                if lake.is_end_of_lake(x):
                    lakes.pop(0)
            else:
                biome = self.get_biome(x)
                ground_elevation = self.get_terrain_height(x)
                water_level = None

            if water_level is not None:
                for y in range(water_level, ground_elevation):
                    self.foreground_grid.set(x, y, Water)

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
                    if ore_noise.find(x, y, biome.biome_ore_modifier[ore]): # returns True if this ore should be here
                        self.foreground_grid.set(x, y, ore)
                i+=1

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
            for y in range(self.get_terrain_height(x)+2, self.foreground_grid.height):
                if type(self.foreground_grid.get(x, y)) is Water:
                    continue
                if self.is_cave(x, y):
                    block_set = None
                    if self.is_cave(x, y+1) and not self.is_cave(x, y-1): # check if block below is a cave
                        if self.get_hash_chance(x, y, 'saltpeter') < self.saltpeter_chance:
                            block_set = Saltpeter
                    self.foreground_grid.set(x, y, block_set)

        # generate ground level objects & structures for the background
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
                    buildInstructions = structure.getStructureInstructions(x, y, self.background_grid, instruction_variance_chance, biome.__name__)
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
                    buildInstructions = structure.getStructureInstructions(x, y, self.foreground_grid, instruction_variance_chance, biome.__name__)
                    for instruction in buildInstructions:
                        instruction.setBlock(self.foreground_grid)
                    bg_build_instructions = structure.getBgStructureInstructions(x, y, self.foreground_grid, instruction_variance_chance, biome.__name__)
                    for instruction in bg_build_instructions:
                        instruction.setBlock(self.background_grid)

                    # jump x past the end of the structure
                    x += structure.get_width()

                    break
                running_odds_total += structureIdentifier.odds
            
            x += 1

        # now generate the border_block layer
        for x in range(self.foreground_grid.width):
            base_y = self.foreground_grid.height - 1
            self.foreground_grid.set(x, base_y, Border_Block) # sets the bottom block to a border block
            for y in range(base_y - self.get_border_block_depth(x), base_y+1):
                self.foreground_grid.set(x, y, Border_Block) # sets the bottom block to a border block

        for x in range(self.background_grid.width):
            base_y = self.background_grid.height - 1
            self.background_grid.set(x, base_y, Border_Block) # sets the bottom block to a border block
            for y in range(base_y - self.get_border_block_depth(x), base_y+1):
                self.background_grid.set(x, y, Border_Block) # sets the bottom block to a border block


        return 'Initializing Inventory', 50
    