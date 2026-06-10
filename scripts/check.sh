#!/usr/bin/env bash
set -e

echo "== ApplyPilot Check =="
pwd
git status --short || true

if [ -f package.json ]; then
  echo "Node project detected"
  npm run 2>/dev/null || true
fi

if [ -f pyproject.toml ] || [ -f requirements.txt ]; then
  echo "Python project detected"
fi

echo "Check complete."
