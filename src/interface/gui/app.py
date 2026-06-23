from os import path

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QMainWindow

from interface.gui.model.settings import SettingsModel
from interface.gui.view.screens.home import HomeScreen
from interface.gui.view.widgets.menu_bar import MenuBar
from interface.gui.viewmodel.home_screen import HomeScreenViewModel
from interface.gui.viewmodel.menu_bar import MenuBarViewModel
from shared.constants import AppMetadata, DefaultPath


class MainWindow(QMainWindow):
    def __init__(self, settings: SettingsModel):
        super().__init__()
        self.settings = settings

        self.setWindowTitle(AppMetadata.APP_NAME)
        icon_path = path.join(DefaultPath.ICONS_DIR, "icon.png")
        self.setWindowIcon(QIcon(icon_path))

        home_screen_view_model = HomeScreenViewModel(self.settings, None)
        self.home_screen = HomeScreen(home_screen_view_model)
        self.setCentralWidget(self.home_screen)

        menu_bar_view_model = MenuBarViewModel(self.settings, None)
        self.menu_bar = MenuBar(menu_bar_view_model, self)
        self.setMenuBar(self.menu_bar)

        self.resize(1000, 800)


class AppGui(QApplication):
    def __init__(self, argv):
        super().__init__(argv)
        self.setApplicationName(AppMetadata.APP_NAME)
        self.setOrganizationName(AppMetadata.APP_ORGANIZATION)
        self.setApplicationVersion(AppMetadata.APP_VERSION)

        self.settings = SettingsModel(self._update_theme, "default", "en_US")

        self.main_window = MainWindow(self.settings)

    def _update_theme(self):
        self.setPalette(self.settings.get_theme_palette())
        self.setStyleSheet(self.settings.get_theme_stylesheet())

    def start(self):
        self.main_window.show()
