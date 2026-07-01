from __future__ import annotations

from typing import Sequence

from cli.args import parse_cli_arguments
from cli.runner import run_conversion


def run_cli_mode(argv: Sequence[str]) -> int:
    config = parse_cli_arguments(argv)
    return run_conversion(config)
