from pathlib import Path
import pygame
from math import floor

from windows_path_resources import *


class Images():
    def __init__(self, images_file_path, BLOCK_SIZE):
        # convert image_folder_path to Path object
        image_path = Path(images_file_path)

        # start converting images
        self.trash = Images.file_to_image(image_path / "trash-can-outline-2.png", floor(BLOCK_SIZE * 0.75))


    @staticmethod
    def file_to_image(image_path, BLOCK_SIZE):
        return pygame.transform.smoothscale(pygame.image.load(resource_path(image_path)).convert_alpha(), (BLOCK_SIZE, BLOCK_SIZE))