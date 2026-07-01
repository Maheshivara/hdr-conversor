from __future__ import annotations

import sys
import time
from pathlib import Path

from PIL import UnidentifiedImageError

from core.encoders.rgbm import RGBMEncoder
from core.enums.effect_id import EffectID
from core.readers.image import ImageReader
from core.transformers.effects import EffectInfo, EffectsTransformer
from core.writers.image import ImageWriter

from cli.config import CliConfig


def _build_effects(config: CliConfig) -> list[EffectInfo]:
    return [
        EffectInfo(EffectID.EXPOSURE, config.enable_exposure_filter, config.exposure_value),
        EffectInfo(
            EffectID.BLACK_LEVEL,
            config.enable_black_level_filter,
            config.black_level_value,
        ),
        EffectInfo(
            EffectID.SATURATION,
            config.enable_saturation_filter,
            config.saturation_value,
        ),
    ]


def _build_output_path(output_directory: Path, image_path: Path, extension: str) -> Path:
    timestamp = time.strftime("%d%m%Y_%H%M%S")
    filename = f"{image_path.stem}_rgbm_{timestamp}.{extension}"
    return output_directory / filename


def run_conversion(config: CliConfig) -> int:
    reader = ImageReader()
    writer = ImageWriter()
    transformer = EffectsTransformer()
    encoder = RGBMEncoder(config.rgbm_coefficient)
    effects = _build_effects(config)

    total_images = len(config.image_paths)
    failures = 0

    for index, image_path in enumerate(config.image_paths, start=1):
        try:
            image = reader.read_image(str(image_path))
            if image is None:
                raise RuntimeError(f"Failed to read image: {image_path}")

            image = transformer.apply_effects(image, effects)
            rgbm_image = (
                encoder.from_exr(image)
                if image_path.suffix.lower() == ".exr"
                else encoder.from_hdr(image)
            )

            written_files: list[str] = []
            for output_format in config.output_formats:
                output_path = _build_output_path(
                    config.output_directory,
                    image_path,
                    output_format,
                )
                if output_format == "png":
                    writer.write_as_png(str(output_path), rgbm_image)
                elif output_format == "dds":
                    writer.write_as_dds(str(output_path), rgbm_image)
                written_files.append(str(output_path))

            print(
                f"[{index}/{total_images}] Converted {image_path.name} -> "
                f"{', '.join(written_files)}"
            )

        except (RuntimeError, ValueError, OSError, UnidentifiedImageError) as exc:
            failures += 1
            print(f"[{index}/{total_images}] Error processing {image_path}: {exc}", file=sys.stderr)

    if failures:
        print(
            f"Completed with {failures} error(s).",
            file=sys.stderr,
        )
        return 1

    print("Conversion completed successfully.")
    return 0
