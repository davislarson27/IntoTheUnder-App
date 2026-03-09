from components.blocks.block_types._base import PowderPile, Item

class Saltpeter_Powder(Item):
    str_name = "Saltpeter Powder"

    @staticmethod
    def draw_manual(screen, x, y, block_width, being_mined=False, is_grid_coordinates=True, use_alt_drawing=False):
        powder_color = (
            205, 
            205, 
            195
        )

        PowderPile.draw_manual(screen, x, y, block_width, powder_color, being_mined, is_grid_coordinates, use_alt_drawing)

class Sulfur_Powder(Item):

    str_name = "Sulfur Powder"

    @staticmethod
    def draw_manual(screen, x, y, block_width, being_mined=False, is_grid_coordinates=True, use_alt_drawing=False):
        powder_color = (
            160,
            170,
            60
        )

        PowderPile.draw_manual(screen, x, y, block_width, powder_color, being_mined, is_grid_coordinates, use_alt_drawing)

class Gunpowder(Item):
    str_name = "Gunpowder"

    @staticmethod
    def draw_manual(screen, x, y, block_width, being_mined=False, is_grid_coordinates=True, use_alt_drawing=False):
        powder_color = (
            88,
            86,
            88
        )

        PowderPile.draw_manual(screen, x, y, block_width, powder_color, being_mined, is_grid_coordinates, use_alt_drawing)

