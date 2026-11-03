#!/usr/bin/env python3
"""pre-analyze-check.py — deterministic cross-artifact gate before analyze.

Runs at the driver's U4 for requirements / plan / tasks and blocks the analyze
dispatch on mechanical drift: duplicate or dangling IDs, count claims that
disagree with the actual definitions, and blockedBy targets that do not exist.
Dead backticked paths are reported as advisories (deliverables may legitimately
not exist yet) and only block under ``--strict``.

Formal artifacts only: notes/, review.md and verification.md are dated records
and are never scanned for live consistency.

Exit codes:
  0 = pass (no blocking findings)
  1 = fail (at least one blocking finding)
  2 = input or parse error

Standard library only, Python >= 3.8. Self-contained; never reads the
framework runtime scripts tree.
"""

import argparse
import json
import os
import re
import sys
import time

FORMAL_NAMES = (
    "requirements.md", "plan.md", "tasks.md", "data-model.md",
    "quickstart.md", "research.md", "feature-ref.md",
)
FORMAL_GLOBS = ("contracts", "checklists")
SKIP_HEADING = re.compile(
    r"(?i)repair record|repair log|history|changelog|修订|变更记录|修复记录")
HEADING = re.compile(r"^(#{1,6})\s+")

FR_DEF = re.compile(r"^- \*\*FR-(\d{3})\*\*:")
SC_DEF = re.compile(r"^- \*\*SC-(\d{3})\*\*:")
TASK_DEF = re.compile(r"^- \[[ xX>~]\] (T\d{3})")
CLAUSE_DEF = re.compile(r"^- \*\*([A-Z]{2,4}-\d{2})\b")
FR_REF = re.compile(r"\bFR-(\d{3})\b")
SC_REF = re.compile(r"\bSC-(\d{3})\b")
CLAUSE_REF = re.compile(r"\b([A-Z]{2,4}-\d{2})\b")
NON_CLAUSE_PREFIXES = {"FR", "SC", "SHA", "ISO", "UTF"}
BLOCKED_BY = re.compile(r"\[blockedBy:\s*([^\]]+)\]")
TASK_TOKEN = re.compile(r"^T\d{3}$")

COUNT_CLAIMS = (
    ("FR", re.compile(r"(?<![\w-])(\d{1,3})\s*FR\b")),
    ("SC", re.compile(r"(?<![\w-])(\d{1,3})\s*SC\b")),
    ("tasks", re.compile(r"(?<![\w-])(\d{1,3})\s*(?:tasks?|条任务|个任务|任务行|task rows)\b")),
)
HISTORICAL_LINE = re.compile(
    r"→|->|\bvs\b|\bfrom\b|\bprevious\b|\bwas\b|\brebaseline|\bre-baseline|"
    r"原|前值|修复|变更|迁移|drift|\brepair(?:ed)?\b|应为|instead|"
    r"\b[0-9a-f]{7,40}\b")
COUNT_SKIP_LINE = re.compile(
    r"(?i)\bgiven\b|\bwhen\b|\bthen\b|fixture|夹具|示例|例如|举例|e\.g\.|"
    r"interval|区间|范围|threshold|ceiling|上限|下限|端点")

BACKTICK = re.compile(r"`([^`\n]+)`")
PATH_TOKEN = re.compile(r"^[A-Za-z0-9._-]+(?:/[A-Za-z0-9._-]+)+/?$")
PATH_ROOTS = (
    ".specify/", "skills/", "shared/", "templates/",
    "src/", "agents/", "tests/", "docs/", "feedback/",
)

STAGES = {
    "requirements": ("requirements.md",),
    "plan": ("requirements.md", "plan.md"),
    "tasks": ("requirements.md", "plan.md", "tasks.md"),
}

# --- ownership / premise findings (081b) ----------------------------------------------------
# The four `check` names are fixed by `contracts/gate-wiring.contract.md` GW-07, so a waiver key
# (`--waive CHECK:REL_PATH:LINE`) stays writable and an accidental weakening shows up in a diff.
# All four are `error`: an `advisory` here would let "must block" degrade into a note nothing
# reads.
CHECK_RUNTIME_ROW = "runtime-stack-row"
CHECK_RUNTIME_CONTRACT = "runtime-contract-incomplete"
CHECK_PREMISE = "premise-undecided"
CHECK_INHERITED = "inherited-blocker"

# The three reason prefixes are *templates* owned by the declaring specification's
# `## Shared Strings` (STR-011…STR-013). A finding carries the *instance* —
# `prefix + ": " + argument` — at the end of its message, introduced by the literal `reason: `,
# so neither producer re-spells a template and a membership test can read the argument.
REASON_RUNTIME = "runtime-dependency-not-owned"
REASON_PREMISE = "falsified-premise-undecided"
REASON_INHERITED = "inherited-blocker-undisposed"
#: The one reserved argument: the zero-data-row shape has no `RS-NNN` to name, and a fabricated
#: id would point at a row nobody wrote.
RESERVED_RUNTIME_ARGUMENT = "runtime-stack"

RUNTIME_SECTION = re.compile(r"^#{2,4}\s+Runtime Stack & Dependency Ownership")
PREMISES_SECTION = re.compile(r"^#{2,4}\s+Execution Premises\s*$")
INHERITED_SECTION = re.compile(r"^#{2,4}\s+Inherited Blockers\s*$")
DEFERRED_SECTION = re.compile(r"^#{2,4}\s+Deferred\s*$")
D10_SECTION = re.compile(r"^#{2,4}\s+D10\b")
FENCE = re.compile(r"^\s*(```|~~~)")
PROSE_DECLARATION = re.compile(r"^-\s*\*\*Runtime dependency\*\*:")
FLOW_CLASS = re.compile(r"(?m)^\*\*Flow Class\*\*:\s*(\S+)\s*$")
FEATURE_ID = re.compile(r"(?m)^\*\*Feature ID\*\*:\s*(\d{3})\s*$")
DETAIL_STATUS = re.compile(r"(?m)^\*\*Status\*\*:\s*(.+?)\s*$")
RS_ID = re.compile(r"^RS-\d{3}$")
EP_ID = re.compile(r"^EP-\d{3}$")
FR_ID = re.compile(r"\bFR-\d{3}\b")
TASK_QUOTES_FR = r"^- \[.\] T\d{3}.*\b%s\b"
CARRIER_TASK = re.compile(r"^task:(T\d{3})\+test:(\S+)$")
CARRIER_GATE = re.compile(r"^gate:(GATE-\d+)$")
CARRIER_TEST_ONLY = re.compile(r"^test:(\S+)$")
SOURCE_LOCATOR = re.compile(r"^\S+:\S+$")
LATER_SLICE = re.compile(r"^\d{3}[a-z]?$")
TABLE_SEPARATOR = re.compile(r"^\|?[\s:|-]+\|?$")
VERIFICATION_FIELD = re.compile(r"(?m)^(?:SC-\d{3}_status|deferred_tasks)=")
GATE_ROW = re.compile(r"(?m)^\s*[-*]?\s*(GATE-\d+)\b")

#: Cells that carry no content. A dash is how these tables spell "nothing here", so it must read
#: as empty rather than as a value.
EMPTY_CELLS = ("", "-", "--", "—", "–")
#: `Source row` values that mean "this row disposes nothing". `(none)` is what the 081a fixtures
#: write for a feature with no dependency set; it is a sentinel, not a malformed locator.
ABSENT_LOCATORS = ("(none)", "none", "n/a", "(no dependency)")
#: The closed `Disposition` domain.
DISPOSITIONS = ("resolved", "inherited", "not-applicable")
#: The closed `Status` domain of `§ Execution Premises`.
PREMISE_STATUSES = ("verified", "unverified", "falsified")
FLOW_CLASSES = ("execution", "expression")


class InputError(Exception):
    pass


def read_file(path):
    try:
        with open(path, "r", encoding="utf-8") as handle:
            return handle.read()
    except OSError as exc:
        raise InputError("cannot read %s: %s" % (path, exc))


def formal_files(spec_dir):
    files = []
    for name in FORMAL_NAMES:
        path = os.path.join(spec_dir, name)
        if os.path.isfile(path):
            files.append(path)
    for folder in FORMAL_GLOBS:
        root = os.path.join(spec_dir, folder)
        if not os.path.isdir(root):
            continue
        for name in sorted(os.listdir(root)):
            path = os.path.join(root, name)
            if os.path.isfile(path) and name.endswith(".md"):
                files.append(path)
    return files


def live_lines(text):
    """Yield (line_no, line) outside dated/history sections."""
    skip_level = None
    for number, line in enumerate(text.splitlines(), 1):
        heading = HEADING.match(line)
        if heading:
            level = len(heading.group(1))
            if skip_level is not None and level <= skip_level:
                skip_level = None
            if skip_level is None and SKIP_HEADING.search(line):
                skip_level = level
                continue
        if skip_level is not None:
            continue
        yield number, line


def definitions(files, spec_dir):
    fr, sc, tasks, clauses = {}, {}, {}, {}
    duplicates = []
    for path in files:
        rel = os.path.relpath(path, spec_dir).replace(os.sep, "/")
        owner = ("requirements.md" if rel == "requirements.md" else
                 "tasks.md" if rel == "tasks.md" else
                 "contracts" if rel.startswith("contracts/") else "")
        for number, line in live_lines(read_file(path)):
            if owner == "requirements.md":
                match = FR_DEF.match(line)
                if match:
                    key = "FR-" + match.group(1)
                    if key in fr:
                        duplicates.append((path, number, key, fr[key]))
                    else:
                        fr[key] = (path, number)
                    continue
                match = SC_DEF.match(line)
                if match:
                    key = "SC-" + match.group(1)
                    if key in sc:
                        duplicates.append((path, number, key, sc[key]))
                    else:
                        sc[key] = (path, number)
                    continue
            if owner == "tasks.md":
                match = TASK_DEF.match(line)
                if match:
                    key = match.group(1)
                    if key in tasks:
                        duplicates.append((path, number, key, tasks[key]))
                    else:
                        tasks[key] = (path, number)
                    continue
            if owner == "contracts":
                match = CLAUSE_DEF.match(line)
                if match:
                    key = match.group(1)
                    if key in clauses:
                        duplicates.append((path, number, key, clauses[key]))
                    else:
                        clauses[key] = (path, number)
    return fr, sc, tasks, clauses, duplicates


def add(findings, check, severity, path, line, message):
    findings.append({
        "check": check, "severity": severity,
        "path": path, "line": line, "message": message,
    })


def check_references(files, fr, sc, clauses, findings, spec_dir):
    has_clauses = bool(clauses)
    local_prefixes = {key.split("-", 1)[0] for key in clauses}
    for path in files:
        rel = os.path.relpath(path, spec_dir)
        for number, line in live_lines(read_file(path)):
            for match in FR_REF.finditer(line):
                key = "FR-" + match.group(1)
                if key not in fr:
                    add(findings, "dangling-id", "error", rel, number,
                        "references %s which is not defined" % key)
            for match in SC_REF.finditer(line):
                key = "SC-" + match.group(1)
                if key not in sc:
                    add(findings, "dangling-id", "error", rel, number,
                        "references %s which is not defined" % key)
            if not has_clauses:
                continue
            for match in CLAUSE_REF.finditer(line):
                key = match.group(1)
                prefix = key.split("-", 1)[0]
                if prefix in NON_CLAUSE_PREFIXES or key in clauses:
                    continue
                if prefix in local_prefixes:
                    add(findings, "dangling-id", "error", rel, number,
                        "references contract clause %s which is not defined" % key)
                else:
                    add(findings, "external-clause", "advisory", rel, number,
                        "references contract clause %s from an external namespace" % key)


def check_blocked_by(spec_dir, tasks, findings):
    path = os.path.join(spec_dir, "tasks.md")
    if not os.path.isfile(path):
        return
    for number, line in live_lines(read_file(path)):
        for match in BLOCKED_BY.finditer(line):
            for token in match.group(1).split(","):
                token = token.strip()
                if not token or not TASK_TOKEN.match(token):
                    add(findings, "blocked-by", "advisory", "tasks.md", number,
                        "non-concrete blockedBy token %r" % token)
                    continue
                if token not in tasks:
                    add(findings, "blocked-by", "error", "tasks.md", number,
                        "blockedBy target %s is not defined" % token)


def in_range(line, start, end):
    before = line[max(0, start - 6):start]
    after = line[end:end + 6]
    return bool(re.search(r"\d\s*[–\-/]\s*$", before)
                or re.match(r"^\s*[–\-/]\s*\d", after))


def check_counts(files, fr, sc, tasks, findings, spec_dir):
    actual = {"FR": len(fr), "SC": len(sc), "tasks": len(tasks) or None}
    for path in files:
        rel = os.path.relpath(path, spec_dir)
        for number, line in live_lines(read_file(path)):
            if HISTORICAL_LINE.search(line) or COUNT_SKIP_LINE.search(line):
                continue
            for kind, pattern in COUNT_CLAIMS:
                expected = actual[kind]
                if expected is None:
                    continue
                for match in pattern.finditer(line):
                    if in_range(line, match.start(), match.end()):
                        continue
                    claimed = int(match.group(1))
                    if claimed != expected:
                        add(findings, "count-claim", "error", rel, number,
                            "claims %d %s but the artifacts define %d"
                            % (claimed, kind, expected))


def check_paths(files, findings, spec_dir, repo):
    if not repo:
        return
    spec_rel = os.path.relpath(spec_dir, repo).replace(os.sep, "/")
    for path in files:
        rel = os.path.relpath(path, spec_dir)
        for number, line in live_lines(read_file(path)):
            for match in BACKTICK.finditer(line):
                token = match.group(1).strip()
                if not PATH_TOKEN.match(token):
                    continue
                if not token.startswith(PATH_ROOTS):
                    continue
                if spec_rel and (token == spec_rel or token.startswith(spec_rel + "/")):
                    continue
                if os.path.exists(os.path.join(repo, token)):
                    continue
                add(findings, "missing-path", "advisory", rel, number,
                    "path does not exist under the repo: %s" % token)


def line_cells(line):
    """The cells of one Markdown table line."""
    stripped = line.strip()
    if stripped.startswith("|"):
        stripped = stripped[1:]
    if stripped.endswith("|"):
        stripped = stripped[:-1]
    return [cell.strip() for cell in stripped.split("|")]


def clean_cell(value):
    """A cell value without its Markdown emphasis/backtick decoration."""
    return (value or "").strip().strip("`").strip()


def blank_cell(value):
    """`True` when a cell carries no content (see EMPTY_CELLS)."""
    return clean_cell(value) in EMPTY_CELLS


def section_lines(text, pattern, name, rel):
    """`[(line_no, line)]` for one `##`-level section body, or an InputError naming the file.

    Line numbers are absolute and 1-based: every finding this module emits is located, and a
    message that points at the wrong line is a defect of the gate. The body stops at the next
    heading of any level, so a table inside the section never bleeds into the prose below it.
    """
    lines = text.splitlines()
    start = None
    for index, line in enumerate(lines):
        if pattern.match(line):
            start = index
            break
    if start is None:
        raise InputError("%s carries no § %s" % (rel, name))
    body = []
    for offset in range(start + 1, len(lines)):
        if HEADING.match(lines[offset]):
            break
        body.append((offset + 1, lines[offset]))
    return body


def section_rows(body):
    """`[(line_no, {lower-cased header: cell})]` for the first table in a section body.

    An empty list means "the section exists and declares no row" — a different fact from "the
    section is missing", and the runtime-row class judges the two differently on purpose.
    """
    header = None
    rows = []
    for number, line in body:
        stripped = line.strip()
        if not stripped.startswith("|"):
            if header is not None and rows:
                break
            continue
        if header is None:
            header = [clean_cell(cell).lower() for cell in line_cells(stripped)]
            continue
        if TABLE_SEPARATOR.match(stripped):
            continue
        cells = line_cells(stripped)
        if len(cells) < len(header):
            cells += [""] * (len(header) - len(cells))
        rows.append((number, dict(zip(header, cells))))
    return rows


def column(row, *names):
    """The first present column among `names` (header wording varies across templates)."""
    for name in names:
        if name in row:
            return row[name]
    return ""


def flow_class_of(text):
    """The declared class, defaulting to the strict side (`execution`)."""
    match = FLOW_CLASS.search(text)
    if not match:
        return "execution"
    value = match.group(1).strip()
    if value not in FLOW_CLASSES:
        raise InputError(
            "`**Flow Class**: %s` is outside the closed set %s"
            % (value, " / ".join(FLOW_CLASSES))
        )
    return value


def task_row_quotes(tasks_text, fr_id):
    """Whether at least one **task row** quotes `fr_id`, by the live-level match of FR-009.

    The match is anchored at the start of the line and requires the row sigil and the task id, so
    an FR named in a table cell or in prose is not a task row. A whole-file substring test would
    answer the wrong question and pass on fixtures written only to be caught.
    """
    pattern = re.compile(TASK_QUOTES_FR % re.escape(fr_id))
    return any(pattern.match(line) for line in tasks_text.splitlines())


# --- § Execution Premises ---------------------------------------------------------------------

def check_premises(plan_text, flow_class, findings):
    """`{EP-NNN: {"line", "status", "decision"}}`; emits the undecided-falsification finding.

    Absent for an `expression`-class feature, an input error for an `execution`-class one: an
    incomplete plan is a defect of the artifact, never a verdict about the feature.
    """
    rel = "plan.md"
    try:
        body = section_lines(plan_text, PREMISES_SECTION, "Execution Premises", rel)
    except InputError:
        if flow_class == "execution":
            raise
        return {}
    premises = {}
    for number, row in section_rows(body):
        ep_id = clean_cell(column(row, "id"))
        if not EP_ID.match(ep_id):
            raise InputError("%s:%d § Execution Premises row carries no `EP-NNN` id" % (rel, number))
        status = clean_cell(column(row, "status"))
        if status not in PREMISE_STATUSES:
            raise InputError(
                "%s:%d § Execution Premises row %s declares `Status: %s`; the closed set is %s"
                % (rel, number, ep_id, status or "<empty>", " / ".join(PREMISE_STATUSES))
            )
        decision = column(row, "decision")
        premises[ep_id] = {"line": number, "status": status, "decision": decision}
        if status == "falsified" and blank_cell(decision):
            add(findings, CHECK_PREMISE, "error", rel, number,
                "premise %s is `falsified` and its `Decision` cell is empty — a known-bad fact "
                "nobody decided about; reason: %s: %s" % (ep_id, REASON_PREMISE, ep_id))
    return premises


# --- § Runtime Stack & Dependency Ownership ---------------------------------------------------

def check_runtime(requirements_text, fr, plan_text, premises, tasks_text, repo, findings):
    """The runtime-row class: findings 1 and 2, the prose rule, and duty ①/②.

    Three shapes, three verdicts, and silence is never one of them: an absent section is an input
    error, a section with **zero data rows** blocks under the reserved argument, and a row whose
    required cell is empty blocks under its own id. Cell-shape defects (a `Form` outside the
    domain, an unresolvable `FR` / `Premises` / `Contract`) exit 2 — a cell that cannot be parsed
    is a fact about the artifact, not about the feature.
    """
    rel = "requirements.md"
    flow_class = flow_class_of(requirements_text)
    allowed_forms = ("in-scope", "signed-contract", "user-waived")
    if flow_class == "expression":
        allowed_forms = allowed_forms + ("not-required",)

    body = None
    try:
        body = section_lines(requirements_text, RUNTIME_SECTION,
                             "Runtime Stack & Dependency Ownership", rel)
    except InputError:
        # The table is mandatory in `requirements.md` of an `execution`-class feature and exempt
        # for an `expression`-class one, whose whole deliverable may consume no runtime
        # capability. A class read from the declaration keeps the exemption mechanical.
        if flow_class == "execution":
            raise
    if body is None:
        return
    rows = section_rows(body)
    if not rows:
        add(findings, CHECK_RUNTIME_ROW, "error", rel, body[0][0] if body else 1,
            "§ Runtime Stack & Dependency Ownership carries zero data rows — the most complete "
            "form of 'no table row', never a silent pass; reason: %s: %s"
            % (REASON_RUNTIME, RESERVED_RUNTIME_ARGUMENT))

    for number, row in rows:
        rs_id = clean_cell(column(row, "id"))
        if not RS_ID.match(rs_id):
            raise InputError(
                "%s:%d § Runtime Stack row carries no `RS-NNN` id" % (rel, number))
        form = clean_cell(column(row, "form"))
        if form and form not in allowed_forms:
            raise InputError(
                "%s:%d § Runtime Stack row %s declares `Form: %s`, outside the closed set %s"
                % (rel, number, rs_id, form, " / ".join(allowed_forms)))

        problems = []
        if not form:
            problems.append("its `Form` cell is empty")
        if not clean_cell(column(row, "capability")):
            problems.append("its `Capability` cell is empty")
        if form == "not-required":
            if problems:
                add(findings, CHECK_RUNTIME_ROW, "error", rel, number,
                    "§ Runtime Stack row %s %s; reason: %s: %s"
                    % (rs_id, "; ".join(problems), REASON_RUNTIME, rs_id))
            continue

        cited = FR_ID.findall(clean_cell(column(row, "fr")))
        if form == "in-scope":
            if not cited:
                raise InputError(
                    "%s:%d § Runtime Stack row %s declares `Form: in-scope` with an empty `FR` "
                    "cell — a defective cell, never a `block` about the feature (duty ①)"
                    % (rel, number, rs_id))
            unresolved = [fr_id for fr_id in cited if fr_id not in fr]
            if unresolved:
                raise InputError(
                    "%s:%d § Runtime Stack row %s cites %s, which this specification does not "
                    "define — a defective cell, never a `block` (duty ①)"
                    % (rel, number, rs_id, ", ".join(sorted(unresolved))))

        if cited:
            premises_cell = column(row, "premises")
            if blank_cell(premises_cell):
                problems.append(
                    "it names %s but its `Premises` cell is empty — every FR that consumes a "
                    "runtime capability cites a premise" % ", ".join(cited))
            elif plan_text is not None:
                for ep_id in EP_ID.findall(clean_cell(premises_cell)):
                    if ep_id not in premises:
                        raise InputError(
                            "%s:%d § Runtime Stack row %s cites %s, which § Execution Premises "
                            "does not define — a defective cell"
                            % (rel, number, rs_id, ep_id))

        if form == "in-scope":
            if blank_cell(column(row, "joint acceptance", "joint_acceptance")):
                problems.append("its `Joint acceptance` cell is empty")
            if tasks_text is not None:
                missing = [fr_id for fr_id in cited if not task_row_quotes(tasks_text, fr_id)]
                if missing:
                    problems.append(
                        "no tasks.md task row quotes %s at line level — an FR named in a table "
                        "cell or in prose is not a task row" % ", ".join(missing))
        elif form == "signed-contract":
            contract = clean_cell(column(row, "contract"))
            if blank_cell(column(row, "pin")):
                problems.append("it is `signed-contract` with an empty `Pin` cell")
            if not contract:
                problems.append("it is `signed-contract` with an empty `Contract` cell")
            if blank_cell(column(row, "joint acceptance", "joint_acceptance")):
                problems.append("it is `signed-contract` with an empty `Joint acceptance` cell")
            if blank_cell(column(row, "owner")):
                problems.append("it is `signed-contract` with no external `Owner`")
            if contract and repo and not os.path.exists(os.path.join(repo, contract)):
                raise InputError(
                    "%s:%d § Runtime Stack row %s names a `Contract` path that does not resolve "
                    "under the repo: %s" % (rel, number, rs_id, contract))
        elif form == "user-waived":
            if blank_cell(column(row, "owner")):
                problems.append("it is `user-waived` and cites no user ruling")
            if blank_cell(column(row, "joint acceptance", "joint_acceptance")):
                problems.append("it is `user-waived` with an empty residual-risk cell")

        if problems:
            check = CHECK_RUNTIME_CONTRACT if form == "signed-contract" else CHECK_RUNTIME_ROW
            add(findings, check, "error", rel, number,
                "§ Runtime Stack row %s: %s; reason: %s: %s"
                % (rs_id, "; ".join(problems), REASON_RUNTIME, rs_id))

    check_prose_declarations(body, rel, findings)


def check_prose_declarations(body, rel, findings):
    """The prose-declaration rule: marker is the rule, code blocks removed first (C-18).

    A marked line carrying an `RS-NNN` is a capability declared with no table row; a marked line
    carrying none can produce no valid instance, so it is an input error naming that line — never
    a silent pass and never an eighth reason. An unmarked narrative line is not a declaration.
    """
    in_fence = False
    for number, line in body:
        stripped = line.strip()
        if FENCE.match(line):
            in_fence = not in_fence
            continue
        if in_fence or HEADING.match(line):
            continue
        if not PROSE_DECLARATION.match(stripped):
            continue
        declared = re.findall(r"\bRS-\d{3}\b", stripped)
        if not declared:
            raise InputError(
                "%s:%d is a prose runtime declaration carrying no `RS-NNN` id: the reason's "
                "argument grammar admits only an id, so this line is an input error rather than "
                "a silent pass" % (rel, number))
        for rs_id in declared:
            add(findings, CHECK_RUNTIME_ROW, "error", rel, number,
                "capability %s is declared only in prose, with no runtime-stack row; "
                "reason: %s: %s" % (rs_id, REASON_RUNTIME, rs_id))


# --- § Inherited Blockers ---------------------------------------------------------------------

def declared_dependency_files(section_text, spec_dir):
    """The dependency artifacts the plan's declaration names, resolved and deduplicated.

    The set is declared, never implied: only a backticked `.md` token inside the section is read,
    so an unopened dependency is visible as a missing row rather than silently assumed away.
    """
    found = []
    for token in BACKTICK.findall(section_text):
        token = token.strip()
        if not token.endswith(".md"):
            continue
        candidate = os.path.normpath(os.path.join(spec_dir, token))
        if os.path.isfile(candidate) and candidate not in found:
            found.append(candidate)
    return found


def deferred_locators(text, feature_id):
    """One locator per non-empty `## Deferred` list item (`deferred:<slug>`, else `row-<n>`)."""
    try:
        body = section_lines(text, DEFERRED_SECTION, "Deferred", "the dependency detail")
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


def verification_locators(text, feature_id):
    """`blocked` / `deferred` / **`partial`** status rows, plus a non-empty `deferred_tasks=`.

    `partial` is inside the set on purpose: a dependency may carry `partial` rows and nothing
    else, and an extraction set that excluded it would be disjoint from the disposition set — the
    finding would then never fire.
    """
    locators = []
    for line in text.splitlines():
        stripped = line.strip()
        status = re.match(r"^(SC-\d{3})_status=(.*)$", stripped)
        if status:
            if status.group(2).strip() in ("blocked", "deferred", "partial"):
                locators.append("%s:%s_status" % (feature_id, status.group(1)))
            continue
        deferred = re.match(r"^deferred_tasks=(.*)$", stripped)
        if deferred and deferred.group(1).strip():
            locators.append("%s:deferred_tasks" % feature_id)
    return locators


def extracted_dependency_rows(section_text, spec_dir):
    """Every row the closed three-source set yields, in declaration order."""
    details = []
    verifications = []
    for path in declared_dependency_files(section_text, spec_dir):
        text = read_file(path)
        if VERIFICATION_FIELD.search(text):
            verifications.append(text)
        else:
            details.append(text)
    feature_ids = []
    for text in details:
        match = FEATURE_ID.search(text)
        feature_ids.append(match.group(1) if match else None)
    default_id = next((fid for fid in feature_ids if fid), None)

    locators = []
    for text, feature_id in zip(details, feature_ids):
        if feature_id:
            locators.extend(deferred_locators(text, feature_id))
    for text in verifications:
        first = next((line for line in text.splitlines() if line.strip()), "")
        match = re.search(r"\b(\d{3})\b", first)
        feature_id = match.group(1) if match else default_id
        if feature_id:
            locators.extend(verification_locators(text, feature_id))
    return locators


def parse_carrier(raw):
    """`("task", T-ID, path)` / `("gate", GATE-ID)` / `("test", path)` / `None`.

    The `test:<path>` form alone is the **`inherited-later`** shape, never a carrier that can
    resolve in this slice; `SC-NNN` is not a carrier at all, because a criterion that may be
    deferred cannot carry a measurement.
    """
    match = CARRIER_TASK.match(raw)
    if match:
        return ("task", match.group(1), match.group(2))
    match = CARRIER_GATE.match(raw)
    if match:
        return ("gate", match.group(1))
    match = CARRIER_TEST_ONLY.match(raw)
    if match:
        return ("test", match.group(1))
    return None


def carrier_resolves(parsed, tasks_text):
    """`(ok, reason)` for a parsed carrier. A carrier the stage cannot read never fails."""
    if tasks_text is None:
        return True, ""
    kind = parsed[0]
    if kind == "task":
        task_id, test_path = parsed[1], parsed[2]
        rows = {}
        for line in tasks_text.splitlines():
            match = TASK_DEF.match(line)
            if match:
                rows[match.group(1)] = line
        if task_id not in rows:
            return False, "task %s is not a mandatory row of this slice's tasks.md" % task_id
        if test_path not in rows[task_id]:
            return False, (
                "the test path %s does not appear verbatim in %s's description — the two-part "
                "carrier is conjunctive" % (test_path, task_id))
        return True, ""
    if kind == "gate":
        if not any(match.group(1) == parsed[1] for match in GATE_ROW.finditer(tasks_text)):
            return False, "gate %s is not one of this slice's completion gates" % parsed[1]
        return True, ""
    return False, (
        "a `test:<path>` carrier is the `inherited-later` form alone; it carries no measurement "
        "in this slice")


def later_slice_is_legal(slice_value, plan_text, spec_dir):
    """A later `Carrier slice` is legal only while the parent is `Blocked` and D10 lists it."""
    detail = os.path.join(spec_dir, "feature-detail.md")
    if not os.path.isfile(detail):
        return False
    match = DETAIL_STATUS.search(read_file(detail))
    if not match or match.group(1).strip() != "Blocked":
        return False
    try:
        body = section_lines(plan_text, D10_SECTION, "D10", "plan.md")
    except InputError:
        return False
    section_text = "\n".join(line for _, line in body)
    return bool(re.search(r"(?<!\w)%s(?!\w)" % re.escape(slice_value), section_text))


def check_inherited(plan_text, requirements_text, tasks_text, spec_dir, findings):
    """Finding 4: an undisposed row, and the `inherited` row whose carrier cannot carry.

    One reason for five ways to fail — undisposed, blank carrier, unparseable carrier,
    unresolvable carrier, deferrable-`supporting`-SC carrier — so the closed set does not grow.
    A later-slice carrier is not one of them: it reads `inherited-later`, disclosed and
    non-blocking, and it is judged by `Carrier slice` plus the parent's claimed status.
    """
    rel = "plan.md"
    flow_class = flow_class_of(requirements_text)
    try:
        body = section_lines(plan_text, INHERITED_SECTION, "Inherited Blockers", rel)
    except InputError:
        if flow_class == "execution":
            raise
        return
    anchor = body[0][0] if body else 1
    section_text = "\n".join(line for _, line in body)
    extracted = extracted_dependency_rows(section_text, spec_dir)

    entries = []
    seen = {}
    for index, (number, row) in enumerate(section_rows(body), start=1):
        label = clean_cell(column(row, "#", "id")) or "row-%d" % index
        source = clean_cell(column(row, "source row", "source"))
        if source and not SOURCE_LOCATOR.match(source):
            if source.lower() not in ABSENT_LOCATORS:
                raise InputError(
                    "%s:%d `Source row` %r is not a `<feature>:<row>` locator — the join key has "
                    "one grammar" % (rel, number, source))
            source = ""
        if source:
            if source in seen:
                raise InputError(
                    "%s:%d disposes %s a second time — the join key must be unique (first "
                    "disposition at line %d)" % (rel, number, source, seen[source]))
            seen[source] = number
        slice_raw = column(row, "carrier slice")
        slice_value = "" if blank_cell(slice_raw) else clean_cell(slice_raw)
        if slice_value and slice_value != "this-slice" and not LATER_SLICE.match(slice_value):
            raise InputError(
                "%s:%d `Carrier slice` %r is neither `this-slice` nor a slice id"
                % (rel, number, slice_value))
        entries.append({
            "line": number,
            "label": label,
            "source": source,
            "disposition": clean_cell(column(row, "disposition")),
            "carrier": clean_cell(column(row, "carrier")),
            "slice": slice_value or "this-slice",
        })

    for entry in entries:
        problems = []
        disposition = entry["disposition"]
        carrier = entry["carrier"]
        if disposition not in DISPOSITIONS:
            problems.append(
                "its `Disposition` cell %r is outside the closed set %s"
                % (disposition or "<empty>", " / ".join(DISPOSITIONS)))
        elif disposition == "inherited":
            parsed = parse_carrier(carrier) if carrier else None
            if not carrier:
                problems.append("its `Carrier` cell is empty")
            elif parsed is None:
                problems.append(
                    "its `Carrier` %r parses as neither `task:<T-ID>+test:<path>` nor "
                    "`gate:<GATE-ID>` — a deferrable `supporting`-path SC is not a carrier"
                    % carrier)
            elif LATER_SLICE.match(entry["slice"]) and later_slice_is_legal(
                    entry["slice"], plan_text, spec_dir):
                if parsed[0] != "test":
                    problems.append(
                        "an `inherited-later` row's `Carrier` is `test:<path>` alone, not %r — "
                        "the task id of an unwritten tasks.md MUST NOT be fabricated" % carrier)
            else:
                ok, why = carrier_resolves(parsed, tasks_text)
                if not ok:
                    problems.append(why)
        if problems:
            target = entry["source"] or "%s:%s" % (
                os.path.basename(spec_dir.rstrip(os.sep)), entry["label"])
            add(findings, CHECK_INHERITED, "error", rel, entry["line"],
                "§ Inherited Blockers row %s: %s; reason: %s: %s"
                % (entry["label"], "; ".join(problems), REASON_INHERITED, target))

    for locator in extracted:
        if locator in seen:
            continue
        add(findings, CHECK_INHERITED, "error", rel, anchor,
            "extracted dependency record %s has no disposition row of its own — extraction "
            "discovers rows, it does not judge the row set it was handed; "
            "reason: %s: %s" % (locator, REASON_INHERITED, locator))


def check_ownership(spec_dir, stage, requirements_text, fr, findings,
                    plan_text=None, tasks_text=None, repo="", carrier_tasks_text=None):
    """Gate every finding to the artifact it needs, so no stage reports what it cannot see.

    `requirements` judges findings 1–2 and duty ①'s input-error class; `plan` re-reads findings
    1–2 with the premises table in hand and adds findings 3–4; `tasks` adds duty ②'s line-level
    row match, the only stage at which `tasks.md` is an input. Duty ③ (the joint-acceptance row
    in `verification.md`) belongs to the closure verdict and is deliberately absent here.

    `tasks_text` and `carrier_tasks_text` differ on purpose: duty ② is *owed* only at the tasks
    stage, while a `Carrier` naming a task row can be resolved whenever the file exists. Reading
    it earlier resolves a carrier instead of inventing an obligation.
    """
    premises = check_premises(plan_text, flow_class_of(requirements_text), findings) \
        if plan_text is not None else {}
    check_runtime(requirements_text, fr, plan_text, premises, tasks_text, repo, findings)
    if plan_text is not None:
        check_inherited(plan_text, requirements_text, carrier_tasks_text, spec_dir, findings)


def apply_waivers(findings, waivers):
    waived = 0
    for finding in findings:
        key = "%s:%s:%d" % (finding["check"], finding["path"], finding["line"])
        if key in waivers:
            finding["waived"] = True
            waived += 1
    return waived


def run(args):
    spec_dir = os.path.abspath(args.spec_dir)
    if not os.path.isdir(spec_dir):
        raise InputError("spec dir not found: %s" % spec_dir)
    stage_inputs = STAGES[args.stage]
    for name in stage_inputs:
        if not os.path.isfile(os.path.join(spec_dir, name)):
            raise InputError("%s stage requires %s" % (args.stage, name))
    repo = os.path.abspath(args.repo) if args.repo else ""

    files = formal_files(spec_dir)
    fr, sc, tasks, clauses, duplicates = definitions(files, spec_dir)
    findings = []
    for path, number, key, first in duplicates:
        add(findings, "duplicate-id", "error", os.path.relpath(path, spec_dir),
            number, "duplicates %s first defined at %s:%d"
            % (key, os.path.relpath(first[0], spec_dir), first[1]))
    check_references(files, fr, sc, clauses, findings, spec_dir)
    check_blocked_by(spec_dir, tasks, findings)
    check_counts(files, fr, sc, tasks, findings, spec_dir)
    check_paths(files, findings, spec_dir, repo)

    # The ownership checks read `plan.md` and `tasks.md` as *stage inputs*, not as formal files:
    # `verification.md` and the dependency artifacts are read directly and never join the
    # live-line scans above, whose scope stays exactly what it was.
    requirements_text = read_file(os.path.join(spec_dir, "requirements.md"))
    plan_text = read_file(os.path.join(spec_dir, "plan.md")) if "plan.md" in stage_inputs else None
    duty_tasks = read_file(os.path.join(spec_dir, "tasks.md")) \
        if "tasks.md" in stage_inputs else None
    # Carrier resolution is a different question from duty ②: a `Carrier` naming a task row can
    # be resolved whenever `tasks.md` exists, while duty ② is only *owed* at the tasks stage.
    carrier_tasks = duty_tasks
    carrier_path = os.path.join(spec_dir, "tasks.md")
    if carrier_tasks is None and os.path.isfile(carrier_path):
        carrier_tasks = read_file(carrier_path)
    check_ownership(
        spec_dir, args.stage, requirements_text, set(fr), findings,
        plan_text=plan_text,
        tasks_text=duty_tasks,
        repo=repo,
        carrier_tasks_text=carrier_tasks,
    )

    waivers = set(args.waive or [])
    waived = apply_waivers(findings, waivers)
    blocking = [f for f in findings
                if not f.get("waived")
                and (f["severity"] == "error"
                     or (args.strict and f["severity"] == "advisory"))]
    errors = sum(1 for f in blocking if f["severity"] == "error")
    advisories = sum(1 for f in findings
                     if f["severity"] == "advisory" and not f.get("waived"))
    record = {
        "stage": args.stage,
        "decision": "fail" if blocking else "pass",
        "findings": findings,
        "summary": {
            "errors": errors,
            "advisories": advisories,
            "waived": waived,
            "fr": len(fr), "sc": len(sc), "tasks": len(tasks),
            "clauses": len(clauses), "files": len(files),
        },
        "checked_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    return record


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Deterministic cross-artifact gate before analyze.")
    parser.add_argument("--spec-dir", required=True)
    parser.add_argument("--stage", choices=tuple(STAGES), default="tasks")
    parser.add_argument("--repo", default="",
                        help="repo root for declared-path existence checks")
    parser.add_argument("--strict", action="store_true",
                        help="treat missing-path advisories as blocking")
    parser.add_argument("--waive", action="append", default=[],
                        metavar="CHECK:REL_PATH:LINE")
    parser.add_argument("--json-out", default="")
    args = parser.parse_args(argv)

    try:
        record = run(args)
    except InputError as exc:
        print("pre-analyze-check: input error: %s" % exc, file=sys.stderr)
        return 2

    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as handle:
            json.dump(record, handle, indent=2, ensure_ascii=False)
            handle.write("\n")
    print(json.dumps(record, ensure_ascii=False))
    summary = record["summary"]
    print("pre-analyze-check: stage=%s decision=%s errors=%d advisories=%d waived=%d"
          % (record["stage"], record["decision"], summary["errors"],
             summary["advisories"], summary["waived"]), file=sys.stderr)
    return 0 if record["decision"] == "pass" else 1


if __name__ == "__main__":
    sys.exit(main())
