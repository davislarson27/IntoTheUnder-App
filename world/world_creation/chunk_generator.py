import hashlib
from noise import pnoise1, pnoise2

from world.chunk import Chunk
from world.region import Region
from .biomes import *
from world.world_creation.structures.structures import *
from .ore import Ore
from .lake_pre_fill import LakePreFill

class Chunk_Generator:
    def __init__(self, screen, chunk_width, world_details, directory=''):
        self.world_details = world_details
        # self.foreground_grid = Grid(world_details.grid_width, world_details.world_height, world_details.block_width, screen, f'{directory}/foreground_grid')
        # self.background_grid = Grid(world_details.grid_width, world_details.world_height, world_details.block_width, screen, f'{directory}/background_grid')

        self.chunk_width = chunk_width
        grid_height = world_details.world_height
        self.screen = screen
        self.directory = directory

        self.terrain_heights_by_x = []
        self.bg_terrain_heights_by_x = []
        self.biomes_by_x = []

        # set seeds
        def make_seed(base, label):
            return int(hashlib.sha256(f"{base}_{label}".encode()).hexdigest(), 16)

        self.seed = world_details.world_seed
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

        self.biome_priority_order = [Volcano, Mountain, Lake, Ravine, Desert, Tundra, Glacier, Rain_Forest, Spruce_Forest, Forest, Montane_Forest, Plains]

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
                min_depth_threshold=0.51,
                min_depth=10,
                max_depth_threshold=0.52,
            ),
            Packed_Dirt: Ore(self.seed, Packed_Dirt, grid_height, # this should go after dirt is inserted
                scale=0.11,
                min_depth_threshold=0.77,
                min_depth=30,
                max_depth_threshold=0.755,
                allow_fill_from=[Dirt, Grass]
            ),
            Gravel: Ore(self.seed, Gravel, grid_height,
                scale=0.11,
                min_depth_threshold=0.525,
                min_depth=10,
                max_depth_threshold=0.545,
                allow_fill_from=[Rock, Ice, Snow_Block, Dirt, Grass, Frozen_Rock]
            ),
            Ice: Ore(self.seed, Ice, grid_height,
                scale=0.11,
                min_depth_threshold=0.51,
                min_depth=10,
                max_depth_threshold=0.58,
                allow_fill_from=[Rock, Frozen_Rock],
                biome_limiter=[Glacier]
            ),
            Frozen_Rock: Ore(self.seed, Frozen_Rock, grid_height,
                scale=0.12,
                min_depth_threshold=0.57,
                min_depth=10,
                max_depth_threshold=0.54,
                biome_limiter=[Glacier, Montane_Forest]
            ),
            Coal_Ore_Block: Ore(self.seed, Coal_Ore_Block, grid_height,
                scale=0.11,
                min_depth_threshold=0.574,
                min_depth=15,
                max_depth_threshold=0.6
            ),
            Iron_Ore_Block: Ore(self.seed, Iron_Ore_Block, grid_height,
                scale=0.17,
                min_depth_threshold=0.596,
                min_depth=45,
                max_depth_threshold=0.59
            ),
            Gold_Ore_Block: Ore(self.seed, Gold_Ore_Block, grid_height,
                scale=0.18,
                min_depth_threshold=0.685,
                min_depth=88,
                max_depth_threshold=0.659
            ),
            Emerald_Ore_Block: Ore(self.seed, Emerald_Ore_Block, grid_height,
                scale=0.18,
                min_depth_threshold=0.72,
                min_depth=35,
                max_depth_threshold=0.77,
                max_depth=95
            ),
            Diamond_Ore_Block: Ore(self.seed, Diamond_Ore_Block, grid_height,
                scale=0.18,
                min_depth_threshold=0.779,
                min_depth=95,
                max_depth_threshold=0.745
            ),
            Mabelite_Ore_Block: Ore(self.seed, Mabelite_Ore_Block, grid_height,
                scale=0.19,
                min_depth_threshold=0.797,
                min_depth=105,
                max_depth_threshold=0.7742
            ),
            Sulfur_Flakes_Block: Ore(self.seed, Sulfur_Flakes_Block, grid_height,
                scale=0.18,
                min_depth_threshold=0.665,
                min_depth=10,
                max_depth_threshold=0.71,
                max_depth=80
            ),
        }

        self.saltpeter_chance = 0.025
    
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

        return int(self.world_details.ground_level + base_altitude_level + mountain + hill + terVar)
    
    def get_bg_terrain_height(self, x):
        # large = pnoise1( x * freq, base=seed % crunch value) * amp
        base_altitude_level = self.get_base_elevation(x)

        mountain = self.get_mountain_elevation(x) // 3 # keeps some of the mountain noise but stops it from following them  all the way up

        hill = pnoise1(x * (1 / self.bg_hill_freq), base=(self.bg_hill_seed) % 256) # more rolling hills
        hill *= abs(hill) * self.bg_hill_amp

        terVar  = pnoise1(x * (1 / self.bg_ter_var_freq),  base=(self.bg_ter_var_freq) % 256) * self.bg_ter_var_amp  # micro variation

        return int(self.world_details.ground_level + base_altitude_level + mountain + hill + terVar)
    
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
        if x > 0: # prevents 1 block wide biomes in the middle of another biome
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

    def get_biome_pregen(self, x):
        if x < len(self.biomes_by_x):
            return self.biomes_by_x[x]
        return self.get_biome(x)
    
    def get_terrain_height_pregen(self, x):
        if x < len(self.terrain_heights_by_x):
            return self.terrain_heights_by_x[x]
        return self.get_terrain_height(x)
    
    def get_bg_terrain_height_pregen(self, x):
        if x < len(self.bg_terrain_heights_by_x):
            return self.bg_terrain_heights_by_x[x]
        return self.get_bg_terrain_height(x)
        

    def generate_fg_region(self, region_id: int) -> Region:
        # get region offset
        x_offset: int = Region.get_x_offset(region_id)

        biomes = []
        elevations = []
        structures = []
        underground_structures = []

        # generate relevant details
        end_range = x_offset+Region.get_region_width()
        for x in range(x_offset, end_range): # this will loop through the grid and let me go x by x
            biome = self.get_biome_pregen(x)
            biomes.append(biome)
            elevation = self.get_terrain_height_pregen(x)
            elevations.append(elevation)

            structure_list_attr_value = "fg_chunk_structures"
            hash = int(hashlib.sha256(f"{self.seed}_{structure_list_attr_value}_fg_struct_{x}".encode()).hexdigest(), 16)
            structure_odds = (hash % 1000) / 1000.0

            # get structure to generate based on biome
            running_odds_total = 0
            structure = None
            hold_x_until = 0
            if x > hold_x_until:
                for structureIdentifier in getattr(biome, structure_list_attr_value):
                    if structureIdentifier.odds + running_odds_total > structure_odds:
                        end_of_structure = x + structureIdentifier.structure.get_width()
                        if end_of_structure < end_range:
                            structure = structureIdentifier.structure
                            hold_x_until = end_of_structure # jump x past the end of the structure
                            break
                    running_odds_total += structureIdentifier.odds
            structures.append(structure)

        return Region(self.directory, region_id, Chunk.chunk_width, biomes, elevations, structures, underground_structures)

    def generate_bg_region(self, region_id: int) -> Region:
        x_offset: int = Region.get_x_offset(region_id)

        biomes = []
        elevations = []
        structures = []
        underground_structures = []

        # generate relevant details
        for x in range(x_offset, x_offset+Region.get_region_width()): # this will loop through the grid and let me go x by x
            biome = self.get_biome_pregen(x)
            biomes.append(biome)
            elevation = self.get_bg_terrain_height_pregen(x)
            elevations.append(elevation)

            # structure_list_attr_value = "structures"
            # hash = int(hashlib.sha256(f"{self.seed}_{structure_list_attr_value}_fg_struct_{x}".encode()).hexdigest(), 16)
            # structure_odds = (hash % 1000) / 1000.0

            # # subStructure_hash = int(hashlib.sha256(f"{self.seed}_{structure_list_attr_value}_sub_struct_{x}".encode()).hexdigest(), 16)
            # # instruction_variance_chance = (subStructure_hash % 1000) / 1000.0

            # # get structure to generate based on biome
            # running_odds_total = 0
            # structure = None
            # hold_x_until = 0
            # if x < hold_x_until:
            #     for structureIdentifier in getattr(biome, structure_list_attr_value):
            #         if structureIdentifier.odds + running_odds_total > structure_odds:
            #             structure = structureIdentifier.structure
            #             # structures.append(structure) # assign structure
            #             hold_x_until = x + structure.get_width() # jump x past the end of the structure
            #             break
            #         running_odds_total += structureIdentifier.odds
            # structures.append(structure)

        return Region(self.directory, region_id, Chunk.chunk_width, biomes, elevations, structures, underground_structures)


    def generate_fg_chunk_using_region(self, grid, region, chunk_id) -> Chunk:
        """generates and returns a foreground chunk based on an id and region"""
        fg_chunk = Chunk(Chunk.chunk_width, self.world_details.world_height, self.world_details.block_width, self.screen)
        global_x_start = fg_chunk.get_x_offset(chunk_id)

        # helper functions
        def _generate_ores_at_x(x, biome, ground_elevation, chunk, x_offset):
            for ore in self.ores:
                ore_spawn_attributes = self.ores[ore]
                if not ore_spawn_attributes.is_valid_biome(biome):
                    continue
                for y in range(ground_elevation, chunk.height):
                    if y < ore_spawn_attributes.min_depth:
                        continue
                    if y >= ore_spawn_attributes.max_depth:
                        continue

                    if ore_spawn_attributes.find(x+x_offset, y, biome.biome_ore_modifier[ore]): # returns True if this ore should be here
                        if ore_spawn_attributes.allow_replace(chunk.get(x, y)):
                            chunk.set(x, y, ore, x_offset=x_offset, grid=grid)

        def _generate_structures(global_x_start, chunk):
            x = 0
            while x < fg_chunk.width:
                structure_type = region.get_structure(x, chunk_id)
                if structure_type is None:
                    x += 1
                    continue

                # get seed based random number (hashed based on x)
                structure_list_attr_value = "fg_chunk_structures"
                subStructure_hash = int(hashlib.sha256(f"{self.seed}_{structure_list_attr_value}_sub_struct_{x}".encode()).hexdigest(), 16)
                instruction_variance_chance = (subStructure_hash % 1000) / 1000.0

                base_start_x = structure_type.get_x_for_start_y(x, instruction_variance_chance)
                structure = structure_type(instruction_variance_chance, x, region.get_elevation(base_start_x, chunk_id), grid, chunk, global_x_start)
                
                col_num = 0
                while x < fg_chunk.width and col_num < structure.get_width():
                    structure.set_fg_col(col_num, region.get_elevation(x, chunk_id))
                    x+=1
                    col_num+=1
                
        # generate the foreground chunk
        for x in range(fg_chunk.width): # this will loop through the grid and let me go x by x
            biome = region.get_biome(x, chunk_id)
            ground_elevation = region.get_elevation(x, chunk_id)
            cur_depth_down = ground_elevation
            
            layer_num = 0
            for layer in biome.layers:
                for y in range(cur_depth_down, layer.depth+cur_depth_down):
                    fg_chunk.set(x, y, layer.block, x_offset=global_x_start, grid=grid)
                variation = self.get_layer_increment(x+global_x_start, layer_num, layer)
                cur_depth_down += layer.depth
                for y in range(cur_depth_down, cur_depth_down+variation):
                    fg_chunk.set(x, y, layer.block, x_offset=global_x_start, grid=grid)
                cur_depth_down += variation
                layer_num+=1
            for y in range(cur_depth_down, fg_chunk.height):
                fg_chunk.set(x, y, biome.sub_layer, x_offset=global_x_start, grid=grid)

            # generate ores at cur x
            _generate_ores_at_x(x, biome, ground_elevation, fg_chunk, global_x_start)

            # generate caves
            for y in range(self.get_terrain_height_pregen(x+global_x_start)+2, fg_chunk.height):
                if type(fg_chunk.get(x, y)) is Water:
                    continue
                if self.is_cave(x+global_x_start, y):
                    block_set = None
                    if self.is_cave(x+global_x_start, y+1) and not self.is_cave(x+global_x_start, y-1): # check if block below is a cave
                        if self.get_hash_chance(x+global_x_start, y, 'saltpeter') < self.saltpeter_chance:
                            block_set = Saltpeter
                    fg_chunk.set(x, y, block_set, x_offset=global_x_start, grid=grid)

            # generate structures
            _generate_structures(global_x_start, fg_chunk)

        return fg_chunk

    def generate_bg_chunk_using_region(self, grid, region, chunk_id) -> Chunk:
        """generates and returns a foreground chunk based on an id and region"""
        fg_chunk = Chunk(Chunk.chunk_width, self.world_details.world_height, self.world_details.block_width, self.screen)
        global_x_start = fg_chunk.get_x_offset(chunk_id)

        # generate the foreground chunk
        for x in range(fg_chunk.width): # this will loop through the grid and let me go x by x
            biome = region.get_biome(x, chunk_id)
            ground_elevation = region.get_elevation(x, chunk_id)
            cur_depth_down = ground_elevation
            
            layer_num = 0
            for layer in biome.layers:
                for y in range(cur_depth_down, layer.depth+cur_depth_down):
                    fg_chunk.set(x, y, layer.block, x_offset=global_x_start, grid=grid)
                variation = self.get_layer_increment(x+global_x_start, layer_num, layer)
                cur_depth_down += layer.depth
                for y in range(cur_depth_down, cur_depth_down+variation):
                    fg_chunk.set(x, y, layer.block, x_offset=global_x_start, grid=grid)
                cur_depth_down += variation
                layer_num+=1
            for y in range(cur_depth_down, fg_chunk.height):
                fg_chunk.set(x, y, biome.sub_layer, x_offset=global_x_start, grid=grid)

        return fg_chunk

