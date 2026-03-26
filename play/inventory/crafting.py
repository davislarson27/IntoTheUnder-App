from .inventory_position import Inventory_Position
from .inventory_item import Inventory_Item
from .crafting_recipes import *
from world.blocks.block_export import *


class Crafting_Slots:
    def __init__(self, input_slots):

        def can_craft_more(inventory_object):
            cur_recipe = inventory_object.crafting_object.possible_crafting_recipes[inventory_object.crafting_object.cur_recipe_index]
            crafting_slots = inventory_object.crafting_object.crafting_input_slots
            input_inventory_item_list = [ip.inventory_item for ip in crafting_slots if ip.inventory_item is not None]
            if not cur_recipe.can_craft(input_inventory_item_list):
                inventory_object.crafting_object.check_on_click(inventory_object)

        def recipe_on_click(inventory_object):
            # step 1: make sure there is a recipe selected
            if len(inventory_object.crafting_object.possible_crafting_recipes) == 0: return

            # step 2: remove materials from slots based on recipe
            if self.cur_recipe_index >= len(inventory_object.crafting_object.possible_crafting_recipes): self.cur_recipe_index = 0  # protects against a bad index
            
            selected_recipe = inventory_object.crafting_object.possible_crafting_recipes[self.cur_recipe_index]
            output_object = inventory_object.crafting_object.output_slot.inventory_item
            if output_object is not None and (selected_recipe.output.block_type != output_object.Block_Type or output_object.count_of_items + selected_recipe.output.count > output_object.MAX_ITEMS_IN_INVENTORY_SLOT):
                return
            for recipe_item in selected_recipe.requirement_list:
                removed_item = False
                for slot in self.crafting_input_slots:
                    if isinstance(slot.inventory_item, Inventory_Item) and slot.inventory_item.Block_Type == recipe_item.block_type:
                        if slot.inventory_item.count_of_items >= recipe_item.count:
                            slot.inventory_item.count_of_items -= recipe_item.count
                            if slot.inventory_item.count_of_items == 0:
                                slot.inventory_item = None
                            removed_item = True
                            break
                if not removed_item:
                    return
                
            if inventory_object.crafting_object.output_slot.inventory_item is None:
                inventory_object.crafting_object.output_slot.inventory_item = Inventory_Item(selected_recipe.output.block_type, selected_recipe.output.count)
            else:
                inventory_object.crafting_object.output_slot.inventory_item.add_block(selected_recipe.output.count)

            # runs on click if the recipe is not longer valid
            can_craft_more(inventory_object)

        def output_onclick(inventory_object):
            # stop selection if empty
            if inventory_object.crafting_object.output_slot.inventory_item is None: return

            # step 2: use the inventory_object's add_item object to throw it in to the inventory!
            for i in range(inventory_object.crafting_object.output_slot.inventory_item.count_of_items):
                inventory_object.add_item(inventory_object.crafting_object.output_slot.inventory_item.Block_Type)
            inventory_object.crafting_object.output_slot.inventory_item = None

        def inc_recipe_up(inventory_object):
            if len(self.possible_crafting_recipes) > 0:
                if self.cur_recipe_index == 0:
                    self.cur_recipe_index = len(self.possible_crafting_recipes) - 1
                else:
                    self.cur_recipe_index -= 1

            if len(self.possible_crafting_recipes) > 0:
                self.recipe_slot.inventory_item.set_recipe(self.possible_crafting_recipes[self.cur_recipe_index])
            else:
                self.recipe_slot.inventory_item.set_recipe(None)

        def inc_recipe_down(inventory_object):
            if len(self.possible_crafting_recipes) > 0:
                if self.cur_recipe_index == len(self.possible_crafting_recipes) - 1:
                    self.cur_recipe_index = 0
                else:
                    self.cur_recipe_index += 1

            if len(self.possible_crafting_recipes) > 0:
                self.recipe_slot.inventory_item.set_recipe(self.possible_crafting_recipes[self.cur_recipe_index])
            else:
                self.recipe_slot.inventory_item.set_recipe(None)

        self.crafting_input_slots = []
        for i in range(input_slots):
            self.crafting_input_slots.append(Inventory_Position(None, None))
        self.recipe_slot = Inventory_Position(None, None, False, recipe_on_click)
        self.output_slot = Inventory_Position(None, None, False, output_onclick)
        self.point_up_slot = Inventory_Position(None, None, False, inc_recipe_up, special_color=(145, 150, 155), block_check_on_click=True)
        self.point_down_slot = Inventory_Position(None, None, False, inc_recipe_down, special_color=(145, 150, 155), block_check_on_click=True)

        self.title_label_text_surface = None
        self.section_label_rect = None

        self.craft_label_text_surface = None
        self.craft_label_rect = None

        self.collect_label_text_surface = None
        self.collect_label_rect = None

        self.recipe_name_text_surface = None
        self.recipe_name_rect = None

        self.needed_slots = 5

        self.possible_crafting_recipes = []

        self.cur_recipe_index = 0

        self.crafting_recipes = User_Crafting_Recipes_List()

    def close(self, inventory_object):
        for slot in self.crafting_input_slots:
            if slot.inventory_item is not None:
                for i in range(slot.inventory_item.count_of_items):
                    inventory_object.add_item(slot.inventory_item.Block_Type)
                slot.inventory_item = None
            
        self.possible_crafting_recipes = []
        self.recipe_slot.inventory_item.set_recipe(None) 
        self.cur_recipe_index = 0

        if self.output_slot.inventory_item is not None:
            for i in range(self.output_slot.inventory_item.count_of_items):
                inventory_object.add_item(self.output_slot.inventory_item.Block_Type)
            self.output_slot.inventory_item = None

    def get_cur_recipe(self):
        if self.cur_recipe_index is None or len(self.possible_crafting_recipes) == 0:
            return None
        else:
            return self.possible_crafting_recipes[self.cur_recipe_index]

    def has_enough_blocks(self, block_type, count_required, only_check_slot_index = None):
        if only_check_slot_index is None:
            for slot in self.crafting_input_slots:
                if slot.inventory_item is not None:
                    if block_type == slot.inventory_item.Block_Type and slot.inventory_item.count_of_items >= count_required:
                        return True
            return False
        else:
            slot = self.crafting_input_slots[only_check_slot_index]
            if slot.inventory_item is not None:
                if block_type == slot.inventory_item.Block_Type and slot.inventory_item.count_of_items >= count_required:
                    return True
            return False

    def get_possible_recipes(self):
        input_inventory_item_list = [ip.inventory_item for ip in self.crafting_input_slots if ip.inventory_item is not None]
        return [recipe for recipe in self.crafting_recipes if recipe.can_craft(input_inventory_item_list)]

    def check_on_click(self, inventory_object): # this figures out what recipes apply on each click
        
        self.possible_crafting_recipes = self.get_possible_recipes()

        # reset the active index if it is out of range (otherwise don't touch it)
        if self.cur_recipe_index >= len(self.possible_crafting_recipes): self.cur_recipe_index = 0

        if len(self.possible_crafting_recipes) > 0:
            self.recipe_slot.inventory_item.set_recipe(self.possible_crafting_recipes[self.cur_recipe_index])
        else:
            self.recipe_slot.inventory_item.set_recipe(None)
        
    def get_slots(self):
        i = 0
        return_slots = []
        for i in range(len(self.crafting_input_slots)):
            return_slots.append(self.crafting_input_slots[i])
        return_slots.append(self.recipe_slot)
        return_slots.append(self.output_slot)
        return_slots.append(self.point_up_slot)
        return_slots.append(self.point_down_slot)

        return return_slots

    def draw(self, inventory_object):
        pipe_color = {}

        if len(self.possible_crafting_recipes) > 0:

            cur_slot_index = 0
            input0_active = False
            if self.crafting_input_slots[cur_slot_index].inventory_item is not None:
                found_block = False
                for req in self.possible_crafting_recipes[inventory_object.crafting_object.cur_recipe_index].requirement_list:
                    if req.block_type == self.crafting_input_slots[cur_slot_index].inventory_item.Block_Type:
                        found_block = True
                        input0_active = self.crafting_input_slots[cur_slot_index].inventory_item is not None and self.has_enough_blocks(req.block_type, req.count, cur_slot_index)
                if not found_block:
                    input0_active = False
            else:
                input0_active = False

            cur_slot_index = 2
            input2_active = False
            if self.crafting_input_slots[cur_slot_index].inventory_item is not None:
                found_block = False
                for req in self.possible_crafting_recipes[inventory_object.crafting_object.cur_recipe_index].requirement_list:
                    if req.block_type == self.crafting_input_slots[cur_slot_index].inventory_item.Block_Type:
                        found_block = True
                        input2_active = self.crafting_input_slots[cur_slot_index].inventory_item is not None and self.has_enough_blocks(req.block_type, req.count, cur_slot_index)
                if not found_block:
                    input2_active = False
            else:
                input2_active = False
            
            cur_slot_index = 1
            input_1_active = False
            if self.crafting_input_slots[cur_slot_index].inventory_item is not None:
                found_block = False
                for req in self.possible_crafting_recipes[inventory_object.crafting_object.cur_recipe_index].requirement_list:
                    if req.block_type == self.crafting_input_slots[cur_slot_index].inventory_item.Block_Type:
                        found_block = True
                        input_1_active = self.crafting_input_slots[cur_slot_index].inventory_item is not None and self.has_enough_blocks(req.block_type, req.count, cur_slot_index)
                if not found_block:
                    input_1_active = False
            else:
                input_1_active = False


            if input0_active:
                pipe_color[0] = inventory_object.pipe_color_active

            if input2_active:
                pipe_color[1] = inventory_object.pipe_color_active

            if input0_active or input2_active or input_1_active:
                pipe_color[2] = inventory_object.pipe_color_active

                if self.output_slot.inventory_item is not None:
                    pipe_color[3] = inventory_object.pipe_color_active

        cur_recipes = inventory_object.crafting_object.get_possible_recipes()
        cur_index = inventory_object.crafting_object.cur_recipe_index
        if cur_index is not None and len(cur_recipes) > 0:
            cur_recipe = cur_recipes[cur_index]
            output_object = inventory_object.crafting_object.output_slot.inventory_item
            if output_object is not None and (cur_recipe.output.block_type != output_object.Block_Type or output_object.count_of_items + cur_recipe.output.count > output_object.MAX_ITEMS_IN_INVENTORY_SLOT):
                pipe_color[3] = inventory_object.pipe_color_inactive
             
        
        for i in range(len(inventory_object.crafting_flow_rects)):
            pipe_color[i] = pipe_color.get(i, inventory_object.pipe_color_inactive)

        i = 0
        for rect in inventory_object.crafting_flow_rects:
            pygame.draw.rect(inventory_object.screen, pipe_color[i], rect)
            i+=1

        # ----------------------------- custom crafting labels ----------------------------- #

        screen = inventory_object.screen

        # static labels
        if self.craft_label_text_surface is not None and self.craft_label_rect is not None:
            screen.blit(self.craft_label_text_surface, self.craft_label_rect)

        if self.collect_label_text_surface is not None and self.collect_label_rect is not None:
            screen.blit(self.collect_label_text_surface, self.collect_label_rect)

        # dynamic recipe name (above center slot up arrow)
        if self.recipe_name_rect is not None:

            cur_recipe = self.get_cur_recipe()

            if cur_recipe is not None:
                recipe_name = cur_recipe.name
            else:
                recipe_name = "None"

            # render the two lines
            recipe_label_surface = inventory_object.inventory_item_name_font.render(
                "Recipe:",
                True,
                inventory_object.slot_label_color
            )

            recipe_name_surface = inventory_object.inventory_item_name_font.render(
                recipe_name,
                True,
                inventory_object.slot_label_color
            )

            # position them
            recipe_label_rect = recipe_label_surface.get_rect(
                center=(self.recipe_name_rect.centerx, self.recipe_name_rect.centery - self.recipe_name_rect.height // 4)
            )

            recipe_name_rect = recipe_name_surface.get_rect(
                center=(self.recipe_name_rect.centerx, self.recipe_name_rect.centery + self.recipe_name_rect.height // 4)
            )

            # draw
            screen.blit(recipe_label_surface, recipe_label_rect)
            screen.blit(recipe_name_surface, recipe_name_rect)

    def get_recipes_dict(self):
        return self.crafting_recipes.to_dict()

    def setRecipesFromDict(self, recipeDict): # fills crafting_recipes with recipes in the save file 
        self.crafting_recipes.fill_from_dict(recipeDict)

    def add_recipe(self, recipe):
        self.crafting_recipes.add_recipe(recipe)
    