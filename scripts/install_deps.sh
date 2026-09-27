#!/usr/bin/env bash
# Installs this project's Python requirements and rustfmt (if rustup is available).
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Installing Python requirements..."
pip install -r "$SCRIPT_DIR/../requirements.txt"

echo
if command -v rustup >/dev/null 2>&1; then
    echo "Installing rustfmt via rustup..."
    rustup component add rustfmt
elif command -v rustfmt >/dev/null 2>&1; then
    echo "rustfmt already installed, skipping."
else
    echo "rustup not found, skipping rustfmt."
    echo "Install Rust via https://rustup.rs, then run: rustup component add rustfmt"
fi
