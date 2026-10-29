#!/usr/bin/env python3
"""validate-decision-tensions.py — deterministic structural checker for Decision Tension Records.

Program-First discipline (shared/guidelines/token-efficiency.md): the propositions checked here
are fixed, textual and decidable, so a program judges them and prints a verdict; an agent MUST
NOT re-derive them by reading the plan and declaring a result. The record shape, the admissibility
criteria, the rejection forms and the load-bearing threshold are owned by
``shared/guidelines/decision-tension.md`` — this checker consumes them, it never restates them.

Checks (the closed six-label set; a record with one label yields at most one finding, and the
cross-label precedence is load-bearing):
  dtr-anchor                     the ``^## `` heading sequence contains the three consecutive
                                 entries ``## Constitution Check`` -> ``## Decision Tensions`` ->
                                 ``## Project Structure``
  dtr-section-missing            the plan carries no ``## Decision Tensions`` section; when it is
                                 missing, ``dtr-anchor`` is suppressed (the adjacency assertion
                                 necessarily reds, and one root cause is counted once)
  dtr-record-incomplete          a record does not carry each of the six field labels exactly
                                 once, or one of ``decision`` / ``antithesis`` /
                                 ``discriminating_evidence`` / ``revision_trigger`` is blank.
                                 A missing field label also suppresses ``expected-sacrifice-unmapped``
  dtr-tension-id                 every record heading begins with ``T-NNN`` (three digits), the
                                 identifiers are unique and increasing in document order
  dtr-rejected-form              the record hits the owner's closed rejection list (the literal
                                 ``expected_sacrifice: none`` or a blank sacrifice, an empty pole,
                                 the undecidable-wording list)
  expected-sacrifice-unmapped    ``expected_sacrifice`` does not resolve to a ``**SC-NNN Source**``
                                 entry of the same feature's ``requirements.md``

Scope of this file in the current implementation stage: the anchor, section, field-presence and
identifier checks are live; ``dtr-rejected-form`` and ``expected-sacrifice-unmapped`` are declared
in the label set and are wired by the immediately following task (T008) — until then they report
``pass (0)``. Their inverse samples already exist and are RED in
``tests/contract/test_decision_tension_validator.py``, so the gap cannot be mistaken for a green.

Exit codes: 0 = no error (warnings allowed) / 1 = at least one error / 2 = input unreadable
(either file missing, undecodable, or without content lines). Read-only: no write point of any
kind, no resident process, standard library only.

Usage: python3 validate-decision-tensions.py --spec <spec-dir> [--json]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

EXIT_OK = 0
EXIT_ERROR = 1
EXIT_INPUT = 2

STATUS_OK = "ok"
STATUS_ERROR = "error"
STATUS_UNREADABLE = "unreadable"

LABELS = (
    "dtr-anchor",
    "dtr-section-missing",
    "dtr-record-incomplete",
    "dtr-tension-id",
    "dtr-rejected-form",
    "expected-sacrifice-unmapped",
)

SECTION_HEADING = "## Decision Tensions"
ANCHOR_BEFORE = "## Constitution Check"
ANCHOR_AFTER = "## Project Structure"

# The six field labels, verbatim; the field set is closed by the owner (FR-002).
FIELD_NAMES = (
    "decision",
    "antithesis",
    "binding_constraints",
    "discriminating_evidence",
    "expected_sacrifice",
    "revision_trigger",
)
# The four fields whose blank value is a record-level incompleteness; ``expected_sacrifice`` and
# the two poles are judged as rejected forms (one root cause, one label).
VALUE_CHECKED_FIELDS = (
    "decision",
    "antithesis",
    "discriminating_evidence",
    "revision_trigger",
)

H2_RE = re.compile(r"^##\s")
H3_RE = re.compile(r"^###\s")
RECORD_HEADING_RE = re.compile(r"^###\s+(.*)$")
TENSION_ID_RE = re.compile(r"^T-\d{3}(?:\s|$)")
FIELD_RE = re.compile(r"^- \*\*([a-z_]+)\*\*:\s*(.*)$")


class Finding:
    __slots__ = ("line", "label", "text", "severity")

    def __init__(self, line, label, text, severity="error"):
        self.line = line
        self.label = label
        self.text = text
        self.severity = severity

    def render(self):
        return "%d: %s: %s" % (self.line, self.label, self.text)


class Record:
    """One ``### T-NNN`` sub-section: heading, absolute line number, field values."""

    __slots__ = ("tension_id", "line", "heading", "body", "fields")

    def __init__(self, heading, line):
        self.heading = heading
        self.line = line
        self.body = []
        token = heading.split()[0] if heading.split() else ""
        self.tension_id = token if TENSION_ID_RE.match(token) else None
        self.fields = {}

    def finalize(self):
        """Parse the field labels once the body is complete (bodies are appended in a scan)."""
        self._parse_fields()

    def _parse_fields(self):
        current = None
        for raw in self.body:
            m = FIELD_RE.match(raw)
            if m:
                name = m.group(1)
                entry = self.fields.setdefault(
                    name, {"inline": "", "continuation": [], "count": 0}
                )
                entry["inline"] = m.group(2).strip()
                entry["count"] += 1
                current = name
                continue
            if not raw.strip():
                current = None
                continue
            if current is not None and (raw.startswith("  ") or raw.startswith("\t")):
                self.fields[current]["continuation"].append(raw.strip())
            else:
                current = None

    def value(self, name):
        entry = self.fields.get(name)
        if entry is None:
            return ""
        chunks = [entry["inline"]] + entry["continuation"]
        return " ".join(chunk for chunk in chunks if chunk).strip()

    def count(self, name):
        entry = self.fields.get(name)
        return 0 if entry is None else entry["count"]


def _visible_lines(text):
    """Lines with fenced code blocks blanked — the same rule the record grammar declares."""
    out = []
    in_fence = False
    for raw in text.splitlines():
        stripped = raw.strip()
        if stripped.startswith("```"):
            in_fence = not in_fence
            out.append("")
            continue
        out.append("" if in_fence else raw)
    return out


def _h2_entries(lines):
    return [(index, line.rstrip()) for index, line in enumerate(lines) if H2_RE.match(line.rstrip())]


def _section_bounds(lines, section_index):
    end = len(lines)
    for index, heading in _h2_entries(lines):
        if index > section_index:
            end = index
            break
    return section_index + 1, end


def _records(lines, start, end):
    records = []
    current = None
    for index in range(start, end):
        line = lines[index]
        if H3_RE.match(line):
            if current is not None:
                current.finalize()
                records.append(current)
            m = RECORD_HEADING_RE.match(line.rstrip())
            current = Record(m.group(1).strip() if m else "", index + 1)
            continue
        if current is not None:
            current.body.append(line)
    if current is not None:
        current.finalize()
        records.append(current)
    return records


def index_records(plan_text):
    """Map ``tension_id`` -> ``{"line", "fields"}`` for every record in a plan.

    One parser, two consumers (``contracts/adr-reference.md`` C-2): this checker's identifier
    check and the ADR dangling-``tension_id`` contract test both call this function. A duplicate
    identifier keeps its first occurrence, so the index answers 'does this id resolve?' without
    hiding the duplicate (``dtr-tension-id`` reports it).
    """
    lines = _visible_lines(plan_text)
    section = None
    for index, heading in _h2_entries(lines):
        if heading == SECTION_HEADING:
            section = index
            break
    if section is None:
        return {}
    start, end = _section_bounds(lines, section)
    index = {}
    for record in _records(lines, start, end):
        if record.tension_id and record.tension_id not in index:
            index[record.tension_id] = {
                "line": record.line,
                "fields": {name: record.value(name) for name in record.fields},
            }
    return index


def _unreadable(spec, reason):
    return {
        "spec": str(spec),
        "status": STATUS_UNREADABLE,
        "checks": [{"label": label, "status": "pass", "count": 0} for label in LABELS],
        "findings": [],
        "reason": reason,
        "scanned": {"lines": 0, "records": 0},
    }


def validate(spec):
    """Judge one spec directory and return ``{spec,status,checks,findings,scanned[,reason]}``."""
    spec_path = Path(spec)
    plan_path = spec_path / "plan.md"
    requirements_path = spec_path / "requirements.md"

    texts = {}
    for path in (plan_path, requirements_path):
        if not path.is_file():
            return _unreadable(spec_path, "%s is missing" % path.name)
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            return _unreadable(spec_path, "%s is not decodable text" % path.name)
        if not text.strip():
            return _unreadable(spec_path, "%s has no content lines" % path.name)
        texts[path.name] = text

    lines = _visible_lines(texts["plan.md"])
    entries = _h2_entries(lines)
    headings = [heading for _, heading in entries]
    section_index = None
    for index, heading in entries:
        if heading == SECTION_HEADING:
            section_index = index
            break

    buckets = {label: [] for label in LABELS}

    if section_index is None:
        buckets["dtr-section-missing"].append(Finding(
            1, "dtr-section-missing",
            "plan carries no `%s` section" % SECTION_HEADING,
        ))
        records = []
    else:
        anchor_ok = False
        if ANCHOR_BEFORE in headings:
            at = headings.index(ANCHOR_BEFORE)
            anchor_ok = (
                len(headings) > at + 2
                and headings[at + 1] == SECTION_HEADING
                and headings[at + 2] == ANCHOR_AFTER
            )
        if not anchor_ok:
            buckets["dtr-anchor"].append(Finding(
                1, "dtr-anchor",
                "`%s` is not the direct successor of `%s` followed by `%s`"
                % (SECTION_HEADING, ANCHOR_BEFORE, ANCHOR_AFTER),
            ))
        start, end = _section_bounds(lines, section_index)
        records = _records(lines, start, end)

    for position, record in enumerate(records, start=1):
        expected_id = "T-%03d" % position
        if record.tension_id is None:
            buckets["dtr-tension-id"].append(Finding(
                record.line, "dtr-tension-id",
                "record heading does not begin with a `T-NNN` identifier: %r" % record.heading,
            ))
        elif record.tension_id != expected_id:
            buckets["dtr-tension-id"].append(Finding(
                record.line, "dtr-tension-id",
                "expected %s in document order, found %s" % (expected_id, record.tension_id),
            ))

        missing = [name for name in FIELD_NAMES if record.count(name) == 0]
        duplicated = [name for name in FIELD_NAMES if record.count(name) > 1]
        blank = [
            name for name in VALUE_CHECKED_FIELDS
            if record.count(name) == 1 and not record.value(name)
        ]
        if missing or duplicated or blank:
            parts = []
            if missing:
                parts.append("missing field label(s): %s" % ", ".join(missing))
            if duplicated:
                parts.append("duplicated field label(s): %s" % ", ".join(duplicated))
            if blank:
                parts.append("blank value(s): %s" % ", ".join(blank))
            buckets["dtr-record-incomplete"].append(Finding(
                record.line, "dtr-record-incomplete", "; ".join(parts),
            ))

    # ``dtr-rejected-form`` and ``expected-sacrifice-unmapped`` are declared in the closed set
    # here and wired by T008 (see the module docstring); their inverse samples are red until then.

    findings = [finding for label in LABELS for finding in buckets[label]]
    checks = [
        {"label": label, "status": "fail" if buckets[label] else "pass",
         "count": len(buckets[label])}
        for label in LABELS
    ]
    status = STATUS_ERROR if any(f.severity == "error" for f in findings) else STATUS_OK
    return {
        "spec": str(spec_path),
        "status": status,
        "checks": checks,
        "findings": findings,
        "scanned": {"lines": len(lines), "records": len(records)},
    }


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="validate-decision-tensions.py",
        description="Judge the structural propositions of a plan's Decision Tension Records.",
    )
    parser.add_argument("--spec", required=True,
                        help="the spec directory holding plan.md and requirements.md")
    parser.add_argument("--json", action="store_true", help="machine-readable output")
    args = parser.parse_args(argv if argv is not None else sys.argv[1:])

    result = validate(args.spec)
    findings = result["findings"]
    errors = sum(1 for f in findings if f.severity == "error")
    warnings = sum(1 for f in findings if f.severity == "warning")

    if args.json:
        print(json.dumps({
            "spec": result["spec"],
            "status": result["status"],
            "checks": result["checks"],
            "errors": errors,
            "warnings": warnings,
            "scanned": result["scanned"],
        }, ensure_ascii=False, indent=2))
    else:
        print("spec: %s" % result["spec"])
        print("status: %s" % result["status"])
        for check in result["checks"]:
            print("  [%s] %s (%d)" % (check["label"], check["status"], check["count"]))
        print("scanned: %d lines, %d record(s)"
              % (result["scanned"]["lines"], result["scanned"]["records"]))
        if result.get("reason"):
            print("unreadable: %s" % result["reason"])
        for finding in findings:
            print(finding.render())
        print("%d error(s), %d warning(s)" % (errors, warnings))

    if result["status"] == STATUS_UNREADABLE:
        return EXIT_INPUT
    return EXIT_ERROR if errors else EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
