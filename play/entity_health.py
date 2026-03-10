import pygame

class Entity_Health:
    def __init__(self, screen, max_health, cur_health, INVENTORY_HEIGHT, HEALTH_BAR_HEIGHT):
        self.max_health = max_health
        self.health = cur_health

        self.screen = screen
        self.INVENTORY_HEIGHT = INVENTORY_HEIGHT
        self.HEALTH_BAR_HEIGHT = HEALTH_BAR_HEIGHT

        self.tot_columns = 24
        self.row_width = screen.get_width() // self.tot_columns
        self.margin_x = 3 * self.row_width
        self.health_bar_width = screen.get_width() - (2 * self.margin_x)
        self.health_bar_start_depth = screen.get_height() - INVENTORY_HEIGHT

        self.health_compartments = 10
        self.health_compartment_width = self.health_bar_width // self.health_compartments


        self.health_width = (self.health / self.max_health) * self.health_bar_width


        self.health_bar_outline_dimentions = (
            self.margin_x,
            self.health_bar_start_depth,
            self.health_bar_width,
            HEALTH_BAR_HEIGHT
        )

        self.margin_left_dimentions = (
            0,
            self.health_bar_start_depth,
            self.margin_x,
            HEALTH_BAR_HEIGHT
        )
        self.margin_right_dimentions = (
            screen.get_width() - self.margin_x,
            self.health_bar_start_depth,
            self.margin_x,
            HEALTH_BAR_HEIGHT
        )


        self.margin_color = (50, 50, 50)
        self.empty_health_bar_color = (200, 200, 200)
        self.divider_color = (150, 150, 150)
        self.full_health_compartment_color = (150, 80, 80)

    def get_health(self):
        return self.health

    def draw(self):
        # draw margins
        pygame.draw.rect(
            self.screen,
            self.margin_color,
            self.margin_left_dimentions
        )
        pygame.draw.rect(
            self.screen,
            self.margin_color,
            self.margin_right_dimentions
        )


        # draw health bar
        # health_bars = self.cur_health //  self.health_compartments

        # if health_bars > position:
        #     use_color = self.full_health_compartment_color
        # else:
        #     use_color = self.empty_health_bar_color

        has_health_dimentions = (
            self.margin_x,
            self.health_bar_start_depth,
            self.health_width,
            self.HEALTH_BAR_HEIGHT
        )

        pygame.draw.rect(
            self.screen,
            self.full_health_compartment_color,
            has_health_dimentions
        )

        empty_health_dimentions = (
            self.margin_x + self.health_width,
            self.health_bar_start_depth,
            self.health_bar_width - self.health_width,
            self.HEALTH_BAR_HEIGHT
        )
        pygame.draw.rect(
            self.screen,
            self.empty_health_bar_color,
            empty_health_dimentions
        )




        for position in range(1, self.health_compartments):
            divider_dimentions = (
                self.margin_x + (self.health_compartment_width * position),
                self.health_bar_start_depth,
                1,
                self.HEALTH_BAR_HEIGHT
            )
            pygame.draw.rect(
                self.screen,
                self.divider_color,
                divider_dimentions
            )


        pygame.draw.rect(
            self.screen,
            self.divider_color,
            self.health_bar_outline_dimentions,
            1
        )