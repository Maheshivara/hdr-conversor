from typing import Any

from core.encoders.default_encoder import DefaultEncoder
from core.encoders.encoder import Encoder
from core.models.input import ColorInput, FloatInput, IntegerInput, TextInput
from shared.constants import AvailableEncoders, AvailableInput


class EncoderDTO:
    def __init__(
        self, type: AvailableEncoders, inputs: dict[str, tuple[AvailableInput, Any]]
    ) -> None:
        self.type = type
        self.inputs = inputs

    @staticmethod
    def from_encoder(encoder: Encoder) -> "EncoderDTO|None":
        t = None

        if isinstance(encoder, DefaultEncoder):
            t = AvailableEncoders.RGBM

        if t is None:
            return None

        inputs = encoder.get_inputs()

        ipt: dict[str, tuple[AvailableInput, Any]] = dict()

        for k, i in inputs.items():
            value = i.get_value()
            if isinstance(i, IntegerInput):
                ipt[k] = (AvailableInput.INT, value)
                continue

            if isinstance(i, FloatInput):
                ipt[k] = (AvailableInput.FLOAT, value)
                continue

            if isinstance(i, TextInput):
                ipt[k] = (AvailableInput.TEXT, value)
                continue

            if isinstance(i, ColorInput):
                ipt[k] = (AvailableInput.COLOR, value)
                continue

            return None

        return EncoderDTO(t, ipt)
