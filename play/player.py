import pygame
from math import floor, pi

from world.blocks.block_export import *
from play.entity_health import Entity_Health


class Player:
    def __init__(self, grid, screen, player_x_pixel, player_y_pixel, BLOCK_WIDTH, health = 100, player_speed = 4, x_vel = 0, y_vel = 0, x_size = 25, y_size = 25, ticks_falling = 1, ticks_inc = True, inventory_bar_height = 100, health_bar_height = 25, images = None, is_left_facing = True):
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
        self.images = images
        self.is_left_facing = is_left_facing

        self.dx = 0


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
        if issubclass(type(self.grid.get(block_positions[0][0], block_positions[1][1])), Block_Type):
            return True
        # if type(self.grid.get(block_positions[0][1], block_positions[1][0])) == Block_Type:
        #     return True
        if issubclass(type(self.grid.get(block_positions[0][1], block_positions[1][1])), Block_Type):
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
            "health": self.health_bar.get_health(),
            "is_left_facing": self.is_left_facing
        }

    
    def get_direction(self, distance_move_x, player_screen_x, mouse_pos_x, is_interacting):
        if is_interacting:
            if self.is_left_facing: # check for if the player is facing left and the mouse is on the right
                if mouse_pos_x > player_screen_x + self.y_size:
                    self.is_left_facing = False
            else:
                if mouse_pos_x < player_screen_x:
                    self.is_left_facing = True
        else:
            distance_move_x
            if self.is_left_facing:
                if distance_move_x > 0:
                    self.is_left_facing = False
            else:
                if distance_move_x < 0:
                    self.is_left_facing = True
    

    def draw(self, screen_x = 0, screen_y = 0):

        # pygame.draw.rect(
        #     self.screen,
        #     (0, 200, 255), #color
        #     (self.x - screen_x, self.y - screen_y, self.x_size, self.y_size) #position
        # )

        if self.is_left_facing:
            player_rect = self.images.player_left.get_rect(
                topleft=(self.x - screen_x, self.y - screen_y)
            )
            self.screen.blit(self.images.player_left, player_rect)
        else:
            player_rect = self.images.player_right.get_rect(
                topleft=(self.x - screen_x, self.y - screen_y)
            )
            self.screen.blit(self.images.player_right, player_rect)


        # self.health_bar.draw()


    # ----------------------------- runs player physics ----------------------------- #
    def move(self, input, physics): # returns assessed damage object
        # ---------------------- step 1: set cur iteration variables ---------------------- #
        dx = 0
        dy = 0
        cur_y_acceleration = physics.Y_ACCELERATION
        cur_player_speed_x = self.player_speed
        cur_y_acceleration, cur_player_speed_x, cur_player_speed_y, jump_is_possible = self.get_player_physics(physics.Y_ACCELERATION)
        if cur_player_speed_y > 0: water_movement = True
        else: water_movement = False


        # ---------------------- step 2: process input ---------------------- #
        if input.a_hold > 0:
            dx -= cur_player_speed_x
        if input.d_hold > 0:
            dx += cur_player_speed_x 
        if input.w_hold > 0 or input.space_hold > 0:
            if not self.is_not_block_below() and jump_is_possible: # add jump_is_possible
                self.y_vel = physics.JUMP_VELOCITY
                self.ticks_falling = 1
                self.ticks_inc = False
            if water_movement:
                cur_y_acceleration = physics.WATER_UPWARD_ACCEL
        if input.s_hold > 0:
            if water_movement: 
                self.y_vel = cur_player_speed_y

        # ---------------------- step 3: move ---------------------- #
        # apply gravity and jumping
        if self.y_vel + (cur_y_acceleration * self.ticks_falling) < self.BLOCK_WIDTH: #limits gravity at 1 block per tick
            dy += self.y_vel + (cur_y_acceleration * self.ticks_falling)


        # check if motion is legal
        if water_movement: dy *= 0.4
        collided = self.is_move_ok_y(dy)

        # if collided and dy > 0 and abs(player.y_vel) > player.take_damage_threshold_velocity:
        #     print("executed")
        #     if player.health_bar.health > 0: player.health_bar.health -= player.loss_per_velocity * (abs(player.y_vel) - player.take_damage_threshold_velocity )

        x_move = abs(dx)
        if dx < 0: x_direction = -1
        else: x_direction = 1
        while x_move >= 0:
            if self.is_move_ok_x(x_move * x_direction):
                self.x += (x_move * x_direction)
                break
            x_move -= 1

        # increment gravity
        if dy == 0:
            self.y_vel = 0
            self.ticks_falling = 1
        else:
            self.y_vel += cur_y_acceleration
            if self.ticks_inc:
                self.ticks_falling += 1
            else:
                self.ticks_inc = True

        self.dx = dx
