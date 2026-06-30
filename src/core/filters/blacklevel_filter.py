import numpy as np

from core.filters.image_filter import ImageFilter
from core.models.enum.effects import EffectType
from core.models.image import Image
from core.models.input import FloatInput


class BlackLevelFilter(ImageFilter):
    def __init__(self):
        super().__init__(EffectType.BLACK_LEVEL)

        self._inputs = {"black_level": FloatInput("Black Level", 0.0)}

    def apply(self, image: Image) -> Image:
        black_level = self._inputs["black_level"].get_value()

        if (image.data < 1.0).any():
            # In practice we're always in linear space at each filter, so this isn't too bad
            image.data = image.data.astype(np.float32) ** float(1.0 / 2.2)
            image.data = np.clip(image.data - black_level, 0.0, None) / (
                1.0 - black_level
            )
            image.data = image.data.astype(np.float32) ** 2.2

        return image
