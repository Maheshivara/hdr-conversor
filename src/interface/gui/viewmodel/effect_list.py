from typing import Any, Optional

from PySide6.QtCore import QObject, Signal

from interface.gui.model.pipeline import PipelineModel
from shared.constants import AvailableEffect


class EffectListViewModel(QObject):
    list_updated = Signal()
    update_error = Signal(str)

    def __init__(
        self,
        model: PipelineModel,
        parent: Optional[QObject] = None,
    ) -> None:
        super().__init__(parent)
        self._model = model

        self._model.effects_updated.connect(self.list_updated)
        self._model.effect_update_error.connect(self.update_error)

    def add_effect(self, type: AvailableEffect):
        self._model.add_effect(type)

    def remove_effect(self, idx: int):
        self._model.remove_effect(idx)

    def update_effect_param(self, idx: int, param: str, new_value: Any):
        self._model.update_effect_input(idx, param, new_value)

    def get_effects(self):
        return self._model.get_available_effects()

    def get_current(self):
        return self._model.get_effects()
