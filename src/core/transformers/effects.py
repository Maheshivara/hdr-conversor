import numpy as np
from typing import List

from core.enums.effect_id import EffectID


class EffectInfo:
    def __init__(self, effect_id: EffectID, enabled: bool, value: float) -> None:
        self.effect_id = effect_id
        self.enabled = enabled
        self.value = value


class EffectsTransformer:
    def apply_gamma_correction(self, image: np.ndarray, gamma: float) -> np.ndarray:
        if gamma <= 0.0:
            raise ValueError("Gamma must be greater than 0.")
        return np.power(image.astype(np.float32), float(1.0 / gamma))

    def revert_gamma_correction(self, image: np.ndarray, gamma: float) -> np.ndarray:
        if gamma <= 0.0:
            raise ValueError("Gamma must be greater than 0.")
        image = np.power(image.astype(np.float32), float(gamma))
        return image

    def adjust_exposure(self, image: np.ndarray, exposure_value: float) -> np.ndarray:
        factor = np.power(2.0, exposure_value)
        image = image.astype(np.float32) * factor
        return image

    def adjust_saturation(
        self, image: np.ndarray, saturation_factor: float
    ) -> np.ndarray:
        lum = (
            image[:, :, 0] * 0.2126 + image[:, :, 1] * 0.7152 + image[:, :, 2] * 0.0722
        )
        image = (1.0 - saturation_factor) * lum[
            ..., np.newaxis
        ] + saturation_factor * image
        return image

    def adjust_black_level(self, image: np.ndarray, black_level: float) -> np.ndarray:
        if black_level < 0.0 or black_level > 1.0:
            raise ValueError("Black level must be in the range [0, 1].")

        # This mostly matches GIMP behavior
        if (image < 1.0).any:
            image = np.pow(
                image.astype(np.float32), float(1.0 / 2.2)
            )  # Encode to gamma space (need to check if it's gamma 2.2 or sRGB)
            image = np.clip(image - black_level, 0.0, None) / (1.0 - black_level)
            image = np.power(
                image.astype(np.float32), 2.2
            )  # Decode back to linear space

        return image

    def apply_effects(self, image: np.ndarray, effects: List[EffectInfo]) -> np.ndarray:
        transformed_image = image

        for effect in effects:
            if not effect.enabled:
                continue

            elif effect.effect_id == EffectID.EXPOSURE:
                transformed_image = self.adjust_exposure(
                    transformed_image, effect.value
                )
            elif effect.effect_id == EffectID.SATURATION:
                transformed_image = self.adjust_saturation(
                    transformed_image, effect.value
                )
            elif effect.effect_id == EffectID.BLACK_LEVEL:
                transformed_image = self.adjust_black_level(
                    transformed_image, effect.value
                )

        return transformed_image
