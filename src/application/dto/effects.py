from typing import Any

from core.filters.image_filter import ImageFilter
from core.models.enum.effects import EffectType
from core.models.input import ColorInput, FloatInput, IntegerInput, TextInput
from shared.constants import AvailableEffect, AvailableInput


class EffectDTO:
    def __init__(
        self, type: AvailableEffect, inputs: dict[str, tuple[AvailableInput, Any]]
    ) -> None:
        self.type = type
        self.inputs = inputs

    @staticmethod
    def from_filter(effect: ImageFilter) -> "EffectDTO|None":
        e = None
        t = effect.get_type()

        match t:
            case EffectType.BLACK_LEVEL:
                e = AvailableEffect.BLACK_LEVEL
            case EffectType.EXPOSURE:
                e = AvailableEffect.EXPOSURE
            case EffectType.GAMMA:
                e = AvailableEffect.GAMMA
            case EffectType.SATURATION:
                e = AvailableEffect.SATURATION

        if e is None:
            return None

        params = effect.get_params()
        inputs: dict[str, tuple[AvailableInput, Any]] = dict()

        for p, i in params.items():
            value = i.get_value()

            if isinstance(i, IntegerInput):
                inputs[p] = (AvailableInput.INT, value)
                continue

            if isinstance(i, FloatInput):
                inputs[p] = (AvailableInput.FLOAT, value)
                continue

            if isinstance(i, TextInput):
                inputs[p] = (AvailableInput.TEXT, value)
                continue

            if isinstance(i, ColorInput):
                inputs[p] = (AvailableInput.COLOR, value)
                continue

            return None

        dto = EffectDTO(e, inputs)

        return dto
