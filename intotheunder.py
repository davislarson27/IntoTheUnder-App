import warnings
import traceback

warnings.filterwarnings( # you should probably delete this at some point but deprecation warnings were getting annoying
    "ignore",
    message="pkg_resources is deprecated as an API.*",
    category=UserWarning,
)

import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

import pygame
from math import floor, sqrt
import json
from pathlib import Path

from components.blocks import *
from menu.menu import Menu
from components.world_details import World_Details
from components.images import Images
from components.game_file_reading import *
from components.input import Input
from play.play import Play
from menu.world_creation.world_generation_settings import World_Generation_Settings
from components.blit_letterboxed import blit_letterboxed

# from windows_path_resources import *
from components.path_resources.mac_path_resources import *

# pyinstaller command line
r"""
mac: python3 -m PyInstaller --clean --noconfirm --windowed --name "IntoTheUnder" --icon "game_files/image_files/ITU-Icon.icns" --add-data "game_files:game_files" intotheunder.py

windows: py -m PyInstaller --clean --noconfirm --windowed --name "IntoTheUnder" --icon "game_files\image_files\ITU-Icon.ico" --add-data "game_files;game_files" intotheunder.py

"""

# converting .png to ico (windows) https://convertico.com/

# to zip without metadata for windows on mac -> zip -r -X IntoTheUnder.zip IntoTheUnder


# update notes:
# - improved inventory UI
# - added crafting new items
# - added chests to store items
# - added functioning doors
# - let left shift key ignore item interactions
# - added items
# - added new blocks
# - fixed incorrect exit screen
# - added TNT and explosives
# - refactored code to be more state based
# - reorganized code into files


# functions
def get_user_worlds_list(game_files_directory, IMAGES_FILE_NAME):
    def convert_file_to_class(wd_file_path): #converts file to class
        try:
            with open(wd_file_path, "r") as world_details_file:
                return World_Details.fill_from_dict(json.load(world_details_file))
        except: # prevents crash on launch with a bad details file by adding dummy file
            cur_timestamp = World_Details.get_corrupted_timestamp()
            file_name = Path(wd_file_path).parent.name
            return World_Details(f"{file_name} (CORRUPTED)", VERSION, cur_timestamp, cur_timestamp, True)

    # gets the file names for all user worlds and sorts them in order of last opened
    game_files_folder = Path(game_files_directory)

    world_details_class_list = [convert_file_to_class(f"{file}/world_details.json") for file in game_files_folder.rglob("*") if file.is_dir() and file.name != IMAGES_FILE_NAME]
    world_details_class_list.sort(key=lambda world:world.last_modified_date, reverse=True)

    return [world.world_name for world in world_details_class_list if not world.version > VERSION]


# implementation details
BLOCK_WIDTH = 25

screen_height_px = 620
screen_width_px = floor(screen_height_px / 0.625) + 100

HEALTH_BAR_HEIGHT = 20 # included in INVENTORY_HEIGHT
grid_height_px = screen_height_px // 48
INVENTORY_HEIGHT = HEALTH_BAR_HEIGHT + (grid_height_px * 7) # this is so hard coded. please change this at some point.


# cur_seed = 12
# random.seed(cur_seed)

APP_NAME = "Into The Under"
APP_DISPLAY_NAME = "Into The Under 1.5.0"
VERSION_NAME = "intotheunder1.5.0"
VERSION = 1.5 # primary version - ex 1.3.1 becomes 1.3
GAME_FILE_FOLDER_NAME = "game_files"
IMAGES_FILE_NAME = "image_files"
pygame_icon_file = "ITU-Icon.png"

game_files_location = VERSION_NAME + '/' + GAME_FILE_FOLDER_NAME

save_path = user_data_dir(APP_NAME)
directory = os.path.join(save_path, game_files_location)
os.makedirs(directory, exist_ok=True)

# initalize pygame
pygame.init()
pygame.font.init()

icon_surface = pygame.image.load(resource_path(f"game_files/{IMAGES_FILE_NAME}/{pygame_icon_file}"))
pygame.display.set_icon(icon_surface)

# create the screen
background_color = (30,30,30)
window = pygame.display.set_mode((screen_width_px, screen_height_px), pygame.RESIZABLE)
screen = pygame.Surface((screen_width_px, screen_height_px))
pygame.display.set_caption(APP_DISPLAY_NAME)

# load in images
images = Images(resource_path(f"game_files/{IMAGES_FILE_NAME}"), BLOCK_WIDTH)

true_height = screen_height_px - INVENTORY_HEIGHT
MOVEMENT_ALTITUDE_PX = (true_height * 13) // 16

# set grid size
grid_width = 5000
grid_height = 100


# clock features
clock = pygame.time.Clock()
TICKS = 60

# run details
running = True
world_generation_settings = World_Generation_Settings(VERSION, INVENTORY_HEIGHT, HEALTH_BAR_HEIGHT, grid_width, grid_height)
menu = Menu(screen, window, images, screen_width_px, screen_height_px, BLOCK_WIDTH, get_user_worlds_list(directory, IMAGES_FILE_NAME), directory, world_generation_settings)

# running class
run_class = menu
input_object = Input()

# ----------------------------------------------- run loop ------------------------------------------------ #
try:
    while True:
        # get scale stuff
        scale, offx, offy = blit_letterboxed(screen, window, background_color)

        # get inputs
        input_object.take_input(scale, offx, offy)

        # quit if requested
        if input_object.check_quit(): break

        # execute run function
        run_class = run_class.run(input_object)

        # update screen
        pygame.display.flip()

        # update clock
        clock.tick(TICKS)

except Exception as e:
    print("CRASH DETECTED")
    traceback.print_exc()

    run_class.catch_exception()

pygame.quit()