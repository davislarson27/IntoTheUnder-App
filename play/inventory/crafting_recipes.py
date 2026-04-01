import pygame

from world.blocks.block_export import *
from .inventory_item import Inventory_Item


class Crafting_Recipe:
    def __init__(self, recipe_name, requirement_list, output=None):
        self.name = recipe_name
        self.requirement_list = requirement_list # expected to be type list<ingredient>
        self.output = output # expected to be type ingredient

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
    
    def __contains__(self, check_item_type):
        """checks if a block type is part of the recipe"""
        if check_item_type is None: return False # returns false if it is a block
        if not isinstance(check_item_type, type): return False # makes sure it is a class
        if not issubclass(check_item_type, Block): return False # checks if it's a block we're looking at

        for item in self.requirement_list:
            if item.block_type is check_item_type:
                return True
        return False
    
    def __str__(self):
        return self.name

    def can_craft(self, inventory_item_list):
        """takes list of inventory items and returns T/F for if the items are sufficient to allow crafting"""

        # convert input inventory items to consolidated ingredients
        input_ingredients = [] # will take type ingredient
        for item in inventory_item_list:
            if isinstance(item, Inventory_Item) and item.Block_Type in self:
                # ok now it is a valid block -> check for if it is already in the inventory_item_list
                not_added_to_input_ingredients = True
                for input in input_ingredients:
                    if input.block_type is item.Block_Type:
                        input.count += item.count_of_items
                        not_added_to_input_ingredients = False
                        break
                if not_added_to_input_ingredients: # if the input hasn't been added, create an ingredient for it
                    input_ingredients.append(Ingredient(item.Block_Type, item.count_of_items))
                
        # now create a list to "check off" requirments as I go
        slot_complete_list = []
        for item in self.requirement_list:
            slot_complete_list.append(item.count)
        
        # now run through the list and check it off
        for input_ingredient in input_ingredients:
            i = 0
            for req in self.requirement_list:
                if slot_complete_list[i] <= 0:
                    i+=1
                    continue
                if req.block_type is input_ingredient.block_type:
                    slot_complete_list[i] -= input_ingredient.count
                    break
                i+=1

        # now look at if the slot_complete_list is complete
        for count_remaining in slot_complete_list:
            if count_remaining > 0:
                return False
        return True

    def draw(self, screen, x, y, block_width, being_mined=False, is_grid_coordinates=True, use_alt_drawing=False):
        if self.output is not None:
            self.output.block_type.draw_manual(screen, x, y, block_width, being_mined, is_grid_coordinates=False, use_alt_drawing=use_alt_drawing)


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


class User_Crafting_Recipes_List:

    default_crafting_recipes = [
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

    additional_possible_recipes = [
        Crafting_Recipe(
            "TNT",
            [
                Ingredient(Gunpowder, 4),
                Ingredient(Gravel, 1),
            ],
            output=Ingredient(TNT, 1)
        ),
    ]

    def __init__(self, discovered_recipes=None, screen=None):
        self.discovered_recipes = []
        if discovered_recipes is not None:
            for recipe in discovered_recipes:
                self.append(recipe)

        self.menu_init(screen) # keeps menu initialization out of list initalization
    
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

    def add_recipe(self, recipe): # returns True if new reciepe was added, false if not
        if recipe is not None and recipe not in self:
            self.discovered_recipes.append(recipe)
            return True
        return False

    def to_dict(self):
        return {
            "discovered_recipes": [str(recipe) for recipe in self.discovered_recipes]
        }

    def fill_from_dict(self, recipe_dictionary):
        for recipeString in recipe_dictionary["discovered_recipes"]:
            recipe = self.getRecipeFromString(recipeString)
            self.add_recipe(recipe)
    
    @classmethod
    def getRecipeFromString(cls, recipeString):
        for recipe in cls.additional_possible_recipes:
            if str(recipe) == recipeString:
                return recipe
        return None

    @classmethod
    def getFindableRecipesList(cls):
        return cls.additional_possible_recipes

    @classmethod
    def getAllRecipesList(cls):
        return cls.default_crafting_recipes + cls.additional_possible_recipes
    

    # -------------------------- displaying recipes for user -------------------------- #
    def menu_init(self, screen=None):
        # set screen
        self.screen = screen

        # set colors (mostly borrowed from the inventory)
        self.background_color = (30, 30, 30)

        self.base_box_color = (200, 200, 200)
        self.selected_box_color = (246, 246, 246)
        self.inventory_text_color = (255, 255, 255)
        self.hot_bar_background_color = (50, 50, 50)
        self.item_mng_background_color = (77, 77, 87)
        self.side_pannel_background_color = (85, 85, 95)

        self.section_title_color = (160, 160, 160)
        self.slot_label_color = (200, 200, 200)

        # grid sizes
        self.tot_columns = 48
        self.tot_rows = 48
        self.grid_width_px = self.screen.get_width() // self.tot_columns
        self.grid_height_px = self.screen.get_height() // self.tot_rows

        # box dimentions
        self.box_width = self.grid_height_px * 4

        # label (textbox) sizing/spacing
        self.label_gap_y = int(self.grid_height_px * 0.5)
        self.label_height = max(12, int(self.grid_height_px * 1.0))

        section_label_height = floor(2.4 * self.grid_height_px)


        # item frame box details
        item_percent_of_box = 0.75
        full_inventory_item_size = floor(self.box_width * item_percent_of_box) # item is 75% as long as its box is
        full_inventory_item_margin = floor((self.box_width - full_inventory_item_size) / 2)

        # initalize fonts
        self.hot_bar_font = pygame.font.Font(None, 36)  # None = default font, 36 = size
        self.percent_font_of_block_full_inventory = 0.75
        self.full_inventory_font = pygame.font.Font(None, floor(full_inventory_item_size * self.percent_font_of_block_full_inventory))

        self.inventory_item_name_font = pygame.font.Font(None, 16)
        self.hot_bar_name_font = pygame.font.Font(None, 15)
        
        self.section_label = pygame.font.Font(None, section_label_height)


        # initalize key section dimentions
        self.display_height = self.grid_height_px * 7
        # self.display_start_height = self.screen.get_height() - self.inventory_height

        exp_display_margin_x = 2 * self.grid_width_px
        exp_display_margin_y = 7 * self.grid_height_px


        # ingredients display section
        section_label_start_height = (exp_display_margin_y - section_label_height) // 3
        display_label_box = pygame.Rect(
            0,
            section_label_start_height,
            self.screen.get_width(),
            section_label_height
        )
        
        self.display_label_text_surface = self.section_label.render(  # optional: bigger font
            "The Recipe Center",
            True,
            self.section_title_color
        )

        self.display_label_rect = self.display_label_text_surface.get_rect(
            center=display_label_box.center
        )

        # display category selector bar
        category_select_bar_start_height = exp_display_margin_y
        count_of_categories = 5



    def run(self, input):
        self.draw()
        return self

    def open(self):
        return
    
    def conditional_close(self, input):
        if input.c_keypress or input.escape_keypress:
            self.close()
            return True
        else:
            return False

    def close(self):
        return

    def draw(self):
        self.screen.fill(self.background_color)

        # draw label
        self.screen.blit(self.display_label_text_surface, self.display_label_rect)
