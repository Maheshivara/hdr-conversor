from core.filters.image_filter import ImageFilter
from core.models.enum.effects import EffectType
from core.models.image import Image
from core.models.input import FloatInput, Input


class DefaultFilter(ImageFilter):
    def __init__(self, type: EffectType) -> None:
        super().__init__(type)
        self._inputs: dict[str, Input] = {"input": FloatInput("Input")}

    def apply(self, image: Image) -> Image:
        return super().apply(image)
