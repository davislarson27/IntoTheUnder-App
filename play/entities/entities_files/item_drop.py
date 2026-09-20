import pygame
import random

from ..entity import Entity

class Item_Drop(Entity):
    def initialize_drawing_vars(self):
        self.main_surface = pygame.Surface((self.BLOCK_WIDTH, self.BLOCK_WIDTH), pygame.SRCALPHA)
        color = (200, 200, 200)
        self.main_surface.fill(color)

    def initialize_unique_entity_attrs(self):
        self.x_size = self.BLOCK_WIDTH // 3
        self.y_size = self.BLOCK_WIDTH // 3
    
    def set_block(self, block_type):
        self.block_type = block_type
    
    def draw(self, screen_x=0, screen_y=0):
        hit_box = self.main_surface.get_rect(
            topleft=(self.x - screen_x, self.y - screen_y)
        )
        self.screen.blit(self.main_surface, hit_box)

    def pathfind(self, input, physics, dx, dy, cur_y_acceleration, cur_player_speed_x, cur_player_speed_y, jump_is_possible, water_movement):
        return dx, dy, cur_y_acceleration, cur_player_speed_y, water_movement
