import numpy as np

from core.filters.image_filter import ImageFilter
from core.models.enum.effects import EffectType
from core.models.image import Image
from core.models.input import FloatInput


class SaturationFilter(ImageFilter):
    def __init__(self):
        super().__init__(EffectType.SATURATION)

        self._inputs = {"saturation": FloatInput("Saturation", 1.0)}

    def apply(self, image: Image) -> Image:
        saturation = self._inputs["saturation"].get_value()

        lum = (
            image[:, :, 0] * 0.2126 + image[:, :, 1] * 0.7152 + image[:, :, 2] * 0.0722
        )
        image = (1.0 - saturation) * lum[..., np.newaxis] + saturation * image

        return image
