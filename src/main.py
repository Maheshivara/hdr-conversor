import sys

from interface.gui.app import AppGui


def main():
    app = AppGui(sys.argv)
    app.start()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
