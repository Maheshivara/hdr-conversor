from abc import ABC, abstractmethod

from core.models.image import Image
from core.models.input import Input


class Encoder(ABC):
    def __init__(
        self,
    ) -> None:
        super().__init__()
        self._inputs: dict[str, Input] = {}

    @abstractmethod
    def encode(self, image: Image) -> Image:
        pass
