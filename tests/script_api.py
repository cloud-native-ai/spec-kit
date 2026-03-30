from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path

from typer.testing import CliRunner

from specify_cli import app

ROOT = Path(__file__).resolve().parents[1]
RUNNER = CliRunner()


def _load_module(name: str, file_name: str):
    module_path = ROOT / "scripts" / "python" / file_name
    spec = importlib.util.spec_from_file_location(name, module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load module from {module_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


tools_utils = _load_module("tools_utils", "tools-utils.py")
skills_utils = _load_module("skills_utils", "skills-utils.py")


def run_specify_init(args: list[str]):
    return RUNNER.invoke(app, ["init", *args])


def run_specify_check():
    return RUNNER.invoke(app, ["check"])


def run_generate_instructions(cwd: Path):
    script = ROOT / "scripts" / "bash" / "generate-instructions.sh"
    return subprocess.run([str(script)], cwd=cwd, check=False, capture_output=True, text=True)
