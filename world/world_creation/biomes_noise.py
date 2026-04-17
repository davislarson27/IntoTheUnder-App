from world.blocks.block_export import *

class Layer:
    def __init__(self, block, layer_depth):
        self.block = block
        self.depth = layer_depth


class Biome: # generic template, fall back in case nothing is claimed for some reason, should be last
    def claim(elevation, temp, humidity, mountain): # elevation is the difference from sea level
        return True
    
    layers  = [Layer(Grass, 1), Layer(Dirt, 1)]
    sub_layer = Rock    

# elev checks for mountains
class Mountain(Biome):
    def claim(elevation, temp, humidity, mountain):
        if mountain < -10:
            return True
        return False
    
    layers = [Layer(Snow_Block, 1), Layer(Gravel, 1), Layer(Rock, 7)]
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
    
    layers = [Layer(Snow_Block, 1), Layer(Ice, 8), Layer(Frozen_Rock, 6)]
    sub_layer = Rock

# high humidity
class Lake(Biome): # set water level, any time humidity gets over a threshold near that point it will iterate around itself filling in water maybe
    def claim(elevation, temp, humidity, mountain):
        if humidity >= 0 and temp >= 0 and elevation >= 0:
            return True
        return False
    
    layers = [Layer(Water, 3), Layer(Sand, 3)]
    sub_layer = Rock

class Forest(Biome):
    def claim(elevation, temp, humidity, mountain):
        if humidity >= 0 and temp < 0 and elevation >= 0:
            return True
        return False
    
    layers = [Layer(Grass, 1), Layer(Dirt, 3)]
    sub_layer = Rock
    
class Montane_Forest(Biome):
    def claim(elevation, temp, humidity, mountain):
        if humidity >= 0 and temp < 0 and elevation < 0:
            return True
        return False
    
    layers = [Layer(Grass, 1), Layer(Packed_Dirt, 3), Layer(Frozen_Rock, 1)]
    sub_layer = Rock
    

class Plains(Biome):
    def claim(elevation, temp, humidity, mountain):
        if True:
            return True
        return False
    
    layers = [Layer(Grass, 1), Layer(Dirt, 4)]
    sub_layer = Rock
