from world.blocks.block_export import *

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

    multiplier = {
        Iron_Ore_Block: 0.00045,
        Coal_Ore_Block: 0.00021,
        Emerald_Ore_Block: -0.001,
        Diamond_Ore_Block: 0.0009,
        Mabelite_Ore_Block: 0.00015,
        Sulfur_Flakes_Block: -0.001
    }

# elev checks for mountains
class Mountain(Biome):
    def claim(elevation, temp, humidity, mountain):
        if mountain < -10:
            return True
        return False
    
    layers = [Layer(Snow_Block, 1, variation_amp=0), Layer(Gravel, 1), Layer(Rock, 7)]
    sub_layer = Rock

class Ravine(Biome):
    def claim(elevation, temp, humidity, mountain):
        if mountain > 10:
            return True
        return False
    
    layers = [Layer(Gravel, 1), Layer(Rock, 7)]
    sub_layer = Rock


# low humidity
class Desert(Biome):
    def claim(elevation, temp, humidity, mountain):
        if humidity < 0 and temp > 0:
            return True
        return False
    
    layers = [Layer(Sand, 6), Layer(Sand_Stone, 3)]
    sub_layer = Rock

class Tundra(Biome):
    def claim(elevation, temp, humidity, mountain):
        if humidity < 0 and temp < 0 and elevation < 0:
            return True
        return False
    
    layers = [Layer(Rock, 8)]
    sub_layer = Rock

class Glacier(Biome):
    def claim(elevation, temp, humidity, mountain):
        if humidity < 0 and temp < 0 and elevation >= 0:
            return True
        return False
    
    layers = [Layer(Snow_Block, 1, variation_amp=0), Layer(Ice, 8), Layer(Frozen_Rock, 6)]
    sub_layer = Rock

# high humidity
class Rain_Forest(Biome):
    def claim(elevation, temp, humidity, mountain):
        if humidity >= 0 and temp >= 0 and elevation >= 0:
            return True
        return False
    
    layers = [Layer(Grass, 1, variation_amp=0), Layer(Dirt, 3)]
    sub_layer = Rock

class Forest(Biome):
    def claim(elevation, temp, humidity, mountain):
        if humidity >= 0 and temp < 0 and elevation >= 0:
            return True
        return False
    
    layers = [Layer(Grass, 1, variation_amp=0), Layer(Dirt, 3)]
    sub_layer = Rock
    
class Montane_Forest(Biome): # at some point get more gravel to appear here near the surface
    def claim(elevation, temp, humidity, mountain):
        if humidity >= 0 and temp < 0 and elevation < 0:
            return True
        return False
    
    layers = [Layer(Grass, 1, variation_amp=0), Layer(Dirt, 3), Layer(Frozen_Rock, 1)]
    sub_layer = Rock
    

class Plains(Biome):
    def claim(elevation, temp, humidity, mountain):
        if True:
            return True
        return False
    
    layers = [Layer(Grass, 1, variation_amp=0), Layer(Dirt, 4)]
    sub_layer = Rock
