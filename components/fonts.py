from pathlib import Path

class Fonts():
    def __init__(self, font_file_path):
        # convert font_folder_path to Path object
        font_path = Path(font_file_path)

        # start converting fonts
        self.PixeloidMono = font_path / Path('Pixeloid') / Path('PixeloidMono.ttf')
        self.PixeloidSans = font_path / Path('Pixeloid') / Path('PixeloidSans.ttf')
        self.PixeloidSans_Bold = font_path / Path('Pixeloid') / Path('PixeloidSans-Bold.ttf')
    