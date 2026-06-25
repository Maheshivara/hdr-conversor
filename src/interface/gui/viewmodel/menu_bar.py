from typing import Optional

from PySide6.QtCore import QObject, Signal

from interface.gui.model.settings import SettingsModel


class MenuBarViewModel(QObject):
    changed_theme = Signal()
    changed_language = Signal()

    def __init__(self, model: SettingsModel, parent: Optional[QObject] = None) -> None:
        super().__init__(parent)
        self._model = model
        self._model.language_changed.connect(self.changed_language)
        self._model.theme_changed.connect(self.changed_theme)

    def set_theme(self, new_theme: str):
        self._model.set_current_theme(new_theme)

    def get_theme(self):
        return self._model.get_current_theme()[0]

    def get_themes(self):
        return self._model.get_available_themes()

    def set_language(self, new_lang: str):
        self._model.set_current_language(new_lang)

    def get_language(self):
        return self._model.get_current_language()[0]

    def get_languages(self):
        return self._model.get_available_languages()

    def t(self, key: str):
        return self._model.t(key)
