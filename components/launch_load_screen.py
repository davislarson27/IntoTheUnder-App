import pygame
from components.blit_letterboxed import blit_letterboxed
import components.fonts as font_manager


class Launch_Load_Screen:
    def __init__(self, screen, window, width_px, height_px):
        self.screen = screen
        self.window = window
        _f = font_manager.get()
        self.font = pygame.font.Font(str(_f.PixeloidSans), 22)
        self.background_color = (30, 30, 30)

        blocks_width = 28
        blocks_height = 28
        menu_block_width = width_px // blocks_width
        menu_block_height = height_px // blocks_height

        center_column_width = 12
        center_column_margin_x = (blocks_width - center_column_width) // 2
        self.bar_rect = pygame.Rect(
            menu_block_width * center_column_margin_x,
            menu_block_height * 13,
            menu_block_width * center_column_width,
            menu_block_height * 2 - 10
        )

    def draw(self, percent_complete=0, message='Loading'):
        self.screen.fill(self.background_color)

        outline_color = (105, 110, 112)
        bar_color = (90, 140, 200)
        outline_width = 2

        inner_rect = pygame.Rect(
            self.bar_rect.left + outline_width,
            self.bar_rect.top + outline_width,
            self.bar_rect.width - (2 * outline_width),
            self.bar_rect.height - (2 * outline_width)
        )

        pygame.draw.rect(self.screen, outline_color, self.bar_rect, width=outline_width)

        fill = pygame.Rect(
            inner_rect.left,
            inner_rect.top,
            (inner_rect.width * percent_complete) // 100,
            inner_rect.height
        )
        pygame.draw.rect(self.screen, bar_color, fill)

        surf = self.font.render(f'{message}...', True, (255, 255, 255))
        rect = surf.get_rect(center=(inner_rect.centerx, inner_rect.top - 38))
        self.screen.blit(surf, rect)

        blit_letterboxed(self.screen, self.window, self.background_color)
        pygame.display.flip()
        pygame.event.pump()