import pygame
from components.blocks.block_types._base import Explosives

class TNT(Explosives):
    str_name = "TNT"
    ticks_to_mine = 30
    tick_threshold = 160
    ticks_till_physics = 0
    blast_power = 400
    blast_radius = 3
    inventory = None

    def interaction(self, inventory):
        if self.ticks_till_physics == 0: self.ticks_till_physics = 1
        self.inventory = inventory
        return True
        
    def physics(self):
        if self.ticks_till_physics >= self.tick_threshold: # explode :)
            self.explode()
        elif self.ticks_till_physics > 0: # if the counter has started, keep counting up
            self.ticks_till_physics += 1
        

    @staticmethod
    def draw_manual(screen, x, y, block_width, being_mined=False, is_grid_coordinates=True, use_alt_drawing=False):
        added = 20 if being_mined else 0
        if is_grid_coordinates:
            x *= block_width
            y *= block_width

        section_width = int(block_width / 5)
        band_height = 0.24
        band_start_height = (1 - band_height) / 2

        tnt_red_mid    = (180 + added, 34 + added, 34 + added)

        tnt_outline = (50 + added, 45 + added, 45 + added)

        tnt_band = (190 + added, 190 + added, 190 + added)

        # fuse_string = (140, 110, 70)
        # fuse_tip    = (200, 160, 60)
        # spark       = (255, 210, 80)

        pygame.draw.rect( # base red
            screen,
            tnt_red_mid,
            (x, y, block_width, block_width)
        )
        pygame.draw.rect( # outline of whole thing
            screen,
            tnt_outline,
            (x, y, block_width, block_width),
            2
        )
        for i in range(5):
            pygame.draw.rect( # outline of whole thing
                screen,
                tnt_outline,
                (x + (section_width * i), y, section_width, block_width),
                1
            )
        pygame.draw.rect(
            screen,
            tnt_band,
            (x, y + int(block_width * band_start_height), block_width, int(block_width * band_height))
        )

