import pygame
from math import floor, ceil
import shutil
from pathlib import Path
import json
import random
import hashlib

from world.world_creation.generate_world import *
from components.text_box import Text_Box
from play.play import Play
from components.blit_letterboxed import blit_letterboxed
from components.game_file_reading import save_game
from world.world_creation.world_generation_settings import World_Generation_Settings
from play.player import Player
from play.inventory.inventory import Inventory
from components.world_details import World_Details
from components.crash_menu import Crash_Menu
from play.bg_overlay import BG_Overlay
from .sub_menus.credits import Credits
from .sub_menus.settings_menu import Settings_Menu

"""
explanation:

the menu works by using a self.blocks_width by self.blocks_height grid. 
boxes are generated during initialization
the main game loops calls the menu by calling menu.draw_function
self.draw_function holds a class method that actually draws the screen and is what click selection is based on
the subclass does the drawing
self.execute_clicked() checks self.draw_function to see what is on the screen
it then checks the mouse coordinates on click and compares them against the expected hit boxes and executes a function

"""


class Menu:
    def __init__(self, screen, window, images, fonts, width_px, height_px, BLOCK_WIDTH, world_names_list, game_files_directory, world_generation_settings, APP_DISPLAY_NAME):
        # draw_function_call
        self.draw_function = self.draw_main

        self.return_to = None

        # most attributes
        self.screen = screen
        self.window = window
        self.images = images
        self.fonts = fonts
        self.width = width_px
        self.height = height_px
        self.block_width = BLOCK_WIDTH
        self.APP_DISPLAY_NAME = APP_DISPLAY_NAME
        self.run_game = False

        # initialize main menu submenus
        self.credits = Credits(screen, self)
        self.settings = Settings_Menu(screen, self)

        # initialize fonts
        self.button_font               = pygame.font.Font(str(fonts.PixeloidSans), 18)
        self.small_button_font         = pygame.font.Font(str(fonts.PixeloidSans), 14)
        self.loading_world_screen_font = pygame.font.Font(str(fonts.PixeloidSans), 22)
        self.title_font                = pygame.font.Font(str(fonts.PixeloidSans_Bold), 48)
        self.small_title_font          = pygame.font.Font(str(fonts.PixeloidSans_Bold), 36)
        self.create_world_title_font   = pygame.font.Font(str(fonts.PixeloidSans_Bold), 32)
        self.subscript_font            = pygame.font.Font(str(fonts.PixeloidSans), 11)
        self.medium_font               = pygame.font.Font(str(fonts.PixeloidSans), 24)
        self.input_font                = pygame.font.Font(str(fonts.PixeloidMono), 18)

        self.camera_x = 0
        self.background_move_speed = 0.2
        self.menu_running = True
        self.button_color = (140, 140, 140)
        self.button_select_color = (165, 165, 165)
        self.game_files_directory = game_files_directory
        self.world_generation_settings = world_generation_settings

        self.string_end_if_corrupted = " (CORRUPTED)" # 12 chars

        self.announce_message = None
        self.prev_draw_func = None

        self.world_names_list = world_names_list
        self.WORLDS_PER_LOAD_SCREEN = 3
        self.load_screen_factor = 0
        self.world_name = None
        self.special_world_reference_index = None
        
        # world options
        self.load_world = False
        self.generate_new_world = False
        self.world_name_length_limit = 50

        # click variables
        self.is_clicked = False
        self.position_on_click = None

        # menu works under 28x28 grid where it chooses which get filled - these are the dementions for the "blocks"
        self.blocks_width = 28
        self.blocks_height = 28
        self.menu_block_width = self.width // self.blocks_width
        self.menu_block_height = self.height // self.blocks_height

        # loading and saving world screen (gets pre initalized)
        self.loading_world_screen_background_color = (30, 30, 30)
        self.saving_world_title_surf = self.loading_world_screen_font.render("Saving World...", True, (255, 255, 255))
        loading_world_screen_column_width = 16
        loading_world_margin_x = (self.blocks_width - loading_world_screen_column_width) // 2
        self.loading_world_title_rect = pygame.Rect(self.menu_block_width * loading_world_margin_x, self.menu_block_height * 12, self.menu_block_width * loading_world_screen_column_width, self.menu_block_height * 2)
        self.saving_world_screen_text_rect = self.saving_world_title_surf.get_rect(center=self.loading_world_title_rect.center)

        # menu titles
        title_column_width = 16
        title_column_margin_x = (self.blocks_width - title_column_width)//2
        self.title_space = pygame.Rect(self.menu_block_width * title_column_margin_x, self.menu_block_height * 5, self.menu_block_width * title_column_width, self.menu_block_height * 4)
        self.small_title_space = pygame.Rect(self.menu_block_width * title_column_margin_x, self.menu_block_height * 5, self.menu_block_width * title_column_width, self.menu_block_height * 4)
        self.main_text_surf = self.title_font.render("Into the Under", True, (255, 255, 255))

        # text box details
        self.padding = 12
        self.new_world_name_text_box = Text_Box()

        # world detail screen state
        self.wd_name_text_box = Text_Box()
        self.wd_world_seed = None
        self.wd_world_size = None
        self.wd_original_clean_name = None
        self.wd_open_btn = pygame.Rect(0, 0, 0, 0)
        self.wd_cancel_btn = pygame.Rect(0, 0, 0, 0)
        self.wd_name_box_rect = pygame.Rect(0, 0, 0, 0)

        # buttons on the menu
        self.button0_dimentions = pygame.Rect(floor(self.menu_block_width * 0.5), self.menu_block_height * 1, floor(self.menu_block_width * 2.5), floor(self.menu_block_height * 1.75))
        
        center_column_width = 12
        center_column_margin_x = (self.blocks_width - center_column_width)//2
        self.button1_dimentions = pygame.Rect(
            self.menu_block_width * center_column_margin_x,
            self.menu_block_height * 10,
            self.menu_block_width * center_column_width,
            self.menu_block_height * 2
        )
        self.button2_dimentions = pygame.Rect(
            self.menu_block_width * center_column_margin_x,
            self.menu_block_height * 13,
            self.menu_block_width * center_column_width,
            self.menu_block_height * 2
        )
        self.button3_dimentions = pygame.Rect(
            self.menu_block_width * center_column_margin_x,
            self.menu_block_height * 16,
            self.menu_block_width * center_column_width,
            self.menu_block_height * 2
        )
        self.button4_dimentions = pygame.Rect(
            self.menu_block_width * center_column_margin_x,
            self.menu_block_height * 19,
            self.menu_block_width * center_column_width,
            self.menu_block_height * 2
        )

        # button 4 has split right-left options
        RL_width = 5.5
        self.button4L_dimentions = pygame.Rect(
            self.menu_block_width * center_column_margin_x,
            self.menu_block_height * 19,
            floor(self.menu_block_width * RL_width),
            self.menu_block_height * 2
        )
        self.button4R_dimentions = pygame.Rect(
            floor(self.menu_block_width * RL_width) + (self.menu_block_width * (center_column_margin_x + 1)),
            self.menu_block_height * 19,
            floor(self.menu_block_width * RL_width),
            self.menu_block_height * 2
        )

        longL_column_width = 9.75
        self.button1_longL_dimentions = pygame.Rect(
            self.menu_block_width * center_column_margin_x,
            self.menu_block_height * 10,
            self.menu_block_width * longL_column_width,
            self.menu_block_height * 2
        )
        self.button2_longL_dimentions = pygame.Rect(
            self.menu_block_width * center_column_margin_x,
            self.menu_block_height * 13,
            self.menu_block_width * longL_column_width,
            self.menu_block_height * 2
        )
        self.button3_longL_dimentions = pygame.Rect(
            self.menu_block_width * center_column_margin_x,
            self.menu_block_height * 16,
            self.menu_block_width * longL_column_width,
            self.menu_block_height * 2
        )

        self.button1_shortR_dimentions = pygame.Rect(
            floor(self.menu_block_width * longL_column_width) + (self.menu_block_width * (center_column_margin_x + 0.25)),
            self.menu_block_height * 10,
            self.menu_block_width * 2,
            self.menu_block_height * 2
        )
        self.button2_shortR_dimentions = pygame.Rect(
            floor(self.menu_block_width * longL_column_width) + (self.menu_block_width * (center_column_margin_x + 0.25)),
            self.menu_block_height * 13,
            self.menu_block_width * 2,
            self.menu_block_height * 2
        )
        self.button3_shortR_dimentions = pygame.Rect(
            floor(self.menu_block_width * longL_column_width) + (self.menu_block_width * (center_column_margin_x + 0.25)),
            self.menu_block_height * 16,
            self.menu_block_width * 2,
            self.menu_block_height * 2
        )

        # subtext boxes
        self.button1_subtext_dimentions = pygame.Rect(
            self.menu_block_width * center_column_margin_x,
            (self.menu_block_height * 9) + 3,
            self.menu_block_width * center_column_width,
            self.menu_block_height
        )


        # ------------------------------- world creation options ------------------------------- #

        self.world_size_options = ["Small", "Medium", "Large"]
        self.default_selected_world_size = 1 # default to Medium
        self.selected_world_size = self.default_selected_world_size
        self.size_to_width_dict = {
            "Small": 1000,
            "Medium": 5000,
            "Large": 15000
        }
        self.world_seed_text_box = Text_Box()
        self.seed_length = 100000000000000000
        self.custom_seed = self.getRandomSeed()
        self.default_keep_inventory = True
        self.keep_inventory = self.default_keep_inventory
        self.default_survival_mode = True
        self.survival_mode = self.default_survival_mode
        self.default_recipe_progression = True
        self.recipe_progression = self.default_recipe_progression

        # options screen - seed input and size selector
        self.seed_label_dimentions = pygame.Rect(
            self.menu_block_width * center_column_margin_x,
            self.menu_block_height * 9,
            self.menu_block_width * center_column_width,
            self.menu_block_height
        )
        self.seed_box_dimentions = pygame.Rect(
            self.menu_block_width * center_column_margin_x,
            self.menu_block_height * 10,
            self.menu_block_width * center_column_width,
            self.menu_block_height * 2
        )

        size_button_width = center_column_width / 3  
        size_button_gap = 0
        self.size_button_dimentions = []
        for i in range(3):
            x_offset = center_column_margin_x + (i * (size_button_width + size_button_gap))
            self.size_button_dimentions.append(pygame.Rect(
                floor(self.menu_block_width * x_offset),
                self.menu_block_height * 14,
                floor(self.menu_block_width * size_button_width),
                self.menu_block_height * 2
            ))

        self.size_label_dimentions = pygame.Rect(
            self.menu_block_width * center_column_margin_x,
            self.menu_block_height * 13,
            self.menu_block_width * center_column_width,
            self.menu_block_height
        )

        # ------------------------------- tabbed create-world panel ------------------------------- #

        empty = lambda: pygame.Rect(0, 0, 0, 0)
        self.active_tab = 0
        self.pixel_font_path = None
        self.tab_rects        = [empty(), empty(), empty()]
        self.cw_name_box_rect = empty()
        self.cw_seed_box_rect = empty()
        self.cw_dice_btn      = empty()
        self.cw_size_rects    = [empty(), empty(), empty()]
        self.cw_keep_inv_on   = empty()
        self.cw_keep_inv_off  = empty()
        self.cw_survival_on        = empty()
        self.cw_survival_off       = empty()
        self.cw_recipe_prog_on    = empty()
        self.cw_recipe_prog_off   = empty()
        self.cw_create_btn    = empty()
        self.cw_cancel_btn    = empty()

        # palette tied to the rest of the menu: gray panels/buttons, with the
        # same blue the loading bar uses (90,140,200) reserved for selection
        self.card_fill     = (50, 50, 50)
        self.card_border   = (80, 80, 80)
        self.field_fill    = (40, 40, 40)
        self.accent        = (90, 140, 200)
        self.accent_bright = (140, 190, 255)
        self.label_col     = (220, 220, 220)
        self.sublabel_col  = (160, 165, 170)
        self.error_border  = (160, 75, 75)

        # ------------------------------- main menu footer bar ------------------------------- #

        # which submenu (if any) the footer wants to open this frame; consumed in run()
        self.open_submenu = None

        self.footer_height = max(34, floor(self.menu_block_height * 1.0))
        self.footer_rect = pygame.Rect(0, self.height - self.footer_height, self.width, self.footer_height)
        self.footer_font = self.subscript_font
        self.footer_pad_x = floor(self.menu_block_width * 0.6)
        footer_cy = self.footer_rect.centery

        self.footer_text_col = (200, 200, 200)

        # version text (left side) — drawn from the app's display name so it stays in sync
        self.footer_version_surf = self.footer_font.render(self.APP_DISPLAY_NAME, True, self.footer_text_col)

        # link list (right side): "Help • Credits • Settings"
        self.footer_sep_surf = self.footer_font.render("•", True, self.footer_text_col)
        sep_w = self.footer_sep_surf.get_width()
        sep_gap = floor(self.menu_block_width * 0.35)

        footer_link_defs = [("Reset Menu", Menu), ("Credits", self.credits), ("Settings", self.settings)]
        link_surfs = [self.footer_font.render(lbl, True, self.footer_text_col) for lbl, _ in footer_link_defs]

        total_w = sum(s.get_width() for s in link_surfs) + (len(link_surfs) - 1) * (sep_gap * 2 + sep_w)
        x = self.width - self.footer_pad_x - total_w

        self.footer_items = []          # each: {"label", "target", "rect"}
        self.footer_sep_positions = []  # topleft positions for the "•" separators
        for i, ((lbl, target), surf) in enumerate(zip(footer_link_defs, link_surfs)):
            rect = surf.get_rect(midleft=(x, footer_cy))
            self.footer_items.append({"label": lbl, "target": target, "rect": rect})
            x += surf.get_width()
            if i < len(link_surfs) - 1:
                x += sep_gap
                self.footer_sep_positions.append(self.footer_sep_surf.get_rect(midleft=(x, footer_cy)).topleft)
                x += sep_w + sep_gap

        # ----------------------------------------- generate menu background world ----------------------------------------- #

        load_screen_block_width = floor(BLOCK_WIDTH * 1.15) #slightly enlarge the blocks
        self.width_blocks = (width_px // load_screen_block_width) * 3
        self.height_blocks = (height_px // load_screen_block_width) + 4
        self.background_world_width_px = floor(self.width_blocks * load_screen_block_width)

        menu_world_settings = World_Generation_Settings(
            world_generation_settings.version, 
            0, 
            0, 
            self.width_blocks, 
            self.height_blocks, 
            load_screen_block_width
        )

        menu_world_seed = self.getRandomSeed()
        menu_world_settings.reset_ground_level(13)
        world_details = World_Details('menu world', 'non-saved data', None, None)
        grid_superstructure = Grid_Superstructure(screen, menu_world_settings, world_details, world_seed=menu_world_seed)
        grid_superstructure.generate_world()
        self.background_grid, self.bg_background_grid = grid_superstructure.get_grids()

        self.bg_overlay = BG_Overlay(screen, self.background_grid.BLOCK_WIDTH, self.background_grid, self.bg_background_grid)

    def getRandomSeed(self):
        return str(int(random.random() * self.seed_length))

    def get_max_load_screens(self):
        return ceil(len(self.world_names_list) / self.WORLDS_PER_LOAD_SCREEN) 

    def execute_load_world(self, button_offset = 0):
        """
        loads world and resets menu to main
        button offset specifies which button got pressed (0 is the first option, 1 is the second, etc)
        """
        self.draw_function = self.draw_main
        self.load_world = True
        self.run_game = True
        self.world_name = self.world_names_list[(self.WORLDS_PER_LOAD_SCREEN * self.load_screen_factor) + button_offset]

    def execute_delete_world_confirmation(self, button_offset = 0):
        """
        runs process for when the delete button is pressed on the load page
        does not actually delete the world files
        """
        self.draw_function = self.draw_confirm_delete_screen
        self.world_name = self.world_names_list[(self.WORLDS_PER_LOAD_SCREEN * self.load_screen_factor) + button_offset]
        self.special_world_reference_index = (self.WORLDS_PER_LOAD_SCREEN * self.load_screen_factor) + button_offset

    def open_world_detail_screen(self, button_offset):
        self.world_name = self.world_names_list[(self.WORLDS_PER_LOAD_SCREEN * self.load_screen_factor) + button_offset]
        self.special_world_reference_index = (self.WORLDS_PER_LOAD_SCREEN * self.load_screen_factor) + button_offset
        clean_name = self.world_name
        if clean_name.endswith(self.string_end_if_corrupted):
            clean_name = clean_name[:-len(self.string_end_if_corrupted)]
        self.wd_original_clean_name = clean_name
        self.wd_name_text_box.open_text_box(clean_name)
        self.wd_world_seed, self.wd_world_size = self._read_world_details_quick(self.world_name)
        self.draw_function = self.draw_world_detail_screen

    def _read_world_details_quick(self, world_name):
        clean = world_name
        if clean.endswith(self.string_end_if_corrupted):
            clean = clean[:-len(self.string_end_if_corrupted)]
        path = Path(self.game_files_directory) / clean / "world_details.json"
        try:
            with open(path) as f:
                d = json.load(f)
            seed = d.get("world_seed", "Unknown")
            spawn_x = d.get("world_spawn_x", 0)
            grid_width = round((spawn_x * 2) / self.block_width)
            if grid_width <= 3000: size = "Small"
            elif grid_width <= 10000: size = "Medium"
            else: size = "Large"
            return seed, size
        except Exception:
            return "Unknown", "Unknown"

    def _rename_world(self, old_name, new_name):
        clean_old = old_name
        if clean_old.endswith(self.string_end_if_corrupted):
            clean_old = clean_old[:-len(self.string_end_if_corrupted)]
        old_path = Path(self.game_files_directory) / clean_old
        new_path = Path(self.game_files_directory) / new_name
        try:
            old_path.rename(new_path)
            details_path = new_path / "world_details.json"
            with open(details_path) as f:
                d = json.load(f)
            d["world_name"] = new_name
            with open(details_path, "w") as f:
                json.dump(d, f)
            idx = self.world_names_list.index(old_name)
            self.world_names_list[idx] = new_name
            return True
        except Exception:
            return False

    def delete_world_files(self, world_file_name):
        # step 1: strip file name of " (CORRUPTED)" if applicable
        # World (CORRUPTED)
        if len(world_file_name) > len(self.string_end_if_corrupted) and world_file_name[len(world_file_name) - len(self.string_end_if_corrupted) : ] == self.string_end_if_corrupted[:]:
            cleaned_world_file_name = world_file_name[0 : len(world_file_name) - len(self.string_end_if_corrupted)]
        else:
            cleaned_world_file_name = world_file_name
        
        delete_file_dir = Path(self.game_files_directory) / cleaned_world_file_name
        if (delete_file_dir).is_dir():
            shutil.rmtree(delete_file_dir)
            self.world_names_list.remove(world_file_name)
            # print(delete_file_dir)
            return True
        return False

    def execute_create_new_world(self):
        self.generate_new_world = True
        self.run_game = True

    def create_world_name(self): # this function will eventually be replaced by user input -> but for now it is auto generated
        add_on_value = len(self.world_names_list) + 1
        new_world_name = f"My World {add_on_value}"

        while new_world_name in self.world_names_list or f"{new_world_name}{self.string_end_if_corrupted}" in self.world_names_list:
            add_on_value += 1
            new_world_name = f"My World {add_on_value}"
        
        return new_world_name

    def create_announce_screen(self, message):
        self.announce_message = message
        self.prev_draw_func = self.draw_create_world_menu
        self.draw_function = self.draw_announce_and_return_screen

    def return_to_main(self):
        self.draw_function = self.draw_main
        self.load_world = False
        self.run_game = False
        self.menu_running = True
        self.generate_new_world = False
        self.world_name = None
        self.load_screen_factor = 0
        self.active_tab = 0

    def move_background(self):
        if self.camera_x + self.width < self.background_world_width_px: self.camera_x += self.background_move_speed

    def _menu_font(self, size):
        if self.pixel_font_path:
            try:
                return pygame.font.Font(self.pixel_font_path, size)
            except Exception:
                pass
        return pygame.font.Font(None, size)

    def _draw_dice_icon(self, rect, color=(222, 224, 230)):
        body = rect.inflate(-rect.width * 0.45, -rect.height * 0.45)
        pygame.draw.rect(self.screen, color, body, width=2, border_radius=4)
        r = max(2, body.width // 11)
        cx, cy = body.center
        ox, oy = body.width * 0.26, body.height * 0.26
        for dx, dy in [(cx - ox, cy - oy), (cx + ox, cy - oy), (cx, cy),
                       (cx - ox, cy + oy), (cx + ox, cy + oy)]:
            pygame.draw.circle(self.screen, color, (int(dx), int(dy)), r)

    def _draw_bag_icon(self, center, color=(200, 204, 210)):
        cx, cy = center
        body = pygame.Rect(cx - 9, cy - 3, 18, 13)
        pygame.draw.rect(self.screen, color, body, border_radius=3)
        pygame.draw.arc(self.screen, color, pygame.Rect(cx - 6, cy - 11, 12, 14),
                        3.14159, 2 * 3.14159, 2)

    def _draw_bulb_icon(self, center, color=(200, 204, 210)):
        cx, cy = center
        pygame.draw.circle(self.screen, color, (cx, cy - 3), 8, 2)
        pygame.draw.rect(self.screen, color, pygame.Rect(cx - 4, cy + 4, 8, 4))

    def _draw_book_icon(self, center, color=(200, 204, 210)):
        cx, cy = center
        pygame.draw.rect(self.screen, color, pygame.Rect(cx - 8, cy - 7, 16, 14))
        pygame.draw.line(self.screen, (50, 50, 50), (cx, cy - 7), (cx, cy + 7), 2)
        pygame.draw.line(self.screen, (50, 50, 50), (cx - 5, cy - 3), (cx - 2, cy - 3), 1)
        pygame.draw.line(self.screen, (50, 50, 50), (cx - 5, cy + 1), (cx - 2, cy + 1), 1)

    def _draw_heart_icon(self, center, color=(200, 204, 210)):
        cx, cy = center
        r, ox, oy = 5, 4, 2
        pygame.draw.circle(self.screen, color, (cx - ox, cy - oy), r)
        pygame.draw.circle(self.screen, color, (cx + ox, cy - oy), r)
        points = [
            (cx - ox - r, cy - oy),
            (cx,          cy + r + oy),
            (cx + ox + r, cy - oy),
        ]
        pygame.draw.polygon(self.screen, color, points)

    def _draw_trash_icon(self, center, color=(222, 224, 230)):
        cx, cy = center
        pygame.draw.rect(self.screen, color, pygame.Rect(cx - 3, cy - 11, 6, 3), border_radius=1)
        pygame.draw.rect(self.screen, color, pygame.Rect(cx - 9, cy - 9, 18, 3), border_radius=1)
        pygame.draw.rect(self.screen, color, pygame.Rect(cx - 7, cy - 6, 14, 14), width=2, border_radius=2)
        for offset in (-3, 0, 3):
            pygame.draw.line(self.screen, color, (cx + offset, cy - 4), (cx + offset, cy + 6), 1)

    def draw_main(self, mx, my, input):
        # draw game title
        text_rect = self.main_text_surf.get_rect(center=self.title_space.center)
        self.screen.blit(self.main_text_surf, text_rect)

        # create "load world" button
        if self.button1_dimentions.collidepoint((mx, my)): cur_button_color = self.button_select_color
        else: cur_button_color = self.button_color
        pygame.draw.rect( # menu button
            self.screen,
            cur_button_color,
            self.button1_dimentions
        )
        text_surf = self.button_font.render("Load World", True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=self.button1_dimentions.center)
        self.screen.blit(text_surf, text_rect)

        # create "create new world" button
        if self.button2_dimentions.collidepoint((mx, my)): cur_button_color = self.button_select_color
        else: cur_button_color = self.button_color
        pygame.draw.rect( # menu button
            self.screen,
            cur_button_color,
            self.button2_dimentions
        )
        text_surf = self.button_font.render("Create New World", True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=self.button2_dimentions.center)
        self.screen.blit(text_surf, text_rect)

        # create "exit" button
        if self.button3_dimentions.collidepoint((mx, my)): cur_button_color = self.button_select_color
        else: cur_button_color = self.button_color
        pygame.draw.rect( # menu button
            self.screen,
            cur_button_color,
            self.button3_dimentions
        )
        text_surf = self.button_font.render("Exit", True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=self.button3_dimentions.center)
        self.screen.blit(text_surf, text_rect)

        # footer bar (over the background art, below the menu buttons)
        self.draw_footer(mx, my)

    def draw_footer(self, mx, my):
        text_col = self.footer_text_col

        # solid background bar
        pygame.draw.rect(self.screen, (40, 40, 40), self.footer_rect)

        # version text (left, vertically centered)
        vrect = self.footer_version_surf.get_rect(midleft=(self.footer_pad_x, self.footer_rect.centery))
        self.screen.blit(self.footer_version_surf, vrect)

        # separators
        for sep_pos in self.footer_sep_positions:
            self.screen.blit(self.footer_sep_surf, sep_pos)

        # clickable links (right), underline on hover
        for item in self.footer_items:
            hovered = item["rect"].collidepoint((mx, my))
            surf = self.footer_font.render(item["label"], True, text_col)
            self.screen.blit(surf, item["rect"].topleft)
            if hovered:
                underline_y = item["rect"].bottom - 1
                pygame.draw.line(self.screen, text_col,
                                 (item["rect"].left, underline_y),
                                 (item["rect"].right, underline_y), 1)

    def draw_load_menu(self, mx, my, input):

        if len(self.world_names_list) > 0: # checks to make sure there are actual worlds that can be loaded
            start_world_position = self.load_screen_factor * self.WORLDS_PER_LOAD_SCREEN

            # draw game title
            load_screen_text_surf = self.small_title_font.render(f"Select World ({self.load_screen_factor+1}/{self.get_max_load_screens()})", True, (255, 255, 255))

            text_rect = load_screen_text_surf.get_rect(center=self.title_space.center)
            self.screen.blit(load_screen_text_surf, text_rect)

            # draw back button
            if self.button0_dimentions.collidepoint((mx, my)): cur_button_color = self.button_select_color
            else: cur_button_color = self.button_color
            pygame.draw.rect( # menu button
                self.screen,
                cur_button_color,
                self.button0_dimentions
            )
            text_surf = self.small_button_font.render("Back", True, (255, 255, 255))
            text_rect = text_surf.get_rect(center=self.button0_dimentions.center)
            self.screen.blit(text_surf, text_rect)


            # create first option button
            if self.WORLDS_PER_LOAD_SCREEN * self.load_screen_factor < len(self.world_names_list):
                if self.button1_longL_dimentions.collidepoint((mx, my)): cur_button_color = self.button_select_color
                else: cur_button_color = self.button_color
                pygame.draw.rect( # menu button
                    self.screen,
                    cur_button_color,
                    self.button1_longL_dimentions
                )
                text_surf = self.button_font.render(self.world_names_list[start_world_position], True, (255, 255, 255))
                text_rect = text_surf.get_rect(center=self.button1_longL_dimentions.center)
                self.screen.blit(text_surf, text_rect)

                # delete button
                if self.button1_shortR_dimentions.collidepoint((mx, my)): cur_button_color = self.button_select_color
                else: cur_button_color = self.button_color
                pygame.draw.rect( # menu button
                    self.screen,
                    cur_button_color,
                    self.button1_shortR_dimentions
                )
                self._draw_trash_icon(self.button1_shortR_dimentions.center)



            # create second option button
            if (self.WORLDS_PER_LOAD_SCREEN * self.load_screen_factor) + 1 < len(self.world_names_list):
                if self.button2_longL_dimentions.collidepoint((mx, my)): cur_button_color = self.button_select_color
                else: cur_button_color = self.button_color
                pygame.draw.rect( # menu button
                    self.screen,
                    cur_button_color,
                    self.button2_longL_dimentions
                )
                text_surf = self.button_font.render(self.world_names_list[start_world_position + 1], True, (255, 255, 255))
                text_rect = text_surf.get_rect(center=self.button2_longL_dimentions.center)
                self.screen.blit(text_surf, text_rect)

                
                # draw delete
                if self.button2_shortR_dimentions.collidepoint((mx, my)): cur_button_color = self.button_select_color
                else: cur_button_color = self.button_color
                pygame.draw.rect( # menu button
                    self.screen,
                    cur_button_color,
                    self.button2_shortR_dimentions
                )
                self._draw_trash_icon(self.button2_shortR_dimentions.center)

            # create third option button
            if (self.WORLDS_PER_LOAD_SCREEN * self.load_screen_factor) + 2 < len(self.world_names_list):
                if self.button3_longL_dimentions.collidepoint((mx, my)): cur_button_color = self.button_select_color
                else: cur_button_color = self.button_color
                pygame.draw.rect( # menu button
                    self.screen,
                    cur_button_color,
                    self.button3_longL_dimentions
                )
                text_surf = self.button_font.render(self.world_names_list[start_world_position + 2], True, (255, 255, 255))
                text_rect = text_surf.get_rect(center=self.button3_longL_dimentions.center)
                self.screen.blit(text_surf, text_rect)
                
                # delete button
                if self.button3_shortR_dimentions.collidepoint((mx, my)): cur_button_color = self.button_select_color
                else: cur_button_color = self.button_color
                pygame.draw.rect( # menu button
                    self.screen,
                    cur_button_color,
                    self.button3_shortR_dimentions
                )
                self._draw_trash_icon(self.button3_shortR_dimentions.center)

            # create "Prev" option button
            if self.button4L_dimentions.collidepoint((mx, my)): cur_button_color = self.button_select_color
            else: cur_button_color = self.button_color
            pygame.draw.rect( # menu button
                self.screen,
                cur_button_color,
                self.button4L_dimentions
            )
            text_surf = self.button_font.render("Prev", True, (255, 255, 255))
            text_rect = text_surf.get_rect(center=self.button4L_dimentions.center)
            self.screen.blit(text_surf, text_rect)

            # create "Next" option button
            if self.button4R_dimentions.collidepoint((mx, my)): cur_button_color = self.button_select_color
            else: cur_button_color = self.button_color
            pygame.draw.rect( # menu button
                self.screen,
                cur_button_color,
                self.button4R_dimentions
            )
            text_surf = self.button_font.render("Next", True, (255, 255, 255))
            text_rect = text_surf.get_rect(center=self.button4R_dimentions.center)
            self.screen.blit(text_surf, text_rect)

        else: # render return button and error message

            text_surf = self.button_font.render("No World Files Found", True, (255, 255, 255))
            text_rect = text_surf.get_rect(center=self.button1_dimentions.center)
            self.screen.blit(text_surf, text_rect)

            # create return button
            if self.button2_dimentions.collidepoint((mx, my)): cur_button_color = self.button_select_color
            else: cur_button_color = self.button_color

            pygame.draw.rect( # return button button
                self.screen,
                cur_button_color,
                self.button2_dimentions
            )
            text_surf = self.button_font.render("Main Menu", True, (255, 255, 255))
            text_rect = text_surf.get_rect(center=self.button2_dimentions.center)
            self.screen.blit(text_surf, text_rect)

        self.draw_footer(mx, my)

    def draw_confirm_delete_screen(self, mx, my, input): # eventually this will allow deleting worlds in the game UI
                
        # draw game title
        load_screen_text_surf = self.medium_font.render(f"Are You Sure You Want to Delete \"{self.world_name}\"", True, (255, 255, 255))
        text_rect = load_screen_text_surf.get_rect(center=self.title_space.center)
        self.screen.blit(load_screen_text_surf, text_rect)

        # create return button
        if self.button1_dimentions.collidepoint((mx, my)): cur_button_color = self.button_select_color
        else: cur_button_color = self.button_color

        pygame.draw.rect( # return button button
            self.screen,
            cur_button_color,
            self.button1_dimentions
        )
        text_surf = self.button_font.render("Delete World", True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=self.button1_dimentions.center)
        self.screen.blit(text_surf, text_rect)


        # create return button
        if self.button2_dimentions.collidepoint((mx, my)): cur_button_color = self.button_select_color
        else: cur_button_color = self.button_color

        pygame.draw.rect( # return button button
            self.screen,
            cur_button_color,
            self.button2_dimentions
        )
        text_surf = self.button_font.render("Cancel", True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=self.button2_dimentions.center)
        self.screen.blit(text_surf, text_rect)

        self.draw_footer(mx, my)

    def draw_world_detail_screen(self, mx, my, input):
        self.wd_name_text_box.take_input(input, self.world_name_length_limit)

        mb_w, mb_h = self.menu_block_width, self.menu_block_height
        card_margin_x = mb_w * 5
        card_h = int(mb_h * 22)
        card = pygame.Rect(card_margin_x, (self.height - card_h) // 2, self.width - card_margin_x * 2, card_h)
        pad = mb_w * 1
        content_left = card.left + pad
        content_w = card.width - pad * 2

        pygame.draw.rect(self.screen, self.card_fill, card, border_radius=8)
        pygame.draw.rect(self.screen, self.card_border, card, width=1, border_radius=8)

        # title
        title_surf = self.create_world_title_font.render("World Details", True, (255, 255, 255))
        self.screen.blit(title_surf, title_surf.get_rect(center=(card.centerx, card.top + int(mb_h * 1.4))))

        y = card.top + mb_h * 3.5

        # world name text box
        self.screen.blit(self.subscript_font.render("WORLD NAME", True, self.sublabel_col), (content_left, int(y)))
        y += mb_h * 0.9
        self.wd_name_box_rect = pygame.Rect(content_left, int(y), int(content_w), int(mb_h * 2))
        active = self.wd_name_text_box.is_typing
        pygame.draw.rect(self.screen, self.field_fill, self.wd_name_box_rect)
        pygame.draw.rect(self.screen, self.accent_bright if active else self.card_border,
                         self.wd_name_box_rect, width=3 if active else 1)
        cursor = self.wd_name_text_box.get_text_cursor() if active else ""
        ns = self.input_font.render(self.wd_name_text_box.get_cur_string() + cursor, True, (235, 235, 235))
        self.screen.blit(ns, ns.get_rect(midleft=(self.wd_name_box_rect.left + self.padding,
                                                  self.wd_name_box_rect.centery)))
        y += mb_h * 2 + mb_h * 1.6

        # world info (seed + size)
        self.screen.blit(self.subscript_font.render("WORLD INFO", True, self.sublabel_col), (content_left, int(y)))
        y += mb_h * 1.1
        self.screen.blit(self.button_font.render(f"Seed:  {self.wd_world_seed}", True, self.label_col),
                         (int(content_left + mb_w * 0.5), int(y)))
        y += mb_h * 1.8
        self.screen.blit(self.button_font.render(f"Size:  {self.wd_world_size}", True, self.label_col),
                         (int(content_left + mb_w * 0.5), int(y)))

        # bottom buttons: Cancel (left) | Open World (right)
        btn_h = int(mb_h * 2)
        btn_y = card.bottom - int(mb_h) - btn_h
        gap = int(mb_w * 0.5)
        half_w = int((content_w - gap) / 2)

        self.wd_cancel_btn = pygame.Rect(content_left, btn_y, half_w, btn_h)
        cancel_hov = self.wd_cancel_btn.collidepoint((mx, my))
        pygame.draw.rect(self.screen, self.button_select_color if cancel_hov else self.button_color,
                         self.wd_cancel_btn, border_radius=4)
        ds = self.button_font.render("Cancel", True, (255, 255, 255))
        self.screen.blit(ds, ds.get_rect(center=self.wd_cancel_btn.center))

        self.wd_open_btn = pygame.Rect(content_left + half_w + gap, btn_y, half_w, btn_h)
        open_hov = self.wd_open_btn.collidepoint((mx, my))
        pygame.draw.rect(self.screen, self.button_select_color if open_hov else self.button_color,
                         self.wd_open_btn, border_radius=4)
        os_surf = self.button_font.render("Open World", True, (255, 255, 255))
        self.screen.blit(os_surf, os_surf.get_rect(center=self.wd_open_btn.center))

    def draw_loading_world_screen(self, percent_complete=0, message='Loading'):
        self.screen.fill(self.loading_world_screen_background_color)

        outline_color = (105, 110, 112)
        bar_color = (90, 140, 200)

        # --- BAR ---
        outline_width = 2
        loading_bar_outline_dimentions = pygame.Rect(
            self.button2_dimentions.left,
            self.button2_dimentions.top,
            self.button2_dimentions.width,
            self.button2_dimentions.height - 10
        )
        loading_bar_dimentions = pygame.Rect(
            loading_bar_outline_dimentions.left + outline_width,
            loading_bar_outline_dimentions.top + outline_width,
            loading_bar_outline_dimentions.width - (2 * outline_width),
            loading_bar_outline_dimentions.height - (2 * outline_width)
        )

        pygame.draw.rect(
            self.screen,
            outline_color,
            loading_bar_outline_dimentions,
            width=outline_width
        )

        percent_bar_fill = pygame.Rect(
            loading_bar_dimentions.left,
            loading_bar_dimentions.top,
            (loading_bar_dimentions.width * percent_complete) // 100,
            loading_bar_dimentions.height
        )
        pygame.draw.rect(self.screen, bar_color, percent_bar_fill)

        # --- TEXT ---
        surf = self.loading_world_screen_font.render(f'{message}...', True, (255,255,255))

        rect = surf.get_rect(
            center=(
                loading_bar_dimentions.centerx,
                loading_bar_dimentions.top - 38   # ← easy control
            )
        )

        self.screen.blit(surf, rect)

        blit_letterboxed(self.screen, self.window, self.loading_world_screen_background_color)
        pygame.display.flip()
        pygame.event.pump()

    def draw_announce_and_return_screen(self, mx, my, input):
            text_surf = self.medium_font.render(self.announce_message, True, (255, 255, 255))
            text_rect = text_surf.get_rect(center=self.button1_dimentions.center)
            self.screen.blit(text_surf, text_rect)

            # create return button
            if self.button2_dimentions.collidepoint((mx, my)): cur_button_color = self.button_select_color
            else: cur_button_color = self.button_color

            pygame.draw.rect( # return button button
                self.screen,
                cur_button_color,
                self.button2_dimentions
            )
            text_surf = self.button_font.render("Return", True, (255, 255, 255))
            text_rect = text_surf.get_rect(center=self.button2_dimentions.center)
            self.screen.blit(text_surf, text_rect)

            if self.prev_draw_func.__func__ is not self.draw_create_world_menu.__func__:
                self.draw_footer(mx, my)

    def draw_create_world_menu(self, mx, my, input):
        self.new_world_name_text_box.take_input(input, self.world_name_length_limit)
        self.world_seed_text_box.take_input(input, 20)
        self.world_name  = self.new_world_name_text_box.get_cur_string()
        self.custom_seed = self.world_seed_text_box.get_cur_string()

        mb_w, mb_h = self.menu_block_width, self.menu_block_height

        card_margin_x = mb_w * 5
        card_h = int(mb_h * 22)
        card = pygame.Rect(card_margin_x, (self.height - card_h) // 2,
                           self.width - card_margin_x * 2, card_h)
        pad = mb_w * 1
        content_left = card.left + pad
        content_w = card.width - pad * 2

        pygame.draw.rect(self.screen, self.card_fill, card, border_radius=8)
        pygame.draw.rect(self.screen, self.card_border, card, width=1, border_radius=8)

        title_surf = self.create_world_title_font.render("Create New World", True, (255, 255, 255))
        self.screen.blit(title_surf, title_surf.get_rect(
            center=(card.centerx, card.top + int(mb_h * 1.4))))

        tab_labels = ["General", "World", "Gameplay"]
        tab_y = card.top + mb_h * 2.7
        tab_h = mb_h * 1.4
        tab_w = content_w / 3
        self.tab_rects = []
        for i, label in enumerate(tab_labels):
            r = pygame.Rect(int(content_left + i * tab_w), int(tab_y), int(tab_w), int(tab_h))
            self.tab_rects.append(r)
            active = (i == self.active_tab)
            hover = r.collidepoint((mx, my))
            col = self.accent_bright if active else (205, 209, 214) if hover else (140, 145, 152)
            ts = self.button_font.render(label, True, col)
            self.screen.blit(ts, ts.get_rect(center=r.center))
            if active:
                ul = pygame.Rect(int(r.left + r.width * 0.18), r.bottom + 2,
                                 int(r.width * 0.64), 3)
                pygame.draw.rect(self.screen, self.accent, ul, border_radius=2)

        divider_y = int(tab_y + tab_h + 10)
        pygame.draw.line(self.screen, self.card_border,
                         (content_left, divider_y), (content_left + content_w, divider_y), 1)

        content_top = tab_y + tab_h + mb_h * 1.4

        if self.active_tab == 0:
            self._draw_basic_tab(mx, my, content_left, content_w, content_top, mb_h)
        elif self.active_tab == 1:
            self._draw_world_options_tab(mx, my, content_left, content_w, content_top, mb_h)
        else:
            self._draw_gameplay_tab(mx, my, content_left, content_w, content_top, mb_h)

        btn_h = int(mb_h * 2)
        btn_y = card.bottom - int(mb_h) - btn_h
        gap = int(mb_w * 0.5)
        half_w = int((content_w - gap) / 2)

        self.cw_cancel_btn = pygame.Rect(content_left, btn_y, half_w, btn_h)
        cancel_hov = self.cw_cancel_btn.collidepoint((mx, my))
        pygame.draw.rect(self.screen, self.button_select_color if cancel_hov else self.button_color,
                         self.cw_cancel_btn, border_radius=4)
        self.screen.blit(self.button_font.render("Cancel", True, (255, 255, 255)),
                         self.button_font.render("Cancel", True, (255, 255, 255)).get_rect(center=self.cw_cancel_btn.center))

        self.cw_create_btn = pygame.Rect(content_left + half_w + gap, btn_y, half_w, btn_h)
        hov = self.cw_create_btn.collidepoint((mx, my))
        pygame.draw.rect(self.screen, self.button_select_color if hov else self.button_color,
                         self.cw_create_btn, border_radius=4)
        cs = self.button_font.render("Create New World", True, (255, 255, 255))
        self.screen.blit(cs, cs.get_rect(center=self.cw_create_btn.center))

    def _draw_basic_tab(self, mx, my, left, w, top, mb_h):
        y = top

        # --- world name ---
        name_taken = (self.world_name in self.world_names_list
                      or f"{self.world_name}{self.string_end_if_corrupted}" in self.world_names_list)
        self.screen.blit(self.subscript_font.render("WORLD NAME", True, self.sublabel_col), (left, int(y)))
        if name_taken:
            err_surf = self.subscript_font.render("already in use", True, self.error_border)
            self.screen.blit(err_surf, err_surf.get_rect(midright=(left + w, int(y) + err_surf.get_height() // 2)))
        y += mb_h * 0.9
        self.cw_name_box_rect = pygame.Rect(left, int(y), int(w), int(mb_h * 2))
        active = self.new_world_name_text_box.is_typing
        pygame.draw.rect(self.screen, self.field_fill, self.cw_name_box_rect)
        name_border = self.error_border if name_taken else (self.accent_bright if active else self.card_border)
        pygame.draw.rect(self.screen, name_border,
                         self.cw_name_box_rect, width=3 if (active or name_taken) else 1)
        cursor = self.new_world_name_text_box.get_text_cursor() if active else ""
        ns = self.input_font.render(self.new_world_name_text_box.get_cur_string() + cursor,
                                    True, (235, 235, 235))
        self.screen.blit(ns, ns.get_rect(midleft=(self.cw_name_box_rect.left + self.padding,
                                                  self.cw_name_box_rect.centery)))
        y += mb_h * 2 + mb_h * 1.2

        # --- world seed (+ dice) ---
        self.screen.blit(self.subscript_font.render("WORLD SEED", True, self.sublabel_col), (left, int(y)))
        y += mb_h * 0.9
        dice_sz = mb_h * 2
        gap = mb_h * 0.4
        self.cw_seed_box_rect = pygame.Rect(left, int(y), int(w - dice_sz - gap), int(mb_h * 2))
        self.cw_dice_btn      = pygame.Rect(int(left + w - dice_sz), int(y), int(dice_sz), int(mb_h * 2))
        active = self.world_seed_text_box.is_typing
        pygame.draw.rect(self.screen, self.field_fill, self.cw_seed_box_rect)
        pygame.draw.rect(self.screen, self.accent_bright if active else self.card_border,
                         self.cw_seed_box_rect, width=3 if active else 1)
        cursor = self.world_seed_text_box.get_text_cursor() if active else ""
        ss = self.input_font.render(self.world_seed_text_box.get_cur_string() + cursor,
                                    True, (235, 235, 235))
        self.screen.blit(ss, ss.get_rect(midleft=(self.cw_seed_box_rect.left + self.padding,
                                                  self.cw_seed_box_rect.centery)))
        dice_hover = self.cw_dice_btn.collidepoint((mx, my))
        pygame.draw.rect(self.screen, self.button_select_color if dice_hover else self.button_color,
                         self.cw_dice_btn)
        self._draw_dice_icon(self.cw_dice_btn)
        y += mb_h * 2 + mb_h * 0.5

    def _draw_world_options_tab(self, mx, my, left, w, top, mb_h):
        y = top

        self.screen.blit(self.subscript_font.render("WORLD SIZE", True, self.sublabel_col), (left, int(y)))
        y += mb_h * 0.9
        sw = w / 3
        sh = mb_h * 2
        self.cw_size_rects = []
        for i, label in enumerate(self.world_size_options):
            bw = int(sw - (4 if i < 2 else 0))
            r = pygame.Rect(int(left + i * sw), int(y), bw, int(sh))
            self.cw_size_rects.append(r)
            if i == self.selected_world_size:
                pygame.draw.rect(self.screen, self.accent, r)
                pygame.draw.rect(self.screen, self.accent_bright, r, width=2)
            elif r.collidepoint((mx, my)):
                pygame.draw.rect(self.screen, self.button_select_color, r)
            else:
                pygame.draw.rect(self.screen, self.button_color, r)
            ts = self.button_font.render(label, True, (255, 255, 255))
            self.screen.blit(ts, ts.get_rect(center=r.center))

    def _draw_gameplay_tab(self, mx, my, left, w, top, mb_h):
        row_h    = mb_h * 2
        toggle_w = mb_h * 2.6
        toggle_h = mb_h * 1.4
        gap      = mb_h * 0.4

        def toggle_row(yc, icon_fn, label_text, value, on_attr, off_attr, locked=False):
            cy = int(yc + row_h / 2)
            label_col = self.sublabel_col if locked else self.label_col
            icon_fn((left + 14, cy), color=(120, 120, 120) if locked else (200, 204, 210))
            ls = self.button_font.render(label_text, True, label_col)
            self.screen.blit(ls, ls.get_rect(midleft=(left + 38, cy)))

            off_rect = pygame.Rect(int(left + w - toggle_w), int(yc + (row_h - toggle_h) / 2),
                                   int(toggle_w), int(toggle_h))
            on_rect = pygame.Rect(int(off_rect.left - gap - toggle_w), off_rect.top,
                                  int(toggle_w), int(toggle_h))
            setattr(self, on_attr, on_rect)
            setattr(self, off_attr, off_rect)

            for rect, is_on, txt in ((on_rect, True, "On"), (off_rect, False, "Off")):
                if locked:
                    pygame.draw.rect(self.screen, (85, 85, 90), rect)
                elif value == is_on:
                    pygame.draw.rect(self.screen, self.accent, rect)
                    pygame.draw.rect(self.screen, self.accent_bright, rect, width=2)
                else:
                    hov = rect.collidepoint((mx, my))
                    pygame.draw.rect(self.screen, self.button_select_color if hov else self.button_color, rect)
                text_col = (130, 130, 135) if locked else (255, 255, 255)
                t = self.small_button_font.render(txt, True, text_col)
                self.screen.blit(t, t.get_rect(center=rect.center))

        keep_inv_locked = not self.survival_mode

        toggle_row(top + mb_h * 0.5, self._draw_heart_icon, "Survival Mode",
                   self.survival_mode,  "cw_survival_on",  "cw_survival_off")
        toggle_row(top + mb_h * 3.0, self._draw_bag_icon,  "Keep Inventory",
                   self.keep_inventory, "cw_keep_inv_on", "cw_keep_inv_off", locked=keep_inv_locked)
        toggle_row(top + mb_h * 5.5, self._draw_book_icon, "Recipe Progression",
                   self.recipe_progression, "cw_recipe_prog_on", "cw_recipe_prog_off")

    def returnToLast(self):
        if self.return_to is None:
            self.return_to_main()
        else:
            self.draw_function = self.return_to
            self.return_to = None

    # ------------------------ main functions ------------------------ #

    def draw_background(self):
        self.screen.fill((30, 30, 30))
        self.bg_background_grid.draw(floor(self.camera_x), 0)
        self.bg_overlay.draw(floor(self.camera_x), 0, 0)
        self.background_grid.draw(floor(self.camera_x), 0)

    def draw(self, mx, my, input):
        self.draw_background()
        self.draw_function(mx, my, input)
    
    def execute_clicked(self, position_on_release): # may need to add in self.

        # main menu
        if self.draw_function.__func__ is self.draw_main.__func__:
            if self.button1_dimentions.collidepoint(self.position_on_click) and self.button1_dimentions.collidepoint(position_on_release):
                self.draw_function = self.draw_load_menu
            elif self.button2_dimentions.collidepoint(self.position_on_click) and self.button2_dimentions.collidepoint(position_on_release):
                self.world_name = self.create_world_name()
                self.new_world_name_text_box.open_text_box(self.world_name)
                self.world_seed_text_box.open_text_box(self.custom_seed)
                self.active_tab = 0
                self.draw_function = self.draw_create_world_menu
            elif self.button3_dimentions.collidepoint(self.position_on_click) and self.button3_dimentions.collidepoint(position_on_release):
                pygame.event.post(pygame.event.Event(pygame.QUIT))

        # if load world menu is active
        elif self.draw_function.__func__ is self.draw_load_menu.__func__:
            if len(self.world_names_list) > 0:
                # check the return button
                if self.button0_dimentions.collidepoint(self.position_on_click) and self.button0_dimentions.collidepoint(position_on_release):
                    self.returnToLast()
                
                # now check the launch world buttons
                elif self.button1_longL_dimentions.collidepoint(self.position_on_click) and self.button1_longL_dimentions.collidepoint(position_on_release):
                    if self.WORLDS_PER_LOAD_SCREEN * self.load_screen_factor < len(self.world_names_list):
                        self.open_world_detail_screen(0)
                elif self.button2_longL_dimentions.collidepoint(self.position_on_click) and self.button2_longL_dimentions.collidepoint(position_on_release):
                    if (self.WORLDS_PER_LOAD_SCREEN * self.load_screen_factor) + 1 < len(self.world_names_list):
                        self.open_world_detail_screen(1)
                elif self.button3_longL_dimentions.collidepoint(self.position_on_click) and self.button3_longL_dimentions.collidepoint(position_on_release):
                    if (self.WORLDS_PER_LOAD_SCREEN * self.load_screen_factor) + 2 < len(self.world_names_list):
                        self.open_world_detail_screen(2)
                
                # check the delete world buttons
                elif self.button1_shortR_dimentions.collidepoint(self.position_on_click) and self.button1_shortR_dimentions.collidepoint(position_on_release):
                    if self.WORLDS_PER_LOAD_SCREEN * self.load_screen_factor < len(self.world_names_list):
                        self.execute_delete_world_confirmation(0)
                elif self.button2_shortR_dimentions.collidepoint(self.position_on_click) and self.button2_shortR_dimentions.collidepoint(position_on_release):
                    if (self.WORLDS_PER_LOAD_SCREEN * self.load_screen_factor) + 1 < len(self.world_names_list):
                        self.execute_delete_world_confirmation(1)
                elif self.button3_shortR_dimentions.collidepoint(self.position_on_click) and self.button3_shortR_dimentions.collidepoint(position_on_release):
                    if (self.WORLDS_PER_LOAD_SCREEN * self.load_screen_factor) + 2 < len(self.world_names_list):
                        self.execute_delete_world_confirmation(2)

                # check the load menu navigation buttons
                elif self.button4L_dimentions.collidepoint(self.position_on_click) and self.button4L_dimentions.collidepoint(position_on_release):
                    # prev button
                    self.load_screen_factor -= 1
                    if self.load_screen_factor < 0:
                        self.load_screen_factor = self.get_max_load_screens() - 1
                elif self.button4R_dimentions.collidepoint(self.position_on_click) and self.button4R_dimentions.collidepoint(position_on_release):
                    # next button
                    self.load_screen_factor += 1
                    if self.load_screen_factor > self.get_max_load_screens() - 1:
                        self.load_screen_factor = 0
            
            else: # allows alt return button to work
                if self.button2_dimentions.collidepoint(self.position_on_click) and self.button2_dimentions.collidepoint(position_on_release):
                    self.draw_function = self.draw_main

        # world detail screen
        elif self.draw_function.__func__ is self.draw_world_detail_screen.__func__:
            def hit(r):
                return r.collidepoint(self.position_on_click) and r.collidepoint(position_on_release)

            if self.wd_name_box_rect.collidepoint(self.position_on_click):
                self.wd_name_text_box.is_typing = True
            elif hit(self.wd_open_btn):
                self.wd_name_text_box.is_typing = False
                new_name = self.wd_name_text_box.get_cur_string().strip()
                if new_name == "":
                    pass
                elif new_name != self.wd_original_clean_name:
                    if (new_name in self.world_names_list
                            or f"{new_name}{self.string_end_if_corrupted}" in self.world_names_list):
                        self.announce_message = f"World Name \"{new_name}\" is Already in Use"
                        self.prev_draw_func = self.draw_world_detail_screen
                        self.draw_function = self.draw_announce_and_return_screen
                    elif self._rename_world(self.world_name, new_name):
                        self.world_name = new_name
                        self.draw_function = self.draw_main
                        self.load_world = True
                        self.run_game = True
                    else:
                        self.announce_message = "Failed to Rename World"
                        self.prev_draw_func = self.draw_world_detail_screen
                        self.draw_function = self.draw_announce_and_return_screen
                else:
                    self.draw_function = self.draw_main
                    self.load_world = True
                    self.run_game = True
            elif hit(self.wd_cancel_btn):
                self.wd_name_text_box.is_typing = False
                new_name = self.wd_name_text_box.get_cur_string().strip()
                if (new_name and new_name != self.wd_original_clean_name
                        and new_name not in self.world_names_list
                        and f"{new_name}{self.string_end_if_corrupted}" not in self.world_names_list):
                    self._rename_world(self.world_name, new_name)
                self.draw_function = self.draw_load_menu
                self.world_name = None
                self.special_world_reference_index = None
                self.wd_original_clean_name = None
            else:
                self.wd_name_text_box.is_typing = False

        # confirm world deletion menu
        elif self.draw_function.__func__ is self.draw_confirm_delete_screen.__func__:
            # selected yes
            if self.button1_dimentions.collidepoint(self.position_on_click) and self.button1_dimentions.collidepoint(position_on_release):
                # self.announce_message = "successfully deleted f{}"  
                if self.delete_world_files(self.world_names_list[self.special_world_reference_index]):
                    self.announce_message = f"Successfully Deleted \"{self.world_name}\""
                else:
                    self.announce_message = f"Failed to Delete \"{self.world_name}\""
                self.draw_function = self.draw_announce_and_return_screen
                self.special_world_reference_index = None
                self.world_name = None
                self.load_screen_factor = 0 # ensures that when the user clicks back in it doesn't throw an index error
                self.prev_draw_func = self.draw_load_menu
            # selected no
            elif self.button2_dimentions.collidepoint(self.position_on_click) and self.button2_dimentions.collidepoint(position_on_release):
                self.draw_function = self.draw_load_menu
                self.special_world_reference_index = None
                self.world_name = None

        # print alert system and return to last
        elif self.draw_function.__func__ is self.draw_announce_and_return_screen.__func__:
            if self.button2_dimentions.collidepoint(self.position_on_click) and self.button2_dimentions.collidepoint(position_on_release):
                self.draw_function = self.prev_draw_func

        # create new world menu (tabbed)
        elif self.draw_function.__func__ is self.draw_create_world_menu.__func__:
            def hit(r):
                return r.collidepoint(self.position_on_click) and r.collidepoint(position_on_release)

            def blur_boxes():
                self.new_world_name_text_box.is_typing = False
                self.world_seed_text_box.is_typing = False

            if hit(self.cw_cancel_btn):
                blur_boxes()
                self.returnToLast()
            elif hit(self.tab_rects[0]):
                self.active_tab = 0; blur_boxes()
            elif hit(self.tab_rects[1]):
                self.active_tab = 1; blur_boxes()
            elif hit(self.tab_rects[2]):
                self.active_tab = 2; blur_boxes()
            elif hit(self.cw_create_btn):
                if (self.world_name in self.world_names_list
                        or f"{self.world_name}{self.string_end_if_corrupted}" in self.world_names_list):
                    self.create_announce_screen(f"World Name \"{self.world_name}\" is Already in Use")
                else:
                    self.execute_create_new_world()
            elif self.active_tab == 0:
                if hit(self.cw_dice_btn):
                    self.custom_seed = self.getRandomSeed()
                    self.world_seed_text_box.open_text_box(self.custom_seed)
                    blur_boxes()
                elif self.cw_name_box_rect.collidepoint(self.position_on_click):
                    self.new_world_name_text_box.is_typing = True
                    self.world_seed_text_box.is_typing = False
                elif self.cw_seed_box_rect.collidepoint(self.position_on_click):
                    self.world_seed_text_box.is_typing = True
                    self.new_world_name_text_box.is_typing = False
                else:
                    blur_boxes()
            elif self.active_tab == 1:
                for i, rect in enumerate(self.cw_size_rects):
                    if hit(rect):
                        self.selected_world_size = i
            elif self.active_tab == 2:
                if hit(self.cw_survival_on):
                    self.survival_mode = True
                elif hit(self.cw_survival_off):
                    self.survival_mode = False
                elif hit(self.cw_keep_inv_on):
                    self.keep_inventory = True
                elif hit(self.cw_keep_inv_off):
                    self.keep_inventory = False
                elif hit(self.cw_recipe_prog_on):
                    self.recipe_progression = True
                elif hit(self.cw_recipe_prog_off):
                    self.recipe_progression = False

        # footer links work on every screen that renders the footer (not create world)
        if self.draw_function.__func__ is not self.draw_create_world_menu.__func__:
            for item in self.footer_items:
                if (item["rect"].collidepoint(self.position_on_click) and
                        item["rect"].collidepoint(position_on_release)):
                    self.open_submenu = item["target"]
                    if self.open_submenu is Menu: # hyjacks situation where the menu class is reset
                        self.open_submenu = Menu(self.screen, self.window, self.images, self.fonts, self.width, self.height, self.block_width, self.world_names_list, self.game_files_directory, self.world_generation_settings, self.APP_DISPLAY_NAME)
                    break

    def check_click(self, mouse, mx, my):
        if not self.is_clicked and mouse.get_pressed()[0]: # detect click
            self.is_clicked = True
            self.position_on_click = (mx, my)

        elif self.is_clicked and not mouse.get_pressed()[0]: # detect release
            self.execute_clicked((mx, my))
            self.is_clicked = False

    # ------------------------ helper functions ------------------------ #
    
    def create_new_world_with_loading(self):
        # initialize the loading screen
        self.draw_loading_world_screen(0, 'Prepping World Generator')

        def resolve_seed():
            seed_string = self.custom_seed.strip()
            try:
                seedValue = int(seed_string)
                return seedValue
            except ValueError:
                value = int(hashlib.sha256(seed_string.encode()).hexdigest(), 16)
                return value % self.seed_length

        # create directory name
        new_directory_path = Path(f"{self.game_files_directory}/{self.world_name}")

        # initialize inventory, player, and world
        self.world_generation_settings.reset_ground_level(50)
        world_seed = resolve_seed()

        self.world_generation_settings.set_grid_width(self.size_to_width_dict[self.world_size_options[self.selected_world_size]])

        inventory = Inventory(self.screen, self.window, self.world_generation_settings.inventory_height, self.world_generation_settings.health_bar_height)
        world_spawn_x = ((self.world_generation_settings.grid_width * self.block_width) // 2)
        world_spawn_y = 0
        world_details = World_Details.create_new_world(self.world_name, self.world_generation_settings.version, world_spawn_x=world_spawn_x, world_spawn_y=world_spawn_y, world_seed=world_seed, keep_inventory=self.keep_inventory, survival_mode=self.survival_mode, recipe_progression=self.recipe_progression)

        # initialize grid and terrain
        grid_superstructure = Grid_Superstructure(self.screen, self.world_generation_settings, world_details, new_directory_path, world_seed, world_spawn_x)
        for GenerationText, percentComplete in grid_superstructure._generate_world():
            self.draw_loading_world_screen(percentComplete, GenerationText)
        grid, background_grid = grid_superstructure.get_grids()

        # create world save directory
        new_directory_path.mkdir()
        grid.generate_save_files()
        background_grid.generate_save_files()
        
        player = Player(grid, self.screen, world_spawn_x, world_spawn_y, self.block_width, x_size=22, y_size=40, inventory_bar_height=self.world_generation_settings.inventory_height, health_bar_height=self.world_generation_settings.health_bar_height, images=self.images, world_details=world_details)

        save_start_percent = 55
        save_end_percent = 99
        for percent, save_message in save_game(new_directory_path, player, inventory, grid, background_grid, world_details, save_start_percent, save_end_percent):
            self.draw_loading_world_screen(percent, save_message)

        # reset the grid caches to speed up saving
        grid.reset_save_cache()
        background_grid.reset_save_cache()

        self.custom_seed = self.getRandomSeed()

        player.prep_initial_spawn()

        return grid, background_grid, inventory, player, world_details
    
    def load_world_from_file(self):
        # load in the grid from the files
        self.draw_loading_world_screen(0, 'Prepping Foreground')
        foreground_directory = f"{self.game_files_directory}/{self.world_name}/foreground_grid"
        chunks_data, max_chunk_id = Grid.load_chunk_files(foreground_directory)

        # initalize the foreground grid
        loading_message = 'Loading Foreground'
        percent_start = 5
        percent_end = 51
        percent_tot_inc = percent_end - percent_start
        self.draw_loading_world_screen(percent_start, loading_message)

        worlds_directory = f"{self.game_files_directory}/{self.world_name}"
        for grid, percent_complete in Grid.fill_from_file_show_loading(chunks_data, max_chunk_id, foreground_directory, self.screen, self.block_width):
            full_process_percent_complete = (percent_tot_inc * percent_complete) + percent_start
            self.draw_loading_world_screen(full_process_percent_complete, loading_message)

        if grid is None:
            raise TypeError('Foreground grid failed to load correctly')
        
        # load in the background grid from the files
        self.draw_loading_world_screen(percent_end, 'Prepping Background')
        background_directory = f"{self.game_files_directory}/{self.world_name}/background_grid"
        chunks_data, max_chunk_id = Grid.load_chunk_files(background_directory)

        # initalize the background grid
        loading_message = 'Loading Background'
        percent_start = percent_end + 5
        percent_end = 94
        percent_tot_inc = percent_end - percent_start
        self.draw_loading_world_screen(percent_start, loading_message)

        for bg_grid, percent_complete in Grid.fill_from_file_show_loading(chunks_data, max_chunk_id, background_directory, self.screen, self.block_width):
            full_process_percent_complete = (percent_tot_inc * percent_complete) + percent_start
            self.draw_loading_world_screen(full_process_percent_complete, loading_message)

        if bg_grid is None:
            raise TypeError('Background grid failed to load correctly')

        self.draw_loading_world_screen(percent_end, 'Loading Inventory')

        with open(f"{worlds_directory}/inventory.json", "r") as inventory_file:
            inventory_dict = json.load(inventory_file)
            inventory = Inventory.fill_from_dict(inventory_dict, self.screen, self.window, self.world_generation_settings.inventory_height, self.world_generation_settings.health_bar_height)

        self.draw_loading_world_screen(97, 'Loading World Details')

        with open(f"{worlds_directory}/world_details.json", "r") as world_details_file:
            world_details_dict = json.load(world_details_file)
            world_details = World_Details.fill_from_dict(world_details_dict)

        with open(f"{worlds_directory}/player_attributes.json", "r") as player_attr_file:
            player_attr_dict = json.load(player_attr_file)
            player_attr_dict["screen"] = self.screen
            player_attr_dict["grid"] = grid
            player_attr_dict["inventory_bar_height"] = self.world_generation_settings.inventory_height
            player_attr_dict["health_bar_height"] = self.world_generation_settings.health_bar_height
            player = Player(**{**player_attr_dict, "images": self.images, "world_details": world_details})

        self.draw_loading_world_screen(99, 'Finishing Up')

        return grid, bg_grid, inventory, player, world_details
    
    def reopen_menu_prep(self):
        self.world_names_list.remove(self.world_name)
        self.world_names_list.insert(0, self.world_name)
        self.run_game = False
        self.return_to_main()
        self.custom_seed = self.getRandomSeed()
        self.selected_world_size = self.default_selected_world_size
        self.return_to = None
        self.keep_inventory = self.default_keep_inventory
        self.survival_mode = self.default_survival_mode
        self.recipe_progression = self.default_recipe_progression

    # ------------------------ functions interacting with the main loop ------------------------ #

    def catch_exception(self): # reboots the menu
        new_menu = Menu(self.screen, self.window, self.images, self.fonts, self.width, self.height, self.block_width, self.world_names_list, self.game_files_directory, self.world_generation_settings, self.APP_DISPLAY_NAME)
        return Crash_Menu(self.screen, new_menu, self, "Sorry... The Menu Crashed", "Attempt to Reload")

    def finalExceptionHandle(self):
        pass

    def run(self, input, clock):
        """runs the menu and returns function of class that will run next (normally itself)"""

        self.check_click(pygame.mouse, input.virtual_mouse_x, input.virtual_mouse_y)
        self.move_background()
        self.draw(input.virtual_mouse_x, input.virtual_mouse_y, input)

        # register keyboard inputs
        if input.escape_keypress:
            self.returnToLast()

        # a footer link was clicked — hand control to that submenu
        if self.open_submenu is not None:
            submenu = self.open_submenu
            self.open_submenu = None
            return submenu

        if self.run_game: # creates the play object that will be returned
            
            play_object = None

            if self.load_world:
                grid, background_grid, inventory, player, world_details = self.load_world_from_file()
                play_object = Play(self.screen, self.block_width, grid, background_grid, inventory, player, world_details, self)

            elif self.generate_new_world:
                self.world_names_list.insert(0, self.world_name)
                grid, background_grid, inventory, player, world_details = self.create_new_world_with_loading()
                play_object = Play(self.screen, self.block_width, grid, background_grid, inventory, player, world_details, self)

            if play_object is None: return self

            return play_object

        else:
            return self
    
    def on_quit(self):
        pass
    