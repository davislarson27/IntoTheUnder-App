import pygame
from math import floor

from components.blocks.blocks import *
from play.entity_health import Entity_Health


class player_entity():
    """includes user and npc player objects"""

    def __init__(self, grid, screen, player_x_pixel, player_y_pixel, BLOCK_WIDTH, health = 100, player_speed = 4, x_vel = 0, y_vel = 0, x_size = 25, y_size = 25, ticks_falling = 1, ticks_inc = True, inventory_bar_height = 100, health_bar_height = 25):
        MAX_HEALTH = 100
        
        self.grid = grid
        self.screen = screen
        self.x = player_x_pixel
        self.y = player_y_pixel
        self.player_speed = player_speed
        self.x_vel = x_vel
        self.y_vel = y_vel
        self.x_size = x_size
        self.y_size = y_size
        self.ticks_falling = ticks_falling
        self.ticks_inc = ticks_inc
        self.BLOCK_WIDTH = BLOCK_WIDTH
        self.health_bar = Entity_Health(screen, MAX_HEALTH, health, inventory_bar_height, health_bar_height)
        self.take_damage_threshold_velocity = 22
        self.loss_per_velocity = 1


    # needs redone to account for widths and heights
    def is_move_ok(self, x, y):
        if(self.grid.in_bounds(x, y) and (self.grid.get(x, y) is None or self.grid.get(x, y).pass_through)):
            return True
        else: 
            return False

    def get_block_positions(self, x_change=0, y_change=0):
        y_blocks = (floor((self.y + y_change) / self.BLOCK_WIDTH), floor((self.y + y_change + self.y_size - 1) / self.BLOCK_WIDTH))
        x_blocks = (floor((self.x + x_change) / self.BLOCK_WIDTH), floor((self.x + x_change + self.x_size - 1) / self.BLOCK_WIDTH))
        
        # block_position is ((x_min, x_max), (y_min, y_max))
        return (x_blocks, y_blocks)
    
    def is_touching(self, block_positions, Block_Type):
        # if type(self.grid.get(block_positions[0][0], block_positions[1][0])) == Block_Type:
        #     return True
        if type(self.grid.get(block_positions[0][0], block_positions[1][1])) == Block_Type:
            return True
        # if type(self.grid.get(block_positions[0][1], block_positions[1][0])) == Block_Type:
        #     return True
        if type(self.grid.get(block_positions[0][1], block_positions[1][1])) == Block_Type:
            return True
        
        return False
    
    def get_player_physics(self, default_y_acceleration):
        "returns y_accel, x_velocity, y_velocity, jump_is_possible"

        if self.is_touching(self.get_block_positions(), Water):
            new_velocity = Water.velocity_reduction(self.player_speed)
            return Water.accel_reduction(default_y_acceleration), new_velocity, new_velocity, False
        return default_y_acceleration, self.player_speed, 0, True


    
    def is_move_ok_y(self, y_change):
        """returns True if a collision happened"""
        if y_change < 0:
            if self.is_move_ok_y_helper(y_change):
                self.y += y_change
                return False
            return True
        else:
            if self.is_move_ok_y_helper(y_change + self.y_size - 1):
                self.y += y_change
                return False
            else:
                y_change -= 1
                for i in range(floor(y_change)):
                    if self.is_move_ok_y_helper(y_change + self.y_size - 1):
                        self.y += y_change
                    else:
                        y_change -= 1
            return True

    # def is_move_ok_y(self, y_change):
    #     block_positions = self.get_block_positions(0, y_change)
    #     x_min, x_max = block_positions[0][0], block_positions[0][1]
    #     y_min, y_max = block_positions[1][0], block_positions[1][1]

    #     for y in range(y_min, y_max + 1):
    #         for x in range(x_min, x_max + 1):
    #             if not self.is_move_ok(x, y):
    #                 return False
    #     return True

    
    def is_move_ok_y_helper(self, y_change): #uses old logic but still works
        if self.is_move_ok(floor(self.x / self.BLOCK_WIDTH), floor((self.y + y_change) / self.BLOCK_WIDTH)):
            if self.is_move_ok(floor((self.x + self.x_size - 1) / self.BLOCK_WIDTH), floor((self.y + y_change) / self.BLOCK_WIDTH)):
                return True
        return False

    def is_move_ok_x(self, x_change):
        block_positions = self.get_block_positions(x_change, 0)
        x_min, x_max = block_positions[0][0], block_positions[0][1]
        y_min, y_max = block_positions[1][0], block_positions[1][1]

        for y in range(y_min, y_max + 1):
            for x in range(x_min, x_max + 1):
                if not self.is_move_ok(x, y):
                    return False
        return True

    def is_not_block_below(self):
        block_positions = self.get_block_positions(0, 1) #checks for block 1 pixel beneath player
        x_min = block_positions[0][0]
        x_max = block_positions[0][1]
        y_max = block_positions[1][1]

        if self.is_move_ok(x_min, y_max) and self.is_move_ok(x_max, y_max):
            return True
        return False
    
    def reject_block_placement(self, block_x, block_y): #blocks the placement of a block due to overlap
        block_positions = self.get_block_positions(0, 0) #checks for block 1 pixel beneath player
        x_min = block_positions[0][0]
        x_max = block_positions[0][1]
        y_min = block_positions[1][0]
        y_max = block_positions[1][1]

        if x_max == block_x or x_min == block_x:
            if y_max == block_y or y_min == block_y:
                return True
        return False

    def to_dict(self):
        return {
            "player_x_pixel": self.x,
            "player_y_pixel": self.y,
            "player_speed": self.player_speed,
            "x_vel": self.x_vel,
            "y_vel": self.y_vel,
            "x_size": self.x_size,
            "y_size": self.y_size,
            "ticks_falling": self.ticks_falling,
            "ticks_inc": self.ticks_inc,
            "BLOCK_WIDTH": self.BLOCK_WIDTH,
            "health": self.health_bar.get_health()
        }



    def draw(self, screen_x = 0, screen_y = 0):
        pygame.draw.rect(
            self.screen,
            (0, 200, 255), #color
            (self.x - screen_x, self.y - screen_y, self.x_size, self.y_size) #position
        )
        self.health_bar.draw()

class npc_entity(player_entity):
    """base for all npc -> adds decision making trees not necessary for the player"""
    def make_decision():
        pass