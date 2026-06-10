from pathlib import Path
import json

class Settings:
    def __init__(self, settings_file_directory_path):
        # general init
        self.settings_file_directory_path = settings_file_directory_path
        settings_file_name = 'global_settings.json'
        self.settings_file_path = Path(settings_file_directory_path) / Path(settings_file_name)

        self.default_settings_values_dict = {
            "in_game_settings": {
                "physics_chunks_beyond_screen": 2,
            },
            "world_gen_settings": {
                "default_world_size": 1
            },
            "visual_settings": {

            }
        }

        try:
            with open(self.settings_file_path, 'r') as settings_file:
                settings_general_dict = self.get_dict_data(settings_file)
        except: # use FileNotFoundError once code cand handle an individual bad setting exception -> that would ruin the game
            self.generate_new_settings_file()
            settings_general_dict = self.default_settings_values_dict

        in_game_settings = settings_general_dict["in_game_settings"]
        world_gen_settings = settings_general_dict["world_gen_settings"]
        visual_settings = settings_general_dict["visual_settings"]

        # set values of settings
        self.physics_chunks_beyond_screen = in_game_settings["physics_chunks_beyond_screen"]
        self.default_world_size = world_gen_settings["default_world_size"]

    def get_dict_data(self, settings_file):
        return json.load(settings_file)
    
    def to_dict(self): # the Settings_Menu class will manage this and edit the file as needed, won't be resaved on every run
        return {
            "in_game_settings": {
                "physics_chunks_beyond_screen": self.physics_chunks_beyond_screen,
            },
            "world_gen_settings": {
                "default_world_size": self.default_world_size
            },
            "visual_settings": {

            }
        }

    def generate_new_settings_file(self):
        """runs if the settings file cannot be found"""
        with open(self.settings_file_path, 'w') as file:
            json.dump(self.default_settings_values_dict, file, indent=2)

settings = None

def init(settings_file_directory_path):
    global settings
    settings = Settings(settings_file_directory_path)

def get():
    return settings
