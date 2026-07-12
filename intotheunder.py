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
from math import floor

from world.blocks.block_export import *
from menu.menu import Menu
from components.images import Images
import components.fonts as Font_Manager
import components.settings as Settings_Manager
from components.game_file_reading import *
from components.input import Input
from world.world_creation.world_generation_settings import World_Generation_Settings
from components.blit_letterboxed import blit_letterboxed
from components.crash_menu import Crash_Menu
from components.game_file_reading import get_user_worlds_list
from components.launch_load_screen import Launch_Load_Screen

# from components.path_resources.windows_path_resources import *
from components.path_resources.mac_path_resources import *

# pyinstaller command line
r"""
mac: python3 -m PyInstaller --clean --noconfirm --windowed --name "IntoTheUnder" --icon "game_files/image_files/ITU-Icon.icns" --add-data "game_files:game_files" intotheunder.py

windows: py -m PyInstaller --clean --noconfirm --windowed --name "IntoTheUnder" --icon "game_files\image_files\ITU-Icon.ico" --add-data "game_files;game_files" intotheunder.py

"""

# tagging code: git tag v1.3.1
# uploading tag: git push origin v1.3.1

# converting .png to ico (windows) https://convertico.com/

# to zip without metadata for windows on mac -> zip -r -X IntoTheUnder.zip IntoTheUnder

# to find game files, use: cd ~/Library/Application\ Support/Into\ The\ Under/intotheunder1.5.1/game_files


"""
update notes:
 - added a health and energy bar
 - added fall damage
 - added dying and respawning
 - added a gold tinted glass
 - added flowers
 - added puddles
 - reorganized the crafting recipes menu
 - added enduring chests
 - redesigned the menu and added new world gen settings
 - added the ability to rename a world
 - added spruce wood blocks
 - added mahogany wood blocks
 - added stars to the far background
 - added respawn beacons to reset a user's spawn point
 - added naturally spawning (but rate) packed dirt
 - added underground recipe caves
"""

"""
notes:
 - this update will probably need to be split into 2 or 3 parts
"""

# implementation details
BLOCK_WIDTH = 25

screen_height_px = 620
screen_width_px = floor(screen_height_px / 0.625) + 100

HEALTH_BAR_HEIGHT = 20 # included in INVENTORY_HEIGHT
grid_height_px = screen_height_px // 48
INVENTORY_HEIGHT = HEALTH_BAR_HEIGHT + (grid_height_px * 7) # this is so hard coded. please change this at some point.


APP_NAME = "Into The Under"
APP_DISPLAY_NAME = "Into The Under v1.7.0"
VERSION_NAME = "intotheunder1.7.0"
VERSION = 1.7 # primary version - ex 1.3.1 becomes 1.3
GAME_FILE_FOLDER_NAME = "game_files"
IMAGES_FILE_NAME = "image_files"
FONTS_FILE_NAME = 'fonts'
pygame_icon_file = "ITU-Icon.png"

game_files_location = VERSION_NAME + '/' + GAME_FILE_FOLDER_NAME

save_path = user_data_dir(APP_NAME)
directory = os.path.join(save_path, game_files_location)
os.makedirs(directory, exist_ok=True)

# initalize pygame
pygame.init()
pygame.font.init()

# create the screen
background_color = (30,30,30)
window = pygame.display.set_mode((screen_width_px, screen_height_px), pygame.RESIZABLE, vsync=1)
screen = pygame.Surface((screen_width_px, screen_height_px))
pygame.display.set_caption(APP_DISPLAY_NAME)

Font_Manager.init(resource_path(f"game_files/{FONTS_FILE_NAME}"))
fonts = Font_Manager.get()

settings_directory = os.path.join(save_path, VERSION_NAME, "settings")
os.makedirs(settings_directory, exist_ok=True)
Settings_Manager.init(settings_directory)
settings = Settings_Manager.get()

launch_load_screen = Launch_Load_Screen(screen, window, screen_width_px, screen_height_px)
launch_load_screen.draw(0, 'Loading Game Files')

icon_surface = pygame.image.load(resource_path(f"game_files/{IMAGES_FILE_NAME}/{pygame_icon_file}"))
pygame.display.set_icon(icon_surface)

# load in images
images = Images(resource_path(f"game_files/{IMAGES_FILE_NAME}"), BLOCK_WIDTH)

launch_load_screen.draw(15, 'Launching Menu')

true_height = screen_height_px - INVENTORY_HEIGHT
MOVEMENT_ALTITUDE_PX = (true_height * 13) // 16

# clock features
clock = pygame.time.Clock()
TICKS = 60

# run details
grid_width = 5000
grid_height = 150
world_generation_settings = World_Generation_Settings(VERSION, INVENTORY_HEIGHT, HEALTH_BAR_HEIGHT, grid_width, grid_height, BLOCK_WIDTH)
menu = Menu(screen, window, images, fonts, screen_width_px, screen_height_px, BLOCK_WIDTH, get_user_worlds_list(directory, IMAGES_FILE_NAME, VERSION), directory, world_generation_settings, APP_DISPLAY_NAME)

# running class
run_class = menu
input_object = Input()

# crash handling
last_frame_failed = False

launch_load_screen.draw(99, 'Finishing Up Menu')

# code for getting fps: fps = clock.get_fps()

# ----------------------------------------------- run loop ------------------------------------------------ #
try:
    while True:

        try:
            # prep reset force quit var
            force_quit_crash = last_frame_failed and not isinstance(run_class, Crash_Menu)

            # get scale stuff
            scale, offx, offy = blit_letterboxed(screen, window, background_color)

            # get inputs
            input_object.take_input(scale, offx, offy)

            # quit if requested
            if input_object.check_quit(): 
                run_class.on_quit()
                break

            # execute run function, includes drawing
            run_class = run_class.run(input_object, clock)

            # update screen
            pygame.display.flip()

            # update clock
            clock.tick(TICKS)

            # reset the quit counter
            if force_quit_crash: last_frame_failed = False

        except Exception as recoverableError:
            print("CRASH DETECTED")
            traceback.print_exc()

            if last_frame_failed: break # kills the game loop on two consecutive failures

            run_class = run_class.catch_exception()
            last_frame_failed = True


except Exception as e: # this means the whole game crashed including on reboot
    print("FATAL CRASH DETECTED")
    traceback.print_exc()

pygame.quit()
