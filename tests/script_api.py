from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


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
