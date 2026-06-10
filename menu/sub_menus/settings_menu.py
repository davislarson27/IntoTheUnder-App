import json
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
        self.active_tab = 0

        self.title_col     = (255, 255, 255)
        self.body_col      = (160, 165, 172)
        self.sublabel_col  = (160, 165, 170)
        self.label_col     = (220, 220, 220)
        self.divider_col   = (90, 95, 105)
        self.btn_col       = (140, 140, 140)
        self.btn_hov_col   = (165, 165, 165)
        self.footer_col    = (200, 200, 200)
        self.panel_color   = (16, 17, 22)
        self.accent        = (90, 140, 200)
        self.accent_bright = (140, 190, 255)

        self.W  = screen.get_width()
        self.H  = screen.get_height()
        self.mw = self.W // 28
        self.mh = self.H // 28

        _f = font_manager.get()
        self.title_font    = pygame.font.Font(str(_f.PixeloidSans_Bold), 32)
        self.sublabel_font = pygame.font.Font(str(_f.PixeloidSans),      11)
        self.body_font     = pygame.font.Font(str(_f.PixeloidSans),      14)
        self.tab_font      = pygame.font.Font(str(_f.PixeloidSans),      18)
        self.btn_font      = pygame.font.Font(str(_f.PixeloidSans),      18)
        self.footer_font   = pygame.font.Font(str(_f.PixeloidSans),      11)

        self.footer_h    = max(34, floor(self.mh * 1.0))
        self.footer_rect = pygame.Rect(0, self.H - self.footer_h, self.W, self.footer_h)

        side = self.mw * 3
        self.panel_rect = pygame.Rect(side, self.mh, self.W - side * 2,
                                      self.H - self.footer_h - self.mh * 2)
        self.panel_surf = pygame.Surface(self.panel_rect.size)
        self.panel_surf.fill(self.panel_color)

        btn_w = self.mw * 7
        btn_h = floor(self.mh * 1.8)
        self.back_btn  = pygame.Rect((self.W - btn_w) // 2, 0, btn_w, btn_h)
        self.tab_rects = []

        # selector options
        self.chunk_options     = ["0", "1", "2", "3", "4", "5"]
        self.world_size_options = ["Small", "Medium", "Large"]
        self.world_size_to_value = {"Small": 0, "Medium": 1, "Large": 2}

        chunk_val = self.settings_obj.physics_chunks_beyond_screen
        self.selected_chunks = chunk_val if 0 <= chunk_val <= 5 else 2

        self.selected_world_size = self.settings_obj.default_world_size

        self.chunk_rects = []
        self.size_rects  = []

    # ------------------------------------------------------------------ #

    def run(self, input, clock):
        mx, my = input.virtual_mouse_x, input.virtual_mouse_y
        self.menu.move_background()

        if not self.is_clicked and input.mouse.get_pressed()[0]:
            self.is_clicked = True
        elif self.is_clicked and not input.mouse.get_pressed()[0]:
            self.is_clicked = False
            if self.back_btn.collidepoint((mx, my)):
                return self.menu
            for i, r in enumerate(self.tab_rects):
                if r.collidepoint((mx, my)):
                    self.active_tab = i
                    break
            for i, r in enumerate(self.chunk_rects):
                if r.collidepoint((mx, my)):
                    self.selected_chunks = i
                    self.settings_obj.physics_chunks_beyond_screen = i
                    self._write_settings()
                    break
            for i, r in enumerate(self.size_rects):
                if r.collidepoint((mx, my)):
                    self.selected_world_size = i
                    self.settings_obj.default_world_size = self.world_size_to_value[self.world_size_options[i]]
                    self._write_settings()
                    break

        if input.escape_keypress:
            return self.menu

        self.draw(mx, my)
        return self

    def draw(self, mx=0, my=0):
        self.menu.draw_background()
        self.screen.blit(self.panel_surf, self.panel_rect.topleft)

        cx      = self.panel_rect.centerx
        inner_x = self.panel_rect.left  + self.mw * 2
        inner_r = self.panel_rect.right - self.mw * 2
        inner_w = inner_r - inner_x
        y = self.panel_rect.top + self.mh

        # title
        title_surf = self.title_font.render("SETTINGS", True, self.title_col)
        self.screen.blit(title_surf, title_surf.get_rect(centerx=cx, top=y))
        y += title_surf.get_height() + self.mh // 2

        # tab bar
        tab_labels = ["In-Game", "World Gen", "Visual"]
        tab_h = int(self.mh * 1.4)
        tab_w = inner_w // 3
        self.tab_rects = []
        for i, label in enumerate(tab_labels):
            r = pygame.Rect(inner_x + i * tab_w, int(y), tab_w, tab_h)
            self.tab_rects.append(r)
            is_active = (i == self.active_tab)
            hover     = r.collidepoint((mx, my))
            col = self.accent_bright if is_active else (205, 209, 214) if hover else (140, 145, 152)
            ts = self.tab_font.render(label, True, col)
            self.screen.blit(ts, ts.get_rect(center=r.center))
            if is_active:
                ul = pygame.Rect(int(r.left + r.width * 0.18), r.bottom + 2,
                                 int(r.width * 0.64), 3)
                pygame.draw.rect(self.screen, self.accent, ul, border_radius=2)
        y += tab_h + 10

        pygame.draw.line(self.screen, self.divider_col, (inner_x, y), (inner_r, y), 1)
        y += int(self.mh * 1.5)

        # tab content
        if self.active_tab == 0:
            self._draw_in_game_tab(mx, my, inner_x, inner_w, y)
        elif self.active_tab == 1:
            self._draw_world_gen_tab(mx, my, inner_x, inner_w, y)
        else:
            self._draw_visual_tab(cx, y)

        # return button pinned to bottom of panel
        self.back_btn.bottom = self.panel_rect.bottom - self.mh
        btn_color = self.btn_hov_col if self.back_btn.collidepoint((mx, my)) else self.btn_col
        pygame.draw.rect(self.screen, btn_color, self.back_btn)
        bs = self.btn_font.render("Return to Menu", True, (255, 255, 255))
        self.screen.blit(bs, bs.get_rect(center=self.back_btn.center))

        # footer
        pygame.draw.rect(self.screen, (30, 30, 30), self.footer_rect)
        pad = floor(self.mw * 0.6)
        fcy = self.footer_rect.centery
        ver = self.footer_font.render(self.menu.APP_DISPLAY_NAME, True, self.footer_col)
        cpy = self.footer_font.render("© Davis Larson 2026",      True, self.footer_col)
        self.screen.blit(ver, ver.get_rect(midleft=(pad, fcy)))
        self.screen.blit(cpy, cpy.get_rect(midright=(self.W - pad, fcy)))

    def _draw_in_game_tab(self, mx, my, left, w, y):
        self.screen.blit(
            self.sublabel_font.render("SIMULATION CHUNKS OFF SCREEN", True, self.sublabel_col),
            (left, int(y)))
        y += self.mh * 0.9
        btn_w = w // len(self.chunk_options)
        btn_h = int(self.mh * 2)
        self.chunk_rects = []
        for i, label in enumerate(self.chunk_options):
            bw = int(btn_w - (4 if i < len(self.chunk_options) - 1 else 0))
            r = pygame.Rect(int(left + i * btn_w), int(y), bw, btn_h)
            self.chunk_rects.append(r)
            if i == self.selected_chunks:
                pygame.draw.rect(self.screen, self.accent, r)
                pygame.draw.rect(self.screen, self.accent_bright, r, width=2)
            elif r.collidepoint((mx, my)):
                pygame.draw.rect(self.screen, self.btn_hov_col, r)
            else:
                pygame.draw.rect(self.screen, self.btn_col, r)
            ts = self.btn_font.render(label, True, (255, 255, 255))
            self.screen.blit(ts, ts.get_rect(center=r.center))

    def _draw_world_gen_tab(self, mx, my, left, w, y):
        self.screen.blit(
            self.sublabel_font.render("DEFAULT WORLD SIZE", True, self.sublabel_col),
            (left, int(y)))
        y += self.mh * 0.9
        sw = w / len(self.world_size_options)
        sh = int(self.mh * 2)
        self.size_rects = []
        for i, label in enumerate(self.world_size_options):
            bw = int(sw - (4 if i < len(self.world_size_options) - 1 else 0))
            r = pygame.Rect(int(left + i * sw), int(y), bw, sh)
            self.size_rects.append(r)
            if i == self.selected_world_size:
                pygame.draw.rect(self.screen, self.accent, r)
                pygame.draw.rect(self.screen, self.accent_bright, r, width=2)
            elif r.collidepoint((mx, my)):
                pygame.draw.rect(self.screen, self.btn_hov_col, r)
            else:
                pygame.draw.rect(self.screen, self.btn_col, r)
            ts = self.btn_font.render(label, True, (255, 255, 255))
            self.screen.blit(ts, ts.get_rect(center=r.center))

    def _draw_visual_tab(self, cx, y):
        surf = self.body_font.render("coming soon", True, self.body_col)
        self.screen.blit(surf, surf.get_rect(centerx=cx, top=y))

    def _write_settings(self):
        with open(self.settings_obj.settings_file_path, 'w') as f:
            json.dump(self.settings_obj.to_dict(), f, indent=2)

    def on_quit(self): pass
    def catch_exception(self): return self.menu
