import sys

from gui.app import HDRApp
from gui.pallete.custom_pallete import create_custom_palette
from gui.fonts.load_font import load_font


def main():
    app = HDRApp(sys.argv)
    font = load_font()
    app.setFont(font)
    app.setPalette(create_custom_palette())
    app.home_screen.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
