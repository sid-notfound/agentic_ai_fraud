#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MODE="${1:-api}"

cd "$ROOT_DIR"

if [[ -x "$ROOT_DIR/.venv/bin/python" ]]; then
  PYTHON_BIN="$ROOT_DIR/.venv/bin/python"
elif [[ -x "$ROOT_DIR/venv/bin/python" ]]; then
  PYTHON_BIN="$ROOT_DIR/venv/bin/python"
elif command -v python3 >/dev/null 2>&1; then
  PYTHON_BIN="$(command -v python3)"
elif command -v python >/dev/null 2>&1; then
  PYTHON_BIN="$(command -v python)"
else
  echo "Python was not found. Create a virtualenv and install requirements first."
  exit 1
fi

case "$MODE" in
  api)
    exec "$PYTHON_BIN" -m uvicorn app:app --reload --port 8000
    ;;
  demo)
    exec "$PYTHON_BIN" scripts/run_demo.py
    ;;
  *)
    echo "Usage: ./run.sh [api|demo]"
    exit 1
    ;;
esac
