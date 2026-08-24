#!/usr/bin/env bash

set -euo pipefail

echo "========================================"
echo "AI Platform Engineering - Dev Bootstrap"
echo "========================================"

PROJECT_ROOT="/workspaces/ai-platform-engineering"

cd "$PROJECT_ROOT"

echo "[1/4] Creating Python virtual environment..."

if [ ! -d ".venv" ]; then
    python -m venv .venv
fi

echo "[2/4] Installing API dependencies..."

.venv/bin/python -m pip install --upgrade pip

.venv/bin/python -m pip install \
    -r services/api/requirements.txt

echo "[3/4] Checking Docker..."

docker info >/dev/null

echo "[4/4] Configuring development shell..."

echo "Bootstrap complete."
echo
echo "Next steps:"
echo "  source .venv/bin/activate"
echo "  ./scripts/dev-up.sh"

SHELL_CONFIG="$HOME/.bashrc"

AUTO_ACTIVATE_LINE="source $PROJECT_ROOT/.devcontainer/auto-activate.sh"

if ! grep -Fxq "$AUTO_ACTIVATE_LINE" "$SHELL_CONFIG"; then
    echo "$AUTO_ACTIVATE_LINE" >> "$SHELL_CONFIG"
fi