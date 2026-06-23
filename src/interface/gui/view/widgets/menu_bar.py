from typing import Optional

from PySide6.QtGui import QActionGroup
from PySide6.QtWidgets import QMainWindow, QMenuBar

from interface.gui.viewmodel.menu_bar import MenuBarViewModel


class MenuBar(QMenuBar):
    def __init__(
        self,
        view_model: MenuBarViewModel,
        parent: Optional[QMainWindow] = None,
    ):
        super().__init__(parent)
        self._view_model = view_model

        self._view_model.changed_language.connect(self._retranslate)
        self._view_model.changed_theme.connect(self._retranslate)

        self._build()

    def _build(self):
        self.settings_menu = self.addMenu(self._view_model.t("ui.menu.settings"))

        self.language_section = self.settings_menu.addMenu(
            self._view_model.t("ui.menu.language")
        )
        self._build_languages_group()

        self.theme_section = self.settings_menu.addMenu(
            self._view_model.t("ui.menu.theme")
        )
        self._build_themes_group()

    def _build_themes_group(self):
        self.theme_section.clear()
        self.theme_group = QActionGroup(self)
        self.theme_group.setExclusive(True)

        self.available_themes = self._view_model.get_themes()
        self.current_theme = self._view_model.get_theme()

        for key, name in self.available_themes:
            action = self.theme_group.addAction(name)
            action.setCheckable(True)
            if key == self.current_theme:
                action.setChecked(True)
            action.triggered.connect(
                lambda checked, k=key: self._view_model.set_theme(k)
            )
            self.theme_section.addAction(action)

    def _build_languages_group(self):
        self.language_section.clear()
        self.language_group = QActionGroup(self)
        self.language_group.setExclusive(True)

        self.available_languages = self._view_model.get_languages()
        self.current_language = self._view_model.get_language()

        for code, name in self.available_languages:
            action = self.language_group.addAction(name)
            action.setCheckable(True)
            if code == self.current_language:
                action.setChecked(True)
            action.triggered.connect(
                lambda checked, c=code: self._view_model.set_language(c)
            )
            self.language_section.addAction(action)

    def _retranslate(self):
        self.settings_menu.setTitle(self._view_model.t("ui.menu.settings"))
        self.language_section.setTitle(self._view_model.t("ui.menu.language"))
        self.theme_section.setTitle(self._view_model.t("ui.menu.theme"))

        self._build_languages_group()
        self._build_themes_group()
