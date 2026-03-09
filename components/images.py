from pathlib import Path
import pygame
from math import floor

class Images():
    def __init__(self, images_file_path, BLOCK_SIZE):
        # convert image_folder_path to Path object
        image_path = Path(images_file_path)

        # start converting images
        self.trash = Images.file_to_image(image_path / "trash-can-outline-2.png", floor(BLOCK_SIZE * 0.75))
        self.player_left = Images.file_to_image(image_path / "robot_left.png", 22, 40)
        self.player_right = Images.file_to_image(image_path / "robot_right.png", 22, 40)


    @staticmethod
    def file_to_image(image_path, image_size_x, image_size_y=None):
        if image_size_y is None: image_size_y = image_size_x
        return pygame.transform.smoothscale(pygame.image.load(image_path).convert_alpha(), (image_size_x, image_size_y))