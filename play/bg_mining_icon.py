import pygame

from world.blocks.block_export import *
from .bg_overlay import BG_Overlay

class Bg_Mining_Icon:
    def __init__(self, screen, x, y, icon_width, icon_height):
        self.screen = screen
        self.x = x
        self.y = y

        block_width = icon_width//2

        # draw the active icon
        active_alpha = 235
        self.active_icon_surface = pygame.Surface((icon_width, icon_height), pygame.SRCALPHA).convert_alpha()
        Grass.draw_manual(self.active_icon_surface, 0, 0, block_width, is_grid_coordinates=False)
        Dirt.draw_manual(self.active_icon_surface, 0, block_width, block_width, is_grid_coordinates=False)
        Grass.draw_manual(self.active_icon_surface, block_width, 0, block_width, is_grid_coordinates=False)
        Grass.draw_manual(self.active_icon_surface, block_width, block_width, block_width, is_grid_coordinates=False)
        self.active_icon_surface.set_alpha(active_alpha)

        # draw the inactive icon
        inactive_alpha = 75
        self.inactive_icon_surface = pygame.Surface((icon_width, icon_height), pygame.SRCALPHA).convert_alpha()
        Grass.draw_manual(self.inactive_icon_surface, 0, 0, block_width, is_grid_coordinates=False)
        Dirt.draw_manual(self.inactive_icon_surface, 0, block_width, block_width, is_grid_coordinates=False)
        Grass.draw_manual(self.inactive_icon_surface, block_width, 0, block_width, is_grid_coordinates=False)
        Grass.draw_manual(self.inactive_icon_surface, block_width, block_width, block_width, is_grid_coordinates=False)
        self.inactive_icon_surface.set_alpha(inactive_alpha)

        bg_overlay = BG_Overlay(screen, block_width, None, None)

        exposures = [
            # (0,         0,             False,  True, False,  True),  # top-left:     (x, y, top, bottom, left, right)

            (0,         0,             False,  False, False,  False),  # top-left:     (x, y, top, bottom, left, right)
            (block_width,         0,   False,  True, False,  False),  #               (x, y, top, bottom, left, right)
            (0,         block_width,   False,  False, False,  True),  #               (x, y, top, bottom, left, right)

            # (block_width, block_width, True,  False, True, False), # bottom-right
        ]

        for draw_x, draw_y, top, bottom, left, right in exposures:
            surf = bg_overlay.get_bg_overlay_surface(top, bottom, left, right)
            self.active_icon_surface.blit(surf, (draw_x, draw_y))
            self.inactive_icon_surface.blit(surf, (draw_x, draw_y))


    def draw(self, input):
        if input.caps_lock:
            self.screen.blit(self.active_icon_surface, (self.x, self.y))
        else:
            self.screen.blit(self.inactive_icon_surface, (self.x, self.y))