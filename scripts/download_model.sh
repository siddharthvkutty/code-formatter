#!/usr/bin/env bash
# Pulls whatever model formatter.py is configured to use, so this never
# drifts out of sync with the actual OLLAMA_MODEL constant.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MODEL=$(sed -n 's/^OLLAMA_MODEL = "\(.*\)"/\1/p' "$SCRIPT_DIR/../formatter.py")

if [ -z "$MODEL" ]; then
    echo "error: could not find OLLAMA_MODEL in formatter.py" >&2
    exit 1
fi

if ! command -v ollama >/dev/null 2>&1; then
    echo "error: ollama is not installed. See https://ollama.com" >&2
    exit 1
fi

echo "Pulling $MODEL (multi-GB download, this can take a while)..."
ollama pull "$MODEL"
