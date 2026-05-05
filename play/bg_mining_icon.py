import pygame

from world.blocks.block_export import *
from .bg_overlay import BG_Overlay

class Bg_Mining_Icon:
    def __init__(self, screen, x, y, icon_width, icon_height):
        # region set attributes
        self.screen = screen
        self.x = x
        self.y = y

        block_width = (icon_width * 2) // 3
        self.foreground_block_offset_position = icon_width - block_width
        # endregion

        # region set surfaces
        self.foreground_icon = pygame.Surface((block_width, block_width), pygame.SRCALPHA).convert_alpha()
        self.background_icon_active = pygame.Surface((block_width, block_width), pygame.SRCALPHA).convert_alpha()
        self.background_icon_inactive = pygame.Surface((block_width, block_width), pygame.SRCALPHA).convert_alpha()
        # endregion

        # region set blocks
        Grass.draw_manual(self.background_icon_active, 0, 0, block_width, is_grid_coordinates=False)
        Grass.draw_manual(self.background_icon_inactive, 0, 0, block_width, is_grid_coordinates=False)
        Grass.draw_manual(self.foreground_icon, 0, 0, block_width, is_grid_coordinates=False)
        # endregion

        # region bg overlays
        exposures = [ # not drawing correctly at the moment
            (0, 0, False, True, False, True),  # top-left corner of bg: shadow on bottom + right (where fg overlaps)
        ]
        bg_overlay = BG_Overlay(screen, block_width, None, None)

        for draw_x, draw_y, top, bottom, left, right in exposures:
            surf = bg_overlay.get_bg_overlay_surface(top, bottom, left, right)
            self.background_icon_active.blit(surf, (draw_x, draw_y))
            self.background_icon_inactive.blit(surf, (draw_x, draw_y))
        # endregion

        # region set alpha
        active_alpha = 230
        inactive_alpha = 85

        self.background_icon_active.set_alpha(active_alpha)
        self.background_icon_inactive.set_alpha(inactive_alpha)
        # endregion

    def draw(self, input):
        if input.caps_lock:
            self.screen.blit(self.background_icon_active, (self.x, self.y))
        else:
            self.screen.blit(self.background_icon_inactive, (self.x, self.y))
        
        self.screen.blit(self.foreground_icon, (self.x+self.foreground_block_offset_position, self.y+self.foreground_block_offset_position))
