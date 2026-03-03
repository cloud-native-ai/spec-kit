#!/usr/bin/env python3
"""List system binaries and environment information."""

import json
import platform
import shutil
import subprocess
from pathlib import Path
from typing import Any, Dict, List


def get_os_release() -> str:
    """Read OS release information from /etc/os-release."""
    os_release_path = Path("/etc/os-release")
    if os_release_path.exists():
        try:
            return os_release_path.read_text(encoding="utf-8").strip()
        except Exception:
            pass
    return ""


def get_kernel_info() -> str:
    """Get kernel information using uname."""
    try:
        result = subprocess.run(
            ["uname", "-a"],
            capture_output=True,
            text=True,
            check=False,
        )
        return result.stdout.strip()
    except Exception:
        return f"{platform.system()} {platform.release()}"


def get_system_binaries() -> List[Dict[str, str]]:
    """Check for common system binaries and their paths."""
    binaries_to_check = [
        "git",
        "docker",
        "kubectl",
        "python3",
        "python",
        "pip",
        "pip3",
        "node",
        "npm",
        "hatch",
        "gh",
        "jq",
        "curl",
        "wget",
        "make",
        "uv",
        "uvx",
    ]

    found_binaries = []
    for binary in binaries_to_check:
        path = shutil.which(binary)
        if path:
            found_binaries.append({"name": binary, "path": path})

    return found_binaries


def get_system_info() -> Dict[str, Any]:
    """Collect all system information."""
    return {
        "os_release": get_os_release(),
        "kernel": get_kernel_info(),
        "binaries": get_system_binaries(),
    }


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(description="List system binaries and environment information")
    parser.parse_args()

    data = get_system_info()
    print(json.dumps(data, indent=2, ensure_ascii=False))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
