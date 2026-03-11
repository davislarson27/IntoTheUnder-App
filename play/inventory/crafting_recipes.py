import pygame

from world.blocks.block_export import *


class Crafting_Recipe:
    def __init__(self, recipe_name, requirement_list, output=None):
        self.name = recipe_name
        self.requirement_list = requirement_list
        self.output = output

    def __eq__(self, other):
        if not isinstance(other, Crafting_Recipe):
            return False
        
        if not self.name == other.name:
            return False
        
        if len(self.requirement_list) != len(other.requirement_list):
            return False
        i = 0
        for requirement in self.requirement_list:
            if not requirement == other.requirement_list[i]:
                return False
            i+=1
        
        if not self.output == other.output:
            return False
        
        return True


class Ingredient:
    def __init__(self, block_type, count):
        self.block_type = block_type
        self.count = count

    def __eq__(self, other):
        return isinstance(other, Ingredient) and self.block_type is other.block_type and self.count == other.count

class Recipe_Slot_Contents:
    def __init__(self, main_rect, block_rect, recipe, outline_width, valid_recipe_color, invalid_recipe_color):
        self.main_rect = main_rect
        self.block_rect = block_rect
        self.recipe = recipe
        self.is_recipe_valid = False
        self.outline_width = outline_width
        self.valid_recipe_color = valid_recipe_color
        self.invalid_recipe_color = invalid_recipe_color

    def set_recipe(self, cur_recipe):
        self.recipe = cur_recipe
        if cur_recipe is not None:
            self.is_recipe_valid = True
        else:
            self.is_recipe_valid = False

    def draw(self, screen):
        if self.is_recipe_valid:
            color = self.valid_recipe_color
        else:
            color = self.invalid_recipe_color

        pygame.draw.rect(
            screen,
            color,
            self.main_rect,
            self.outline_width
        )

        if self.recipe is not None and self.recipe.output is not None:
            block_type = self.recipe.output.block_type
            block_type.draw_manual(
                    screen, 
                    self.block_rect.x,
                    self.block_rect.y,
                    self.block_rect.width,
                    is_grid_coordinates = False # set to draw by pixel
                )

class User_Recipes_List: # not in use yet
    def __init__(self, discovered_recipes=None):
        self.default_crafting_recipes = [
            Crafting_Recipe(
                "Dirt",
                [
                    Ingredient(Grass, 1)
                ],
                output=Ingredient(Dirt, 1)
            ),
            Crafting_Recipe(
                "Chest",
                [
                    Ingredient(Wood_Planks, 6), 
                    Ingredient(Iron_Ingot, 1)
                ],
                output=Ingredient(Chest, 1)
            ),
            Crafting_Recipe(
                "Iron Ore Ingot",
                [
                    Ingredient(Iron_Ore_Block, 1),
                ],
                output=Ingredient(Iron_Ingot, 1)
            ),
            Crafting_Recipe(
                "Gold Ore Ingot",
                [
                    Ingredient(Gold_Ore_Block, 1),
                ],
                output=Ingredient(Gold_Ingot, 1)
            ),
            Crafting_Recipe(
                "Gravel",
                [
                    Ingredient(Rock, 1),
                ],
                output=Ingredient(Gravel, 2)
            ),
            Crafting_Recipe(
                "Door",
                [
                    Ingredient(Wood_Planks, 3),
                ],
                output=Ingredient(Door, 2)
            ),
            Crafting_Recipe(
                "Wood Planks",
                [
                    Ingredient(Log, 1),
                ],
                output=Ingredient(Wood_Planks, 3)
            ),
            Crafting_Recipe(
                "Sulfur Powder",
                [
                    Ingredient(Sulfur_Flakes_Block, 3),
                ],
                output=Ingredient(Sulfur_Powder, 1)
            ),
            Crafting_Recipe(
                "Saltpeter Powder",
                [
                    Ingredient(Saltpeter, 1),
                ],
                output=Ingredient(Saltpeter_Powder, 5)
            ),
            Crafting_Recipe(
                "Coal",
                [
                    Ingredient(Coal_Ore_Block, 1),
                ],
                output=Ingredient(Coal, 1)
            ),
            Crafting_Recipe(
                "Gun Powder",
                [
                    Ingredient(Saltpeter_Powder, 7),
                    Ingredient(Coal, 2),
                    Ingredient(Sulfur_Powder, 1),
                ],
                output=Ingredient(Gunpowder, 1)
            ),
        ]                

        self.additional_possible_recipes = [
            Crafting_Recipe(
                "TNT",
                [
                    Ingredient(Gunpowder, 4),
                    Ingredient(Gravel, 1),
                ],
                output=Ingredient(TNT, 1)
            ),
        ]

        self.discovered_recipes = []
        if discovered_recipes is not None:
            for recipe in discovered_recipes:
                self.append(recipe)
    
    def __getitem__(self, index): # this is the dunder method for the [] operator
        if index < 0:
            return list(self)[index]

        default_recipe_count = len(self.default_crafting_recipes)            
        if index < default_recipe_count: # access additional recipes
            return self.default_crafting_recipes[index]
        else:
            index_offset = index - default_recipe_count
            return self.discovered_recipes[index_offset]

    def __len__(self):
        return len(self.default_crafting_recipes) + len(self.discovered_recipes)

    def __iter__(self): # allows for x in list -> needs tested
        yield from self.default_crafting_recipes
        yield from self.discovered_recipes

    def __contains__(self, recipe): # runs the in operator
        for item in self.default_crafting_recipes:
            if item == recipe:
                return True
        for item in self.discovered_recipes:
            if item == recipe:
                return True
        return False

    def append(self, recipe):
        """appends new recipes onto the list"""
        # step 1: check for if the recipe is in self.additional_possible_recipes and throw error if it isn't (or just don't add)
        if recipe not in self.additional_possible_recipes:
            raise ValueError("Attempted to add invalid recipe to user's crafting recipe list")

        # step 2: blocks adding duplicate recipes silently
        # # this will make it less efficient if there are duplicates but improves user experiences
        if recipe in self:
            return

        # step 3: append recipe onto self.additional_discovered_recipes
        self.discovered_recipes.append(recipe)