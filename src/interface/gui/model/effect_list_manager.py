from typing import Any

from core.filters.default_filter import DefaultFilter
from core.filters.image_filter import ImageFilter
from core.models.enum.effects import EffectType
from core.models.input import Input


class EffectListManager:
    _filters: dict[int, ImageFilter] = dict()

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
        s: set[EffectType] = set()
        s.add(EffectType.BLACK_LEVEL)
        s.add(EffectType.EXPOSURE)
        s.add(EffectType.GAMMA)
        s.add(EffectType.SATURATION)
        return s

    def remove_effect(self, idx: int) -> bool:
        effect = self._filters.pop(idx, None)
        if effect is None:
            return False

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
        return self._filters

    def clear(self):
        self._filters.clear()
