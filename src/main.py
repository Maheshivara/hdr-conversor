import sys

from gui.app import HDRApp
from gui.pallete.custom_pallete import create_custom_palette


def main():

    app = HDRApp(sys.argv)
    app.setPalette(create_custom_palette())
    app.home_screen.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
