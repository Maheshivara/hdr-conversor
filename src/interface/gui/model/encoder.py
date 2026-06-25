from typing import Any

from PySide6.QtCore import QObject, Signal

from core.encoders.encoder import Encoder
from interface.gui.model.encoder_manager import EncoderManager


class EncoderModel(QObject):
    changed_encoder = Signal()

    def __init__(self) -> None:
        super().__init__()
        self._manager = EncoderManager()

    def get_current(self) -> tuple[str, Encoder]:
        return self._manager.get_current_encoder()

    def set_current(self, new_enc: str):
        changed = self._manager.set_current_encoder(new_enc)
        if changed:
            self.changed_encoder.emit()

    def get_available(self) -> set[str]:
        return self._manager.get_encoders()

    def update_param(self, param: str, new_value: Any):
        self._manager.update_current_param(param, new_value)
