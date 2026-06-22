#!/bin/bash

root_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.." && pwd)"

uv run --directory "$root_dir" ruff format
uv run --directory "$root_dir" ruff check --fix
