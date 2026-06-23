from enum import Enum, auto

import numpy as np


class ImageOriginalExtension(Enum):
    EXR = auto()
    HDR = auto()


class Image:
    def __init__(
        self,
        original_extension: ImageOriginalExtension,
        data: np.ndarray,
        file_path: str,
    ) -> None:
        self.original_extension = original_extension
        self.data = data
        self.file_path = file_path
        self.encoded: bool = False
