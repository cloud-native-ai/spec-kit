"""Structural tamper variants for the journal checker (Feature 096, wp01 T014).

Each variant returns a doctored copy of a rendered journal; the caller writes it back and runs
``journal-utils.py --action check``, which must exit 1 naming the touched row. The variants are
structural — no semantic (language) detection is involved (SC-004).
"""
from __future__ import annotations

VARIANTS = ("ten-column", "unknown-event", "free-narrative", "forged-pointer",
            "unresolvable-commit")


def _split(line):
    body = line.strip()
    if body.startswith("|"):
        body = body[1:]
    if body.endswith("|") and not body.endswith("\\|"):
        body = body[:-1]
    cells, current, index = [], [], 0
    while index < len(body):
        char = body[index]
        if char == "\\" and index + 1 < len(body) and body[index + 1] == "|":
            current.append("|")
            index += 2
            continue
        if char == "|":
            cells.append("".join(current).strip())
            current = []
            index += 1
            continue
        current.append(char)
        index += 1
    cells.append("".join(current).strip())
    return cells


def _render(cells):
    return "| " + " | ".join(cells) + " |"


def _data_row_indices(lines):
    indices = []
    for index, line in enumerate(lines):
        if line.strip().startswith("|"):
            cells = _split(line)
            if cells and cells[0].isdigit():
                indices.append(index)
    return indices


def tamper(text: str, variant: str) -> str:
    """Return ``text`` with one structural tamper applied; raises on an undrilled variant."""
    lines = text.splitlines()
    rows = _data_row_indices(lines)
    if not rows:
        raise ValueError("the journal carries no data row to tamper with")
    target = rows[-1]
    if variant == "ten-column":
        lines[target] = lines[target].rstrip() + " recommendation |"
    elif variant == "unknown-event":
        cells = _split(lines[target])
        cells[4] = "should-improve"
        lines[target] = _render(cells)
    elif variant == "free-narrative":
        lines.extend(["", "The observer should improve stage coverage."])
    elif variant == "forged-pointer":
        cells = _split(lines[target])
        cells[8] = "persistent:artifact:docs/does-not-exist.md"
        lines[target] = _render(cells)
    elif variant == "unresolvable-commit":
        cells = _split(lines[target])
        cells[8] = "persistent:commit:" + "0" * 40
        lines[target] = _render(cells)
    else:
        raise ValueError("unknown tamper variant: %s" % variant)
    return "\n".join(lines) + "\n"
