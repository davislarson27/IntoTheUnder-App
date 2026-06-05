from world.blocks.block_export import *
from world.world_creation.structures.structures import *
from world.world_creation.structures.structure_identifier import Structure_Identifier
from .ore import Ore

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
        Gravel: 1,
        Iron_Ore_Block: 1,
        Coal_Ore_Block: 1,
        Gold_Ore_Block: 1,
        Emerald_Ore_Block: 1,
        Diamond_Ore_Block: 1,
        Mabelite_Ore_Block: 1,
        Sulfur_Flakes_Block: 1
    }

    structures = [ # make sure that odds combined do not add up even close to 100 or the whole area will be covered
        Structure_Identifier(Recipe_Burrow, 0.0002),
        Structure_Identifier(Tree, 0.1),
    ]
    bg_structures = [ # make sure that odds combined do not add up even close to 100 or the whole area will be covered
        Structure_Identifier(Tree, 0.1)
    ]


# elev checks for ultra high/low areas
class Volcano(Biome):
    def claim(elevation, temp, humidity, mountain):
        if mountain < -10 and temp > 6:
            return True
        return False
    
    layers = [Layer(Snow_Block, 1, variation_amp=0), Layer(Gravel, 1), Layer(Rock, 7)]
    sub_layer = Rock

    structures = [ # make sure that odds combined do not add up even close to 100 or the whole area will be covered
        Structure_Identifier(Tree, 0.007),
    ]
    bg_structures = [ # make sure that odds combined do not add up even close to 100 or the whole area will be covered
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

    structures = [ # make sure that odds combined do not add up even close to 100 or the whole area will be covered
        Structure_Identifier(Snow_Tree, 0.01),
        Structure_Identifier(Snow_Man_Structure, 0.0001)
    ]
    bg_structures = [ # make sure that odds combined do not add up even close to 100 or the whole area will be covered
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

    structures = [ # make sure that odds combined do not add up even close to 100 or the whole area will be covered
    ]
    bg_structures = [ # make sure that odds combined do not add up even close to 100 or the whole area will be covered
    ]


class Ravine(Biome):
    def claim(elevation, temp, humidity, mountain):
        if mountain > 10:
            return True
        return False
    
    layers = [Layer(Gravel, 1, variation_amp=1), Layer(Rock, 7)]
    sub_layer = Rock

    structures = [ # make sure that odds combined do not add up even close to 100 or the whole area will be covered
        Structure_Identifier(Tree, 0.01),
        Structure_Identifier(Flowers, 0.018)
    ]
    bg_structures = [ # make sure that odds combined do not add up even close to 100 or the whole area will be covered
    ]


# low humidity
class Desert(Biome):
    def claim(elevation, temp, humidity, mountain):
        if humidity < 0 and temp > 0:
            return True
        return False
    
    layers = [Layer(Sand, 6), Layer(Sand_Stone, 3)]
    sub_layer = Rock

    structures = [ # make sure that odds combined do not add up even close to 100 or the whole area will be covered
        Structure_Identifier(Recipe_Burrow, 0.0002),
        Structure_Identifier(Cactus_Structure, 0.05)
    ]
    bg_structures = [ # make sure that odds combined do not add up even close to 100 or the whole area will be covered
        Structure_Identifier(Cactus_Structure, 0.015)
    ]


class Tundra(Biome):
    def claim(elevation, temp, humidity, mountain):
        if humidity < 0 and temp < 0 and elevation < 0:
            return True
        return False
    
    layers = [Layer(Rock, 8)]
    sub_layer = Rock

    structures = [ # make sure that odds combined do not add up even close to 100 or the whole area will be covered
        Structure_Identifier(Recipe_Burrow, 0.0002),
        Structure_Identifier(Small_Bush, 0.05),
        Structure_Identifier(Flowers, 0.015)
    ]
    bg_structures = [ # make sure that odds combined do not add up even close to 100 or the whole area will be covered
    ]


class Glacier(Biome):
    def claim(elevation, temp, humidity, mountain):
        if humidity < 0 and temp < 0 and elevation >= 0:
            return True
        return False
    
    layers = [Layer(Snow_Block, 1, variation_amp=0), Layer(Ice, 8), Layer(Frozen_Rock, 6)]
    sub_layer = Rock

    structures = [ # make sure that odds combined do not add up even close to 100 or the whole area will be covered
        Structure_Identifier(Recipe_Burrow, 0.0002),
        Structure_Identifier(Snow_Man_Structure, 0.006),
        Structure_Identifier(Flowers, 0.001)
    ]
    bg_structures = [ # make sure that odds combined do not add up even close to 100 or the whole area will be covered
    ]


# high humidity
class Rain_Forest(Biome):
    def claim(elevation, temp, humidity, mountain):
        if humidity >= 0 and temp >= 0 and elevation >= 0:
            return True
        return False
    
    layers = [Layer(Grass, 1, variation_amp=0), Layer(Dirt, 3)]
    sub_layer = Rock

    structures = [ # make sure that odds combined do not add up even close to 100 or the whole area will be covered
        Structure_Identifier(Recipe_Burrow, 0.0002),
        Structure_Identifier(Tree, 0.12),
        Structure_Identifier(Small_Bush, 0.02),
        Structure_Identifier(Flowers, 0.03),
    ]
    bg_structures = [ # make sure that odds combined do not add up even close to 100 or the whole area will be covered
        Structure_Identifier(Tree, 0.12)
    ]


class Forest(Biome):
    def claim(elevation, temp, humidity, mountain):
        if humidity >= 0 and temp < 0 and elevation >= 0:
            return True
        return False
    
    layers = [Layer(Grass, 1, variation_amp=0), Layer(Dirt, 3)]
    sub_layer = Rock

    structures = [ # make sure that odds combined do not add up even close to 100 or the whole area will be covered
        Structure_Identifier(Recipe_Burrow, 0.0002),
        Structure_Identifier(Tree, 0.1),
        Structure_Identifier(Small_Bush, 0.01),
        Structure_Identifier(Flowers, 0.028),
    ]
    bg_structures = [ # make sure that odds combined do not add up even close to 100 or the whole area will be covered
        Structure_Identifier(Tree, 0.1)
    ]
    

class Montane_Forest(Biome): # at some point get more gravel to appear here near the surface
    def claim(elevation, temp, humidity, mountain):
        if humidity >= 0 and temp < 0 and elevation < 0:
            return True
        return False
    
    layers = [Layer(Grass, 1, variation_amp=0), Layer(Dirt, 3), Layer(Frozen_Rock, 1)]
    sub_layer = Rock

    structures = [ # make sure that odds combined do not add up even close to 100 or the whole area will be covered
        Structure_Identifier(Recipe_Burrow, 0.0002),
        Structure_Identifier(Tree, 0.028),
        Structure_Identifier(Snow_Tree, 0.002),
        Structure_Identifier(Small_Bush, 0.025),
        Structure_Identifier(Flowers, 0.03)
    ]
    bg_structures = [ # make sure that odds combined do not add up even close to 100 or the whole area will be covered
        Structure_Identifier(Tree, 0.02)
    ]
    

class Plains(Biome):
    def claim(elevation, temp, humidity, mountain):
        if True:
            return True
        return False
    
    layers = [Layer(Grass, 1, variation_amp=0), Layer(Dirt, 4)]
    sub_layer = Rock
    
    structures = [ # make sure that odds combined do not add up even close to 100 or the whole area will be covered
        Structure_Identifier(Recipe_Burrow, 0.0002),
        Structure_Identifier(Tree, 0.02),
        Structure_Identifier(Small_Bush, 0.03),
        Structure_Identifier(Flowers, 0.28)
    ]
    bg_structures = [ # make sure that odds combined do not add up even close to 100 or the whole area will be covered
        Structure_Identifier(Tree, 0.02)
    ]

