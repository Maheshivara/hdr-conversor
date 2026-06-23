from typing import Optional

from PySide6.QtCore import Property, QObject, Signal
from PySide6.QtGui import QPalette

from interface.gui.model.theme_manager import ThemeManager


class SettingsModel(QObject):
    theme_changed = Signal()
    language_changed = Signal()

    def __init__(self, theme: Optional[str], language: Optional[str]) -> None:
        super().__init__()
        self._theme_manager = ThemeManager(theme)
        self._theme = self._theme_manager.get_current_theme()[0]
        self._language = language or "en_US"

    @Property(str, notify=theme_changed)
    def theme(self):
        return self._theme_manager.get_current_theme()[0]

    @theme.setter
    def set_theme(self, new_theme: str):
        if self._theme != new_theme:
            changed = self._theme_manager.set_current_theme(new_theme)
            if changed:
                self._theme = new_theme
                self.theme_changed.emit()

    @Property(str, notify=language_changed)
    def language(self):
        return self._language

    @theme.setter
    def set_language(self, new_language: str):
        if self._language != new_language:
            self._language = new_language
            self.language_changed.emit()

    def get_theme_stylesheet(self) -> str:
        return self._theme_manager.get_stylesheet()

    def get_theme_palette(self) -> QPalette:
        return self._theme_manager.get_palette()

    def get_available_themes(self, lang: Optional[str]) -> list[tuple[str, str]]:
        return self._theme_manager.get_themes_options(lang)
