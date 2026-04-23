import pygame
from world.blocks.block_types._base import Block

class Glass(Block):

    # remember to update the blocks_list for loading when you add a new type of block :)

    str_name = "Glass"
    ticks_to_mine = 15

    draw_background = True
    ignore_shading_from = {
        (0, 1): True, # coming from the top
        (0, -1): True, # coming from the bottom
        (1, 0): True, # coming from the right
        (-1, 0): True # comin from the left
    }


    @staticmethod
    def draw_manual(screen, x, y, block_width, being_mined=False, is_grid_coordinates=True, use_alt_drawing=False):
        if being_mined:
            added_color = 20
        else:
            added_color = 0

        if is_grid_coordinates:
            x *= block_width
            y *= block_width

        # new warmer and lighter colors
        primary_background_color = (215, 215, 220, 50)
        detail_color = (180, 180, 185, 65)

        pygame.draw.rect(
            screen,
            (primary_background_color[0] + added_color, primary_background_color[1] + added_color, primary_background_color[2] + added_color, primary_background_color[3]),
            (x, y, block_width, block_width)
        )
        pygame.draw.rect(
            screen,
            (detail_color[0] + added_color, detail_color[1] + added_color, detail_color[2] + added_color, primary_background_color[3]),
            ((x) + (block_width // 10) , (y) + (block_width // 10), block_width // 4, block_width // 4)
        )

    def onDestroy(self, inventory=None):
        self.grid.set(self.x, self.y, None)
        return None
