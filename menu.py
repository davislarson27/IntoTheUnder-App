import pygame
from math import floor

from grid import Grid
from world_generation import generate_world_blocks


class Menu:
    def __init__(self, screen, width_px, height_px, BLOCK_WIDTH):
        #most attributes
        self.menu_type = "main"
        self.screen = screen
        self.width = width_px
        self.height = height_px
        self.run_game = False
        self.button_font = pygame.font.Font(None, 35)  # None = default font
        self.title_font = pygame.font.Font(None, 60)
        self.camera_x = 0
        self.background_move_speed = 0.2
        self.menu_running = True
        self.button_color = (140, 140, 140)
        self.button_select_color = (165, 165, 165)
        
        # world options
        self.load_world = False
        self.generate_new_world = False


        #click variables
        self.is_clicked = False
        self.position_on_click = None

        # menu works under 10x10 grid where it chooses which get filled - these are the dementions for the "blocks"
        self.menu_block_width = self.width // 24
        self.menu_block_height = self.height // 24

        #objects on the menu
        self.load_world_dimentions = pygame.Rect(self.menu_block_width * 6, self.menu_block_height * 9, self.menu_block_width * 12, self.menu_block_height * 2)
        self.create_new_world_dimentions = pygame.Rect(self.menu_block_width * 6, self.menu_block_height * 12, self.menu_block_width * 12, self.menu_block_height * 2)
        self.exit_dimentions = pygame.Rect(self.menu_block_width * 6, self.menu_block_height * 15, self.menu_block_width * 12, self.menu_block_height * 2)



        # generate menu background world
        load_screen_block_width = floor(BLOCK_WIDTH * 1.15) #slightly enlarge the blocks
        self.width_blocks = (width_px // load_screen_block_width) * 4
        self.height_blocks = (height_px // load_screen_block_width) * 4
        self.background_world_width_px = floor(self.width_blocks * load_screen_block_width)
        self.background_grid = Grid(self.width_blocks, self.height_blocks, load_screen_block_width, screen)
        generate_world_blocks(self.background_grid, self.width_blocks, self.height_blocks)


    def execute_clicked(self, position_on_release):
        if self.menu_type == "main":
            if self.load_world_dimentions.collidepoint(self.position_on_click) and self.load_world_dimentions.collidepoint(position_on_release):
                # self.menu_type = "load"
                self.load_world = True
                self.run_game = True
            elif self.create_new_world_dimentions.collidepoint(self.position_on_click) and self.create_new_world_dimentions.collidepoint(position_on_release):
                self.generate_new_world = True
                self.run_game = True
            elif self.exit_dimentions.collidepoint(self.position_on_click) and self.exit_dimentions.collidepoint(position_on_release):
                self.menu_running = False
                self.run_game = True


    def check_click(self, mouse):
        if not self.is_clicked and mouse.get_pressed()[0]: # detect click
            self.is_clicked = True
            self.position_on_click = mouse.get_pos()

        elif self.is_clicked and not mouse.get_pressed()[0]: # detect release
            self.execute_clicked(mouse.get_pos())
            self.is_clicked = False


    def move_background(self):
        if self.camera_x + self.width < self.background_world_width_px: self.camera_x += self.background_move_speed

    def draw(self, mouse):
        # draw background before menus
        self.screen.fill((30,30,30))
        self.background_grid.draw(floor(self.camera_x), 0)
        

        if self.menu_type == "main":
            # draw game title
            title_space = pygame.Rect(self.menu_block_width * 4, self.menu_block_height * 3, self.menu_block_width * 16, self.menu_block_height * 4)
            text_surf = self.title_font.render("Zombie Archeology", True, (255, 255, 255))
            text_rect = text_surf.get_rect(center=title_space.center)
            self.screen.blit(text_surf, text_rect)

            # create "load world" button
            if self.load_world_dimentions.collidepoint(mouse.get_pos()): cur_button_color = self.button_select_color
            else: cur_button_color = self.button_color
            pygame.draw.rect( # menu button
                self.screen,
                cur_button_color,
                self.load_world_dimentions
            )
            text_surf = self.button_font.render("Load World", True, (255, 255, 255))
            text_rect = text_surf.get_rect(center=self.load_world_dimentions.center)
            self.screen.blit(text_surf, text_rect)

            # create "create new world" button
            if self.create_new_world_dimentions.collidepoint(mouse.get_pos()): cur_button_color = self.button_select_color
            else: cur_button_color = self.button_color
            pygame.draw.rect( # menu button
                self.screen,
                cur_button_color,
                self.create_new_world_dimentions
            )
            text_surf = self.button_font.render("Create New World", True, (255, 255, 255))
            text_rect = text_surf.get_rect(center=self.create_new_world_dimentions.center)
            self.screen.blit(text_surf, text_rect)

            # create "exit" button
            if self.exit_dimentions.collidepoint(mouse.get_pos()): cur_button_color = self.button_select_color
            else: cur_button_color = self.button_color
            pygame.draw.rect( # menu button
                self.screen,
                cur_button_color,
                self.exit_dimentions
            )
            text_surf = self.button_font.render("Exit", True, (255, 255, 255))
            text_rect = text_surf.get_rect(center=self.exit_dimentions.center)
            self.screen.blit(text_surf, text_rect)