#!/usr/bin/env python3
"""closure-acceptance-check.py — the one deterministic answer to
"may this feature be called `Implemented`?".

Program-First discipline (`shared/guidelines/token-efficiency.md`): the question has a fixed,
decidable answer, so a program produces it and prints a verdict. No caller may decide it another
way — not a model judgement, not a different script, not an ad-hoc grep (contract
`contracts/gate-wiring.contract.md` GW-04).

Schema owner: `shared/workflow/acceptance-hardening.md` — § Closure Verdict (this program's
verdict, closed reason set, exit codes and `final_path` counts), § Verification Vocabulary (the
status set, the five measurement-ladder fields, the smoke record), § Feature Status (the claimed
status). This script **implements** those schemas; it never redefines them.

Calling surface (contract `contracts/closure-acceptance-check.contract.md` C-01…C-06, C-10):

  --spec-dir <dir>          REQUIRED. Holds requirements.md, plan.md, tasks.md, verification.md.
  --repo <root>             Repository root for repo-relative path resolution (default: the
                            checkout this script lives in).
  --feature-detail <path>   The claimed feature status, read from a feature detail file.
  --feature-registry <path> The claimed feature status, read from a registry file. Either flag
                            may be given; when neither is, the status is resolved from the spec
                            directory's own claim carriers and then from the repository registry
                            by the spec directory's key (see `resolve_claimed_status`).
  --audit-existing          Read-only audit mode: report, write nothing, and let the exit code
                            reflect input validity only.
  --json                    Machine-readable payload on stdout.
  --json-out <path>         Write the identical payload to a file as well.
  --waive CODE:TARGET       Repeatable. Removes one reason from the blocking set while still
                            counting it as waived.

Exit codes (C-10): 0 = accept, 1 = block, 2 = an input is missing or unparsable. A missing input
is never reported as `block`, and in audit mode the exit code reflects input validity only.

IMPLEMENTATION STATE — read this before trusting an exit code
--------------------------------------------------------------
This is the verdict slice (task T015). Argument parsing, input resolution, the exit-2 contract and
the judgement are implemented. One deliberate absence, with a named owner, so it is never a
silent hole:

* `--audit-existing` is **not implemented in this slice** — `plan.md` § Slice Boundary defers
  FR-020 to 081d. Passing it exits `2` with an explicit message. That is deliberate: an
  unimplemented mode MUST NOT emit a per-feature verdict, because an audit run whose exit code
  came from one feature's verdict would report the opposite of what C-10 requires of the mode.

The external-source extraction landed in 081b (contract C-13 / C-17 / C-18): the runtime-row
class's three shapes, the prose-declaration rule, the `signed-contract` `Contract` cell, the
dependency-feature extraction over the closed three-source set, the `Source row` join key and the
`inherited` carrier's three limbs. Its sibling is
`skills/external/sdd-loop-driver/scripts/pre-analyze-check.py`, which judges the same closed set at
the stage gates; `tests/contract/test_acceptance_premises.py` asserts the two name the same reason
instance, so the pair cannot drift into two spellings.

Read-only and stdlib-only (C-01, V-14): no network, no model, no write — `--json-out` is the one
declared output file, and it is written only when a payload exists.

Usage:
  python3 scripts/python/closure-acceptance-check.py --spec-dir .specify/specs/<key>
  python3 scripts/python/closure-acceptance-check.py --spec-dir <dir> --feature-registry <path> --json
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

EXIT_ACCEPT = 0
EXIT_BLOCK = 1
EXIT_INPUT = 2

#: Inputs the check cannot run without (C-02). Missing any of them is an input error, never a
#: `block`: the artifact is incomplete, which is a different fact from the feature failing.
REQUIRED_INPUTS = ("requirements.md", "plan.md", "tasks.md", "verification.md")

# --- the closed reason set -------------------------------------------------------------------
# The seven templates are owned by `requirements.md` § Shared Strings (STR-008…STR-014) and by the
# owner doc § Closure Verdict. An emitted reason is a code plus its argument; the instance form
# `code + ": " + target` is produced by `instance()` for display and by the callers' two-part
# membership test, never by a third spelling here.
R_ZERO_FINAL_PASS = "zero-final-path-pass"
R_FINAL_PATH_NOT_PASS = "final-path-not-pass"
R_LADDER = "blocked-without-measurement-ladder"
R_RUNTIME = "runtime-dependency-not-owned"
R_PREMISE = "falsified-premise-undecided"
R_INHERITED = "inherited-blocker-undisposed"
R_CLAIMED = "status-claims-implemented-but-blocked"

#: The seven-member closed set (C-09). Closed: an eighth reason requires revising the owner doc,
#: never a local addition. `--waive` codes are validated against this set, so a typo cannot
#: silently waive nothing.
REASON_CODES = (
    R_ZERO_FINAL_PASS,
    R_FINAL_PATH_NOT_PASS,
    R_LADDER,
    R_RUNTIME,
    R_PREMISE,
    R_INHERITED,
    R_CLAIMED,
)

#: The two templates that take no argument. Their instance carries no target, so a `--waive` entry
#: for them names the feature (or `*`) instead of a reason argument.
ARGUMENTLESS_REASONS = (R_ZERO_FINAL_PASS, R_CLAIMED)

# --- vocabularies (owner: acceptance-hardening.md § Verification Vocabulary) ------------------
STATUS_VALUES = ("pass", "fail", "partial", "blocked", "deferred", "unknown")
#: Statuses that oblige the five-field measurement ladder.
LADDER_STATUSES = ("blocked", "deferred", "partial")
LADDER_FIELDS = (
    "blocked_at",
    "reduced_measurement",
    "reduced_measurement_run",
    "why_reduced_insufficient",
    "unblock",
)
SMOKE_FIELDS = ("smoke_command", "smoke_exit_code", "smoke_evidence_path")
#: `final_path` is a closed count record (C-08): six status buckets plus the total. The set is the
#: owner doc's (`§ Closure Verdict`), not this file's: `unknown` means *no status row exists*,
#: while `partial` is a measured status and is therefore counted as itself.
FINAL_PATH_BUCKETS = ("pass", "blocked", "deferred", "partial", "fail", "unknown")

FLOW_CLASSES = ("execution", "expression")
#: An undeclared class degrades to `execution` — the strict side. 077 FR-004 owns the default, and
#: the `expression` exemption is mechanical: it is read from the declaration, never inferred.
DEFAULT_FLOW_CLASS = "execution"

#: Claimed statuses that assert the feature is already implemented. V-12: the claimed-but-blocked
#: reason can only fire for one of these, so a `Planned → Implemented` run never emits it.
CLAIMED_IMPLEMENTED = ("Implemented", "Ready for Review")

#: Cells that carry no content. A dash is how these tables spell "nothing here", so it must read as
#: empty rather than as a value (the fixtures use the em dash for a verified premise's absent
#: decision).
EMPTY_CELLS = ("", "-", "--", "—", "–")

#: `Form` domain (AS-06). `not-required` is admissible only for an `expression`-class feature,
#: which is why the allowed set is computed per run instead of frozen.
FORM_IN_SCOPE = "in-scope"
FORM_SIGNED = "signed-contract"
FORM_WAIVED = "user-waived"
FORM_NOT_REQUIRED = "not-required"

#: The three dispositions of `§ Inherited Blockers` (AS-10).
DISPOSITIONS = ("resolved", "inherited", "not-applicable")

#: Resolved once so a `--json-out` relative path and an evidence path are read the same way.
_REPO_ROOT = Path(__file__).resolve().parents[2]
# Guard: invoked through the `.specify/scripts/python/` mirror, `parents[2]` is `.specify` and
# every repo-relative resolution would land inside `.specify/` instead of the checkout. A directory
# named `.specify` is never a repository root.
if _REPO_ROOT.name == ".specify":
    _REPO_ROOT = _REPO_ROOT.parent


class InputError(Exception):
    """An input is missing or unparsable — exit 2, never a verdict about the feature."""


class ModeNotImplemented(InputError):
    """A documented mode whose behaviour belongs to a later slice: exit 2, never a verdict."""


# --------------------------------------------------------------------------- #
# Small parsing helpers — line-anchored, so a prose mention never becomes a row
# --------------------------------------------------------------------------- #

SC_DEFINITION_RE = re.compile(r"^- \*\*SC-(\d{3})\*\*:")
FR_DEFINITION_RE = re.compile(r"(?m)^- \*\*(FR-\d{3})\*\*:")
PATH_MARKER_ANY_RE = re.compile(r"\*\*Path\*\*")
PATH_MARKER_LAST_RE = re.compile(r"\*\*Path\*\*:\s*(\S+)\s*$")
FLOW_CLASS_RE = re.compile(r"(?m)^\*\*Flow Class\*\*:\s*(\S+)\s*$")
DETAIL_STATUS_RE = re.compile(r"(?m)^\*\*Status\*\*:\s*(.+?)\s*$")
TASK_ROW_RE = re.compile(r"^\s*- \[(.)\]")
# `SC-NNN_...` / `RS-NNN_...` keys carry hyphens, so the key pattern admits them.
FIELD_RE = re.compile(r"^([A-Za-z][A-Za-z0-9_-]*)=(.*)$")
SC_STATUS_KEY_RE = re.compile(r"^(SC-\d{3})_status$")
SC_LADDER_KEY_RE = re.compile(r"^(SC-\d{3})_(%s)$" % "|".join(LADDER_FIELDS))
JOINT_ACCEPTANCE_KEY_RE = re.compile(r"^(RS-\d{3})_joint_acceptance$")
TABLE_SEPARATOR_RE = re.compile(r"^\|[\s:|-]+\|?\s*$")
RS_ID_RE = re.compile(r"^RS-\d{3}$")
EP_ID_RE = re.compile(r"^EP-\d{3}$")
FR_ID_RE = re.compile(r"FR-\d{3}")
SOURCE_LOCATOR_RE = re.compile(r"^\S+:\S+$")

RUNTIME_SECTION_RE = re.compile(r"(?m)^#{2,4}\s*Runtime Stack & Dependency Ownership")
PREMISES_SECTION_RE = re.compile(r"(?m)^#{2,4}\s*Execution Premises\s*$")
INHERITED_SECTION_RE = re.compile(r"(?m)^#{2,4}\s*Inherited Blockers\s*$")
DEFERRED_SECTION_RE = re.compile(r"(?m)^#{2,4}\s*Deferred\s*$")
D10_SECTION_RE = re.compile(r"(?m)^#{2,4}\s*D10\b")
HEADING_RE = re.compile(r"^#{1,6}\s")

#: The prose-declaration rule is mechanical, and this is the rule (C-18): a fenced code block or a
#: heading is removed first, then a line of this shape is a declaration. A narrative line without
#: the marker is not — otherwise "prose" would be a judgement.
FENCE_RE = re.compile(r"^\s*(```|~~~)")
PROSE_DECLARATION_RE = re.compile(r"^-\s*\*\*Runtime dependency\*\*:")
FEATURE_ID_RE = re.compile(r"(?m)^\*\*Feature ID\*\*:\s*(\d{3})\s*$")
VERIFICATION_FIELD_RE = re.compile(r"(?m)^(?:SC-\d{3}_status|deferred_tasks)=")
GATE_ROW_RE = re.compile(r"(?m)^\s*[-*]?\s*(GATE-\d+)\b")
TASK_ROW_ID_RE = re.compile(r"^- \[.\] (T\d{3})")

#: The `inherited` carrier's two forms (C-17), plus the `test:`-alone form that only an
#: `inherited-later` row may use — the task id of an unwritten `tasks.md` MUST NOT be fabricated.
CARRIER_TASK_RE = re.compile(r"^task:(T\d{3})\+test:(\S+)$")
CARRIER_GATE_RE = re.compile(r"^gate:(GATE-\d+)$")
CARRIER_TEST_ONLY_RE = re.compile(r"^test:(\S+)$")
#: A later `Carrier slice` (081c, 081d, …). `this-slice` is the other legal value.
LATER_SLICE_RE = re.compile(r"^\d{3}[a-z]?$")

#: The one reserved argument slot (C-09 / C-13): the zero-data-row shape has no `RS-NNN` to name,
#: and a fabricated id would point at a row nobody wrote.
RESERVED_RUNTIME_ARGUMENT = "runtime-stack"

#: The closed `Status` domain of `§ Execution Premises` (AS-09).
PREMISE_STATUSES = ("verified", "unverified", "falsified")

#: `Source row` values that mean "this row disposes nothing". `(none)` is the sentinel the 081a
#: fixtures write for a feature with no dependency set; it is not a malformed locator.
ABSENT_LOCATORS = ("(none)", "none", "n/a", "(no dependency)")

#: Statuses the dependency extraction selects on (C-17). `partial` is inside the set on purpose: a
#: dependency may carry `partial` rows and nothing else, and an extraction set that excluded it
#: would be disjoint from the disposition set, which makes the fourth finding unreachable.
EXTRACTED_STATUSES = ("blocked", "deferred", "partial")


def _blank(value):
    """`True` when a cell carries no content (see EMPTY_CELLS)."""
    return value is None or value.strip() in EMPTY_CELLS


def _clean(value):
    """A cell value without its Markdown emphasis/backtick decoration."""
    return (value or "").strip().strip("`").strip()


def _read(path):
    try:
        return Path(path).read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        raise InputError("input is not readable as UTF-8: %s (%s)" % (path, exc))


def _section_lines(text, pattern, name, path):
    """`[(line_no, line)]` for one `##`-level section body, or an InputError naming the file.

    The body stops at the next heading of any level, so a table inside the section never bleeds
    into the following prose. Line numbers are absolute and 1-based: a finding that points at the
    wrong line is a defect of the checker.
    """
    match = pattern.search(text)
    if not match:
        raise InputError("%s carries no § %s" % (path, name))
    heading_line = text[:match.start()].count("\n") + 1
    lines = text[match.end():].splitlines()
    if lines and lines[0].strip():
        # The carrier regex does not consume a heading's trailing tail (a parenthetical title),
        # so that fragment is still heading text, not body.
        lines = lines[1:]
    body = []
    for step, line in enumerate(lines):
        if HEADING_RE.match(line):
            break
        body.append((heading_line + 1 + step, line))
    return body


def _section(text, pattern, name, path):
    """The body of one `##`-level section, or an InputError naming the file."""
    return "\n".join(line for _, line in _section_lines(text, pattern, name, path))


def _table_rows(body_lines):
    """The rows of the first Markdown table in `body_lines`, as `[(line_no, {header: cell})]`.

    Returns a list of `{header: cell}` pairs. A section with no table yields an empty list: "the
    section exists and declares nothing" is a different fact from "the section is missing", and
    only the second is an input error (C-14) — while the runtime-row class judges the first as the
    reserved `runtime-stack` block (C-13).
    """
    header = None
    rows = []
    for number, line in body_lines:
        stripped = line.strip()
        if not stripped.startswith("|"):
            if header is not None and rows:
                break
            continue
        if header is None:
            header = [_clean(c).lower() for c in stripped.strip("|").split("|")]
            continue
        if TABLE_SEPARATOR_RE.match(stripped):
            continue
        cells = [c.strip() for c in stripped.strip("|").split("|")]
        if len(cells) < len(header):
            cells += [""] * (len(header) - len(cells))
        rows.append((number, dict(zip(header, cells))))
    return rows


def _column(row, *names):
    """The first present column among `names` (header wording varies across templates)."""
    for name in names:
        if name in row:
            return row[name]
    return ""


# --------------------------------------------------------------------------- #
# Waivers (C-06)
# --------------------------------------------------------------------------- #

def parse_waiver(raw):
    """`CODE:TARGET` → `(code, target)`, or an InputError.

    Shape only: the code is everything before the first colon and the target is everything after
    it (a target may legitimately contain colons of its own — a relative path plus a line number
    is the sibling script's waiver shape). Membership of the code in the closed reason set is
    checked once the set is in hand, together with the waiver's effect.
    """
    code, sep, target = raw.partition(":")
    code = code.strip()
    target = target.strip()
    if not sep or not code or not target:
        raise InputError(
            "--waive expects CODE:TARGET with both halves non-empty, got %r" % raw
        )
    return code, target


# --------------------------------------------------------------------------- #
# Input resolution (C-02, C-03)
# --------------------------------------------------------------------------- #

def resolve_inputs(args):
    """Resolve and validate every declared input. Returns a dict of absolute paths.

    Every failure names the path or the argument, so the caller never has to guess which input the
    exit code was about (C-02).
    """
    if not args.spec_dir:
        raise InputError(
            "--spec-dir <dir> is required (no spec directory given); "
            "it must contain %s" % ", ".join(REQUIRED_INPUTS)
        )

    spec_dir = Path(os.path.abspath(args.spec_dir))
    if not spec_dir.is_dir():
        raise InputError("spec dir not found: %s" % spec_dir)

    resolved = {"spec_dir": spec_dir}
    for name in REQUIRED_INPUTS:
        path = spec_dir / name
        if not path.is_file():
            raise InputError("required input not found: %s" % path)
        if not _read(path).strip():
            raise InputError("required input is empty: %s" % path)
        resolved[name] = path

    repo = Path(os.path.abspath(args.repo)) if args.repo else _REPO_ROOT
    if not repo.is_dir():
        raise InputError("repo root not found: %s" % repo)
    resolved["repo"] = repo

    for flag, value in (("--feature-detail", args.feature_detail),
                        ("--feature-registry", args.feature_registry)):
        if value is None:
            continue
        path = Path(os.path.abspath(value))
        if not path.is_file():
            raise InputError("%s names a file that does not exist: %s" % (flag, path))
        resolved[flag] = path

    resolved["waivers"] = [parse_waiver(raw) for raw in (args.waive or [])]
    return resolved


def feature_key(spec_dir):
    """The registry key a spec directory is filed under (`.specify/specs/<key>/`)."""
    return spec_dir.name


def _registry_status(path, key):
    """The `Status` cell of the registry row whose first column is `key` (or `key`'s digits)."""
    wanted = {key}
    digits = re.match(r"^(\d+)", key)
    if digits:
        wanted.add(digits.group(1))
    for line in _read(path).splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = [c.strip() for c in stripped.strip("|").split("|")]
        if not cells or cells[0] not in wanted:
            continue
        if len(cells) < 4:
            raise InputError("registry row for %s has no Status cell: %s" % (key, path))
        status = cells[3].strip()
        if not status:
            raise InputError("registry row for %s carries an empty Status: %s" % (key, path))
        return status
    return None


def _detail_status(path):
    """The `**Status**: <value>` line of a feature detail file."""
    match = DETAIL_STATUS_RE.search(_read(path))
    if not match:
        raise InputError("feature detail carries no `**Status**:` line: %s" % path)
    return match.group(1).strip()


def resolve_claimed_status(resolved):
    """`(status, source)` for the claimed feature status, or an InputError (C-03).

    Resolution order, stated once because two of these carriers are easy to confuse:

    1. `--feature-detail` — the most specific carrier a caller can name;
    2. `--feature-registry`;
    3. the spec directory's **own** claim carriers (`feature-detail.md`, then
       `feature-registry.md`). `data-model.md` § Fixture set declares the feature detail and the
       registry row to be part of each declarative fixture's file set, so a fixture directory
       carries its claim exactly the way a real spec directory carries its artifacts;
    4. the repository registry (`.specify/memory/features.md`) by the spec directory's key.

    A caller that names a carrier explicitly (1, 2) is never silently overruled; step 3 is what
    makes a fixture — whose key is not a registry row — still have a determinable claim.
    """
    spec_dir = resolved["spec_dir"]
    if "--feature-detail" in resolved:
        path = resolved["--feature-detail"]
        return _detail_status(path), str(path)
    if "--feature-registry" in resolved:
        path = resolved["--feature-registry"]
        status = _registry_status(path, feature_key(spec_dir))
        if status is None:
            raise InputError("no registry row for %s in %s" % (feature_key(spec_dir), path))
        return status, str(path)

    local_detail = spec_dir / "feature-detail.md"
    if local_detail.is_file():
        return _detail_status(local_detail), str(local_detail)
    local_registry = spec_dir / "feature-registry.md"
    if local_registry.is_file():
        status = _registry_status(local_registry, feature_key(spec_dir))
        if status is not None:
            return status, str(local_registry)

    repo_registry = Path(resolved["repo"]) / ".specify" / "memory" / "features.md"
    if repo_registry.is_file():
        status = _registry_status(repo_registry, feature_key(spec_dir))
        if status is not None:
            return status, str(repo_registry)

    raise InputError(
        "cannot determine the claimed feature status for %s: no --feature-detail / "
        "--feature-registry was given, the spec dir carries no feature-detail.md or "
        "feature-registry.md, and %s has no row for %r"
        % (spec_dir, repo_registry, feature_key(spec_dir))
    )


# --------------------------------------------------------------------------- #
# requirements.md — flow class, `Path` markers, runtime-stack rows (C-13)
# --------------------------------------------------------------------------- #

def parse_requirements(path):
    """`{path, flow_class, criteria, runtime_rows, runtime_row_count, prose}`.

    `criteria` is `{SC-NNN: "final"|"supporting"}`. A marker that cannot be parsed is an input
    error (V-3 / AS-04), never a `block`: a defect of the artifact is not a finding about the
    feature. `runtime_row_count` is carried separately from `runtime_rows` because **zero data
    rows** is a verdict of its own (C-13), not the same thing as "no runtime-stack section".
    """
    text = _read(path)
    match = FLOW_CLASS_RE.search(text)
    flow_class = DEFAULT_FLOW_CLASS
    if match:
        flow_class = match.group(1).strip()
        if flow_class not in FLOW_CLASSES:
            raise InputError(
                "%s declares `**Flow Class**: %s`, outside the closed set %s"
                % (path, flow_class, " / ".join(FLOW_CLASSES))
            )

    criteria = {}
    for number, line in enumerate(text.splitlines(), start=1):
        sc_match = SC_DEFINITION_RE.match(line)
        if not sc_match:
            continue
        sc_id = "SC-%s" % sc_match.group(1)
        markers = PATH_MARKER_ANY_RE.findall(line)
        if len(markers) != 1:
            raise InputError(
                "%s:%d %s carries %d `**Path**` markers; exactly one is required (AS-01)"
                % (path, number, sc_id, len(markers))
            )
        last = PATH_MARKER_LAST_RE.search(line.rstrip())
        if not last:
            raise InputError(
                "%s:%d %s does not end with its `**Path**: <value>` marker (AS-01)"
                % (path, number, sc_id)
            )
        value = last.group(1).strip()
        if value not in ("final", "supporting"):
            raise InputError(
                "%s:%d %s declares `**Path**: %s`, outside the closed set final / supporting"
                % (path, number, sc_id, value)
            )
        if sc_id in criteria:
            raise InputError("%s:%d %s is defined twice" % (path, number, sc_id))
        criteria[sc_id] = value

    allowed_forms = (FORM_IN_SCOPE, FORM_SIGNED, FORM_WAIVED)
    if flow_class == "expression":
        allowed_forms = allowed_forms + (FORM_NOT_REQUIRED,)
    try:
        body = _section_lines(text, RUNTIME_SECTION_RE,
                             "Runtime Stack & Dependency Ownership", path)
        present = True
    except InputError:
        # Mandatory in `requirements.md` of an `execution`-class feature, exempt for an
        # `expression`-class one: the exemption is mechanical because the class is declared.
        if flow_class == "execution":
            raise
        body, present = [], False
    runtime_rows = []
    for index, (number, row) in enumerate(_table_rows(body), start=1):
        rs_id = _clean(_column(row, "id"))
        if not RS_ID_RE.match(rs_id):
            raise InputError(
                "%s § Runtime Stack row %d carries no `RS-NNN` id (AS-05)" % (path, index)
            )
        form = _clean(_column(row, "form"))
        if form not in allowed_forms:
            raise InputError(
                "%s § Runtime Stack row %s declares `Form: %s`; the closed set for a %s-class "
                "feature is %s (AS-06)"
                % (path, rs_id, form or "<empty>", flow_class, " / ".join(allowed_forms))
            )
        runtime_rows.append({
            "id": rs_id,
            "form": form,
            "capability": _column(row, "capability"),
            "owner": _column(row, "owner"),
            "pin": _column(row, "pin"),
            "contract": _column(row, "contract"),
            "joint_acceptance": _column(row, "joint acceptance", "joint_acceptance"),
            "fr": _column(row, "fr"),
            "premises": _column(row, "premises"),
        })

    return {
        "path": str(path),
        "flow_class": flow_class,
        "criteria": criteria,
        "runtime_rows": runtime_rows,
        "runtime_row_count": len(runtime_rows),
        "runtime_section_present": present,
        "prose": _prose_declarations(body, path),
    }


def _prose_declarations(body_lines, path):
    """`[(line_no, [RS-NNN, …])]` for the section's prose declarations (C-18).

    Fenced code blocks (backtick and tilde fences) and heading lines are removed first; a
    remaining `- **Runtime dependency**: …` line is a declaration. With an id it is a finding;
    without one it is an input error naming the line, because the reason's argument grammar
    admits only an id — and a silent pass there would be the false green this rule removes.
    """
    declarations = []
    in_fence = False
    for number, line in body_lines:
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if in_fence or HEADING_RE.match(line):
            continue
        stripped = line.strip()
        if not PROSE_DECLARATION_RE.match(stripped):
            continue
        declared = re.findall(r"\bRS-\d{3}\b", stripped)
        if not declared:
            raise InputError(
                "%s:%d is a prose runtime declaration carrying no `RS-NNN` id: the reason's "
                "argument grammar admits only an id, so this line is an input error rather than "
                "a silent pass" % (path, number)
            )
        declarations.append((number, declared))
    return declarations


def parse_fr_ids(path):
    """The `FR-NNN` ids `requirements.md` itself defines (obligation ①'s resolution target)."""
    return set(FR_DEFINITION_RE.findall(_read(path)))


# --------------------------------------------------------------------------- #
# plan.md — premises and inherited blockers (C-14)
# --------------------------------------------------------------------------- #

def parse_plan(path, flow_class):
    """`{premises, inherited}` rows from the two tables.

    C-14: both sections MUST be present for an `execution`-class feature; their absence is an
    input error, because an incomplete plan is a defect of the artifact rather than a finding
    about the feature. The inherited table is read by column name, and `Carrier slice` is part of
    every `inherited` judgement (C-17).
    """
    text = _read(path)
    result = {"premises": [], "inherited": []}

    try:
        premises_lines = _section_lines(text, PREMISES_SECTION_RE, "Execution Premises", path)
    except InputError:
        if flow_class == "execution":
            raise
        premises_lines = []
    for number, row in _table_rows(premises_lines):
        ep_id = _clean(_column(row, "id"))
        if not EP_ID_RE.match(ep_id):
            raise InputError(
                "%s § Execution Premises row %d carries no `EP-NNN` id (AS-09)" % (path, number)
            )
        status = _clean(_column(row, "status"))
        if status not in PREMISE_STATUSES:
            raise InputError(
                "%s § Execution Premises row %s declares `Status: %s`; the closed set is "
                "verified / unverified / falsified (AS-09)" % (path, ep_id, status or "<empty>")
            )
        result["premises"].append({
            "id": ep_id,
            "status": status,
            "decision": _column(row, "decision"),
        })

    try:
        inherited_lines = _section_lines(text, INHERITED_SECTION_RE, "Inherited Blockers", path)
    except InputError:
        if flow_class == "execution":
            raise
        inherited_lines = []
    for index, (number, row) in enumerate(_table_rows(inherited_lines), start=1):
        result["inherited"].append({
            "line": number,
            "row": _clean(_column(row, "#", "id")) or "row-%d" % index,
            "source": _column(row, "source row", "source"),
            "disposition": _clean(_column(row, "disposition")),
            "carrier": _column(row, "carrier (must be filled when `inherited`)", "carrier"),
            "carrier_slice": _column(row, "carrier slice"),
        })
    result["inherited_declaration"] = "\n".join(
        line for _, line in inherited_lines
    )
    try:
        d10_lines = _section_lines(text, D10_SECTION_RE, "D10", path)
    except InputError:
        d10_lines = []
    result["d10"] = "\n".join(line for _, line in d10_lines)
    return result


# --------------------------------------------------------------------------- #
# tasks.md — the three open-row counts (C-15)
# --------------------------------------------------------------------------- #

def parse_tasks(path):
    """`{open, in_progress, deferred, closed}` row counts.

    The counts are read because they are completion condition ①; the closed reason set carries no
    reason keyed on them, so an open row alone cannot force a `block` — it can only make a
    claimed-`Implemented` status exceed its evidence (V-12).
    """
    counts = {"open": 0, "in_progress": 0, "deferred": 0, "closed": 0}
    for line in _read(path).splitlines():
        match = TASK_ROW_RE.match(line)
        if not match:
            continue
        mark = match.group(1)
        if mark == " ":
            counts["open"] += 1
        elif mark == ">":
            counts["in_progress"] += 1
        elif mark == "~":
            counts["deferred"] += 1
        elif mark in ("x", "X"):
            counts["closed"] += 1
    return counts


# --------------------------------------------------------------------------- #
# verification.md — status rows, the five ladder fields, the smoke record (C-16)
# --------------------------------------------------------------------------- #

def parse_verification(path):
    """`{statuses, ladder, smoke, joint_acceptance}`.

    Values are collected per key rather than overwritten: a duplicated key is a defect the smoke
    record must be able to see (V-8), and silently keeping the last one would hide it.
    """
    statuses = {}
    ladder = {}
    smoke = {}
    joint = {}
    for raw in _read(path).splitlines():
        match = FIELD_RE.match(raw.rstrip())
        if not match:
            continue
        key, value = match.group(1), match.group(2).strip()
        status_match = SC_STATUS_KEY_RE.match(key)
        if status_match:
            statuses.setdefault(status_match.group(1), []).append(value)
            continue
        ladder_match = SC_LADDER_KEY_RE.match(key)
        if ladder_match:
            ladder.setdefault(ladder_match.group(1), {})[ladder_match.group(2)] = value
            continue
        if key in SMOKE_FIELDS:
            smoke.setdefault(key, []).append(value)
            continue
        joint_match = JOINT_ACCEPTANCE_KEY_RE.match(key)
        if joint_match:
            joint.setdefault(joint_match.group(1), []).append(value)
    return {
        "statuses": statuses,
        "ladder": ladder,
        "smoke": smoke,
        "joint_acceptance": joint,
    }


def evaluate_smoke(verification, repo):
    """`(passes, detail)` for completion condition ④.

    A missing record is **not** an input error: the owner doc says so explicitly — it is a
    completeness fact about the feature. Three fields, exactly one record (V-8): a second
    `smoke_command=` line is a defect, so it cannot pass. The evidence path is read relative to
    the repository root, never to the current working directory, so the verdict does not depend on
    where the caller stood.
    """
    smoke = verification["smoke"]
    commands = smoke.get("smoke_command", [])
    exits = smoke.get("smoke_exit_code", [])
    evidence = smoke.get("smoke_evidence_path", [])
    detail = {
        "present": bool(commands),
        "records": len(commands),
        "command": commands[0] if commands else "",
        "exit_code": exits[0] if exits else "",
        "evidence_path": evidence[0] if evidence else "",
        "evidence_exists": False,
    }
    if len(commands) != 1 or len(exits) != 1 or len(evidence) != 1:
        return False, detail
    if exits[0].strip() != "0":
        return False, detail
    rel = evidence[0].strip()
    if _blank(rel):
        return False, detail
    candidate = Path(rel)
    if not candidate.is_absolute():
        candidate = Path(repo) / rel
    try:
        detail["evidence_exists"] = candidate.is_file() and candidate.stat().st_size > 0
    except OSError:
        detail["evidence_exists"] = False
    return bool(detail["evidence_exists"]), detail


# --------------------------------------------------------------------------- #
# The judgement
# --------------------------------------------------------------------------- #

def _reason(code, target=""):
    return {"code": code, "target": target}


def _dedupe(reasons):
    """One instance per fact: the same `(code, argument)` is reported once, in first-seen order.

    The reason record counts reasons, and two paths to the same fact (a runtime-stack row citing a
    falsified premise, and the premise table itself) would otherwise make one defect look like two.
    """
    seen = set()
    unique = []
    for reason in reasons:
        instance = (reason["code"], reason["target"])
        if instance in seen:
            continue
        seen.add(instance)
        unique.append(reason)
    return unique


def _first_status(statuses, sc_id):
    values = statuses.get(sc_id, [])
    return values[0] if values else ""


def final_path_counts(criteria, statuses):
    """C-08: the closed count record over the `final`-path criteria, computed once, here.

    No caller, template or report recomputes these: a report copies them. An SC with no status row
    counts as `unknown` — a missing measurement is not evidence of anything, least of all of a
    pass.
    """
    counts = {bucket: 0 for bucket in FINAL_PATH_BUCKETS}
    counts["total"] = 0
    for sc_id, path in criteria.items():
        if path != "final":
            continue
        counts["total"] += 1
        value = _first_status(statuses, sc_id)
        counts[value if value in FINAL_PATH_BUCKETS else "unknown"] += 1
    return counts


def final_path_reasons(flow_class, criteria, statuses, counts):
    """V-11: one reason shape per situation, and none at all for an `expression` feature.

    `zero-final-path-pass` is emitted **once** when the `final`-path pass count is zero;
    `final-path-not-pass: SC-NNN` is emitted per failing SC when at least one other `final`-path SC
    passed. The rule is vacuous for `expression`, whose class is read from the declaration, so such
    a feature is never forced to invent a `final` criterion.
    """
    if flow_class != "execution":
        return []
    if counts["total"] == 0 or counts["pass"] == 0:
        return [_reason(R_ZERO_FINAL_PASS)]
    return [
        _reason(R_FINAL_PATH_NOT_PASS, sc_id)
        for sc_id in sorted(criteria)
        if criteria[sc_id] == "final" and _first_status(statuses, sc_id) != "pass"
    ]


def ladder_reasons(criteria, verification):
    """V-5/V-6: a `blocked` / `deferred` / `partial` row that cannot account for itself.

    The trigger is mechanical on both halves: a missing ladder field, or a `reduced_measurement`
    written down whose `..._run` is not `yes`. The second is the one that matters — a measurement
    recorded and not run is the same shape as the defect the ladder exists to stop, not an honest
    substitute for running it. This is a row-legality rule, so it applies whatever the row's path:
    the `supporting` exemption covers a non-`pass` **status**, never a missing required field.
    """
    reasons = []
    for sc_id in sorted(criteria):
        if _first_status(verification["statuses"], sc_id) not in LADDER_STATUSES:
            continue
        row = verification["ladder"].get(sc_id, {})
        missing = [field for field in LADDER_FIELDS if _blank(row.get(field, ""))]
        written_not_run = (
            not _blank(row.get("reduced_measurement", ""))
            and row.get("reduced_measurement_run", "").strip() != "yes"
        )
        if missing or written_not_run:
            reasons.append(_reason(R_LADDER, sc_id))
    return reasons


def runtime_reasons(requirements, fr_ids, tasks_text, verification, premises, repo):
    """AS-05…AS-08 / C-13 / C-18: the runtime-stack class and the prose-declaration rule.

    Three shapes, three verdicts, and **silence is not one of them**: an absent section is an
    input error (raised by `parse_requirements`), a section with zero data rows blocks under the
    reserved `runtime-stack` argument, and a row with a required-but-empty cell blocks under its
    own id. Cell-shape defects — a `Form` outside the domain, a `Premises` id with no matching
    row, a `signed-contract` `Contract` path that does not resolve — exit 2, because a cell that
    cannot be parsed is a fact about the artifact.

    Duty ③ (a joint-acceptance row naming the `RS-NNN`) is judged here, at closure: no stage gate
    takes `verification.md` as input. Duty ② is a **line-level** `tasks.md` row match, never a
    whole-file substring — an FR named in a table cell or in prose is not a task row (FR-009).
    """
    reasons = []
    if not requirements.get("runtime_section_present", True):
        # `expression`-class feature with no table: legal, and the reserved block does not apply —
        # the section is absent for a class that is exempt, not present-and-empty.
        return reasons
    if requirements["runtime_row_count"] == 0:
        reasons.append(_reason(R_RUNTIME, RESERVED_RUNTIME_ARGUMENT))
    for _, declared in requirements["prose"]:
        for rs_id in declared:
            reasons.append(_reason(R_RUNTIME, rs_id))

    for row in requirements["runtime_rows"]:
        rs_id, form = row["id"], row["form"]
        if form == FORM_NOT_REQUIRED:
            continue
        problems = False
        if _blank(row["capability"]):
            problems = True
        cited = FR_ID_RE.findall(_clean(row["fr"]))
        if form == FORM_IN_SCOPE:
            if not cited:
                raise InputError(
                    "%s § Runtime Stack row %s declares `Form: in-scope` with an empty `FR` "
                    "cell — a defect of the artifact, never a `block` about the feature "
                    "(AS-07 ①)" % (requirements["path"], rs_id)
                )
            unresolved = [fr for fr in cited if fr not in fr_ids]
            if unresolved:
                raise InputError(
                    "%s § Runtime Stack row %s cites %s, which this specification does not "
                    "define — a defect of the artifact, never a `block` about the feature "
                    "(AS-07 ①)" % (requirements["path"], rs_id, ", ".join(sorted(unresolved)))
                )
            if _blank(row["joint_acceptance"]):
                problems = True
            if not any(_task_row_quotes(tasks_text, fr) for fr in cited):
                problems = True
            if rs_id not in verification["joint_acceptance"]:
                problems = True
        elif form == FORM_SIGNED:
            contract = _clean(row["contract"])
            if (_blank(row["pin"]) or not contract or _blank(row["joint_acceptance"])
                    or _blank(row["owner"])):
                problems = True
            if contract and not _resolves(contract, repo):
                raise InputError(
                    "%s § Runtime Stack row %s names a `Contract` path that does not resolve in "
                    "the checkout: %s (AS-06)" % (requirements["path"], rs_id, contract)
                )
        elif _blank(row["owner"]) or _blank(row["joint_acceptance"]):
            problems = True

        if cited:
            if _blank(row["premises"]):
                problems = True
            else:
                for ep_id in EP_ID_RE.findall(_clean(row["premises"])):
                    if ep_id not in premises:
                        raise InputError(
                            "%s § Runtime Stack row %s cites %s, which § Execution Premises does "
                            "not define — a defective cell (AS-09 / AS-11)"
                            % (requirements["path"], rs_id, ep_id)
                        )
        if problems:
            reasons.append(_reason(R_RUNTIME, rs_id))
    return reasons


def _task_row_quotes(tasks_text, fr_id):
    """Whether a **task row** quotes `fr_id` — the line-level match of FR-009, never a substring."""
    pattern = re.compile(r"^- \[.\] T\d{3}.*\b%s\b" % re.escape(fr_id))
    return any(pattern.match(line) for line in tasks_text.splitlines())


def _resolves(relative_path, repo):
    """Whether a repo-relative path resolves in the checkout."""
    candidate = Path(relative_path)
    if not candidate.is_absolute():
        candidate = Path(repo) / relative_path
    return candidate.is_file()


def premise_reasons(plan):
    """AS-09: a `falsified` premise with no decision recorded.

    `unverified` is not a block: the closed reason set names only the undecided falsification, and
    a set that grew to cover "still being checked" would refuse every plan in progress.
    """
    return [
        _reason(R_PREMISE, row["id"])
        for row in plan["premises"]
        if row["status"] == "falsified" and _blank(row["decision"])
    ]


def declared_dependency_files(section_text, spec_dir):
    """The dependency artifacts the plan's declaration names, resolved and deduplicated.

    The dependency set is **declared, never implied**: only a backticked `.md` token inside
    `§ Inherited Blockers` is read, so an unopened dependency is visible as a missing row instead
    of being silently assumed away.
    """
    found = []
    for token in re.findall(r"`([^`\n]+)`", section_text):
        token = token.strip()
        if not token.endswith(".md"):
            continue
        candidate = Path(spec_dir) / token
        if candidate.is_file() and candidate not in found:
            found.append(candidate)
    return found


def _deferred_locators(text, feature_id):
    """One locator per non-empty `## Deferred` list item (`deferred:<slug>`, else `row-<n>`)."""
    try:
        body = _section_lines(text, DEFERRED_SECTION_RE, "Deferred", "the dependency detail")
    except InputError:
        return []
    locators = []
    index = 0
    for _, line in body:
        stripped = line.strip()
        if not stripped.startswith("-"):
            continue
        content = stripped.lstrip("-").strip()
        if not content:
            continue
        index += 1
        label = re.match(r"\*\*(.+?)\*\*", content)
        slug = ""
        if label:
            slug = re.sub(r"\s+", "-", label.group(1).strip().lower())
            if not re.match(r"^[a-z0-9][a-z0-9-]*$", slug):
                slug = ""
        locators.append("%s:deferred:%s" % (feature_id, slug or "row-%d" % index))
    return locators


def _verification_locators(text, feature_id):
    """`blocked` / `deferred` / **`partial`** status rows plus a non-empty `deferred_tasks=`."""
    locators = []
    for line in text.splitlines():
        stripped = line.strip()
        status = re.match(r"^(SC-\d{3})_status=(.*)$", stripped)
        if status:
            if status.group(2).strip() in EXTRACTED_STATUSES:
                locators.append("%s:%s_status" % (feature_id, status.group(1)))
            continue
        deferred = re.match(r"^deferred_tasks=(.*)$", stripped)
        if deferred and deferred.group(1).strip():
            locators.append("%s:deferred_tasks" % feature_id)
    return locators


def extracted_dependency_rows(section_text, spec_dir):
    """Every row the closed three-source set yields (C-17), in declaration order.

    Three sources and nowhere else: the dependency's `## Deferred` list items, its `verification.md`
    status rows in `blocked` / `deferred` / `partial`, and a **non-empty** `deferred_tasks=` list.
    `partial` is inside the set because a dependency may carry `partial` rows and nothing else —
    an extraction set that excluded it would be disjoint from the disposition set and the finding
    could never fire.
    """
    details, verifications = [], []
    for path in declared_dependency_files(section_text, spec_dir):
        text = _read(path)
        (verifications if VERIFICATION_FIELD_RE.search(text) else details).append(text)

    feature_ids = []
    for text in details:
        match = FEATURE_ID_RE.search(text)
        feature_ids.append(match.group(1) if match else None)
    default_id = next((fid for fid in feature_ids if fid), None)

    locators = []
    for text, feature_id in zip(details, feature_ids):
        if feature_id:
            locators.extend(_deferred_locators(text, feature_id))
    for text in verifications:
        first = next((line for line in text.splitlines() if line.strip()), "")
        match = re.search(r"\b(\d{3})\b", first)
        feature_id = match.group(1) if match else default_id
        if feature_id:
            locators.extend(_verification_locators(text, feature_id))
    return locators


def parse_carrier(raw):
    """`("task", T-ID, path)` / `("gate", GATE-ID)` / `("test", path)` / `None`.

    `SC-NNN` is not a carrier at all: a criterion that may be deferred cannot carry an inherited
    measurement, so a `supporting`-path SC in this cell is judged exactly as an undisposed row.
    """
    match = CARRIER_TASK_RE.match(raw)
    if match:
        return ("task", match.group(1), match.group(2))
    match = CARRIER_GATE_RE.match(raw)
    if match:
        return ("gate", match.group(1))
    match = CARRIER_TEST_ONLY_RE.match(raw)
    if match:
        return ("test", match.group(1))
    return None


def carrier_resolves(parsed, tasks_text):
    """`True` when the named carrier resolves in this slice's `tasks.md`."""
    kind = parsed[0]
    if kind == "task":
        task_id, test_path = parsed[1], parsed[2]
        rows = {}
        for line in tasks_text.splitlines():
            match = TASK_ROW_ID_RE.match(line)
            if match:
                rows[match.group(1)] = line
        return task_id in rows and test_path in rows[task_id]
    if kind == "gate":
        return any(match.group(1) == parsed[1] for match in GATE_ROW_RE.finditer(tasks_text))
    return False


def later_slice_is_legal(slice_value, spec_dir, claimed_status, plan):
    """A later `Carrier slice` is legal only while the parent is `Blocked` and D10 lists it."""
    if claimed_status != "Blocked":
        return False
    return bool(re.search(r"(?<!\w)%s(?!\w)" % re.escape(slice_value),
                          plan.get("d10", "")))


def inherited_reasons(plan, key, spec_dir, tasks_text, claimed_status):
    """AS-10 / C-17: the undisposed row, and the `inherited` row whose carrier cannot carry.

    Extraction **discovers** rows: the three closed sources are read from the dependency artifacts
    the plan declares, and every extracted locator is joined to a disposition row by its own
    `Source row` cell. One reason covers five ways to fail — undisposed, blank carrier,
    unparseable carrier, unresolvable carrier, deferrable-`supporting`-SC carrier — so the closed
    set does not grow. A later-slice carrier is not one of them: `Carrier slice` plus the parent's
    claimed status make it **`inherited-later`** — disclosed, neither blocking nor resolved.
    """
    reasons = []
    seen = {}
    entries = []
    for row in plan["inherited"]:
        source = _clean(row["source"])
        if source and not SOURCE_LOCATOR_RE.match(source):
            if source.lower() not in ABSENT_LOCATORS:
                raise InputError(
                    "plan.md § Inherited Blockers row %s carries `Source row` %r, which is not a "
                    "`<feature>:<row>` locator — the join key has one grammar (C-17)"
                    % (row["row"], source)
                )
            source = ""
        if source:
            if source in seen:
                raise InputError(
                    "plan.md § Inherited Blockers disposes %s twice (rows %s and %s) — the join "
                    "key must be unique" % (source, seen[source], row["row"])
                )
            seen[source] = row["row"]
        entries.append({
            "source": source,
            "row": row["row"],
            "disposition": row["disposition"],
            "carrier": _clean(row["carrier"]),
            "slice": "" if _blank(row["carrier_slice"]) else _clean(row["carrier_slice"]),
        })

    for entry in entries:
        disposition = entry["disposition"]
        carrier = entry["carrier"]
        slice_value = entry["slice"]
        if slice_value and slice_value != "this-slice" and not LATER_SLICE_RE.match(slice_value):
            raise InputError(
                "plan.md § Inherited Blockers row %s declares `Carrier slice: %s`, which is "
                "neither `this-slice` nor a slice id (C-17)" % (entry["row"], slice_value)
            )
        failed = False
        if disposition not in DISPOSITIONS:
            failed = True
        elif disposition == "inherited":
            parsed = parse_carrier(carrier) if carrier else None
            if not carrier or parsed is None:
                failed = True
            elif LATER_SLICE_RE.match(slice_value or "") and later_slice_is_legal(
                    slice_value, spec_dir, claimed_status, plan):
                # `inherited-later`: the carrier is the test path alone, and the task id of an
                # unwritten `tasks.md` MUST NOT be fabricated.
                failed = parsed[0] != "test"
            else:
                failed = not carrier_resolves(parsed, tasks_text)
        if failed:
            reasons.append(_reason(
                R_INHERITED, entry["source"] or "%s:%s" % (key, entry["row"])))

    for locator in extracted_dependency_rows(plan.get("inherited_declaration", ""), spec_dir):
        if locator not in seen:
            reasons.append(_reason(R_INHERITED, locator))
    return reasons


def completion_conditions(criteria, statuses, tasks, smoke_passes, flow_class):
    """The four conjunctive conditions of `Planned → Implemented` (owner § Feature Status).

    Read only to answer V-12's question — "does the claimed status exceed its evidence?" — and
    never to force a `block` on its own: the closed reason set has no reason keyed on an open task
    row, and inventing one here would grow the set locally.
    """
    no_open_rows = tasks["open"] == 0 and tasks["in_progress"] == 0
    every_row = bool(criteria) and all(
        _first_status(statuses, sc_id) in STATUS_VALUES for sc_id in criteria
    )
    final_all_pass = True
    if flow_class == "execution":
        final_all_pass = all(
            _first_status(statuses, sc_id) == "pass"
            for sc_id, path in criteria.items() if path == "final"
        )
    return {
        "no_open_rows": no_open_rows,
        "status_row_per_criterion": every_row,
        "every_final_path_pass": final_all_pass,
        "smoke_record_pass": smoke_passes,
    }


def apply_waivers(reasons, waivers, key):
    """C-06: a waived reason leaves the blocking set and is still counted as waived.

    Matching is one part of the reason's own instance: for an argument-taking template the waiver's
    target must equal the reason's argument, while an argument-less template has no argument to
    match, so its waiver target names the feature instead (`<spec key>`, or `*`). Only reasons
    actually removed are reported as waived — a waiver that suppressed nothing is not evidence of
    anything and must not pad the summary.
    """
    blocking = list(reasons)
    waived = []
    for code, target in waivers:
        if code not in REASON_CODES:
            raise InputError(
                "--waive %r names no member of the closed reason set: %s"
                % (code, ", ".join(REASON_CODES))
            )
        if code in ARGUMENTLESS_REASONS:
            if target not in (key, "*"):
                raise InputError(
                    "--waive %s takes no argument, so its target names the feature being "
                    "waived: use %r (or `*`), got %r" % (code, key, target)
                )
            matched = [r for r in blocking if r["code"] == code]
        else:
            matched = [r for r in blocking if r["code"] == code and r["target"] == target]
        for reason in matched:
            blocking.remove(reason)
            waived.append(_reason(reason["code"], reason["target"]))
    return blocking, waived


def run(args):
    """Compute the record the schema owner describes, or raise an InputError.

    It never returns a verdict it cannot justify from the inputs: every `block` carries at least
    one reason from the closed set, and an input defect is raised as an input error instead of
    being reported as a finding about the feature.
    """
    if args.audit_existing:
        raise ModeNotImplemented(
            "--audit-existing is not implemented in this slice: FR-020's read-only audit is "
            "081d work (plan.md § Slice Boundary). Refusing to emit a per-feature verdict from "
            "an audit invocation rather than report the opposite of what the mode must do."
        )

    resolved = resolve_inputs(args)
    spec_dir = resolved["spec_dir"]
    requirements = parse_requirements(resolved["requirements.md"])
    flow_class = requirements["flow_class"]
    criteria = requirements["criteria"]
    plan = parse_plan(resolved["plan.md"], flow_class)
    tasks = parse_tasks(resolved["tasks.md"])
    tasks_text = _read(resolved["tasks.md"])
    verification = parse_verification(resolved["verification.md"])
    smoke_passes, smoke_detail = evaluate_smoke(verification, resolved["repo"])
    claimed_status, claimed_source = resolve_claimed_status(resolved)

    statuses = verification["statuses"]
    counts = final_path_counts(criteria, statuses)
    premises = {row["id"]: row for row in plan["premises"]}

    reasons = []
    reasons.extend(final_path_reasons(flow_class, criteria, statuses, counts))
    reasons.extend(ladder_reasons(criteria, verification))
    reasons.extend(runtime_reasons(
        requirements,
        parse_fr_ids(resolved["requirements.md"]),
        tasks_text,
        verification,
        premises,
        resolved["repo"],
    ))
    reasons.extend(premise_reasons(plan))
    reasons.extend(inherited_reasons(
        plan, feature_key(spec_dir), spec_dir, tasks_text, claimed_status))
    # Two producers, one closed set, one instance per fact: the runtime-row duty and the
    # premise table can each reach the same falsified premise, and the payload counts reasons, so
    # the same instance is reported once.
    reasons = _dedupe(reasons)

    conditions = completion_conditions(criteria, statuses, tasks, smoke_passes, flow_class)
    if claimed_status in CLAIMED_IMPLEMENTED and not all(conditions.values()):
        reasons.append(_reason(R_CLAIMED))

    blocking, waived = apply_waivers(reasons, resolved["waivers"], feature_key(spec_dir))

    return {
        "verdict": "block" if blocking else "accept",
        "reasons": blocking,
        "waived": waived,
        "final_path": counts,
        "flow_class": flow_class,
        "claimed_status": claimed_status,
        "claimed_status_source": claimed_source,
        "tasks": tasks,
        "smoke": smoke_detail,
        "completion_conditions": conditions,
        "spec_dir": str(spec_dir),
    }


def instance(reason):
    """`{code, target}` → the emitted instance, `code + ": " + target` (or `code`)."""
    return reason["code"] if not reason["target"] else "%s: %s" % (reason["code"], reason["target"])


def render_human(record):
    """C-05: the default output is the report — verdict, every reason, the final-path counts."""
    counts = record["final_path"]
    lines = [
        "verdict: %s" % record["verdict"],
        "spec_dir: %s" % record["spec_dir"],
        "flow_class: %s" % record["flow_class"],
        "claimed_status: %s" % record["claimed_status"],
        "final_path: " + " ".join(
            "%s=%d" % (bucket, counts[bucket]) for bucket in FINAL_PATH_BUCKETS + ("total",)
        ),
    ]
    for reason in record["reasons"]:
        lines.append("reason: %s" % instance(reason))
    for reason in record["waived"]:
        lines.append("waived: %s" % instance(reason))
    if not record["reasons"]:
        lines.append("reason: none")
    return "\n".join(lines)


def emit(record, args, exit_code):
    """Print the payload and honour `--json` / `--json-out` (C-05).

    `--json` replaces the human report with the payload on stdout; `--json-out` writes the same
    payload to a file. The payload is computed once either way, so the two outputs cannot drift.
    """
    if record is None:
        return
    payload = json.dumps(record, indent=2, ensure_ascii=False, sort_keys=True)
    if args.json:
        print(payload)
    else:
        print(render_human(record))
    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as handle:
            handle.write(payload + "\n")


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Deterministic closure verdict for a feature: may it be called Implemented?",
    )
    # `--spec-dir` is validated in resolve_inputs rather than by argparse's `required=True`, so the
    # exit-2 message names the path argument and the inputs it must carry (C-02) instead of
    # argparse's usage banner.
    parser.add_argument("--spec-dir", default="",
                        help="spec directory holding requirements/plan/tasks/verification")
    parser.add_argument("--repo", default="",
                        help="repository root for repo-relative path resolution")
    parser.add_argument("--feature-detail", default=None,
                        help="feature detail file carrying the claimed status")
    parser.add_argument("--feature-registry", default=None,
                        help="feature registry file carrying the claimed status")
    parser.add_argument("--audit-existing", action="store_true",
                        help="read-only audit mode; exit code reflects input validity only")
    parser.add_argument("--json", action="store_true",
                        help="machine-readable payload on stdout")
    parser.add_argument("--json-out", default="",
                        help="write the identical payload to this file")
    parser.add_argument("--waive", action="append", default=[], metavar="CODE:TARGET",
                        help="remove one reason from the blocking set, counting it as waived")
    args = parser.parse_args(argv)

    try:
        record = run(args)
    except InputError as exc:
        print("closure-acceptance-check: input error: %s" % exc, file=sys.stderr)
        return EXIT_INPUT

    exit_code = EXIT_ACCEPT if record["verdict"] == "accept" else EXIT_BLOCK
    emit(record, args, exit_code)
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
