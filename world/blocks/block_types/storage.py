import pygame
from math import floor, cos, sin, pi
from world.blocks.block_types._base import Block

class Chest(Block):

    # remember to update the blocks_list for loading when you add a new type of block :)

    str_name = "Chest"
    ticks_to_mine = 60

    can_store_items = True
    chest_cols = 3 # the number for how many chest slots exist and their layout exists here
    chest_rows = 4 # the number for how many chest slots exist and their layout exists here
    chest_slots_count = chest_cols * chest_rows

    def interaction(self, player):
        player.inventory.open_chest(self.stored_inventory_items)
        return True

    def onDestroy(self, inventory): # this needs to get called on each block -> needs to give each item to the inventory
        for item in self.stored_inventory_items:
            if item is not None:
                for i in range(item.count_of_items):
                    inventory.add_item(item.Block_Type)
        self.stored_inventory_items = []
        block_type = type(self)
        self.grid.set(self.x, self.y, None)
        return block_type


    @staticmethod
    def draw_manual(screen, x, y, block_width, being_mined=False, is_grid_coordinates=True, use_alt_drawing=False):
        if being_mined:
            added_color = 20
        else:
            added_color = 0

        if is_grid_coordinates:
            x *= block_width
            y *= block_width

        primary_bg_color = (220, 175, 138)
        outline_color = (85, 70, 55)
        latch_color = (140, 140, 140)

        pygame.draw.rect( # draw base color
            screen,
            (primary_bg_color[0] + added_color, primary_bg_color[1] + added_color, primary_bg_color[2] + added_color),
            (x, y, block_width, block_width)
        )
        pygame.draw.rect( # draw outline
            screen,
            (outline_color[0] + added_color, outline_color[1] + added_color, outline_color[2] + added_color),
            (x, y, block_width, block_width),
            floor(block_width * 0.08) # width of border
        )
        pygame.draw.rect( # draw divider between top and bottom of the chest
            screen,
            (outline_color[0] + added_color, outline_color[1] + added_color, outline_color[2] + added_color),
            (x, y + floor(block_width * 0.3), block_width, floor(block_width * 0.08))
        )
        pygame.draw.rect( # draw the latch
            screen,
            (latch_color[0] + added_color, latch_color[1] + added_color, latch_color[2] + added_color),
            (x + floor(block_width * 0.42), y + floor(block_width * 0.3),floor(block_width * 0.18), floor(block_width * 0.24))
        )

class Spruce_Chest(Chest):

    # remember to update the blocks_list for loading when you add a new type of block :)

    str_name = "Spruce Chest"
    ticks_to_mine = 60

    can_store_items = True
    
    def interaction(self, player):
        player.inventory.open_chest(self.stored_inventory_items)
        return True

    def onDestroy(self, inventory): # this needs to get called on each block -> needs to give each item to the inventory
        for item in self.stored_inventory_items:
            if item is not None:
                for i in range(item.count_of_items):
                    inventory.add_item(item.Block_Type)
        self.stored_inventory_items = []
        block_type = type(self)
        self.grid.set(self.x, self.y, None)
        return block_type


    @staticmethod
    def draw_manual(screen, x, y, block_width, being_mined=False, is_grid_coordinates=True, use_alt_drawing=False):
        if being_mined:
            added_color = 20
        else:
            added_color = 0

        if is_grid_coordinates:
            x *= block_width
            y *= block_width

        primary_bg_color = (100,  91,  85)
        outline_color    = ( 66,  60,  57)
        latch_color      = (205, 190, 125)

        pygame.draw.rect( # draw base color
            screen,
            (primary_bg_color[0] + added_color, primary_bg_color[1] + added_color, primary_bg_color[2] + added_color),
            (x, y, block_width, block_width)
        )
        pygame.draw.rect( # draw outline
            screen,
            (outline_color[0] + added_color, outline_color[1] + added_color, outline_color[2] + added_color),
            (x, y, block_width, block_width),
            floor(block_width * 0.08) # width of border
        )
        pygame.draw.rect( # draw divider between top and bottom of the chest
            screen,
            (outline_color[0] + added_color, outline_color[1] + added_color, outline_color[2] + added_color),
            (x, y + floor(block_width * 0.3), block_width, floor(block_width * 0.08))
        )
        pygame.draw.rect( # draw the latch
            screen,
            (latch_color[0] + added_color, latch_color[1] + added_color, latch_color[2] + added_color),
            (x + floor(block_width * 0.42), y + floor(block_width * 0.3),floor(block_width * 0.18), floor(block_width * 0.24))
        )

class Mahogany_Chest(Chest):

    # remember to update the blocks_list for loading when you add a new type of block :)

    str_name = "Mahogany Chest"
    ticks_to_mine = 60

    can_store_items = True

    def interaction(self, player):
        player.inventory.open_chest(self.stored_inventory_items)
        return True

    def onDestroy(self, inventory): # this needs to get called on each block -> needs to give each item to the inventory
        for item in self.stored_inventory_items:
            if item is not None:
                for i in range(item.count_of_items):
                    inventory.add_item(item.Block_Type)
        self.stored_inventory_items = []
        block_type = type(self)
        self.grid.set(self.x, self.y, None)
        return block_type


    @staticmethod
    def draw_manual(screen, x, y, block_width, being_mined=False, is_grid_coordinates=True, use_alt_drawing=False):
        if being_mined:
            added_color = 20
        else:
            added_color = 0

        if is_grid_coordinates:
            x *= block_width
            y *= block_width

        primary_bg_color = (158,  86,  60)
        outline_color    = (88,  62,  45)
        latch_color      = (150, 140, 140)

        pygame.draw.rect( # draw base color
            screen,
            (primary_bg_color[0] + added_color, primary_bg_color[1] + added_color, primary_bg_color[2] + added_color),
            (x, y, block_width, block_width)
        )
        pygame.draw.rect( # draw outline
            screen,
            (outline_color[0] + added_color, outline_color[1] + added_color, outline_color[2] + added_color),
            (x, y, block_width, block_width),
            floor(block_width * 0.08) # width of border
        )
        pygame.draw.rect( # draw divider between top and bottom of the chest
            screen,
            (outline_color[0] + added_color, outline_color[1] + added_color, outline_color[2] + added_color),
            (x, y + floor(block_width * 0.3), block_width, floor(block_width * 0.08))
        )
        pygame.draw.rect( # draw the latch
            screen,
            (latch_color[0] + added_color, latch_color[1] + added_color, latch_color[2] + added_color),
            (x + floor(block_width * 0.42), y + floor(block_width * 0.3),floor(block_width * 0.18), floor(block_width * 0.24))
        )

class Enduring_Chest(Block):

    # remember to update the blocks_list for loading when you add a new type of block :)

    str_name = "Enduring Chest"
    ticks_to_mine = 90

    can_store_items = True
    
    def interaction(self, player):
        player.inventory.open_enduring_chest(self.stored_inventory_items)
        return True

    @staticmethod
    def draw_manual(screen, x, y, block_width, being_mined=False, is_grid_coordinates=True, use_alt_drawing=False): 
        if being_mined:
            added_color = 20
        else:
            added_color = 0

        if is_grid_coordinates:
            x *= block_width
            y *= block_width

        primary_bg_color = (145, 155, 165)
        outline_color = (95, 100, 102)
        latch_color = (30, 155, 90)
        primary_bg_color = (220, 175, 138)
        outline_color = (85, 70, 55)

        pygame.draw.rect( # draw base color
            screen,
            (primary_bg_color[0] + added_color, primary_bg_color[1] + added_color, primary_bg_color[2] + added_color),
            (x, y, block_width, block_width)
        )
        pygame.draw.rect( # draw outline
            screen,
            (outline_color[0] + added_color, outline_color[1] + added_color, outline_color[2] + added_color),
            (x, y, block_width, block_width),
            floor(block_width * 0.08) # width of border
        )
        pygame.draw.rect( # draw divider between top and bottom of the chest
            screen,
            (outline_color[0] + added_color, outline_color[1] + added_color, outline_color[2] + added_color),
            (x, y + floor(block_width * 0.3), block_width, floor(block_width * 0.08))
        )
        latch_cx = x + floor(block_width * 0.51)
        latch_cy = y + floor(block_width * 0.42)
        latch_hw = floor(block_width * 0.10)
        latch_hh = floor(block_width * 0.13)
        latch_draw_color = (latch_color[0] + added_color, latch_color[1] + added_color, latch_color[2] + added_color)
        diamond_points = [
            (latch_cx, latch_cy - latch_hh),
            (latch_cx + latch_hw, latch_cy),
            (latch_cx, latch_cy + latch_hh),
            (latch_cx - latch_hw, latch_cy),
        ]
        pygame.draw.polygon(screen, latch_draw_color, diamond_points)
        shine_color = (min(255, latch_color[0] + added_color + 120), min(255, latch_color[1] + added_color + 90), min(255, latch_color[2] + added_color + 90))
        pygame.draw.line(
            screen, shine_color,
            (latch_cx - floor(latch_hw * 0.55), latch_cy - floor(latch_hh * 0.3)),
            (latch_cx - floor(latch_hw * 0.1), latch_cy - floor(latch_hh * 0.65)),
            max(1, floor(block_width * 0.025))
        )

class Recipe_Frame(Block):
    
    # remember to update the blocks_list for loading when you add a new type of block :)

    str_name = "Recipe Frame"
    ticks_to_mine = 35
    tick_threshold = 20

    can_store_items = True

    def hasCraftingRecipe(self): # helper function
        from play.inventory.submenus.crafting_recipes import Crafting_Recipe
        if len(self.stored_inventory_items) == 1 and isinstance(self.stored_inventory_items[0], Crafting_Recipe):
            return True
        return False
    
    def interaction(self, player):
        if self.hasCraftingRecipe():
            self.ticks_till_physics = 1
            self.inventory = player.inventory
            return True
        else:
            return False
    
    def physics(self): # runs animation counter for this case
        if self.hasCraftingRecipe() and self.ticks_till_physics > 0: # blocks physics (or animation in this case) if there is no recipe
            self.ticks_till_physics += 1

        if self.ticks_till_physics == self.tick_threshold: # this will add the recipe when it is done
            self.ticks_till_physics = 0
            self.addRecipe()

    def addRecipe(self, inventory=None):
        if self.inventory is None:
            self.inventory = inventory
        self.inventory.add_recipe(self.stored_inventory_items[0])
        self.stored_inventory_items.pop()

    def onDestroy(self, inventory): # this needs to get called on each block -> needs to give each item to the inventory
        if len(self.stored_inventory_items) > 0: self.addRecipe(inventory)
        self.grid.set(self.x, self.y, None)
        return type(self)
    
    def drawDependentDetails(self, screen, x, y, block_width, being_mined=False, is_grid_coordinates=True, use_alt_drawing=False):
        if is_grid_coordinates:
            x *= block_width
            y *= block_width

        block_width_percentage = 0.6
        sub_block_width = block_width * block_width_percentage
        position_offset = int(block_width * ((1 - block_width_percentage) / 2))
        sub_x = x + position_offset
        sub_y = y + position_offset

        # draws crafting recipe output on block
        if self.hasCraftingRecipe():
            self.stored_inventory_items[0].draw(screen, sub_x, sub_y, sub_block_width, is_grid_coordinates=False)
            self.animation(screen, sub_x, sub_y, sub_block_width, is_grid_coordinates=False)            

    def animation(self, screen, x, y, block_width, being_mined=False, is_grid_coordinates=True, use_alt_drawing=False):
        """responsible for drawing animations"""
        if self.ticks_till_physics == 0: # no animation if physics are not running
            return
        
        def draw_ray(screen, cx, cy, angle, length, color, start_distance=0, thickness=1): # helper function for drawing the reys outward
            """draws rays, angle is measured in radians"""

            # start point (offset from center)
            start_x = cx + cos(angle) * start_distance
            start_y = cy + sin(angle) * start_distance

            # end point (continues outward)
            end_x = start_x + cos(angle) * length
            end_y = start_y + sin(angle) * length

            pygame.draw.line(
                screen,
                color,
                (start_x, start_y),
                (end_x, end_y),
                thickness
            )

        # set ray color
        rayColor = (245, 225, 140)

        # calculate ray length
        maxRayLength = int(block_width * 0.6)

        maxPositionPercent = 0.65
        ticksToEndGrowth = int(self.tick_threshold * maxPositionPercent)
        percentGrown = min((self.ticks_till_physics - 1) / ticksToEndGrowth, 1)
        rayLength = int(maxRayLength * percentGrown)

        # calculate ray position
        rayCount = 5
        anglePerRay = 2 * pi / rayCount
        offsetFromStart = 0
        startDistanceFromCenter = block_width + int(block_width * 0.2)

        center_x = x + block_width // 2
        center_y = y + block_width // 2

        # draw rays
        for i in range(rayCount):
            curAngle = (anglePerRay * i) + offsetFromStart
            draw_ray(screen, center_x, center_y, curAngle, rayLength, rayColor, startDistanceFromCenter)
        
        # draw short rays
        shortRayOffSet = anglePerRay / 2
        shortRayMaxPercent = 0.75
        shortRayLength = min(shortRayMaxPercent * maxRayLength, rayLength)
        for i in range(rayCount):
            curAngle = (anglePerRay * i) + shortRayOffSet
            draw_ray(screen, center_x, center_y, curAngle, shortRayLength, rayColor, startDistanceFromCenter)

    @staticmethod
    def draw_manual(screen, x, y, block_width, being_mined=False, is_grid_coordinates=True, use_alt_drawing=False): 
        if being_mined:
            added_color = 20
        else:
            added_color = 0

        if is_grid_coordinates:
            x *= block_width
            y *= block_width

        paper_color = (
            min(255, 225 + added_color),
            min(255, 205 + added_color),
            min(255, 170 + added_color)
        )
        border_color = (
            min(255, 120 + added_color),
            min(255, 100 + added_color),
            min(255, 80 + added_color)
        )
        line_color = (
            min(255, 160 + added_color),
            min(255, 140 + added_color),
            min(255, 110 + added_color)
        )

        # base
        pygame.draw.rect(screen, paper_color, (x, y, block_width, block_width))

        # border
        border_thickness = max(1, block_width // 10)
        pygame.draw.rect(screen, border_color, (x, y, block_width, block_width), border_thickness)

        # inner frame
        margin = max(2, block_width // 6)
        inner_x = x + margin
        inner_y = y + margin
        inner_w = block_width - margin * 2
        inner_h = block_width - margin * 2

        if inner_w > 4 and inner_h > 4:
            pygame.draw.rect(screen, border_color, (inner_x, inner_y, inner_w, inner_h), 1)

            # two simple horizontal lines
            line1_y = inner_y + inner_h // 3
            line2_y = inner_y + (inner_h * 2) // 3

            pygame.draw.line(screen, line_color, (inner_x + 2, line1_y), (inner_x + inner_w - 3, line1_y), 1)
            pygame.draw.line(screen, line_color, (inner_x + 2, line2_y), (inner_x + inner_w - 3, line2_y), 1)

            # tiny center mark
            mark_size = max(2, block_width // 8)
            mark_x = x + (block_width - mark_size) // 2
            mark_y = y + (block_width - mark_size) // 2
            pygame.draw.rect(screen, border_color, (mark_x, mark_y, mark_size, mark_size), 1)
