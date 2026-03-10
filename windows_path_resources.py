import os, sys
from pathlib import Path


def resource_path(relative_path: str) -> str:
    # When bundled by PyInstaller, files are unpacked to a temp folder: sys._MEIPASS
    base_path = getattr(sys, "_MEIPASS", os.path.abspath("."))
    return os.path.join(base_path, relative_path)

def user_data_dir(app_name="Into The Under"):
    base = os.path.expanduser("~\\AppData\\Roaming")
    path = os.path.join(base, app_name)
    os.makedirs(path, exist_ok=True)
    return path

