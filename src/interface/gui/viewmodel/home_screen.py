from typing import Optional

from PySide6.QtCore import QObject, Signal

from interface.gui.model.settings import SettingsModel


class HomeScreenViewModel(QObject):
    changed_theme = Signal()
    changed_language = Signal()

    def __init__(self, model: SettingsModel, parent: Optional[QObject]) -> None:
        super().__init__(parent)
        self._model = model
        self._model.language_changed.connect(self.changed_language)
        self._model.theme_changed.connect(self.changed_theme)

    def t(self, key: str):
        return self._model.t(key)
