#!/usr/bin/env python3
"""Goal definition engine for `/speckit.goal` (requirement 037, Feature 041).

The command owns the interaction; this engine owns the deterministic parts —
identity grammar, the three-part structure, the lifecycle table, change history,
and anchoring enumeration. Fixed rules belong in a program, not in a model
(Constitution Principle XII / token-efficiency Program-First).

A Goal is composed of exactly three parts: objective narrative, zero-or-more
verifiable success criteria, and lifecycle state. Identity is the directory name;
timestamps are change-traceability metadata, never a fourth part.

Concept authority: shared/definitions/goal-definitions.md (read-only).
File contract:  .specify/specs/037-goal-registry/contracts/goal-definition.contract.md

Actions, grouped by whether they write:

Read group (zero writes):
  list
  validate        <path|slug>
  check-statement <statement>
  targets         <slug> --list | --check STATEMENT
  run-checks      <team-slug> [--target T-nnn | <goal-slug>.T-nnn]
  binding         <goal|teams> <slug>
  command-family  --command <name>      (094: family verdict from the declared class)
  handoff-decision --tasks <path>       (094: direct | handoff from the declared threshold)
  probe-residual  (094: enumerate the spec-local goal/team residuals)

Write group (mutates one definition file):
  create    <slug> --objective TEXT [--title TEXT] [--criterion TEXT ...] [--boundary TEXT ...]
  status    <slug> --set STATE
  objective <slug> --set TEXT
  criteria  <slug> --criterion TEXT ... | --clear
  targets   <slug> --add TEXT | --set STATE --id T-nnn
  migrate   <team-slug> [--keep-inline/--drop-inline]
  bind      <goal|teams> <slug> --owner V --owner-id V [--origin V]

Write group (094 unified archive; explicit actions, never implicit):
  migrate-archive   --dry-run | --apply   (move spec-local trees, archive-not-delete)
  backfill-bindings --dry-run | --apply   (insert the recorded binding on residents)
  handoff-ref       --handoff <path>      (validate a handoff contract's two keys and
                                           write the reverse handoff_ref on both
                                           definitions)

Exit codes: 0 ok | 2 input error | 3 not found or migration interrupted | 4 validation failed or migration conflict | 5 blocked
"""

from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

EXIT_OK = 0
EXIT_INPUT_ERROR = 2
EXIT_NOT_FOUND = 3
EXIT_INVALID = 4
#: 053 FR-033 — a run-precondition check judged the run blocked. The next free code: the
#: four above keep their existing meanings byte for byte, so one code never carries two
#: meanings across actions, and the 0/2 branches `templates/commands/team.md` already has
#: keep working unchanged.
EXIT_BLOCKED = 5

#: The three archive layers (owner: shared/definitions/anchor-definitions.md § Archive
#: Layers). A layer is an archive row with its own store and its own definition filename.
ARCHIVE_DIRNAME = ".specify/anchoring"
GOALS_DIRNAME = ".specify/goals"
TEAM_DIRNAME = ".specify/teams"
#: The retired spec-local layout: a migration SOURCE only, never a write target.
SPEC_GOAL_DIRNAME = "goal"
SPEC_TEAM_DIRNAME = "team"
SUMMARY_DIRNAME = "summary"

#: C-23 — layer -> definition filename. This mapping is the single source; no module-level
#: single-filename constant survives, and `definition_filename()` is its only accessor.
DEFINITION_FILENAMES = {"anchor": "anchor.md", "goals": "goal.md", "teams": "team.md"}

#: The closed archive-layer value set (C-24; owner: the Anchor owner's § Archive Layers).
#: `auto` is a read-only resolver, never a write target; the retired member `goal` does
#: not exist and has no alias.
ARCHIVE_SCOPES = ("anchor", "teams", "goals", "auto")


def definition_filename(layer: str) -> str:
    """The definition filename of one archive layer (C-23) — the only accessor."""
    try:
        return DEFINITION_FILENAMES[layer]
    except KeyError:
        raise GoalError(
            f"layer {layer!r} is outside the closed set "
            f"{' / '.join(DEFINITION_FILENAMES)}") from None

#: Resolved once per CLI invocation by `resolve_scope`; direct API callers leave it None,
#: which keeps the default archive roots for the two-archive model.
_ACTIVE_SCOPE = None


class ScopeError(Exception):
    """A scope selection that cannot be resolved; the message names the failing condition."""


class Scope:
    """The three archive-layer roots resolved for one CLI invocation.

    Each layer keeps its own root and resolves its own filename through
    `definition_filename`, so no caller — and no attribute — assumes one file name for
    every store (C-23).
    """

    __slots__ = ("scope", "repo_root", "spec_dir", "anchor_root", "goals_root",
                 "team_root")

    def __init__(self, scope: str, repo_root: Path, spec_dir: Path | None,
                 anchor_root: Path, goals_root: Path, team_root: Path):
        self.scope = scope
        self.repo_root = Path(repo_root)
        self.spec_dir = spec_dir
        self.anchor_root = Path(anchor_root)
        self.goals_root = Path(goals_root)
        self.team_root = Path(team_root)

    def anchor_definition(self, slug: str) -> Path:
        return self.anchor_root / slug / definition_filename("anchor")

    def goal_definition(self, slug: str) -> Path:
        return self.goals_root / slug / definition_filename("goals")

    def team_definition(self, slug: str) -> Path:
        # The single default team of a spec lives at `<team-root>/team.md`; only an
        # ADDITIONAL named team nests under `<team-root>/<team-slug>/`. Nesting the default
        # team under its own spec slug duplicates the slug in the path.
        default = self.team_root / "team.md"
        if default.is_file():
            return default
        return self.team_root / slug / "team.md"

    def as_dict(self, slug: str | None = None) -> dict:
        row = {
            "scope": self.scope,
            "spec_dir": str(self.spec_dir) if self.spec_dir else None,
            "anchor_root": str(self.anchor_root),
            "goals_root": str(self.goals_root),
            "team_root": str(self.team_root),
        }
        if slug:
            row["anchor_definition"] = str(self.anchor_definition(slug))
            row["goal_definition"] = str(self.goal_definition(slug))
            row["team_definition"] = str(self.team_definition(slug))
        return row


def _has_any_definition(root: Path, layer: str) -> bool:
    if not root.is_dir():
        return False
    filename = definition_filename(layer)
    return any(child.is_dir() and (child / filename).is_file()
               for child in root.iterdir())


def _anchor_layer_contains(root: Path, slug: str | None = None) -> bool:
    """Anchor-layer membership by either filename: before its cleanup renames it, a
    retained Anchor of the archive still lives as `goal.md` (it is still THIS layer)."""
    if not root.is_dir():
        return False
    names = (definition_filename("anchor"), "goal.md")
    if slug:
        return any((root / slug / name).is_file() for name in names)
    return any(child.is_dir() and any((child / name).is_file() for name in names)
               for child in root.iterdir())


def _has_team(root: Path, slug: str | None) -> bool:
    if not root.is_dir():
        return False
    if (root / "team.md").is_file():
        return True
    if slug:
        return (root / slug / "team.md").is_file()
    return any(child.is_dir() and (child / "team.md").is_file()
               for child in root.iterdir())


def resolve_scope(repo_root: Path, scope: str = "anchor",
                  spec_dir: str | os.PathLike | None = None,
                  identity_slug: str | None = None) -> Scope:
    """Resolve the three archive-layer roots. The path rule has exactly one owner: this function.

    `scope` is the closed archive-layer set `anchor` / `teams` / `goals` / `auto` (C-24).
    The three layer members always return ALL roots in one `Scope` object, so a caller
    never needs two calls; `auto` is a read-only resolver that picks the single layer
    containing the requested identity (or the single non-empty layer when no identity is
    requested) and refuses — exit 2, no guessing — when that is not decidable.
    """
    repo_root = Path(repo_root)
    anchor_path = repo_root / ARCHIVE_DIRNAME
    goals_path = repo_root / GOALS_DIRNAME
    team_path = repo_root / TEAM_DIRNAME
    if scope not in ARCHIVE_SCOPES:
        raise ScopeError(
            f"scope {scope!r} is outside the closed set {' / '.join(ARCHIVE_SCOPES)}")

    resolved_spec = _resolve_spec_dir(repo_root, spec_dir)
    if scope in ARCHIVE_SCOPES and scope != "auto":
        return Scope(scope, repo_root, resolved_spec, anchor_path, goals_path, team_path)

    # `auto` (C-25): ONE candidate layer or a named refusal. Never writes.
    candidates: list[str] = []
    if identity_slug:
        if _anchor_layer_contains(anchor_path, identity_slug):
            candidates.append("anchor")
        if (goals_path / identity_slug / definition_filename("goals")).is_file():
            candidates.append("goals")
        if _team_layer_contains(team_path, identity_slug):
            candidates.append("teams")
    else:
        if _anchor_layer_contains(anchor_path):
            candidates.append("anchor")
        if _has_any_definition(goals_path, "goals"):
            candidates.append("goals")
        if _has_team(team_path, None):
            candidates.append("teams")
    if not candidates:
        subject = f"slug {identity_slug!r}" if identity_slug else "any definition"
        raise ScopeError(
            f"not-found: no archive layer contains {subject} "
            f"(checked {ARCHIVE_DIRNAME}, {GOALS_DIRNAME} and {TEAM_DIRNAME})")
    if len(candidates) > 1:
        raise ScopeError(
            "scope-ambiguous: more than one archive layer contains the requested "
            f"identity ({', '.join(candidates)}); name the layer with --scope "
            + " or --scope ".join(("anchor", "teams", "goals")))
    return Scope(candidates[0], repo_root, resolved_spec, anchor_path, goals_path, team_path)


def _resolve_spec_dir(repo_root: Path,
                      spec_dir: str | os.PathLike | None) -> Path | None:
    """`--spec-dir` is accepted for `origin` resolution and `auto` input validity only
    (C-12); it never decides where a definition lands. Outside `.specify/specs/` is a
    named refusal."""
    if spec_dir:
        candidate = Path(spec_dir)
        if not candidate.is_absolute():
            candidate = repo_root / candidate
        candidate = candidate.resolve()
        try:
            candidate.relative_to((repo_root / ".specify" / "specs").resolve())
        except ValueError as exc:
            raise ScopeError(
                f"spec-dir-unresolvable: --spec-dir must name a directory under "
                f".specify/specs/: {candidate}") from exc
        return candidate
    if os.environ.get("SPECIFY_FEATURE"):
        candidate = repo_root / ".specify" / "specs" / os.environ["SPECIFY_FEATURE"]
        if candidate.is_dir():
            return candidate.resolve()
    return None


def _team_layer_contains(team_root_path: Path, slug: str) -> bool:
    """Does the team archive row contain a definition with this slug?"""
    if (team_root_path / slug / "team.md").is_file():
        return True
    default = team_root_path / "team.md"
    if not default.is_file():
        return False
    meta, _start, _end = read_frontmatter_subset(
        default.read_text(encoding="utf-8"))
    declared = str(meta.get("team_slug") or meta.get("slug") or "").strip()
    return not declared or declared == slug

#: Exactly three, per the concept authority. `superseded` is deliberately absent.
LIFECYCLE_STATES = ("active", "achieved", "abandoned")
TERMINAL_STATES = ("achieved", "abandoned")

#: FR-003 — the same grammar the summary generator enforces; no second mechanism.
_IDENTITY = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.\-]*$")

NO_CRITERIA_MARKER = "None provided."

_SECTION_OBJECTIVE = "## Objective"
_SECTION_CRITERIA = "## Success Criteria"
_SECTION_BOUNDARIES = "## Boundaries"
_SECTION_HISTORY = "## History"
_SECTION_TARGETS = "## Targets"

_TITLE_LINE = re.compile(r"^#\s+Goal:\s*(.+?)\s*$", re.M)

#: Target (038): run-assignable scope slices under a goal. [[STR-002]] three states.
TARGET_STATES = ("open", "done", "dropped")
TARGET_IDENTITY = re.compile(r"^T-\d{3}$")
_TARGET_ROW = re.compile(r"^\| (T-\d{3}) \| (.+) \| (open|done|dropped) \|$")
_TARGETS_HEADER = "| ID | Target | Status |"
_TARGETS_SEPARATOR = "|----|--------|--------|"

#: Legal Target lifecycle moves (FR-006); terminal→terminal is deliberately absent.
TARGET_LEGAL_TRANSITIONS = {
    ("open", "done"),
    ("open", "dropped"),
    ("done", "open"),
    ("dropped", "open"),
}

#: GD-2 — an objective states an outcome. Numbered/bulleted steps are a task list.
_TASKLIST = re.compile(r"(?m)^\s*(?:\d+[.)]\s+|[-*+]\s+)")
_STEP_VERBS = ("首先", "然后", "接着", "step 1", "then ", "next, ")

#: GD-2 — phased wording is a plan's timeline wearing an outcome's clothes. Ordinal-
#: qualified on purpose: a bare 阶段/phase is ordinary domain vocabulary, so matching
#: it would reject legitimate objectives (and every `migrate` of an inline goal).
_PHASED = re.compile(
    r"分阶段|阶段\s*[一二三四五六七八九十\d]|第\s*[一二三四五六七八九十\d]+\s*(?:阶段|步)"
    r"|phase\s*\d|stage\s*\d",
    re.IGNORECASE,
)

#: What `targets <slug> --check` judges. Declared on every verdict so a green is never
#: read as broader than it is; `check-statement`'s narrower "shape-only" is the sibling.
TARGET_CHECK_SCOPE = "shape+criteria-restatement"

#: GD-3 — one goal, one objective. Conjunctions joining independent clauses.
_COMPOSITE = re.compile(
    r"\b(?:and also|and additionally|as well as|;\s*also)\b|并且还|同时还|以及另外",
    re.IGNORECASE,
)


class GoalError(Exception):
    """Raised for any rejection the contract defines."""


class GoalNotFound(GoalError):
    """Raised when a referenced target identity does not exist (exit code 3)."""


class GoalInvalid(GoalError):
    """Raised when a definition exists but cannot be interpreted (exit code 4).

    Kept distinct from GoalNotFound and from a bad argument so that the three tiers 053's
    run-checks contract requires — blocked / input error / definition unusable — stay
    mutually distinguishable instead of collapsing onto one code.
    """


#: STR-004 (053 FR-032) — a check whose precondition does not hold, or which raised, is
#: reported as NOT evaluated. Never `ok`: a check that did not run must not report green,
#: which is the exact shape this feature exists to remove. Single definition point.
NOT_EVALUATED = "not-evaluated"

#: The five run-precondition checks, in reporting order (053 FR-029). `name` says which
#: check ran; `verdict` says what it concluded. Four of these five names are ALSO verdict
#: literals below in preview_target_check — an accident of vocabulary, not an invariant, so
#: nothing may rely on the two fields being interchangeable (053 C-10).
RUN_CHECK_NAMES = (
    "goal-binding", "dangling", "target-terminal", "cross-goal", "goal-terminal",
)

#: Verdicts that stop a run. `input-error` is deliberately absent: a malformed argument is
#: the input tier (exit 2), not a block (exit 5).
BLOCKING_VERDICTS = frozenset({
    "no-goal-definition", "dangling", "target-terminal", "cross-goal", "goal-terminal",
})

#: preview_target_check's own evaluation order, as check ids: binding, then the reference
#: grammar, then cross-goal, goal-terminal, dangling, target-terminal. The top-level verdict
#: is the first non-ok in THIS order, which is what makes the five-check array a faithful
#: projection of the authoritative gate rather than a second opinion beside it.
_TOP_VERDICT_ORDER = (1, 4, 5, 2, 3)


# --------------------------------------------------------------------------
# identity
# --------------------------------------------------------------------------

def is_valid_identity(slug: str) -> bool:
    """Grammar plus path-segment safety."""
    if not slug or slug in (".", ".."):
        return False
    if "/" in slug or "\\" in slug:
        return False
    return bool(_IDENTITY.match(slug))


def layer_root(repo_root: Path, layer: str = "anchor") -> Path:
    """One archive layer's root, honouring the resolved scope when a CLI invocation set it."""
    if layer not in DEFINITION_FILENAMES:
        raise GoalError(
            f"layer {layer!r} is outside the closed set "
            f"{' / '.join(DEFINITION_FILENAMES)}")
    if _ACTIVE_SCOPE is not None:
        return Path(getattr(_ACTIVE_SCOPE, {"anchor": "anchor_root",
                                            "goals": "goals_root",
                                            "teams": "team_root"}[layer]))
    return Path(repo_root) / {"anchor": ARCHIVE_DIRNAME, "goals": GOALS_DIRNAME,
                              "teams": TEAM_DIRNAME}[layer]


def anchor_root(repo_root: Path) -> Path:
    """The anchoring archive root (`.specify/anchoring/`)."""
    return layer_root(repo_root, "anchor")


def goals_root(repo_root: Path) -> Path:
    """The action-level Goal archive root (`.specify/goals/`)."""
    return layer_root(repo_root, "goals")


def team_root(repo_root: Path) -> Path:
    return layer_root(repo_root, "teams")


def definition_path(repo_root: Path, slug: str, layer: str = "anchor") -> Path:
    return layer_root(repo_root, layer) / slug / definition_filename(layer)


def summary_dir(repo_root: Path, slug: str, layer: str = "anchor") -> Path:
    """The derived subtree — the only surface a refresh may write. Layer-aware (C-23)."""
    return definition_path(repo_root, slug, layer).parent / SUMMARY_DIRNAME


# --------------------------------------------------------------------------
# binding record (094, contracts/binding-and-lifecycle.md C-1…C-8)
# --------------------------------------------------------------------------

#: C-2 — the closed owner domain: exactly these three values.
OWNER_VALUES = ("sdd-run", "command-run", "human")

#: C-1 — exactly these three keys under `binding`, no fourth.
BINDING_KEYS = ("owner", "owner_id", "origin")
BINDING_MARKER = "binding:"

#: C-3 — shape only. The grammar is owned by the state spine; this file cites that
#: owner and never re-declares it as a second schema.
RUN_ID_SHAPE = re.compile(r"^r\d{8}T\d{6}Z-[A-Za-z0-9][A-Za-z0-9_.\-]*$")
STATE_SPINE_GRAMMAR_OWNER = "skills/external/sdd-loop-driver/references/state-awareness.md"

#: R-06 — the closed frontmatter subset: `key: value` scalars (null / bool / int /
#: string), inline lists, and one nested mapping level. Nothing else is guessed.
_SUBSET_INT = re.compile(r"^-?\d+$")


def _parse_subset_scalar(raw: str):
    text = raw.strip()
    if text == "" or text in ("null", "~", "Null", "NULL"):
        return None
    if text in ("true", "false"):
        return text == "true"
    if _SUBSET_INT.match(text):
        return int(text)
    if text.startswith("[") and text.endswith("]"):
        inner = text[1:-1].strip()
        return [] if not inner else [_parse_subset_scalar(part) for part in inner.split(",")]
    if len(text) >= 2 and text[0] == text[-1] and text[0] in "\"'":
        return text[1:-1]
    return text


def read_frontmatter_subset(text: str) -> tuple[dict, int, int]:
    """Read a definition's frontmatter under the closed subset (R-06).

    Returns `(meta, start, end)`; `start`/`end` are the line indexes of the frontmatter
    content (`---` lines excluded). An absent frontmatter returns `({}, 0, 0)`.
    """
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, 0, 0
    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration:
        return {}, 0, 0
    meta: dict = {}
    i = 1
    while i < end:
        line = lines[i]
        if not line.strip() or line[:1] in (" ", "\t"):
            i += 1
            continue
        key, sep, raw = line.partition(":")
        if not sep:
            i += 1
            continue
        key = key.strip()
        if not raw.strip() and i + 1 < end and lines[i + 1][:1] in (" ", "\t"):
            nested = {}
            j = i + 1
            while j < end and lines[j][:1] in (" ", "\t"):
                nkey, nsep, nraw = lines[j].strip().partition(":")
                if nsep:
                    nested[nkey.strip()] = _parse_subset_scalar(nraw)
                j += 1
            meta[key] = nested
            i = j
            continue
        meta[key] = _parse_subset_scalar(raw)
        i += 1
    return meta, 1, end


def _binding_block_lines(text: str) -> tuple[int | None, list[str], int]:
    """The raw `binding:` block: (start line index, block lines, occurrence count)."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None, [], 0
    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration:
        return None, [], 0
    starts = [i for i in range(1, end) if lines[i].startswith(BINDING_MARKER)]
    if not starts:
        return None, [], 0
    start = starts[0]
    block = [lines[start]]
    j = start + 1
    while j < end and lines[j][:1] in (" ", "\t"):
        block.append(lines[j])
        j += 1
    return start, block, len(starts)


def _render_binding_block(binding: dict) -> str:
    origin = "null" if binding["origin"] is None else binding["origin"]
    return (f"{BINDING_MARKER}\n"
            f"  owner: {binding['owner']}\n"
            f"  owner_id: {binding['owner_id']}\n"
            f"  origin: {origin}\n")


def read_binding(path: Path) -> dict:
    """Read and validate one definition's complete binding record (C-1…C-5).

    A definition without a complete block is uninterpretable (`binding-missing`); a block
    that is not byte-identical to the engine's canonical rendering is reported as
    `binding-hand-edited` rather than trusted — the engine is the only writer (FR-003).
    """
    path = Path(path)
    text = path.read_text(encoding="utf-8")
    start, block, occurrences = _binding_block_lines(text)
    if start is None:
        raise GoalError(
            f"binding-missing: {path} carries no binding block; a definition without a "
            "complete binding record is uninterpretable (owner / owner_id / origin)")
    parsed: dict = {}
    for line in block[1:]:
        key, sep, raw = line.strip().partition(":")
        if sep:
            parsed[key.strip()] = raw.strip()
    missing = [key for key in BINDING_KEYS if key not in parsed]
    if missing:
        raise GoalError(
            f"binding-missing: {path} is missing the binding key(s) "
            f"{', '.join(missing)}; exactly owner / owner_id / origin are required")
    origin_raw = parsed["origin"]
    binding = {
        "owner": parsed["owner"],
        "owner_id": parsed["owner_id"],
        "origin": None if origin_raw in ("null", "~") else origin_raw,
    }
    canonical = _render_binding_block(binding).splitlines()
    if occurrences != 1 or block != canonical:
        raise GoalError(
            f"binding-hand-edited: the binding block in {path} is not in the "
            "engine-written canonical form; the binding is written only by this engine, "
            "never by a template, skill or driver")
    return binding


def _validate_binding_values(repo_root: Path, owner: str, owner_id: str,
                             origin: str | None) -> None:
    """C-2 / C-3 / C-4 — validate candidate values before anything is written."""
    if owner not in OWNER_VALUES:
        raise GoalError(
            f"owner {owner!r} is outside the closed set {' / '.join(OWNER_VALUES)}")
    if owner_id == "human":
        if owner != "human":
            raise GoalError(
                f"owner_id 'human' is reserved for owner: human; {owner!r} requires a "
                "state-spine run_id")
    elif not RUN_ID_SHAPE.match(owner_id or ""):
        raise GoalError(
            f"owner_id {owner_id!r} does not match the state-spine run_id shape "
            "r<YYYYMMDD>T<HHMMSS>Z-<slice-token>; the grammar is owned by "
            f"{STATE_SPINE_GRAMMAR_OWNER} and is not re-declared here")
    if origin is not None:
        if (not origin or origin in (".", "..") or "/" in origin or "\\" in origin):
            raise GoalError(
                f"origin-unresolvable: origin {origin!r} is not a spec directory basename")
        if not (Path(repo_root) / ".specify" / "specs" / origin).is_dir():
            raise GoalError(
                f"origin-unresolvable: origin {origin!r} names no directory under "
                ".specify/specs/; an unresolvable origin is never auto-created")


def bound_team_slugs(repo_root: Path, goal_slug: str) -> list[str]:
    """Every team in the team archive row whose `goal_slug` names this goal (C-14)."""
    root = Path(repo_root) / TEAM_DIRNAME
    if not root.is_dir():
        return []
    candidates: list[tuple[str, Path]] = []
    default = root / "team.md"
    if default.is_file():
        candidates.append(("team", default))
    for child in sorted(root.iterdir()):
        if child.is_dir() and (child / "team.md").is_file():
            candidates.append((child.name, child / "team.md"))
    rows: list[str] = []
    for slug, path in candidates:
        meta, _start, _end = read_frontmatter_subset(path.read_text(encoding="utf-8"))
        if str(meta.get("goal_slug") or "").strip() == goal_slug:
            rows.append(slug)
    return rows


def writable(kind: str, binding: dict, bound_teams: list[str]) -> tuple[bool, str | None]:
    """C-14 — writability is computed, never declared (FR-038)."""
    if kind == "teams":
        return True, None
    if binding.get("owner") == "human":
        return True, None
    if bound_teams:
        return False, "bound-by:" + ",".join(bound_teams)
    return True, None


def _path_for_kind(repo_root: Path, kind: str, slug: str) -> Path:
    if kind == "goal":
        return definition_path(repo_root, slug)
    if kind == "teams":
        root = team_root(repo_root)
        default = root / "team.md"
        if default.is_file():
            return default
        return root / slug / "team.md"
    raise GoalError(f"kind {kind!r} is outside the closed set goal / teams")


def _lifecycle_for_kind(path: Path, kind: str) -> str:
    meta, _start, _end = read_frontmatter_subset(path.read_text(encoding="utf-8"))
    key = "status" if kind == "goal" else "lifecycle_state"
    return str(meta.get(key) or "")


def bind_definition(repo_root: Path, kind: str, slug: str, owner: str,
                    owner_id: str, origin: str | None,
                    origin_given: bool) -> tuple[Path, dict]:
    """C-6 — rewrite the binding record; every other byte stays identical."""
    path = _path_for_kind(repo_root, kind, slug)
    if not path.is_file():
        raise GoalNotFound(f"{kind} definition not found: {slug} ({path})")
    current = read_binding(path)
    lifecycle = _lifecycle_for_kind(path, kind)
    if kind == "goal" and lifecycle in TERMINAL_STATES:
        raise GoalError(
            f"terminal-goal-rebind: goal {slug!r} is in terminal state {lifecycle!r} "
            "and refuses a new binding; reopening is an explicit lifecycle action")
    if kind == "teams" and lifecycle == "archived":
        raise GoalError(
            f"terminal-team-rebind: team {slug!r} is archived ({lifecycle!r}); an "
            "archived team refuses any binding rewrite")
    if not origin_given:
        origin = current["origin"]
    _validate_binding_values(repo_root, owner, owner_id, origin)
    new_binding = {"owner": owner, "owner_id": owner_id, "origin": origin}
    if kind == "goal":
        allowed, reason = writable(kind, new_binding, bound_team_slugs(repo_root, slug))
        if not allowed:
            teams = (reason or "").split(":", 1)[-1]
            raise GoalError(
                f"{reason}: goal {slug!r} is bound by team(s) {teams} in the team "
                "archive row; only owner: human may rewrite a bound goal (FR-038)")
    text = path.read_text(encoding="utf-8")
    start, block, _occurrences = _binding_block_lines(text)
    new_block = _render_binding_block(new_binding).splitlines()
    rewritten = text.splitlines()[:start] + new_block + text.splitlines()[start + len(block):]
    new_text = "\n".join(rewritten)
    if text.endswith("\n"):
        new_text += "\n"
    path.write_text(new_text, encoding="utf-8")
    return path, new_binding


def binding_payload(repo_root: Path, kind: str, slug: str) -> dict:
    """C-8 — answer ownership from the record, never from the filesystem layout."""
    path = _path_for_kind(repo_root, kind, slug)
    if not path.is_file():
        raise GoalNotFound(f"{kind} definition not found: {slug} ({path})")
    binding = read_binding(path)
    try:
        shown = path.relative_to(repo_root).as_posix()
    except ValueError:
        shown = str(path)
    return {
        "kind": kind,
        "slug": slug,
        "owner": binding["owner"],
        "owner_id": binding["owner_id"],
        "origin": binding["origin"],
        "path": shown,
        "archive_layer": kind,
        "lifecycle": _lifecycle_for_kind(path, kind),
    }


# --------------------------------------------------------------------------
# lifecycle
# --------------------------------------------------------------------------

def transition_allowed(current: str, target: str) -> bool:
    if current not in LIFECYCLE_STATES or target not in LIFECYCLE_STATES:
        return False
    if current == target:
        return True
    return current == "active" and target in TERMINAL_STATES


def target_transition_allowed(current: str, target: str) -> bool:
    """Target lifecycle (FR-006): exactly the four moves in the legal set."""
    if current not in TARGET_STATES or target not in TARGET_STATES:
        return False
    return (current, target) in TARGET_LEGAL_TRANSITIONS


# --------------------------------------------------------------------------
# objective shape
# --------------------------------------------------------------------------

def _bad_shape(text: str) -> str | None:
    """Shared GD-2/GD-3 detection — one grammar for objectives and target slices."""
    if (_TASKLIST.search(text) or _PHASED.search(text)
            or any(v in text.lower() for v in _STEP_VERBS)):
        return "GD-2"
    if _COMPOSITE.search(text):
        return "GD-3"
    return None


def _reject_bad_objective(objective: str) -> None:
    text = objective.strip()
    if not text:
        raise GoalError("objective is empty; a goal MUST state a desired outcome")
    kind = _bad_shape(text)
    if kind == "GD-2":
        raise GoalError(
            "GD-2 violation: the objective reads as a task list or plan. State the "
            "desired end outcome instead of the steps to reach it."
        )
    if kind == "GD-3":
        raise GoalError(
            "GD-3 violation: the objective bundles more than one objective. Split it "
            "into separate goal identities, each with its own directory and lifecycle."
        )


def _reject_bad_target_statement(statement: str) -> None:
    """Same-source GD-2/GD-3 detection at slice scale (FR-003, SC-003)."""
    text = statement.strip()
    if not text:
        raise GoalError("target statement is empty; a slice MUST state a sub-outcome")
    kind = _bad_shape(text)
    if kind == "GD-2":
        raise GoalError(
            "GD-2 violation: the target reads as a task list or steps. Rewrite it as a "
            "sub-outcome direction — what holds when the slice is done, not how to get there."
        )
    if kind == "GD-3":
        raise GoalError(
            "GD-3 violation: the target bundles more than one sub-outcome. Split it so "
            "each slice is independently judgeable — one slice, one sub-outcome."
        )


def _normalize(text: str) -> str:
    """D5 normalization: lowercase, keep only letters/digits/CJK."""
    return re.sub(r"[^0-9a-z\u4e00-\u9fff]+", "", text.lower())


# --------------------------------------------------------------------------
# targets data layer (038)
# --------------------------------------------------------------------------

def _next_target_id(targets: list[dict]) -> str:
    """Monotone max+1; terminal identities are never reused (FR-005)."""
    highest = 0
    for row in targets:
        match = TARGET_IDENTITY.match(row["id"])
        if match:
            highest = max(highest, int(row["id"][2:]))
    return f"T-{highest + 1:03d}"


def _render_targets_table(targets: list[dict]) -> str:
    """D3 grammar: fixed header, rows sorted by ID ascending."""
    rows = [f"| {t['id']} | {t['statement']} | {t['status']} |"
            for t in sorted(targets, key=lambda t: t["id"])]
    return "\n".join([_TARGETS_HEADER, _TARGETS_SEPARATOR] + rows)


def _parse_targets_text(text: str) -> list[dict]:
    """Parse the table body; rows not matching the grammar are skipped here —
    validate_goal is the surface that flags them."""
    targets: list[dict] = []
    for line in (text or "").splitlines():
        match = _TARGET_ROW.match(line.strip())
        if match:
            targets.append({"id": match.group(1), "statement": match.group(2),
                            "status": match.group(3)})
    return targets


# --------------------------------------------------------------------------
# read / write
# --------------------------------------------------------------------------

def _today() -> str:
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%d")


def _render(objective: str, criteria: list[str], status: str, created: str,
            updated: str, history: list[str], title: str,
            targets: list[dict] | None = None,
            boundaries: list[str] | None = None,
            binding_lines: list[str] | None = None) -> str:
    if criteria:
        body = "\n".join(f"{i}. {c}" for i, c in enumerate(criteria, 1))
    else:
        body = NO_CRITERIA_MARKER
    hist = "\n".join(history)
    # Section absent entirely when the goal has no boundaries / no targets
    # (SC-002: byte-identical to the pre-annex rendering).
    boundaries_block = (f"{_SECTION_BOUNDARIES}\n\n"
                        + "\n".join(f"- {b}" for b in boundaries) + "\n\n"
                        if boundaries else "")
    targets_block = (f"{_SECTION_TARGETS}\n\n{_render_targets_table(targets)}\n\n"
                     if targets else "")
    # C-20 — a lifecycle/objective/criteria/targets write never touches the binding
    # block: it is carried through byte for byte (C-6's byte rule).
    frontmatter = f"status: {status}\ncreated: {created}\nupdated: {updated}\n"
    if binding_lines:
        frontmatter += "\n".join(binding_lines) + "\n"
    return (
        f"---\n{frontmatter}---\n\n"
        f"# Goal: {title}\n\n"
        f"{_SECTION_OBJECTIVE}\n\n{objective.strip()}\n\n"
        f"{_SECTION_CRITERIA}\n\n{body}\n\n"
        f"{boundaries_block}"
        f"{targets_block}"
        f"{_SECTION_HISTORY}\n\n{hist}\n"
    )


def _atomic_write_text(path: Path, text: str) -> None:
    """One replace, so a definition is never observed half-written."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    os.replace(tmp, path)


def _frontmatter_span(text: str) -> tuple[str, str]:
    """Split the `---…---` block from the body, preserving the block's bytes."""
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        return "", text
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            return "".join(lines[:index + 1]), "".join(lines[index + 1:])
    return "", text


def _split_frontmatter(text: str) -> tuple[dict, str]:
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    meta = {}
    for line in parts[1].strip().splitlines():
        if ":" in line:
            k, _, v = line.partition(":")
            meta[k.strip()] = v.strip()
    return meta, parts[2]


def _section(body: str, heading: str) -> str:
    lines = body.split("\n")
    out: list[str] = []
    inside = False
    for line in lines:
        if line.strip() == heading:
            inside = True
            continue
        if inside and line.startswith("## "):
            break
        if inside:
            out.append(line)
    return "\n".join(out).strip()


def _parse_bullets(raw: str) -> list[str]:
    """Parse a `- ` bullet annex; blank lines carry no entry."""
    out: list[str] = []
    for line in (raw or "").splitlines():
        stripped = re.sub(r"^\s*[-*+]\s*", "", line).strip()
        if stripped:
            out.append(stripped)
    return out


def _title_from_body(body: str) -> str:
    match = _TITLE_LINE.search(body)
    return match.group(1).strip() if match else ""


#: 053 FR-035 — the criterion-subject reference form. Single definition point; the literal
#: itself is owned by shared/definitions/goal-definitions.md § 判据主体指代形 (Criterion
#: Subject Reference), which also states the two failure tiers and the conflict rule below.
SUBJECT_REF = re.compile(r"\[subjects:\s*([^\]]+)\]")
#: The only machine-decidable member-enumeration marker: a brace expansion holding a comma.
#: A PROSE enumeration ("所有绘图技能") carries no marker at all and is therefore NOT
#: detected — the owner document states that boundary explicitly instead of claiming
#: coverage it does not have, which is what the artifact/behavior clause split forbids.
BRACE_ENUM = re.compile(r"\{[^}]*,[^}]*\}")

#: STR-010 and its two siblings. Distinct prefixes, because "the path is not there" and
#: "the path is there and matches nothing" have opposite remedies; both exit 4, so the
#: prefix is what tells them apart.
SUBJECT_PROBLEM_PREFIXES = {
    "missing": "SUBJECT MISSING:",
    "empty": "SUBJECT EMPTY:",
    "conflict": "SUBJECT CONFLICT:",
}
#: Closed state vocabulary of derive_subjects. `absent` is the state every pre-existing
#: pure-enumeration criterion stays in, which is what keeps their parse byte-identical.
SUBJECT_STATES = ("absent", "ok", "missing", "empty", "conflict")

_WILDCARD_CHARS = "*?["


def _repo_root_for(path: Path) -> Path:
    """The repository root a definition path lives under, or the cwd if none does."""
    for parent in Path(path).resolve().parents:
        if (parent / ".specify").is_dir():
            return parent
    return Path.cwd()


def _glob_literal_prefix(pattern: str, repo_root: Path) -> Path:
    """The leading wildcard-free part of a glob — what "the path does not exist" means."""
    segments = []
    for segment in pattern.replace("\\", "/").split("/"):
        if any(ch in segment for ch in _WILDCARD_CHARS):
            break
        segments.append(segment)
    return repo_root.joinpath(*segments) if segments else repo_root


def derive_subjects(criterion: str, repo_root: Path) -> dict:
    """The subject set one criterion's reference form derives to, at parse time.

    Returns {"glob", "paths", "state"} with state in SUBJECT_STATES. Deriving the set here
    rather than trusting members retyped into the criterion text is the whole point: a
    derived set cannot go stale, which is the churn this repository's own goal History shows
    (the same criterion rewritten from six skills to seven and back as the directory moved).

    An empty derivation is NOT a pass — "every one of zero subjects satisfies this" is
    vacuously true — so it is reported, and separately from a glob whose literal prefix does
    not exist, because the two have opposite remedies.
    """
    repo_root = Path(repo_root)
    matches = SUBJECT_REF.findall(criterion)
    if not matches:
        return {"glob": None, "paths": [], "state": "absent"}
    pattern = matches[0].strip()
    if len(matches) > 1 or BRACE_ENUM.search(criterion):
        return {"glob": pattern, "paths": [], "state": "conflict"}
    if not _glob_literal_prefix(pattern, repo_root).exists():
        return {"glob": pattern, "paths": [], "state": "missing"}
    paths = sorted({p.relative_to(repo_root).as_posix() for p in repo_root.glob(pattern)})
    return {"glob": pattern, "paths": paths, "state": "ok" if paths else "empty"}


def _subject_problems(criteria: list, repo_root: Path) -> list:
    problems = []
    for index, criterion in enumerate(criteria, start=1):
        derived = derive_subjects(criterion, repo_root)
        state = derived["state"]
        if state == "absent" or state == "ok":
            continue
        glob = f"[subjects: {derived['glob']}]"
        if state == "conflict":
            problems.append(
                f"{SUBJECT_PROBLEM_PREFIXES['conflict']} criterion {index} carries both the "
                f"reference form {glob} and a brace-expanded member list — one subject set "
                "must have one source, so drop the retyped members or drop the reference")
        elif state == "missing":
            problems.append(
                f"{SUBJECT_PROBLEM_PREFIXES['missing']} criterion {index} references {glob}, "
                "whose literal prefix does not exist in the repository — a reference that "
                "denotes nothing is not the same fact as one denoting an empty set; fix the "
                "glob or restore the directory")
        elif state == "empty":
            problems.append(
                f"{SUBJECT_PROBLEM_PREFIXES['empty']} criterion {index} references {glob}, "
                "which exists but matches nothing — an empty subject set would make 'every "
                "subject satisfies this' vacuously true; widen the glob or populate the "
                "directory")
    return problems


def parse_goal(path: Path) -> dict:
    text = Path(path).read_text(encoding="utf-8")
    meta, body = _split_frontmatter(text)
    raw_criteria = _section(body, _SECTION_CRITERIA)
    criteria: list[str] = []
    if raw_criteria and raw_criteria.strip() != NO_CRITERIA_MARKER:
        for line in raw_criteria.splitlines():
            stripped = re.sub(r"^\s*(?:\d+[.)]|[-*+])\s*", "", line).strip()
            if stripped:
                criteria.append(stripped)
    return {
        "slug": Path(path).parent.name,
        # Parsed back so an unrelated write never downgrades a --title to the slug.
        "title": _title_from_body(body) or Path(path).parent.name,
        "status": meta.get("status", ""),
        "created": meta.get("created", ""),
        "updated": meta.get("updated", ""),
        "objective": _section(body, _SECTION_OBJECTIVE),
        "criteria": criteria,
        "history": _section(body, _SECTION_HISTORY),
        "criteria_count": len(criteria),
        "boundaries": _parse_bullets(_section(body, _SECTION_BOUNDARIES)),
        "targets": _parse_targets_text(_section(body, _SECTION_TARGETS)),
        # C-20: the raw binding block travels with the parsed data so any write that
        # re-renders the definition preserves it byte for byte.
        "binding_block": _binding_block_lines(text)[1],
        # 053 FR-035: subject sets derived at parse time, one entry per criterion that
        # carries a reference form. A pure-enumeration criterion derives nothing, so this
        # list is empty for every definition that predates the form.
        "subjects": [
            derived for derived in
            (derive_subjects(c, _repo_root_for(path)) for c in criteria)
            if derived["state"] != "absent"
        ],
    }


def validate_goal(path: Path, repo_root: Path | None = None) -> tuple[bool, list[str]]:
    path = Path(path)
    problems: list[str] = []
    if not path.is_file():
        return False, [f"definition not found: {path}"]
    text = path.read_text(encoding="utf-8")
    meta, body = _split_frontmatter(text)

    slug = path.parent.name
    if not is_valid_identity(slug):
        problems.append(f"identity {slug!r} violates the grammar or path-safety rule")

    status = meta.get("status", "")
    if status not in LIFECYCLE_STATES:
        problems.append(
            f"status {status!r} is outside the valid set {LIFECYCLE_STATES}"
        )
    for field in ("created", "updated"):
        if not meta.get(field):
            problems.append(f"frontmatter is missing {field}")

    for heading in (_SECTION_OBJECTIVE, _SECTION_CRITERIA, _SECTION_HISTORY):
        if heading not in body:
            problems.append(f"required section missing: {heading}")

    if _SECTION_OBJECTIVE in body and not _section(body, _SECTION_OBJECTIVE):
        problems.append("## Objective is empty")

    if _SECTION_CRITERIA in body:
        raw = _section(body, _SECTION_CRITERIA)
        if not raw:
            problems.append(
                "## Success Criteria is empty; an empty set requires the explicit "
                f"{NO_CRITERIA_MARKER!r} marker"
            )

    if _SECTION_TARGETS in body:
        problems.extend(_validate_targets_section(_section(body, _SECTION_TARGETS)))

    # 053 FR-035/FR-036: the criterion-subject reference form. The criteria list comes from
    # parse_goal rather than a second extraction here, so validation and parsing can never
    # disagree about which criteria exist.
    root = Path(repo_root) if repo_root is not None else _repo_root_for(path)
    problems.extend(_subject_problems(parse_goal(path)["criteria"], root))
    return (not problems), problems


def _validate_targets_section(raw: str) -> list[str]:
    """data-model.md §Entity 1 Validation Rules (038). Section present ⇒ checked."""
    problems: list[str] = []
    lines = [line for line in (raw or "").splitlines() if line.strip()]
    if not lines:
        problems.append(
            "## Targets section is empty; the correct form for a goal without "
            "targets is the section being absent entirely (空表格非法)"
        )
        return problems
    if lines[0].strip() != _TARGETS_HEADER:
        problems.append(
            "## Targets table header is wrong — the section MUST be rendered by the "
            "engine; hand edits are violations (结构由引擎渲染,手写即违规)"
        )
    rows = lines[1:]
    if rows and rows[0].strip().startswith("|---"):
        rows = rows[1:]
    seen: list[int] = []
    for row in rows:
        match = _TARGET_ROW.match(row.strip())
        if not match:
            problems.append(
                f"## Targets row does not match the render grammar ({row.strip()!r}) — "
                "结构由引擎渲染,手写即违规"
            )
            continue
        seen.append(int(match.group(1)[2:]))
    if lines[0].strip() == _TARGETS_HEADER and not seen and not any(
            p.startswith("## Targets row") for p in problems):
        problems.append(
            "## Targets table is empty (header without rows); a goal without targets "
            "carries no section at all"
        )
    if len(seen) != len(set(seen)):
        problems.append("## Targets contains duplicate identities (节内唯一)")
    for prev, cur in zip(seen, seen[1:]):
        if cur <= prev:
            problems.append(
                f"## Targets identities are not monotone (T-{cur:03d} after "
                f"T-{prev:03d}); identities are issued max+1 and never reused"
            )
            break
    return problems


# --------------------------------------------------------------------------
# actions
# --------------------------------------------------------------------------

def create_goal(repo_root: Path, slug: str, objective: str,
                criteria: list[str] | None = None, *,
                title: str | None = None,
                boundaries: list[str] | None = None) -> Path:
    if not is_valid_identity(slug):
        raise GoalError(
            f"identity {slug!r} is invalid: the first character must be alphanumeric, "
            "the rest limited to [A-Za-z0-9_.-], and it must be a safe path segment"
        )
    _reject_bad_objective(objective)
    path = definition_path(repo_root, slug)
    if path.exists():
        raise GoalError(
            f"goal {slug!r} already exists at {path}; use the modify path "
            "(`objective` / `status` / `criteria`) — the existing definition is never "
            "overwritten"
        )
    today = _today()
    # Identity stays the slug; the title is presentation and collapses to one line.
    heading = " ".join((title or "").split()) or slug
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        _render(objective, list(criteria or []), "active", today, today,
                [f"- {today} — created."], heading,
                boundaries=[b.strip() for b in (boundaries or []) if b.strip()] or None),
        encoding="utf-8",
    )
    return path


def set_status(path: Path, target: str) -> Path:
    path = Path(path)
    data = parse_goal(path)
    current = data["status"]
    if not transition_allowed(current, target):
        raise GoalError(
            f"transition {current!r} -> {target!r} is not defined; terminal goals are "
            "retained and never reopened"
        )
    today = _today()
    history = [line for line in data["history"].splitlines() if line.strip()]
    history.append(f"- {today} — status {current} -> {target}.")
    path.write_text(
        _render(data["objective"], data["criteria"], target, data["created"],
                today, history, data["title"], data["targets"], data["boundaries"],
                data["binding_block"]),
        encoding="utf-8",
    )
    return path


def set_objective(path: Path, objective: str) -> Path:
    """Deliberate objective replacement — `set_criteria`'s change discipline:
    the prior value stays traceable, `updated` bumps, terminal goals stay read-only."""
    path = Path(path)
    data = parse_goal(path)
    _assert_goal_mutable(data, "the objective cannot be replaced")
    _reject_bad_objective(objective)
    today = _today()
    history = [line for line in data["history"].splitlines() if line.strip()]
    previous = " ".join(data["objective"].split())
    history.append(f"- {today} — objective changed; prior value: {previous}")
    path.write_text(
        _render(objective, data["criteria"], data["status"], data["created"],
                today, history, data["title"], data["targets"], data["boundaries"],
                data["binding_block"]),
        encoding="utf-8",
    )
    return path


def set_criteria(path: Path, criteria: list[str]) -> Path:
    """FR-005: the prior value stays traceable in History, never silently replaced."""
    path = Path(path)
    data = parse_goal(path)
    today = _today()
    history = [line for line in data["history"].splitlines() if line.strip()]
    previous = data["criteria"] or [NO_CRITERIA_MARKER]
    history.append(
        f"- {today} — criteria changed; prior value: " + " | ".join(previous)
    )
    path.write_text(
        _render(data["objective"], list(criteria), data["status"], data["created"],
                today, history, data["title"], data["targets"], data["boundaries"],
                data["binding_block"]),
        encoding="utf-8",
    )
    return path


def _assert_goal_mutable(data: dict,
                         consequence: str = "targets cannot be added or transitioned") -> None:
    """Terminal goals are read-only — no new targets, no transitions (038)."""
    if data["status"] in TERMINAL_STATES:
        raise GoalError(
            f"goal is in terminal state {data['status']!r} and read-only "
            f"(终态 goal 只读); {consequence}"
        )


def _validate_target_statement(data: dict, statement: str) -> None:
    """Same-source statement validation shared by --add and --check (042 C-1):
    GD-2/GD-3 shape plus criteria-restatement — one grammar, zero forks."""
    _reject_bad_target_statement(statement)
    normalized = _normalize(statement.strip())
    for criterion in data["criteria"]:
        if normalized == _normalize(criterion):
            raise GoalError(
                "target statement is normalized-equal to a success criterion; the "
                "criteria axis is authoritative — rewrite the slice as a scope cut "
                "(判据权威互斥,改写为范围切片)"
            )


def add_target(path: Path, statement: str) -> str:
    """Authorize a new open Target; returns the issued identity (D6 history)."""
    path = Path(path)
    data = parse_goal(path)
    _assert_goal_mutable(data)
    _validate_target_statement(data, statement)
    statement = statement.strip()
    targets = data["targets"]
    tid = _next_target_id(targets)
    targets.append({"id": tid, "statement": statement, "status": "open"})
    today = _today()
    history = [line for line in data["history"].splitlines() if line.strip()]
    history.append(f"- {today} target {tid} added: {statement}")
    path.write_text(
        _render(data["objective"], data["criteria"], data["status"], data["created"],
                today, history, data["title"], targets, data["boundaries"],
                data["binding_block"]),
        encoding="utf-8",
    )
    return tid


def set_target_status(path: Path, tid: str, new_status: str) -> Path:
    """Apply one legal Target transition; no-op on equal state, never silent history."""
    path = Path(path)
    data = parse_goal(path)
    _assert_goal_mutable(data)
    targets = data["targets"]
    row = next((t for t in targets if t["id"] == tid), None)
    if row is None:
        raise GoalNotFound(f"target {tid} not found in goal {data['slug']!r}")
    current = row["status"]
    if current == new_status:
        return path  # contract §2: no-op, exit 0, no history line
    if not target_transition_allowed(current, new_status):
        raise GoalError(
            f"transition {current} -> {new_status} is not in the legal set "
            f"{sorted(TARGET_LEGAL_TRANSITIONS)}; legal moves: "
            "open→done, open→dropped, done→open, dropped→open"
        )
    row["status"] = new_status
    today = _today()
    history = [line for line in data["history"].splitlines() if line.strip()]
    history.append(f"- {today} target {tid} {current}→{new_status}")
    path.write_text(
        _render(data["objective"], data["criteria"], data["status"], data["created"],
                today, history, data["title"], targets, data["boundaries"],
                data["binding_block"]),
        encoding="utf-8",
    )
    return path


def resolve_team_goal_identity(repo_root: Path, team_slug: str) -> tuple[str | None, str]:
    """Two-level goal identity resolution (036 §10.1) — explicit `goal_slug`
    wins, else the team slug when it names an anchored definition. No third
    level (038 contract §2.1)."""
    root = team_root(repo_root)
    team_md = root / "team.md"
    if not team_md.is_file():
        team_md = root / team_slug / "team.md"
    if not team_md.is_file():
        raise GoalNotFound(f"team not found: {team_slug}")
    meta, _ = _split_frontmatter(team_md.read_text(encoding="utf-8"))
    declared = str(meta.get("goal_slug") or "").strip()
    if declared:
        return declared, "explicit"
    if definition_path(repo_root, team_slug).is_file():
        return team_slug, "inferred"
    return None, "none"


_QUALIFIED_TARGET = re.compile(r"^([A-Za-z0-9][A-Za-z0-9_.\-]*)\.(T-\d{3})$")


def preview_target_check(repo_root: Path, team_slug: str, reference: str) -> dict:
    """The deterministic core of run --target preview validation (038 contract §2).

    Read-only: parses, never writes. The verdict dict carries everything the
    command's gate disclosure needs (goal_slug, identity_kind, statement, status).
    """
    goal_slug, identity_kind = resolve_team_goal_identity(repo_root, team_slug)
    base = {"goal_slug": goal_slug, "identity_kind": identity_kind}
    if goal_slug is None:
        return {**base, "verdict": "no-goal-definition",
                "message": ("Target 依赖 goal 定义——该团队没有绑定的 goal 定义;"
                            "先经 /speckit.goal migrate 将内联 goal 落为定义")}

    qualified = _QUALIFIED_TARGET.match(reference)
    if qualified:
        prefix, tid = qualified.groups()
        if prefix != goal_slug:
            return {**base, "verdict": "cross-goal",
                    "message": (f"跨 goal 引用 {reference!r}:绑定 goal 为 "
                                f"{goal_slug!r},绑定轴不可越界(FR-012)")}
    elif TARGET_IDENTITY.match(reference):
        tid = reference
    else:
        return {**base, "verdict": "input-error",
                "message": (f"引用 {reference!r} 不符合文法 T-<nnn> 或 "
                            "<goal-slug>.T-<nnn>")}

    goal_path = definition_path(repo_root, goal_slug)
    if not goal_path.is_file():
        return {**base, "verdict": "no-goal-definition",
                "message": (f"绑定 goal {goal_slug!r} 无定义文件;先经 "
                            "/speckit.goal migrate 落为定义")}
    data = parse_goal(goal_path)
    if data["status"] in TERMINAL_STATES:
        return {**base, "verdict": "goal-terminal",
                "message": (f"goal {goal_slug!r} 处于终态 {data['status']!r},"
                            "终态 goal 只读,拒绝指派")}
    row = next((t for t in data["targets"] if t["id"] == tid), None)
    if row is None:
        return {**base, "verdict": "dangling",
                "message": (f"悬空引用 {tid}:goal {goal_slug!r} 无此 Target;"
                            "先经 /speckit.goal targets --add 添加")}
    if row["status"] in ("done", "dropped"):
        return {**base, "verdict": "target-terminal", "status": row["status"],
                "statement": row["statement"],
                "message": (f"Target {tid} 处于终态 {row['status']!r},run 停止——"
                            "复核二分:属实则返回报告结束;证据不符则经 "
                            f"/speckit.goal targets --set open --id {tid} 重开后"
                            "重新发起 run。不提供终态执行旁路")}
    return {**base, "verdict": "ok", "status": row["status"],
            "statement": row["statement"], "target_id": tid, "message": ""}


def resolve_effective_target(team_md_path: Path, explicit_target: str | None = None) -> dict:
    """Resolve the effective run Target (042 contract §C-1): explicit --target
    > team.md `focus_target` > none.

    Pure resolution — never judges: the effective value (when not None) is fed
    to preview_target_check for the unchanged five-check pass. `source=none`
    (no explicit target, no declared field) keeps field-less teams
    byte-equivalent to pre-042 behavior. A malformed `focus_target` is a
    configuration error: input-error stop, never silently ignored, never
    degraded to none."""
    team_md_path = Path(team_md_path)
    if not team_md_path.is_file():
        raise GoalNotFound(f"team not found: {team_md_path}")
    meta, _ = _split_frontmatter(team_md_path.read_text(encoding="utf-8"))
    raw_focus = meta.get("focus_target")
    declared_focus = str(raw_focus).strip() if raw_focus is not None else None
    if explicit_target:
        return {"effective": explicit_target, "source": "explicit",
                "declared_focus": declared_focus or None}
    if declared_focus is not None and not TARGET_IDENTITY.match(declared_focus):
        return {"effective": None, "source": "input-error",
                "declared_focus": declared_focus,
                "message": ("input-error: focus_target 值 " f"{declared_focus!r} 不符合文法 "
                            "T-<nnn>(配置错误,停止——不静默忽略、不降级为无;经 "
                            "improve-team 修正字段)")}
    if declared_focus:
        return {"effective": declared_focus, "source": "team-default",
                "declared_focus": declared_focus}
    return {"effective": None, "source": "none", "declared_focus": None}


# --------------------------------------------------------------------------
# 053 run-checks — the five run-precondition checks, one call, zero writes
# --------------------------------------------------------------------------

def _check(cid: int, name: str, verdict: str, message: str = "") -> dict:
    return {"id": cid, "name": name, "verdict": verdict, "message": message}


def _goal_binding_check(ctx: dict) -> tuple[str, str]:
    """① Is a goal definition bound to this team, and does the file exist?"""
    goal_slug, _kind = resolve_team_goal_identity(ctx["repo_root"], ctx["team_slug"])
    if goal_slug is None:
        return "no-goal-definition", (
            "该团队没有绑定的 goal 定义;先经 /speckit.goal migrate 将内联 goal 落为定义")
    if not definition_path(ctx["repo_root"], goal_slug).is_file():
        return "no-goal-definition", (
            f"绑定 goal {goal_slug!r} 无定义文件;先经 /speckit.goal migrate 落为定义")
    return "ok", ""


def _dangling_check(ctx: dict) -> tuple[str, str]:
    """② Does the referenced Target exist in the bound goal's `## Targets`?"""
    if ctx["tid"] is None:
        return NOT_EVALUATED, "无有效 Target 引用,悬空检查无判定主体"
    if ctx["goal_data"] is None:
        return NOT_EVALUATED, "无 goal 定义可查,悬空检查无判定主体"
    row = next((t for t in ctx["goal_data"]["targets"] if t["id"] == ctx["tid"]), None)
    if row is None:
        return "dangling", (
            f"悬空引用 {ctx['tid']}:goal {ctx['goal_slug']!r} 无此 Target;"
            "先经 /speckit.goal targets --add 添加")
    return "ok", ""


def _target_terminal_check(ctx: dict) -> tuple[str, str]:
    """③ Is the referenced Target already in a terminal state?"""
    if ctx["tid"] is None:
        return NOT_EVALUATED, "无有效 Target 引用,终态引用检查无判定主体"
    if ctx["goal_data"] is None:
        return NOT_EVALUATED, "无 goal 定义可查,终态引用检查无判定主体"
    row = next((t for t in ctx["goal_data"]["targets"] if t["id"] == ctx["tid"]), None)
    if row is None:
        return NOT_EVALUATED, f"Target {ctx['tid']} 不存在,其状态无从判定(见悬空检查)"
    if row["status"] in ("done", "dropped"):
        return "target-terminal", (
            f"Target {ctx['tid']} 处于终态 {row['status']!r},run 停止——复核二分:属实则返回"
            f"报告结束;证据不符则经 /speckit.goal targets --set open --id {ctx['tid']} 重开后"
            "重新发起 run。不提供终态执行旁路")
    return "ok", ""


def _cross_goal_check(ctx: dict) -> tuple[str, str]:
    """④ Does a QUALIFIED reference cross the binding axis?"""
    if ctx["grammar"] != "qualified":
        # A local-form `T-<nnn>` carries no prefix, so no cross-goal question arises. This is
        # a check with no subject, not a check that passed — reporting `ok` here would claim
        # a comparison ran that never did.
        return NOT_EVALUATED, (
            "引用不是限定形 <goal-slug>.T-<nnn>,无跨 goal 前缀可比"
            if ctx["grammar"] == "local" else "无有效 Target 引用,跨 goal 检查无判定主体")
    if ctx["prefix"] != ctx["goal_slug"]:
        return "cross-goal", (
            f"跨 goal 引用 {ctx['reference']!r}:绑定 goal 为 {ctx['goal_slug']!r},"
            "绑定轴不可越界")
    return "ok", ""


def _goal_terminal_check(ctx: dict) -> tuple[str, str]:
    """⑤ Is the bound goal itself in a terminal lifecycle state?"""
    if ctx["goal_data"] is None:
        return NOT_EVALUATED, "无 goal 定义可读,goal 终态检查无判定主体"
    if ctx["goal_data"]["status"] in TERMINAL_STATES:
        return "goal-terminal", (
            f"goal {ctx['goal_slug']!r} 处于终态 {ctx['goal_data']['status']!r},"
            "终态 goal 只读,拒绝指派")
    return "ok", ""


#: Reporting order == id order. Each entry is called under its own guard, because one check
#: raising must leave the other four reported rather than swallowing the whole verdict.
_RUN_CHECK_FUNCTIONS = (
    _goal_binding_check, _dangling_check, _target_terminal_check,
    _cross_goal_check, _goal_terminal_check,
)


def _compose_verdict(checks: list, grammar: str) -> str:
    """The top-level verdict projected from the five, in the gate's own priority order.

    The reference grammar is judged before any of the five, exactly as preview_target_check
    judges it, so an unusable reference is `input-error` and not a projection of the array.
    """
    if grammar in ("input-error", "invalid"):
        return "input-error"
    by_id = {c["id"]: c for c in checks}
    for cid in _TOP_VERDICT_ORDER:
        verdict = by_id[cid]["verdict"]
        if verdict not in ("ok", NOT_EVALUATED):
            return verdict
    return "ok"


def run_checks(repo_root: Path, team_slug: str, explicit_target: str | None = None) -> dict:
    """The five run-precondition checks for one team, in ONE call. Zero writes.

    Every verdict comes from the engine's own code path — resolve_team_goal_identity,
    definition_path, parse_goal, TERMINAL_STATES, _QUALIFIED_TARGET, TARGET_IDENTITY and
    resolve_effective_target — and where a reference is in play the top-level verdict is
    `preview_target_check`'s own, verbatim. So this action reports the gate run mode already
    trusts; it does not re-decide it, and it defines no grammar of its own.

    A check whose precondition does not hold is NOT_EVALUATED, never `ok`, and each check is
    guarded separately so one raising leaves the other four reported.

    Blocking is target-scoped for ① goal-binding and NOT for ⑤ goal-terminal, because that
    is what the recorded rule says: team.md's check 1 states that a team with no goal
    definition stops only when a --target was given ("不指定 --target 时一切照旧"), while
    check 5 ("终态 goal 只读") is a property of the goal and carries no such scoping.

    This binary has no EXIT_USAGE=1, so an argparse usage failure exits 2 and cannot be told
    apart from an in-body input error. run-checks does not depend on that distinction: a
    usage failure never reaches this function, and every input error it can itself produce
    is the `input-error` verdict, which maps to exit 2 for either cause alike.
    """
    repo_root = Path(repo_root)
    root = team_root(repo_root)
    team_md = root / "team.md"
    if not team_md.is_file():
        team_md = root / team_slug / "team.md"
    if not team_md.is_file():
        raise GoalNotFound(f"team not found: {team_slug}")

    # C-18 / T046: the team lifecycle is its own closed two-value set; a definition
    # outside it is refused instead of being run under a state nobody defined.
    lifecycle_state = _lifecycle_for_kind(team_md, "teams")
    if lifecycle_state not in ("", "active", "archived"):
        raise GoalError(
            f"team-lifecycle: team {team_slug!r} declares lifecycle_state "
            f"{lifecycle_state!r}, outside the closed set active / archived")

    # C-30 / T048: carry the loaded team's binding record additively. A team that
    # predates the binding model keeps working — the key reports the absence (null)
    # rather than turning the run preview into a new refusal.
    binding = None
    if _binding_block_lines(team_md.read_text(encoding="utf-8"))[0] is not None:
        binding = read_binding(team_md)

    resolution = resolve_effective_target(team_md, explicit_target)
    reference = resolution["effective"]

    grammar, prefix, tid = "none", None, None
    if resolution["source"] == "input-error":
        grammar = "input-error"
    elif reference is not None:
        if TARGET_IDENTITY.match(reference):
            grammar, tid = "local", reference
        else:
            qualified = _QUALIFIED_TARGET.match(reference)
            if qualified:
                grammar = "qualified"
                prefix, tid = qualified.groups()
            else:
                # Matches neither grammar. This is a distinct state from "no reference at
                # all": preview_target_check reports it as `input-error` and stops, so the
                # projection must too — folding it into `none` would exit 0 on an argument
                # the engine rejects, which is a green verdict on a run that cannot happen.
                grammar = "invalid"

    goal_slug, identity_kind = resolve_team_goal_identity(repo_root, team_slug)
    goal_data = None
    if goal_slug is not None:
        path = definition_path(repo_root, goal_slug)
        if path.is_file():
            try:
                goal_data = parse_goal(path)
            except GoalError as exc:
                raise GoalInvalid(
                    f"goal definition {goal_slug!r} cannot be parsed: {exc}") from exc
            if goal_data["status"] not in LIFECYCLE_STATES:
                raise GoalInvalid(
                    f"goal definition {goal_slug!r} declares status "
                    f"{goal_data['status']!r}, outside the lifecycle set {LIFECYCLE_STATES} "
                    "— the goal-terminal check has no decidable subject")

    ctx = {
        "repo_root": repo_root, "team_slug": team_slug, "team_md": team_md,
        "resolution": resolution, "reference": reference, "grammar": grammar,
        "prefix": prefix, "tid": tid, "goal_slug": goal_slug,
        "identity_kind": identity_kind, "goal_data": goal_data,
    }

    checks = []
    for index, check_fn in enumerate(_RUN_CHECK_FUNCTIONS):
        try:
            verdict, message = check_fn(ctx)
        except Exception as exc:      # one check failing must not swallow the other four
            verdict = NOT_EVALUATED
            message = f"{RUN_CHECK_NAMES[index]} 检查自身失败,未得出判定:{exc}"
        checks.append(_check(index + 1, RUN_CHECK_NAMES[index], verdict, message))

    # The authoritative gate decides the top-level verdict whenever it can run; the
    # projection is the fallback for the two cases it cannot (no reference at all, or a
    # reference whose grammar failed before any check had a subject).
    verdict = None
    if grammar in ("local", "qualified"):
        try:
            verdict = preview_target_check(repo_root, team_slug, reference)["verdict"]
        except GoalError:
            verdict = None
    if verdict is None:
        verdict = _compose_verdict(checks, grammar)

    blocked = False
    for check in checks:
        if check["verdict"] not in BLOCKING_VERDICTS:
            continue
        if check["id"] == 1 and grammar == "none":
            continue        # team.md check 1: no --target, 一切照旧 — informational only
        blocked = True
    if verdict == "input-error":
        blocked = False     # a bad argument is the input tier, not a block

    return {
        "team_slug": team_slug,
        "goal_slug": goal_slug,
        "identity_kind": identity_kind,
        "binding": binding,
        "resolution": {k: resolution.get(k) for k in ("effective", "source", "declared_focus")},
        "checks": checks,
        "verdict": verdict,
        "blocked": blocked,
    }


def migrate_team(repo_root: Path, team_slug: str, *, keep_inline: bool = True) -> tuple[Path, str]:
    """Derive a goal definition from a team's inline goal and switch it to a reference.

    Per-team and optional (FR-016..FR-019). The inline goal is kept by default —
    removal is the user's choice, never forced. Semantics are preserved: the objective
    the team resolved before migration is the objective the definition carries after.
    """
    team_md = team_root(repo_root) / team_slug / "team.md"
    if not team_md.is_file():
        raise GoalError(f"team not found: {team_md}")
    text = team_md.read_text(encoding="utf-8")
    fm, body = _split_frontmatter(text)

    inline = str(fm.get("goal") or "").strip()
    if not inline:
        raise GoalError(f"team {team_slug!r} has no inline goal to migrate")

    # objective = first sentence/line of the inline goal; criteria = 成功标准/success lines
    objective = " ".join(inline.split())
    criteria: list[str] = []
    goal_body = _section(body, "## Goal")
    for line in goal_body.splitlines():
        stripped = re.sub(r"^\s*(?:\d+[.)]|[-*+])\s*", "", line).strip()
        if stripped and re.search(r"成功标准|success crit|criteri|判据|阈值|threshold", stripped, re.I):
            criteria.append(stripped)

    identity = str(fm.get("goal_slug") or team_slug)
    if definition_path(repo_root, identity).exists():
        raise GoalError(
            f"a definition for {identity!r} already exists; migration would overwrite it — "
            "resolve manually via the modify path"
        )
    created = create_goal(repo_root, identity, objective, criteria)

    # set goal_slug on the team, preserving the rest of the file verbatim
    if "goal_slug:" in text:
        new_text = re.sub(r"(?m)^goal_slug:.*$", f"goal_slug: {identity}", text)
    else:
        # insert right after the `goal:` line (or its folded block's first line)
        new_text = re.sub(r"(?m)^(goal:.*\n(?:\s+.*\n)*)", r"\1" + f"goal_slug: {identity}\n",
                          text, count=1)
        if "goal_slug:" not in new_text:  # no goal line matched; append to frontmatter
            new_text = text.replace("---\n", f"---\ngoal_slug: {identity}\n", 1)
    if not keep_inline:
        # the caller explicitly opted to drop the inline copy
        new_text = re.sub(r"(?m)^goal:.*(?:\n\s+.*)*\n", "", new_text, count=1)
    team_md.write_text(new_text, encoding="utf-8")
    return created, identity


def list_goals(repo_root: Path) -> list[dict]:
    root = anchor_root(repo_root)
    if not root.is_dir():
        return []
    rows = []
    for child in sorted(root.iterdir()):
        definition = child / definition_filename("anchor")
        if child.is_dir() and definition.is_file():
            data = parse_goal(definition)
            rows.append({
                "slug": data["slug"],
                "status": data["status"],
                "criteria_count": data["criteria_count"],
                "updated": data["updated"],
            })
    return rows


# --------------------------------------------------------------------------
# action-level Goal group (101, FR-019…FR-027; contracts/goal-engine C-28)
# --------------------------------------------------------------------------

GOAL_SECTION_GUIDANCE = "## Guidance"
GOAL_SECTION_DONE = "## Completion Conditions"
GOAL_SECTION_MIGRATED = "## Migrated Targets"

#: FR-004 — a Goal carries no Anchor pointer. The binding record's `origin` is the only
#: cross-reference; a key named after an Anchor is undeclared and rejected (exit 2).
_ANCHOR_POINTER_KEY = re.compile(r"(?i)^anchor(?:_|$)")

#: C-28 — the collision refusal names both stores because they are distinct namespaces.
GOAL_ACTIONS = ("goal-create", "goal-list", "goal-view", "goal-modify", "goal-status")


def _binding_values(text: str) -> dict | None:
    """The binding record's three values, or None when the block is absent."""
    start, block, _end = _binding_block_lines(text)
    if start is None:
        return None
    values: dict = {"owner": None, "owner_id": None, "origin": None}
    for line in block[1:]:
        key, _, value = line.strip().partition(":")
        if key in values:
            values[key] = None if value.strip() in ("", "null") else value.strip()
    return values


def _render_action_goal(*, title: str, guidance: str, conditions: list[str],
                        status: str, created: str, updated: str,
                        history: list[str], migrated: list[str] | None = None,
                        boundaries: list[str] | None = None,
                        binding_lines: list[str] | None = None) -> str:
    frontmatter = f"status: {status}\ncreated: {created}\nupdated: {updated}\n"
    if binding_lines:
        frontmatter += "\n".join(binding_lines) + "\n"
    done_block = ("\n".join(f"{i}. {c}" for i, c in enumerate(conditions, 1))
                  if conditions else NO_CRITERIA_MARKER)
    sections = [
        f"{GOAL_SECTION_GUIDANCE}\n\n{guidance.strip()}",
        f"{GOAL_SECTION_DONE}\n\n{done_block}",
    ]
    if migrated:
        sections.append(f"{GOAL_SECTION_MIGRATED}\n\n"
                        + "\n".join(f"- {statement}" for statement in migrated))
    if boundaries:
        sections.append(f"{_SECTION_BOUNDARIES}\n\n"
                        + "\n".join(f"- {b}" for b in boundaries))
    sections.append(f"{_SECTION_HISTORY}\n\n" + "\n".join(history))
    return (f"---\n{frontmatter}---\n\n# Goal: {title}\n\n"
            + "\n\n".join(sections) + "\n")


def parse_action_goal(path: Path) -> dict:
    """Interpret one Goal. A schema violation is exit 4 (the file exists but is unusable)."""
    path = Path(path)
    text = path.read_text(encoding="utf-8")
    meta, body = _split_frontmatter(text)
    offending = sorted(key for key in meta if _ANCHOR_POINTER_KEY.match(key))
    if offending:
        raise GoalInvalid(
            f"goal-schema: {_relative(_repo_root_for(path), path)} declares Anchor pointer "
            f"key(s) {', '.join(offending)}; an action-level Goal carries no Anchor "
            "reference — the only cross-reference is the binding record's origin")
    status = str(meta.get("status") or "").strip()
    if status not in LIFECYCLE_STATES:
        raise GoalInvalid(
            f"goal-schema: status {status!r} in {_relative(_repo_root_for(path), path)} is "
            f"outside the shared lifecycle {LIFECYCLE_STATES}")
    raw_conditions = _section(body, GOAL_SECTION_DONE)
    conditions: list[str] = []
    if raw_conditions.strip() and raw_conditions.strip() != NO_CRITERIA_MARKER:
        for line in raw_conditions.splitlines():
            stripped = re.sub(r"^\s*(?:\d+[.)]|[-*+])\s*", "", line).strip()
            if stripped:
                conditions.append(stripped)
    return {
        "slug": path.parent.name,
        "title": _title_from_body(body),
        "status": status,
        "created": str(meta.get("created") or "").strip(),
        "updated": str(meta.get("updated") or "").strip(),
        "guidance": _section(body, GOAL_SECTION_GUIDANCE),
        "conditions": conditions,
        "migrated_targets": _parse_bullets(_section(body, GOAL_SECTION_MIGRATED)),
        "boundaries": _parse_bullets(_section(body, _SECTION_BOUNDARIES)),
        "history": _parse_bullets(_section(body, _SECTION_HISTORY)),
        "path": str(path),
    }


def _assert_goal_identity_free(repo_root: Path, slug: str) -> Path:
    """C-28 — refuse a slug the anchor store already owns, naming both candidates.

    Both filenames are read: before the cleanup renames it, a retained Anchor still
    lives as `goal.md`, and a collision is a collision either way.
    """
    anchor_dir = layer_root(repo_root, "anchor") / slug
    goal_path = definition_path(repo_root, slug, "goals")
    for filename in ("goal.md", definition_filename("anchor")):
        occupied = anchor_dir / filename
        if occupied.is_file():
            raise GoalError(
                f"cross-layer-collision: slug {slug!r} already names the Anchor "
                f"{_relative(repo_root, occupied)}; the two stores are distinct "
                f"namespaces and a collision is an authoring error, not a merge — "
                f"{_relative(repo_root, goal_path)} is refused and nothing is written")
    return goal_path


def create_action_goal(repo_root: Path, slug: str, guidance: str,
                       conditions: list[str], *, title: str | None = None) -> Path:
    """C-28 — write an action-level Goal. Guidance gets no GD-2 shape check (FR-024)."""
    if not is_valid_identity(slug):
        raise GoalError(
            f"identity {slug!r} is invalid: the first character must be alphanumeric, "
            "the rest limited to [A-Za-z0-9_.-], and it must be a safe path segment")
    if not " ".join(guidance.split()):
        raise GoalError(
            "goal-create requires --guidance: an action-level Goal states the practical "
            "action it guides")
    if not conditions:
        raise GoalError(
            "goal-create requires at least one --done: a Goal needs at least one "
            "verifiable completion condition (FR-024)")
    path = _assert_goal_identity_free(repo_root, slug)
    if path.exists():
        raise GoalError(
            f"goal {slug!r} already exists at {_relative(repo_root, path)}; use "
            "goal-modify — the existing definition is never overwritten")
    today = _today()
    heading = " ".join((title or "").split()) or slug
    path.parent.mkdir(parents=True, exist_ok=True)
    _atomic_write_text(path, _render_action_goal(
        title=heading, guidance=guidance,
        conditions=[" ".join(c.split()) for c in conditions],
        status="active", created=today, updated=today,
        history=[f"- {today} — created."],
        binding_lines=_render_binding_block(dict(RESIDENT_BINDING)).splitlines()))
    read_binding(path)
    return path


def list_action_goals(repo_root: Path) -> list[dict]:
    root = goals_root(repo_root)
    if not root.is_dir():
        return []
    rows = []
    for child in sorted(root.iterdir()):
        definition = child / definition_filename("goals")
        if child.is_dir() and definition.is_file():
            data = parse_action_goal(definition)
            rows.append({"slug": data["slug"], "status": data["status"],
                         "done_count": len(data["conditions"]),
                         "updated": data["updated"]})
    return rows


def modify_action_goal(path: Path, *, guidance: str | None = None,
                       conditions: list[str] | None = None,
                       clear: bool = False) -> dict:
    """C-28 — prior values stay traceable in History; `--clear-done` is the one
    destructive write and needs its explicit flag (and at least one replacement when
    it leaves the Goal with nothing)."""
    path = Path(path)
    data = parse_action_goal(path)
    if data["status"] in TERMINAL_STATES:
        raise GoalError(
            f"terminal-goal: {data['slug']!r} is {data['status']} and terminal is "
            "absorbing for writes; only a human-owned reopen (`goal-status --set active`) "
            "makes it writable again")
    today = _today()
    history = list(data["history"])
    if guidance is not None:
        if not " ".join(guidance.split()):
            raise GoalError("goal-modify --guidance must not be empty")
        history.append(f"- {today} — guidance changed; prior value: "
                       + " ".join(data["guidance"].split()))
        data["guidance"] = guidance
    if clear or conditions is not None:
        prior = data["conditions"] or [NO_CRITERIA_MARKER]
        history.append(f"- {today} — completion conditions changed; prior value: "
                       + " | ".join(prior))
    if clear:
        data["conditions"] = []
    elif conditions is not None:
        data["conditions"] = [" ".join(c.split()) for c in conditions]
    binding_lines = None
    if _binding_values(path.read_text(encoding="utf-8")):
        binding_lines = _binding_block_lines(path.read_text(encoding="utf-8"))[1]
    _atomic_write_text(path, _render_action_goal(
        title=data["title"] or data["slug"], guidance=data["guidance"],
        conditions=data["conditions"], status=data["status"],
        created=data["created"], updated=today, history=history,
        migrated=data["migrated_targets"], boundaries=data["boundaries"],
        binding_lines=binding_lines))
    return {"slug": data["slug"], "conditions": data["conditions"],
            "path": str(path)}


def action_goal_status(path: Path, target: str | None = None) -> dict:
    """C-28 — without `--set` this reports only; terminal states are retained, and a
    reopen is allowed for a human-owned Goal alone (D-3)."""
    path = Path(path)
    data = parse_action_goal(path)
    current = data["status"]
    if target is None or target == current:
        return {"slug": data["slug"], "status": current, "changed": False}
    if target not in LIFECYCLE_STATES:
        raise GoalError(f"status {target!r} is outside the shared lifecycle "
                        f"{LIFECYCLE_STATES}")
    if current in TERMINAL_STATES:
        binding = _binding_values(path.read_text(encoding="utf-8")) or {}
        if target != "active" or binding.get("owner") != "human":
            raise GoalError(
                f"transition {current!r} -> {target!r} is not defined; terminal Goals are "
                "retained, and only a human-owned Goal may be reopened (D-3)")
    elif not transition_allowed(current, target):
        raise GoalError(
            f"transition {current!r} -> {target!r} is not defined by the shared lifecycle")
    today = _today()
    history = list(data["history"])
    history.append(f"- {today} — status {current} -> {target}.")
    _atomic_write_text(path, _render_action_goal(
        title=data["title"] or data["slug"], guidance=data["guidance"],
        conditions=data["conditions"], status=target, created=data["created"],
        updated=today, history=history, migrated=data["migrated_targets"],
        boundaries=data["boundaries"],
        binding_lines=_binding_block_lines(path.read_text(encoding="utf-8"))[1]))
    return {"slug": data["slug"], "status": target, "changed": True}


def _resolve_action_goal(repo_root: Path, slug: str) -> Path:
    path = definition_path(repo_root, slug, "goals")
    if not path.is_file():
        raise GoalNotFound(
            f"goal not found: {_relative(repo_root, path)} (the action-level Goal store "
            "is .specify/goals/; Anchors live in .specify/anchoring/)")
    return path


# --------------------------------------------------------------------------
# unified archive: migration, residual probe, resident backfill
# (094, contracts/unified-archive-and-migration.md C-31…C-52, C-112…C-113)
# --------------------------------------------------------------------------

#: The migration destination history (STR-003): receipts and moved source trees.
ARCHIVE_HISTORY_DIRNAME = ".specify/archive/goal-team"
RECEIPTS_DIRNAME = "receipts"
TREES_DIRNAME = "trees"
DELETE_POLICY = "archive-not-delete"

#: C-33 / C-34 — the two receipt shapes. A migration receipt carries one of the four
#: migration outcomes below; an archive receipt (`result: archived`, written when a
#: definition retires in place) shares the directory family and is never a read surface.
MIGRATION_RESULTS = ("migrated", "noop", "conflict", "interrupted")

#: C-43 — the spec-local forms the residual probe enumerates. These are migration
#: SOURCES, never write targets; `.specify/.tmp/` is outside `.specify/specs/` entirely.
#: The filename is frozen to the retired legacy layout: a dated source is not a layer.
RESIDUAL_FORMS = {
    "goal": ("goal", "goal.md"),
    "teams": ("team", "team.md"),
}

#: C-112 — the backfill values are a recorded ruling (Clarifications Q14), not inference.
RESIDENT_BINDING = {"owner": "human", "owner_id": "human", "origin": None}

#: C-39 test seam: the two step boundaries an interruption can be injected after.
#: Declared, closed and side-effect-free; unset in production.
FAULT_ENV = "GOAL_UTILS_FAULT_AFTER"
FAULT_STEPS = ("target-write", "source-move")


class _Interrupted(Exception):
    """C-39 — a migration stopped between steps; carries the reached step."""

    def __init__(self, step: str, row: dict, state: dict):
        super().__init__(step)
        self.step = step
        self.row = row
        self.state = state


def _specs_root(repo_root: Path) -> Path:
    return Path(repo_root) / ".specify" / "specs"


def _history_root(repo_root: Path) -> Path:
    return Path(repo_root) / ARCHIVE_HISTORY_DIRNAME


def _receipt_path(repo_root: Path, kind: str, slug: str) -> Path:
    return _history_root(repo_root) / RECEIPTS_DIRNAME / f"{kind}-{slug}.yaml"


def _archived_tree_path(repo_root: Path, spec: str, kind: str, slug: str) -> Path:
    return _history_root(repo_root) / TREES_DIRNAME / spec / kind / slug


def _target_definition_path(repo_root: Path, kind: str, slug: str) -> Path:
    """C-31 — the two unified-archive landing points, and nothing else."""
    if kind == "goal":
        return Path(repo_root) / ARCHIVE_DIRNAME / slug / definition_filename("anchor")
    return Path(repo_root) / TEAM_DIRNAME / slug / "team.md"


def _relative(root: Path, path: Path) -> str:
    try:
        return Path(path).relative_to(root).as_posix()
    except ValueError:
        return str(path)


def probe_residual(repo_root: Path) -> dict:
    """C-43 — read-only enumeration of the spec-local residual trees (zero writes)."""
    repo_root = Path(repo_root)
    residuals: dict[str, list[str]] = {"goal": [], "teams": []}
    specs = _specs_root(repo_root)
    if specs.is_dir():
        for kind, (layer_dir, filename) in RESIDUAL_FORMS.items():
            for definition in sorted(specs.glob(f"*/{layer_dir}/*/{filename}")):
                residuals[kind].append(_relative(repo_root, definition))
    return {"residuals": residuals,
            "counts": {kind: len(rows) for kind, rows in residuals.items()}}


def _raw_frontmatter_value(text: str, key: str) -> str:
    """The raw value of one frontmatter key, folded continuation lines included.

    The closed-subset reader (R-06) parses four scalar kinds; a folded block scalar
    (`key: >-`) is outside them, yet a team's concept statement lives there. This slice
    reads that one key's text and does not grow into a second YAML parser.
    """
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return ""
    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration:
        return ""
    for i in range(1, end):
        if lines[i].startswith(key + ":"):
            raw = lines[i].partition(":")[2].strip()
            parts = [] if raw in (">", ">-", "|", "|-", "") else [raw]
            j = i + 1
            while j < end and lines[j][:1] in (" ", "\t"):
                parts.append(lines[j].strip())
                j += 1
            return " ".join(part for part in parts if part).strip()
    return ""


def _goal_concept_payload(path: Path) -> dict:
    data = parse_goal(path)
    return {
        "objective": " ".join(data["objective"].split()),
        "criteria": [" ".join(criterion.split()) for criterion in data["criteria"]],
        "status": data["status"].strip(),
        "targets": [[t["id"], " ".join(t["statement"].split()), t["status"]]
                    for t in data["targets"]],
    }


def _team_concept_payload(path: Path) -> dict:
    text = Path(path).read_text(encoding="utf-8")
    meta, _start, _end = read_frontmatter_subset(text)
    return {
        "description": str(meta.get("description") or "").strip(),
        "goal": _raw_frontmatter_value(text, "goal"),
        "goal_slug": str(meta.get("goal_slug") or "").strip(),
        "lifecycle_state": str(meta.get("lifecycle_state") or "").strip(),
    }


def concept_payload(kind: str, path: Path) -> dict:
    """C-40/C-41 — what "did this definition change" compares.

    Goal: Objective, Success Criteria, Lifecycle status, Targets text. Team: the nearest
    concept fields (description, the inline goal statement, goal_slug, lifecycle_state);
    territory is operational data and the binding block is excluded for both kinds.
    """
    return _goal_concept_payload(path) if kind == "goal" else _team_concept_payload(path)


def concept_digest(kind: str, path: Path) -> str:
    canonical = json.dumps(concept_payload(kind, path), sort_keys=True,
                           ensure_ascii=False, separators=(",", ":"))
    return "sha256:" + hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _read_binding_keys(text: str, path: Path) -> dict:
    """The binding block's three values, refusing any non-canonical or incomplete block."""
    start, block, occurrences = _binding_block_lines(text)
    if start is None:
        return {}
    parsed: dict = {}
    for line in block[1:]:
        key, sep, raw = line.strip().partition(":")
        if sep:
            parsed[key.strip()] = raw.strip()
    missing = [key for key in BINDING_KEYS if key not in parsed]
    if missing:
        raise GoalError(
            f"binding-incomplete: {path} carries a binding block missing "
            f"{', '.join(missing)}; the engine refuses to overwrite an incomplete record")
    binding = {"owner": parsed["owner"], "owner_id": parsed["owner_id"],
               "origin": None if parsed["origin"] in ("null", "~") else parsed["origin"]}
    if occurrences != 1 or block != _render_binding_block(binding).splitlines():
        raise GoalError(
            f"binding-hand-edited: the binding block in {path} is not in the "
            "engine-written canonical form; the binding is written only by this engine, "
            "never by a template, skill or driver")
    return binding


def _insert_binding_block(text: str, binding: dict) -> str:
    """Insert the binding block as the last frontmatter key; every other byte is kept."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise GoalInvalid("the definition carries no frontmatter; the binding record "
                          "cannot be inserted (owner / owner_id / origin)")
    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration:
        raise GoalInvalid("the definition's frontmatter is unterminated; the binding "
                          "record cannot be inserted") from None
    rewritten = lines[:end] + _render_binding_block(binding).splitlines() + lines[end:]
    new_text = "\n".join(rewritten)
    if text.endswith("\n"):
        new_text += "\n"
    return new_text


def _definition_with_origin(text: str, path: Path, origin: str) -> str:
    """C-36 — set origin on the definition; the rest of the binding, when present, stays."""
    existing = _read_binding_keys(text, path)
    binding = {"owner": existing.get("owner", RESIDENT_BINDING["owner"]),
               "owner_id": existing.get("owner_id", RESIDENT_BINDING["owner_id"]),
               "origin": origin}
    if not existing:
        return _insert_binding_block(text, binding)
    start, block, _occurrences = _binding_block_lines(text)
    lines = text.splitlines()
    rewritten = lines[:start] + _render_binding_block(binding).splitlines() \
        + lines[start + len(block):]
    new_text = "\n".join(rewritten)
    if text.endswith("\n"):
        new_text += "\n"
    return new_text


def _utc_now() -> str:
    return _dt.datetime.now(_dt.timezone.utc).replace(
        microsecond=0).strftime("%Y-%m-%dT%H:%M:%SZ")


def _receipt_body(*, kind: str, source_spec: str, source_slug: str, target_slug: str,
                  target_path: str, archived_path: str, digest: str, result: str,
                  at: str, reached_step: str | None = None) -> dict:
    body = {
        "kind": kind,
        "source_spec": source_spec,
        "source_slug": source_slug,
        "target_slug": target_slug,
        "target_path": target_path,
        "archived_path": archived_path,
        "concept_digest": digest,
        "result": result,
        "at": at,
        "delete_policy": DELETE_POLICY,
    }
    if reached_step:
        body["reached_step"] = reached_step
    return body


def _write_receipt(repo_root: Path, body: dict) -> Path:
    """One file per definition (`<kind>-<slug>.yaml`); never a shared stream (C-32)."""
    path = _receipt_path(repo_root, body["kind"], body["target_slug"])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(f"{key}: {value}" for key, value in body.items()) + "\n",
                    encoding="utf-8")
    return path


def _read_receipt(path: Path) -> dict:
    fields: dict = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        key, sep, value = line.partition(":")
        if sep and key and not key.startswith((" ", "\t")):
            fields[key.strip()] = value.strip()
    return fields


def _residual_sources(repo_root: Path) -> list[dict]:
    rows = []
    for kind, paths in probe_residual(repo_root)["residuals"].items():
        for rel in paths:
            definition = repo_root / rel
            rows.append({"kind": kind, "slug": definition.parent.name,
                         "source_spec": definition.parents[2].name,
                         "definition": definition, "source_tree": definition.parent})
    return rows


def _planned_receipt(row: dict) -> dict:
    return _receipt_body(
        kind=row["kind"], source_spec=row["source_spec"], source_slug=row["slug"],
        target_slug=row["slug"], target_path=row["target_path"],
        archived_path=row["archived_path"], digest=row["concept_digest"],
        result="migrated", at=_utc_now())


def _plan_row(repo_root: Path, kind: str, spec: str, slug: str, definition: Path,
              source_tree: Path | None) -> dict:
    target = _target_definition_path(repo_root, kind, slug)
    archived_tree = _archived_tree_path(repo_root, spec, kind, slug)
    if kind == "goal":
        ok, problems = validate_goal(definition, repo_root)
        if not ok:
            raise GoalInvalid(
                f"migration-invalid: {_relative(repo_root, definition)} fails validation "
                f"and is not migrated: {'; '.join(problems)}")
    digest = concept_digest(kind, definition)
    existing = _read_binding_keys(definition.read_text(encoding="utf-8"), definition)
    row = {
        "kind": kind, "slug": slug, "source_spec": spec,
        "source_path": _relative(repo_root, definition),
        "target_path": _relative(repo_root, target),
        "archived_path": _relative(repo_root, archived_tree),
        "concept_digest": digest,
        "definition": definition, "source_tree": source_tree,
        "binding": {"owner": existing.get("owner", RESIDENT_BINDING["owner"]),
                    "owner_id": existing.get("owner_id", RESIDENT_BINDING["owner_id"]),
                    "origin": spec},
    }
    if target.is_file():
        if concept_digest(kind, target) != digest:
            row["action"] = "conflict"
            row["result"] = "conflict"
            row["receipt"] = None
            return row
        row["action"] = "resume-move" if source_tree is not None else "resume-receipt"
    elif archived_tree.exists() and source_tree is None:
        row["action"] = "finish-write"
    else:
        row["action"] = "migrate"
    row["result"] = "migrated"
    row["receipt"] = _planned_receipt(row)
    return row


def _orphan_decisions(repo_root: Path, covered: set) -> list[dict]:
    """Definitions whose source tree moved but whose receipt is absent or interrupted."""
    trees_root = _history_root(repo_root) / TREES_DIRNAME
    rows: list[dict] = []
    if not trees_root.is_dir():
        return rows
    for spec_dir in sorted(path for path in trees_root.iterdir() if path.is_dir()):
        for kind in ("goal", "teams"):
            kind_dir = spec_dir / kind
            if not kind_dir.is_dir():
                continue
            for tree in sorted(path for path in kind_dir.iterdir() if path.is_dir()):
                definition = tree / ("goal.md" if kind == "goal" else "team.md")
                if not definition.is_file() or (kind, tree.name) in covered:
                    continue
                receipt = _receipt_path(repo_root, kind, tree.name)
                if receipt.is_file() and _read_receipt(receipt).get("result") != "interrupted":
                    continue
                rows.append(_plan_row(repo_root, kind, spec_dir.name, tree.name,
                                      definition, None))
    return rows


def _noop_decisions(repo_root: Path, covered: set) -> list[dict]:
    """C-38 — one noop entry per already-migrated definition, from its receipt."""
    receipts = _history_root(repo_root) / RECEIPTS_DIRNAME
    rows: list[dict] = []
    if not receipts.is_dir():
        return rows
    for path in sorted(receipts.glob("*.yaml")):
        fields = _read_receipt(path)
        if fields.get("result") != "migrated":
            continue
        kind, slug = fields.get("kind"), fields.get("target_slug")
        if kind not in ("goal", "teams") or not slug or (kind, slug) in covered:
            continue
        rows.append({
            "kind": kind, "slug": slug, "source_spec": fields.get("source_spec", ""),
            "source_path": "", "target_path": fields.get("target_path", ""),
            "archived_path": fields.get("archived_path", ""),
            "concept_digest": fields.get("concept_digest", ""),
            "action": "noop", "result": "noop", "receipt": None,
        })
    return rows


def _fault_after() -> str | None:
    value = os.environ.get(FAULT_ENV)
    return value if value in FAULT_STEPS else None


def _write_target(repo_root: Path, row: dict, target: Path, source_text: str) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        _definition_with_origin(source_text, target, row["source_spec"]),
        encoding="utf-8")
    read_binding(target)


def _execute_decision(repo_root: Path, row: dict) -> None:
    """C-35's three ordered steps, with the interruption seam at each boundary."""
    action = row["action"]
    if action in ("noop", "conflict"):
        return
    target = _target_definition_path(repo_root, row["kind"], row["slug"])
    archived = _archived_tree_path(repo_root, row["source_spec"], row["kind"], row["slug"])
    fault = _fault_after()

    def step(work, name: str) -> None:
        try:
            work()
        except OSError as exc:
            raise _Interrupted(name, row, {"target_exists": target.is_file()}) from exc
        if fault == name:
            raise _Interrupted(name, row, {"target_exists": target.is_file()})

    if action in ("migrate", "finish-write"):
        step(lambda: _write_target(repo_root, row, target,
                                   row["definition"].read_text(encoding="utf-8")),
             "target-write")
    if action in ("migrate", "resume-move"):
        def move() -> None:
            archived.parent.mkdir(parents=True, exist_ok=True)
            row["source_tree"].rename(archived)
        step(move, "source-move")
    step(lambda: _write_receipt(repo_root, _planned_receipt(row)), "source-move")


def _public_decision(row: dict) -> dict:
    return {key: value for key, value in row.items()
            if key not in ("definition", "source_tree")}


def migrate_archive(repo_root: Path, *, apply: bool) -> dict:
    """FR-009/FR-010 — move spec-local definitions into the unified archive.

    Planning is shared by `--dry-run` and `--apply`, which is what makes C-42's "same
    decisions" structural rather than a claim, and every write is one of the three
    ordered steps: target written and validated, source tree moved, receipt written.
    """
    repo_root = Path(repo_root)
    sources = _residual_sources(repo_root)
    for row in sources:
        archived = _archived_tree_path(repo_root, row["source_spec"], row["kind"],
                                       row["slug"])
        if archived.exists() and row["source_tree"].exists():
            raise GoalError(
                f"archive-conflict: {_relative(repo_root, archived)} already holds a "
                f"tree and {_relative(repo_root, row['source_tree'])} still exists; the "
                "move would overwrite the archived copy, so the migration refuses "
                "before writing anything (C-37)")

    decisions = [_plan_row(repo_root, row["kind"], row["source_spec"], row["slug"],
                           row["definition"], row["source_tree"]) for row in sources]
    covered = {(row["kind"], row["slug"]) for row in decisions}
    for row in _orphan_decisions(repo_root, covered):
        decisions.append(row)
    covered = {(row["kind"], row["slug"]) for row in decisions}
    for row in _noop_decisions(repo_root, covered):
        decisions.append(row)
    decisions.sort(key=lambda row: (row["kind"], row["slug"]))

    interrupted: dict | None = None
    if apply:
        executed: list[dict] = []
        for row in decisions:
            try:
                _execute_decision(repo_root, row)
            except _Interrupted as exc:
                receipt = _receipt_body(
                    kind=exc.row["kind"], source_spec=exc.row["source_spec"],
                    source_slug=exc.row["slug"], target_slug=exc.row["slug"],
                    target_path=exc.row["target_path"],
                    archived_path=exc.row["archived_path"],
                    digest=exc.row["concept_digest"], result="interrupted",
                    at=_utc_now(), reached_step=exc.step)
                _write_receipt(repo_root, receipt)
                interrupted = {
                    "result": "interrupted",
                    "error": (f"interrupted: the migration of {exc.row['kind']} "
                              f"{exc.row['slug']!r} stopped after the {exc.step} step; a "
                              "second call resumes from that step (C-39)"),
                    "reached_step": exc.step,
                    "target_exists": exc.state["target_exists"],
                    "target_path": exc.row["target_path"],
                    "archived_path": exc.row["archived_path"],
                }
                row_copy = dict(_public_decision(row))
                row_copy["result"] = "interrupted"
                row_copy["reached_step"] = exc.step
                decisions = executed + [row_copy]
                break
            executed.append(row)

    conflicts = [row for row in decisions if row["result"] == "conflict"]
    payload: dict = {
        "action": "migrate-archive",
        "mode": "apply" if apply else "dry-run",
        "decisions": [(_public_decision(row) if isinstance(row, dict) else row)
                      for row in decisions],
        "counts": {name: sum(1 for row in decisions if row["result"] == name)
                   for name in MIGRATION_RESULTS},
    }
    if interrupted:
        payload.update({key: interrupted[key] for key in
                        ("result", "error", "reached_step", "target_exists",
                         "target_path", "archived_path")})
    elif conflicts:
        payload["error"] = "conflict: " + "; ".join(
            f"target {row['target_path']} already exists with a different concept "
            f"payload than the source {row['source_path']} — the migration refuses to "
            "overwrite and names both candidates (C-40)" for row in conflicts)
    return payload


def _resident_definitions(repo_root: Path) -> list[dict]:
    """C-112 — every definition already living in the unified archive."""
    rows = []
    for path in sorted((Path(repo_root) / ARCHIVE_DIRNAME).glob("*/goal.md")):
        rows.append({"kind": "goal", "slug": path.parent.name, "path": path})
    for path in sorted((Path(repo_root) / TEAM_DIRNAME).glob("*/team.md")):
        rows.append({"kind": "teams", "slug": path.parent.name, "path": path})
    return rows


def backfill_bindings(repo_root: Path, *, apply: bool) -> dict:
    """C-112/C-113 — insert the recorded binding on every unbound archive resident.

    Every refusal is computed before the first write, so an incomplete or hand-edited
    block leaves the whole tree untouched rather than half-backfilled.
    """
    repo_root = Path(repo_root)
    planned: list[dict] = []
    refusals: list[str] = []
    for resident in _resident_definitions(repo_root):
        text = resident["path"].read_text(encoding="utf-8")
        if _binding_block_lines(text)[0] is None:
            result = "backfilled"
        else:
            try:
                _read_binding_keys(text, resident["path"])
            except GoalError as exc:
                refusals.append(str(exc))
                continue
            result = "already-bound"
        shown = _relative(repo_root, resident["path"])
        planned.append({"kind": resident["kind"], "slug": resident["slug"],
                        "path": shown, "result": result,
                        "_path": resident["path"]})
    if refusals:
        raise GoalError("; ".join(refusals))
    if apply:
        for row in planned:
            if row["result"] != "backfilled":
                continue
            text = row["_path"].read_text(encoding="utf-8")
            row["_path"].write_text(_insert_binding_block(text, RESIDENT_BINDING),
                                    encoding="utf-8")
    rows = [{key: value for key, value in row.items() if key != "_path"}
            for row in planned]
    return {"action": "backfill-bindings",
            "mode": "apply" if apply else "dry-run",
            "definitions": rows,
            "counts": {"backfilled": sum(1 for row in rows
                                         if row["result"] == "backfilled"),
                       "already-bound": sum(1 for row in rows
                                            if row["result"] == "already-bound")}}


# --------------------------------------------------------------------------
# definition cleanup group (101, FR-032…FR-045; migration-cleanup C-36…C-49)
# --------------------------------------------------------------------------

CLEANUP_SCHEMA = "101-classification/v1"
CLEANUP_MAPPING_VERSION = "101-mapping-v1"
CLEANUP_CLASSES = ("anchor", "action-goal", "obsolete")
#: FR-036's three decision rules, paired with the class each one decides.
CLEANUP_RULES = {"anchor": "FR-036(c)", "action-goal": "FR-036(a)",
                 "obsolete": "FR-036(b)"}
CLEANUP_ARCHIVE_DIRNAME = ".specify/archive/anchoring"
MIGRATION_RECEIPT_NAME = "migration-receipt.json"
MIGRATION_RECEIPT_SCHEMA = "101-migration-receipt/v1"
BODY_RECEIPT_NAME = "anchor-body-receipt.json"
BODY_RECEIPT_SCHEMA = "101-anchor-body-receipt/v1"
#: E-8's `action` literals and C-41's idempotent result literals.
RECEIPT_ACTIONS = {"migrate": "migrate-action-goal", "archive": "archive-obsolete"}
CLEANUP_DONE_RESULTS = {"migrate": "already-migrated", "archive": "already-archived"}
TEAM_DISPOSITIONS = ("R1", "R2", "R3")
TEAM_DISPOSITION_STATES = ("apply", "already-satisfied")
DISPOSITION_RECEIPT_NAME = "disposition-receipt.json"

#: C-42 phases. `READ`/`PROJECT` leave nothing on disk; the three that do are the seam.
CLEANUP_PHASES = ("read", "project", "write-target", "write-receipt", "remove-source")
#: T069's two declared injection points (unset in production, side-effect-free).
CLEANUP_FAULT_ENV = "GOAL_UTILS_CLEANUP_FAULT_AFTER"
CLEANUP_FAULT_STEPS = ("write-target", "write-receipt")

#: C-38 A-N. `.specify/goals` is the NEW store and MUST NOT be rewritten.
_RETIRED_GOAL_PATH = re.compile(r"\.specify/goal(?![a-z])")
_ANCHOR_TITLE = re.compile(r"^#\s*Goal:")
_RETIRED_COMMAND = re.compile(r"/speckit\.goal\b")

#: C-38 field mapping: exactly the two section renames, nothing else.
_GOAL_HEADING_MAP = {"## Objective": "## Guidance",
                     "## Success Criteria": "## Completion Conditions"}


class _CleanupInterrupted(Exception):
    def __init__(self, phase: str, row: dict):
        super().__init__(phase)
        self.phase = phase
        self.row = row


def _cleanup_archive_root(repo_root: Path) -> Path:
    return Path(repo_root) / CLEANUP_ARCHIVE_DIRNAME


def _engine_identity() -> str:
    try:
        from script_interface_cli import version_text
        return version_text("goal-utils.py")
    except Exception:  # a sandbox copy carries the engine but not the helper
        return "goal-utils.py unknown"


def _load_cleanup_json(path: Path) -> dict:
    try:
        raw = Path(path).read_text(encoding="utf-8")
    except OSError as exc:
        raise GoalError(f"classification-unreadable: {path} cannot be read ({exc}); "
                        "nothing is written") from None
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise GoalError(f"classification-invalid: {path} is not JSON ({exc}); nothing "
                        "is written") from None
    if not isinstance(data, dict):
        raise GoalError(f"classification-invalid: {path} must hold one JSON object")
    return data


def _live_anchor_slugs(repo_root: Path) -> set:
    root = anchor_root(repo_root)
    if not root.is_dir():
        return set()
    return {child.name for child in root.iterdir()
            if child.is_dir() and ((child / "goal.md").is_file()
                                   or (child / definition_filename("anchor")).is_file())}


def _team_binding_slugs(repo_root: Path) -> dict:
    """team slug -> the slug its frontmatter binds (goal_slug or anchor_slug), or None."""
    root = team_root(repo_root)
    rows: dict = {}
    if not root.is_dir():
        return rows
    for definition in sorted(root.glob("*/team.md")):
        meta, _start, _end = read_frontmatter_subset(
            definition.read_text(encoding="utf-8"))
        bound = meta.get("anchor_slug") or meta.get("goal_slug")
        rows[definition.parent.name] = str(bound).strip() if bound else None
    return rows


def _disposition_receipt(repo_root: Path, team_slug: str) -> dict | None:
    path = team_root(repo_root) / team_slug / DISPOSITION_RECEIPT_NAME
    if not path.is_file():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {"unreadable": True}


def _classification_problems(repo_root: Path, data: dict) -> list[str]:
    problems: list[str] = []
    if data.get("schema") != CLEANUP_SCHEMA:
        problems.append(f"schema must be {CLEANUP_SCHEMA!r}, found {data.get('schema')!r}")
    if data.get("mapping_version") != CLEANUP_MAPPING_VERSION:
        problems.append(f"mapping_version must be {CLEANUP_MAPPING_VERSION!r}, found "
                        f"{data.get('mapping_version')!r}")
    baseline = str(data.get("baseline_commit") or "").strip()
    if not baseline:
        problems.append("baseline_commit is absent")
    else:
        resolved = subprocess.run(
            ["git", "-C", str(repo_root), "rev-parse", "--verify", f"{baseline}^{{commit}}"],
            capture_output=True, text=True)
        if resolved.returncode != 0:
            problems.append(f"baseline_commit {baseline!r} does not resolve in this repo")

    entries = data.get("entries")
    if not isinstance(entries, list):
        problems.append("entries must be a list")
        entries = []
    seen: set = set()
    for index, entry in enumerate(entries):
        where = f"entries[{index}]"
        if not isinstance(entry, dict):
            problems.append(f"{where} must be an object")
            continue
        slug = str(entry.get("slug") or "")
        if not is_valid_identity(slug):
            problems.append(f"{where}.slug {slug!r} is not a valid identity")
        elif slug in seen:
            problems.append(f"{where}.slug {slug!r} is duplicated")
        seen.add(slug)
        cls = entry.get("class")
        if cls not in CLEANUP_CLASSES:
            problems.append(f"{where}.class {cls!r} is outside {CLEANUP_CLASSES}")
        elif entry.get("rule") != CLEANUP_RULES[cls]:
            problems.append(f"{where}.rule must be {CLEANUP_RULES[cls]!r} for class "
                            f"{cls!r}, found {entry.get('rule')!r}")
        if not isinstance(entry.get("targets"), int) or entry.get("targets") < 0:
            problems.append(f"{where}.targets must be a non-negative integer")
        if not isinstance(entry.get("summary"), bool):
            problems.append(f"{where}.summary must be a boolean")
    live = _live_anchor_slugs(repo_root)
    missing = sorted(live - seen)
    gone = sorted(seen - live)
    # C-41 — an entry that already moved is absent from the anchor store BY CONTRACT;
    # it is accounted for by its target + receipt, which is what keeps a second run
    # complete instead of reporting its own success as missing input.
    settled: set = set()
    for entry in entries:
        if not isinstance(entry, dict) or entry.get("class") == "anchor":
            continue
        slug = entry.get("slug")
        if slug not in gone:
            continue
        paths = _cleanup_paths(repo_root, entry)
        # A receipt-less target is still accounted for on disk: the plan turns that
        # state into the exit-4 half-state (or the resumable receipt write), never
        # into a coverage complaint that hides the real defect.
        if paths["target"].is_file():
            settled.add(slug)
    unsettled = sorted(set(gone) - settled)
    if missing or unsettled:
        problems.append("entries do not cover the live anchor store exactly"
                        + (f"; unclassified: {', '.join(missing)}" if missing else "")
                        + (f"; not on disk: {', '.join(unsettled)}" if unsettled else ""))

    teams = data.get("teams")
    if not isinstance(teams, list):
        problems.append("teams must be a list")
        teams = []
    classified: set = set()
    for index, row in enumerate(teams):
        where = f"teams[{index}]"
        if not isinstance(row, dict):
            problems.append(f"{where} must be an object")
            continue
        slug = str(row.get("slug") or "")
        if not is_valid_identity(slug):
            problems.append(f"{where}.slug {slug!r} is not a valid identity")
        elif slug in classified:
            problems.append(f"{where}.slug {slug!r} is duplicated")
        classified.add(slug)
        if row.get("disposition") not in TEAM_DISPOSITIONS:
            problems.append(f"{where}.disposition {row.get('disposition')!r} is outside "
                            f"{TEAM_DISPOSITIONS}")
        if row.get("state") not in TEAM_DISPOSITION_STATES:
            problems.append(f"{where}.state {row.get('state')!r} is outside "
                            f"{TEAM_DISPOSITION_STATES}")
        if not " ".join(str(row.get("reason") or "").split()):
            problems.append(f"{where}.reason must name the measured basis")

    live_teams = _team_binding_slugs(repo_root)
    unknown = sorted(slug for slug in classified if slug not in live_teams)
    if unknown:
        problems.append(f"classified team(s) not found on disk: {', '.join(unknown)}")
    non_anchor = {entry["slug"] for entry in entries
                  if isinstance(entry, dict) and entry.get("class") in ("action-goal", "obsolete")}
    affected = {slug for slug, bound in live_teams.items()
                if bound and (bound in non_anchor or bound not in live)}
    # C-47's R3 removes the binding; a team that already carries its disposition
    # receipt is accounted for, which keeps a post-apply re-read complete.
    affected |= {slug for slug in classified if _disposition_receipt(repo_root, slug)}
    if affected != classified:
        missing = sorted(affected - classified)
        extra = sorted(classified - affected)
        problems.append("team set is incomplete against the live bindings"
                        + (f"; unclassified: {', '.join(missing)}" if missing else "")
                        + (f"; not affected: {', '.join(extra)}" if extra else ""))
    return problems


def load_classification(repo_root: Path, path: Path) -> dict:
    """C-36 — read and adjudicate the input before any decision or write."""
    data = _load_cleanup_json(path)
    problems = _classification_problems(Path(repo_root), data)
    if problems:
        raise GoalError("classification-invalid: " + "; ".join(problems)
                        + " — nothing is written")
    return data


# ---- C-38 / C-39: the two declared mappings and the concept digest ----------

def _map_anchor_line(line: str) -> tuple[str, list[str]]:
    """Apply A-N-1…A-N-4 to ONE line; returns (new line, rules that matched)."""
    rules: list[str] = []
    new = line
    if _ANCHOR_TITLE.match(new):
        new = _ANCHOR_TITLE.sub("# Anchor:", new, count=1)
        rules.append("A-N-1")
    if _RETIRED_GOAL_PATH.search(new):
        rule = "A-N-3" if re.search(r"\.specify/goal/", new) else "A-N-2"
        new = _RETIRED_GOAL_PATH.sub(".specify/anchoring", new)
        rules.append(rule)
    if rules and _RETIRED_COMMAND.search(new):
        new = _RETIRED_COMMAND.sub("/speckit.anchor", new)
        rules.append("A-N-4")
    return new, rules


def _map_anchor_body(body: str, *, first_line: int = 1,
                     path: str = "") -> tuple[str, list[dict]]:
    out: list[str] = []
    records: list[dict] = []
    for offset, line in enumerate(body.splitlines(keepends=True)):
        new, rules = _map_anchor_line(line)
        if new != line:
            records.append({"path": path, "line": first_line + offset,
                            "rule": "+".join(rules),
                            "before": line.rstrip("\n"), "after": new.rstrip("\n")})
        out.append(new)
    return "".join(out), records


def _extract_targets_section(lines: list[str]) -> tuple[int | None, int, list[dict]]:
    """Locate the `## Targets` section and parse its rows (C-38 / FR-040)."""
    start = None
    end = len(lines)
    for index, line in enumerate(lines):
        if line.strip() == _SECTION_TARGETS:
            start = index
            for later in range(index + 1, len(lines)):
                if lines[later].startswith("## "):
                    end = later
                    break
            break
    if start is None:
        return None, end, []
    targets: list[dict] = []
    for line in lines[start + 1:end]:
        stripped = line.strip()
        if not stripped or stripped == _TARGETS_HEADER or stripped == _TARGETS_SEPARATOR:
            continue
        match = _TARGET_ROW.match(stripped)
        if not match:
            # FR-040: a line the grammar cannot carry would be dropped — hard failure.
            raise GoalInvalid(
                "migration-target-loss: the ## Targets section holds a line the table "
                f"grammar cannot carry ({stripped!r}); refusing rather than dropping it")
        targets.append({"id": match.group(1), "statement": match.group(2),
                        "status": match.group(3)})
    return start, end, targets


def _map_goal_body(body: str) -> tuple[str, list[dict], bool]:
    """C-38 action-goal mapping: the two section renames plus Targets re-rendering."""
    renamed: list[str] = []
    for line in body.splitlines(keepends=True):
        stripped = line.strip()
        renamed.append(_GOAL_HEADING_MAP[stripped] + "\n"
                       if stripped in _GOAL_HEADING_MAP else line)
    start, end, targets = _extract_targets_section(renamed)
    if start is None:
        return "".join(renamed), [], False
    if not targets:
        return "".join(renamed[:start] + renamed[end:]), [], True
    block = ([f"{GOAL_SECTION_MIGRATED}\n", "\n"]
             + [f"- {row['statement']}\n" for row in targets] + ["\n"])
    return "".join(renamed[:start] + block + renamed[end:]), targets, True


def _remove_section(body: str, heading: str) -> str:
    out: list[str] = []
    skipping = False
    for line in body.split("\n"):
        if line.strip() == heading:
            skipping = True
            continue
        if skipping and line.startswith("## "):
            skipping = False
        if not skipping:
            out.append(line)
    return "\n".join(out)


def _normalized_projection(text: str) -> str:
    lines = [line.rstrip() for line in
             text.replace("\r\n", "\n").replace("\r", "\n").split("\n")]
    return "\n".join(lines).strip("\n") + "\n"


def concept_projection(text: str, *, mapping: str) -> str:
    """C-39 — the digest input. `mapping` is the class the entry is acted under."""
    meta, _start, _end = read_frontmatter_subset(text)
    rows = [f"status: {str(meta.get('status') or '')}",
            f"created: {str(meta.get('created') or '')}",
            f"updated: {str(meta.get('updated') or '')}"]
    values = _binding_values(text)
    rows.append(_render_binding_block(values).rstrip("\n")
                if values is not None else "(no binding block)")
    _frontmatter, body = _frontmatter_span(text)
    if mapping == "action-goal":
        body, _targets, _present = _map_goal_body(body)
    elif mapping == "anchor":
        body, _records = _map_anchor_body(body)
    body = _remove_section(body, _SECTION_TARGETS)
    body = _remove_section(body, GOAL_SECTION_MIGRATED)
    return _normalized_projection("\n\n".join(["\n".join(rows), body]))


def migration_digest(text: str, *, mapping: str) -> str:
    return hashlib.sha256(
        concept_projection(text, mapping=mapping).encode("utf-8")).hexdigest()


# ---- planning --------------------------------------------------------------

def _cleanup_paths(repo_root: Path, entry: dict) -> dict:
    slug = entry["slug"]
    source_dir = anchor_root(repo_root) / slug
    source = source_dir / "goal.md"
    if entry["class"] == "anchor":
        target = source_dir / "anchor.md"
        receipt = source_dir / BODY_RECEIPT_NAME
    elif entry["class"] == "action-goal":
        target = goals_root(repo_root) / slug / "goal.md"
        receipt = target.parent / MIGRATION_RECEIPT_NAME
    else:
        target_dir = _cleanup_archive_root(repo_root) / slug
        target = target_dir / "goal.md"
        receipt = target_dir / MIGRATION_RECEIPT_NAME
    return {"source_dir": source_dir, "source": source, "target": target,
            "receipt": receipt}


def _read_json_file(path: Path) -> dict | None:
    if not path.is_file():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        raise GoalInvalid(f"invalid-state: {path} exists but cannot be read as a receipt")


def _plan_anchor_entry(repo_root: Path, entry: dict, paths: dict) -> dict:
    slug, source, target = entry["slug"], paths["source"], paths["target"]
    if source.is_file() and target.is_file():
        raise GoalInvalid(
            f"conflict: {_relative(repo_root, source)} and "
            f"{_relative(repo_root, target)} both exist; the rename would overwrite one "
            "of them, so nothing is written")
    if target.is_file():
        text = target.read_text(encoding="utf-8")
    elif source.is_file():
        text = source.read_text(encoding="utf-8")
    else:
        raise GoalNotFound(
            f"source-missing: {_relative(repo_root, source)} is declared but absent and "
            f"no receipt at {_relative(repo_root, paths['receipt'])} explains it")
    _front, body = _frontmatter_span(text)
    _mapped, records = _map_anchor_body(
        body, first_line=text[:len(text) - len(body)].count("\n") + 1,
        path=_relative(repo_root, target))
    receipt = _read_json_file(paths["receipt"])
    if target.is_file():
        after = migration_digest(text, mapping="anchor")
        if receipt is None:
            if records:
                return {"kind": "anchor", "slug": slug, "action": "normalize",
                        "result": "normalize",
                        "source_path": _relative(repo_root, source),
                        "target_path": _relative(repo_root, target),
                        "note": "receipt absent; the normalization resumes",
                        "_paths": paths}
            return {"kind": "anchor", "slug": slug, "action": "noop",
                    "result": "already-normalized",
                    "source_path": _relative(repo_root, source),
                    "target_path": _relative(repo_root, target), "_paths": paths}
        recorded = receipt.get("concept_digest_after_normalization")
        if recorded != after:
            raise GoalInvalid(
                f"conflict: {_relative(repo_root, target)} does not match its body receipt "
                f"{_relative(repo_root, paths['receipt'])} (recorded digest {recorded}, "
                f"measured {after}); the file is not rewritten")
        return {"kind": "anchor", "slug": slug, "action": "noop",
                "result": "already-normalized",
                "source_path": _relative(repo_root, source),
                "target_path": _relative(repo_root, target), "_paths": paths}
    return {"kind": "anchor", "slug": slug,
            "action": "rename+normalize" if records else "rename",
            "result": "rename+normalize" if records else "rename",
            "source_path": _relative(repo_root, source),
            "target_path": _relative(repo_root, target), "_paths": paths,
            "_records": records}


def _plan_move_entry(repo_root: Path, entry: dict, paths: dict, *,
                     action: str, mapping: str, move_summary: bool) -> dict:
    """Shared C-41 state table for the two moving classes.

    `source present, target present, no receipt` is a resumable state (C-42): the target
    is re-derived from the source and the move continues. A receipt-less target with no
    source is the half state C-41 refuses (I5).
    """
    slug, source, target = entry["slug"], paths["source"], paths["target"]
    receipt = _read_json_file(paths["receipt"])
    base = {"kind": entry["class"], "slug": slug,
            "source_path": _relative(repo_root, source),
            "target_path": _relative(repo_root, target), "_paths": paths,
            "_action_name": action, "_mapping": mapping,
            "_move_summary": move_summary}

    source_text = source.read_text(encoding="utf-8") if source.is_file() else None
    source_digest = (migration_digest(source_text, mapping=mapping)
                     if source_text is not None else None)
    if source_text is not None:
        body = _frontmatter_span(source_text)[1]
        if mapping == "action-goal":
            _mapped, targets, _present = _map_goal_body(body)
            if len(targets) != entry["targets"]:
                raise GoalInvalid(
                    f"migration-target-loss: {_relative(repo_root, source)} declares "
                    f"{entry['targets']} Target(s) but {len(targets)} could be carried "
                    "into the migration; a migration that drops a statement is a hard "
                    "failure (FR-040)")
        else:
            targets = _parse_targets_text(_section(body, _SECTION_TARGETS))

    if target.is_file():
        target_digest = migration_digest(target.read_text(encoding="utf-8"),
                                         mapping=mapping)
        if receipt is None:
            if source_text is None:
                raise GoalInvalid(
                    f"half-state: {_relative(repo_root, target)} exists without "
                    f"{_relative(repo_root, paths['receipt'])} and its source is gone; "
                    "a receipt-less target is a defect the action refuses to bless "
                    "(C-41 I5)")
            if target_digest != source_digest:
                raise GoalInvalid(
                    f"conflict: {_relative(repo_root, source)} and "
                    f"{_relative(repo_root, target)} hold different concept payloads "
                    f"({source_digest} vs {target_digest}); no winner is picked and "
                    "nothing is written")
            base.update({"action": "resume-receipt", "result": action,
                         "resumed_at": "write-receipt",
                         "_source_text": source_text, "_source_digest": source_digest,
                         "_targets": targets, "_resume": "write-receipt"})
            return base
        recorded = receipt.get("concept_digest_target")
        if recorded != target_digest:
            raise GoalInvalid(
                f"conflict: {_relative(repo_root, target)} does not match its receipt "
                f"{_relative(repo_root, paths['receipt'])} (recorded digest {recorded}, "
                f"measured {target_digest}); both paths are named and nothing is rewritten")
        if source_text is None:
            return {**base, "action": "noop",
                    "result": CLEANUP_DONE_RESULTS[action]}
        if source_digest != target_digest:
            raise GoalInvalid(
                f"conflict: {_relative(repo_root, source)} and "
                f"{_relative(repo_root, target)} hold different concept payloads "
                f"({source_digest} vs {target_digest}); no winner is picked")
        base.update({"action": "resume-remove",
                     "result": CLEANUP_DONE_RESULTS[action],
                     "resumed_at": "remove-source",
                     "_targets": targets, "_resume": "remove-source"})
        return base

    if source_text is None:
        raise GoalNotFound(
            f"source-missing: {_relative(repo_root, source)} is declared but absent and "
            f"no receipt at {_relative(repo_root, paths['receipt'])} explains it")
    if target.parent.exists():
        raise GoalInvalid(
            f"conflict: {_relative(repo_root, target.parent)} already exists without "
            f"{_relative(repo_root, target)}; the migration refuses to merge into it")
    base.update({"action": action, "result": action,
                 "_source_text": source_text, "_source_digest": source_digest,
                 "_targets": targets})
    return base


def _plan_cleanup_entry(repo_root: Path, entry: dict) -> dict:
    paths = _cleanup_paths(repo_root, entry)
    if entry["class"] == "anchor":
        return _plan_anchor_entry(repo_root, entry, paths)
    if entry["class"] == "action-goal":
        return _plan_move_entry(repo_root, entry, paths, action="migrate",
                                mapping="action-goal", move_summary=True)
    return _plan_move_entry(repo_root, entry, paths, action="archive",
                            mapping="obsolete", move_summary=False)


# ---- applying --------------------------------------------------------------

def _fault_cleanup() -> str | None:
    value = os.environ.get(CLEANUP_FAULT_ENV)
    return value if value in CLEANUP_FAULT_STEPS else None


def _migration_receipt_body(row: dict, *, digest_source: str, digest_target: str,
                            summary: str, phase: str = "complete") -> dict:
    return {
        "schema": MIGRATION_RECEIPT_SCHEMA,
        "action": RECEIPT_ACTIONS[row["_action_name"]],
        "source_path": row["source_path"],
        "target_path": row["target_path"],
        "concept_digest_source": digest_source,
        "concept_digest_target": digest_target,
        "mapping_version": CLEANUP_MAPPING_VERSION,
        "result_identity": row["slug"],
        "engine": _engine_identity(),
        "timestamp": _utc_now(),
        "delete_policy": DELETE_POLICY,
        "targets": row.get("_targets", []),
        "summary": summary,
        "phase": phase,
    }


def _move_summary_tree(source_dir: Path, target_dir: Path) -> str:
    summary = source_dir / SUMMARY_DIRNAME
    if not summary.is_dir():
        return "absent"
    destination = target_dir / SUMMARY_DIRNAME
    if destination.exists():
        raise GoalInvalid(
            f"conflict: summary trees exist at both {summary} and {destination}; the "
            "move refuses to merge or overwrite them")
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(summary), str(destination))
    return "moved"


def _write_json(path: Path, body: dict) -> None:
    _atomic_write_text(path, json.dumps(body, ensure_ascii=False, indent=2) + "\n")


def _apply_anchor(repo_root: Path, row: dict) -> None:
    paths = row["_paths"]
    source, target = paths["source"], paths["target"]
    if source.is_file() and not target.is_file():
        # C-38 sub-step 1: the rename changes the file name and nothing else.
        source.rename(target)
    text = target.read_text(encoding="utf-8")
    front, body = _frontmatter_span(text)
    mapped_body, records = _map_anchor_body(
        body, first_line=front.count("\n") + 1, path=row["target_path"])
    if not records:
        return
    before_digest = migration_digest(text, mapping="anchor")
    after_digest = migration_digest(front + mapped_body, mapping="anchor")
    if before_digest != after_digest:
        raise GoalInvalid(
            f"digest-mismatch: normalizing {row['target_path']} changed the concept "
            f"projection ({before_digest} -> {after_digest}); the source is left as it was")
    _atomic_write_text(target, front + mapped_body)
    _write_json(paths["receipt"], {
        "schema": BODY_RECEIPT_SCHEMA,
        "action": "anchor-body-normalization",
        "path": row["target_path"],
        "concept_digest_before_normalization": before_digest,
        "concept_digest_after_normalization": after_digest,
        "engine": _engine_identity(),
        "timestamp": _utc_now(),
        "lines": records,
    })
    row["normalized_lines"] = len(records)


def _apply_move(repo_root: Path, row: dict) -> None:
    paths = row["_paths"]
    source, target = paths["source"], paths["target"]
    fault = _fault_cleanup()
    action = row["action"]
    if action == "noop":
        return
    if action in ("migrate", "archive", "resume-receipt"):
        if not target.is_file():
            # C-42 `write-target`: the archive copy is the whole tree, the migration's
            # is the mapped definition.
            if row["_action_name"] == "archive":
                if target.parent.exists():
                    raise GoalInvalid(
                        f"conflict: {_relative(repo_root, target.parent)} exists; the "
                        "archive copy refuses to overwrite it")
                target.parent.parent.mkdir(parents=True, exist_ok=True)
                shutil.copytree(paths["source_dir"], target.parent)
            else:
                text = row["_source_text"]
                front, body = _frontmatter_span(text)
                mapped_body, _targets, _present = _map_goal_body(body)
                target.parent.mkdir(parents=True, exist_ok=True)
                _atomic_write_text(target, front + mapped_body)
            if fault == "write-target":
                raise _CleanupInterrupted("write-target", row)
        if row["_move_summary"]:
            if (paths["source_dir"] / SUMMARY_DIRNAME).is_dir():
                row["summary"] = _move_summary_tree(paths["source_dir"], target.parent)
            elif (target.parent / SUMMARY_DIRNAME).is_dir():
                row["summary"] = "moved"
            else:
                row["summary"] = "absent"
        else:
            row["summary"] = ("moved" if (target.parent / SUMMARY_DIRNAME).is_dir()
                              else "absent")
        if not paths["receipt"].is_file():
            # C-42 `write-receipt`: never before the target, never after the removal.
            if row.get("_source_digest") is None:
                row["_source_digest"] = migration_digest(
                    source.read_text(encoding="utf-8"), mapping=row["_mapping"])
            target_digest = migration_digest(target.read_text(encoding="utf-8"),
                                             mapping=row["_mapping"])
            if row["_source_digest"] != target_digest:
                raise GoalInvalid(
                    f"digest-mismatch: {row['source_path']} projects to "
                    f"{row['_source_digest']} but {row['target_path']} projects to "
                    f"{target_digest}; the source is not removed")
            _write_json(paths["receipt"], _migration_receipt_body(
                row, digest_source=row["_source_digest"],
                digest_target=target_digest, summary=row["summary"]))
            if fault == "write-receipt":
                raise _CleanupInterrupted("write-receipt", row)
    if row["_action_name"] == "archive":
        # The whole tree moved; the source copy goes only after the target + receipt exist.
        if paths["source_dir"].is_dir():
            shutil.rmtree(paths["source_dir"])
        elif source.is_file():
            source.unlink()
    else:
        if source.is_file():
            source.unlink()
        try:
            paths["source_dir"].rmdir()
        except OSError:
            row["source_dir_remaining"] = _relative(repo_root, paths["source_dir"])


def _cleanup_public(row: dict) -> dict:
    return {key: value for key, value in row.items() if not key.startswith("_")}


def cleanup_store(repo_root: Path, *, apply: bool, classification_path: Path) -> dict:
    """C-29 / C-36…C-45 — plan every entry, then (on apply) act in C-42 phase order."""
    repo_root = Path(repo_root)
    data = load_classification(repo_root, Path(classification_path))
    decisions = [_plan_cleanup_entry(repo_root, entry) for entry in data["entries"]]
    decisions.sort(key=lambda row: (row["kind"], row["slug"]))

    interrupted: dict | None = None
    if apply:
        done: list[dict] = []
        for row in decisions:
            try:
                if row["kind"] == "anchor":
                    _apply_anchor(repo_root, row)
                else:
                    _apply_move(repo_root, row)
            except _CleanupInterrupted as exc:
                receipt_path = exc.row["_paths"]["receipt"]
                interrupted = {
                    "result": "interrupted",
                    "error": (f"interrupted: {exc.row['kind']} {exc.row['slug']!r} stopped "
                              f"after the {exc.phase} phase; a second call resumes at "
                              f"the next phase ({', '.join(CLEANUP_PHASES)})"),
                    "reached_phase": exc.phase,
                    "target_path": exc.row["target_path"],
                    "receipt_path": _relative(repo_root, receipt_path),
                    "target_exists": exc.row["_paths"]["target"].is_file(),
                }
                row_copy = dict(_cleanup_public(row))
                row_copy["result"] = "interrupted"
                done.append(row_copy)
                decisions = done
                break
            done.append(row)
        else:
            decisions = done

    results = sorted({row["result"] for row in decisions})
    payload: dict = {
        "action": "cleanup",
        "mode": "apply" if apply else "check",
        "decisions": [_cleanup_public(row) for row in decisions],
        "counts": {name: sum(1 for row in decisions if row["result"] == name)
                   for name in results},
    }
    if interrupted:
        payload.update(interrupted)
    return payload


# --------------------------------------------------------------------------
# 094 — declaration-driven read actions (command family, handoff decision)
#
# Both actions read their values through the declaration layer's one parser and
# delegate the class predicate to `flow-class-check.py`'s lookup; neither keeps a
# second copy of any table. Authority: contracts/command-family-and-declarations.md
# C-71…C-87 in `.specify/specs/094-goal-team-parallel/`.
# --------------------------------------------------------------------------

FAMILY_FACT_SLUG = "goal-team-command-family"
HANDOFF_FACT_SLUG = "goal-team-handoff-threshold"
UNIT_ID_PREFIX = "/speckit."
FLOW_CLASS_ENGINE = "flow-class-check.py"
DECLARED_SUBSET = "declaration-subset/v1"
DEGRADED_OWNER = "owner-unavailable"
DECLARATION_INVALID = "declaration-invalid"
TASK_ROW_LINE = re.compile(r"^- \[[ xX>~]\]\s+\S+")


def _declaration_reader():
    """The declaration layer's one read entry, importable beside this engine."""
    here = str(Path(__file__).resolve().parent)
    if here not in sys.path:
        sys.path.insert(0, here)
    try:
        import declaration_reader
    except ImportError:
        return None
    return declaration_reader


def _load_registered_fact(repo_root: Path, slug: str):
    """(body, registration, None, None) or (None, None, label, detail).

    C-83 — an absent layer, an absent fact and a fact the contract does not
    register are the same refusal at the consumer: `owner-unavailable`, never a
    default. The registration row is returned so the action validates against the
    declared domain instead of a private copy (C-84/C-85).
    """
    reader = _declaration_reader()
    if reader is None:
        return None, None, DEGRADED_OWNER, \
            "declaration_reader.py is not importable beside this engine"
    try:
        contract = reader.load_contract(str(repo_root))
    except (reader.DeclarationError, OSError) as exc:
        return None, None, DEGRADED_OWNER, str(exc)
    registration = None
    declared = contract.get("registered_facts")
    for row in declared if isinstance(declared, list) else []:
        if isinstance(row, dict) and str(row.get("fact", "")).strip() == slug:
            registration = row
            break
    if registration is None:
        return None, None, DEGRADED_OWNER, \
            f"fact {slug!r} is not registered in shared/declarations/contract.yaml"
    try:
        body = reader.load_fact(str(repo_root), slug)["body"]
    except (reader.DeclarationError, OSError) as exc:
        return None, None, DEGRADED_OWNER, str(exc)
    if not isinstance(body, dict):
        return None, None, DEGRADED_OWNER, f"fact {slug!r} does not parse as a mapping"
    return body, registration, None, None


def _registration_problem(registration: dict, expected_domain: str):
    """C-84/C-85 — a fact is read only under the grammar and domain it registers."""
    subset = str(registration.get("subset_id", "")).strip()
    if subset != DECLARED_SUBSET:
        return (f"fact registers grammar {subset!r}, but the shared reader implements "
                f"{DECLARED_SUBSET!r}")
    domain = str(registration.get("value_domain", "")).strip()
    if domain != expected_domain:
        return (f"fact registers value domain {domain!r}, but this consumer validates "
                f"{expected_domain!r}")
    return None


def _flow_class_lookup(repo_root: Path, unit_id: str):
    """(record, label, detail, exit) — the class engine's lookup, never a second table."""
    engine = Path(__file__).resolve().parent / FLOW_CLASS_ENGINE
    try:
        proc = subprocess.run(
            [sys.executable, str(engine), "--action", "lookup", "--unit-id", unit_id,
             "--repo", str(repo_root), "--format", "json"],
            capture_output=True, text=True)
    except OSError as exc:
        return None, "lookup-unavailable", str(exc), EXIT_INPUT_ERROR
    record = None
    if proc.stdout.strip():
        try:
            record = json.loads(proc.stdout)
        except json.JSONDecodeError:
            record = None
    if proc.returncode != 0 or not isinstance(record, dict):
        error = (record or {}).get("error") or {}
        label = str(error.get("label") or "lookup-unavailable")
        detail = str(error.get("detail") or proc.stderr.strip()
                     or "the class lookup produced no JSON record")
        return record, label, detail, EXIT_INPUT_ERROR
    return record, None, None, EXIT_OK


def command_family(repo_root: Path, command: str):
    """(payload, exit) for `command-family --command <name>` (C-71…C-77).

    The verdict is `source: ledger` and nothing else — `flow_class` and the exit
    code are not criteria (C-71). The declared addition list can only add a name
    whose carrier exists (C-77); an absent carrier keeps a command out of the
    family without failing the read (C-72/C-75), and a degraded lookup refuses
    with exit 2 rather than guessing.
    """
    repo_root = Path(repo_root)
    unit_id = f"{UNIT_ID_PREFIX}{command}"
    body, registration, label, detail = _load_registered_fact(repo_root, FAMILY_FACT_SLUG)
    additions: list[str] = []
    if body is not None:
        problem = _registration_problem(registration, "closed-set")
        statement = body.get("statement")
        if problem is None and not isinstance(statement, list):
            problem = "the family statement is not a sequence (the addition list)"
        if problem is None:
            orphans = [str(name) for name in statement
                       if "/" in str(name)
                       or not (repo_root / "templates" / "commands" / f"{name}.md").is_file()]
            if orphans:
                problem = ("declared addition(s) without a carrier under "
                           f"templates/commands/: {', '.join(orphans)}")
        if problem is not None:
            body, label, detail = None, DECLARATION_INVALID, problem
        else:
            additions = [str(name) for name in statement]
    record, lookup_label, lookup_detail, lookup_exit = _flow_class_lookup(repo_root, unit_id)
    carrier = (repo_root / "templates" / "commands" / f"{command}.md").is_file()
    payload = {
        "command": command,
        "unit_id": unit_id,
        "in_family": False,
        "source": (record or {}).get("source"),
        "flow_class": (record or {}).get("flow_class"),
        "marker": (record or {}).get("marker"),
    }
    if body is None:
        payload["error"] = {"label": label, "detail": detail}
        return payload, EXIT_INPUT_ERROR
    if lookup_exit != EXIT_OK:
        payload["error"] = {"label": lookup_label, "detail": lookup_detail}
        return payload, EXIT_INPUT_ERROR
    payload["in_family"] = bool(carrier and (payload["source"] == "ledger"
                                             or command in additions))
    return payload, EXIT_OK


def handoff_decision(repo_root: Path, tasks_path: Path):
    """(payload, exit) for `handoff-decision --tasks <path>` (C-79…C-82).

    One declared statement answers both questions: `task_count > threshold` is
    `handoff` (equality stays `direct`), and the creation-timing pair is carried
    through untouched. An absent or unregistered fact exits 2 as
    `owner-unavailable` and never falls back to a built-in number (C-81/C-83).
    """
    payload = {"decision": None, "task_count": None, "threshold": None,
               "creation": {"on_direct": None, "on_handoff": None}}
    try:
        text = Path(tasks_path).read_text(encoding="utf-8")
    except OSError as exc:
        payload["error"] = {"label": "tasks-unreadable", "detail": str(exc)}
        return payload, EXIT_INPUT_ERROR
    payload["task_count"] = sum(1 for line in text.splitlines()
                                if TASK_ROW_LINE.match(line))
    body, registration, label, detail = _load_registered_fact(repo_root, HANDOFF_FACT_SLUG)
    if body is None:
        payload["error"] = {"label": label, "detail": detail}
        return payload, EXIT_INPUT_ERROR
    problem = _registration_problem(registration, "threshold+timing-map")
    statement = body.get("statement")
    if problem is None and not isinstance(statement, dict):
        problem = "the threshold statement is not a mapping"
    if problem is None:
        metric = statement.get("metric")
        raw_threshold = statement.get("threshold")
        boundary = statement.get("boundary")
        if metric != "task-count":
            problem = f"metric {metric!r} is not the implemented 'task-count'"
        elif not re.fullmatch(r"[0-9]+", str(raw_threshold)):
            problem = f"threshold {raw_threshold!r} is not an integer literal"
        elif boundary != "exclusive":
            problem = f"boundary {boundary!r} is not the implemented 'exclusive'"
        elif statement.get("on_direct") is None or statement.get("on_handoff") is None:
            problem = "the creation-timing pair is incomplete"
    if problem is not None:
        payload["error"] = {"label": DECLARATION_INVALID, "detail": problem}
        return payload, EXIT_INPUT_ERROR
    threshold = int(str(raw_threshold))
    payload["threshold"] = threshold
    payload["decision"] = "handoff" if payload["task_count"] > threshold else "direct"
    payload["creation"] = {"on_direct": statement.get("on_direct"),
                           "on_handoff": statement.get("on_handoff")}
    return payload, EXIT_OK


# --------------------------------------------------------------------------
# 094 — handoff contract keys (C-58/C-59): validate both keys, write the reverse refs
# --------------------------------------------------------------------------

HANDOFF_REF_KEY = "handoff_ref"
HANDOFF_DANGLING = "handoff-dangling-key"


def _with_handoff_ref(text: str, ref: str, path: Path) -> tuple[str, bool]:
    """Set one `handoff_ref` frontmatter line; every other byte is preserved (C-6/C-59)."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise GoalError(
            f"handoff-ref-unwritable: {path} carries no frontmatter; the reverse key "
            "cannot be written without one")
    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration:
        raise GoalError(
            f"handoff-ref-unwritable: {path}'s frontmatter is unterminated") from None
    key = f"{HANDOFF_REF_KEY}:"
    wanted = f"{key} {ref}"
    hits = [i for i in range(1, end) if lines[i].startswith(key)]
    if len(hits) > 1:
        raise GoalError(
            f"handoff-ref-unwritable: {path} carries {len(hits)} handoff_ref lines; "
            "the engine refuses to guess which one is the reverse key")
    if hits and lines[hits[0]] == wanted:
        return text, False
    if hits:
        rewritten = lines[:hits[0]] + [wanted] + lines[hits[0] + 1:]
    else:
        rewritten = lines[:end] + [wanted] + lines[end:]
    new_text = "\n".join(rewritten)
    if text.endswith("\n"):
        new_text += "\n"
    return new_text, True


def handoff_ref(repo_root: Path, handoff_path: Path) -> dict:
    """`handoff-ref --handoff <path>` (C-58/C-59): validate the keys, write the refs.

    `goal_slug` and `team_slug` must each resolve to an archive definition; an
    unresolvable one is `handoff-dangling-key` (exit 2) naming the value, because a
    contract never names a goal or team that does not exist. Once both resolve, each
    definition gains exactly one `handoff_ref` pointing back at this contract; every
    other byte of each file stays identical (C-6's discipline applied to C-59).
    """
    repo_root = Path(repo_root)
    handoff_path = Path(handoff_path)
    try:
        text = handoff_path.read_text(encoding="utf-8")
    except OSError as exc:
        raise GoalError(
            f"handoff-unreadable: {handoff_path} ({exc.strerror or exc})") from None
    meta, _start, _end = read_frontmatter_subset(text)
    resolved: dict[str, Path] = {}
    unresolved: list[str] = []
    for key, layer, filename in (("goal_slug", ARCHIVE_DIRNAME, definition_filename("anchor")),
                                 ("team_slug", TEAM_DIRNAME, "team.md")):
        value = str(meta.get(key) or "").strip()
        path = (Path(repo_root) / layer / value / filename
                if is_valid_identity(value) else None)
        if path is None or not path.is_file():
            unresolved.append(f"{key} {value!r}")
        else:
            resolved[key] = path
    if unresolved:
        raise GoalError(
            f"{HANDOFF_DANGLING}: " + ", ".join(unresolved)
            + f" resolves to no definition under {ARCHIVE_DIRNAME}/ or {TEAM_DIRNAME}/; "
            "a handoff contract never names a goal or team that does not exist (C-58)")
    try:
        ref = handoff_path.resolve().relative_to(repo_root.resolve()).as_posix()
    except ValueError:
        raise GoalError(
            f"handoff-outside-repo: {handoff_path} is not inside {repo_root}; the "
            "reverse key is a repo-relative path (C-59)") from None
    written = []
    for kind, key in (("goal", "goal_slug"), ("team", "team_slug")):
        path = resolved[key]
        original = path.read_text(encoding="utf-8")
        rewritten, changed = _with_handoff_ref(original, ref, path)
        if changed:
            path.write_text(rewritten, encoding="utf-8")
        written.append({"kind": kind, "slug": str(meta.get(key)).strip(),
                        "path": str(path.relative_to(repo_root)), "changed": changed})
    return {"action": "handoff-ref", "handoff": ref, "refs": written}


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

def _resolve(repo_root: Path, target: str) -> Path:
    candidate = Path(target)
    if candidate.is_file():
        return candidate
    return definition_path(repo_root, target)


# --version, wired through the one version source (C-8)
#
# `guard_argv()` answers `--version` (and rejects an undeclared option) BEFORE any parser
# reads the line, so it works for a flat argparse parser, for one whose subcommands are
# required, and for the two modules that read sys.argv by hand. It writes nothing and
# resolves `<script-name> <framework-version>` from the nearest pyproject.toml at run
# time — this file carries no version literal. `--help` is left to the module's own body.
import sys as _sig_sys  # noqa: E402
import pathlib as _sig_pathlib

_SIG_DIR = str(_sig_pathlib.Path(__file__).resolve().parent)
if _SIG_DIR not in _sig_sys.path:
    _sig_sys.path.insert(0, _SIG_DIR)
try:  # the helper owns the rule; an engine copied WITHOUT it still runs its actions
    from script_interface_cli import configure_parser as _sig_configure  # noqa: E402
    from script_interface_cli import guard_argv as _sig_guard  # noqa: E402
except ImportError:  # a sandbox/handler copy carries the engine but not the helper
    def _sig_configure(parser, **_kwargs):
        return parser

    def _sig_guard(_argv=None, declared=None, **_kwargs):
        return None

def _run_archive_action(args, repo_root: Path) -> int:
    """Dispatch the 094 archive actions; they span both archive layers and therefore
    bypass the single-layer `--scope` resolution (C-31 applies to them directly)."""
    try:
        if args.action == "probe-residual":
            payload = probe_residual(repo_root)
        elif args.action == "migrate-archive":
            payload = migrate_archive(repo_root, apply=bool(args.apply))
        else:
            payload = backfill_bindings(repo_root, apply=bool(args.apply))
    except GoalNotFound as exc:
        _emit({"error": str(exc)}, args.json)
        return EXIT_NOT_FOUND
    except GoalInvalid as exc:
        _emit({"error": str(exc)}, args.json)
        return EXIT_INVALID
    except GoalError as exc:
        _emit({"error": str(exc)}, args.json)
        return EXIT_INPUT_ERROR
    _emit(payload, args.json)
    if payload.get("result") == "interrupted":
        # C-39: exit 3, distinguishable from 0 (complete) and 2 (input error).
        return EXIT_NOT_FOUND
    if "error" in payload:
        return EXIT_INVALID
    return EXIT_OK


def _run_cleanup_action(args, repo_root: Path) -> int:
    """Dispatch the cleanup group; its exit codes are C-30's single meanings."""
    try:
        payload = cleanup_store(repo_root, apply=bool(args.apply),
                                classification_path=Path(args.classification))
    except GoalNotFound as exc:
        _emit({"error": str(exc)}, args.json)
        return EXIT_NOT_FOUND
    except GoalInvalid as exc:
        _emit({"error": str(exc)}, args.json)
        return EXIT_INVALID
    except GoalError as exc:
        _emit({"error": str(exc)}, args.json)
        return EXIT_INPUT_ERROR
    _emit(payload, args.json)
    if payload.get("result") == "interrupted":
        return EXIT_NOT_FOUND
    return EXIT_OK


def _run_declaration_action(args, repo_root: Path) -> int:
    """Dispatch the 094 declaration read actions; they touch no archive layer."""
    if args.action == "command-family":
        payload, code = command_family(repo_root, args.command_name)
    else:
        payload, code = handoff_decision(repo_root, Path(args.tasks_path))
    _emit(payload, args.json)
    return code


def _run_handoff_action(args, repo_root: Path) -> int:
    """Dispatch `handoff-ref`; it addresses both archive layers directly (C-58/C-59)."""
    try:
        payload = handoff_ref(repo_root, Path(args.handoff_path))
    except GoalNotFound as exc:
        _emit({"error": str(exc)}, args.json)
        return EXIT_NOT_FOUND
    except GoalInvalid as exc:
        _emit({"error": str(exc)}, args.json)
        return EXIT_INVALID
    except GoalError as exc:
        _emit({"error": str(exc)}, args.json)
        return EXIT_INPUT_ERROR
    _emit(payload, args.json)
    return EXIT_OK


def main(argv: list[str] | None = None) -> int:
    _sig_guard(argv, declared=['--repo-root', '--json', '--scope', '--spec-dir', '--team', '--objective', '--title', '--criterion', '--boundary', '--set', '--clear', '--drop-inline', '--add', '--check', '--list', '--id', '--target', '--owner', '--owner-id', '--origin', '--dry-run', '--apply', '--command', '--tasks', '--handoff', '--classification', '--guidance', '--done', '--clear-done'])  # answer --version / reject an undeclared option
    # Shared flags are attached to BOTH the top-level parser and every subparser. That does
    # NOT make them position-independent, and the comment here used to claim it did: argparse
    # lets a subparser overwrite a namespace attribute the top level already set, so
    # `goal-utils.py --json list` silently emits the human form and `--repo-root X list`
    # silently resolves to the cwd. Measured 2026-10-04 (both orders compared through _emit).
    # Pass these flags AFTER the action. Fixing the precedence would change behavior for all
    # ten actions, which is outside 053's declared scope — escalated as research.md A-9 of
    # spec 053-machine-decidable-artifacts, and pinned as measured by test_run_checks.py C-11
    # so it cannot change silently in either direction.
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--repo-root", default=None, help="repository root (default: cwd)")
    common.add_argument("--json", action="store_true", help="machine-readable output")
    common.add_argument("--scope", choices=ARCHIVE_SCOPES, default=None,
                        help="archive layer: anchor (.specify/anchoring/anchor.md), "
                             "goals (.specify/goals/goal.md), teams (.specify/teams/), "
                             "or auto (read-only single-layer resolution); the closed "
                             "member set is owned by shared/definitions/"
                             "anchor-definitions.md § Archive Layers")
    common.add_argument("--spec-dir", default=None,
                        help="the spec directory used to resolve origin and validate auto "
                             "inputs (repo-relative or absolute); never decides a landing point")

    parser = argparse.ArgumentParser(
        description="Definition engine — stores anchor.md in the .specify/anchoring "
                    "archive, goal.md in the .specify/goals archive, and team.md in "
                    ".specify/teams/.",
        parents=[common],
    )
    _sig_configure(parser)
    sub = parser.add_subparsers(dest="action", required=True)

    p_scope = sub.add_parser("resolve-scope", parents=[common],
                             help="read: resolve the anchor/goals/teams/auto archive-layer roots")
    p_scope.add_argument("--team", default=None, help="optional team slug for identity-aware auto")

    p_create = sub.add_parser("create", parents=[common],
                              help="write: add a new definition to the anchoring archive")
    p_create.add_argument("slug")
    p_create.add_argument("--objective", required=True)
    p_create.add_argument("--title", default=None, metavar="TEXT",
                          help="human-readable heading; falls back to the slug")
    p_create.add_argument("--criterion", action="append", default=[])
    p_create.add_argument("--boundary", action="append", default=[], metavar="TEXT",
                          help="an explicit exclusion, rendered under ## Boundaries")

    p_validate = sub.add_parser("validate", parents=[common],
                                help="read: validate one definition")
    p_validate.add_argument("target", help="goal slug or path to goal.md")

    p_check_stmt = sub.add_parser(
        "check-statement", parents=[common],
        help="read: standalone dry-run shape validation of one Target statement "
             "(GD-2/GD-3); requires NO goal — usable before `create`")
    p_check_stmt.add_argument("statement", help="candidate Target statement")

    sub.add_parser("list", parents=[common],
                   help="read: enumerate the anchoring archive")

    p_status = sub.add_parser("status", parents=[common],
                              help="write: change lifecycle state")
    p_status.add_argument("slug")
    p_status.add_argument("--set", dest="target_state", required=True,
                          choices=LIFECYCLE_STATES)

    p_objective = sub.add_parser("objective", parents=[common],
                                 help="write: replace the objective, recording the prior value")
    p_objective.add_argument("slug")
    p_objective.add_argument("--set", dest="new_objective", required=True, metavar="TEXT",
                             help="the replacement objective (outcome-shaped; GD-2/GD-3 apply)")

    p_criteria = sub.add_parser(
        "criteria", parents=[common],
        help="write: replace criteria, recording the prior value "
             "(destructive when emptied via --clear)")
    p_criteria.add_argument("slug")
    p_criteria.add_argument("--criterion", action="append", default=[])
    p_criteria.add_argument("--clear", dest="clear_criteria", action="store_true",
                            help="deliberately empty the criteria set — overwrites the "
                                 f"existing criteria with {NO_CRITERIA_MARKER!r}")

    p_migrate = sub.add_parser("migrate", parents=[common],
                               help="write: derive a definition from a team's inline goal "
                                    "and reference it")
    p_migrate.add_argument("team_slug")
    p_migrate.add_argument("--drop-inline", action="store_true",
                           help="remove the team's inline goal after migrating (default: keep)")

    p_bind = sub.add_parser("bind", parents=[common],
                            help="write: rewrite one definition's binding record "
                                 "(owner / owner_id / origin); every other byte is preserved")
    p_bind.add_argument("kind", choices=("goal", "team", "teams"),
                        help="the archive layer the definition lives in")
    p_bind.add_argument("slug")
    p_bind.add_argument("--owner", required=True,
                        help="sdd-run / command-run / human (validated by the engine)")
    p_bind.add_argument("--owner-id", dest="owner_id", required=True,
                        help="the state-spine run_id, or the literal 'human' for owner: human")
    p_bind.add_argument("--origin", default=None,
                        help="null or an existing .specify/specs/<dir> basename; omit to keep")

    p_binding = sub.add_parser("binding", parents=[common],
                               help="read: answer who owns one definition, from its "
                                    "binding record (zero writes)")
    p_binding.add_argument("kind", choices=("goal", "team", "teams"),
                           help="the archive layer the definition lives in")
    p_binding.add_argument("slug")

    p_targets = sub.add_parser("targets", parents=[common],
                               help="read (--list/--check) | write (--add/--set): the "
                                    "Targets of one goal (038)")
    p_targets.add_argument("slug")
    p_targets.add_argument("--add", dest="add_statement", default=None,
                           metavar="STATEMENT", help="append a new open Target")
    p_targets.add_argument("--check", dest="check_statement", default=None,
                           metavar="STATEMENT",
                           help="dry-run statement validation; zero writes (042)")
    p_targets.add_argument("--list", dest="list_targets", action="store_true",
                           help="list every Target, machine-parseable lines")
    p_targets.add_argument("--set", dest="set_state", default=None,
                           choices=TARGET_STATES, help="transition one Target")
    p_targets.add_argument("--id", dest="target_id", default=None,
                           metavar="T-NNN", help="Target identity paired with --set")

    p_run_checks = sub.add_parser(
        "run-checks", parents=[common],
        help="read: the five run-precondition checks for one team, in a single call "
             "(zero writes; 053)")
    p_run_checks.add_argument("team_slug", metavar="<team-slug>",
                              help="team directory name under .specify/teams/")
    p_run_checks.add_argument("--target", dest="run_target", default=None,
                              metavar="T-NNN",
                              help="T-<nnn> or <goal-slug>.T-<nnn>; omit to resolve via "
                                   "team.md focus_target")

    sub.add_parser(
        "probe-residual", parents=[common],
        help="read: enumerate the spec-local goal/team residuals (zero writes; 094)")

    p_family = sub.add_parser(
        "command-family", parents=[common],
        help="read: is a /speckit.<command> run in the goal/team command family? "
             "(zero writes; 094)")
    p_family.add_argument("--command", dest="command_name", required=True,
                          metavar="NAME",
                          help="the command stem to judge, e.g. feedback")

    p_handoff = sub.add_parser(
        "handoff-decision", parents=[common],
        help="read: direct | handoff from the declared task-count threshold "
             "(zero writes; 094)")
    p_handoff.add_argument("--tasks", dest="tasks_path", required=True, metavar="PATH",
                           help="path to the tasks file whose task rows are counted")

    p_handoff_ref = sub.add_parser(
        "handoff-ref", parents=[common],
        help="write: validate a handoff contract's goal_slug/team_slug and write the "
             "reverse handoff_ref on both definitions (094; C-58/C-59)")
    p_handoff_ref.add_argument("--handoff", dest="handoff_path", required=True,
                               metavar="PATH",
                               help="path to the handoff contract whose two keys are "
                                    "validated before either reverse key is written")

    p_migrate_archive = sub.add_parser(
        "migrate-archive", parents=[common],
        help="write: move spec-local definitions into the unified archive "
             "(archive-not-delete; explicit action, never implicit; 094)")
    archive_mode = p_migrate_archive.add_mutually_exclusive_group(required=True)
    archive_mode.add_argument("--dry-run", dest="dry_run", action="store_true",
                              help="perform every read and decision, print the plan and "
                                   "the receipt bodies, and write nothing")
    archive_mode.add_argument("--apply", dest="apply", action="store_true",
                              help="write the target, move the source tree, write the receipt")

    p_backfill = sub.add_parser(
        "backfill-bindings", parents=[common],
        help="write: insert the recorded binding (human / human / null) on archive "
             "residents that carry none (explicit action, never implicit; 094)")
    backfill_mode = p_backfill.add_mutually_exclusive_group(required=True)
    backfill_mode.add_argument("--dry-run", dest="dry_run", action="store_true",
                               help="print the per-definition plan and write nothing")
    backfill_mode.add_argument("--apply", dest="apply", action="store_true",
                               help="insert the binding record on every unbound resident")

    # C-28 — the action-level Goal group: a separate, clearly named group in this one
    # executable; it writes `.specify/goals/<slug>/goal.md` and nothing else.
    p_goal_create = sub.add_parser(
        "goal-create", parents=[common],
        help="write: add an action-level Goal to .specify/goals/<goal-slug>/goal.md "
             "(requires at least one --done; guidance gets no GD-2 shape check)")
    p_goal_create.add_argument("slug")
    p_goal_create.add_argument("--guidance", required=True, metavar="TEXT",
                               help="the practical action this Goal guides (step-shaped "
                                    "text is accepted)")
    p_goal_create.add_argument("--done", dest="done", action="append", default=[],
                               metavar="TEXT",
                               help="one verifiable completion condition; repeatable, "
                                    "at least one required")
    p_goal_create.add_argument("--title", default=None, metavar="TEXT",
                               help="human-readable heading; falls back to the slug")

    sub.add_parser("goal-list", parents=[common],
                   help="read: enumerate the action-level Goal store")

    p_goal_view = sub.add_parser("goal-view", parents=[common],
                                 help="read: render one action-level Goal (exit 3 when absent)")
    p_goal_view.add_argument("slug")

    p_goal_modify = sub.add_parser(
        "goal-modify", parents=[common],
        help="write: change guidance or completion conditions, recording the prior value")
    p_goal_modify.add_argument("slug")
    p_goal_modify.add_argument("--guidance", default=None, metavar="TEXT")
    p_goal_modify.add_argument("--done", dest="done", action="append", default=[],
                               metavar="TEXT", help="replacement completion conditions")
    p_goal_modify.add_argument("--clear-done", dest="clear_done", action="store_true",
                               help="deliberately empty the completion conditions")

    p_goal_status = sub.add_parser(
        "goal-status", parents=[common],
        help="read (no --set) | write (--set): shared lifecycle; terminal is retained")
    p_goal_status.add_argument("slug")
    p_goal_status.add_argument("--set", dest="target_state", default=None,
                               choices=LIFECYCLE_STATES)

    # C-29 — the cleanup group: its own name, its own input, `--scope` inapplicable.
    p_cleanup = sub.add_parser(
        "cleanup", parents=[common],
        help="read (--check) | write (--apply): the classified definition cleanup "
             "(anchor rename/normalization, action-goal migration, obsolete archival)")
    cleanup_mode = p_cleanup.add_mutually_exclusive_group(required=True)
    cleanup_mode.add_argument("--check", dest="check", action="store_true",
                              help="perform every read and decision; write nothing")
    cleanup_mode.add_argument("--apply", dest="apply", action="store_true",
                              help="execute the plan in the declared phase order")
    p_cleanup.add_argument("--classification", required=True, metavar="PATH",
                           help="the classification record read verbatim "
                                "(schema 101-classification/v1)")

    args = parser.parse_args(argv)
    repo_root = Path(args.repo_root or ".").resolve()
    if getattr(args, "kind", None) == "team":
        # `team` is the singular spelling the 094 peer-lines fixture addresses the
        # team row with; the closed layer value stays `teams` everywhere downstream.
        args.kind = "teams"

    if args.action in ("probe-residual", "migrate-archive", "backfill-bindings"):
        return _run_archive_action(args, repo_root)
    if args.action in ("command-family", "handoff-decision"):
        return _run_declaration_action(args, repo_root)
    if args.action == "handoff-ref":
        return _run_handoff_action(args, repo_root)
    if args.action == "cleanup":
        # C-29 — the group spans the stores it cleans by design; a layer selector would
        # contradict that, so it is refused before any read or write.
        if args.scope is not None:
            _emit({"error": "scope-not-applicable: the cleanup group spans the anchor, "
                            "Goal and archive stores by design; --scope does not apply to "
                            "it and nothing is written"}, args.json)
            return EXIT_INPUT_ERROR
        return _run_cleanup_action(args, repo_root)

    global _ACTIVE_SCOPE
    _ACTIVE_SCOPE = None
    write_action = args.action in ("create", "status", "objective", "criteria",
                                   "migrate", "bind", "goal-create", "goal-modify",
                                   "goal-status")
    if args.action == "targets":
        write_action = bool(args.add_statement or args.set_state)
    if args.action == "goal-status":
        write_action = args.target_state is not None
    requested_scope = args.scope
    if requested_scope is None:
        if args.action == "resolve-scope":
            requested_scope = "auto"
        elif args.action == "run-checks":
            requested_scope = "teams"
        elif args.action in ("bind", "binding"):
            # The legacy actions keep their own kind vocabulary; only `--scope` is the
            # closed four-member surface, so the old kind names translate here instead
            # of being retired out from under an existing caller.
            requested_scope = {"goal": "anchor", "team": "teams",
                               "teams": "teams"}[args.kind]
        elif args.action in GOAL_ACTIONS:
            requested_scope = "goals"
        else:
            requested_scope = "anchor"
    if requested_scope == "auto" and write_action:
        _emit({"error": "scope-read-only: --scope auto resolves a single archive layer "
                        "for reads only; name the layer with --scope anchor, --scope "
                        "goals or --scope teams for a write"},
              args.json)
        return EXIT_INPUT_ERROR
    team_slug = getattr(args, "team_slug", None) or getattr(args, "team", None)
    identity_slug = team_slug or getattr(args, "slug", None)
    try:
        scope_obj = resolve_scope(repo_root, requested_scope, args.spec_dir, identity_slug)
    except ScopeError as exc:
        _emit({"error": str(exc)}, args.json)
        return EXIT_INPUT_ERROR
    if args.action == "resolve-scope":
        _emit(scope_obj.as_dict(team_slug), args.json)
        return EXIT_OK
    # C-16 — a write may not target a layer other than the one its definition resolves
    # to; the two layers are named so the caller can correct the address.
    action_layer = None
    if args.action in ("bind", "binding"):
        action_layer = {"goal": "anchor", "team": "teams",
                        "teams": "teams"}[args.kind]
    elif args.action == "run-checks":
        action_layer = "teams"
    elif args.action in GOAL_ACTIONS:
        action_layer = "goals"
    elif write_action:
        action_layer = "anchor"
    if write_action and action_layer and scope_obj.scope != action_layer:
        _emit({"error": f"cross-layer-write: this write targets the {scope_obj.scope} "
                        f"archive layer but the definition resolves to the {action_layer} "
                        "archive layer; both layers are named so the caller can address "
                        "the right one"},
              args.json)
        return EXIT_INPUT_ERROR
    _ACTIVE_SCOPE = scope_obj

    try:
        if args.action == "create":
            path = create_goal(repo_root, args.slug, args.objective, args.criterion,
                               title=args.title, boundaries=args.boundary)
            result = {"created": str(path.relative_to(repo_root))}
        elif args.action == "validate":
            path = _resolve(repo_root, args.target)
            ok, problems = validate_goal(path, repo_root)
            result = {"valid": ok, "problems": problems, "path": str(path)}
            if not ok:
                _emit(result, args.json)
                return EXIT_INVALID
        elif args.action == "list":
            result = {"goals": list_goals(repo_root)}
        elif args.action == "status":
            path = _resolve(repo_root, args.slug)
            if not path.is_file():
                _emit({"error": f"goal not found: {args.slug}"}, args.json)
                return EXIT_NOT_FOUND
            set_status(path, args.target_state)
            result = {"slug": args.slug, "status": args.target_state}
        elif args.action == "objective":
            path = _resolve(repo_root, args.slug)
            if not path.is_file():
                _emit({"error": f"goal not found: {args.slug}"}, args.json)
                return EXIT_NOT_FOUND
            set_objective(path, args.new_objective)
            result = {"slug": args.slug,
                      "objective": " ".join(args.new_objective.split())}
        elif args.action == "criteria":
            path = _resolve(repo_root, args.slug)
            if not path.is_file():
                _emit({"error": f"goal not found: {args.slug}"}, args.json)
                return EXIT_NOT_FOUND
            # Exit 2, never a read fallback: `criteria` is a write, so an argument-less
            # call is a malformed write — silently downgrading it to a read would hide
            # the dropped flag and leave the caller believing the criteria were shown.
            if not args.criterion and not args.clear_criteria:
                _emit({"error": "criteria replaces the whole set: pass --criterion at "
                                "least once, or --clear to empty it deliberately. "
                                "An argument-less call would overwrite the existing "
                                "criteria with an empty set."}, args.json)
                return EXIT_INPUT_ERROR
            set_criteria(path, list(args.criterion))
            result = {"slug": args.slug, "criteria": list(args.criterion),
                      "cleared": bool(args.clear_criteria)}
        elif args.action == "migrate":
            created, identity = migrate_team(
                repo_root, args.team_slug, keep_inline=not args.drop_inline)
            result = {"migrated_team": args.team_slug, "goal_slug": identity,
                      "created": str(created.relative_to(repo_root)),
                      "inline_kept": not args.drop_inline}
        elif args.action == "bind":
            origin_given = args.origin is not None
            origin = None if args.origin in (None, "null") else args.origin
            path, binding = bind_definition(
                repo_root, args.kind, args.slug, args.owner, args.owner_id,
                origin, origin_given)
            result = {"kind": args.kind, "slug": args.slug, "binding": binding,
                      "path": str(path.relative_to(repo_root))}
        elif args.action == "binding":
            result = binding_payload(repo_root, args.kind, args.slug)
        elif args.action == "check-statement":
            # Standalone pre-creation path (F-E12): `targets <slug> --check`
            # needs an existing goal (exit 3 without one), which made the
            # dry-run unusable exactly when it is most needed — before
            # `create`. This runs the SAME-source shape grammar
            # (_reject_bad_target_statement: GD-2/GD-3, zero writes); the
            # criteria-restatement comparison needs the goal's criteria and
            # stays with `targets <slug> --check` after creation.
            try:
                _reject_bad_target_statement(args.statement)
            except GoalError as exc:
                _emit({"verdict": "rejected", "error": str(exc),
                       "scope": "shape-only"}, args.json)
                return EXIT_INPUT_ERROR
            result = {"verdict": "ok", "scope": "shape-only",
                      "note": "criteria-restatement check requires the goal's "
                              "criteria — run `targets <slug> --check` after "
                              "creation for the full verdict"}
        elif args.action == "targets":
            path = definition_path(repo_root, args.slug)
            if not path.is_file():
                _emit({"error": f"goal not found: {args.slug} — to validate a "
                                "statement BEFORE the goal exists, use "
                                "`check-statement \"<statement>\"` "
                                "(shape-only: GD-2/GD-3)"}, args.json)
                return EXIT_NOT_FOUND
            chosen = [args.add_statement is not None, args.list_targets,
                      args.set_state is not None, args.check_statement is not None]
            if sum(chosen) != 1:
                _emit({"error": "targets expects exactly one of --add / --check / --list / --set"},
                      args.json)
                return EXIT_INPUT_ERROR
            if args.check_statement is not None:
                # 042 dry-run: same-source validation as --add, zero writes.
                data = parse_goal(path)
                if data["status"] in TERMINAL_STATES:
                    _emit({"verdict": "goal-terminal",
                           "error": f"goal is in terminal state {data['status']!r} "
                                    "(终态 goal 只读); a proposal has nowhere to land"},
                          args.json)
                    return EXIT_INVALID
                try:
                    _validate_target_statement(data, args.check_statement)
                except GoalError as exc:
                    _emit({"verdict": "rejected", "error": str(exc),
                           "scope": TARGET_CHECK_SCOPE}, args.json)
                    return EXIT_INPUT_ERROR
                result = {"slug": args.slug, "verdict": "ok",
                          "scope": TARGET_CHECK_SCOPE}
            elif args.list_targets:
                targets = parse_goal(path)["targets"]
                if args.json:
                    result = {"targets": targets}
                else:
                    for row in targets:
                        print(f"{row['id']}\t{row['status']}\t{row['statement']}")
                    return EXIT_OK
            elif args.add_statement is not None:
                tid = add_target(path, args.add_statement)
                result = {"slug": args.slug, "added": tid}
            else:  # --set
                if not args.target_id:
                    _emit({"error": "--set must be paired with --id"}, args.json)
                    return EXIT_INPUT_ERROR
                set_target_status(path, args.target_id, args.set_state)
                result = {"slug": args.slug, "id": args.target_id,
                          "status": args.set_state}
        elif args.action == "run-checks":
            payload = run_checks(repo_root, args.team_slug, args.run_target)
            _emit(payload, args.json)
            if payload["verdict"] == "input-error":
                return EXIT_INPUT_ERROR
            return EXIT_BLOCKED if payload["blocked"] else EXIT_OK
        elif args.action == "goal-create":
            path = create_action_goal(repo_root, args.slug, args.guidance,
                                      list(args.done), title=args.title)
            result = {"created": _relative(repo_root, path), "slug": args.slug,
                      "status": "active"}
        elif args.action == "goal-list":
            result = {"goals": list_action_goals(repo_root)}
        elif args.action == "goal-view":
            path = _resolve_action_goal(repo_root, args.slug)
            data = parse_action_goal(path)
            data["path"] = _relative(repo_root, path)
            result = data
        elif args.action == "goal-modify":
            path = _resolve_action_goal(repo_root, args.slug)
            if args.clear_done and args.done:
                _emit({"error": "--clear-done and --done contradict each other in one "
                                "call; pass one of them"}, args.json)
                return EXIT_INPUT_ERROR
            if args.guidance is None and not args.done and not args.clear_done:
                _emit({"error": "goal-modify needs at least one of --guidance / --done / "
                                "--clear-done; an argument-less call would be a write "
                                "with no instruction"}, args.json)
                return EXIT_INPUT_ERROR
            result = modify_action_goal(
                path, guidance=args.guidance,
                conditions=list(args.done) if args.done else None,
                clear=args.clear_done)
            result["path"] = _relative(repo_root, path)
        elif args.action == "goal-status":
            path = _resolve_action_goal(repo_root, args.slug)
            result = action_goal_status(path, args.target_state)
        else:  # pragma: no cover - argparse guards this
            parser.error(f"unknown action {args.action}")
    except GoalNotFound as exc:
        _emit({"error": str(exc)}, args.json)
        return EXIT_NOT_FOUND
    except GoalInvalid as exc:
        # The definition exists but cannot be interpreted, which is neither a bad argument
        # (2) nor a blocked run (5): 053 C-18 requires the three tiers be distinguishable.
        _emit({"error": str(exc)}, args.json)
        return EXIT_INVALID
    except GoalError as exc:
        _emit({"error": str(exc)}, args.json)
        return EXIT_INPUT_ERROR
    finally:
        # The scope is per invocation; a leaked value would redirect a later
        # direct API call (e.g. a fixture's create_goal) into the wrong root.
        _ACTIVE_SCOPE = None

    _emit(result, args.json)
    return EXIT_OK


def _emit(payload: dict, as_json: bool) -> None:
    if as_json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return
    if "error" in payload:
        print(f"error: {payload['error']}", file=sys.stderr)
        return
    if "goals" in payload:
        if not payload["goals"]:
            print("(no definitions in this archive layer)")
            return
        if "done_count" in payload["goals"][0]:
            for row in payload["goals"]:
                print(f"{row['slug']:<32} {row['status']:<10} "
                      f"done={row['done_count']:<3} updated={row['updated']}")
            return
        for row in payload["goals"]:
            print(f"{row['slug']:<32} {row['status']:<10} "
                  f"criteria={row['criteria_count']:<3} updated={row['updated']}")
        return
    if "problems" in payload:
        print("valid" if payload["valid"] else "INVALID")
        for problem in payload["problems"]:
            print(f"  - {problem}")
        return
    if "checks" in payload and "team_slug" in payload:
        res = payload.get("resolution") or {}
        print(f"team: {payload['team_slug']}   goal: {payload['goal_slug']}   "
              f"identity: {payload['identity_kind']}")
        print(f"target: {res.get('effective')}   source: {res.get('source')}   "
              f"declared focus: {res.get('declared_focus')}")
        for row in payload["checks"]:
            tail = f" — {row['message']}" if row["message"] else ""
            print(f"  {row['id']}. {row['name']:<16} {row['verdict']}{tail}")
        print(f"verdict: {payload['verdict']}   blocked: "
              f"{str(payload['blocked']).lower()}")
        return
    if "residuals" in payload:
        for heading, kind in (("goal", "goal"), ("team", "teams")):
            print(f"## {heading}")
            for path in payload["residuals"][kind]:
                print(path)
            print(f"count={payload['counts'][kind]}")
        return
    if "decisions" in payload:
        for row in payload["decisions"]:
            print(f"{row['kind']}\t{row['slug']}\t{row['result']}\t"
                  f"{row.get('source_path', '')} -> {row.get('target_path', '')}")
        counts = payload.get("counts") or {}
        if counts:
            print("counts: " + " ".join(f"{name}={value}"
                                        for name, value in counts.items()))
        return
    if "definitions" in payload:
        for row in payload["definitions"]:
            print(f"{row['result']}\t{row['path']}")
        return
    if "refs" in payload:
        for row in payload["refs"]:
            state = "updated" if row["changed"] else "already-set"
            print(f"{row['kind']}\t{state}\t{row['path']}")
        return
    for key, value in payload.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    raise SystemExit(main())
