from PySide6.QtGui import QFont, QFontDatabase
from os import path

from core.constants import Paths

FONT_PATH = path.join(Paths.ASSETS_DIR, "fonts", "Flexi_IBM_VGA_True.ttf")


def load_font() -> QFont:
    font_id = QFontDatabase.addApplicationFont(FONT_PATH)
    font_families = QFontDatabase.applicationFontFamilies(font_id)
    if font_families:
        font_family = font_families[0]
        return QFont(font_family)
    else:
        raise RuntimeError(f"Failed to load font from {FONT_PATH}")
