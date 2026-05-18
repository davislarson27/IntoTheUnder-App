from .block_types._base import *

from .block_types.explosives import *
from .block_types.ingots import *
from .block_types.multiblocks import *
from .block_types.gems import *
from .block_types.ores import *
from .block_types.powders import *
from .block_types.special_terrain import *
from .block_types.storage import *
from .block_types.terrain import *
from .block_types.water import *
from .block_types.wood import *
from .block_types.resource_blocks import *
from .block_types.bricks import *
from .block_types.glass import *

"""
make sure ot add each block to the get_str_to_block() function and add any new files to the import list
"""

def get_blocks_list():
        return [
        Iron_Ingot,
        Gold_Ingot,
        Rock,
        Iron_Ore_Block,
        Gold_Ore_Block,
        Diamond_Ore_Block,
        Emerald_Ore_Block,
        Mabelite_Ore_Block,
        Coal_Ore_Block,
        Coal,
        Diamond,
        Emerald,
        Mabelite,
        Dirt,
        Packed_Dirt,
        Grass,
        Log,
        Leaves,
        Snow_Leaves,
        Snow_Leaves_Top,
        Sand,
        Sand_Stone,
        Gravel,
        Cactus,
        Snow_Block,
        Snow_Man_Head,
        Ice,
        Packed_Ice,
        Frozen_Rock,
        Chest,
        Door,
        Door_Top,
        Door_Bottom,
        Wood_Planks,
        Saltpeter,
        Saltpeter_Powder,
        Sulfur_Flakes_Block,
        Sulfur_Powder,
        Gunpowder,
        TNT,
        Recipe_Frame,
        Iron_Block,
        Emerald_Block,
        Diamond_Block,
        Coal_Block,
        Gold_Block,
        Mabelite_Block,
        Stone_Bricks,
        Frozen_Stone_Bricks,
        Ice_Bricks,
        Sand_Bricks,
        Iron_Ladder,
        Wood_Ladder,
        Border_Block,
        Glass,
        Water, # water subclasses after this
            Water_R1,
            Water_L1,
            Water_R2,
            Water_L2,
            Water_R3,
            Water_L3,
            Water_R4,
            Water_L4
    ]

def get_block_refuel_dict():
    return {
        Coal: 40,
        Coal_Block: 120,
        Log: 30,
        Wood_Planks: 10,
        Wood_Ladder: 5,
        Door: 5,
        Chest: 30,
        Gunpowder: 50
    }

def get_block_repair_dict():
    return {
        Iron_Ingot: 30,
        Iron_Block: 240,
        Diamond: 70,
        Diamond_Block: 560,
        Mabelite: 100,
        Mabelite_Block: 800
    }
    
def get_block_refuel_values(block_type):
    block_refuel_dict = get_block_refuel_dict()
    if block_type not in block_refuel_dict.keys():
        return 0
    else:
        return block_refuel_dict[block_type]

def get_block_repair_values(block_type):
    block_refuel_dict = get_block_repair_dict()
    if block_type not in block_refuel_dict.keys():
        return 0
    else:
        return block_refuel_dict[block_type]


def get_str_to_block(): # uses blocks_list to generate dictionary that converts str names to their types
    blocks_list = get_blocks_list()

    blocks_dict = {}
    for block in blocks_list:
        blocks_dict[block.str_name] = block
    return blocks_dict