import pygame

class Star_Background:
    def __init__(self, screen):
        self.screen = screen
        self.star_bg_surf = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)

        self.sm_px = 2

        self.star_color_bright = (250, 250, 250)
        self.star_color_cool = (220, 225, 235)
        self.star_color_warm = (235, 230, 215)
        self.star_color_dim = (180, 185, 195)

        self.generate_stars()

    def get_star_sm(self, color):
        star_surf = pygame.Surface((self.sm_px, self.sm_px), pygame.SRCALPHA)
        pygame.draw.rect(
            star_surf,
            color,
            (
                0,
                0,
                self.sm_px,
                self.sm_px
            )
        )
        return star_surf
    
    def generate_stars(self):
        width = self.screen.get_width()
        height = self.screen.get_height()

        self.star_bg_surf.blit(self.get_star_sm(self.star_color_bright), (width//8, height//7))
    
    def draw(self, camera_x, camera_y):
        self.screen.blit(self.star_bg_surf, (0,0))
