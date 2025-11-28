from PySide6.QtGui import QPalette
from os import path
import json

PALETTE_INFO_PATH = path.join(path.dirname(path.abspath(__file__)), "info.json")


def create_custom_palette() -> QPalette:
    with open(PALETTE_INFO_PATH, "r") as f:
        palette_data = json.load(f)["palette"]

    palette = QPalette()

    for role_name, color_hex in palette_data.items():
        role = getattr(QPalette, role_name, None)
        if role is not None:
            palette.setColor(role, color_hex)
    return palette
