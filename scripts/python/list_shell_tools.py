#!/usr/bin/env python3
"""List available shell functions."""

import json
import subprocess
from typing import Any, Dict, List


def get_shell_functions() -> List[Dict[str, str]]:
    """Get list of shell functions using compgen."""
    try:
        result = subprocess.run(
            ["bash", "-c", "compgen -A function | sort"],
            capture_output=True,
            text=True,
            check=False,
        )
        functions = []
        for line in result.stdout.strip().split("\n"):
            func_name = line.strip()
            if func_name and not func_name.startswith("_"):
                functions.append({"name": func_name})
        return functions
    except Exception:
        return []


def get_shell_info() -> Dict[str, Any]:
    """Collect shell function information."""
    functions = get_shell_functions()
    return {
        "functions": functions,
        "count": len(functions),
    }


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(description="List available shell functions")
    parser.add_argument(
        "--functions-only",
        action="store_true",
        help="Output only the functions array in JSON format",
    )
    args = parser.parse_args()

    data = get_shell_info()

    if args.functions_only:
        print(json.dumps(data.get("functions", []), ensure_ascii=False))
        return 0

    print(json.dumps(data, indent=2, ensure_ascii=False))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
