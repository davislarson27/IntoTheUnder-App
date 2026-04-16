import pygame

class Escape_Menu:
    def __init__(self, screen):
        # general variables
        self.screen = screen

        # click variables
        self.is_clicked = False

        # colors
        self.background_color = (30, 30, 30)

    def open(self, side_pannel_use=None):
        pass

    def open_off_cycle(self):
        pass

    def open_chest(self, chest_items):
        pass

    def close(self):
        pass

    def draw(self):
        self.screen.fill(self.background_color)

    def run(self, input):
        self.check_click(input.mouse, input.virtual_mouse_x, input.virtual_mouse_y)
        self.draw()

        return self

    def check_click(self, mouse, mx, my):
        if not self.is_clicked and mouse.get_pressed()[0]:
            self.is_clicked = True
        elif self.is_clicked and not mouse.get_pressed()[0]:
            self.is_clicked = False
            self.execute_clicked((mx, my))
