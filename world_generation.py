from math import floor
import random

from biomes import *
from blocks import *

class World_Generation:
    def __init__(self, grid, world_width, world_depth):
        self.grid, self.world_width, self.world_depth = grid, world_width, world_depth

        

