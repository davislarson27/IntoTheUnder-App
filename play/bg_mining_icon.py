import pygame

from world.blocks.block_export import *

class Bg_Mining_Icon:
    def __init__(self, screen, x, y, icon_width, icon_height):
        self.screen = screen
        self.x = x
        self.y = y

        # draw the active icon
        self.active_icon_surface = pygame.surface((icon_width, icon_height), pygame.SRCALPHA).convert_alpha()
        Rock.draw_manual(self.active_icon_surface, 0, 0, icon_width//2, is_grid_coordinates=False)
        Rock.draw_manual(self.active_icon_surface, 0, icon_width//2, icon_width//2, is_grid_coordinates=False)
        Rock.draw_manual(self.active_icon_surface, icon_width//2, 0, icon_width//2, is_grid_coordinates=False)
        Rock.draw_manual(self.active_icon_surface, icon_width//2, icon_width//2, icon_width//2, is_grid_coordinates=False)

        # draw the inactive icon
        inactive_alpha = 200
        self.inactive_icon_surface = pygame.surface((icon_width, icon_height), pygame.SRCALPHA).convert_alpha()
        Rock.draw_manual(self.inactive_icon_surface, 0, 0, icon_width//2, is_grid_coordinates=False)
        Rock.draw_manual(self.inactive_icon_surface, 0, icon_width//2, icon_width//2, is_grid_coordinates=False)
        Rock.draw_manual(self.inactive_icon_surface, icon_width//2, 0, icon_width//2, is_grid_coordinates=False)
        Rock.draw_manual(self.inactive_icon_surface, icon_width//2, icon_width//2, icon_width//2, is_grid_coordinates=False)
        self.inactive_icon_surface.set_alpha(inactive_alpha)


    def draw(self, input):
        if input.caps_lock:
            self.screen.blit(self.active_icon_surface, (self.x, self.y))
        else:
            self.screen.blit(self.inactive_icon_surface, (self.x, self.y))