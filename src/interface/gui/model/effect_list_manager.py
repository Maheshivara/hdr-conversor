from typing import Any

from core.filters.default_filter import DefaultFilter
from core.filters.image_filter import ImageFilter
from core.models.enum.effects import EffectType
from core.models.input import Input
from core.pipelines.image_pipeline import ImagePipeline


class EffectListManager:
    _filters: dict[int, ImageFilter] = dict()

    def __init__(self) -> None:
        self._availables: set[EffectType] = set()
        self._availables.add(EffectType.BLACK_LEVEL)
        self._availables.add(EffectType.EXPOSURE)
        self._availables.add(EffectType.GAMMA)
        self._availables.add(EffectType.SATURATION)

    def add_effect(self, type: EffectType) -> bool:
        idx = len(self._filters)
        match type:
            case EffectType.BLACK_LEVEL:
                self._filters[idx] = DefaultFilter(EffectType.BLACK_LEVEL)
            case EffectType.EXPOSURE:
                self._filters[idx] = DefaultFilter(EffectType.EXPOSURE)
            case EffectType.GAMMA:
                self._filters[idx] = DefaultFilter(EffectType.GAMMA)
            case EffectType.SATURATION:
                self._filters[idx] = DefaultFilter(EffectType.SATURATION)

        return idx < len(self._filters)

    def get_available(self) -> set[EffectType]:
        return self._availables

    def remove_effect(self, idx: int) -> bool:
        size = len(self._filters)
        effect = self._filters.pop(idx, None)
        if effect is None:
            return False
        if size - 1 > idx:
            for i in range(idx + 1, size):
                old = self._filters.pop(i, None)
                if old is not None:
                    self._filters[i - 1] = old
        return True

    def get_effect_params(self, idx: int) -> dict[str, Input]:
        effect = self._filters.get(idx, None)
        if effect is None:
            return dict()

        return effect.get_params()

    def update_effect_param(self, idx: int, param: str, new_value: Any) -> bool:
        effect = self._filters.get(idx, None)
        if effect is None:
            return False

        params = effect.get_params()
        p = params.get(param, None)
        if p is None:
            return False

        res = p.update_value(new_value)

        return res

    def current_effects(self) -> dict[int, ImageFilter]:
        return dict(sorted(self._filters.items()))

    def clear(self):
        self._filters.clear()

    def get_pipeline(self) -> ImagePipeline:
        pipe = ImagePipeline()
        effects = self.current_effects()

        for _, effect in effects.items():
            pipe.add_stage(effect)

        return pipe
