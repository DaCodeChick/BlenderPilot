#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

echo "[verify] Running syntax checks"
python3 -m py_compile \
  "$ROOT_DIR"/__init__.py \
  "$ROOT_DIR"/core/*.py \
  "$ROOT_DIR"/core/providers/*.py \
  "$ROOT_DIR"/mcp_server/main.py \
  "$ROOT_DIR"/mcp_server/tool_definitions/*.py \
  "$ROOT_DIR"/mcp_server/handler_modules/*.py \
  "$ROOT_DIR"/ops/*.py \
  "$ROOT_DIR"/tests/test_*.py

echo "[verify] Running unit tests"
python3 -m unittest discover -s "$ROOT_DIR/tests" -p "test_*.py" -v

echo "[verify] Release verification passed"
