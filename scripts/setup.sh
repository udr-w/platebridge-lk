#!/usr/bin/env sh
set -eu
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
python3 -m venv "$ROOT/backend/.venv"
"$ROOT/backend/.venv/bin/pip" install -r "$ROOT/backend/requirements.txt"
cd "$ROOT/frontend" && npm install
cd "$ROOT/backend" && .venv/bin/python -m app.seed
echo "Setup complete. Run ./scripts/start.sh"
