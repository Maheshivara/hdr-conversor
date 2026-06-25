from typing import Any, Optional

from PySide6.QtCore import QObject, Signal

from interface.gui.model.encoder import EncoderModel
from interface.gui.viewmodel.effect_list import EffectListViewModel
from interface.gui.viewmodel.home_screen import HomeScreenViewModel


class EncoderViewModel(QObject):
    changed_theme = Signal()
    changed_language = Signal()
    changed_encoder = Signal()

    def __init__(
        self,
        home_view_model: HomeScreenViewModel,
        effects_view_model: EffectListViewModel,
        model: EncoderModel,
        parent: Optional[QObject] = None,
    ) -> None:
        super().__init__(parent)
        self._model = model
        self._home_view_model = home_view_model
        self._effects_view_model = effects_view_model

        self._home_view_model.changed_language.connect(self.changed_language)
        self._home_view_model.changed_theme.connect(self.changed_theme)
        self._model.changed_encoder.connect(self.changed_encoder)

    def get_current(self):
        return self._model.get_current()

    def get_available(self):
        return self._model.get_available()

    def set_current(self, new: str):
        self._model.set_current(new)

    def update_param(self, param: str, new_value: Any):
        self._model.update_param(param, new_value)

    def t(self, key: str):
        return self._home_view_model.t(key)
