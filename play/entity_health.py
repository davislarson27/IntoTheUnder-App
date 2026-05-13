import pygame

class Entity_Health:
    def __init__(self, screen, max_health, cur_health):
        self.max_health = max_health
        self.health = 80

        self.screen = screen

        self.tot_columns = 24
        self.row_width = screen.get_width() // self.tot_columns

        margin = 30
        health_bar_height = 50
        health_bar_width = self.row_width * 4
        bar_margin_y = int(health_bar_height / 4.4)
        
        self.bar_start_x = margin + health_bar_width // 8
        self.bar_full_width = 6 * health_bar_width // 8
        self.bar_height = 8

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
            margin + bar_margin_y,
            self.bar_full_width,
            self.bar_height
        )
        self.energy_bar_outline = pygame.rect.Rect(
            self.bar_start_x,
            self.energy_bar_start_y,
            self.bar_full_width,
            self.bar_height
        )


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
