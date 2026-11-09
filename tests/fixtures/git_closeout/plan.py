"""The strategy -> authorized-action transition, and the four model sequences.

This module is the *runnable arm* of `closeout-executor.contract.md` C-8 ("the strongest
strategy value is settled by a runnable transition, not by the declaration's prose") and of
C-3 (four models, four derived sequences). It performs no git work; ``repo.run_closeout``
executes the steps it plans.

Vocabulary
----------
``Step``      one named stage of the derived sequence: ``commit`` / ``merge`` / ``push`` /
              ``branch`` / ``delete-branch``.
``CloseoutPlan`` the ordered steps, the set of steps the declared strategy *skips*, and the
              terminal state (``executed`` / ``presented``).
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Sequence

#: Model name -> the branch roles that model declares. A sequence names only its own roles.
MODEL_ROLES: dict[str, tuple[str, ...]] = {
    "single-branch": ("trunk",),
    "dual-branch": ("daily", "archive"),
    "temp-branch": ("trunk",),
    "three-tier": ("MAIN", "PRE", "DEV"),
}

#: Model name -> the model menu token the declaration cell carries (positional read of the
#: menu SKILL.md owns; this table is a *projection* of it, never a second menu).
MODEL_TOKENS: dict[str, tuple[str, ...]] = {
    "single-branch": ("单分支", "single-branch"),
    "dual-branch": ("双分支", "dual-branch"),
    "temp-branch": ("临时分支", "temp-branch", "trunk-based"),
    "three-tier": ("三层", "three-tier", "MAIN/PRE/DEV", "MAIN-PRE-DEV"),
}

#: Strategy -> the steps it forbids. `commit` is never forbidden: a read-only run never
#: reaches the close-out at all (C-5 fork 1), which is a different question.
_NOT_AUTHORIZED: dict[str, tuple[str, ...]] = {
    "commit+merge+push": (),
    "commit+merge": ("push",),
    "commit-only": ("merge", "push"),
}
_NOT_AUTHORIZED["ask"] = ("commit", "merge", "push")

_ABSENT = _NOT_AUTHORIZED["ask"]


@dataclass(frozen=True)
class Step:
    """One stage of a close-out sequence."""

    kind: str  # branch | commit | merge | delete-branch | push
    target: str  # branch name, or the remote token for a push
    detail: str = ""

    def render(self) -> str:
        if self.kind == "push":
            return f"push {self.target}"
        if self.kind == "merge":
            return f"merge into {self.target} ({self.detail})"
        if self.kind == "branch":
            return f"branch {self.target}"
        if self.kind == "delete-branch":
            return f"delete-branch {self.target}"
        return f"commit {self.target}"


@dataclass(frozen=True)
class CloseoutPlan:
    model: str
    strategy: str
    steps: tuple[Step, ...]
    skipped: tuple[str, ...]
    terminal_state: str
    targets: tuple[str, ...] = field(default_factory=tuple)
    push_branches: tuple[str, ...] = field(default_factory=tuple)
    note: str = ""
    feature_branch: str = ""

    @property
    def kinds(self) -> tuple[str, ...]:
        """The sequence's stage kinds in order — what the derivation table can be compared to."""
        return tuple(step.kind for step in self.steps)

    def render(self) -> str:
        lines = [f"model={self.model} strategy={self.strategy} terminal={self.terminal_state}"]
        for step in self.steps:
            state = "skipped (not authorized)" if step.kind in self.skipped else "run"
            lines.append(f"  [{state}] {step.render()}")
        return "\n".join(lines)


def normalize_model(cell: str) -> str | None:
    """Map a declared `Workflow model` cell onto the four-model closed set."""
    low = cell.lower()
    # order matters: "三层" never contains "单分支"; but "临时分支" contains "分支"
    for model, tokens in MODEL_TOKENS.items():
        if any(tok.lower() in low for tok in tokens):
            return model
    return None


def derive_closeout(
    *,
    model: str,
    strategy: str,
    remotes: Sequence[str],
    readonly: Sequence[str],
    trunk: str = "master",
    daily: str = "develop",
    archive: str = "archive",
    feature_branch: str = "091-fixture",
    branches_present: Sequence[str] | None = None,
    tiers: tuple[str, str, str] = ("main", "pre", "dev"),
) -> CloseoutPlan:
    """Derive the ordered sequence for one model under one strategy.

    ``remotes`` is the declared `Closeout remotes` list; ``readonly`` the block's read-only
    role marking. The push targets are ``remotes - readonly`` — exclusion is by **role**, and
    an empty result degrades the push step rather than falling back to configured remotes
    (`closeout-declaration.contract.md` C-4).
    """
    normalised = normalize_model(model) or model
    if normalised not in MODEL_ROLES:
        raise ValueError(f"unknown model {model!r}")

    targets = tuple(r for r in remotes if r not in set(readonly))
    steps: list[Step] = []
    note = ""

    if normalised == "single-branch":
        steps.append(Step("commit", trunk, "artifact + records commit"))
        steps.append(Step("push", "<remote>", "push the trunk"))
    elif normalised == "dual-branch":
        steps.append(Step("commit", daily, "artifact + records commit"))
        steps.append(Step("merge", archive, f"{daily} -> {archive}"))
        steps.append(Step("push", "<remote>", "push the daily branch, then the archive branch"))
    elif normalised == "temp-branch":
        steps.append(Step("branch", feature_branch, f"cut from {trunk}"))
        steps.append(Step("commit", feature_branch, "artifact + records commit"))
        steps.append(Step("merge", trunk, f"{feature_branch} -> {trunk}"))
        steps.append(Step("delete-branch", feature_branch, "local only, after the merge landed"))
        steps.append(Step("push", "<remote>", "push the trunk"))
    else:  # three-tier
        main, pre, dev = tiers
        steps.append(Step("commit", dev, "artifact + records commit"))
        steps.append(Step("merge", pre, f"{dev} -> {pre}"))
        steps.append(Step("merge", main, f"{pre} -> {main}"))
        steps.append(Step("push", "<remote>", f"push {dev}, {pre}, {main} in that order"))

    if normalised == "temp-branch" and branches_present is not None:
        if feature_branch in set(branches_present):
            note = "collision"

    if not targets:
        skipped = _NOT_AUTHORIZED.get(strategy, _NOT_AUTHORIZED["ask"])
        if "push" not in skipped:
            skipped = tuple(skipped) + ("push",)
            note = note or "no pushable remote"
    else:
        skipped = _NOT_AUTHORIZED.get(strategy, _NOT_AUTHORIZED["ask"])

    terminal = "presented" if skipped is _ABSENT else "executed"
    if normalised == "single-branch":
        push_branches: tuple[str, ...] = (trunk,)
    elif normalised == "dual-branch":
        push_branches = (daily, archive)
    elif normalised == "temp-branch":
        push_branches = (trunk,)
    else:
        push_branches = (tiers[2], tiers[1], tiers[0])  # DEV, PRE, MAIN
    return CloseoutPlan(
        model=normalised,
        strategy=strategy,
        steps=tuple(steps),
        skipped=tuple(skipped),
        terminal_state=terminal,
        targets=targets,
        push_branches=push_branches,
        note=note,
        feature_branch=feature_branch,
    )
