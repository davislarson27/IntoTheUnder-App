from world.blocks.block_export import *
from noise import pnoise2
import hashlib

class Ore:
    def __init__(self, world_seed, ore, world_height, scale, min_depth_threshold, min_depth, max_depth_threshold, max_depth=None, allow_fill_from=[Rock], biome_limiter=None): # default allow fill is just from rock
        def make_seed(base, label):
            return int(hashlib.sha256(f"{base}_{label}".encode()).hexdigest(), 16)

        self.seed = make_seed(world_seed, ore.str_name)
        self.min_depth_threshold = min_depth_threshold
        self.scale = scale
        self.min_depth = min_depth

        if max_depth is None: max_depth = world_height # adjust the max depth if it is not set to be the true max depth
        self.delta_treshold = (max_depth_threshold - min_depth_threshold) / (max_depth - min_depth)# change in threshold per one block of additional depth
        self.max_depth = max_depth

        self.allow_fill_from = allow_fill_from
        self.biome_limiter = biome_limiter

    def find(self, x, y, biome_multiplier=1):
        ore_noise = pnoise2(x * self.scale, y * self.scale,  base=(self.seed) % 256)
        if ore_noise > (self.min_depth_threshold + ((y - self.min_depth) * self.delta_treshold)) / biome_multiplier:
            return True
        else:
            return False
        
    def allow_replace(self, preexisting_block):
        if preexisting_block is None:
            preexisting_block_type = None
        else:
            preexisting_block_type = type(preexisting_block)
        return preexisting_block_type in self.allow_fill_from
    
    def is_valid_biome(self, cur_biome):
        if self.biome_limiter is None:
            return True
        return cur_biome in self.biome_limiter
