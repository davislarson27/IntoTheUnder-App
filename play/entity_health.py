import pygame

class Entity_Health:
    def __init__(self, screen, max_health, cur_health, max_energy, energy, images):
        self.max_health = max_health
        self.health = cur_health

        self.max_energy = max_energy
        self.energy = energy

        self.low_energy_speed_reduction_factor = 0.5

        self.screen = screen
        self.images = images

        self.tot_columns = 24
        self.row_width = screen.get_width() // self.tot_columns

        margin = 30
        icon_width = 15
        self.health_bar_height = 50
        health_bar_width = self.row_width * 4 + int(icon_width * 1.5)
        bar_margin_y = int(self.health_bar_height / 4.4)

        self.bar_start_x = margin + health_bar_width // 6
        self.bar_full_width = health_bar_width - health_bar_width // 6 - health_bar_width // 12

        self.health_icon_x = self.bar_start_x - int(icon_width * 1.5)
        self.energy_icon_x = self.bar_start_x - int(icon_width * 1.5)


        self.bar_height = 8
        icon_offset_y = (icon_width - self.bar_height) // 2

        self.health_bar_start_y = margin + bar_margin_y
        self.energy_bar_start_y = self.health_bar_height + margin - bar_margin_y - self.bar_height

        self.main_box = pygame.rect.Rect(
            margin,
            margin,
            health_bar_width,
            self.health_bar_height
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

        self.health_icon_x = self.bar_start_x - int(icon_width * 1.5)
        self.health_icon_y = self.health_bar_start_y - icon_offset_y

        self.energy_icon_x = self.bar_start_x - int(icon_width * 1.5)
        self.energy_icon_y = self.energy_bar_start_y - icon_offset_y

        self.margin_color = (50, 50, 50)
        self.bg_color = (190, 190, 190)
        self.divider_color = (150, 150, 150)
        self.full_health_compartment_color = (185, 68, 68)
        self.full_energy_bar_color = (90, 140, 200)

        # region drawing the cross myself

        def draw_health_icon(surface, color=self.full_health_compartment_color, border_color=(135, 45, 45)):
            surf_size = 90
            border = 4
            padding = border + 10  # shift inward so caps aren't clipped
            size = surf_size - padding * 2
            third = size // 3

            x, y = padding, padding

            # Horizontal caps
            pygame.draw.rect(surface, border_color, (x - border, y + third - border, border, third + border * 2))
            pygame.draw.rect(surface, border_color, (x + size, y + third - border, border, third + border * 2))
            # Vertical caps
            pygame.draw.rect(surface, border_color, (x + third - border, y - border, third + border * 2, border))
            pygame.draw.rect(surface, border_color, (x + third - border, y + size, third + border * 2, border))
            # Cross body border
            pygame.draw.rect(surface, border_color, (x, y + third - border, size, third + border * 2))
            pygame.draw.rect(surface, border_color, (x + third - border, y, third + border * 2, size))
            # Fill
            pygame.draw.rect(surface, color, (x, y + third, size, third))
            pygame.draw.rect(surface, color, (x + third, y, third, size))

        self.health_icon_surf = pygame.Surface((90, 90), pygame.SRCALPHA)
        draw_health_icon(self.health_icon_surf)
        self.health_icon_surf = pygame.transform.smoothscale(self.health_icon_surf, (15, 15))

        # region end

    def change_health(self, change_in_health):
        """takes the change in the health and applies it"""
        self.health += change_in_health
        self.health = min(self.health, self.max_health)

    def change_energy(self, change_in_energy):
        """takes the change in the energy and applies it"""
        self.energy += change_in_energy
        self.energy = min(self.energy, self.max_energy)

    def is_alive(self):
        if self.health <= 0:
            return False
        elif self.energy <= 0:
            return False
        return True
    
    def reset_health(self):
        self.health = self.max_health

    def reset_energy(self):
        self.energy = self.max_energy

    def get_low_energy_speed_reduction_factor(self):
        energy_percent = self.energy / self.max_energy
        if energy_percent > 0.05:
            return 1
        elif energy_percent > 0.01:
            return self.low_energy_speed_reduction_factor
        else:
            return self.low_energy_speed_reduction_factor / 2

    def get_health(self):
        return self.health

    def get_energy(self):
        return self.energy
    
    def get_health_bar_height(self):
        return self.health_bar_height + self.health_bar_start_y

    def draw(self):

        # calculate percentages
        health_percent = max(min(self.health / self.max_health, 1), 0)
        energy_percent = max(min(self.energy / self.max_energy, 1), 0)

        pygame.draw.rect( # draw bg
            self.screen,
            self.bg_color,
            self.main_box
        )

        # health bar
        self.screen.blit(self.health_icon_surf, (self.health_icon_x, self.health_icon_y))
        pygame.draw.rect(
            self.screen,
            self.divider_color,
            self.health_bar_outline
        )
        pygame.draw.rect(
            self.screen,
            self.full_health_compartment_color,
            (
                self.bar_start_x,
                self.health_bar_start_y,
                int(self.bar_full_width * health_percent),
                self.bar_height
            )
        )

        # draw energy bar
        self.screen.blit(self.images.energy_icon, (self.energy_icon_x, self.energy_icon_y))
        pygame.draw.rect( 
            self.screen,
            self.divider_color,
            self.energy_bar_outline
        )
        pygame.draw.rect(
            self.screen,
            self.full_energy_bar_color,
            (
                self.bar_start_x,
                self.energy_bar_start_y,
                int(self.bar_full_width * energy_percent),
                self.bar_height
            )
        )
