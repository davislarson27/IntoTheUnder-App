from math import floor
import hashlib

from world.blocks.block_export import *
from .structure_instruction import Structure_Instruction
from play.inventory.crafting_recipes import User_Crafting_Recipes_List

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
    def getStructureInstructions(cls, ground_x, ground_y, grid, random_factor=0):
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
        recipeList = User_Crafting_Recipes_List.getFindableRecipesList()
        index = int(random_factor * len(recipeList)) % len(recipeList)
        randomRecipe = recipeList[index]
        recipeFrameBlock.stored_inventory_items.append(randomRecipe)
        structureInstructionsList.append(Structure_Instruction(recipeFrame_x, recipeFrame_y, recipeFrameBlock, blockIsInitialized=True))

        # return list
        return structureInstructionsList

    @classmethod
    def getBgStructureInstructions(cls, ground_x, ground_y, grid, random_factor=0): # needs to actually reflect the background
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
        return structureInstructionsList


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
    def getStructureInstructions(cls, ground_x, ground_y, grid, random_factor=0):
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
        return structureInstructionsList

    @classmethod
    def getBgStructureInstructions(cls, ground_x, ground_y, grid, random_factor=0): # needs to actually reflect the background
        """takes top left block coordinates and returns list of coordinates and a list of blocks to access in the same order"""
        return [] # trees don't have backgrounds


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
    def getStructureInstructions(cls, ground_x, ground_y, grid, random_factor=0):
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
        return structureInstructionsList

    @classmethod
    def getBgStructureInstructions(cls, ground_x, ground_y, grid, random_factor=0): # needs to actually reflect the background
        """takes top left block coordinates and returns list of coordinates and a list of blocks to access in the same order"""
        return [] # trees don't have backgrounds


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
    def getStructureInstructions(cls, ground_x, ground_y, grid, random_factor=0):
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
        return structureInstructionsList

    @classmethod
    def getBgStructureInstructions(cls, ground_x, ground_y, grid, random_factor=0): # needs to actually reflect the background
        """takes top left block coordinates and returns list of coordinates and a list of blocks to access in the same order"""
        return [] # trees don't have backgrounds


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
    def getStructureInstructions(cls, ground_x, ground_y, grid, random_factor=0):
        """takes top left block coordinates and returns list of coordinates and a list of blocks to access in the same order"""
        # initialize list
        structureInstructionsList = []

        structureInstructionsList.append(Structure_Instruction(ground_x, ground_y-1, Snow_Block))
        structureInstructionsList.append(Structure_Instruction(ground_x, ground_y-2, Snow_Man_Head))

        # return list
        return structureInstructionsList

    @classmethod
    def getBgStructureInstructions(cls, ground_x, ground_y, grid, random_factor=0): # needs to actually reflect the background
        """takes top left block coordinates and returns list of coordinates and a list of blocks to access in the same order"""
        return [] # trees don't have backgrounds
    

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
    def getStructureInstructions(cls, ground_x, ground_y, grid, random_factor=0):
        """takes top left block coordinates and returns list of coordinates and a list of blocks to access in the same order"""
        # initialize list
        structureInstructionsList = []

        structureInstructionsList.append(Structure_Instruction(ground_x, ground_y-1, Leaves(grid, grid.screen, ground_x, ground_y-1, grid.BLOCK_WIDTH, pass_through=True), blockIsInitialized=True))

        # return list
        return structureInstructionsList

    @classmethod
    def getBgStructureInstructions(cls, ground_x, ground_y, grid, random_factor=0): # needs to actually reflect the background
        """takes top left block coordinates and returns list of coordinates and a list of blocks to access in the same order"""
        return [] # trees don't have backgrounds
    
