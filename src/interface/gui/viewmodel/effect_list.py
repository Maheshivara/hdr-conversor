from typing import Any, Optional

from PySide6.QtCore import QObject, Signal

from core.models.enum.effects import EffectType
from interface.gui.model.effect_list import EffectListModel
from interface.gui.viewmodel.home_screen import HomeScreenViewModel


class EffectListViewModel(QObject):
    changed_theme = Signal()
    changed_language = Signal()
    list_updated = Signal()

    def __init__(
        self,
        home_view_model: HomeScreenViewModel,
        list_model: EffectListModel,
        parent: Optional[QObject] = None,
    ) -> None:
        super().__init__(parent)
        self._model = list_model
        self._home_view_model = home_view_model

        self._home_view_model.changed_language.connect(self.changed_language)
        self._home_view_model.changed_theme.connect(self.changed_theme)
        self._model.list_updated.connect(self.list_updated)

    def add_effect(self, type: EffectType):
        self._model.add_item(type)

    def remove_effect(self, idx: int):
        self._model.remove_item(idx)

    def update_effect_param(self, idx: int, param: str, new_value: Any):
        self._model.update_param(idx, param, new_value)

    def get_effects(self) -> set[EffectType]:
        return self._model.get_available()

    def get_current(self):
        return self._model.get_current()

    def get_effect_params(self, idx: int):
        return self._model.get_effect_params(idx)

    def t(self, key: str):
        return self._home_view_model.t(key)
