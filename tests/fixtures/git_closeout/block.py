"""The declaration read: managed block -> (model, strategy, remotes, roles).

Mirrors `closeout-declaration.contract.md` C-1/C-3/C-4/C-5 and the read rules in
`skills/external/git-utils/references/closeout-commands.md` § Reading the declaration.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Mapping

START = "<!-- GIT_WORKFLOW_START -->"
END = "<!-- GIT_WORKFLOW_END -->"

#: The closed strategy value domain, strongest first (C-1).
CLOSEOUT_VALUES = ("commit+merge+push", "commit+merge", "commit-only", "ask")

#: The Bootstrap placeholder literal that means "workflow not declared" (C-5 row 2).
PLACEHOLDER_TOKENS = ("<MODEL>", "None yet.")

_ROW = re.compile(r"^- \*\*(?P<label>[^*]+)\*\*:\s*(?P<value>.*)$")


def _row_value(block: str, label: str) -> str | None:
    for line in block.splitlines():
        m = _ROW.match(line)
        if m and m.group("label").strip().lower() == label.lower():
            return m.group("value").strip()
    return None


@dataclass(frozen=True)
class BlockState:
    """What a close-out could read out of a project's state surface.

    ``state`` is one of the three C-5 rows: ``missing`` (no file / unpaired markers),
    ``placeholder`` (model row still the Bootstrap literal) or ``declared``.
    """

    state: str
    model: str | None = None
    strategy: str = "ask"
    remotes: tuple[str, ...] = ()
    remotes_absent: bool = True
    readonly: tuple[str, ...] = field(default_factory=tuple)


def parse_block(text: str, *, remote_roles: Mapping[str, str] | None = None) -> BlockState:
    """Read a state-surface document into a :class:`BlockState`.

    ``remote_roles`` maps remote name -> ``"readonly"`` / ``"pushable"`` and is the caller's
    reading of the block's role marking; when omitted, every remote mentioned in the
    `Remote roles` row with a read-only cue is treated as read-only.
    """
    if text is None or text.count(START) != 1 or text.count(END) != 1:
        return BlockState(state="missing")
    start = text.index(START) + len(START)
    end = text.index(END)
    if start > end:
        return BlockState(state="missing")
    block = text[start:end]

    model_cell = _row_value(block, "Workflow model")
    if model_cell is None or any(tok in model_cell for tok in PLACEHOLDER_TOKENS) or not model_cell:
        return BlockState(state="placeholder")

    model = model_cell

    strategy_cell = _row_value(block, "Closeout")
    strategy = "ask"
    if strategy_cell is not None:
        spans = re.findall(r"`([^`]+)`", strategy_cell)
        for candidate in CLOSEOUT_VALUES:
            if candidate in spans:
                strategy = candidate
                break

    remotes_cell = _row_value(block, "Closeout remotes")
    remotes_absent = remotes_cell is None
    remotes: tuple[str, ...] = ()
    if remotes_cell is not None:
        spans = re.findall(r"`([^`]+)`", remotes_cell)
        if spans:
            remotes = tuple(s for s in spans if s != "-" and s not in CLOSEOUT_VALUES)
        else:
            remotes = tuple(
                part.strip().strip("`") for part in re.split(r"[,，]", remotes_cell) if part.strip()
            )
        # an explicitly empty list: a lone backticked dash, or an empty cell
        if remotes and set(remotes) <= {"-", "none", "—"}:
            remotes = ()

    if remote_roles is None:
        # the role marking is written as a ⚠ row; accept the plain label too, so the reader does
        # not silently skip a block whose marker differs only by decoration
        roles_cell = _row_value(block, "Remote roles") or _row_value(block, "⚠ Remote roles") or ""
        readonly = []
        cursor = 0
        for match in re.finditer(r"`([A-Za-z0-9._-]+)`", roles_cell):
            name = match.group(1)
            # the cue about a remote is written immediately after its own code span
            tail = roles_cell[match.end():][:160]
            if "只读" in tail or "read-only" in tail.lower() or "禁止推送" in tail:
                readonly.append(name)
            cursor = match.end()
        remote_roles = {name: "readonly" for name in readonly}
    readonly = tuple(sorted(n for n, r in (remote_roles or {}).items() if r == "readonly"))
    # A remote list is a claim about pushability, so a read-only remote demoted by role is
    # never a push target even when the declaration still lists it (C-4's role axis).
    remotes = tuple(r for r in remotes if r not in readonly)

    return BlockState(
        state="declared",
        model=model,
        strategy=strategy,
        remotes=remotes,
        remotes_absent=remotes_absent,
        readonly=readonly,
    )


def read_declaration(path: Path, *, remote_roles: Mapping[str, str] | None = None) -> BlockState:
    """Read a state file; an absent file is the ``missing`` row, not an exception."""
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return BlockState(state="missing")
    return parse_block(text, remote_roles=remote_roles)
