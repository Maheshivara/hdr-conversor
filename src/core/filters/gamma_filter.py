from core.filters.image_filter import ImageFilter
from core.models.enum.effects import EffectType
from core.models.image import Image
from core.models.input import FloatInput


class GammaFilter(ImageFilter):
    def __init__(self):
        super().__init__(EffectType.GAMMA)

        self._inputs = {"gamma": FloatInput("Gamma", 2.2)}

    def apply(self, image: Image) -> Image:
        gamma = float(self._inputs["gamma"].get_value())

        image.data = image.data**gamma

        return image
