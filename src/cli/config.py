from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

SUPPORTED_EXTENSIONS = (".exr", ".hdr")
SUPPORTED_FORMATS = ("png", "dds")

DEFAULT_RGBM_COEFFICIENT = 8.0
DEFAULT_EXPOSURE_VALUE = 0.0
DEFAULT_BLACK_LEVEL_VALUE = 0.1
DEFAULT_SATURATION_VALUE = 1.0


@dataclass(frozen=True)
class CliConfig:
    image_paths: tuple[Path, ...]
    output_directory: Path
    output_formats: tuple[str, ...]
    rgbm_coefficient: float
    enable_exposure_filter: bool
    exposure_value: float
    enable_black_level_filter: bool
    black_level_value: float
    enable_saturation_filter: bool
    saturation_value: float


def get_default_output_directory() -> Path:
    pictures_path = Path.home() / "Pictures"
    if pictures_path.is_dir():
        return pictures_path

    return Path.cwd()


def _resolve_image_paths(images: Sequence[str], directory: str | None) -> tuple[Path, ...]:
    resolved_paths: list[Path] = []

    for image_path in images:
        path = Path(image_path).expanduser()
        if not path.is_file():
            raise ValueError(f"Image path does not exist: {image_path}")
        if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            raise ValueError(
                f"Unsupported image extension for '{image_path}'. Supported: {', '.join(SUPPORTED_EXTENSIONS)}"
            )
        resolved_paths.append(path.resolve())

    if directory:
        directory_path = Path(directory).expanduser()
        if not directory_path.is_dir():
            raise ValueError(f"Directory does not exist: {directory}")

        directory_images: list[Path] = []
        for item in sorted(directory_path.iterdir()):
            if item.is_file() and item.suffix.lower() in SUPPORTED_EXTENSIONS:
                directory_images.append(item.resolve())

        if not directory_images and not resolved_paths:
            raise ValueError(
                "No supported images found in directory. Supported extensions: .exr, .hdr"
            )
        resolved_paths.extend(directory_images)

    if not resolved_paths:
        raise ValueError("At least one input image is required.")

    unique_paths = dict.fromkeys(resolved_paths)
    return tuple(unique_paths.keys())


def _resolve_output_directory(output_directory: str | None) -> Path:
    if output_directory:
        resolved_output = Path(output_directory).expanduser()
    else:
        resolved_output = get_default_output_directory()

    if not resolved_output.is_dir():
        raise ValueError(
            f"Output directory does not exist: {resolved_output}"
        )

    return resolved_output.resolve()


def _resolve_output_formats(formats: Sequence[str]) -> tuple[str, ...]:
    normalized = [fmt.lower() for fmt in formats]
    if not normalized:
        raise ValueError("--format_out is required and must include at least one format.")

    for fmt in normalized:
        if fmt not in SUPPORTED_FORMATS:
            raise ValueError(
                f"Unsupported output format: {fmt}. Supported: {', '.join(SUPPORTED_FORMATS)}"
            )

    unique_formats = tuple(dict.fromkeys(normalized).keys())
    return unique_formats


def build_cli_config(
    images: Sequence[str],
    directory: str | None,
    output_directory: str | None,
    output_formats: Sequence[str],
    rgbm_coefficient: float,
    enable_exposure_filter: bool,
    exposure_value: float,
    enable_black_level_filter: bool,
    black_level_value: float,
    enable_saturation_filter: bool,
    saturation_value: float,
) -> CliConfig:
    if rgbm_coefficient <= 0.0:
        raise ValueError("RGBM Coefficient must be greater than zero.")

    if enable_black_level_filter and not (0.0 < black_level_value <= 1.0):
        raise ValueError("Black level must be in the range (0, 1].")

    image_paths = _resolve_image_paths(images, directory)
    resolved_output_directory = _resolve_output_directory(output_directory)
    resolved_output_formats = _resolve_output_formats(output_formats)

    return CliConfig(
        image_paths=image_paths,
        output_directory=resolved_output_directory,
        output_formats=resolved_output_formats,
        rgbm_coefficient=rgbm_coefficient,
        enable_exposure_filter=enable_exposure_filter,
        exposure_value=exposure_value,
        enable_black_level_filter=enable_black_level_filter,
        black_level_value=black_level_value,
        enable_saturation_filter=enable_saturation_filter,
        saturation_value=saturation_value,
    )
