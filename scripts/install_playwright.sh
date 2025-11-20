#!/usr/bin/env bash
set -euo pipefail

# Install Playwright Chromium into a writable path (works on Render build machines).
export PLAYWRIGHT_BROWSERS_PATH="${PLAYWRIGHT_BROWSERS_PATH:-/tmp/playwright}"
mkdir -p "$PLAYWRIGHT_BROWSERS_PATH"

PYTHON_BIN="${PYTHON_BIN:-python3}"
if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
  PYTHON_BIN="python"
fi

echo "PLAYWRIGHT_BROWSERS_PATH=${PLAYWRIGHT_BROWSERS_PATH}"
echo "Using Python interpreter: ${PYTHON_BIN}"

if ! "$PYTHON_BIN" - <<'PY'
import importlib.util
import sys

if importlib.util.find_spec("playwright") is None:
    sys.exit("Playwright Python package not found. Run `pip install playwright` before this script.")
PY
then
  exit 1
fi

# Install Chromium browser. Avoid --with-deps to prevent sudo prompts on Render.
"$PYTHON_BIN" -m playwright install chromium

echo "Playwright Chromium installed successfully."
