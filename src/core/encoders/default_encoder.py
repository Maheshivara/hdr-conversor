import numpy as np

from core.encoders.encoder import Encoder
from core.models.image import Image, ImageOriginalExtension
from core.models.input import FloatInput, Input


class DefaultEncoder(Encoder):
    def __init__(self) -> None:
        super().__init__()
        self._inputs: dict[str, Input] = {"input": FloatInput("Input")}

    def encode(self, image: Image) -> Image:
        print("Encoded using Default")
        image_data = np.zeros([100, 100, 3], dtype=np.uint8)
        image = Image(ImageOriginalExtension.EXR, data=image_data, file_path="here")
        return image
