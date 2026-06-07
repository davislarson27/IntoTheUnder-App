import pygame


class Menu_Help:
    def __init__(self, screen, menu):
        self.screen = screen
        self.menu = menu

    def run(self, input, clock):
        if input.escape_keypress:
            return self.menu
        self.draw()
        return self

    def draw(self):
        self.screen.fill((0, 0, 0))

    def on_quit(self):
        pass

    def catch_exception(self):
        return self.menu
