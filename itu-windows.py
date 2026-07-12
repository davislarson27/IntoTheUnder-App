from game_loop import main_game_loop
from components.path_resources.windows_path_resources import resource_path, user_data_dir

if __name__ == '__main__':
    main_game_loop(resource_path, user_data_dir)