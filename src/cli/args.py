from __future__ import annotations

import argparse
from typing import Sequence

from cli.config import (
    DEFAULT_BLACK_LEVEL_VALUE,
    DEFAULT_EXPOSURE_VALUE,
    DEFAULT_RGBM_COEFFICIENT,
    DEFAULT_SATURATION_VALUE,
    SUPPORTED_FORMATS,
    build_cli_config,
    CliConfig,
)


def _bounded_float(min_value: float, max_value: float):
    def _validator(value: str) -> float:
        converted = float(value)
        if converted < min_value or converted > max_value:
            raise argparse.ArgumentTypeError(
                f"Value must be between {min_value} and {max_value}."
            )
        return converted

    return _validator


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="hdr-converter-cli",
        description="Convert HDR/EXR images to RGBM in PNG and/or DDS format.",
    )

    parser.add_argument(
        "--image",
        action="append",
        default=[],
        metavar="PATH",
        help="Path to an input image (.hdr or .exr). Can be repeated.",
    )
    parser.add_argument(
        "--directory",
        type=str,
        help="Directory containing .hdr and .exr images.",
    )
    parser.add_argument(
        "--output",
        type=str,
        help="Output directory. Defaults to your Pictures folder when available.",
    )
    parser.add_argument(
        "--format_out",
        nargs="+",
        choices=SUPPORTED_FORMATS,
        required=True,
        metavar="FORMAT",
        help="Required output format(s). Accepts: png dds.",
    )

    parser.add_argument(
        "--rgbm_coe",
        type=float,
        default=DEFAULT_RGBM_COEFFICIENT,
        help="RGBM coefficient. Default: 8.0",
    )

    parser.add_argument(
        "-eef",
        "--exposure",
        nargs="?",
        const=DEFAULT_EXPOSURE_VALUE,
        type=_bounded_float(-100.0, 100.0),
        default=None,
        metavar="VALUE",
        help=(
            "Enable exposure filter. Optional value from -100.0 to 100.0. "
            "If omitted, uses 0.0."
        ),
    )

    parser.add_argument(
        "-eblf",
        "--black_level",
        nargs="?",
        const=DEFAULT_BLACK_LEVEL_VALUE,
        type=_bounded_float(0.01, 1.0),
        default=None,
        metavar="VALUE",
        help=(
            "Enable black level filter. Optional value from 0.01 to 1.0. "
            "If omitted, uses 0.1."
        ),
    )

    parser.add_argument(
        "-esf",
        "--saturation",
        nargs="?",
        const=DEFAULT_SATURATION_VALUE,
        type=_bounded_float(0.1, 5.0),
        default=None,
        metavar="VALUE",
        help=(
            "Enable saturation filter. Optional value from 0.1 to 5.0. "
            "If omitted, uses 1.0."
        ),
    )

    return parser


def parse_cli_arguments(argv: Sequence[str]) -> CliConfig:
    parser = create_parser()
    args = parser.parse_args(list(argv))

    if not args.image and not args.directory:
        parser.error("At least one of --image or --directory must be provided.")

    exposure_enabled = args.exposure is not None
    exposure_value = args.exposure if exposure_enabled else DEFAULT_EXPOSURE_VALUE

    black_level_enabled = args.black_level is not None
    black_level_value = (
        args.black_level if black_level_enabled else DEFAULT_BLACK_LEVEL_VALUE
    )

    saturation_enabled = args.saturation is not None
    saturation_value = (
        args.saturation if saturation_enabled else DEFAULT_SATURATION_VALUE
    )

    try:
        return build_cli_config(
            images=args.image,
            directory=args.directory,
            output_directory=args.output,
            output_formats=args.format_out,
            rgbm_coefficient=args.rgbm_coe,
            enable_exposure_filter=exposure_enabled,
            exposure_value=exposure_value,
            enable_black_level_filter=black_level_enabled,
            black_level_value=black_level_value,
            enable_saturation_filter=saturation_enabled,
            saturation_value=saturation_value,
        )
    except ValueError as exc:
        parser.error(str(exc))
