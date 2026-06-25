from abc import ABC, abstractmethod

from core.models.enum.effects import EffectType
from core.models.image import Image
from core.models.input import Input


class ImageFilter(ABC):
    def __init__(self, type: EffectType) -> None:
        super().__init__()
        self._type: EffectType = type
        self._inputs: dict[str, Input] = dict()

    @abstractmethod
    def apply(
        self,
        image: Image,
    ) -> Image:
        pass

    def get_params(self) -> dict[str, Input]:
        return self._inputs

    def get_type(self) -> EffectType:
        return self._type
