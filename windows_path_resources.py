import os, sys
from pathlib import Path


def resource_path(relative_path: str) -> str:
    # When bundled by PyInstaller, files are unpacked to a temp folder: sys._MEIPASS
    base_path = getattr(sys, "_MEIPASS", os.path.abspath("."))
    return os.path.join(base_path, relative_path)
