#!/usr/bin/env python3
"""List available shell functions."""

import json
import subprocess
from typing import Any, Dict, List

# Shell profile files to source for function discovery
_SHELL_PROFILE_SOURCES = """
# Source system profile
[ -f /etc/profile ] && source /etc/profile

# Source user bashrc
[ -f ~/.bashrc ] && source ~/.bashrc

# Source user profile (fallback for login shells)
[ -f ~/.profile ] && source ~/.profile

# Source bash profile (for login shells)
[ -f ~/.bash_profile ] && source ~/.bash_profile
"""


def get_shell_functions() -> List[Dict[str, str]]:
    """Get list of shell functions using compgen."""
    try:
        # Build the command: source profiles first, then list functions
        cmd = f"{_SHELL_PROFILE_SOURCES}\ncompgen -A function | sort"
        result = subprocess.run(
            ["bash", "-c", cmd],
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
