#!/usr/bin/env bash
# Adds a `format` alias to ~/.bashrc so you can run `format file.py` from anywhere.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

PYTHON="python3"
if [ -x "$REPO_ROOT/.venv/bin/python" ]; then
    PYTHON="$REPO_ROOT/.venv/bin/python"
fi

ALIAS_LINE="alias format=\"$PYTHON $REPO_ROOT/formatter.py\""

if grep -qF "$REPO_ROOT/formatter.py" ~/.bashrc 2>/dev/null; then
    echo "Alias already present in ~/.bashrc, skipping."
else
    echo "$ALIAS_LINE" >> ~/.bashrc
    echo "Added: $ALIAS_LINE"
    echo "Run 'source ~/.bashrc' or open a new terminal, then: format file.py"
fi
