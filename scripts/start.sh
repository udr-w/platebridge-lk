#!/usr/bin/env sh
set -eu
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
trap 'kill 0' INT TERM EXIT
cd "$ROOT/backend" && .venv/bin/uvicorn app.main:app --reload --port 8000 &
cd "$ROOT/frontend" && npm run dev &
wait
