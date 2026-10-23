#!/usr/bin/env bash
# MoCapAnything V2 - one-click installer (Linux/macOS) by PixelArtistry
set -e
cd "$(dirname "$0")"
if ! command -v uv >/dev/null 2>&1; then
  echo "Installing uv (Python package manager)..."
  curl -LsSf https://astral.sh/uv/install.sh | sh
  export PATH="$HOME/.local/bin:$PATH"
fi
uv run --python 3.11 --no-project install_mocapanything.py
echo "Done. Start it with ./run.sh"
