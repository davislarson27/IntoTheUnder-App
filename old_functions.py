# # from zombiearcheology.py

# def remove_block(grid, pixel_x_coordinate, pixel_y_coordinate):
#     grid_x = pixel_to_grid(pixel_x_coordinate, grid.BLOCK_WIDTH)
#     grid_y = pixel_to_grid(pixel_y_coordinate, grid.BLOCK_WIDTH)
#
#     if grid.in_bounds(grid_x, grid_y):
#         if grid.get(grid_x, grid_y) == None:
#             # return None
#             return
#         else:
#             grid.set(grid_x, grid_y, None)
#
#         #     grid.set(grid_x, grid_y, Rock(grid, screen, grid_x, grid_y, BLOCK_WIDTH))
        
# # from zombiearcheology.py

# def insert_block(grid, screen, pixel_x_coordinate, pixel_y_coordinate):
#     grid_x = pixel_to_grid(pixel_x_coordinate, grid.BLOCK_WIDTH)
#     grid_y = pixel_to_grid(pixel_y_coordinate, grid.BLOCK_WIDTH)
#
#     if grid.in_bounds(grid_x, grid_y):
#         if grid.get(grid_x, grid_y) == None:
#             grid.set(grid_x, grid_y, Rock(grid, screen, grid_x, grid_y, BLOCK_WIDTH))


# class Packed_Sand(Block):

#     # remember to update the blocks_list for loading when you add a new type of block :)

#     str_name = "Sand"

#     @staticmethod
#     def draw_manual(screen, x, y, block_width, being_mined = False, is_grid_coordinates = True):
#         if being_mined:
#             added_color = 20
#         else:
#             added_color = 0

#         if is_grid_coordinates:
#             x *= block_width
#             y *= block_width
        
#         pygame.draw.rect( # draw base color
#             screen,
#             (215 + added_color, 200 + added_color, 155 + added_color),           # color
#             (x, y, block_width, block_width)
#         )
        
#         squares_in_block = 5
#         length_of_subsquare = block_width // squares_in_block
#         for side_y in range(squares_in_block):
#             start_px_y = y + (side_y * length_of_subsquare)
#             if side_y % 2 == 0:
#                 for side_x in range(squares_in_block):
#                     start_px_x = x + (side_x * length_of_subsquare)
#                     if side_x % 2 == 0:
#                         pygame.draw.rect(
#                             screen,
#                             (170 + added_color, 168 + added_color, 158 + added_color),           # color
#                             (start_px_x , start_px_y, length_of_subsquare, length_of_subsquare)
#                         )
