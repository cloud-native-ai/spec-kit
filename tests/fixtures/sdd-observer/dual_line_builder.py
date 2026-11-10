"""Two independent temp project roots for the dual-line isolation drill (Feature 096, wp01 T036).

Each line gets its own project root, spec directory, state spine and state directory, built by the
same line builder (which reads the declared stage sequence from the fact owner). No path is shared
between the two fixtures (SC-005).
"""
from __future__ import annotations

import importlib.util
from pathlib import Path

_LINE_BUILDER = Path(__file__).with_name("line_builder.py")


def _line_builder():
    spec = importlib.util.spec_from_file_location("sdd_observer_line_builder", _LINE_BUILDER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def build_dual(root: Path):
    """Build two independent lines under ``root`` and return both fixture mappings."""
    root = Path(root)
    builder = _line_builder()
    first = builder.build_line(root / "line-a", line_id="line-a", run_id="run-a",
                               spec_key="096-sdd-observer-agent-a")
    second = builder.build_line(root / "line-b", line_id="line-b", run_id="run-b",
                                spec_key="096-sdd-observer-agent-b")
    return [first, second]
