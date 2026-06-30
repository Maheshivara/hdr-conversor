import numpy as np

from core.encoders.encoder import Encoder
from core.models.image import Image
from core.models.input import FloatInput, Input


class RGBMEncoder(Encoder):
    def __init__(self) -> None:
        super().__init__()
        self._inputs: dict[str, Input] = {
            "coefficient": FloatInput("Coefficient", 8.0, checker=self._c_check)
        }

    def encode(self, image: Image) -> Image:
        c = float(self._inputs["coefficient"].get_value())

        image.data = image.data.astype(np.float32) ** float(1.0 / 2.2)

        data = image.data

        color = data[..., :3] / c
        alpha = np.maximum(
            np.maximum(color[..., 0], color[..., 1]), np.maximum(color[..., 2], 1e-6)
        )
        alpha = np.clip(alpha, 0.0, 1.0)

        alpha = np.ceil(alpha * 255.0) / 255.0

        alpha_exp = alpha[..., np.newaxis]
        del alpha
        rgb = color / alpha_exp

        encoded = np.concatenate([rgb, alpha_exp], axis=-1)
        del rgb, alpha_exp
        image.data = np.clip(encoded, 0.0, 1.0) * 255

        return image

    def _c_check(self, c: float):
        if c < 1:
            return False

        return True
