import pygame
from math import floor
from components.blocks.block_types._base import Block

class Chest(Block):

    # remember to update the blocks_list for loading when you add a new type of block :)

    str_name = "Chest"
    ticks_to_mine = 60

    can_store_items = True
    
    def interaction(self, inventory):
        inventory.open_chest(self.stored_inventory_items)
        return True
    
    def onDestruction(self, inventory): # this needs to get called on each block -> needs to give each item to the inventory
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
        
        pygame.draw.rect( # draw base color
            screen,
            (220 + added_color, 175 + added_color, 138 + added_color),           # color
            (x, y, block_width, block_width)
        )
        pygame.draw.rect( # draw base color
            screen,
            (85 + added_color, 70 + added_color, 55 + added_color),           # color
            (x, y, block_width, block_width),
            2
        )
        pygame.draw.rect( # draw outline
            screen,
            (85 + added_color, 70 + added_color, 55 + added_color),           # color
            (x, y, block_width, block_width),
            floor(block_width * 0.08) # width of border
        )
        pygame.draw.rect( # draw divider between top and bottom of the chest
            screen,
            (85 + added_color, 70 + added_color, 55 + added_color),           # color
            (x, y + floor(block_width * 0.3), block_width, floor(block_width * 0.08))
        )
        pygame.draw.rect(
            screen,
            (140 + added_color, 140 + added_color, 140 + added_color),
            (x + floor(block_width * 0.42), y + floor(block_width * 0.3),floor(block_width * 0.18), floor(block_width * 0.24))
        )
