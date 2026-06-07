import pygame
from math import floor
import components.fonts as font_manager


class Credits:
    def __init__(self, screen, menu):
        self.screen = screen
        self.menu = menu
        self.is_clicked = False

        # colors
        self.title_col   = (255, 255, 255)
        self.heading_col = (150, 170, 200)
        self.body_col    = (225, 225, 228)
        self.muted_col   = (150, 155, 162)
        self.divider_col = (90, 95, 105)
        self.btn_col     = (140, 140, 140)
        self.btn_hov_col = (165, 165, 165)
        self.footer_col  = (200, 200, 200)
        self.panel_color = (16, 17, 22)

        # grid
        self.W  = screen.get_width()
        self.H  = screen.get_height()
        self.mw = self.W // 28
        self.mh = self.H // 28

        # fonts
        _f = font_manager.get()
        self.title_font   = pygame.font.Font(str(_f.PixeloidSans_Bold), 32)
        self.heading_font = pygame.font.Font(str(_f.PixeloidSans_Bold), 12)
        self.name_font    = pygame.font.Font(str(_f.PixeloidSans),      18)
        self.body_font    = pygame.font.Font(str(_f.PixeloidSans),      14)
        self.btn_font     = pygame.font.Font(str(_f.PixeloidSans),      18)

        # footer
        self.footer_h    = max(34, floor(self.mh * 1.0))
        self.footer_rect = pygame.Rect(0, self.H - self.footer_h, self.W, self.footer_h)
        self.footer_font = pygame.font.Font(str(_f.PixeloidSans), 11)

        # content panel (behind everything, leaves margins + clears the footer)
        side = self.mw * 3
        self.panel_rect = pygame.Rect(side, self.mh, self.W - side * 2,
                                      self.H - self.footer_h - self.mh * 2)
        self.panel_surf = pygame.Surface(self.panel_rect.size)
        self.panel_surf.fill(self.panel_color)

        # thank-you message (wrapped to panel width)
        message = ("Thank you for playing Into the Under! I always wanted to learn "
                   "to make a game, and the fact that you are here reading this right "
                   "now means I have succeeded! Thank you for helping my dreams "
                   "become reality!")
        self.message_lines = self._wrap(message, self.body_font, self.panel_rect.width - self.mw * 4)

        # back button
        btn_w = self.mw * 7
        btn_h = floor(self.mh * 1.8)
        self.back_btn = pygame.Rect((self.W - btn_w) // 2, 0, btn_w, btn_h)  # y set in draw

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

        if input.escape_keypress:
            return self.menu

        self.draw(mx, my)
        return self

    def draw(self, mx=0, my=0):
        self.menu.draw_background()

        # dark panel behind content
        self.screen.blit(self.panel_surf, self.panel_rect.topleft)

        cx = self.panel_rect.centerx
        inner_x = self.panel_rect.left + self.mw * 2
        inner_r = self.panel_rect.right - self.mw * 2
        y = self.panel_rect.top + self.mh

        # ── CREDITS title ──────────────────────────────────────────────── #
        title_surf = self.title_font.render("CREDITS", True, self.title_col)
        self.screen.blit(title_surf, title_surf.get_rect(centerx=cx, top=y))
        y += title_surf.get_height() + self.mh // 2

        # divider under heading
        pygame.draw.line(self.screen, self.divider_col, (inner_x, y), (inner_r, y), 1)
        y += self.mh

        # ── GAME BY ────────────────────────────────────────────────────── #
        y = self._section_label("GAME BY", cx, y)
        name_surf = self.name_font.render("Davis Larson", True, self.body_col)
        self.screen.blit(name_surf, name_surf.get_rect(centerx=cx, top=y))
        y += name_surf.get_height() + self.mh

        # ── THANK YOU ──────────────────────────────────────────────────── #
        y = self._section_label("THANK YOU", cx, y)
        for line in self.message_lines:
            ls = self.body_font.render(line, True, self.body_col)
            self.screen.blit(ls, ls.get_rect(centerx=cx, top=y))
            y += ls.get_height() + 3
        y += self.mh

        # ── TOOLS & TECHNOLOGIES ───────────────────────────────────────── #
        y += self.mh // 2
        y = self._section_label("TOOLS & TECHNOLOGIES", cx, y, divider=True,
                                inner_x=inner_x, inner_r=inner_r)
        y += self.mh // 2

        ce_logo = self.menu.images.pygame_ce_logo
        py_logo = self.menu.images.python_logo
        logo_h  = max(ce_logo.get_height(), py_logo.get_height())
        half_gap = self.mw * 2
        ce_cx = cx - half_gap - ce_logo.get_width() // 2
        py_cx = cx + half_gap + py_logo.get_width() // 2

        self.screen.blit(ce_logo, ce_logo.get_rect(centerx=ce_cx, top=y))
        self.screen.blit(py_logo, py_logo.get_rect(centerx=py_cx, top=y))
        y = y + logo_h + self.mh

        # ── back button (pinned near the bottom of the panel) ──────────── #
        self.back_btn.bottom = self.panel_rect.bottom - self.mh
        btn_color = self.btn_hov_col if self.back_btn.collidepoint((mx, my)) else self.btn_col
        pygame.draw.rect(self.screen, btn_color, self.back_btn)
        bs = self.btn_font.render("Return to Menu", True, (255, 255, 255))
        self.screen.blit(bs, bs.get_rect(center=self.back_btn.center))

        # ── footer ─────────────────────────────────────────────────────── #
        pygame.draw.rect(self.screen, (30, 30, 30), self.footer_rect)
        pad = floor(self.mw * 0.6)
        fcy = self.footer_rect.centery
        ver  = self.footer_font.render(self.menu.APP_DISPLAY_NAME, True, self.footer_col)
        cpy  = self.footer_font.render("© Davis Larson 2026",      True, self.footer_col)
        self.screen.blit(ver, ver.get_rect(midleft=(pad, fcy)))
        self.screen.blit(cpy, cpy.get_rect(midright=(self.W - pad, fcy)))

    # ── helpers ─────────────────────────────────────────────────────────── #

    def _section_label(self, text, cx, y, divider=False, inner_x=0, inner_r=0):
        surf = self.heading_font.render(text, True, self.heading_col)
        rect = surf.get_rect(centerx=cx, top=y)
        if divider:
            gap = rect.width // 2 + self.mw
            line_y = rect.centery
            pygame.draw.line(self.screen, self.divider_col, (inner_x, line_y), (cx - gap, line_y), 1)
            pygame.draw.line(self.screen, self.divider_col, (cx + gap, line_y), (inner_r, line_y), 1)
        self.screen.blit(surf, rect)
        return y + surf.get_height() + self.mh // 3

    def _wrap(self, text, font, max_w):
        words = text.split()
        lines, cur = [], ""
        for word in words:
            test = word if not cur else cur + " " + word
            if font.size(test)[0] <= max_w:
                cur = test
            else:
                if cur:
                    lines.append(cur)
                cur = word
        if cur:
            lines.append(cur)
        return lines

    # ── main loop interface ─────────────────────────────────────────────── #

    def on_quit(self):
        pass

    def catch_exception(self):
        return self.menu
