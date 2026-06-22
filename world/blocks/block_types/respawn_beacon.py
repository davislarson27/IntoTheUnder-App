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
        rayColor = (160, 240, 185) # diamond color

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

        bg_color = (95, 100, 102)
        bg_outline_color_mid = (80, 85, 91)
        bg_outline_color = (65, 73, 80)
        gem_color = (160, 240, 185)
        gem_inner_outline_color = (90, 210, 130)
        gem_outline_color = (160, 240, 185)

        pygame.draw.rect( # draw the background
            screen,
            (bg_color[0]+added_color, bg_color[1]+added_color, bg_color[2]+added_color), 
            (
                0,
                0,
                block_width,
                block_width
            )
        )
        pygame.draw.rect( # draw the background
            screen,
            (bg_outline_color_mid[0]+added_color, bg_outline_color_mid[1]+added_color, bg_outline_color_mid[2]+added_color), 
            (
                0,
                0,
                block_width,
                block_width
            ),
            width=3
        )
        pygame.draw.rect( # outline the block
            screen,
            (bg_outline_color[0]+added_color, bg_outline_color[1]+added_color, bg_outline_color[2]+added_color), 
            (
                0,
                0,
                block_width,
                block_width
            ),
            width=1
        )

        center_detail_width = block_width // 2
        center_detail_offset = (block_width - center_detail_width) // 2
        points = [ # points in the gem
            (center_detail_width//2 + center_detail_offset, center_detail_offset), # top point
            (center_detail_width + center_detail_offset, center_detail_width//2 + center_detail_offset), # right point
            (center_detail_width//2 + center_detail_offset, center_detail_width + center_detail_offset), # bottom point
            (center_detail_offset, center_detail_width//2 + center_detail_offset) # bottom left point
        ]

        pygame.draw.polygon( # draw the diamond shape
            screen,
            (min(gem_color[0]+added_color, 255), min(gem_color[1]+added_color, 255), min(gem_color[2]+added_color, 255)), 
            points
        )
        pygame.draw.polygon( # draw the diamond shape outline
            screen,
            (min(gem_inner_outline_color[0]+added_color, 255), min(gem_inner_outline_color[1]+added_color, 255), min(gem_inner_outline_color[2]+added_color, 255)), 
            points,
            width=4
        )
        pygame.draw.polygon( # draw the diamond shape outline
            screen,
            (min(gem_outline_color[0]+added_color, 255), min(gem_outline_color[1]+added_color, 255), min(gem_outline_color[2]+added_color, 255)), 
            points,
            width=2
        )
        