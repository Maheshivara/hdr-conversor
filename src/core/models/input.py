import os
import re
from abc import ABC, abstractmethod
from enum import Enum, auto
from pathlib import Path
from typing import Any, Callable, Optional, cast, override


class InputType(Enum):
    TEXT = auto()
    INTEGER = auto()
    CHECKBOX = auto()
    FLOAT = auto()
    COLOR = auto()
    FILE_PATH = auto()


class Input(ABC):
    def __init__(
        self,
        label: str,
        type: InputType,
        display_name: Optional[str],
        default: Optional[Any],
    ) -> None:
        super().__init__()
        self.label = label
        self._type = type
        self._default = default
        self._value = default
        self._display_name = display_name or label

    def update_value(self, new_value: Any) -> bool:
        valid = self.validate(new_value)
        if valid:
            self._value = new_value
            return True
        return False

    def get_value(self) -> Any:
        return self._value

    def reset_value(self):
        self._value = self._default

    def get_display_name(self) -> str:
        """
        Returns the param name to display.
        """
        return self._display_name

    @abstractmethod
    def validate(self, value: Any) -> bool:
        """
        Validate the input value.
        """
        pass

    @abstractmethod
    def get_display_value(self) -> str:
        """
        Returns the param value as string to display.
        """
        pass


class IntegerInput(Input):
    def __init__(
        self,
        label: str,
        default: Optional[int],
        display_name: Optional[str],
        checker: Optional[Callable[[int], bool]],
    ) -> None:
        super().__init__(label, InputType.INTEGER, display_name, default)
        self._checker = checker

    @override
    def validate(self, value: int) -> bool:
        if self._checker:
            return self._checker(value)
        return True

    @override
    def update_value(self, new_value: int) -> bool:
        return super().update_value(new_value)

    @override
    def get_value(self) -> int | None:
        return super().get_value()

    @override
    def get_display_value(self) -> str:
        if self._value is None:
            return ""
        return str(self._value)


class TextInput(Input):
    def __init__(
        self,
        label: str,
        default: Optional[str],
        display_name: Optional[str],
        checker: Optional[Callable[[str], bool]],
    ) -> None:
        super().__init__(label, InputType.TEXT, display_name, default)
        self._checker = checker

    @override
    def validate(self, value: str) -> bool:
        if self._checker:
            return self._checker(value)
        return True

    @override
    def update_value(self, new_value: str) -> bool:
        return super().update_value(new_value)

    @override
    def get_value(self) -> str | None:
        return super().get_value()

    @override
    def get_display_value(self) -> str:
        if self._value is None:
            return ""
        return str(self._value)


class CheckboxInput(Input):
    def __init__(
        self,
        label: str,
        default: Optional[bool],
        display_name: Optional[str],
        checker: Optional[Callable[[bool], bool]],
    ) -> None:
        super().__init__(label, InputType.CHECKBOX, display_name, default)
        self._checker = checker

    @override
    def validate(self, value: bool) -> bool:
        if self._checker:
            return self._checker(value)
        return True

    @override
    def update_value(self, new_value: bool) -> bool:
        return super().update_value(new_value)

    @override
    def get_value(self) -> bool | None:
        value = super().get_value()
        return cast(bool, value)

    @override
    def get_display_value(self) -> str:
        if self._value is None:
            return ""
        return str(bool(self._value))


class FloatInput(Input):
    def __init__(
        self,
        label: str,
        default: Optional[float],
        display_name: Optional[str],
        checker: Optional[Callable[[float], bool]],
    ) -> None:
        super().__init__(label, InputType.FLOAT, display_name, default)
        self._checker = checker

    @override
    def validate(self, value: float) -> bool:
        if self._checker:
            return self._checker(value)
        return True

    @override
    def update_value(self, new_value: float) -> bool:
        return super().update_value(new_value)

    @override
    def get_value(self) -> float | None:
        value = super().get_value()
        return cast(float, value)

    @override
    def get_display_value(self) -> str:
        if self._value is None:
            return ""
        return str(self._value)


class ColorInput(Input):
    """
    Accepts simple color representations:
    - Hex string like "#RRGGBB" or "#RGB"
    - Tuple/list of three integers (R, G, B) in 0-255
    """

    _HEX_RE = re.compile(r"^#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})$")

    def __init__(
        self,
        label: str,
        default: Optional[Any],
        display_name: Optional[str],
        checker: Optional[Callable[[Any], bool]],
    ) -> None:
        super().__init__(label, InputType.COLOR, display_name, default)
        self._checker = checker

    @override
    def validate(self, value: str | tuple[int, int, int]) -> bool:
        if self._checker:
            return self._checker(value)
        if isinstance(value, str):
            return bool(self._HEX_RE.fullmatch(value))
        if isinstance(value, (tuple, list)):
            if len(value) >= 3 and all(
                isinstance(c, int) and 0 <= c <= 255 for c in value[:3]
            ):
                return True
        return False

    @override
    def update_value(self, new_value: str | tuple[int, int, int]) -> bool:
        if isinstance(new_value, str):
            m = self._HEX_RE.fullmatch(new_value)
            if not m:
                return False
            raw = m.group(1)
            if len(raw) == 3:
                raw = "".join(ch * 2 for ch in raw)
            try:
                r = int(raw[0:2], 16)
                g = int(raw[2:4], 16)
                b = int(raw[4:6], 16)
            except Exception:
                return False
            tup = (r, g, b)
            return super().update_value(tup)

        try:
            tup = (int(new_value[0]), int(new_value[1]), int(new_value[2]))
        except Exception:
            return False
        if any(c < 0 or c > 255 for c in tup):
            return False
        return super().update_value(tup)

    @override
    def get_value(self) -> tuple[int, int, int] | None:
        if self._value is None:
            return None

        v = cast(tuple[int, int, int], self._value)
        return v

    @override
    def get_display_value(self) -> str:
        tup = self.get_value()
        if tup is None:
            return ""
        r, g, b = tup
        return f"#{r:02x}{g:02x}{b:02x}"


class FilePathInput(Input):
    def __init__(
        self,
        label: str,
        default: Optional[Any],
        display_name: Optional[str],
        checker: Optional[Callable[[Path], bool]],
    ) -> None:
        super().__init__(label, InputType.FILE_PATH, display_name, default)
        self._checker = checker

    @override
    def validate(self, value: Path | str) -> bool:
        p = Path(value)
        if self._checker:
            return self._checker(p)

        return os.path.exists(p) and os.path.isfile(p)

    @override
    def update_value(self, new_value: str | Path) -> bool:
        p = Path(new_value)
        return super().update_value(p)

    @override
    def get_value(self) -> Path | None:
        return super().get_value()

    @override
    def get_display_value(self) -> str:
        if self._value is None:
            return ""
        return str(self._value)
