from typing import Any

from PySide6.QtCore import QObject, Signal

from core.models.enum.effects import EffectType
from core.models.input import Input
from interface.gui.model.effect_list_manager import EffectListManager


class EffectListModel(QObject):
    list_updated = Signal()
    _list_manager = EffectListManager()

    def __init__(self) -> None:
        super().__init__()

    def remove_item(self, idx: int):
        result = self._list_manager.remove_effect(idx)
        if result:
            self.list_updated.emit()

    def add_item(self, type: EffectType):
        result = self._list_manager.add_effect(type)
        if result:
            self.list_updated.emit()

    def get_available(self) -> set[EffectType]:
        return self._list_manager.get_available()

    def update_param(self, idx: int, param: str, new_value: Any) -> bool:
        return self._list_manager.update_effect_param(idx, param, new_value)

    def get_effect_params(self, idx: int) -> dict[str, Input]:
        return self._list_manager.get_effect_params(idx)

    def get_current(self):
        return self._list_manager.current_effects()

    def clear(self):
        self._list_manager.clear()
        self.list_updated.emit()
