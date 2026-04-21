from world.blocks.block_export import *
from noise import pnoise2
import hashlib

class Ore:
    def __init__(self, world_seed, ore, threshold, scale, min_depth):
        def make_seed(base, label):
            return int(hashlib.sha256(f"{base}_{label}".encode()).hexdigest(), 16)

        self.seed = make_seed(world_seed, ore.str_name)
        self.threshold = threshold
        self.scale = scale
        self.min_depth = min_depth

    def find(self, x, y, threshold_adjustment=0, depth_discount=0):
        ore_noise = pnoise2(x * self.scale, y * self.scale,  base=(self.seed) % 256)
        if ore_noise > self.threshold - depth_discount - threshold_adjustment:
            return True
        return False
    