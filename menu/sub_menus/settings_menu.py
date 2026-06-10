import pygame
from math import floor

import components.settings as settings
import components.fonts as font_manager


class Settings_Menu:
    def __init__(self, screen, menu):
        self.screen = screen
        self.menu = menu
        self.is_clicked = False

        self.settings_obj = settings.get()

        self.title_col   = (255, 255, 255)
        self.body_col    = (160, 165, 172)
        self.divider_col = (90, 95, 105)
        self.btn_col     = (140, 140, 140)
        self.btn_hov_col = (165, 165, 165)
        self.footer_col  = (200, 200, 200)
        self.panel_color = (16, 17, 22)

        self.W  = screen.get_width()
        self.H  = screen.get_height()
        self.mw = self.W // 28
        self.mh = self.H // 28

        _f = font_manager.get()
        self.title_font  = pygame.font.Font(str(_f.PixeloidSans_Bold), 32)
        self.body_font   = pygame.font.Font(str(_f.PixeloidSans),      14)
        self.btn_font    = pygame.font.Font(str(_f.PixeloidSans),      18)
        self.footer_font = pygame.font.Font(str(_f.PixeloidSans),      11)

        self.footer_h    = max(34, floor(self.mh * 1.0))
        self.footer_rect = pygame.Rect(0, self.H - self.footer_h, self.W, self.footer_h)

        side = self.mw * 3
        self.panel_rect = pygame.Rect(side, self.mh, self.W - side * 2,
                                      self.H - self.footer_h - self.mh * 2)
        self.panel_surf = pygame.Surface(self.panel_rect.size)
        self.panel_surf.fill(self.panel_color)

        btn_w = self.mw * 7
        btn_h = floor(self.mh * 1.8)
        self.back_btn = pygame.Rect((self.W - btn_w) // 2, 0, btn_w, btn_h)

    def run(self, input, clock):
        mx, my = input.virtual_mouse_x, input.virtual_mouse_y
        self.menu.move_background()

        if not self.is_clicked and input.mouse.get_pressed()[0]:
            self.is_clicked = True
        elif self.is_clicked and not input.mouse.get_pressed()[0]:
            self.is_clicked = False
            if self.back_btn.collidepoint((mx, my)):
                return self.menu

        if input.escape_keypress:
            return self.menu

        self.draw(mx, my)
        return self

    def draw(self, mx=0, my=0):
        self.menu.draw_background()
        self.screen.blit(self.panel_surf, self.panel_rect.topleft)

        cx = self.panel_rect.centerx
        inner_x = self.panel_rect.left + self.mw * 2
        inner_r = self.panel_rect.right - self.mw * 2
        y = self.panel_rect.top + self.mh

        title_surf = self.title_font.render("SETTINGS", True, self.title_col)
        self.screen.blit(title_surf, title_surf.get_rect(centerx=cx, top=y))
        y += title_surf.get_height() + self.mh // 2

        pygame.draw.line(self.screen, self.divider_col, (inner_x, y), (inner_r, y), 1)
        y += self.mh * 2

        body_surf = self.body_font.render("this menu is coming soon!", True, self.body_col)
        self.screen.blit(body_surf, body_surf.get_rect(centerx=cx, top=y))
        y += body_surf.get_height() + self.mh * 2

        self.back_btn.top = y
        btn_color = self.btn_hov_col if self.back_btn.collidepoint((mx, my)) else self.btn_col
        pygame.draw.rect(self.screen, btn_color, self.back_btn)
        bs = self.btn_font.render("Return to Menu", True, (255, 255, 255))
        self.screen.blit(bs, bs.get_rect(center=self.back_btn.center))

        pygame.draw.rect(self.screen, (30, 30, 30), self.footer_rect)
        pad = floor(self.mw * 0.6)
        fcy = self.footer_rect.centery
        ver = self.footer_font.render(self.menu.APP_DISPLAY_NAME, True, self.footer_col)
        cpy = self.footer_font.render("© Davis Larson 2026",      True, self.footer_col)
        self.screen.blit(ver, ver.get_rect(midleft=(pad, fcy)))
        self.screen.blit(cpy, cpy.get_rect(midright=(self.W - pad, fcy)))

    def on_quit(self): pass
    def catch_exception(self): return self.menu
