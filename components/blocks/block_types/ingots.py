from components.blocks.block_types._base import Item, Ingot

class Iron_Ingot(Item):
    str_name = "Iron Ingot"

    @staticmethod
    def draw_manual(screen, x, y, block_width, being_mined=False, is_grid_coordinates=True, use_alt_drawing=False):
        iron_base_color = (185, 188, 196)
        Ingot.draw_ingot_manual(screen, x, y, block_width, iron_base_color, being_mined, is_grid_coordinates)

class Gold_Ingot(Item):
    str_name = "Gold Ingot"

    @staticmethod
    def draw_manual(screen, x, y, block_width, being_mined=False, is_grid_coordinates=True, use_alt_drawing=False):
        ingot_gold_base = (210, 205, 95)
        Ingot.draw_ingot_manual(screen, x, y, block_width, ingot_gold_base, being_mined, is_grid_coordinates)
