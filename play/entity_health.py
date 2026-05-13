import pygame

class Entity_Health:
    def __init__(self, screen, max_health, cur_health, images):
        self.max_health = max_health
        self.health = 80

        self.screen = screen
        self.images = images

        self.tot_columns = 24
        self.row_width = screen.get_width() // self.tot_columns

        margin = 30
        icon_width = 15
        health_bar_height = 50
        health_bar_width = self.row_width * 4 + int(icon_width * 1.5)
        bar_margin_y = int(health_bar_height / 4.4)

        self.bar_start_x = margin + health_bar_width // 8 + icon_width
        self.bar_full_width = 6 * health_bar_width // 8
        self.bar_height = 8
        icon_offset_y = (icon_width - self.bar_height) // 2

        self.health_bar_start_y = margin + bar_margin_y
        self.energy_bar_start_y = health_bar_height + margin - bar_margin_y - self.bar_height

        self.main_box = pygame.rect.Rect(
            margin,
            margin,
            health_bar_width,
            health_bar_height
        )

        self.health_bar_outline = pygame.rect.Rect(
            self.bar_start_x,
            self.health_bar_start_y,
            self.bar_full_width,
            self.bar_height
        )
        self.energy_bar_outline = pygame.rect.Rect(
            self.bar_start_x,
            self.energy_bar_start_y,
            self.bar_full_width,
            self.bar_height
        )

        # bar side icons
        self.health_icon_rect = (
            self.bar_start_x - int(2 * icon_width),
            self.health_bar_start_y - icon_offset_y,
            icon_width,
            icon_width
        )
        self.health_icon_x = self.bar_start_x - int(2 * icon_width)
        self.health_icon_y = self.health_bar_start_y - icon_offset_y
        self.energy_icon_rect = (
            self.bar_start_x - int(2 * icon_width),
            self.energy_bar_start_y - icon_offset_y,
            icon_width,
            icon_width
        )
        self.energy_icon_x = self.bar_start_x - int(2 * icon_width)
        self.energy_icon_y = self.energy_bar_start_y - icon_offset_y

        # bar side icon surfaces
        # self.health_icon_surf = pygame.Surface((icon_width, icon_width), pygame.SRCALPHA)


        self.margin_color = (50, 50, 50)
        self.bg_color = (190, 190, 190)
        self.divider_color = (150, 150, 150)
        self.full_health_compartment_color = (150, 80, 80)
        self.full_energy_bar_color = (90, 140, 200)

    def get_health(self):
        return self.health

    def draw(self):

        # calculate percentages
        health_percent = min(self.health / self.max_health, 1)
        energy_percent = min(0.6, 1)

        pygame.draw.rect( # draw bg
            self.screen,
            self.bg_color,
            self.main_box
        )

        # pygame.draw.rect( # health bar icon
        #     self.screen,
        #     self.full_health_compartment_color,
        #     self.health_icon_rect
        # )
        self.screen.blit(self.images.health_icon, (self.health_icon_x, self.health_icon_y))
        pygame.draw.rect( # draw health bar outline
            self.screen,
            self.divider_color,
            self.health_bar_outline
        )
        pygame.draw.rect( # draw health bar outline
            self.screen,
            self.full_health_compartment_color,
            (
                self.bar_start_x,
                self.health_bar_start_y,
                int(self.bar_full_width * health_percent),
                self.bar_height
            )
        )

        # pygame.draw.rect( # energy bar icon
        #     self.screen,
        #     self.full_energy_bar_color,
        #     self.energy_icon_rect
        # )
        self.screen.blit(self.images.energy_icon, (self.energy_icon_x, self.energy_icon_y))
        pygame.draw.rect( # draw energy bar outline
            self.screen,
            self.divider_color,
            self.energy_bar_outline
        )
        pygame.draw.rect( # draw energy bar outline
            self.screen,
            self.full_energy_bar_color,
            (
                self.bar_start_x,
                self.energy_bar_start_y,
                int(self.bar_full_width * energy_percent),
                self.bar_height
            )
        )
