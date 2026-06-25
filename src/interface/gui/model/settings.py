from typing import Callable, Optional

from PySide6.QtCore import QObject, Signal
from PySide6.QtGui import QPalette

from interface.gui.model.language_manager import LanguageManager
from interface.gui.model.theme import Theme
from interface.gui.model.theme_manager import ThemeManager


class SettingsModel(QObject):
    theme_changed = Signal()
    language_changed = Signal()

    def __init__(
        self,
        on_theme_changed: Callable[[], None],
        theme: Optional[str] = None,
        language: Optional[str] = None,
    ) -> None:
        super().__init__()
        self.on_theme_changed = on_theme_changed
        self._language_manager = LanguageManager(language)
        self._current_language = self._language_manager.get_current_language()

        self._theme_manager = ThemeManager(theme)
        self._current_theme = self._theme_manager.get_current_theme()

    def set_current_theme(self, new_theme: str):
        if self._current_theme[0] != new_theme:
            changed = self._theme_manager.set_current_theme(new_theme)
            if changed:
                self._current_theme = self._theme_manager.get_current_theme()
                self.on_theme_changed()
                self.theme_changed.emit()

    def set_current_language(self, new_language: str):
        if self._current_language[0] == new_language:
            return
        changed = self._language_manager.set_current_language(new_language)
        if changed:
            self._current_language = self._language_manager.get_current_language()
            self.language_changed.emit()

    def get_current_theme(self) -> tuple[str, Theme]:
        return self._current_theme

    def get_theme_stylesheet(self) -> str:
        return self._theme_manager.get_stylesheet()

    def get_theme_palette(self) -> QPalette:
        return self._theme_manager.get_palette()

    def get_available_themes(self) -> list[tuple[str, str]]:
        themes_keys = self._theme_manager.get_themes_options()
        available: list[tuple[str, str]] = []
        for key in themes_keys:
            name = self._language_manager.t(f"themes.{key}")
            available.append((key, name))

        return available

    def get_available_languages(self) -> list[tuple[str, str]]:
        return self._language_manager.get_available_languages()

    def get_current_language(self) -> tuple[str, str]:
        return self._current_language

    def t(self, key: str) -> str:
        return self._language_manager.t(key)
