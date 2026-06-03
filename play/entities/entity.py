from math import floor

from world.blocks.block_export import *
from play.entity_health import Entity_Health
from world.grid import Grid


class Entity:
    def __init__(self, grid, screen, player_x_pixel, player_y_pixel, BLOCK_WIDTH, health=100, energy=100, player_speed=4, x_vel=0, y_vel=0, x_size=25, y_size=25, ticks_falling=0, ticks_inc=False, inventory_bar_height=100, health_bar_height=25, images=None, is_left_facing=True, player_spawn_x=None, player_spawn_y=None, world_details=None, can_take_fall_damage=True):
        MAX_HEALTH = 100
        MAX_ENERGY = 100
        
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
        self.health_bar = Entity_Health(screen, MAX_HEALTH, health, MAX_ENERGY, energy, images)
        self.take_damage_threshold_velocity = 22
        self.loss_per_velocity = 1
        self.images = images
        self.is_left_facing = is_left_facing
        self.can_take_fall_damage = can_take_fall_damage

        self.dx = 0
        self.y_remainder = 0
        if player_spawn_x is None:
            self.player_spawn_x = world_details.world_spawn_x
        else:
            self.player_spawn_x = player_spawn_x
        if player_spawn_y is None:
            self.player_spawn_y = world_details.world_spawn_y
        else:
            self.player_spawn_y = player_spawn_y

        self.base_net_energy_change = -0.00417

        self.initialize_drawing_vars()
        self.initialize_unique_entity_attrs()

        self.entity_chunk = self.compute_chunk_id()

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
    
    def get_player_center_x(self):
        return self.x + (self.x_size//2)

    def is_touching(self, block_positions, Block_Type):
        if issubclass(type(self.grid.get(block_positions[0][0], block_positions[1][1])), Block_Type):
            return True
        if issubclass(type(self.grid.get(block_positions[0][1], block_positions[1][1])), Block_Type):
            return True
        return False
    
    def get_player_physics(self, default_y_acceleration):
        "returns y_accel, x_velocity, y_velocity, jump_is_possible"

        if self.is_touching(self.get_block_positions(), Water):
            new_velocity = Water.velocity_reduction(self.player_speed)
            return Water.accel_reduction(default_y_acceleration), new_velocity, new_velocity, False
        
        elif self.is_touching(self.get_block_positions(), Wood_Ladder):
            return 0, self.player_speed, self.player_speed, False  # no gravity, can move freely

        elif self.is_touching(self.get_block_positions(), Iron_Ladder):
            return 0, self.player_speed, self.player_speed, False  # no gravity, can move freely

        return default_y_acceleration, self.player_speed, 0, True

    def is_move_ok_y_helper(self, check_y):
        if self.is_move_ok(floor(self.x / self.BLOCK_WIDTH), floor(check_y / self.BLOCK_WIDTH)):
            if self.is_move_ok(floor((self.x + self.x_size - 1) / self.BLOCK_WIDTH), floor(check_y / self.BLOCK_WIDTH)):
                return True
        return False

    def is_move_ok_y(self, y_change):
        step = 1 if y_change > 0 else -1
        for _ in range(abs(int(y_change))):
            check_y = self.y + self.y_size if step > 0 else self.y + step
            if self.is_move_ok_y_helper(check_y):
                self.y += step
            else:
                self.y_vel = 0
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
            "energy": self.health_bar.get_energy(),
            "is_left_facing": self.is_left_facing,
            "player_spawn_x": self.player_spawn_x,
            "player_spawn_y": self.player_spawn_y,
            "can_take_fall_damage": self.can_take_fall_damage
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
    
    def get_block_below(self, x_offset):
        """returns the block that is one px below the center of the entity's feet"""
        x, y = floor((self.x + x_offset) / self.BLOCK_WIDTH), floor((self.y + self.y_size + 1) / self.BLOCK_WIDTH)
        return self.grid.get(x, y)
    
    def get_block_below_center(self):
        return self.get_block_below(self.x_size // 2)
    
    def get_block_below_right(self):
        return self.get_block_below(self.x_size)
    
    def get_block_below_left(self):
        return self.get_block_below(0)

    def get_player_block_coordinates(self):
        return (floor((self.x + (self.x_size // 2)) / self.BLOCK_WIDTH), floor((self.y) / self.BLOCK_WIDTH))

    def is_block_above(self, grid):
        grid_pos_x = floor(self.get_player_center_x() / self.BLOCK_WIDTH)
        grid_pos_y = floor(self.y  / self.BLOCK_WIDTH)
        for y in range(grid_pos_y-1, -1, -1):
            if grid.get(grid_pos_x, y) is not None:
                return True
        return False
    
    def apply_movement_cost_x(self):
        self.health_bar.change_energy(self.base_net_energy_change)

    def apply_movement_cost_y(self):
        self.health_bar.change_energy(self.base_net_energy_change)

    def apply_movement_cost_jump(self):
        jump_energy_loss_multiplier = 3
        self.health_bar.change_energy(self.base_net_energy_change * jump_energy_loss_multiplier)

    def manage_energy(self, grid): # manages energy loss + solar gains in energy
        energy_per_tick_in_sun = 0.00622
        if not self.is_block_above(grid):
            self.health_bar.change_energy(energy_per_tick_in_sun)

    def is_alive(self):
        return self.health_bar.is_alive()

    def respawn(self):
        self.can_take_fall_damage = False
        self.x = self.player_spawn_x
        self.y = self.player_spawn_y
        self.health_bar.reset_health()
        self.health_bar.reset_energy()

    def prep_initial_spawn(self):
        self.can_take_fall_damage = False

    def draw(self, screen_x=0, screen_y=0):

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


        self.health_bar.draw()

    def get_health_bar_height(self):
        return self.health_bar.get_health_bar_height()
    
    def initialize_drawing_vars(self):
        pass
    
    def initialize_unique_entity_attrs(self):
        pass

    def compute_chunk_id(self):
        global_x, _ = self.get_player_block_coordinates()
        return global_x // Grid.chunk_width

    @classmethod
    def spawn_new(cls, grid, screen, BLOCK_WIDTH, x_px, y_px):
        # step 1: initialize the entity
        new_entity = cls(grid, screen, player_x_pixel=x_px, player_y_pixel=y_px, BLOCK_WIDTH=BLOCK_WIDTH, player_spawn_x=x_px, player_spawn_y=y_px)

        # step 2: insert the entity into the appropriate chunk
        grid.insert_entity(new_entity)

        # step 3: return in case the play class wants it for this frame
        return new_entity

    # ----------------------------- get movement inputs ----------------------------- #
        
    def initialize_temp_movement_vars(self, physics):
        dx = 0
        dy = 0
        cur_y_acceleration = physics.Y_ACCELERATION
        cur_player_speed_x = self.player_speed
        cur_y_acceleration, cur_player_speed_x, cur_player_speed_y, jump_is_possible = self.get_player_physics(physics.Y_ACCELERATION)
        if cur_player_speed_y > 0: water_movement = True
        else: water_movement = False

        return dx, dy, cur_y_acceleration, cur_player_speed_x, cur_player_speed_y, jump_is_possible, water_movement
    
    def pathfind(self, input, physics, dx, dy, cur_y_acceleration, cur_player_speed_x, cur_player_speed_y, jump_is_possible, water_movement):

        # pathfind
                
        return dx, dy, cur_y_acceleration, cur_player_speed_y, water_movement


    # ----------------------------- runs player physics ----------------------------- #

    def move(self, input, physics): # returns assessed damage object
        # ---------------------- step 1: process input ---------------------- #
        dx, dy, cur_y_acceleration, cur_player_speed_x, cur_player_speed_y, jump_is_possible, water_movement = self.initialize_temp_movement_vars(physics)
        
        # ---------------------- step 2: pathfind ---------------------- #
        dx, dy, cur_y_acceleration, cur_player_speed_y, water_movement = self.pathfind(input, physics, dx, dy, cur_y_acceleration, cur_player_speed_x, cur_player_speed_y, jump_is_possible, water_movement)

        # ---------------------- step 2: move ---------------------- #
        # apply gravity and jumping
        dy += self.y_vel

        # check if motion is legal
        if water_movement:
            self.y_vel *= 0.5
            dy *= 0.4
            dy = max(-cur_player_speed_y, min(cur_player_speed_y, dy))
        
        self.y_remainder += dy
        int_dy = int(self.y_remainder)
        self.y_remainder -= int_dy

        prevel = abs(self.y_vel)
        collided = self.is_move_ok_y(int_dy)
        damage_threshold_velocity = 20

        if collided:
            if prevel > damage_threshold_velocity:
                damage = (prevel - damage_threshold_velocity)
                damage *= physics.FALL_DAMAGE_BASE_MULTIPLIER
                # print(f'damage = {damage}, prevel = {prevel}')
                if self.can_take_fall_damage: # stops fall damage from spawning
                    self.health_bar.change_health(-damage)
                else:
                    self.can_take_fall_damage = True


        x_move = abs(dx)
        if dx < 0: x_direction = -1
        else: x_direction = 1
        while x_move >= 0:
            if self.is_move_ok_x(x_move * x_direction):
                self.x += (x_move * x_direction)
                break
            x_move -= 1

        # increment gravity
        self.y_vel += cur_y_acceleration

        self.dx = dx
