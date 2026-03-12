#!/usr/bin/env python3
from __future__ import annotations

import argparse
import ast
import dataclasses
import json
import os
import platform
import shutil
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


def _group_tools_by_server() -> Dict[str, List[dict]]:
    from cws_ai.mcp import get_all_tools

    tools = get_all_tools()
    tools_by_server: Dict[str, List[dict]] = {}
    for tool in tools:
        tools_by_server.setdefault(tool.server_name, []).append(dataclasses.asdict(tool))
    return tools_by_server


def get_mcp_payload() -> dict:
    from cws_ai.mcp import get_all_mcp_servers

    servers = get_all_mcp_servers()
    tools_by_server = _group_tools_by_server()

    servers_payload = []
    for server in servers:
        server_data = dataclasses.asdict(server)
        server_tools = tools_by_server.get(server.name, [])
        server_data["tools"] = server_tools
        server_data["tools_count"] = len(server_tools)
        servers_payload.append(server_data)

    return {
        "timestamp": datetime.now().isoformat(),
        "count": len(servers_payload),
        "servers": servers_payload,
        "note": "This list represents configured MCP servers. 'tools' field populated for HTTP servers if reachable.",
    }


def find_root_dir(start: Optional[Path] = None) -> Path:
    current = (start or Path.cwd()).resolve()
    for candidate in [current, *current.parents]:
        if (candidate / ".git").exists():
            return candidate
        if (candidate / "pyproject.toml").exists() and (candidate / "scripts").exists():
            return candidate
    return current


def detect_scripts_dir(root_dir: Path) -> Optional[Path]:
    specify_scripts = root_dir / ".specify" / "scripts"
    local_scripts = root_dir / "scripts"
    if specify_scripts.exists() and specify_scripts.is_dir():
        return specify_scripts
    if local_scripts.exists() and local_scripts.is_dir():
        return local_scripts
    return None


def extract_python_docstring(file_path: Path) -> str:
    try:
        content = file_path.read_text(encoding="utf-8")
        doc = ast.get_docstring(ast.parse(content))
        if doc:
            return doc.splitlines()[0].strip()
    except Exception:
        pass
    return "No description available"


def extract_shell_comment(file_path: Path) -> str:
    try:
        for line in file_path.read_text(encoding="utf-8").splitlines():
            stripped = line.strip()
            if stripped.startswith("#!"):
                continue
            if stripped.startswith("#"):
                return stripped.lstrip("#").strip() or "No description available"
    except Exception:
        pass
    return "No description available"


def list_project_scripts(root_dir: Path) -> List[Dict[str, str]]:
    scripts_dir = detect_scripts_dir(root_dir)
    if not scripts_dir:
        return []

    results: List[Dict[str, str]] = []
    for file_path in sorted(scripts_dir.rglob("*")):
        if not file_path.is_file():
            continue
        if file_path.suffix not in {".sh", ".py"}:
            continue

        rel_path = file_path.resolve().relative_to(root_dir.resolve()).as_posix()
        script_type = "python" if file_path.suffix == ".py" else "bash"
        if script_type == "python":
            description = extract_python_docstring(file_path)
        else:
            description = extract_shell_comment(file_path)

        results.append(
            {
                "name": file_path.name,
                "path": rel_path,
                "type": script_type,
                "description": description,
            }
        )
    return results


_SHELL_PROFILE_SOURCES = """
[ -f /etc/profile ] && source /etc/profile
[ -f ~/.bashrc ] && source ~/.bashrc
[ -f ~/.profile ] && source ~/.profile
[ -f ~/.bash_profile ] && source ~/.bash_profile
"""


def get_shell_functions() -> List[Dict[str, str]]:
    try:
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
    functions = get_shell_functions()
    return {
        "functions": functions,
        "count": len(functions),
    }


def get_os_release() -> str:
    os_release_path = Path("/etc/os-release")
    if os_release_path.exists():
        try:
            return os_release_path.read_text(encoding="utf-8").strip()
        except Exception:
            pass
    return ""


def get_kernel_info() -> str:
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
    return {
        "os_release": get_os_release(),
        "kernel": get_kernel_info(),
        "binaries": get_system_binaries(),
    }


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Unified tools utilities")
    parser.add_argument("--action", required=True, choices=["list"])
    parser.add_argument("--type", choices=["mcp", "system", "shell", "project"], default=None)
    parser.add_argument("--functions-only", action="store_true")
    parser.add_argument("--root-dir", default=".")
    return parser


def main() -> int:
    parser = _build_parser()
    args = parser.parse_args()

    if args.action == "list":
        if args.type == "mcp":
            if not os.environ.get("MCP_AUTH"):
                print("[Error] MCP_AUTH environment variable is not set.", file=os.sys.stderr)
                return 1
            payload = get_mcp_payload()
            print(json.dumps(payload, indent=2, ensure_ascii=False))
            return 0

        if args.type == "system":
            print(json.dumps(get_system_info(), indent=2, ensure_ascii=False))
            return 0

        if args.type == "shell":
            payload = get_shell_info()
            if args.functions_only:
                print(json.dumps(payload.get("functions", []), ensure_ascii=False))
            else:
                print(json.dumps(payload, indent=2, ensure_ascii=False))
            return 0

        if args.type == "project":
            root_dir = find_root_dir(Path(args.root_dir))
            records = list_project_scripts(root_dir)
            print(json.dumps(records, ensure_ascii=False, indent=2))
            return 0

        parser.error("--action list requires --type")

    parser.error("Unknown action")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
