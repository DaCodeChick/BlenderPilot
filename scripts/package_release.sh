#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
DIST_DIR="$ROOT_DIR/dist"
VERSION="${1:-0.1.0}"

mkdir -p "$DIST_DIR"

CLASSIC_ZIP="$DIST_DIR/BlenderPilot-v${VERSION}.zip"
EXT_ZIP="$DIST_DIR/BlenderPilot-v${VERSION}-extension.zip"

tmpdir="$(mktemp -d)"
cleanup() {
  rm -rf "$tmpdir"
}
trap cleanup EXIT

rsync -a "$ROOT_DIR/" "$tmpdir/BlenderPilot/" \
  --exclude .git \
  --exclude __pycache__ \
  --exclude .ruff_cache \
  --exclude dist \
  --exclude .env \
  --exclude '*.pyc'

(
  cd "$tmpdir"
  zip -rq "$CLASSIC_ZIP" BlenderPilot
  zip -rq "$EXT_ZIP" BlenderPilot
)

echo "Created: $CLASSIC_ZIP"
echo "Created: $EXT_ZIP"
