from world.blocks.block_export import *
from world.world_creation.structures.structures import *
from world.world_creation.structures.structure_identifier import Structure_Identifier

class Layer:
    def __init__(self, block, layer_depth, variation_amp=2, variation_freq=6):
        self.block = block
        self.depth = layer_depth
        self.variation_amp = variation_amp
        self.variation_freq = variation_freq


class Biome: # generic template, fall back in case nothing is claimed for some reason, should be last
    def claim(elevation, temp, humidity, mountain): # elevation is the difference from sea level
        return True
    
    layers  = [Layer(Grass, 1, variation_amp=0), Layer(Dirt, 1)]
    sub_layer = Rock

    biome_ore_modifier = {
        Dirt: 1,
        Packed_Dirt: 1,
        Gravel: 1,
        Ice: 1,
        Frozen_Rock: 1,
        Iron_Ore_Block: 1,
        Coal_Ore_Block: 1,
        Gold_Ore_Block: 1,
        Emerald_Ore_Block: 1,
        Diamond_Ore_Block: 1,
        Mabelite_Ore_Block: 1,
        Sulfur_Flakes_Block: 1,
    }

    fg_chunk_structures = [
        Structure_Identifier(Col_Recipe_Burrow, 0.0002),
        Structure_Identifier(Col_Tree, 0.1),
    ]
    bg_chunk_structures = [
        Structure_Identifier(Col_Tree, 0.1),
    ]
    underground_fg_chunk_structures = [
        Structure_Identifier(Col_Recipe_Cave, 0.0015),
    ]


# elev checks for ultra high/low areas
class Volcano(Biome):
    def claim(elevation, temp, humidity, mountain):
        if mountain < -10 and temp > 6:
            return True
        return False
    
    layers = [Layer(Snow_Block, 1, variation_amp=0), Layer(Gravel, 1), Layer(Rock, 7)]
    sub_layer = Rock

    fg_chunk_structures = [
        Structure_Identifier(Col_Tree, 0.007),
        Structure_Identifier(Col_Recipe_Burrow, 0.00001),
    ]
    bg_chunk_structures = [
    ]

    biome_ore_modifier = {**Biome.biome_ore_modifier}
    biome_ore_modifier[Sulfur_Flakes_Block] *= 1.5


class Mountain(Biome):
    def claim(elevation, temp, humidity, mountain):
        if mountain < -10:
            return True
        return False
    
    layers = [Layer(Snow_Block, 1, variation_amp=1), Layer(Gravel, 1), Layer(Rock, 7)]
    sub_layer = Rock

    fg_chunk_structures = [ # make sure that odds combined do not add up even close to 100 or the whole area will be covered
        Structure_Identifier(Col_Snow_Tree, 0.01),
        Structure_Identifier(Col_Snow_Man_Structure, 0.0001),
        Structure_Identifier(Col_Watermellon_Patch, 0.00005),
    ]
    bg_chunk_structures = [ # make sure that odds combined do not add up even close to 100 or the whole area will be covered
    ]

    biome_ore_modifier = {**Biome.biome_ore_modifier}
    biome_ore_modifier[Sulfur_Flakes_Block] *= 1.4

class Lake(Biome):
    def claim(elevation, temp, humidity, mountain):
        if temp > 6 and humidity > 6:
            return True
        return False
        
    layers = [Layer(Sand, 2, variation_amp=3), Layer(Sand_Stone, 3)]
    sub_layer = Rock

    fg_chunk_structures = [ # make sure that odds combined do not add up even close to 100 or the whole area will be covered
    ]
    bg_chunk_structures = [ # make sure that odds combined do not add up even close to 100 or the whole area will be covered
    ]


class Ravine(Biome):
    def claim(elevation, temp, humidity, mountain):
        if mountain > 10:
            return True
        return False
    
    layers = [Layer(Gravel, 1, variation_amp=1), Layer(Rock, 7)]
    sub_layer = Rock

    fg_chunk_structures = [ # make sure that odds combined do not add up even close to 100 or the whole area will be covered
        Structure_Identifier(Col_Tree, 0.01),
        Structure_Identifier(Col_Wild_Flower_Struct, 0.018),
        Structure_Identifier(Col_Watermellon_Patch, 0.00005),
    ]
    bg_chunk_structures = [ # make sure that odds combined do not add up even close to 100 or the whole area will be covered
    ]

# low humidity
class Desert(Biome):
    def claim(elevation, temp, humidity, mountain):
        if humidity < 0 and temp > 0:
            return True
        return False
    
    layers = [Layer(Sand, 6), Layer(Sand_Stone, 3)]
    sub_layer = Rock

    fg_chunk_structures = [ # make sure that odds combined do not add up even close to 100 or the whole area will be covered
        Structure_Identifier(Col_Recipe_Burrow, 0.0002),
        Structure_Identifier(Col_Cactus_Structure, 0.05),
    ]
    bg_chunk_structures = [ # make sure that odds combined do not add up even close to 100 or the whole area will be covered
        Structure_Identifier(Col_Cactus_Structure, 0.002),
    ]


class Tundra(Biome):
    def claim(elevation, temp, humidity, mountain):
        if humidity < 0 and temp < 0 and elevation < 0:
            return True
        return False
    
    layers = [Layer(Rock, 8)]
    sub_layer = Rock

    fg_chunk_structures = [ # make sure that odds combined do not add up even close to 100 or the whole area will be covered
        Structure_Identifier(Col_White_Lily_Struct, 0.015),
        Structure_Identifier(Col_Watermellon_Patch, 0.025),
        Structure_Identifier(Col_Recipe_Burrow, 0.0002),
        Structure_Identifier(Col_Small_Bush, 0.02),
    ]
    bg_chunk_structures = [ # make sure that odds combined do not add up even close to 100 or the whole area will be covered
    ]
    

class Glacier(Biome):
    def claim(elevation, temp, humidity, mountain):
        if humidity < 0 and temp < 0 and elevation >= 0:
            return True
        return False
    
    layers = [Layer(Snow_Block, 1, variation_amp=0), Layer(Ice, 8), Layer(Frozen_Rock, 6)]
    sub_layer = Rock

    fg_chunk_structures = [ # make sure that odds combined do not add up even close to 100 or the whole area will be covered
        Structure_Identifier(Col_Recipe_Burrow, 0.0002),
        Structure_Identifier(Col_Snow_Man_Structure, 0.006),
        Structure_Identifier(Col_Rose_Struct, 0.001),
    ]
    bg_chunk_structures = [ # make sure that odds combined do not add up even close to 100 or the whole area will be covered
    ]

# high humidity
class Rain_Forest(Biome):
    def claim(elevation, temp, humidity, mountain):
        if humidity >= 0 and temp >= 0 and elevation >= 0:
            return True
        return False
    
    layers = [Layer(Grass, 1, variation_amp=0), Layer(Dirt, 3)]
    sub_layer = Rock

    fg_chunk_structures = [ # make sure that odds combined do not add up even close to 100 or the whole area will be covered
        Structure_Identifier(Col_Recipe_Burrow, 0.0002),
        Structure_Identifier(Col_Mahogany_Tree, 0.12),
        Structure_Identifier(Col_Tree, 0.02),
        Structure_Identifier(Col_Small_Bush, 0.02),
        Structure_Identifier(Col_Puddle, 0.01),
        Structure_Identifier(Col_Watermellon_Patch, 0.02),
        Structure_Identifier(Col_Wild_Flower_Struct, 0.0025),
        Structure_Identifier(Col_White_Lily_Struct, 0.0025),
        Structure_Identifier(Col_Forget_Me_Not_Struct, 0.0025),
        Structure_Identifier(Col_Rose_Struct, 0.0042),
    ]
    bg_chunk_structures = [ # make sure that odds combined do not add up even close to 100 or the whole area will be covered
        Structure_Identifier(Col_Mahogany_Tree, 0.17),
        Structure_Identifier(Col_Tree, 0.01),
    ]

class Spruce_Forest(Biome):
    def claim(elevation, temp, humidity, mountain):
        if humidity >= 0 and temp < -1 and elevation >= 0:
            return True
        return False
    
    layers = [Layer(Grass, 1, variation_amp=0), Layer(Dirt, 3)]
    sub_layer = Rock

    fg_chunk_structures = [ # make sure that odds combined do not add up even close to 100 or the whole area will be covered
        Structure_Identifier(Col_Recipe_Burrow, 0.0002),
        Structure_Identifier(Col_Spruce_Tree, 0.07),
        Structure_Identifier(Col_Small_Bush, 0.01),
        Structure_Identifier(Col_Wild_Flower_Struct, 0.007),
        Structure_Identifier(Col_White_Lily_Struct, 0.007),
        Structure_Identifier(Col_Forget_Me_Not_Struct, 0.007),
        Structure_Identifier(Col_Rose_Struct, 0.007),
    ]
    bg_chunk_structures = [ # make sure that odds combined do not add up even close to 100 or the whole area will be covered
        Structure_Identifier(Col_Spruce_Tree, 0.065),
    ]

class Forest(Biome):
    def claim(elevation, temp, humidity, mountain):
        if humidity >= 0 and temp < 0 and elevation >= 0:
            return True
        return False
    
    layers = [Layer(Grass, 1, variation_amp=0), Layer(Dirt, 3)]
    sub_layer = Rock
    
    fg_chunk_structures = [ # make sure that odds combined do not add up even close to 100 or the whole area will be covered
        Structure_Identifier(Col_Recipe_Burrow, 0.0002),
        Structure_Identifier(Col_Tree, 0.1),
        Structure_Identifier(Col_Small_Bush, 0.01),
        Structure_Identifier(Col_Mahogany_Tree, 0.00001),
        Structure_Identifier(Col_Wild_Flower_Struct, 0.007),
        Structure_Identifier(Col_White_Lily_Struct, 0.007),
        Structure_Identifier(Col_Forget_Me_Not_Struct, 0.007),
        Structure_Identifier(Col_Rose_Struct, 0.007),
    ]
    bg_chunk_structures = [ # make sure that odds combined do not add up even close to 100 or the whole area will be covered
        Structure_Identifier(Col_Tree, 0.1),
    ]

class Montane_Forest(Biome): # at some point get more gravel to appear here near the surface
    def claim(elevation, temp, humidity, mountain):
        if humidity >= 0 and temp < 0 and elevation < 0:
            return True
        return False
    
    layers = [Layer(Grass, 1, variation_amp=0), Layer(Dirt, 3), Layer(Frozen_Rock, 1)]
    sub_layer = Rock
    
    fg_chunk_structures = [ # make sure that odds combined do not add up even close to 100 or the whole area will be covered
        Structure_Identifier(Col_Recipe_Burrow, 0.0002),
        Structure_Identifier(Col_Tree, 0.028),
        Structure_Identifier(Col_Snow_Tree, 0.002),
        Structure_Identifier(Col_Small_Bush, 0.025),
        Structure_Identifier(Col_Puddle, 0.012),
        Structure_Identifier(Col_Spruce_Tree, 0.0003),
        Structure_Identifier(Col_White_Lily_Struct, 0.014),
        Structure_Identifier(Col_Rose_Struct, 0.0014),
    ]
    bg_chunk_structures = [ # make sure that odds combined do not add up even close to 100 or the whole area will be covered
        Structure_Identifier(Col_Tree, 0.019)
    ]


class Plains(Biome):
    def claim(elevation, temp, humidity, mountain):
        if True:
            return True
        return False
    
    layers = [Layer(Grass, 1, variation_amp=0), Layer(Dirt, 4)]
    sub_layer = Rock
    
    fg_chunk_structures = [ # make sure that odds combined do not add up even close to 100 or the whole area will be covered
        Structure_Identifier(Col_Recipe_Burrow, 0.0002),
        Structure_Identifier(Col_Tree, 0.02),
        Structure_Identifier(Col_Small_Bush, 0.03),
        Structure_Identifier(Col_Wild_Flower_Struct, 0.0065),
        Structure_Identifier(Col_White_Lily_Struct, 0.0065),
        Structure_Identifier(Col_Forget_Me_Not_Struct, 0.0065),
        Structure_Identifier(Col_Rose_Struct, 0.0065),
    ]
    bg_chunk_structures = [ # make sure that odds combined do not add up even close to 100 or the whole area will be covered
        Structure_Identifier(Col_Tree, 0.02)
    ]
