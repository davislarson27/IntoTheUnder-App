from math import floor
import hashlib

from world.blocks.block_export import *
from .structure_instruction import Structure_Instruction, Var_Structure_Instruction
from play.inventory.submenus.crafting_recipes import User_Crafting_Recipes_List
from .chest_loot import Chest_Loot, Loot_Odds

class Recipe_Burrow:
    width = 8
    start_x_diff = -1 # distance from the origin x that the y elevation should be set to
    height = 3
    depth = 2

    def __init__(self):
        pass

    @classmethod
    def get_width(cls):
        return cls.width
    
    @classmethod
    def get_x_difference_for_y(cls):
        """returns the value to add to x to get the corect elevation this object is calcualated for (i.e., for a tree it would be +1)"""
        return cls.start_x_diff
    
    @classmethod
    def get_height(cls):
        """gets height above the start point"""
        return cls.height

    @classmethod
    def get_depth(cls):
        """gets depth below the start point"""
        return cls.depth

    @classmethod
    def getStructureInstructions(cls, ground_x, ground_y, grid, random_factor=0, biome_name=None):
        """takes top left block coordinates and returns list of coordinates and a list of blocks to access in the same order"""
        # initialize list
        structureInstructionsList = []

        # shift start_y up to true start
        start_x = ground_x
        start_y = ground_y - cls.height
        
        # now fill the list with the structure by iterating through each x level
        bottom_y_add = 3
        top_y_add = 0
        for x in range(1):
            structureInstructionsList.append(Structure_Instruction(start_x + x, start_y, Wood_Planks))
            structureInstructionsList.append(Structure_Instruction(start_x + x, start_y + 1, Door_Top))
            structureInstructionsList.append(Structure_Instruction(start_x + x, start_y + 2, Door_Bottom))
            structureInstructionsList.append(Structure_Instruction(start_x + x, start_y + bottom_y_add, Wood_Planks))
        for x in range(1, 2):
            structureInstructionsList.append(Structure_Instruction(start_x + x, start_y, Wood_Planks))
            structureInstructionsList.append(Structure_Instruction(start_x + x, start_y + bottom_y_add, Wood_Planks))
            for y in range(start_y + top_y_add + 1, start_y + bottom_y_add): # clear out inside
                structureInstructionsList.append(Structure_Instruction(start_x + x, y, None))
        for x in range(2, 4):
            structureInstructionsList.append(Structure_Instruction(start_x + x, start_y, Wood_Planks))
            structureInstructionsList.append(Structure_Instruction(start_x + x, start_y + bottom_y_add, Wood_Planks))
            structureInstructionsList.append(Structure_Instruction(start_x + x, start_y + bottom_y_add + 1, Wood_Planks))
            for y in range(start_y + top_y_add + 1, start_y + bottom_y_add): # clear out inside
                structureInstructionsList.append(Structure_Instruction(start_x + x, y, None))
            bottom_y_add += 1
        for x in range(4, 6):
            structureInstructionsList.append(Structure_Instruction(start_x + x, start_y + top_y_add, Wood_Planks))
            structureInstructionsList.append(Structure_Instruction(start_x + x, start_y + top_y_add + 1, Wood_Planks))
            structureInstructionsList.append(Structure_Instruction(start_x + x, start_y + bottom_y_add, Wood_Planks))
            for y in range(start_y + top_y_add + 2, start_y + bottom_y_add): # clear out inside
                structureInstructionsList.append(Structure_Instruction(start_x + x, y, None))
            top_y_add += 1
        for x in range(6, 8):
            structureInstructionsList.append(Structure_Instruction(start_x + x, start_y + top_y_add, Wood_Planks))
            structureInstructionsList.append(Structure_Instruction(start_x + x, start_y + bottom_y_add, Wood_Planks))
            for y in range(start_y + top_y_add + 1, start_y + bottom_y_add): # clear out inside
                structureInstructionsList.append(Structure_Instruction(start_x + x, y, None))
        for x in range(8, 9):
            structureInstructionsList.append(Structure_Instruction(start_x + x, start_y + top_y_add, Wood_Planks))
            structureInstructionsList.append(Structure_Instruction(start_x + x, start_y + top_y_add + 1, Wood_Planks))
            structureInstructionsList.append(Structure_Instruction(start_x + x, start_y + top_y_add + 2, Wood_Planks))
            structureInstructionsList.append(Structure_Instruction(start_x + x, start_y + bottom_y_add, Wood_Planks))

        # now add the recipe frame block
        recipeFrame_x, recipeFrame_y = start_x + 6, start_y + bottom_y_add - 1
        recipeFrameBlock = Recipe_Frame(grid, grid.screen, recipeFrame_x, recipeFrame_y, grid.BLOCK_WIDTH)

        recipeList = User_Crafting_Recipes_List.getBiomeWeightedFindableRecipesList(biome_name)

        index = int(random_factor * len(recipeList)) % len(recipeList)
        randomRecipe = recipeList[index]
        recipeFrameBlock.stored_inventory_items.append(randomRecipe)
        structureInstructionsList.append(Structure_Instruction(recipeFrame_x, recipeFrame_y, recipeFrameBlock, blockIsInitialized=True))

        # return list
        return structureInstructionsList, []

    @classmethod
    def getBgStructureInstructions(cls, ground_x, ground_y, grid, random_factor=0, biome_name=None): # needs to actually reflect the background
        """takes top left block coordinates and returns list of coordinates and a list of blocks to access in the same order"""
        # initialize list
        structureInstructionsList = []

        # shift start_y up to true start
        start_x = ground_x
        start_y = ground_y - cls.height
        
        # now fill the list with the structure by iterating through each x level
        bottom_y_add = 3
        top_y_add = 0
        for x in range(1):
            structureInstructionsList.append(Structure_Instruction(start_x + x, start_y, Wood_Planks))
            structureInstructionsList.append(Structure_Instruction(start_x + x, start_y + 1, Wood_Planks))
            structureInstructionsList.append(Structure_Instruction(start_x + x, start_y + 2, Wood_Planks))
            structureInstructionsList.append(Structure_Instruction(start_x + x, start_y + bottom_y_add, Wood_Planks))
        for x in range(1, 2):
            structureInstructionsList.append(Structure_Instruction(start_x + x, start_y, Wood_Planks))
            structureInstructionsList.append(Structure_Instruction(start_x + x, start_y + bottom_y_add, Wood_Planks))
            for y in range(start_y + top_y_add + 1, start_y + bottom_y_add): # clear out inside
                structureInstructionsList.append(Structure_Instruction(start_x + x, y, Wood_Planks))
        for x in range(2, 4):
            structureInstructionsList.append(Structure_Instruction(start_x + x, start_y, Wood_Planks))
            structureInstructionsList.append(Structure_Instruction(start_x + x, start_y + bottom_y_add, Wood_Planks))
            structureInstructionsList.append(Structure_Instruction(start_x + x, start_y + bottom_y_add + 1, Wood_Planks))
            for y in range(start_y + top_y_add + 1, start_y + bottom_y_add): # clear out inside
                structureInstructionsList.append(Structure_Instruction(start_x + x, y, Wood_Planks))
            bottom_y_add += 1
        for x in range(4, 6):
            structureInstructionsList.append(Structure_Instruction(start_x + x, start_y + top_y_add, Wood_Planks))
            structureInstructionsList.append(Structure_Instruction(start_x + x, start_y + top_y_add + 1, Wood_Planks))
            structureInstructionsList.append(Structure_Instruction(start_x + x, start_y + bottom_y_add, Wood_Planks))
            for y in range(start_y + top_y_add + 2, start_y + bottom_y_add): # clear out inside
                structureInstructionsList.append(Structure_Instruction(start_x + x, y, Wood_Planks))
            top_y_add += 1
        for x in range(6, 8):
            structureInstructionsList.append(Structure_Instruction(start_x + x, start_y + top_y_add, Wood_Planks))
            structureInstructionsList.append(Structure_Instruction(start_x + x, start_y + bottom_y_add, Wood_Planks))
            for y in range(start_y + top_y_add + 1, start_y + bottom_y_add): # clear out inside
                structureInstructionsList.append(Structure_Instruction(start_x + x, y, Wood_Planks))
        for x in range(8, 9):
            structureInstructionsList.append(Structure_Instruction(start_x + x, start_y + top_y_add, Wood_Planks))
            structureInstructionsList.append(Structure_Instruction(start_x + x, start_y + top_y_add + 1, Wood_Planks))
            structureInstructionsList.append(Structure_Instruction(start_x + x, start_y + top_y_add + 2, Wood_Planks))
            structureInstructionsList.append(Structure_Instruction(start_x + x, start_y + bottom_y_add, Wood_Planks))

        # now add the recipe frame block
        recipeFrame_x, recipeFrame_y = start_x + 6, start_y + bottom_y_add - 1
        structureInstructionsList.append(Structure_Instruction(recipeFrame_x, recipeFrame_y, Wood_Planks))

        # return list
        return structureInstructionsList, []


class Recipe_Cave:
    width = 6
    start_x_diff = -1 # distance from the origin x that the y elevation should be set to
    height = 5
    depth = 0

    chest_loot = Chest_Loot([
        Loot_Odds(Rose, 3, 0.025),
        Loot_Odds(White_Lily, 3, 0.025),
        Loot_Odds(Packed_Ice, 15, 0.06),
        Loot_Odds(Spruce_Planks, 15, 0.06),
        Loot_Odds(Spruce_Log, 4, 0.02),
        Loot_Odds(Gravel, 15, 0.06),
        Loot_Odds(Gold_Ingot, 4, 0.0008),
        Loot_Odds(Iron_Ingot, 4, 0.0008),
        Loot_Odds(Diamond, 2, 0.00045),
    ])

    def __init__(self):
        pass

    @classmethod
    def get_width(cls):
        return cls.width
    
    @classmethod
    def get_x_difference_for_y(cls):
        """returns the value to add to x to get the corect elevation this object is calcualated for (i.e., for a tree it would be +1)"""
        return cls.start_x_diff
    
    @classmethod
    def get_height(cls):
        """gets height above the start point"""
        return cls.height

    @classmethod
    def get_depth(cls):
        """gets depth below the start point"""
        return cls.depth

    @classmethod
    def getStructureInstructions(cls, ground_x, ground_y, grid, random_factor=0, biome_name=None):
        """takes top left block coordinates and returns list of coordinates and a list of blocks to access in the same order"""
        # initialize list
        structureInstructionsList = []

        # get the depth
        min_depth = 20
        max_depth = grid.height

        chance = int(hashlib.sha256(f"{random_factor}_depth".encode()).hexdigest(), 16) / (2**256 - 1)
        adjusted_ground_y = ground_y + min_depth + int(chance * (grid.height - ground_y))

        if adjusted_ground_y > grid.height:
            return structureInstructionsList, []

        # shift start_y up to true start
        start_x = ground_x
        start_y = adjusted_ground_y - cls.height

        # top level
        y = 0
        for x in range(6):
            structureInstructionsList.append(Structure_Instruction(start_x + x, start_y + y, Stone_Bricks))

        # fill in the middle section
        for y in range(1, 4):
            x = 0
            structureInstructionsList.append(Structure_Instruction(start_x + x, start_y + y, Stone_Bricks))
            x = 5
            structureInstructionsList.append(Structure_Instruction(start_x + x, start_y + y, Stone_Bricks))
            for x in range(1, 5):
                structureInstructionsList.append(Structure_Instruction(start_x + x, start_y + y, None))


        # bottom level
        y = 4
        for x in range(6):
            structureInstructionsList.append(Structure_Instruction(start_x + x, start_y + y, Stone_Bricks))

        # now add the recipe frame block
        recipeFrame_x, recipeFrame_y = start_x + 3, start_y + 3
        recipeFrameBlock = Recipe_Frame(grid, grid.screen, recipeFrame_x, recipeFrame_y, grid.BLOCK_WIDTH)

        recipeList = User_Crafting_Recipes_List.getBiomeWeightedFindableRecipesList(biome_name)

        index = int(random_factor * len(recipeList)) % len(recipeList)
        randomRecipe = recipeList[index]
        recipeFrameBlock.stored_inventory_items.append(randomRecipe)
        structureInstructionsList.append(Structure_Instruction(recipeFrame_x, recipeFrame_y, recipeFrameBlock, blockIsInitialized=True))

        chest_x, chest_y = recipeFrame_x - 1, recipeFrame_y
        chest_block = Spruce_Chest(grid, grid.screen, chest_x, chest_y, grid.BLOCK_WIDTH)
        for chest_slot_num in range(chest_block.chest_slots_count):
            chest_loot_random_factor = int(hashlib.sha256(f"{random_factor}_{chest_slot_num}".encode()).hexdigest(), 16) / (2**256 - 1)
            chest_block.stored_inventory_items.append(cls.chest_loot.get_slot(chest_loot_random_factor))
        structureInstructionsList.append(Structure_Instruction(chest_x, chest_y, chest_block, blockIsInitialized=True))

        # return list
        return structureInstructionsList, []

    @classmethod
    def getBgStructureInstructions(cls, ground_x, ground_y, grid, random_factor=0, biome_name=None): # needs to actually reflect the background
        """takes top left block coordinates and returns list of coordinates and a list of blocks to access in the same order"""
        # initialize list
        structureInstructionsList = []

        # get the depth
        min_depth = 20
        max_depth = grid.height

        chance = int(hashlib.sha256(f"{random_factor}_depth".encode()).hexdigest(), 16) / (2**256 - 1)
        adjusted_ground_y = ground_y + min_depth + int(chance * (grid.height - ground_y))

        if adjusted_ground_y > grid.height:
            return structureInstructionsList, []

        # shift start_y up to true start
        start_x = ground_x
        start_y = adjusted_ground_y - cls.height

        for y in range(0, cls.height):
            for x in range(0, cls.width):
                structureInstructionsList.append(Structure_Instruction(start_x + x, start_y + y, Spruce_Planks))

        # return list
        return structureInstructionsList, []


class Tree:
    width = 3
    start_x_diff = 1 # distance from the origin x that the y elevation should be set to
    height = 5 # distance above ground
    depth = 0 # distance below ground

    def __init__(self):
        pass

    @classmethod
    def get_width(cls):
        return cls.width
    
    @classmethod
    def get_x_difference_for_y(cls):
        """returns the value to add to x to get the corect elevation this object is calcualated for (i.e., for a tree it would be +1)"""
        return cls.start_x_diff

    @classmethod
    def get_height(cls):
        """gets height above the start point"""
        return cls.height

    @classmethod
    def get_depth(cls):
        """gets depth below the start point"""
        return cls.depth

    @classmethod
    def getStructureInstructions(cls, ground_x, ground_y, grid, random_factor=0, biome_name=None):
        """takes top left block coordinates and returns list of coordinates and a list of blocks to access in the same order"""
        # initialize list
        structureInstructionsList = []

        # determine the height of the tree
        if random_factor < 0.0001:
            tree_height = 4
        elif random_factor < 0.2:
            tree_height = 1
        elif random_factor < 0.4:
            tree_height = 3
        else:
            tree_height = 2

        # trunk
        start_y = ground_y-1
        for y in range(tree_height):
            structureInstructionsList.append(Structure_Instruction(ground_x+1, start_y-y, Log))

        # leaves disappearing time thresholds
        def get_ticks(x, y):
            value = int(hashlib.sha256(f"{random_factor}_{x}_{y}".encode()).hexdigest(), 16)
            normalized = value / (2**256)
            return int(normalized * 1000) + 200 # ticks will be between 200 and 1200

        # add the leaves to the structure instructions
        for y in range(3):
            for x in range(3):
                ticks = get_ticks(x, y)
                structureInstructionsList.append(Structure_Instruction(ground_x+x, start_y-y-tree_height, Leaves(grid, grid.screen, ground_x+x, start_y-y-tree_height, grid.BLOCK_WIDTH, pass_through=True, anchor_x=ground_x+1, anchor_y=start_y, tick_threshold=ticks), blockIsInitialized=True))
        
        # return list
        return structureInstructionsList, []

    @classmethod
    def getBgStructureInstructions(cls, ground_x, ground_y, grid, random_factor=0, biome_name=None): # needs to actually reflect the background
        """takes top left block coordinates and returns list of coordinates and a list of blocks to access in the same order"""
        return [], [] # trees don't have backgrounds


class Spruce_Tree:
    width = 3
    start_x_diff = 1 # distance from the origin x that the y elevation should be set to
    height = 9 # distance above ground
    depth = 0 # distance below ground

    def __init__(self):
        pass

    @classmethod
    def get_width(cls):
        return cls.width
    
    @classmethod
    def get_x_difference_for_y(cls):
        """returns the value to add to x to get the corect elevation this object is calcualated for (i.e., for a tree it would be +1)"""
        return cls.start_x_diff

    @classmethod
    def get_height(cls):
        """gets height above the start point"""
        return cls.height

    @classmethod
    def get_depth(cls):
        """gets depth below the start point"""
        return cls.depth

    @classmethod
    def getStructureInstructions(cls, ground_x, ground_y, grid, random_factor=0, biome_name=None):
        """takes top left block coordinates and returns list of coordinates and a list of blocks to access in the same order"""
        # initialize list
        structureInstructionsList = []

        # determine the height of the tree
        if random_factor < 0.1:
            tree_height = 5
        elif random_factor < 0.4:
            tree_height = 3
        else:
            tree_height = 4

        # trunk
        start_y = ground_y-1
        for y in range(tree_height):
            structureInstructionsList.append(Structure_Instruction(ground_x+1, start_y-y, Spruce_Log))
        extra_log_y = ground_y - tree_height - 2
        structureInstructionsList.append(Structure_Instruction(ground_x+1, extra_log_y, Spruce_Log))
        
        # leaves disappearing time thresholds
        def get_ticks(x, y):
            value = int(hashlib.sha256(f"{random_factor}_{x}_{y}".encode()).hexdigest(), 16)
            normalized = value / (2**256)
            return int(normalized * 1000) + 200 # ticks will be between 200 and 1200

        # add the leaves to the structure instructions
        y = ground_y - tree_height - 1
        for x in range(3):
            ticks = get_ticks(x, y)
            structureInstructionsList.append(Structure_Instruction(ground_x+x, y, Spruce_Leaves(grid, grid.screen, ground_x+x, y, grid.BLOCK_WIDTH, pass_through=True, anchor_x=ground_x+1, anchor_y=start_y, tick_threshold=ticks), blockIsInitialized=True))

        y = ground_y - tree_height - 3
        for x in range(3):
            ticks = get_ticks(x, y)
            structureInstructionsList.append(Structure_Instruction(ground_x+x, y, Spruce_Leaves(grid, grid.screen, ground_x+x, y, grid.BLOCK_WIDTH, pass_through=True, anchor_x=ground_x+1, anchor_y=start_y, tick_threshold=ticks), blockIsInitialized=True))

        y = ground_y - tree_height - 4
        x = 1
        ticks = get_ticks(x, y)
        structureInstructionsList.append(Structure_Instruction(ground_x+x, y, Spruce_Leaves(grid, grid.screen, ground_x+x, y, grid.BLOCK_WIDTH, pass_through=True, anchor_x=ground_x+1, anchor_y=start_y, tick_threshold=ticks), blockIsInitialized=True))

        # return list
        return structureInstructionsList, []

    @classmethod
    def getBgStructureInstructions(cls, ground_x, ground_y, grid, random_factor=0, biome_name=None): # needs to actually reflect the background
        """takes top left block coordinates and returns list of coordinates and a list of blocks to access in the same order"""
        return [], [] # trees don't have backgrounds


class Mahogany_Tree_Rand_Width:
    width = 5
    start_x_diff = 1 # distance from the origin x that the y elevation should be set to
    height = 8 # distance above ground
    depth = 0 # distance below ground

    def __init__(self):
        pass

    @classmethod
    def get_width(cls):
        return cls.width
    
    @classmethod
    def get_x_difference_for_y(cls):
        """returns the value to add to x to get the corect elevation this object is calcualated for (i.e., for a tree it would be +1)"""
        return cls.start_x_diff

    @classmethod
    def get_height(cls):
        """gets height above the start point"""
        return cls.height

    @classmethod
    def get_depth(cls):
        """gets depth below the start point"""
        return cls.depth

    @classmethod
    def getStructureInstructions(cls, ground_x, ground_y, grid, random_factor=0, biome_name=None):
        """takes top left block coordinates and returns list of coordinates and a list of blocks to access in the same order"""
        # initialize list
        structureInstructionsList = []

        tree_style_chance = int(hashlib.sha256(f"{random_factor}_tree_type".encode()).hexdigest(), 16) / (2**256 - 1)
        if tree_style_chance > 0.8: # 2 wide style
            structureInstructionsList, var_structure_instructions = Mahogany_Tree_Double.getStructureInstructions(ground_x, ground_y, grid, random_factor, biome_name)
        else:
            structureInstructionsList, var_structure_instructions = Mahogany_Tree.getStructureInstructions(ground_x, ground_y, grid, random_factor, biome_name)

        # return list
        return structureInstructionsList, var_structure_instructions

    @classmethod
    def getBgStructureInstructions(cls, ground_x, ground_y, grid, random_factor=0, biome_name=None): # needs to actually reflect the background
        """takes top left block coordinates and returns list of coordinates and a list of blocks to access in the same order"""
        return [], [] # trees don't have backgrounds


class Mahogany_Tree_Double:
    width = 6
    start_x_diff = 1 # distance from the origin x that the y elevation should be set to
    height = 7 # distance above ground
    depth = 0 # distance below ground

    def __init__(self):
        pass

    @classmethod
    def get_width(cls):
        return cls.width
    
    @classmethod
    def get_x_difference_for_y(cls):
        """returns the value to add to x to get the corect elevation this object is calcualated for (i.e., for a tree it would be +1)"""
        return cls.start_x_diff

    @classmethod
    def get_height(cls):
        """gets height above the start point"""
        return cls.height

    @classmethod
    def get_depth(cls):
        """gets depth below the start point"""
        return cls.depth

    @classmethod
    def getStructureInstructions(cls, ground_x, ground_y, grid, random_factor=0, biome_name=None):
        """takes top left block coordinates and returns list of coordinates and a list of blocks to access in the same order"""
        # initialize list
        structureInstructionsList = []

        # leaves disappearing time thresholds
        def get_ticks(x, y):
            value = int(hashlib.sha256(f"{random_factor}_{x}_{y}".encode()).hexdigest(), 16)
            normalized = value / (2**256)
            return int(normalized * 1000) + 200 # ticks will be between 200 and 1200

        # determine the height of the tree
        if random_factor < 0.1:
            tree_height = 6
        elif random_factor < 0.4:
            tree_height = 4
        else:
            tree_height = 5

        # trunk
        start_y = ground_y-1
        for y in range(tree_height):
            for x in range(2):
                structureInstructionsList.append(Structure_Instruction(ground_x+x+2, start_y-y, Mahogany_Log))
        
        # add the leaves to the structure instructions
        y = ground_y - tree_height - 1
        for x in range(6):
            ticks = get_ticks(x, y)
            structureInstructionsList.append(Structure_Instruction(ground_x+x, y, Mahogany_Leaves(grid, grid.screen, ground_x+x, y, grid.BLOCK_WIDTH, pass_through=True, anchor_x=ground_x+2, anchor_y=start_y, tick_threshold=ticks), blockIsInitialized=True))

        y = ground_y - tree_height - 2
        for x in range(1, 5):
            ticks = get_ticks(x, y)
            structureInstructionsList.append(Structure_Instruction(ground_x+x, y, Mahogany_Leaves(grid, grid.screen, ground_x+x, y, grid.BLOCK_WIDTH, pass_through=True, anchor_x=ground_x+2, anchor_y=start_y, tick_threshold=ticks), blockIsInitialized=True))

        y = ground_y - tree_height - 3
        for x in range(2, 4):
            ticks = get_ticks(x, y)
            structureInstructionsList.append(Structure_Instruction(ground_x+x, y, Mahogany_Leaves(grid, grid.screen, ground_x+x, y, grid.BLOCK_WIDTH, pass_through=True, anchor_x=ground_x+2, anchor_y=start_y, tick_threshold=ticks), blockIsInitialized=True))

        # add a branched off leaf
        extra_leaf_odds = int(hashlib.sha256(f"{random_factor}_extra_leaf_odds".encode()).hexdigest(), 16) / (2**256 - 1)
        add_branched_leaf = True
        if extra_leaf_odds < 0.35:
            x = 1
            y_diff = 1
        elif extra_leaf_odds < 0.7:
            x = 1
            y_diff = 1
        elif extra_leaf_odds < 0.84:
            x = 4
            y_diff = 2
        elif extra_leaf_odds < 0.98:
            x = 4
            y_diff = 2
        else:
            add_branched_leaf = False

        if add_branched_leaf:
            y = ground_y - tree_height + y_diff
            ticks = get_ticks(x, y)
            structureInstructionsList.append(Structure_Instruction(ground_x+x, y, Mahogany_Leaves(grid, grid.screen, ground_x+x, y, grid.BLOCK_WIDTH, pass_through=True, anchor_x=ground_x+2, anchor_y=start_y, tick_threshold=ticks), blockIsInitialized=True))

        # return list
        return structureInstructionsList, [Var_Structure_Instruction(ground_x + 2, ground_y, Mahogany_Log, None, 1), Var_Structure_Instruction(ground_x + 3, ground_y, Mahogany_Log, None, 1)]

    @classmethod
    def getBgStructureInstructions(cls, ground_x, ground_y, grid, random_factor=0, biome_name=None): # needs to actually reflect the background
        """takes top left block coordinates and returns list of coordinates and a list of blocks to access in the same order"""
        return [], [] # trees don't have backgrounds


class Mahogany_Tree:
    width = 3
    start_x_diff = 1 # distance from the origin x that the y elevation should be set to
    height = 8 # distance above ground
    depth = 0 # distance below ground

    def __init__(self):
        pass

    @classmethod
    def get_width(cls):
        return cls.width
    
    @classmethod
    def get_x_difference_for_y(cls):
        """returns the value to add to x to get the corect elevation this object is calcualated for (i.e., for a tree it would be +1)"""
        return cls.start_x_diff

    @classmethod
    def get_height(cls):
        """gets height above the start point"""
        return cls.height

    @classmethod
    def get_depth(cls):
        """gets depth below the start point"""
        return cls.depth

    @classmethod
    def getStructureInstructions(cls, ground_x, ground_y, grid, random_factor=0, biome_name=None):
        """takes top left block coordinates and returns list of coordinates and a list of blocks to access in the same order"""
        # initialize list
        structureInstructionsList = []

        # leaves disappearing time thresholds
        def get_ticks(x, y):
            value = int(hashlib.sha256(f"{random_factor}_{x}_{y}".encode()).hexdigest(), 16)
            normalized = value / (2**256)
            return int(normalized * 1000) + 200 # ticks will be between 200 and 1200

        # determine the height of the tree
        if random_factor < 0.1:
            tree_height = 3
        elif random_factor < 0.35:
            tree_height = 5
        else:
            tree_height = 4

        # trunk
        start_y = ground_y-1
        for y in range(tree_height):
            structureInstructionsList.append(Structure_Instruction(ground_x+2, start_y-y, Mahogany_Log))
        
        # add the leaves to the structure instructions
        y = ground_y - tree_height - 1
        for x in range(5):
            ticks = get_ticks(x, y)
            structureInstructionsList.append(Structure_Instruction(ground_x+x, y, Mahogany_Leaves(grid, grid.screen, ground_x+x, y, grid.BLOCK_WIDTH, pass_through=True, anchor_x=ground_x+2, anchor_y=start_y, tick_threshold=ticks), blockIsInitialized=True))

        y = ground_y - tree_height - 2
        for x in range(1, 4):
            ticks = get_ticks(x, y)
            structureInstructionsList.append(Structure_Instruction(ground_x+x, y, Mahogany_Leaves(grid, grid.screen, ground_x+x, y, grid.BLOCK_WIDTH, pass_through=True, anchor_x=ground_x+2, anchor_y=start_y, tick_threshold=ticks), blockIsInitialized=True))

        # add a branched off leaf
        extra_leaf_odds = int(hashlib.sha256(f"{random_factor}_extra_leaf_odds".encode()).hexdigest(), 16) / (2**256 - 1)
        add_branched_leaf = True
        if extra_leaf_odds < 0.35:
            x = 1
        elif extra_leaf_odds < 0.7:
            x = 3
        else:
            add_branched_leaf = False
        
        if add_branched_leaf:
            y = ground_y - tree_height + 1
            ticks = get_ticks(x, y)
            structureInstructionsList.append(Structure_Instruction(ground_x+x, y, Mahogany_Leaves(grid, grid.screen, ground_x+x, y, grid.BLOCK_WIDTH, pass_through=True, anchor_x=ground_x+2, anchor_y=start_y, tick_threshold=ticks), blockIsInitialized=True))

        # return list
        return structureInstructionsList, [Var_Structure_Instruction(ground_x + 2, ground_y, Mahogany_Log, None, 1)]

    @classmethod
    def getBgStructureInstructions(cls, ground_x, ground_y, grid, random_factor=0, biome_name=None): # needs to actually reflect the background
        """takes top left block coordinates and returns list of coordinates and a list of blocks to access in the same order"""
        return [], [] # trees don't have backgrounds


class Snow_Tree:
    width = 3
    start_x_diff = 1 # distance from the origin x that the y elevation should be set to
    height = 5 # distance above ground
    depth = 0 # distance below ground

    def __init__(self):
        pass

    @classmethod
    def get_width(cls):
        return cls.width
    
    @classmethod
    def get_x_difference_for_y(cls):
        """returns the value to add to x to get the corect elevation this object is calcualated for (i.e., for a tree it would be +1)"""
        return cls.start_x_diff

    @classmethod
    def get_height(cls):
        """gets height above the start point"""
        return cls.height

    @classmethod
    def get_depth(cls):
        """gets depth below the start point"""
        return cls.depth

    @classmethod
    def getStructureInstructions(cls, ground_x, ground_y, grid, random_factor=0, biome_name=None):
        """takes top left block coordinates and returns list of coordinates and a list of blocks to access in the same order"""
        # initialize list
        structureInstructionsList = []

        # determine the height of the tree
        if random_factor < 0.0001:
            tree_height = 4
        elif random_factor < 0.2:
            tree_height = 1
        elif random_factor < 0.4:
            tree_height = 3
        else:
            tree_height = 2

        # trunk
        start_y = ground_y-1
        for y in range(tree_height):
            structureInstructionsList.append(Structure_Instruction(ground_x+1, start_y-y, Log))

        # leaves disappearing time thresholds
        def get_ticks(x, y):
            value = int(hashlib.sha256(f"{random_factor}_{x}_{y}".encode()).hexdigest(), 16)
            normalized = value / (2**256)
            return int(normalized * 1000) + 200 # ticks will be between 200 and 1200

        # add the leaves to the structure instructions
        for y in range(2):
            for x in range(3):
                ticks = get_ticks(x, y)
                structureInstructionsList.append(Structure_Instruction(ground_x+x, start_y-y-tree_height, Snow_Leaves(grid, grid.screen, ground_x+x, start_y-y-tree_height, grid.BLOCK_WIDTH, pass_through=True, anchor_x=ground_x+1, anchor_y=start_y, tick_threshold=ticks), blockIsInitialized=True))
        for x in range(3):
            y = 2
            ticks = get_ticks(x, y)
            structureInstructionsList.append(Structure_Instruction(ground_x+x, start_y-2-tree_height, Snow_Leaves_Top(grid, grid.screen, ground_x+x, start_y-2-tree_height, grid.BLOCK_WIDTH, pass_through=True, anchor_x=ground_x+1, anchor_y=start_y, tick_threshold=ticks), blockIsInitialized=True))

        # return list
        return structureInstructionsList, []

    @classmethod
    def getBgStructureInstructions(cls, ground_x, ground_y, grid, random_factor=0, biome_name=None): # needs to actually reflect the background
        """takes top left block coordinates and returns list of coordinates and a list of blocks to access in the same order"""
        return [], [] # trees don't have backgrounds


class Cactus_Structure:
    width = 1
    start_x_diff = 0 # distance from the origin x that the y elevation should be set to
    height = 3 # distance above ground
    depth = 0 # distance below ground

    def __init__(self):
        pass

    @classmethod
    def get_width(cls):
        return cls.width
    
    @classmethod
    def get_x_difference_for_y(cls):
        """returns the value to add to x to get the corect elevation this object is calcualated for (i.e., for a tree it would be +1)"""
        return cls.start_x_diff

    @classmethod
    def get_height(cls):
        """gets height above the start point"""
        return cls.height

    @classmethod
    def get_depth(cls):
        """gets depth below the start point"""
        return cls.depth

    @classmethod
    def getStructureInstructions(cls, ground_x, ground_y, grid, random_factor=0, biome_name=None):
        """takes top left block coordinates and returns list of coordinates and a list of blocks to access in the same order"""
        # initialize list
        structureInstructionsList = []

        # determine the height of the tree
        if random_factor < 0.0001:
            tree_height = 4
        elif random_factor < 0.2:
            tree_height = 1
        elif random_factor < 0.4:
            tree_height = 3
        else:
            tree_height = 2

        # trunk
        start_y = ground_y-1
        for y in range(tree_height):
            structureInstructionsList.append(Structure_Instruction(ground_x, start_y-y, Cactus))

        # return list
        return structureInstructionsList, []

    @classmethod
    def getBgStructureInstructions(cls, ground_x, ground_y, grid, random_factor=0, biome_name=None): # needs to actually reflect the background
        """takes top left block coordinates and returns list of coordinates and a list of blocks to access in the same order"""
        return [], [] # trees don't have backgrounds


class Snow_Man_Structure:
    width = 1
    start_x_diff = 0 # distance from the origin x that the y elevation should be set to
    height = 2 # distance above ground
    depth = 0 # distance below ground

    def __init__(self):
        pass

    @classmethod
    def get_width(cls):
        return cls.width
    
    @classmethod
    def get_x_difference_for_y(cls):
        """returns the value to add to x to get the corect elevation this object is calcualated for (i.e., for a tree it would be +1)"""
        return cls.start_x_diff

    @classmethod
    def get_height(cls):
        """gets height above the start point"""
        return cls.height

    @classmethod
    def get_depth(cls):
        """gets depth below the start point"""
        return cls.depth

    @classmethod
    def getStructureInstructions(cls, ground_x, ground_y, grid, random_factor=0, biome_name=None):
        """takes top left block coordinates and returns list of coordinates and a list of blocks to access in the same order"""
        # initialize list
        structureInstructionsList = []

        structureInstructionsList.append(Structure_Instruction(ground_x, ground_y-1, Snow_Block))
        structureInstructionsList.append(Structure_Instruction(ground_x, ground_y-2, Snow_Man_Head))

        # return list
        return structureInstructionsList, []

    @classmethod
    def getBgStructureInstructions(cls, ground_x, ground_y, grid, random_factor=0, biome_name=None): # needs to actually reflect the background
        """takes top left block coordinates and returns list of coordinates and a list of blocks to access in the same order"""
        return [], [] # trees don't have backgrounds


class Small_Bush:
    width = 1
    start_x_diff = 0 # distance from the origin x that the y elevation should be set to
    height = 1 # distance above ground
    depth = 0 # distance below ground

    def __init__(self):
        pass

    @classmethod
    def get_width(cls):
        return cls.width
    
    @classmethod
    def get_x_difference_for_y(cls):
        """returns the value to add to x to get the corect elevation this object is calcualated for (i.e., for a tree it would be +1)"""
        return cls.start_x_diff

    @classmethod
    def get_height(cls):
        """gets height above the start point"""
        return cls.height

    @classmethod
    def get_depth(cls):
        """gets depth below the start point"""
        return cls.depth

    @classmethod
    def getStructureInstructions(cls, ground_x, ground_y, grid, random_factor=0, biome_name=None):
        """takes top left block coordinates and returns list of coordinates and a list of blocks to access in the same order"""
        # initialize list
        structureInstructionsList = []

        structureInstructionsList.append(Structure_Instruction(ground_x, ground_y-1, Bush))

        # return list
        return structureInstructionsList, []

    @classmethod
    def getBgStructureInstructions(cls, ground_x, ground_y, grid, random_factor=0, biome_name=None): # needs to actually reflect the background
        """takes top left block coordinates and returns list of coordinates and a list of blocks to access in the same order"""
        return [], [] # trees don't have backgrounds


class Flowers:
    width = 1
    start_x_diff = 0 # distance from the origin x that the y elevation should be set to
    height = 1 # distance above ground
    depth = 0 # distance below ground

    def __init__(self):
        pass

    @classmethod
    def get_width(cls):
        return cls.width
    
    @classmethod
    def get_x_difference_for_y(cls):
        """returns the value to add to x to get the corect elevation this object is calcualated for (i.e., for a tree it would be +1)"""
        return cls.start_x_diff

    @classmethod
    def get_height(cls):
        """gets height above the start point"""
        return cls.height

    @classmethod
    def get_depth(cls):
        """gets depth below the start point"""
        return cls.depth

    @classmethod
    def getStructureInstructions(cls, ground_x, ground_y, grid, random_factor=0, biome_name=None):
        """takes top left block coordinates and returns list of coordinates and a list of blocks to access in the same order"""
        # initialize list
        structureInstructionsList = []

        
        if biome_name == 'Glacier':
            flower_options = [Rose]
        elif biome_name == 'Ravine':
            flower_options = [Wild_Flower]
        elif biome_name == 'Tundra':
            flower_options = [White_Lily]
        elif biome_name == 'Montane_Forest':
            flower_options = [Rose, White_Lily]
        else:
            flower_options = [Rose, Wild_Flower, White_Lily, Forget_Me_Not]
            
        index = int(random_factor * len(flower_options)) % len(flower_options)
        Flower = flower_options[index]

        structureInstructionsList.append(Structure_Instruction(ground_x, ground_y-1, Flower(grid, grid.screen, ground_x, ground_y-1, grid.BLOCK_WIDTH, pass_through=True), blockIsInitialized=True))

        # return list
        return structureInstructionsList, []

    @classmethod
    def getBgStructureInstructions(cls, ground_x, ground_y, grid, random_factor=0, biome_name=None): # needs to actually reflect the background
        """takes top left block coordinates and returns list of coordinates and a list of blocks to access in the same order"""
        return [], [] # trees don't have backgrounds


class Puddle:
    width = 1
    start_x_diff = 0 # distance from the origin x that the y elevation should be set to
    height = 0 # distance above ground
    depth = 0 # distance below ground

    def __init__(self):
        pass

    @classmethod
    def get_width(cls):
        return cls.width
    
    @classmethod
    def get_x_difference_for_y(cls):
        """returns the value to add to x to get the corect elevation this object is calcualated for (i.e., for a tree it would be +1)"""
        return cls.start_x_diff

    @classmethod
    def get_height(cls):
        """gets height above the start point"""
        return cls.height

    @classmethod
    def get_depth(cls):
        """gets depth below the start point"""
        return cls.depth

    @classmethod
    def getStructureInstructions(cls, ground_x, ground_y, grid, random_factor=0, biome_name=None):
        """takes top left block coordinates and returns list of coordinates and a list of blocks to access in the same order"""
        # initialize list
        structureInstructionsList = []

        structureInstructionsList.append(Structure_Instruction(ground_x, ground_y, Water))

        # return list
        return structureInstructionsList, []

    @classmethod
    def getBgStructureInstructions(cls, ground_x, ground_y, grid, random_factor=0, biome_name=None): # needs to actually reflect the background
        """takes top left block coordinates and returns list of coordinates and a list of blocks to access in the same order"""
        return [], [] # trees don't have backgrounds


class Watermellon_Patch:
    width = 1
    start_x_diff = 0 # distance from the origin x that the y elevation should be set to
    height = 1 # distance above ground
    depth = 0 # distance below ground

    def __init__(self):
        pass

    @classmethod
    def get_width(cls):
        return cls.width
    
    @classmethod
    def get_x_difference_for_y(cls):
        """returns the value to add to x to get the corect elevation this object is calcualated for (i.e., for a tree it would be +1)"""
        return cls.start_x_diff

    @classmethod
    def get_height(cls):
        """gets height above the start point"""
        return cls.height

    @classmethod
    def get_depth(cls):
        """gets depth below the start point"""
        return cls.depth

    @classmethod
    def getStructureInstructions(cls, ground_x, ground_y, grid, random_factor=0, biome_name=None):
        """takes top left block coordinates and returns list of coordinates and a list of blocks to access in the same order"""
        # initialize list
        structureInstructionsList = []

        structureInstructionsList.append(Structure_Instruction(ground_x, ground_y-1, Watermellon))

        # return list
        return structureInstructionsList, []

    @classmethod
    def getBgStructureInstructions(cls, ground_x, ground_y, grid, random_factor=0, biome_name=None): # needs to actually reflect the background
        """takes top left block coordinates and returns list of coordinates and a list of blocks to access in the same order"""
        return [], [] # trees don't have backgrounds

