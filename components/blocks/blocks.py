from .block_types._base import *

from .block_types.explosives import *
from .block_types.ingots import *
from .block_types.ingots import *
from .block_types.multiblocks import *
from .block_types.ore_derivatives import *
from .block_types.ores import *
from .block_types.powders import *
from .block_types.special_terrain import *
from .block_types.storage import *
from .block_types.submutliblocks import *
from .block_types.terrain import *
from .block_types.water import *
from .block_types.wood import *

"""
make sure ot add each block to the get_str_to_block() function and add any new files to the import list
"""

def get_str_to_block(): # uses blocks_list to generate dictionary that converts str names to their types
    blocks_list = [
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
        Dirt,
        Grass,
        Log,
        Leaves,
        Sand,
        Gravel,
        Cactus,
        Snow_Block,
        Snow_Man_Head,
        Ice,
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

    blocks_dict = {}
    for block in blocks_list:
        blocks_dict[block.str_name] = block
    return blocks_dict