#!/usr/bin/env python3
"""team-view.py — deterministic read-only reader behind `/speckit.team view` (103-team-view).

Owner of the fixed-rule extraction for the view mode: team definition facts, archive
enumeration, report listing, ledger aggregation and the latest-report summary. Binding and
anchor facts are composed from the goal-utils reads (`binding`, `list`, `targets --list`);
this program re-implements none of their semantics and writes nothing.

Contract: `.specify/specs/103-team-view/contracts/team-view-program.contract.md`
(C-24 read-only, C-25 engine composition, C-26 closed CLI surface, C-27 script interface,
C-28 closed exit codes, C-29 output modes).

Usage:
  team-view.py [options] [<team-slug>]

Exit codes:
  0  rendering produced (single team, overview, empty archive, dangling binding)
  2  input error (undeclared option, invalid --scope, extra positional, no-slug --scope auto)
  3  team not found (single mode)
  4  definition corrupt (single mode: team.md missing, unreadable or unparseable)
  5  rendered, but a required fact group is unreadable because an engine read failed

Python >= 3.8, standard library only; the only sibling import is ``script_interface_cli``.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

EXIT_OK = 0
EXIT_INPUT = 2
EXIT_NOT_FOUND = 3
EXIT_CORRUPT = 4
EXIT_DEGRADED = 5

APPROVED_EXIT_CODES = (EXIT_OK, EXIT_INPUT, EXIT_NOT_FOUND, EXIT_CORRUPT, EXIT_DEGRADED)

SCOPE_VALUES = ("teams", "auto", "anchor", "goals")
DEFAULT_SCOPE = "teams"

PROGRAM_NAME = "team-view.py"

DECLARED_OPTIONS = (
    "--repo-root",
    "--scope",
    "--spec-dir",
    "--json",
)

try:  # pragma: no cover - exercised through every CLI test
    from script_interface_cli import (
        VersionAction,
        configure_parser,
        preparse_version_guard,
        version_text,
    )
except ImportError:  # pragma: no cover - the helper ships beside this file
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from script_interface_cli import (  # type: ignore[no-redef]
        VersionAction,
        configure_parser,
        preparse_version_guard,
        version_text,
    )


def resolve_repo_root(explicit: str | None) -> Path:
    """The repository root: the explicit option, or derived from this file's own path.

    Two Hats rule (`shared/definitions/dogfooding-definitions.md` § 2.1): self-location
    may fire only on a literal ``.specify`` component of this file's own resolved path
    (the mirror copy). The framework-source copy `<repo>/scripts/python/team-view.py`
    takes the plain three-level parent instead; walking up to "any ancestor containing
    .specify" is forbidden because it self-matches in this repository. A derived root
    named ``.specify`` is never a repository root.
    """
    if explicit:
        return Path(explicit).expanduser().resolve()
    own = Path(__file__).resolve()
    parts = own.parts
    if ".specify" in parts[:-1]:
        index = parts.index(".specify")
        root = Path(*parts[:index]) if index > 0 else Path(parts[0])
    else:
        root = own.parents[2]
    while root.name == ".specify":
        root = root.parent
    return root


def resolve_scope(requested, team_slug):
    """Return ``(effective_scope, error_message)`` for the closed ``--scope`` surface.

    ``teams`` is serviced; ``auto`` is serviced only for a single slug (a no-slug ``auto``
    is not decidable); ``anchor`` / ``goals`` are refused by name as not applicable to the
    team archive layer. A value the team archive cannot serve is reported, never ignored.
    """
    value = requested or DEFAULT_SCOPE
    if value == "teams":
        return "teams", None
    if value == "auto":
        if team_slug is None:
            return value, (
                "--scope auto 不可用于无 slug 的概览：auto 需要且仅需要单个 team slug"
                " 以解析团队身份；请改用 --scope teams 或提供一个 slug"
            )
        return value, None
    return value, (
        "--scope %s 对 view 不适用：view 只在团队档案层（teams）解析团队，"
        "无法服务的取值必须显式报告；请改用 --scope teams（或单 slug 的 --scope auto）"
        % value
    )


# --------------------------------------------------------------------------- #
# Presentation vocabulary (owner: data-model.md § Rendering Line Types)
# --------------------------------------------------------------------------- #
STATE_MISSING = "缺失"
STATE_EMPTY = "为空"
STATE_UNREADABLE = "不可读"
STATE_UNRECORDED = "未记录"
STATE_MALFORMED = "形态异常"
STATE_DANGLING = "悬空（dangling）"
STATE_CORRUPT = "定义损坏"
STATE_UNDECLARED = "未声明"
STATE_LISTED = "已列出"
STATE_FOLDED = "已聚合"
DEFAULT_POINTER = "（默认值见 create-mode.md § Schema notes）"
NESTED_NONE = "本次无嵌套 SDD 调用"
TRUNCATION_MARKER = "…（截断）"

EXCERPT_LINE_CAP = 10
EXCERPT_CHAR_CAP = 800
REPORT_SHOWN_CAP = 20
SLUG_LIST_CAP = 20

REPORT_NAME_RE = re.compile(r"^(\d{8}T\d{6}Z)-report\.md$")
REQUIRED_MATRIX_COLUMNS = ("role", "stage", "type")
SPINE_FILES = ("constraints.md", "STATE.md", "run-log.jsonl")
LEDGER_STATES = ("completed", "in-progress", "delayed", "not-started", "unknown")
LEDGER_TERMINAL_STATES = ("completed",)

SCHEMA_KEYS = (
    "slug", "name", "description", "lifecycle_state", "anchor_slug", "goal_slug",
    "handoff_ref", "binding", "created", "updated", "pattern", "config",
    "members", "seats", "stage_seats", "focus_target", "territory", "preset",
)
OPTIONAL_SCHEMA_KEYS = (
    "lifecycle_state", "anchor_slug", "focus_target", "territory", "preset",
    "seats", "stage_seats",
)

_MISSING = object()


class Facts(dict):
    """Parsed frontmatter facts; an absent key reads ``None`` without being invented."""

    def __missing__(self, key):
        return None


# --------------------------------------------------------------------------- #
# Closed-subset frontmatter parser (C-35)
# --------------------------------------------------------------------------- #
def _strip_inline_comment(text: str) -> str:
    quote = None
    for index, char in enumerate(text):
        if quote:
            if char == quote:
                quote = None
            continue
        if char in "\"'":
            quote = char
            continue
        if char == "#" and index > 0 and text[index - 1] in " \t":
            return text[:index].rstrip()
    return text


def _split_flow(body: str) -> list:
    parts, current, depth, quote = [], [], 0, None
    for char in body:
        if quote:
            current.append(char)
            if char == quote:
                quote = None
            continue
        if char in "\"'":
            quote = char
            current.append(char)
            continue
        if char in "[{":
            depth += 1
        elif char in "]}":
            depth -= 1
        if char == "," and depth == 0:
            parts.append("".join(current).strip())
            current = []
            continue
        current.append(char)
    tail = "".join(current).strip()
    if tail:
        parts.append(tail)
    return parts


def _parse_scalar(text: str, problems: dict, key: str):
    value = _strip_inline_comment(text.strip())
    if value == "":
        return None
    if value[0] in "|>":
        problems[key] = STATE_UNREADABLE
        return _MISSING
    if value[0] == '"':
        try:
            return json.loads(value)
        except ValueError:
            problems[key] = STATE_UNREADABLE
            return _MISSING
    if value[0] == "'":
        if len(value) >= 2 and value.endswith("'"):
            return value[1:-1].replace("''", "'")
        problems[key] = STATE_UNREADABLE
        return _MISSING
    if value.startswith("["):
        if not value.endswith("]"):
            problems[key] = STATE_UNREADABLE
            return _MISSING
        inner = value[1:-1].strip()
        if not inner:
            return []
        items = []
        for part in _split_flow(inner):
            item = _parse_scalar(part, problems, key)
            if item is _MISSING:
                return _MISSING
            items.append(item)
        return items
    if value.startswith("{"):
        if not value.endswith("}"):
            problems[key] = STATE_UNREADABLE
            return _MISSING
        inner = value[1:-1].strip()
        result = Facts()
        if not inner:
            return result
        for part in _split_flow(inner):
            sub_key, sep, sub_rest = part.partition(":")
            if not sep or not sub_key.strip():
                problems[key] = STATE_MALFORMED
                return _MISSING
            parsed = _parse_scalar(sub_rest, problems, key)
            if parsed is _MISSING:
                return _MISSING
            result[sub_key.strip().strip("\"'")] = parsed
        return result
    lowered = value.lower()
    if lowered in ("true", "false"):
        return lowered == "true"
    if lowered in ("null", "~"):
        return None
    if re.fullmatch(r"[-+]?\d+", value):
        return int(value)
    if re.fullmatch(r"[-+]?\d+\.\d+", value):
        return float(value)
    return value


def _indent_of(line: str) -> int:
    return len(line) - len(line.lstrip(" "))


def _next_content(lines: list, index: int):
    while index < len(lines):
        stripped = lines[index].strip()
        if stripped and not stripped.startswith("#"):
            return index
        index += 1
    return None


def _skip_deeper(lines: list, index: int, indent: int) -> int:
    while index < len(lines):
        if not lines[index].strip():
            index += 1
            continue
        if _indent_of(lines[index]) <= indent:
            return index
        index += 1
    return len(lines)


def _item_block(lines: list, index: int, content_indent: int):
    parent_indent = _indent_of(lines[index])
    block = [" " * content_indent + lines[index].strip()[2:].strip()]
    cursor = index + 1
    while cursor < len(lines):
        line = lines[cursor]
        if not line.strip():
            lookahead = _next_content(lines, cursor)
            if lookahead is None or _indent_of(lines[lookahead]) <= parent_indent:
                break
            block.append("")
            cursor += 1
            continue
        if _indent_of(line) <= parent_indent:
            break
        block.append(line)
        cursor += 1
    return block, cursor


def _parse_sequence(lines: list, index: int, indent: int, problems: dict):
    items = []
    cursor = index
    while True:
        idx = _next_content(lines, cursor)
        if idx is None:
            return items, len(lines)
        current = _indent_of(lines[idx])
        content = lines[idx].strip()
        if current < indent or current > indent or not content.startswith("- "):
            return items, idx
        item_text = content[2:].strip()
        if item_text == "":
            cursor = idx + 1
            continue
        if item_text.startswith("{"):
            value = _parse_scalar(item_text, problems, "item")
            if value is not _MISSING:
                items.append(value)
            cursor = idx + 1
            continue
        key, sep, _rest = item_text.partition(":")
        first_key = key.strip()
        starts_quoted = item_text[0] in "\"'["
        looks_like_map = (
            bool(sep) and not starts_quoted
            and re.fullmatch(r"[A-Za-z0-9_.-]+", first_key) is not None
        )
        if not looks_like_map:
            value = _parse_scalar(item_text, problems, "item")
            if value is not _MISSING:
                items.append(value)
            cursor = idx + 1
            continue
        block, cursor = _item_block(lines, idx, indent + 2)
        item, _ = _parse_mapping(block, 0, indent + 2, problems)
        items.append(item)


def _parse_mapping(lines: list, index: int, indent: int, problems: dict):
    data = Facts()
    while True:
        idx = _next_content(lines, index)
        if idx is None:
            return data, len(lines)
        line = lines[idx]
        current = _indent_of(line)
        content = line.strip()
        if current < indent:
            return data, idx
        if current > indent or content.startswith("- "):
            index = idx + 1
            continue
        key, sep, rest = content.partition(":")
        key = key.strip()
        if not sep or not key:
            index = idx + 1
            continue
        raw_value = _strip_inline_comment(rest.strip())
        if key in data:
            problems[key] = STATE_MALFORMED
            data.pop(key, None)
            index = _skip_deeper(lines, idx + 1, current)
            continue
        if raw_value == "":
            nxt = _next_content(lines, idx + 1)
            if nxt is not None and _indent_of(lines[nxt]) > current:
                nested_indent = _indent_of(lines[nxt])
                if lines[nxt].strip().startswith("- "):
                    value, index = _parse_sequence(lines, nxt, nested_indent, problems)
                else:
                    value, index = _parse_mapping(lines, nxt, nested_indent, problems)
                data[key] = value
            else:
                data[key] = None
                index = idx + 1
            continue
        if re.fullmatch(r"[|>][+-]?\d*", raw_value):
            problems[key] = STATE_UNREADABLE
            index = _skip_deeper(lines, idx + 1, current)
            continue
        value = _parse_scalar(raw_value, problems, key)
        if value is _MISSING:
            index = _skip_deeper(lines, idx + 1, current)
            continue
        data[key] = value
        index = idx + 1


def parse_frontmatter(text: str):
    """Parse ``team.md``'s frontmatter inside the closed subset (C-35).

    Returns ``(facts, problems)``: a fact outside the subset is reported in
    ``problems`` under its key and never guessed; an absent key stays absent.
    """
    problems = {}
    lines = text.splitlines()
    fence_start = None
    for index, line in enumerate(lines):
        if not line.strip():
            continue
        if line.strip() == "---":
            fence_start = index
        break
    if fence_start is None:
        problems["frontmatter"] = STATE_MISSING
        return Facts(), problems
    fence_end = None
    for index in range(fence_start + 1, len(lines)):
        if lines[index].strip() == "---":
            fence_end = index
            break
    if fence_end is None:
        problems["frontmatter"] = STATE_MALFORMED
        return Facts(), problems
    data, _ = _parse_mapping(lines[fence_start + 1:fence_end], 0, 0, problems)
    return data, problems


def definition_body(text: str) -> str:
    """Everything after the closing frontmatter fence (the whole text if unfenced)."""
    lines = text.splitlines()
    fence_start = None
    for index, line in enumerate(lines):
        if not line.strip():
            continue
        if line.strip() == "---":
            fence_start = index
        break
    if fence_start is None:
        return text
    for index in range(fence_start + 1, len(lines)):
        if lines[index].strip() == "---":
            return "\n".join(lines[index + 1:])
    return ""


def is_definition_corrupt(problems: dict) -> bool:
    """Corrupt = no readable definition identity at all (C-28 exit 4)."""
    return "frontmatter" in problems or "slug" in problems


# --------------------------------------------------------------------------- #
# Static structure matrix (E3)
# --------------------------------------------------------------------------- #
def _section_lines(text: str, heading_prefix: str):
    lines = text.splitlines()
    start = None
    for index, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("## ") and stripped[3:].strip().startswith(heading_prefix):
            start = index
            break
    if start is None:
        return None
    collected = []
    for line in lines[start + 1:]:
        if re.match(r"^#{1,3} ", line):
            break
        collected.append(line)
    return collected


def _cells(line: str) -> list:
    stripped = line.strip()
    if stripped.startswith("|"):
        stripped = stripped[1:]
    if stripped.endswith("|"):
        stripped = stripped[:-1]
    return [cell.strip() for cell in stripped.split("|")]


def parse_static_matrix(text: str):
    """Parse the ``## Static Structure`` GFM table: ``(rows, state)`` (E3, FR-009)."""
    section = _section_lines(text, "Static Structure")
    if section is None:
        return [], STATE_MISSING
    table = [line for line in section if line.strip().startswith("|")]
    if len(table) < 2:
        return [], STATE_UNREADABLE
    header = [cell.strip().lower() for cell in _cells(table[0])]
    if any(required not in header for required in REQUIRED_MATRIX_COLUMNS):
        return [], STATE_UNREADABLE
    if any(header.count(required) > 1 for required in REQUIRED_MATRIX_COLUMNS):
        return [], STATE_UNREADABLE
    rows = []
    for line in table[2:]:
        cells = _cells(line)
        if len(cells) != len(header):
            return [], STATE_MALFORMED
        rows.append({name: cell for name, cell in zip(header, cells)})
    if not rows:
        return [], STATE_EMPTY
    return rows, None


def matrix_columns(rows: list) -> list:
    order = []
    for row in rows:
        for key in row:
            if key not in order:
                order.append(key)
    return order


# --------------------------------------------------------------------------- #
# Report segments and bounded excerpt (E6, C-33)
# --------------------------------------------------------------------------- #
def _h2_sections(text: str) -> dict:
    sections = {}
    current = None
    buffer = []
    for line in text.splitlines():
        heading = re.match(r"^##\s+(.+?)\s*$", line)
        top = re.match(r"^#\s+", line)
        if heading or top:
            if current is not None:
                sections[current] = "\n".join(buffer).strip()
            current = heading.group(1) if heading else None
            buffer = []
            continue
        if current is not None:
            buffer.append(line)
    if current is not None:
        sections[current] = "\n".join(buffer).strip()
    return sections


def parse_report(text: str) -> dict:
    """Extract the latest-report fields the view renders (E6, C-33)."""
    parsed = {
        "outcome": None,
        "target_assignment": None,
        "result_summary": None,
        "verification": None,
        "nested_runs": None,
    }
    outcome = re.search(r"\*\*Outcome\*\*:\s*([^·\n]+)", text)
    if outcome:
        parsed["outcome"] = outcome.group(1).strip()
    target = re.search(r"\*\*Target 指派\*\*:\s*(.+)", text)
    if target:
        parsed["target_assignment"] = target.group(1).strip()
    sections = _h2_sections(text)
    for name, key in (
        ("Result Summary", "result_summary"),
        ("Verification", "verification"),
        ("Nested SDD Runs", "nested_runs"),
    ):
        if name in sections:
            parsed[key] = sections[name]
    return parsed


def summarize_nested(section):
    """An unrecorded anomalies field never renders as "无异常" (INV-09)."""
    if section is None or not section.strip():
        return STATE_UNRECORDED
    if NESTED_NONE in section:
        return NESTED_NONE
    for line in section.splitlines():
        match = re.search(r"anomalies:\s*(.*)$", line)
        if match:
            value = match.group(1).strip()
            return [value] if value else STATE_UNRECORDED
    return STATE_UNRECORDED


def bounded_excerpt(text):
    """First 10 non-empty lines or 800 characters, whichever hits first (C-33)."""
    if text is None:
        return None
    body = text.strip()
    if not body:
        return body
    kept = []
    truncated = False
    for line in body.splitlines():
        if not line.strip():
            continue
        if len(kept) >= EXCERPT_LINE_CAP:
            truncated = True
            break
        kept.append(line.strip())
    excerpt = "\n".join(kept)
    if len(excerpt) > EXCERPT_CHAR_CAP:
        excerpt = excerpt[:EXCERPT_CHAR_CAP]
        truncated = True
    return excerpt + TRUNCATION_MARKER if truncated else excerpt


# --------------------------------------------------------------------------- #
# Item ledger aggregation (E5, owner rule IL-2)
# --------------------------------------------------------------------------- #
def aggregate_ledger(lines) -> dict:
    """Fold the append-only ledger to each item's current state (IL-2)."""
    result = {"total_lines": 0, "bad_lines": 0, "by_state": {}, "non_terminal": []}
    last = {}
    order = []
    for position, raw in enumerate(lines):
        stripped = raw.strip() if isinstance(raw, str) else ""
        if not stripped:
            continue
        result["total_lines"] += 1
        try:
            event = json.loads(stripped)
        except ValueError:
            result["bad_lines"] += 1
            continue
        if not isinstance(event, dict):
            result["bad_lines"] += 1
            continue
        item_id = event.get("item_id")
        state = event.get("state")
        ts = event.get("ts")
        if (
            not isinstance(item_id, str) or not item_id.strip()
            or not isinstance(state, str) or state not in LEDGER_STATES
            or not isinstance(ts, str) or not ts.strip()
        ):
            result["bad_lines"] += 1
            continue
        if item_id not in last:
            order.append(item_id)
        previous = last.get(item_id)
        if previous is None or ts >= previous[0]:
            excluded = bool(str(event.get("excluded_reason") or "").strip())
            last[item_id] = (ts, position, state, excluded)
    for item_id in order:
        _ts, _position, state, excluded = last[item_id]
        result["by_state"][state] = result["by_state"].get(state, 0) + 1
        if state not in LEDGER_TERMINAL_STATES and not excluded:
            result["non_terminal"].append({"item_id": item_id, "state": state})
    return result


# --------------------------------------------------------------------------- #
# Value rendering helpers
# --------------------------------------------------------------------------- #
def _text(value):
    if value is None:
        return None
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)


def _render_value(value) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (list, tuple)):
        return "[" + ", ".join(_render_value(item) for item in value) + "]"
    if isinstance(value, dict):
        return "{" + ", ".join(
            "%s: %s" % (key, _render_value(item)) for key, item in value.items()
        ) + "}"
    return str(value)


def _flatten_config(prefix: str, value, out: list) -> None:
    if isinstance(value, dict):
        for key, item in value.items():
            _flatten_config("%s.%s" % (prefix, key), item, out)
        return
    out.append((prefix, _render_value(value)))


def _max_mtime_iso(paths) -> str:
    newest = None
    for path in paths:
        try:
            stamp = Path(path).stat().st_mtime
        except OSError:
            continue
        if newest is None or stamp > newest:
            newest = stamp
    if newest is None:
        return STATE_UNRECORDED
    return datetime.fromtimestamp(newest, timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# --------------------------------------------------------------------------- #
# Engine composition (C-25): the three declared reads only, never a write action
# --------------------------------------------------------------------------- #
def engine_read(repo_root: Path, *args):
    """Run one declared read of the sibling ``goal-utils.py`` engine."""
    script = Path(__file__).resolve().parent / "goal-utils.py"
    command = [sys.executable, str(script), *args, "--json", "--repo-root", str(repo_root)]
    try:
        proc = subprocess.run(command, capture_output=True, text=True, timeout=120)
    except OSError as exc:
        return None, None, "engine 不可执行: %s" % exc
    payload = None
    if proc.stdout.strip():
        try:
            payload = json.loads(proc.stdout)
        except ValueError:
            payload = None
    note = (proc.stderr or "").strip()
    if not note and isinstance(payload, dict) and payload.get("error"):
        note = str(payload["error"])
    return proc.returncode, payload, note


def read_binding(repo_root: Path, slug: str):
    """E2 binding: engine answer only, never parsed from the definition file."""
    code, payload, note = engine_read(repo_root, "binding", "team", slug)
    if code == 0 and isinstance(payload, dict):
        return {
            "owner": _text(payload.get("owner")),
            "owner_id": _text(payload.get("owner_id")),
            "origin": _text(payload.get("origin")),
        }, None
    return None, note or "engine 退出码 %s" % code


def read_anchor(repo_root: Path, anchor_slug: str) -> dict:
    """E7 anchor facts from ``list`` + ``targets --list``; content never copied."""
    code, payload, note = engine_read(repo_root, "list")
    if code != 0 or not isinstance(payload, dict):
        return {"state": STATE_UNREADABLE, "reason": note or "engine 退出码 %s" % code}
    goals = payload.get("goals") or []
    match = next((item for item in goals if item.get("slug") == anchor_slug), None)
    if match is None:
        return {"state": STATE_DANGLING, "reason": "engine list 未返回该 anchor slug"}
    code, payload, note = engine_read(repo_root, "targets", anchor_slug, "--list")
    if code == 3:
        return {"state": STATE_DANGLING, "reason": note or "engine targets 未找到该 anchor"}
    if code != 0 or not isinstance(payload, dict):
        return {"state": STATE_UNREADABLE, "reason": note or "engine 退出码 %s" % code}
    targets = []
    for item in payload.get("targets") or []:
        if isinstance(item, dict):
            targets.append({
                "id": _text(item.get("id")),
                "statement": _text(item.get("statement")),
                "status": _text(item.get("status")),
            })
    return {
        "state": "ok",
        "lifecycle": _text(match.get("status")),
        "criteria_count": match.get("criteria_count"),
        "updated": _text(match.get("updated")),
        "targets": targets,
    }


# --------------------------------------------------------------------------- #
# Archive readers (E2–E7 extraction)
# --------------------------------------------------------------------------- #
def _declared_block_map(value) -> dict:
    if value is None:
        return {"state": STATE_UNDECLARED}
    if isinstance(value, dict):
        return {"state": None, "entries": value}
    return {"state": STATE_MALFORMED}


def anchor_identity_of(front, slug: str) -> dict:
    """Identity resolution order owned by create-mode § Schema notes (C-36, FR-020)."""
    anchor_slug = front.get("anchor_slug")
    goal_slug = front.get("goal_slug")
    if anchor_slug:
        return {"kind": "declared", "value": _text(anchor_slug)}
    if goal_slug:
        return {"kind": "legacy", "value": _text(goal_slug)}
    return {"kind": "inferred", "value": slug}


def lifecycle_of(front) -> dict:
    value = front.get("lifecycle_state")
    if value is None:
        return {"value": "active", "declared": False}
    return {"value": _text(value), "declared": True}


def build_definition(front, problems: dict, slug: str) -> dict:
    lifecycle = lifecycle_of(front)
    anchor_identity = anchor_identity_of(front, slug)
    other_keys = []
    for key in front:
        if key not in SCHEMA_KEYS:
            other_keys.append({"key": key, "problem": problems.get(key)})
    for key, problem in problems.items():
        if key != "frontmatter" and key not in front and key not in SCHEMA_KEYS:
            other_keys.append({"key": key, "problem": problem})
    return {
        "slug": _text(front.get("slug")),
        "name": _text(front.get("name")),
        "description": _text(front.get("description")),
        "lifecycle": lifecycle,
        "anchor_identity": anchor_identity,
        "handoff_ref": _text(front.get("handoff_ref")),
        "other_keys": other_keys,
        "problems": problems,
    }


def _roster_names(values) -> list:
    names = []
    for item in values:
        if isinstance(item, dict):
            name = _text(item.get("agent"))
            if name and name not in names:
                names.append(name)
    return names


def build_static(front, body: str) -> dict:
    rows, matrix_state = parse_static_matrix(body)
    members_raw = front.get("members")
    if members_raw is None:
        members = {"state": STATE_UNDECLARED, "rows": []}
    elif isinstance(members_raw, list) and all(isinstance(item, dict) for item in members_raw):
        members = {"state": None, "rows": members_raw}
    else:
        members = {"state": STATE_MALFORMED, "rows": []}
    matrix_names = _roster_names(rows)
    member_names = _roster_names(members["rows"])
    matrix_has_agent = any("agent" in row for row in rows)
    comparable = matrix_state is None and matrix_has_agent and members["state"] is None
    reason = None
    if not matrix_has_agent:
        reason = "正文矩阵无 agent 列，两侧名册不可比对"
    elif members["state"] is not None:
        reason = "frontmatter 名册%s，两侧名册不可比对" % members["state"]
    return {
        "matrix_rows": rows,
        "matrix_state": matrix_state,
        "members": members,
        "seats": _declared_block_map(front.get("seats")),
        "stage_seats": _declared_block_map(front.get("stage_seats")),
        "roster_delta": {
            "comparable": comparable,
            "reason": reason,
            "only_in_matrix": [n for n in matrix_names if n not in member_names] if comparable else [],
            "only_in_members": [n for n in member_names if n not in matrix_names] if comparable else [],
        },
        "type_source": "body-matrix",
    }


def build_dynamic(front) -> dict:
    config_raw = front.get("config")
    config_entries = []
    if isinstance(config_raw, dict):
        for key, value in config_raw.items():
            _flatten_config(key, value, config_entries)
    optional = []
    for key in OPTIONAL_SCHEMA_KEYS:
        declared = front.get(key) is not None
        optional.append({
            "key": key,
            "declared": declared,
            "value": _render_value(front.get(key)) if declared else None,
        })
    summary_declared = isinstance(config_raw, dict) and "summary" in config_raw
    optional.append({
        "key": "config.summary",
        "declared": summary_declared,
        "value": _render_value(config_raw.get("summary")) if summary_declared else None,
    })
    reason_declared = isinstance(config_raw, dict) and "reporting-reason" in config_raw
    optional.append({
        "key": "config.reporting-reason",
        "declared": reason_declared,
        "value": _render_value(config_raw.get("reporting-reason")) if reason_declared else None,
    })
    return {
        "pattern": _text(front.get("pattern")),
        "config_state": None if config_entries else STATE_UNDECLARED,
        "config_entries": [{"key": "config." + key, "value": value} for key, value in config_entries],
        "optional_keys": optional,
        "focus_target": _text(front.get("focus_target")),
    }


def build_persistence(team_dir: Path, front) -> dict:
    runs = team_dir / "runs"
    reports = {
        "state": STATE_MISSING,
        "path": str(runs),
        "total": 0,
        "shown": [],
        "omitted": 0,
        "unrecognized": [],
        "latest_path": None,
    }
    if runs.is_dir():
        try:
            entries = sorted(path for path in runs.iterdir() if path.is_file())
        except OSError:
            entries = None
        if entries is None:
            reports["state"] = STATE_UNREADABLE
        else:
            recognized = []
            unrecognized = []
            for path in entries:
                match = REPORT_NAME_RE.match(path.name)
                if match:
                    recognized.append((match.group(1), path.name, path))
                else:
                    unrecognized.append(path.name)
            recognized.sort(key=lambda item: item[1])
            recognized.sort(key=lambda item: item[0], reverse=True)
            reports["total"] = len(recognized)
            reports["omitted"] = max(0, len(recognized) - REPORT_SHOWN_CAP)
            reports["shown"] = [item[1] for item in recognized[:REPORT_SHOWN_CAP]]
            reports["unrecognized"] = sorted(unrecognized)
            reports["state"] = STATE_LISTED if recognized else STATE_EMPTY
            if recognized:
                reports["latest_path"] = str(recognized[0][2])

    items_path = team_dir / "items.jsonl"
    ledger = {"state": STATE_MISSING, "path": str(items_path)}
    if items_path.is_file():
        try:
            text = items_path.read_text(encoding="utf-8", errors="replace")
        except OSError as exc:
            ledger = {"state": STATE_UNREADABLE, "path": str(items_path), "reason": str(exc)}
        else:
            lines = [line for line in text.splitlines() if line.strip()]
            if not lines:
                ledger = {
                    "state": STATE_EMPTY,
                    "path": str(items_path),
                    "total_lines": 0,
                    "bad_lines": 0,
                    "by_state": {},
                    "non_terminal": [],
                }
            else:
                ledger = aggregate_ledger(lines)
                ledger["state"] = STATE_FOLDED
                ledger["path"] = str(items_path)

    spine = []
    for name in SPINE_FILES:
        path = team_dir / name
        spine.append({
            "name": name,
            "path": str(path),
            "present": path.is_file(),
            "empty": path.is_file() and path.stat().st_size == 0,
        })

    config_raw = front.get("config")
    delivery = None
    if isinstance(config_raw, dict):
        summary = config_raw.get("summary")
        if isinstance(summary, dict):
            delivery = _text(summary.get("delivery_dir"))
    return {
        "team_dir": str(team_dir),
        "reports": reports,
        "ledger": ledger,
        "spine": spine,
        "summary_delivery": delivery,
    }


def build_latest(persistence: dict) -> dict:
    latest_path = persistence["reports"].get("latest_path")
    if not latest_path:
        return {
            "report": None,
            "outcome": None,
            "target_assignment": None,
            "result_summary": None,
            "verification": None,
            "nested_runs": STATE_UNRECORDED,
            "readable": True,
        }
    try:
        text = Path(latest_path).read_text(encoding="utf-8", errors="replace")
    except OSError:
        return {
            "report": Path(latest_path).name,
            "outcome": None,
            "target_assignment": None,
            "result_summary": None,
            "verification": None,
            "nested_runs": STATE_UNRECORDED,
            "readable": False,
        }
    parsed = parse_report(text)
    return {
        "report": Path(latest_path).name,
        "outcome": parsed["outcome"],
        "target_assignment": parsed["target_assignment"],
        "result_summary": parsed["result_summary"],
        "verification": parsed["verification"],
        "nested_runs": summarize_nested(parsed["nested_runs"]),
        "readable": True,
    }


def assemble_single(repo_root: Path, slug: str) -> dict:
    """One extraction shared by the default rendering and the ``--json`` envelope."""
    team_dir = repo_root / ".specify" / "teams" / slug
    if not team_dir.is_dir():
        return {"state": "not-found", "slug": slug}
    definition_path = team_dir / "team.md"
    try:
        text = definition_path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        return {"state": "corrupt", "slug": slug, "path": str(definition_path), "reason": str(exc)}
    front, problems = parse_frontmatter(text)
    if is_definition_corrupt(problems):
        return {
            "state": "corrupt",
            "slug": slug,
            "path": str(definition_path),
            "reason": problems.get("frontmatter") or problems.get("slug"),
        }

    binding, binding_error = read_binding(repo_root, slug)
    definition = build_definition(front, problems, slug)
    definition["binding"] = binding
    definition["binding_error"] = binding_error

    static = build_static(front, definition_body(text))
    dynamic = build_dynamic(front)
    persistence = build_persistence(team_dir, front)
    latest = build_latest(persistence)

    anchor_identity = definition["anchor_identity"]
    archive = {
        "handoff_ref": definition["handoff_ref"],
        "anchor": read_anchor(repo_root, anchor_identity["value"]),
        "anchor_pointer": "/speckit.anchor view",
    }

    degraded = binding_error is not None or archive["anchor"]["state"] == STATE_UNREADABLE
    errors = []
    if binding_error is not None:
        errors.append({
            "code": "engine-degraded",
            "message": "binding 读取失败: %s" % binding_error,
            "path": str(team_dir),
        })
    if archive["anchor"]["state"] == STATE_UNREADABLE:
        errors.append({
            "code": "engine-degraded",
            "message": "anchor 读取失败: %s" % archive["anchor"].get("reason", ""),
            "path": str(team_dir),
        })

    consumed = [definition_path]
    ledger_path = persistence["ledger"].get("path")
    if persistence["ledger"]["state"] in (STATE_EMPTY, STATE_FOLDED):
        consumed.append(Path(ledger_path))
    for entry in persistence["spine"]:
        if entry["present"]:
            consumed.append(Path(entry["path"]))
    if persistence["reports"].get("latest_path"):
        consumed.append(Path(persistence["reports"]["latest_path"]))

    return {
        "state": "ok",
        "mode": "single",
        "slug": slug,
        "definition": definition,
        "static": static,
        "dynamic": dynamic,
        "persistence": persistence,
        "latest": latest,
        "archive": archive,
        "degraded": degraded,
        "errors": errors,
        "as_of": _max_mtime_iso(consumed),
        "latest_report_timestamp": (
            REPORT_NAME_RE.match(persistence["reports"]["shown"][0]).group(1)
            if persistence["reports"]["shown"] else None
        ),
    }


# --------------------------------------------------------------------------- #
# Overview (E8): one linear pass over .specify/teams/*/, no engine call (R-04)
# --------------------------------------------------------------------------- #
OVERVIEW_HEADERS = (
    "slug",
    "name",
    "pattern",
    "lifecycle",
    "绑定锚点（anchor）",
    "updated",
    "最近运行（latest run）",
)


def _latest_report_token(team_dir: Path):
    runs = team_dir / "runs"
    if not runs.is_dir():
        return None
    try:
        names = [path.name for path in runs.iterdir() if path.is_file()]
    except OSError:
        return None
    tokens = [match.group(1) for match in map(REPORT_NAME_RE.match, names) if match]
    return max(tokens) if tokens else None


def build_overview_row(repo_root: Path, slug: str) -> dict:
    team_dir = repo_root / ".specify" / "teams" / slug
    definition_path = team_dir / "team.md"
    row = {
        "slug": slug,
        "name": None,
        "pattern": None,
        "lifecycle": {"value": "active", "declared": False},
        "anchor_identity": {"kind": "inferred", "value": slug},
        "updated": None,
        "latest_run": None,
        "state": STATE_CORRUPT,
        "path": str(definition_path),
    }
    try:
        text = definition_path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return row
    front, problems = parse_frontmatter(text)
    if is_definition_corrupt(problems):
        return row
    row["state"] = "ok"
    row["name"] = _text(front.get("name"))
    row["pattern"] = _text(front.get("pattern"))
    row["lifecycle"] = lifecycle_of(front)
    row["anchor_identity"] = anchor_identity_of(front, slug)
    row["updated"] = _text(front.get("updated"))
    row["latest_run"] = _latest_report_token(team_dir)
    return row


def available_slugs(repo_root: Path) -> list:
    """Sorted directory names under the team archive; the not-found navigation source."""
    teams_root = repo_root / ".specify" / "teams"
    try:
        return sorted(
            path.name for path in teams_root.iterdir()
            if path.is_dir() and not path.name.startswith(".")
        )
    except OSError:
        return []


def render_not_found(repo_root: Path, slug: str) -> str:
    """Not-found navigation: shared string, bounded list, create suggestion (C-31, FR-006)."""
    names = available_slugs(repo_root)
    lines = ["team not found: %s" % slug]
    if not names:
        lines.append("No teams found")
    else:
        shown = names[:SLUG_LIST_CAP]
        omitted = len(names) - len(shown)
        header = "可用 slug（available slugs；共 %d，显示 %d" % (len(names), len(shown))
        if omitted:
            header += "，省略 %d" % omitted
        lines.append(header + "）:")
        for name in shown:
            lines.append("  - %s" % name)
    lines.append("建议（next step）: /speckit.team create %s" % slug)
    return "\n".join(lines)


def assemble_overview(repo_root: Path) -> dict:
    """Scan the archive layer; a corrupt directory is counted, never silently dropped."""
    teams_root = repo_root / ".specify" / "teams"
    try:
        directories = sorted(
            path for path in teams_root.iterdir()
            if path.is_dir() and not path.name.startswith(".")
        )
    except OSError:
        directories = []
    rows = []
    corrupt_rows = []
    consumed = []
    for team_dir in directories:
        row = build_overview_row(repo_root, team_dir.name)
        if row["state"] == "ok":
            rows.append(row)
            consumed.append(team_dir / "team.md")
        else:
            corrupt_rows.append(row)
    return {
        "mode": "overview",
        "rows": rows,
        "total": len(rows),
        "corrupt_total": len(corrupt_rows),
        "corrupt_rows": corrupt_rows,
        "empty": not directories,
        "as_of": _max_mtime_iso(consumed),
        "latest_report_timestamp": None,
        "degraded": False,
        "errors": [],
    }


def render_overview(view: dict) -> str:
    if view["empty"]:
        return "No teams found"
    header = "Team Overview: %d teams" % (view["total"] + view["corrupt_total"])
    if view["corrupt_total"]:
        header += "（其中 %d %s）" % (view["corrupt_total"], STATE_CORRUPT)
    lines = [
        header + " · as-of: %s（文件时间；非实时探测）" % view["as_of"],
        "",
        "| " + " | ".join(OVERVIEW_HEADERS) + " |",
        "|" + "|".join("---" for _ in OVERVIEW_HEADERS) + "|",
    ]
    for row in sorted(view["rows"] + view["corrupt_rows"], key=lambda item: item["slug"]):
        if row["state"] == STATE_CORRUPT:
            cells = (
                row["slug"],
                "%s（%s）" % (STATE_CORRUPT, row["path"]),
                STATE_UNRECORDED,
                STATE_UNRECORDED,
                STATE_UNRECORDED,
                STATE_UNRECORDED,
                STATE_UNRECORDED,
            )
        else:
            lifecycle = row["lifecycle"]
            lifecycle_text = lifecycle["value"] if lifecycle["declared"] else (
                lifecycle["value"] + "（" + STATE_UNDECLARED + "）")
            anchor = row["anchor_identity"]
            cells = (
                row["slug"],
                row["name"] or STATE_UNRECORDED,
                row["pattern"] or STATE_UNRECORDED,
                lifecycle_text,
                "%s — %s" % (anchor["kind"], anchor["value"]),
                row["updated"] or STATE_UNRECORDED,
                row["latest_run"] or STATE_UNRECORDED,
            )
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog=PROGRAM_NAME,
        description=(
            "Read-only team view: six information groups for one team, or an overview "
            "of every team in the archive."
        ),
    )
    configure_parser(
        parser,
        effects="none; reads the team archive and prints; a flag-only invocation writes nothing",
        codes=(
            "0 rendering produced; 2 input error; 3 team not found; "
            "4 definition corrupt; 5 rendered with a degraded engine read"
        ),
    )
    parser.add_argument(
        "team_slug",
        nargs="?",
        default=None,
        metavar="<team-slug>",
        help="exact slug under .specify/teams/; omitted = overview of every team",
    )
    parser.add_argument(
        "--repo-root",
        default=None,
        help="repository root (default: derived from this file's own resolved path)",
    )
    parser.add_argument(
        "--scope",
        default=None,
        choices=SCOPE_VALUES,
        help="archive layer selector; teams is the serviced layer, auto only for one slug",
    )
    parser.add_argument(
        "--spec-dir",
        default=None,
        help="forwarded to engine reads that accept it; never decides a landing point",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="emit the internal test envelope instead of the human-facing rendering",
    )
    VersionAction.attach(parser)
    return parser


# --------------------------------------------------------------------------- #
# Default rendering (C-29 / C-30 / C-32 / C-33 / C-34)
# --------------------------------------------------------------------------- #
GROUP_HEADINGS = (
    "## 1. 身份与绑定（Identity & Binding）",
    "## 2. 静态结构（Static Structure）",
    "## 3. 动态结构（Dynamic Structure）",
    "## 4. 持久化清单（Persistence Inventory）",
    "## 5. 最近运行状态（Recent Run State）",
    "## 6. 其他归档层引用（Archive References）",
)
STATE_DECLARED = "已声明"


def _fact(value, key=None, problems=None):
    if problems and key in problems:
        return problems[key]
    return value if value is not None else STATE_UNRECORDED


def _block_map_text(view: dict) -> str:
    if view["state"] == STATE_UNDECLARED:
        return STATE_UNDECLARED + DEFAULT_POINTER
    if view["state"]:
        return view["state"]
    entries = view["entries"]
    if not entries:
        return STATE_EMPTY
    parts = []
    for key, value in entries.items():
        if isinstance(value, dict):
            inner = ", ".join("%s=%s" % (k, _render_value(v)) for k, v in value.items())
            parts.append("%s: %s" % (key, inner))
        else:
            parts.append("%s: %s" % (key, _render_value(value)))
    return STATE_DECLARED + "（" + "；".join(parts) + "）"


def _excerpt_text(value) -> str:
    excerpt = bounded_excerpt(value)
    if excerpt is None or excerpt == "":
        return STATE_UNRECORDED
    return excerpt.replace("\n", "\n  ")


def _nested_text(value) -> str:
    if isinstance(value, list):
        return "; ".join(str(item) for item in value) if value else STATE_UNRECORDED
    return value if value else STATE_UNRECORDED


def _render_identity(view: dict, lines: list) -> None:
    definition = view["definition"]
    problems = definition["problems"]
    lines.append(GROUP_HEADINGS[0])
    lines.append("- slug: %s" % _fact(definition["slug"], "slug", problems))
    lines.append("- name: %s" % _fact(definition["name"], "name", problems))
    lines.append("- description: %s" % _fact(definition["description"], "description", problems))
    lifecycle = definition["lifecycle"]
    if lifecycle["declared"]:
        lifecycle_text = _fact(lifecycle["value"], "lifecycle_state", problems)
    else:
        lifecycle_text = STATE_UNDECLARED + " → active"
    lines.append("- lifecycle: %s" % lifecycle_text)
    if definition["binding_error"]:
        lines.append("- 绑定（binding）: %s（%s）" % (STATE_UNREADABLE, definition["binding_error"]))
    else:
        binding = definition["binding"] or {}
        lines.append("- 绑定（binding）: owner=%s · owner_id=%s · origin=%s" % (
            _fact(binding.get("owner")),
            _fact(binding.get("owner_id")),
            _fact(binding.get("origin")),
        ))
    identity = definition["anchor_identity"]
    lines.append("- 锚点身份（anchor_identity）: %s — %s" % (identity["kind"], identity["value"]))
    lines.append("- handoff_ref: %s" % _fact(definition["handoff_ref"], "handoff_ref", problems))
    if definition["other_keys"]:
        rendered = []
        for item in definition["other_keys"]:
            if item["problem"]:
                rendered.append("%s（%s）" % (item["key"], item["problem"]))
            else:
                rendered.append(item["key"])
        lines.append("- 其它声明键: %s" % ", ".join(rendered))
    else:
        lines.append("- 其它声明键: 无")


def _render_static(view: dict, lines: list) -> None:
    static = view["static"]
    lines.append(GROUP_HEADINGS[1])
    lines.append("- type 来源（type_source）: 正文矩阵（body-matrix）")
    rows = static["matrix_rows"]
    if static["matrix_state"]:
        lines.append("- 正文矩阵: %s" % static["matrix_state"])
    else:
        lines.append("- 正文矩阵: %d 行" % len(rows))
        columns = matrix_columns(rows)
        lines.append("  | " + " | ".join(columns) + " |")
        lines.append("  |" + "|".join("---" for _ in columns) + "|")
        for row in rows:
            lines.append("  | " + " | ".join(row.get(column, "") for column in columns) + " |")
    members = static["members"]
    if members["state"]:
        lines.append("- 成员（frontmatter）: %s" % members["state"])
    else:
        lines.append("- 成员（frontmatter）: %d 名" % len(members["rows"]))
        for item in members["rows"]:
            parts = ["%s=%s" % (key, _render_value(value)) for key, value in item.items()]
            lines.append("  - " + " · ".join(parts))
    lines.append("- seats: %s" % _block_map_text(static["seats"]))
    lines.append("- stage_seats: %s" % _block_map_text(static["stage_seats"]))
    delta = static["roster_delta"]
    if delta["comparable"]:
        lines.append("- 仅正文矩阵: %s" % (", ".join(delta["only_in_matrix"]) or "无"))
        lines.append("- 仅 frontmatter: %s" % (", ".join(delta["only_in_members"]) or "无"))
    else:
        lines.append("- 名册差异（roster_delta）: 未记录（%s）" % delta["reason"])


def _render_dynamic(view: dict, lines: list) -> None:
    dynamic = view["dynamic"]
    lines.append(GROUP_HEADINGS[2])
    lines.append("- pattern: %s" % (dynamic["pattern"] or STATE_UNRECORDED))
    if dynamic["config_state"]:
        lines.append("- config: %s%s" % (STATE_UNDECLARED, DEFAULT_POINTER))
    else:
        lines.append("- config:")
        for entry in dynamic["config_entries"]:
            lines.append("  - %s: %s" % (entry["key"], entry["value"]))
    lines.append("- 可选键声明（optional keys）:")
    for item in dynamic["optional_keys"]:
        if item["declared"]:
            lines.append("  - %s: 已声明 (%s)" % (item["key"], item["value"]))
        else:
            lines.append("  - %s: 未声明%s" % (item["key"], DEFAULT_POINTER))
    lines.append("- focus_target: %s" % (dynamic["focus_target"] or STATE_UNDECLARED))


def _render_persistence(view: dict, lines: list) -> None:
    persistence = view["persistence"]
    reports = persistence["reports"]
    ledger = persistence["ledger"]
    lines.append(GROUP_HEADINGS[3])
    lines.append("- 团队目录（team_dir）: %s" % persistence["team_dir"])
    if reports["state"] == STATE_LISTED:
        lines.append("- 运行报告: 已列出（共 %d 份，显示最新 %d 份，省略 %d）" % (
            reports["total"], min(reports["total"], REPORT_SHOWN_CAP), reports["omitted"]))
        for name in reports["shown"]:
            lines.append("  - %s" % name)
    else:
        lines.append("- 运行报告: %s（%s）" % (reports["state"], reports["path"]))
    if reports["unrecognized"]:
        lines.append("- 未识别（unrecognized）: %s" % ", ".join(reports["unrecognized"]))
    if ledger["state"] == STATE_FOLDED:
        counts = " · ".join(
            "%s %d" % (state, count) for state, count in sorted(ledger["by_state"].items())
        )
        lines.append("- 台账: 已聚合（共 %d 行，坏行 %d；状态计数: %s）" % (
            ledger["total_lines"], ledger["bad_lines"], counts or STATE_EMPTY))
        for item in ledger["non_terminal"]:
            lines.append("  - 非终态: %s (%s)" % (item["item_id"], item["state"]))
    elif ledger["state"] == STATE_UNREADABLE:
        lines.append("- 台账: 不可读（%s；%s）" % (ledger["path"], ledger.get("reason", "")))
    else:
        lines.append("- 台账: %s（%s）" % (ledger["state"], ledger["path"]))
    present = [entry["name"] for entry in persistence["spine"] if entry["present"]]
    if present:
        lines.append("- 脊柱文件（存在）: %s" % ", ".join(present))
    for entry in persistence["spine"]:
        if not entry["present"]:
            lines.append("- %s %s（%s）" % (entry["name"], STATE_MISSING, entry["path"]))
    delivery = persistence["summary_delivery"]
    lines.append("- summary 送达目录: %s" % (
        delivery if delivery else STATE_UNDECLARED + DEFAULT_POINTER))


def _render_latest(view: dict, lines: list) -> None:
    latest = view["latest"]
    ledger = view["persistence"]["ledger"]
    lines.append(GROUP_HEADINGS[4])
    lines.append("- 最近报告（latest_report）: %s" % (latest["report"] or STATE_UNRECORDED))
    lines.append("- Outcome: %s" % (latest["outcome"] or STATE_UNRECORDED))
    lines.append("- Target 指派: %s" % (latest["target_assignment"] or STATE_UNRECORDED))
    lines.append("- Result Summary: %s" % _excerpt_text(latest["result_summary"]))
    lines.append("- Verification: %s" % _excerpt_text(latest["verification"]))
    lines.append("- Nested SDD Runs: %s" % _nested_text(latest["nested_runs"]))
    if ledger["state"] == STATE_FOLDED:
        lines.append("- 台账信号: 非终态 %d · 坏行 %d" % (
            len(ledger["non_terminal"]), ledger["bad_lines"]))
    else:
        lines.append("- 台账信号: %s" % ledger["state"])


def _render_archive(view: dict, lines: list) -> None:
    archive = view["archive"]
    identity = view["definition"]["anchor_identity"]
    anchor = archive["anchor"]
    lines.append(GROUP_HEADINGS[5])
    lines.append("- handoff_ref: %s" % (archive["handoff_ref"] or STATE_UNDECLARED))
    lines.append("- 锚点（anchor）: %s（%s）" % (identity["value"], identity["kind"]))
    if anchor["state"] == "ok":
        lines.append("  - 生命周期: %s" % (anchor["lifecycle"] or STATE_UNRECORDED))
        lines.append("  - 判据数: %s" % (
            anchor["criteria_count"] if anchor["criteria_count"] is not None else STATE_UNRECORDED))
        if anchor["targets"]:
            for target in anchor["targets"]:
                lines.append("  - Target: %s (%s) — %s" % (
                    target["id"], target["status"], target["statement"]))
        else:
            lines.append("  - Targets: 为空")
    elif anchor["state"] == STATE_DANGLING:
        lines.append("  - 生命周期: %s" % STATE_DANGLING)
        lines.append("  - 原因: %s" % anchor.get("reason", STATE_UNRECORDED))
        lines.append("  - Targets: 未记录")
    else:
        lines.append("  - 生命周期: %s（%s）" % (STATE_UNREADABLE, anchor.get("reason", "")))
        lines.append("  - Targets: %s" % STATE_UNREADABLE)
    lines.append("- 内容入口: %s" % archive["anchor_pointer"])


def render_single(view: dict) -> str:
    definition = view["definition"]
    title = definition["name"] if definition["name"] is not None else STATE_UNRECORDED
    lines = [
        "Team View: %s（%s）" % (title, view["slug"]),
        "mode: single · as-of: %s（文件时间；非实时探测）" % view["as_of"],
        "",
    ]
    _render_identity(view, lines)
    lines.append("")
    _render_static(view, lines)
    lines.append("")
    _render_dynamic(view, lines)
    lines.append("")
    _render_persistence(view, lines)
    lines.append("")
    _render_latest(view, lines)
    lines.append("")
    _render_archive(view, lines)
    return "\n".join(lines)


# --------------------------------------------------------------------------- #
# Internal test envelope (E9, A-5)
# --------------------------------------------------------------------------- #
def framework_version() -> str:
    parts = version_text(PROGRAM_NAME).split(" ", 1)
    return parts[1] if len(parts) > 1 else "unknown"


def build_envelope(view: dict, repo_root: Path, requested_scope: str) -> dict:
    team = None
    overview = {"rows": [], "total": 0, "corrupt_total": 0}
    if view.get("mode") == "single":
        team = {
            "definition": view["definition"],
            "static": view["static"],
            "dynamic": view["dynamic"],
            "persistence": view["persistence"],
            "latest": view["latest"],
            "archive": view["archive"],
        }
    else:
        overview = {
            "rows": view["rows"],
            "total": view["total"],
            "corrupt_total": view["corrupt_total"],
        }
    return {
        "tool": "team-view",
        "version": framework_version(),
        "mode": view.get("mode", "overview"),
        "repo_root": str(repo_root),
        "scope": {"requested": requested_scope, "effective": "teams", "note": None},
        "as_of": {
            "max_file_mtime_utc": view.get("as_of"),
            "latest_report_timestamp": view.get("latest_report_timestamp"),
        },
        "overview": overview,
        "team": team,
        "errors": view.get("errors", []),
        "degraded": bool(view.get("degraded")),
    }


def emit_view(args, mode: str, repo_root: Path, scope: str) -> int:
    """Render one view: the six-group reading for one team, or the sorted overview."""
    if mode == "single":
        view = assemble_single(repo_root, args.team_slug)
        if view["state"] == "not-found":
            print(render_not_found(repo_root, args.team_slug))
            return EXIT_NOT_FOUND
        if view["state"] == "corrupt":
            print("定义损坏: %s" % view["path"])
            return EXIT_CORRUPT
        if args.json:
            print(json.dumps(
                build_envelope(view, repo_root, scope),
                ensure_ascii=False,
                indent=2,
            ))
        else:
            print(render_single(view))
        return EXIT_DEGRADED if view["degraded"] else EXIT_OK
    view = assemble_overview(repo_root)
    if args.json:
        print(json.dumps(
            build_envelope(view, repo_root, scope),
            ensure_ascii=False,
            indent=2,
        ))
    else:
        print(render_overview(view))
    return EXIT_OK


def main(argv=None) -> int:
    line = list(sys.argv[1:] if argv is None else argv)
    preparse_version_guard(line, declared=DECLARED_OPTIONS)
    parser = build_parser()
    args = parser.parse_args(line)

    scope, error = resolve_scope(args.scope, args.team_slug)
    if error is not None:
        print("error: " + error, file=sys.stderr)
        return EXIT_INPUT

    repo_root = resolve_repo_root(args.repo_root)
    mode = "overview" if args.team_slug is None else "single"

    if scope == "auto" and not (repo_root / ".specify" / "teams" / args.team_slug).is_dir():
        print(
            "error: --scope auto 无法在团队档案中解析 slug %r；auto 只服务身份可解析的单团队"
            % args.team_slug,
            file=sys.stderr,
        )
        return EXIT_INPUT

    return emit_view(args, mode, repo_root, scope)


if __name__ == "__main__":
    sys.exit(main())
