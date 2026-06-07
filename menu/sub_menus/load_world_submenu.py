import pygame
from math import floor
import components.fonts as font_manager


class Credits:
    def __init__(self, screen, menu, world_directory, world_names_list):
        self.screen = screen
        self.menu = menu
        self.world_directory = world_directory
        self.world_names_list = world_names_list
        self.is_clicked = False

    # ------------------------------------------------------------------ #

    def run(self, input, clock):
        pass

    def draw(self, mx=0, my=0):
        pass

    # ── main loop interface ─────────────────────────────────────────────── #

    def on_quit(self):
        pass

    def catch_exception(self):
        return self.menu
