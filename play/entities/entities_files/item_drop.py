import pygame
import random

from ..entity import Entity
from world.blocks.block_export import get_str_to_block

class Item_Drop(Entity):
    def initialize_drawing_vars(self):
        self.main_surface = pygame.Surface((self.BLOCK_WIDTH // 2, self.BLOCK_WIDTH // 2), pygame.SRCALPHA)

    def initialize_unique_entity_attrs(self):
        self.x_size = self.BLOCK_WIDTH // 2
        self.y_size = self.BLOCK_WIDTH
        self.is_collected = False

        self.tick_threshold_to_be_collected = 2

    def set_random_subblock_location(self, set_random_subblock_location=True):
        if set_random_subblock_location:
            self.x = self.x + (random.random() * (self.BLOCK_WIDTH - self.x_size))
        else:
            self.x = self.x - (self.x_size // 2) + ((random.random() - 0.5) * (self.BLOCK_WIDTH - self.x_size))

    def set_initial_velocity(self, init_vel_x, init_vel_y):
        self.dx = init_vel_x
        self.y_vel = init_vel_y

    def set_immunity_threshold(self, threshold):
        self.tick_threshold_to_be_collected = threshold

    def set_block(self, block_type):
        self.block_type = block_type

        key = (block_type, self.BLOCK_WIDTH, False, False)
        if key not in block_type.surfaces:
            block_type.draw_to_surface(self.BLOCK_WIDTH, being_mined=False, use_alt_drawing=False)

        self.main_surface = pygame.transform.smoothscale(block_type.surfaces[key], (self.x_size, self.x_size))

    def execute_collide_with_player(self, player, player_inventory):
        """is executed when a player is touching an entity"""
        # step 1: make sure it isn't somehow collected already and has been dropped for long enough
        if self.is_collected or self.ticks < self.tick_threshold_to_be_collected: return
        # step 2: give the block_type to the player's inventory
        self.is_collected = player_inventory.add_item(self.block_type)

    def is_dead(self):
        return self.is_collected

    def draw(self, screen_x=0, screen_y=0):
        draw_hit_box = self.main_surface.get_rect(
            topleft=(self.x - screen_x, self.y - screen_y)
        )
        cur_surface = pygame.transform.rotate(self.main_surface, -self.ticks)
        self.screen.blit(cur_surface, draw_hit_box)
        self.ticks += 1
        
    def initialize_temp_movement_vars(self, physics):
        dx = self.dx
        dy = 0
        cur_y_acceleration = physics.Y_ACCELERATION // 4
        cur_player_speed_x = self.player_speed
        cur_y_acceleration, cur_player_speed_x, cur_player_speed_y, jump_is_possible = self.get_player_physics(physics.Y_ACCELERATION)
        if cur_player_speed_y > 0: water_movement = True
        else: water_movement = False

        if dx != 0 and (self.get_block_below_right() is not None or self.get_block_below_left() is not None or water_movement):
            if dx > 0:
                dx -= 1
            elif dx < 0:
                dx += 1

        return dx, dy, cur_y_acceleration, cur_player_speed_x, cur_player_speed_y, jump_is_possible, water_movement

    def pathfind(self, input, physics, dx, dy, cur_y_acceleration, cur_player_speed_x, cur_player_speed_y, jump_is_possible, water_movement, player=None):
        if player is None: return dx, dy, cur_y_acceleration, cur_player_speed_y, water_movement
        if not player.inventory.can_add_item(self.block_type): return dx, dy, cur_y_acceleration, cur_player_speed_y, water_movement
        if self.ticks < self.tick_threshold_to_be_collected: return dx, dy, cur_y_acceleration, cur_player_speed_y, water_movement

        can_travel_px = self.BLOCK_WIDTH * 1.5
        travel_speed = 3
        player_center_x, player_center_y = player.get_center_px()
        x_center, y_center = self.get_center_px()
        if abs(x_center - player_center_x) < can_travel_px and abs(y_center - player_center_y) < can_travel_px:
            if self.x > player_center_x:
                dx -= travel_speed
            else:
                dx += travel_speed
                
        return dx, dy, cur_y_acceleration, cur_player_speed_y, water_movement

    # ---------------------------------------------- loading and saving methods ---------------------------------------------- #
    def to_dict(self):
        return {
            "entity_type": type(self).__name__,
            "x_pixel": self.x,
            "y_pixel": self.y,
            "x_vel": self.x_vel,
            "y_vel": self.y_vel,
            "ticks_falling": self.ticks_falling,
            "ticks_inc": self.ticks_inc,
            "is_left_facing": self.is_left_facing,
            "ticks": self.ticks,
            "block_type": self.block_type.str_name,
        }
    
    @classmethod
    def fill_entity_object(cls, entity_dict, grid, screen, block_width):
        x_pixel = entity_dict["x_pixel"]
        y_pixel = entity_dict["y_pixel"]
        x_vel = entity_dict["x_vel"]
        y_vel = entity_dict["y_vel"]
        ticks = entity_dict["ticks"]

        str_to_block = get_str_to_block()
        block_type = str_to_block[entity_dict["block_type"]]
        
        entity_obj = Item_Drop(grid, screen, player_x_pixel=x_pixel, player_y_pixel=y_pixel, x_vel=x_vel, y_vel=y_vel, BLOCK_WIDTH=block_width, ticks=ticks)
        entity_obj.set_block(block_type)
        return entity_obj
