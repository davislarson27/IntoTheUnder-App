class World_Generation_Settings:
    def __init__(self, version, inventory_height, health_bar_height, grid_width, grid_height):
        self.version = version
        self.default_inventory_height = inventory_height
        self.default_health_bar_height = inventory_height
        self.default_grid_width = grid_width
        self.default_grid_depth = grid_height

        self.inventory_height = inventory_height
        self.health_bar_height = inventory_height
        self.grid_width = grid_width
        self.grid_depth = grid_height

    def reset_defaults(self):
        self.inventory_height = self.default_inventory_height
        self.health_bar_height = self.default_inventory_height
        self.grid_width = self.default_grid_width
        self.grid_depth = self.default_grid_height