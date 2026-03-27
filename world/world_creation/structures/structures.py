import random

from world.blocks.block_export import *
from .structure_instruction import Structure_Instruction
from play.inventory.crafting_recipes import User_Crafting_Recipes_List

class Recipe_Burrow:
    width = 8
    height = 3
    depth = 2

    def __init__(self):
        pass

    @classmethod
    def get_width(cls):
        return cls.width
    
    @classmethod
    def get_height(cls):
        """gets height above the start point"""
        return cls.height

    @classmethod
    def get_depth(cls):
        """gets depth below the start point"""
        return cls.depth

    @classmethod
    def getStructureInstructions(cls, ground_x, ground_y, grid):
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
        randomRecipe = random.choice(User_Crafting_Recipes_List.getFindableRecipesList())
        recipeFrameBlock.stored_inventory_items.append(randomRecipe)
        structureInstructionsList.append(Structure_Instruction(recipeFrame_x, recipeFrame_y, recipeFrameBlock, blockIsInitialized=True))

        # return list
        return structureInstructionsList
