import pygame
from math import cos, sin, pi
from world.blocks.block_types._base import Block

class Respawn_Beacon(Block):
    
    # remember to update the blocks_list for loading when you add a new type of block :)

    str_name = "Respawn Beacon"
    ticks_to_mine = 85
    tick_threshold = 20
    
    def interaction(self, player):
        self.ticks_till_physics = 1 # just for the animation
        self.set_spawn_point(player)
        return True

    def physics(self): # runs animation counter for this case
        if self.ticks_till_physics > 0: # blocks physics (or animation in this case) if there is no recipe
            self.ticks_till_physics += 1

        if self.ticks_till_physics == self.tick_threshold: # this will add the recipe when it is done
            self.ticks_till_physics = 0

    def set_spawn_point(self, player):
        player.player_spawn_x = self.grid.get_block_to_px(self.x)
    
    def drawDependentDetails(self, screen, x, y, block_width, being_mined=False, is_grid_coordinates=True, use_alt_drawing=False):
        if is_grid_coordinates:
            x *= block_width
            y *= block_width

        block_width_percentage = 0.6
        sub_block_width = block_width * block_width_percentage
        position_offset = int(block_width * ((1 - block_width_percentage) / 2))
        sub_x = x + position_offset
        sub_y = y + position_offset

        # draws crafting recipe output on block
        self.animation(screen, sub_x, sub_y, sub_block_width, is_grid_coordinates=False)            

    def animation(self, screen, x, y, block_width, being_mined=False, is_grid_coordinates=True, use_alt_drawing=False):
        """responsible for drawing animations"""
        if self.ticks_till_physics == 0: # no animation if physics are not running
            return
        
        def draw_ray(screen, cx, cy, angle, length, color, start_distance=0, thickness=1): # helper function for drawing the reys outward
            """draws rays, angle is measured in radians"""

            # start point (offset from center)
            start_x = cx + cos(angle) * start_distance
            start_y = cy + sin(angle) * start_distance

            # end point (continues outward)
            end_x = start_x + cos(angle) * length
            end_y = start_y + sin(angle) * length

            pygame.draw.line(
                screen,
                color,
                (start_x, start_y),
                (end_x, end_y),
                thickness
            )

        # set ray color
        rayColor = (245, 225, 140)

        # calculate ray length
        maxRayLength = int(block_width * 0.6)

        maxPositionPercent = 0.65
        ticksToEndGrowth = int(self.tick_threshold * maxPositionPercent)
        percentGrown = min((self.ticks_till_physics - 1) / ticksToEndGrowth, 1)
        rayLength = int(maxRayLength * percentGrown)

        # calculate ray position
        rayCount = 5
        anglePerRay = 2 * pi / rayCount
        offsetFromStart = 0
        startDistanceFromCenter = block_width + int(block_width * 0.2)

        center_x = x + block_width // 2
        center_y = y + block_width // 2

        # draw rays
        for i in range(rayCount):
            curAngle = (anglePerRay * i) + offsetFromStart
            draw_ray(screen, center_x, center_y, curAngle, rayLength, rayColor, startDistanceFromCenter)
        
        # draw short rays
        shortRayOffSet = anglePerRay / 2
        shortRayMaxPercent = 0.75
        shortRayLength = min(shortRayMaxPercent * maxRayLength, rayLength)
        for i in range(rayCount):
            curAngle = (anglePerRay * i) + shortRayOffSet
            draw_ray(screen, center_x, center_y, curAngle, shortRayLength, rayColor, startDistanceFromCenter)

    @staticmethod
    def draw_manual(screen, x, y, block_width, being_mined=False, is_grid_coordinates=True, use_alt_drawing=False): 
        if being_mined:
            added_color = 20
        else:
            added_color = 0

        if is_grid_coordinates:
            x *= block_width
            y *= block_width

        paper_color = (
            min(255, 225 + added_color),
            min(255, 205 + added_color),
            min(255, 170 + added_color)
        )
        border_color = (
            min(255, 120 + added_color),
            min(255, 100 + added_color),
            min(255, 80 + added_color)
        )
        line_color = (
            min(255, 160 + added_color),
            min(255, 140 + added_color),
            min(255, 110 + added_color)
        )

        # base
        pygame.draw.rect(screen, paper_color, (x, y, block_width, block_width))

        # border
        border_thickness = max(1, block_width // 10)
        pygame.draw.rect(screen, border_color, (x, y, block_width, block_width), border_thickness)

        # inner frame
        margin = max(2, block_width // 6)
        inner_x = x + margin
        inner_y = y + margin
        inner_w = block_width - margin * 2
        inner_h = block_width - margin * 2

        if inner_w > 4 and inner_h > 4:
            pygame.draw.rect(screen, border_color, (inner_x, inner_y, inner_w, inner_h), 1)

            # two simple horizontal lines
            line1_y = inner_y + inner_h // 3
            line2_y = inner_y + (inner_h * 2) // 3

            pygame.draw.line(screen, line_color, (inner_x + 2, line1_y), (inner_x + inner_w - 3, line1_y), 1)
            pygame.draw.line(screen, line_color, (inner_x + 2, line2_y), (inner_x + inner_w - 3, line2_y), 1)

            # tiny center mark
            mark_size = max(2, block_width // 8)
            mark_x = x + (block_width - mark_size) // 2
            mark_y = y + (block_width - mark_size) // 2
            pygame.draw.rect(screen, border_color, (mark_x, mark_y, mark_size, mark_size), 1)
