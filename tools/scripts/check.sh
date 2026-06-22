#!/bin/bash

root_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.." && pwd)"

uv run --directory "$root_dir" pre-commit run
