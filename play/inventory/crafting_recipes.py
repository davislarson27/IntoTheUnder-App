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

        self.menu_init(screen)
    
    def __getitem__(self, index):
        if index < 0:
            return list(self)[index]

        default_recipe_count = len(self.default_crafting_recipes)            
        if index < default_recipe_count:
            return self.default_crafting_recipes[index]
        else:
            index_offset = index - default_recipe_count
            return self.discovered_recipes[index_offset]

    def __len__(self):
        return len(self.default_crafting_recipes) + len(self.discovered_recipes)

    def __iter__(self):
        yield from self.default_crafting_recipes
        yield from self.discovered_recipes

    def __contains__(self, recipe):
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

    def add_recipe(self, recipe):
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
    

    # ========================== display / menu ========================== #

    def menu_init(self, screen=None):
        self.screen = screen

        # colors
        self.background_color           = (85, 85, 95)
        self.base_box_color             = (200, 200, 200)
        self.selected_box_color         = (246, 246, 246)
        self.inventory_text_color       = (255, 255, 255)
        self.item_mng_background_color  = (77, 77, 87)
        self.section_title_color        = (160, 160, 160)
        self.slot_label_color           = (200, 200, 200)
        self.select_button_color        = (100, 100, 112)
        self.select_button_text         = (240, 240, 240)
        self.recipe_slot_color          = (110, 110, 122)

        # grid unit sizes — mirrors Inventory exactly
        self.tot_columns    = 48
        self.tot_rows       = 48
        self.grid_width_px  = self.screen.get_width()  // self.tot_columns
        self.grid_height_px = self.screen.get_height() // self.tot_rows
        self.box_width      = self.grid_height_px * 4

        # label sizing
        self.label_gap_y   = int(self.grid_height_px * 0.5)
        self.label_height  = max(12, int(self.grid_height_px * 1.0))

        section_label_height = floor(2.4 * self.grid_height_px)

        # item frame sizing — matches inventory's 75% rule
        item_percent_of_box         = 0.75
        self.full_item_size         = floor(self.box_width * item_percent_of_box)
        self.full_item_margin       = floor((self.box_width - self.full_item_size) / 2)

        # fonts
        self.full_inventory_font        = pygame.font.Font(None, floor(self.full_item_size * 0.75))
        self.inventory_item_name_font   = pygame.font.Font(None, 16)
        self.section_label_font         = pygame.font.Font(None, section_label_height)
        self.category_font              = pygame.font.Font(None, floor(1.8 * self.grid_height_px))

        # ── layout measurements ────────────────────────────────────────── #

        exp_display_margin_x     =  3 * self.grid_width_px
        display_grid_margin_x    =  5 * self.grid_width_px
        exp_display_margin_y     =  5 * self.grid_height_px   # top of tab bar
        category_selector_height =  4 * self.grid_height_px
        
        buffer_space_px = 2

        # grid starts below tab bar, with a small breathing gap
        grid_top_gap    = self.grid_height_px * 2            # gap between tab bar bottom and first grid row
        self.grid_top_y = exp_display_margin_y + category_selector_height + grid_top_gap

        # ingredient strip at the bottom — same height as the inventory hot bar
        self.ingr_strip_height  = self.grid_height_px * 7
        self.ingr_strip_top_y   = self.screen.get_height() - self.ingr_strip_height

        # usable vertical space for the recipe grid
        grid_bottom_pad = self.grid_height_px * 3  # breathing room above the strip
        grid_available_h = self.ingr_strip_top_y - self.grid_top_y - grid_bottom_pad

        # grid layout: 8 columns, as many full rows as fit
        self.boxes_per_row  = 8
        max_rows            = 4   # cap rows so slots don't crowd the strip

        # horizontal spacing — mirrors inventory's margin calculation
        grid_usable_w = self.screen.get_width() - (display_grid_margin_x * 2)
        self.margin_between_boxes_x = (
            grid_usable_w - (self.boxes_per_row * self.box_width)
        ) // (self.boxes_per_row - 1)

        # vertical spacing — divide available height evenly across rows
        self.margin_between_boxes_y = (
            grid_available_h - (max_rows * self.box_width)
        ) // (max_rows - 1)  # gap between rows

        self.boxes_high = max_rows

        # ── title label ───────────────────────────────────────────────── #

        section_label_start_height = (exp_display_margin_y - section_label_height) // 3
        display_label_box = pygame.Rect(
            0, section_label_start_height,
            self.screen.get_width(), section_label_height
        )
        self.display_label_text_surface = self.section_label_font.render(
            "The Recipe Center", True, self.section_title_color
        )
        self.display_label_rect = self.display_label_text_surface.get_rect(
            center=display_label_box.center
        )

        # ── category tab bar ──────────────────────────────────────────── #
        categories = ["Materials", "Building", "Items", "Minerals", "Special"]
        self.categories_rects           = []
        self.category_label_surfaces    = []
        self.category_label_rects       = []

        category_selector_width = (
            self.screen.get_width() - (exp_display_margin_x * 2)
        ) // len(categories)

        for i, category in enumerate(categories):
            cur_rect = pygame.Rect(
                exp_display_margin_x + (category_selector_width * i) + buffer_space_px,
                exp_display_margin_y,
                category_selector_width - (buffer_space_px * 2),
                category_selector_height
            )
            self.categories_rects.append(cur_rect)

            surf = self.category_font.render(category, True, self.select_button_text)
            self.category_label_surfaces.append(surf)
            self.category_label_rects.append(surf.get_rect(center=cur_rect.center))

        # ── recipe grid slot rects ────────────────────────────────────── #
        # build hit_box and item_frame for every grid position up front,
        # exactly like the inventory does for expanded_inventory.

        self.recipe_slot_hit_boxes  = []   # pygame.Rect — for click detection
        self.recipe_slot_item_frames = []  # pygame.Rect — where the block icon is drawn
        self.recipe_slot_label_rects = []  # pygame.Rect — name label below slot

        for row in range(self.boxes_high):
            for col in range(self.boxes_per_row):
                x = (
                    display_grid_margin_x
                    + col * (self.box_width + self.margin_between_boxes_x)
                )
                y = (
                    self.grid_top_y
                    + row * (self.box_width + self.margin_between_boxes_y)
                )

                hit_box = pygame.Rect(x, y, self.box_width, self.box_width)

                item_frame = pygame.Rect(
                    x + self.full_item_margin,
                    y + self.full_item_margin,
                    self.full_item_size,
                    self.full_item_size
                )

                label_rect = pygame.Rect(
                    hit_box.x,
                    hit_box.bottom + self.label_gap_y,
                    hit_box.width,
                    self.label_height
                )

                self.recipe_slot_hit_boxes.append(hit_box)
                self.recipe_slot_item_frames.append(item_frame)
                self.recipe_slot_label_rects.append(label_rect)

        self.slots_per_page = self.boxes_per_row * self.boxes_high

        # ── ingredient strip background rect ─────────────────────────── #

        self.ingr_strip_rect = pygame.Rect(
            0,
            self.ingr_strip_top_y,
            self.screen.get_width(),
            self.ingr_strip_height
        )

        # track selected recipe (None = nothing selected)
        self.selected_recipe = None


    # ------------------------------------------------------------------ #
    #  open / close / run                                                  #
    # ------------------------------------------------------------------ #

    def run(self, input):
        self.draw()
        return self

    def open(self):
        self.selected_recipe = None

    def conditional_close(self, input):
        if input.c_keypress or input.escape_keypress:
            self.close()
            return True
        return False

    def close(self):
        self.selected_recipe = None


    # ------------------------------------------------------------------ #
    #  drawing                                                             #
    # ------------------------------------------------------------------ #

    def draw(self):
        self.screen.fill(self.background_color)
        self._draw_title()
        self._draw_category_tabs()
        self._draw_recipe_grid()
        self._draw_ingredient_strip()

    def _draw_title(self):
        self.screen.blit(self.display_label_text_surface, self.display_label_rect)

    def _draw_category_tabs(self):
        for i, rect in enumerate(self.categories_rects):
            pygame.draw.rect(self.screen, self.select_button_color, rect)
            self.screen.blit(self.category_label_surfaces[i], self.category_label_rects[i])

    def _draw_recipe_grid(self):
        all_recipes = list(self)   # iterates default + discovered via __iter__

        for slot_index in range(self.slots_per_page):
            hit_box    = self.recipe_slot_hit_boxes[slot_index]
            item_frame = self.recipe_slot_item_frames[slot_index]
            label_rect = self.recipe_slot_label_rects[slot_index]

            if slot_index >= len(all_recipes):
                # empty slot — draw an outline-only box so the grid shape is clear
                pygame.draw.rect(self.screen, self.recipe_slot_color, hit_box, 1)
                continue

            recipe = all_recipes[slot_index]
            is_selected = (recipe is self.selected_recipe)

            # slot background
            slot_bg = self.selected_box_color if is_selected else self.recipe_slot_color
            pygame.draw.rect(self.screen, slot_bg, hit_box)

            # output block icon
            if recipe.output is not None:
                recipe.output.block_type.draw_manual(
                    self.screen,
                    item_frame.x,
                    item_frame.y,
                    item_frame.width,
                    is_grid_coordinates=False
                )

            # recipe name label below slot
            name_surf = self.inventory_item_name_font.render(
                recipe.name, True, self.slot_label_color
            )
            name_rect = name_surf.get_rect(center=label_rect.center)
            self.screen.blit(name_surf, name_rect)

    def _draw_ingredient_strip(self):
        # darker background to separate it from the grid area
        strip_bg = (60, 60, 70)
        pygame.draw.rect(self.screen, strip_bg, self.ingr_strip_rect)

        # top border line
        pygame.draw.rect(
            self.screen, (40, 40, 50),
            pygame.Rect(0, self.ingr_strip_top_y, self.screen.get_width(), 2)
        )

        if self.selected_recipe is None:
            # placeholder hint text
            hint_surf = self.inventory_item_name_font.render(
                "Select a recipe to see ingredients", True, (130, 130, 140)
            )
            hint_rect = hint_surf.get_rect(center=self.ingr_strip_rect.center)
            self.screen.blit(hint_surf, hint_rect)
            return

        # ── draw selected recipe detail in the strip ─────────────────── #
        # Layout: [output icon + name]  |  [ingr icon x count]  [ingr icon x count] ...
        #          left zone                right zone (one slot per ingredient)

        recipe      = self.selected_recipe
        strip_cx_y  = self.ingr_strip_rect.centery
        icon_size   = self.full_item_size
        icon_margin = self.full_item_margin
        pad_x       = self.grid_width_px * 3

        # output icon on the far left
        out_icon_x = pad_x
        out_icon_y = strip_cx_y - icon_size // 2

        if recipe.output is not None:
            recipe.output.block_type.draw_manual(
                self.screen, out_icon_x, out_icon_y, icon_size,
                is_grid_coordinates=False
            )
            # name below icon
            out_name_surf = self.inventory_item_name_font.render(
                recipe.name, True, self.slot_label_color
            )
            out_name_rect = out_name_surf.get_rect(
                centerx=out_icon_x + icon_size // 2,
                top=out_icon_y + icon_size + 3
            )
            self.screen.blit(out_name_surf, out_name_rect)

            # output count
            out_count_surf = self.full_inventory_font.render(
                f"x{recipe.output.count}", True, (255, 255, 255)
            )
            self.screen.blit(out_count_surf, (out_icon_x, out_icon_y))

        # divider between output and ingredients
        divider_x = out_icon_x + icon_size + self.grid_width_px * 3
        pygame.draw.rect(
            self.screen, (90, 90, 100),
            pygame.Rect(divider_x, self.ingr_strip_top_y + 8, 2, self.ingr_strip_height - 16)
        )

        # ingredients to the right of the divider
        ingr_start_x = divider_x + self.grid_width_px * 3
        ingr_step_x  = self.box_width + self.grid_width_px * 2

        for i, ingredient in enumerate(recipe.requirement_list):
            ix = ingr_start_x + i * ingr_step_x
            iy = strip_cx_y - icon_size // 2

            ingredient.block_type.draw_manual(
                self.screen, ix, iy, icon_size,
                is_grid_coordinates=False
            )

            # count badge
            ingr_count_surf = self.full_inventory_font.render(
                f"x{ingredient.count}", True, (255, 255, 255)
            )
            self.screen.blit(ingr_count_surf, (ix, iy))

            # ingredient name below icon
            ingr_name_surf = self.inventory_item_name_font.render(
                ingredient.block_type.str_name, True, self.slot_label_color
            )
            ingr_name_rect = ingr_name_surf.get_rect(
                centerx=ix + icon_size // 2,
                top=iy + icon_size + 3
            )
            self.screen.blit(ingr_name_surf, ingr_name_rect)