from abc import ABC, abstractmethod

from core.models.image import Image
from core.models.input import Input


class ImageFilter(ABC):
    def __init__(self) -> None:
        super().__init__()
        self._inputs: dict[str, Input] = {}

    @abstractmethod
    def apply(
        self,
        image: Image,
    ) -> Image:
        pass
