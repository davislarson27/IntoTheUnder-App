import pygame
from enum import Enum
import random

from ..entity import Entity
from world.blocks.block_export import *

class State_Type(Enum):
    turn = 0
    eat = 1
    wander = 2

class State:
    def __init__(self, state_type, frames_until_action):
        self.state_type = state_type
        self.frames_until_action = frames_until_action

    def do_action(self):
        if self.frames_until_action > 0:
            self.frames_until_action -= 1
            return False
        return True
    

class Blob(Entity):
    """basically a green thing that moves for testing"""

    def initialize_drawing_vars(self):
        self.main_surface = pygame.Surface((self.BLOCK_WIDTH, self.BLOCK_WIDTH), pygame.SRCALPHA)
        color = (200, 200, 200)
        self.main_surface.fill(color)

    def initialize_unique_entity_attrs(self):
        self.face_right = True
        self.path = None

    def draw(self, screen_x=0, screen_y=0):
        hit_box = self.main_surface.get_rect(
            topleft=(self.x - screen_x, self.y - screen_y)
        )
        self.screen.blit(self.main_surface, hit_box)

    # def is_valid_path(self):
    #     if self.path is None:
    #         return False
    #     return True
    
    # def set_path(self):
    #     # goal: move until you hit a block
    #     return

    def pathfind(self, input, physics, dx, dy, cur_y_acceleration, cur_player_speed_x, cur_player_speed_y, jump_is_possible, water_movement):

        # idea: have two parts: is_valid_path, then set_path
        # is_valid_path returns False if the path isn't set or doesn't work anymore
        # set_path runs if is_valid_path returns true and finds a new path to a location it chooses
        block_in_view = False

        view_range = 10
        cur_block_x, cur_block_y = self.get_player_block_coordinates()
        for check_x in range(cur_block_x, cur_block_x + view_range):
            if self.grid.get(check_x, cur_block_y) is not None: # i.e., there is a block to move to
                block_in_view = True
                break
        
        if block_in_view:
            dx += cur_player_speed_x

        return dx, dy, cur_y_acceleration, cur_player_speed_y, water_movement

class Highly_Motivated_Blob(Entity):
    """he may be highly motivated, but maybe isn't the brightest"""

    def initialize_drawing_vars(self):
        self.main_surface = pygame.Surface((self.BLOCK_WIDTH, self.BLOCK_WIDTH), pygame.SRCALPHA)
        color = (200, 200, 200)
        self.main_surface.fill(color)

    def initialize_unique_entity_attrs(self):
        self.face_right = True
        self.target = None
        self.view_range = 10
        self.min_wait = 30
        self.max_wait = 240
        self.stuck_counter = 0
        self.last_x = None
        self.stuck_threshold = 90
        self.state = self.get_next_action()

    def draw(self, screen_x=0, screen_y=0):
        hit_box = self.main_surface.get_rect(
            topleft=(self.x - screen_x, self.y - screen_y)
        )
        self.screen.blit(self.main_surface, hit_box)
    
    def get_direction_to_target(self):
        entity_center = self.x + self.x_size // 2
        target_center = self.target[0] * self.BLOCK_WIDTH + self.BLOCK_WIDTH // 2
        if target_center > entity_center:
            return 1
        elif target_center < entity_center:
            return -1
        return 0

    def is_at_target(self):
        entity_center = self.x + self.x_size // 2
        target_left = self.target[0] * self.BLOCK_WIDTH
        target_right = (self.target[0] + 1) * self.BLOCK_WIDTH
        return target_left <= entity_center < target_right
        
    def find_random_location(self):
        cur_block_x, cur_block_y = self.get_player_block_coordinates()
        random_x = random.randint(0, self.view_range)
        if self.face_right:
            x = min(cur_block_x + random_x, self.grid.width-1)
        else:
            x = max(cur_block_x - random_x, 0)

        y = cur_block_y
        if self.face_right:
            step_direction = 1
        else:
            step_direction = -1

        if random_x == 0:
            return cur_block_x, cur_block_y
        
        for cx in range(cur_block_x, x, step_direction):
            if self.grid.get(cx+step_direction, y) is not None: # on level has a block
                if self.grid.get(cx+step_direction, y-1) is not None: # up one level has a block
                    return cx, y
                else:
                    y-=1
            else:
                if self.grid.get(cx+step_direction, y+1) is None: # if there is a drop in front of the entity
                    if self.grid.get(cx+step_direction, y+2) is None:
                        return cx, y
                    else:
                        y+=1
        return cx+step_direction, y
    
    def get_next_action(self, last_action=None):
        state_type = random.choice([state for state in State_Type if state is not last_action]) # picks random next option, assumes no repeats for this entity
        state_wait = random.randint(self.min_wait, self.max_wait)
        return State(state_type, state_wait)

    def set_next_action(self, last_action=None):
        self.state = self.get_next_action(last_action)
        self.stuck_counter = 0
        self.last_x = None
        if self.state.state_type is State_Type.wander:
            x, y = self.find_random_location()
            self.target = (x, y, self.grid.get(x, y))

    def go_to_target(self, cur_player_speed_x):
        return self.get_direction_to_target() * cur_player_speed_x

    def pathfind(self, input, physics, dx, dy, cur_y_acceleration, cur_player_speed_x, cur_player_speed_y, jump_is_possible, water_movement):
        if self.state.do_action():
            if self.state.state_type is State_Type.turn:
                self.face_right = not self.face_right
                self.set_next_action()
            elif self.state.state_type is State_Type.wander:
                if self.target is None:
                    self.find_random_location()
                elif self.is_at_target():
                    self.set_next_action()
                else:
                    x, y = self.target[0], self.target[1]
                    if self.grid.get(x, y) is not self.target[2]: # if the block changes
                        self.set_next_action()
                    else:
                        # stuck detection
                        if self.last_x == self.x:
                            self.stuck_counter += 1
                            if self.stuck_counter >= self.stuck_threshold:
                                self.set_next_action()
                                return dx, dy, cur_y_acceleration, cur_player_speed_y, water_movement
                        else:
                            self.stuck_counter = 0
                        self.last_x = self.x

                        # jump if there's a 1-block wall ahead
                        cur_block_x, cur_block_y = self.get_player_block_coordinates()
                        direction = self.get_direction_to_target()
                        next_x = cur_block_x + direction
                        if (self.grid.get(next_x, cur_block_y) is not None and
                                self.grid.get(next_x, cur_block_y - 1) is None and
                                not self.is_not_block_below() and
                                jump_is_possible):
                            self.y_vel = physics.JUMP_VELOCITY

                        dx += self.go_to_target(cur_player_speed_x)
            else: # get a new state if there isn't a good state
                self.set_next_action()

        return dx, dy, cur_y_acceleration, cur_player_speed_y, water_movement

class Sheep(Entity):

    def initialize_drawing_vars(self):
        self.main_surface = pygame.Surface((self.BLOCK_WIDTH, self.BLOCK_WIDTH), pygame.SRCALPHA)
        color = (200, 200, 200)
        self.main_surface.fill(color)

    def initialize_unique_entity_attrs(self):
        self.face_right = True
        self.target = None
        self.view_range = 10
        self.min_wait = 30
        self.max_wait = 240
        self.state = self.get_next_action()

    def draw(self, screen_x=0, screen_y=0):
        hit_box = self.main_surface.get_rect(
            topleft=(self.x - screen_x, self.y - screen_y)
        )
        self.screen.blit(self.main_surface, hit_box)
    
    def go_to_target(self):
        pass

    def is_at_target(self):
        pass
        
    def find_grass(self):
        pass

    def find_random_location(self):
        cur_block_x, cur_block_y = self.get_player_block_coordinates()
        if self.face_right:
            random_x = random.randint(0, self.view_range)
            # y = cur_block_y
            # for x in range(cur_block_x, cur_block_x+random_x):
            #     cur_level = self.grid.get(x, y)
            #     down = self.grid.get(x, y+1)
            #     if self.grid.get(x, y+1) is not None:
            #         y = y+1
            #     elif self.grid.get(x, y) is None:
            #         pass
            return random_x

            

    def eat_grass(self):
        if self.target is not None:
            x = self.target[0]
            y = self.target[1]
            if isinstance(self.grid.get(x, y), Grass):
                self.grid.set(x, y, Dirt)
            return True
        else:
            return False
    
    def get_next_action(self, last_action=None):
        state_type = random.choice([state for state in State_Type if state is not last_action]) # picks random next option, assumes no repeats for this entity
        state_wait = random.randint(self.min_wait, self.max_wait)
        return State(state_type, state_wait)

    def set_next_action(self, last_action=None):
        self.state = self.get_next_action(last_action)

    def pathfind(self, input, physics, dx, dy, cur_y_acceleration, cur_player_speed_x, cur_player_speed_y, jump_is_possible, water_movement):
        if self.state.do_action():
            if self.state.state_type is State_Type.turn:
                self.face_right = not self.face_right
                self.set_next_action()
            elif self.state.state_type is State_Type.eat:
                if self.target is None:
                    self.find_grass()
                elif self.is_at_target():
                    self.eat_grass()
                    self.set_next_action()
                else:
                    x, y = self.target[0], self.target[1]
                    if self.grid.get(x, y) is not self.target[2]: # if the block changes
                        self.set_next_action()
                    else: # if the target is still valid
                        self.go_to_target()
            elif self.state.state_type is State_Type.wander:
                if self.target is None:
                    self.find_random_location()
                elif self.is_at_target():
                    self.set_next_action()
                else:
                    x, y = self.target[0], self.target[1]
                    if self.grid.get(x, y) is not self.target[2]: # if the block changes
                        self.set_next_action()
                    else: # if the target is still valid
                        self.go_to_target()
            else: # get a new state if there isn't a good state
                self.set_next_action()

        return dx, dy, cur_y_acceleration, cur_player_speed_y, water_movement
