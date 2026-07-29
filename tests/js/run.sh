#!/usr/bin/env bash
# Engine-subset regression runner (node --test). Skips cleanly when Node is absent.
if ! command -v node >/dev/null 2>&1; then
  echo "SKIP: node not available; engine-subset tests skipped."
  exit 0
fi
cd "$(dirname "$0")/../.." && exec node --test tests/js/*.test.mjs
