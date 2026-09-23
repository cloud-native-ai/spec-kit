#!/usr/bin/env python3
"""Deterministic structural validator for a feature's tasks.md.

Program-First discipline (shared/guidelines/token-efficiency.md): the fixed
mechanical rules that /speckit.tasks must enforce are checked here, once,
instead of being re-improvised as ad-hoc greps on every run.

Checks performed:
  row-format      every task row matches `- [state] T<NNN>[letter] ...` on ONE
                  line; checkbox lines with a missing/placeholder/malformed ID
                  are errors; indented continuation lines directly after a task
                  row (a wrapped row) are errors
  id-unique       task IDs are unique across the file
  blockedBy       every [blockedBy: Txxx,Tyyy] reference resolves to an
                  existing task ID (dangling/self references are errors;
                  references to LATER tasks are warnings)
  parallel-safe   two [P] tasks in the same phase must not WRITE the same file
                  path (warning: path extraction from prose is heuristic, and a
                  row's paths are split into write targets and pointer targets —
                  a path governed by an explicit read-only marker (a cite
                  governor such as `per` / `see` / `against` / `owner` / `指向`,
                  `read-only`, or a `grep` / `diff -` probe in the preceding
                  window) is a pointer target, so two rows that merely cite the
                  same owner do not conflict. Confirm each reported overlap
                  against the rows' actual write targets, then drop [P] from one
                  row or re-target it — never silence a warning by deleting the
                  cited path from the row text)
  story-labels    inside a `## Phase ... User Story ...` phase every row
                  carries exactly one [US<n>] label; NON-story phases
                  (Setup / Foundational / Polish / anything else) carry zero
                  `[US` markers (placeholders like [US-none] are violations)
  dod-format      no checkbox-syntax line (`- [ ]` / `- [x]` ...) inside the
                  `## Definition of Done` section (reserved for task rows)

Usage:
  python3 scripts/python/validate-tasks.py <path/to/tasks.md> [--json]

Exit codes:
  0  no errors (warnings may still be reported)
  1  at least one error
  2  file missing / unreadable / no task rows found
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

TASK_ROW = re.compile(r"^- \[([ xX>~])\]\s+(\S+)(.*)$")
VALID_ID = re.compile(r"^T\d{3}[A-Za-z]?$")
BLOCKED_BY = re.compile(r"\[blockedBy:\s*([^\]]+)\]")
STORY_LABEL = re.compile(r"\[US(\d+)\]")
ANY_US_MARKER = re.compile(r"\[US[^\]]*\]")
PHASE_HEADING = re.compile(r"^##\s+Phase\b(.*)$", re.IGNORECASE)
USER_STORY_PHASE = re.compile(r"User Story", re.IGNORECASE)
DOD_HEADING = re.compile(r"^##\s+Definition of Done\b", re.IGNORECASE)
NEXT_H2 = re.compile(r"^##\s")
PARALLEL_MARKER = re.compile(r"(?<!\S)\[P\](?!\S)")
# path-like tokens: contains a slash, or a filename with a common extension
PATH_TOKEN = re.compile(
    r"(?:[\w.@+~-]+/)+[\w.@+~/-]+|[\w@+~-]+\.(?:py|sh|bash|md|ya?ml|json|toml|txt|js|mjs|ts|tsx|ini|cfg|tpl|sql|go|rs|java|c|h|cpp)\b"
)
# A path token governed by one of these is a POINTER target (read/cited), not a
# WRITE target. Deliberately a closed list of unambiguous read-only governors:
# ambiguous ones (`from`, `via`, `in`) also head write phrases, so a token they
# govern keeps the default classification and the overlap is still reported.
POINTER_GOVERNOR = re.compile(
    r"(?:\b(?:per|see|against|cite|cited|cites|owner|owned)\b|"
    r"read-only|readonly|只读|指向|参见|详见|MUST NOT edit|(?:do not|never) edit)"
    r"[\s`'\"(:,、。]*$",
    re.IGNORECASE,
)
# A read-only probe named in the window preceding the token also demotes it --
# covers `grep <pat> in <path>`, where the governor word (`in`) is ambiguous and
# so cannot be used on its own.
POINTER_CONTEXT = re.compile(
    r"\bgrep\b|\brg\b|\bdiff\s+-|\bgit diff\b|no matches",
    re.IGNORECASE,
)
# A write verb inside that same window cancels the demotion: `grep X in a.md then
# rewrite b.py` must keep b.py a write target, or the guard loses real conflicts.
WRITE_VERB = re.compile(
    r"\b(?:create|write|add|update|edit|rewrite|extend|insert|rename|remove|"
    r"delete|author|fill|implement|modify|append|replace|patch|port|copy|sync)\b|"
    r"新建|写入|新增|插入|扩写|改写|修改|重写|追加|替换|同步",
    re.IGNORECASE,
)
POINTER_WINDOW = 40


def _classify_paths(text: str):
    """Split a row's path tokens into (write targets, pointer targets).

    The default is WRITE: only an unambiguous read-only governor immediately
    before the token, or a read-only probe in the preceding window with no write
    verb in it, demotes a token. Two [P] rows that merely cite the same owner
    therefore stop being reported as a write conflict, while every overlap the
    guard reported before is still reported.
    """
    write, pointer = set(), set()
    for m in PATH_TOKEN.finditer(text):
        tok = m.group(0).strip(".,;:()")
        if "[" in tok or "]" in tok:  # template placeholder, not a real path
            continue
        before = text[max(0, m.start() - POINTER_WINDOW):m.start()]
        governed = bool(POINTER_GOVERNOR.search(before))
        probed = bool(POINTER_CONTEXT.search(before)) and not WRITE_VERB.search(before)
        (pointer if (governed or probed) else write).add(tok)
    return write, pointer


def validate(path: Path):
    errors, warnings = [], []
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError as exc:
        return [f"0: cannot read {path}: {exc}"], []

    tasks = {}          # id -> {line, phase, parallel, write_paths, pointer_paths, order}
    order = 0
    phase_name = None
    phase_is_story = False
    in_dod = False
    prev_was_task = False

    for lineno, line in enumerate(lines, start=1):
        # --- section tracking -------------------------------------------
        if DOD_HEADING.match(line):
            in_dod, phase_name = True, None
            prev_was_task = False
            continue
        if in_dod:
            if NEXT_H2.match(line):
                in_dod = False
            elif re.match(r"^\s*- \[[ xX~]\]", line):
                errors.append(
                    f"{lineno}: dod-format: checkbox syntax inside Definition of Done "
                    f"(use `- DoD-N:` prefix): {line.strip()[:80]}"
                )
        m_phase = PHASE_HEADING.match(line)
        if m_phase:
            phase_name = m_phase.group(0).strip()
            phase_is_story = bool(USER_STORY_PHASE.search(phase_name))
            prev_was_task = False
            continue
        if re.match(r"^##\s", line):  # any other H2 ends the current phase
            phase_name, phase_is_story = None, False

        # --- task rows ----------------------------------------------------
        m = TASK_ROW.match(line)
        if m:
            prev_was_task = True
            if in_dod:
                continue  # already reported by the dod-format check above
            state, tid, rest = m.group(1), m.group(2), m.group(3)
            if not VALID_ID.match(tid):
                errors.append(
                    f"{lineno}: row-format: checkbox row with missing/placeholder/malformed "
                    f"Task ID `{tid}` (expected T<NNN>): {line.strip()[:80]}"
                )
                continue
            if tid in tasks:
                errors.append(
                    f"{lineno}: id-unique: duplicate Task ID {tid} "
                    f"(first defined at line {tasks[tid]['line']})"
                )
                continue
            order += 1
            write_paths, pointer_paths = _classify_paths(rest)
            tasks[tid] = {
                "line": lineno,
                "state": state,
                "phase": phase_name,
                "phase_is_story": phase_is_story,
                "parallel": bool(PARALLEL_MARKER.search(rest)),
                "write_paths": write_paths,
                "pointer_paths": pointer_paths,
                "order": order,
                "blocked_by": [
                    t.strip() for t in re.split(r"[,\s]+", (BLOCKED_BY.search(rest).group(1) if BLOCKED_BY.search(rest) else "")) if t.strip()
                ],
            }
            # story-label placement
            labels = STORY_LABEL.findall(rest)
            any_us = ANY_US_MARKER.search(rest)
            if phase_is_story and len(labels) != 1:
                errors.append(
                    f"{lineno}: story-labels: {tid} in User Story phase "
                    f"`{phase_name[:60]}` must carry exactly one [US<n>] label "
                    f"(found {len(labels)})"
                )
            elif not phase_is_story and any_us:
                errors.append(
                    f"{lineno}: story-labels: {tid} in NON-story phase "
                    f"`{(phase_name or '<no phase>')[:60]}` must not carry any "
                    f"[US...] marker: {any_us.group(0)}"
                )
            continue

        # --- wrapped continuation line -------------------------------------
        if prev_was_task and line.strip() and re.match(r"^\s+\S", line) \
                and not re.match(r"^\s*(?:[-*#>|`]|\d+\.)", line):
            errors.append(
                f"{lineno}: row-format: wrapped task row — continuation text must be "
                f"folded into the single-line task row above: {line.strip()[:80]}"
            )
        if not line.strip():
            prev_was_task = False
        elif not line.startswith((" ", "\t")):
            prev_was_task = False

    if not tasks:
        errors.append(f"0: no task rows found in {path} (expected `- [ ] T<NNN> ...` lines)")
        return errors, warnings

    # --- blockedBy resolvability -----------------------------------------
    for tid, t in tasks.items():
        for ref in t["blocked_by"]:
            if ref == tid:
                errors.append(f"{t['line']}: blockedBy: {tid} references itself")
            elif ref not in tasks:
                errors.append(
                    f"{t['line']}: blockedBy: {tid} references {ref}, which does not exist "
                    f"(dangling reference)"
                )
            elif tasks[ref]["order"] > t["order"]:
                warnings.append(
                    f"{t['line']}: blockedBy: {tid} references later task {ref} "
                    f"(forward dependency — verify this is intentional)"
                )

    # --- [P] parallel safety (same phase, same file) -----------------------
    by_phase = {}
    for tid, t in tasks.items():
        if t["parallel"]:
            by_phase.setdefault(t["phase"], []).append((tid, t))
    for phase, rows in by_phase.items():
        for i in range(len(rows)):
            for j in range(i + 1, len(rows)):
                tid_a, a = rows[i]
                tid_b, b = rows[j]
                phase_label = (phase or "<no phase>")[:60]
                both_write = a["write_paths"] & b["write_paths"]
                if both_write:
                    warnings.append(
                        f"{a['line']}: parallel-safe: [P] tasks {tid_a} (line {a['line']}) and "
                        f"{tid_b} (line {b['line']}) both WRITE {sorted(both_write)} in phase "
                        f"`{phase_label}` — [P] requires different write targets; drop [P] from "
                        f"one row or re-target it, never by deleting the cited path"
                    )
                    continue
                # One row writes what the other only cites: a real ordering
                # hazard, but weaker than two writers, so it is labelled
                # distinctly and the two-writer remedy is not offered for it.
                # Reported per direction — both directions can hold at once.
                a_writes = a["write_paths"] & b["pointer_paths"]
                b_writes = b["write_paths"] & a["pointer_paths"]
                for writer, wline, reader, rline, paths in (
                    (tid_a, a["line"], tid_b, b["line"], a_writes),
                    (tid_b, b["line"], tid_a, a["line"], b_writes),
                ):
                    if not paths:
                        continue
                    warnings.append(
                        f"{wline}: parallel-safe: [P] task {writer} (line {wline}) WRITES "
                        f"{sorted(paths)} while {reader} (line {rline}) only references it as a "
                        f"read-only target in phase `{phase_label}` — the reader may observe a "
                        f"half-written file; sequence the pair with [blockedBy:] or drop [P]"
                    )

    # stable file order: each entry starts with "<lineno>: "
    errors.sort(key=lambda e: int(e.split(":", 1)[0]))
    warnings.sort(key=lambda w: int(w.split(":", 1)[0]))
    return errors, warnings


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        prog="validate-tasks.py",
        description="Deterministic structural validator for a feature's tasks.md "
                    "(row format, ID uniqueness, blockedBy resolvability, [P] "
                    "parallel safety, story-label placement, DoD format).",
        epilog="Exit codes: 0 = no errors (warnings possible), 1 = errors found, "
               "2 = file missing / no task rows.",
    )
    parser.add_argument("tasks_md", help="path to the tasks.md file to validate")
    parser.add_argument("--json", action="store_true",
                        help="emit a machine-readable JSON report instead of text")
    args = parser.parse_args(argv)

    path = Path(args.tasks_md)
    if not path.is_file():
        print(f"FAIL: {path} does not exist", file=sys.stderr)
        return 2

    errors, warnings = validate(path)
    unparseable = any(e.startswith("0:") for e in errors)

    if args.json:
        print(json.dumps({
            "file": str(path),
            "errors": errors,
            "warnings": warnings,
            "status": "FAIL" if (errors or unparseable) else "PASS",
        }, ensure_ascii=False, indent=2))
    else:
        for w in warnings:
            print(f"WARN  {w}")
        for e in errors:
            print(f"ERROR {e}")
        status = "FAIL" if errors else ("PASS (with warnings)" if warnings else "PASS")
        print(f"{status}: {path} — {len(errors)} error(s), {len(warnings)} warning(s)")

    return 2 if unparseable else (1 if errors else 0)


if __name__ == "__main__":
    sys.exit(main())
