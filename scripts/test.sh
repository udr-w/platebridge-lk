#!/usr/bin/env sh
set -eu
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cd "$ROOT/backend" && .venv/bin/python -m pytest
cd "$ROOT/frontend" && npm test && npm run typecheck && npm run build
