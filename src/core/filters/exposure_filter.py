from core.filters.image_filter import ImageFilter
from core.models.enum.effects import EffectType
from core.models.image import Image
from core.models.input import FloatInput


class ExposureFilter(ImageFilter):
    def __init__(self):
        super().__init__(EffectType.EXPOSURE)

        self._inputs = {"exposure": FloatInput("Exposure", 0.0)}

    def apply(self, image: Image) -> Image:
        exposure = self._inputs["exposure"].get_value()

        image.data *= 2.0**exposure

        return image
