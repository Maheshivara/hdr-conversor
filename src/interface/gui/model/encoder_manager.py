from typing import Any

from core.encoders.default_encoder import DefaultEncoder
from core.encoders.encoder import Encoder


class EncoderManager:
    def __init__(self) -> None:
        self._available: dict[str, Encoder] = dict()
        self._available["default"] = DefaultEncoder()

        self._current: tuple[str, Encoder] = ("default", self._available["default"])

    def get_encoders(self) -> set[str]:
        return set(self._available.keys())

    def get_current_encoder(self) -> tuple[str, Encoder]:
        return self._current

    def set_current_encoder(self, encoder: str) -> bool:
        e = self._available.get(encoder, None)
        if e is None:
            return False
        if self._current[0] == encoder:
            return False
        self._current = (encoder, e)
        return True

    def update_current_param(self, param: str, new_value: Any) -> bool:
        inputs = self._current[1].get_inputs()
        p = inputs.get(param, None)
        if p is None:
            return False
        updated = p.update_value(new_value)
        return updated
