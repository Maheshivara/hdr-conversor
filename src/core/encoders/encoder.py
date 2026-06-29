from abc import ABC, abstractmethod
from typing import Any

from core.models.image import Image
from core.models.input import Input


class Encoder(ABC):
    def __init__(
        self,
    ) -> None:
        super().__init__()
        self._inputs: dict[str, Input] = dict()

    @abstractmethod
    def encode(self, image: Image) -> Image:
        pass

    def get_inputs(self) -> dict[str, Input]:
        return self._inputs

    def update_input_value(self, input: str, new_value: Any) -> bool:
        i = self._inputs.get(input, None)
        if i is None:
            return False

        updated = i.update_value(new_value)

        return updated
