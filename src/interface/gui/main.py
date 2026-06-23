from os import path

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

from interface.gui.view.home import HomeScreen
from shared.constants import AppMetadata, DefaultPath


class AppGui(QApplication):
    def __init__(self, argv):
        super().__init__(argv)
        self.setApplicationName(AppMetadata.APP_NAME)
        self.setOrganizationName(AppMetadata.APP_ORGANIZATION)
        self.setApplicationVersion(AppMetadata.APP_VERSION)

        icon_path = path.join(DefaultPath.ICONS_DIR, "icon.png")
        self.setWindowIcon(QIcon(icon_path))
        self.home_screen = HomeScreen()

    def start(self):
        self.home_screen.show()
