import sys
from dataclasses import dataclass
from os import path
from pathlib import Path


@dataclass(frozen=True)
class AppMetadata:
    APP_NAME = "HDR Converter"
    APP_DESCRIPTION = "A simple Python tool that converts HDR images (.hdr and .exr) to RGBM, RGBE or LogLUV format using OpenCV and Pillow"
    APP_VERSION = "2.0.0"
    APP_ORGANIZATION = "HJLW"


@dataclass(frozen=True)
class DefaultPath:
    ROOT_DIR = Path(
        path.abspath(path.join(path.dirname(__file__), "..", ".."))
        if not getattr(sys, "frozen", False)
        else getattr(
            sys, "_MEIPASS", path.abspath(path.join(path.dirname(__file__), "..", ".."))
        )
    )
    ASSETS_DIR = Path(path.join(ROOT_DIR, "assets"))
    ICONS_DIR = Path(path.join(ASSETS_DIR, "icons"))
    LUTS_DIR = Path(path.join(ASSETS_DIR, "LUTs"))
    FONTS_DIR = Path(path.join(ASSETS_DIR, "fonts"))
    PALETTES_DIR = Path(path.join(ASSETS_DIR, "palettes"))
    LOCALES_DIR = Path(path.join(ASSETS_DIR, "locales"))


@dataclass(frozen=True)
class ImageConfig:
    VALID_EXTENSIONS = [".exr", ".hdr"]

    def is_valid_path(self, p: str) -> bool:
        if path.exists(p) and path.isfile(p):
            for ext in self.VALID_EXTENSIONS:
                if p.endswith(ext):
                    return True
        return False
