#!/usr/bin/env bash
# Canonical test runner for spec-kit SDD baseline/regression tasks.
# Resolves the pytest interpreter once and fails loudly — pipe-safe, alias-proof.
set -euo pipefail

resolve_python() {
    for candidate in "${SPECKIT_PYTHON:-}" ".venv/bin/python" "python3" "python"; do
        [ -n "$candidate" ] || continue
        if command -v "$candidate" >/dev/null 2>&1 || [ -x "$candidate" ]; then
            if "$candidate" -m pytest --version >/dev/null 2>&1; then
                echo "$candidate"
                return 0
            fi
        fi
    done
    echo "error: no interpreter with pytest found (tried SPECKIT_PYTHON, .venv/bin/python, python3, python)" >&2
    return 1
}

PY="$(resolve_python)"
echo "# test runner: $PY -m pytest $*" >&2
exec "$PY" -m pytest "$@"
