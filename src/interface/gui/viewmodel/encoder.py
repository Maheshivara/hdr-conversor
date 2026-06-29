from typing import Any, Optional

from PySide6.QtCore import QObject, Signal

from interface.gui.model.pipeline import PipelineModel
from shared.constants import AvailableEncoders


class EncoderViewModel(QObject):
    updated_encoder = Signal()

    def __init__(
        self,
        model: PipelineModel,
        parent: Optional[QObject] = None,
    ) -> None:
        super().__init__(parent)
        self._model = model

        self._model.encoder_updated.connect(self.updated_encoder)

    def get_current(self):
        return self._model.get_encoder()

    def get_available(self):
        return self._model.get_encoders()

    def set_current(self, new: AvailableEncoders):
        self._model.set_encoder(new)

    def update_param(self, param: str, new_value: Any):
        self._model.update_encoder_input(param, new_value)
