#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MODE="${1:-api}"

cd "$ROOT_DIR"

case "$MODE" in
  api)
    exec uvicorn app:app --reload --port 8000
    ;;
  demo)
    exec python scripts/run_demo.py
    ;;
  *)
    echo "Usage: ./run.sh [api|demo]"
    exit 1
    ;;
esac
