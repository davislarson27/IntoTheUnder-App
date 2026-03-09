import pygame
from components.blocks.block_types._base import Block

class Water(Block):

    # remember to update the blocks_list for loading when you add a new type of block :)
    
    str_name = "Water"
    tick_threshold = 20
    water_value = 0
    max_water_value = 4

    def convert_water_value(self, water_value):
        return self.max_water_value + water_value

    def physics(self):
        if self.grid.in_bounds(self.x, self.y + 1) and (issubclass(type(self.grid.get(self.x, self.y + 1)), Water) or self.grid.get(self.x, self.y + 1) is None): # checks for block directly under the water
            if self.ticks_till_physics < self.tick_threshold:
                self.ticks_till_physics += 1
            else: #tick count has reached go time :)
                self.grid.set(self.x, self.y+1, Water, True)
                self.ticks_till_physics = 0
        elif issubclass(type(self.grid.get(self.x, self.y - 1)), Water) and self.water_value != 0:
            if self.ticks_till_physics < self.tick_threshold:
                self.grid.set(self.x, self.y, Water, True)
                self.ticks_till_physics = 0
            else:
                self.ticks_till_physics += 1
        elif self.grid.in_bounds(self.x + 1, self.y) and ((issubclass(type(self.grid.get(self.x, self.y + 1)), Water)) or self.grid.get(self.x + 1, self.y) is None): # check to the right
            if self.ticks_till_physics < self.tick_threshold:
                self.ticks_till_physics += 1
            else: #tick count has reached go time :)
                self.grid.set(self.x + 1, self.y, self.get_right_fill(), True)
                self.ticks_till_physics = 0
        elif self.grid.in_bounds(self.x - 1, self.y) and ((issubclass(type(self.grid.get(self.x, self.y + 1)), Water)) or self.grid.get(self.x - 1, self.y) is None): # check the left
            if self.ticks_till_physics < self.tick_threshold:
                self.ticks_till_physics += 1
            else: #tick count has reached go time :)
                self.grid.set(self.x - 1, self.y, self.get_left_fill(), True)
                self.ticks_till_physics = 0


        if self.water_value > 0: # right block
            left_block = self.grid.get(self.x - 1, self.y)
            if left_block is not None and issubclass(type(left_block), Water):
                if left_block.water_value != self.water_value - 1:
                    if left_block.water_value < self.max_water_value:
                        self.grid.set(self.x, self.y, water_value_reference[self.convert_water_value(left_block.water_value + 1)], True)
            else:
                if self.grid.in_bounds(self.x - 1, self.y):
                    self.grid.set(self.x, self.y, None)
        elif self.water_value < 0: # right block
            right_block = self.grid.get(self.x + 1, self.y)
            if right_block is not None and issubclass(type(right_block), Water):
                if right_block.water_value != self.water_value + 1:
                    if abs(right_block.water_value) < self.max_water_value:
                        self.grid.set(self.x, self.y, water_value_reference[self.convert_water_value(right_block.water_value - 1)], True)
            else:
                if self.grid.in_bounds(self.x + 1, self.y):
                    self.grid.set(self.x, self.y, None)


        if self.water_value != 0:
            left_block = self.grid.get(self.x - 1, self.y)
            right_block = self.grid.get(self.x + 1, self.y)
            if issubclass(type(right_block), Water) and issubclass(type(left_block), Water):
                if abs(right_block.water_value) < 2 and abs(left_block.water_value) < 2:
                    self.grid.set(self.x, self.y, Water, True)


    @staticmethod
    def get_left_fill():
        return Water_L1
                    
    @staticmethod
    def get_right_fill():
        return Water_R1


    def can_move_to_inventory(self):
        return False
    
    @staticmethod
    def accel_reduction(accel):
        return accel // 3
    
    @staticmethod
    def velocity_reduction(velocity):
        return velocity // 2


    @staticmethod
    def draw_manual(screen, x, y, block_width, being_mined=False, is_grid_coordinates=True, use_alt_drawing=False):
        if being_mined:
            added_color = 20
        else:
            added_color = 0

        if is_grid_coordinates:
            x *= block_width
            y *= block_width

        # (40, 110, 170) (80, 160, 200) (25, 80, 130)

        pygame.draw.rect( # draw base color
            screen,
            (40 + added_color, 110 + added_color, 170 + added_color),           # color
            (x, y, block_width, block_width)
        )

class Water_R1(Water):

    # remember to update the blocks_list for loading when you add a new type of block :)
    
    str_name = "Water R1"
    water_value = 1

    @staticmethod
    def get_left_fill():
        return Water
                    
    @staticmethod
    def get_right_fill():
        return Water_R2

                    

    @staticmethod
    def draw_manual(screen, x, y, block_width, being_mined=False, is_grid_coordinates=True, use_alt_drawing=False):
        if being_mined:
            added_color = 20
        else:
            added_color = 0

        if is_grid_coordinates:
            x *= block_width
            y *= block_width

        # (40, 110, 170) (80, 160, 200) (25, 80, 130)
        drop_off_px = block_width // 4
        points = [
            (x, y),             # top-left high
            (x + block_width, y + drop_off_px),  # top-right lower
            (x + block_width, y + block_width),
            (x, y + block_width)
        ]

        pygame.draw.polygon( # draw base color
            screen,
            (40 + added_color, 110 + added_color, 170 + added_color),           # color
            points
        )

class Water_L1(Water):

    # remember to update the blocks_list for loading when you add a new type of block :)
    
    str_name = "Water L1"
    water_value = -1
                    
    @staticmethod
    def get_left_fill():
        return Water_L2
                    
    @staticmethod
    def get_right_fill():
        return Water


    @staticmethod
    def draw_manual(screen, x, y, block_width, being_mined=False, is_grid_coordinates=True, use_alt_drawing=False):
        if being_mined:
            added_color = 20
        else:
            added_color = 0

        if is_grid_coordinates:
            x *= block_width
            y *= block_width

        drop_off_px = block_width // 4
        points = [
            (x, y + drop_off_px),                         # top-left of box
            (x + block_width, y),          # roof peak
            (x + block_width, y + block_width),              # bottom right
            (x, y + block_width)                             # bottom-left

        ]

        pygame.draw.polygon( # draw base color
            screen,
            (40 + added_color, 110 + added_color, 170 + added_color),           # color
            points
        )

class Water_R2(Water):

    # remember to update the blocks_list for loading when you add a new type of block :)
    
    str_name = "Water R2"
    water_value = 2

    @staticmethod
    def get_left_fill():
        return Water_R1
                    
    @staticmethod
    def get_right_fill():
        return Water_R3
      

    @staticmethod
    def draw_manual(screen, x, y, block_width, being_mined=False, is_grid_coordinates=True, use_alt_drawing=False):
        if being_mined:
            added_color = 20
        else:
            added_color = 0

        if is_grid_coordinates:
            x *= block_width
            y *= block_width

        # (40, 110, 170) (80, 160, 200) (25, 80, 130)
        drop_off_px = block_width // 4
        points = [
            (x, y + drop_off_px),
            (x + block_width, y + 2*drop_off_px),
            (x + block_width, y + block_width),
            (x, y + block_width)
        ]

        pygame.draw.polygon( # draw base color
            screen,
            (40 + added_color, 110 + added_color, 170 + added_color),           # color
            points
        )

class Water_L2(Water):

    # remember to update the blocks_list for loading when you add a new type of block :)
    
    str_name = "Water L2"
    water_value = -2

    @staticmethod
    def get_left_fill():
        return Water_L3
                    
    @staticmethod
    def get_right_fill():
        return Water_L1
                

    @staticmethod
    def draw_manual(screen, x, y, block_width, being_mined=False, is_grid_coordinates=True, use_alt_drawing=False):
        if being_mined:
            added_color = 20
        else:
            added_color = 0

        if is_grid_coordinates:
            x *= block_width
            y *= block_width

        # (40, 110, 170) (80, 160, 200) (25, 80, 130)
        drop_off_px = block_width // 4
        points = [
            (x, y + drop_off_px * 2),                         # top-left of box
            (x + block_width, y + drop_off_px),          # roof peak
            (x + block_width, y + block_width),              # bottom right
            (x, y + block_width)                             # bottom-left
        ]

        pygame.draw.polygon( # draw base color
            screen,
            (40 + added_color, 110 + added_color, 170 + added_color),           # color
            points
        )

class Water_R3(Water):

    # remember to update the blocks_list for loading when you add a new type of block :)
    
    str_name = "Water R3"
    water_value = 3

    @staticmethod
    def get_left_fill():
        return Water_R2
                    
    @staticmethod
    def get_right_fill():
        return Water_R4
      

    @staticmethod
    def draw_manual(screen, x, y, block_width, being_mined=False, is_grid_coordinates=True, use_alt_drawing=False):
        if being_mined:
            added_color = 20
        else:
            added_color = 0

        if is_grid_coordinates:
            x *= block_width
            y *= block_width

        # (40, 110, 170) (80, 160, 200) (25, 80, 130)
        drop_off_px = block_width // 4
        points = [
            (x, y + 2 * drop_off_px),
            (x + block_width, y + 3 * drop_off_px),
            (x + block_width, y + block_width),
            (x, y + block_width)
        ]

        pygame.draw.polygon( # draw base color
            screen,
            (40 + added_color, 110 + added_color, 170 + added_color),           # color
            points
        )

class Water_L3(Water):

    # remember to update the blocks_list for loading when you add a new type of block :)
    
    str_name = "Water L3"
    water_value = -3

    @staticmethod
    def get_left_fill():
        return Water_L4
                    
    @staticmethod
    def get_right_fill():
        return Water_L2
                

    @staticmethod
    def draw_manual(screen, x, y, block_width, being_mined=False, is_grid_coordinates=True, use_alt_drawing=False):
        if being_mined:
            added_color = 20
        else:
            added_color = 0

        if is_grid_coordinates:
            x *= block_width
            y *= block_width

        # (40, 110, 170) (80, 160, 200) (25, 80, 130)
        drop_off_px = block_width // 4
        points = [
            (x, y + drop_off_px * 3),                         # top-left of box
            (x + block_width, y + drop_off_px * 2),          # roof peak
            (x + block_width, y + block_width),              # bottom right
            (x, y + block_width)                             # bottom-left
        ]

        pygame.draw.polygon( # draw base color
            screen,
            (40 + added_color, 110 + added_color, 170 + added_color),           # color
            points
        )

class Water_R4(Water):

    # remember to update the blocks_list for loading when you add a new type of block :)
    
    str_name = "Water R4"
    water_value = 4

    @staticmethod
    def get_left_fill():
        return Water_R3
                    
    @staticmethod
    def get_right_fill():
        return None
      

    @staticmethod
    def draw_manual(screen, x, y, block_width, being_mined=False, is_grid_coordinates=True, use_alt_drawing=False):
        if being_mined:
            added_color = 20
        else:
            added_color = 0

        if is_grid_coordinates:
            x *= block_width
            y *= block_width

        # (40, 110, 170) (80, 160, 200) (25, 80, 130)
        drop_off_px = block_width // 4
        points = [
            (x, y + 3 * drop_off_px),
            (x + block_width, y + 4 * drop_off_px),
            (x + block_width, y + block_width),
            (x, y + block_width)
        ]

        pygame.draw.polygon( # draw base color
            screen,
            (40 + added_color, 110 + added_color, 170 + added_color),           # color
            points
        )

class Water_L4(Water):

    # remember to update the blocks_list for loading when you add a new type of block :)
    
    str_name = "Water L4"
    water_value = -4

    @staticmethod
    def get_left_fill():
        # return Water
        return None
                    
    @staticmethod
    def get_right_fill():
        return Water_L3
                

    @staticmethod
    def draw_manual(screen, x, y, block_width, being_mined=False, is_grid_coordinates=True, use_alt_drawing=False):
        if being_mined:
            added_color = 20
        else:
            added_color = 0

        if is_grid_coordinates:
            x *= block_width
            y *= block_width

        # (40, 110, 170) (80, 160, 200) (25, 80, 130)
        drop_off_px = block_width // 4
        points = [
            (x, y + drop_off_px * 4),                         # top-left of box
            (x + block_width, y + drop_off_px * 3),          # roof peak
            (x + block_width, y + block_width),              # bottom right
            (x, y + block_width)                             # bottom-left
        ]

        pygame.draw.polygon( # draw base color
            screen,
            (40 + added_color, 110 + added_color, 170 + added_color),           # color
            points
        )


water_value_reference = [Water_L4, Water_L3, Water_L2, Water_L1, Water, Water_R1, Water_R2, Water_R3, Water_R4]
