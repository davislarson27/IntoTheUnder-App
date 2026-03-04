# this version's goal is to refactor 1.2 version in a way that allows for simpler mechanics and a cleaner game loop

import pygame
from math import floor
import json

from grid import Grid
from player import Player
from blocks import *
from full_inventory import Inventory
from menu import Menu
from world_generation import *

# functions
def pixel_to_grid(pixel_coordinates, BLOCK_WIDTH):
    grid_coordinates = floor(pixel_coordinates / BLOCK_WIDTH)
    return grid_coordinates

def get_affected_block(player, grid, pointer_x, pointer_y, build_mode = True): #pointers (expected as 1, 0, or -1) give direction of arrow
    # get center of origin
    x = pixel_to_grid(player.x + (0.5 * player.x_size), BLOCK_WIDTH)
    y = pixel_to_grid(player.y + (0.5 * player.y_size), BLOCK_WIDTH)

    # set out of bounds savers
    out_of_bounds_x, out_of_bounds_y = None, None

    # run through the first 3 blocks away to see when you hit a block
    for i in range(1, 4):
        x += pointer_x
        y += pointer_y
        if grid.in_bounds(x,y):
            if grid.get(x,y) != None:
                return x, y
        else:
            out_of_bounds_x, out_of_bounds_y = x, y
        
    if not build_mode:
        return None, None
    return out_of_bounds_x, out_of_bounds_y

def save_game(directory, player, inventory, grid):
    grid_dictionary = grid.to_dict()
    with open(f"{directory}/grid.json", "w") as grid_file:
        json.dump(grid_dictionary, grid_file, indent=3)

    player_dictionary = player.to_dict()
    with open(f"{directory}/player_attributes.json", "w") as player_attr_file:
        json.dump(player_dictionary, player_attr_file, indent=3)
    
    inventory_dict = inventory.to_dict()
    with open(f"{directory}/inventory.json", "w") as inventory_file:
        json.dump(inventory_dict,inventory_file, indent=3)

def load_world(directory, screen, width, height, INVENTORY_HEIGHT, BLOCK_WIDTH):
    with open(f"{directory}/grid.json", "r") as grid_file:
        grid_dict = json.load(grid_file)
        grid = Grid.fill_from_dict(grid_dict, screen, BLOCK_WIDTH)

    with open(f"{directory}/inventory.json", "r") as inventory_file:
        inventory_dict = json.load(inventory_file)
        inventory = Inventory.fill_from_dict(inventory_dict, screen, height, width, INVENTORY_HEIGHT, HEALTH_BAR_HEIGHT)

    with open(f"{directory}/player_attributes.json", "r") as player_attr_file:
        player_attr_dict = json.load(player_attr_file)
        player_attr_dict["screen"] = screen
        player_attr_dict["grid"] = grid
        player_attr_dict["inventory_bar_height"] = INVENTORY_HEIGHT
        player_attr_dict["health_bar_height"] = HEALTH_BAR_HEIGHT
        player = Player(**player_attr_dict)

    return grid, inventory, player

def generate_world(screen, grid_width, grid_depth):
    # initialize grid
    grid = Grid(grid_width, grid_depth, BLOCK_WIDTH, screen) #sets width at 200 blocks

    # generate world terrain
    generate_world_blocks(grid, grid_width, grid_depth)

    # initialize inventory
    inventory = Inventory(screen, screen_height_px, screen_width_px, INVENTORY_HEIGHT, HEALTH_BAR_HEIGHT)

    # initialize player in grid
    player = Player(grid, screen, ((grid_width * BLOCK_WIDTH) // 2), 0, BLOCK_WIDTH, x_size=23, y_size = 23, inventory_bar_height=INVENTORY_HEIGHT, health_bar_height = HEALTH_BAR_HEIGHT)

    return grid, inventory, player


# implementation details
BLOCK_WIDTH = 25
INVENTORY_HEIGHT = 120
HEALTH_BAR_HEIGHT = 20 # included in INVENTORY_HEIGHT

# initalize pygame
pygame.init()
pygame.font.init()

# create the screen
screen_width_px, screen_height_px = 1000, 620
screen = pygame.display.set_mode((screen_width_px, screen_height_px))
pygame.display.set_caption("Zombie Archeology")

true_height = screen_height_px - INVENTORY_HEIGHT
MOVEMENT_ALTITUDE_PX = (true_height * 13) // 16

# set grid size
grid_width = 5000
# grid_depth = (screen_height_px - INVENTORY_HEIGHT)//BLOCK_WIDTH + 10
grid_height = 100

# clock features
clock = pygame.time.Clock()
TICKS = 60

directory = "zombie_archeology2.0/game_files/my_first_world"

# set gravity variables
Y_ACCELERATION = 1
WATER_UPWARD_ACCEL = -0.05
JUMP_VELOCITY = -15


# arrow key press variables
held_time = 0 # holds count of frames held
DESTROY_HOLD_THRESHOLD = 15 # count of frames held before destroyed motion happens
BUILD_HOLD_THRESHOLD = 3 # count of frames held before destroyed motion happens
block_selected = (None, None) # block coordinates of which block will be affected
game_is_loaded = False

# counters of frames with key pressed
return_key_state = 0

# run details
running = True
menu = Menu(screen, screen_width_px, screen_height_px, BLOCK_WIDTH)



# now time to execute the main game loop
while running:
    pass