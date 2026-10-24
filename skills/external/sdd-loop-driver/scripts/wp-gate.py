#!/usr/bin/env python3
"""wp-gate.py — deterministic Work Package decomposition gate.

Reads a Work Package plan from a line state spine (or from ``--plan-json`` for
fixture use), validates it, and emits the WG-04 JSON verdict. It never
dispatches, never writes the spine, and never modifies the plan. The only file
it writes is the optional ``--json-out`` evidence record.

The plan and its amendments are fences in the existing line state spine:

    <!-- wp-plan:begin stage=<stage> stage_attempt=<n> -->
    <!-- wp-plan-amendment:begin stage=<stage> stage_attempt=<n> seq=<n> -->
    <!-- wp-ledger:begin --> ... <!-- wp-ledger:end -->

Exit codes:
  0 = admit or single-package
  1 = reject (plan-level findings)
  2 = input, parse, or I/O error, or a check the gate cannot evaluate
      (the driver treats exit 2 as decomposition-unavailable, never as a
      plan rejection)

Standard library only, Python >= 3.8.
"""

import argparse
import copy
import hashlib
import json
import os
import re
import sys
import time

SCHEMA_VERSION = 1
STAGES = ("plan", "implement", "review", "analyze", "clarify")
DECISIONS = ("decomposed", "single-package", "disabled", "fallback")
GATE_VERDICTS = ("admit", "single-package", "no-gate-run")
RULES = (
    "decompose-plan-v1",
    "decompose-implement-v1",
    "decompose-review-v1",
    "decompose-investigation-v1",
)
PATTERNS = ("parallel", "serial", "iteration")
KINDS = ("read-only", "write")
BOUNDED_UNITS = ("tasks", "clauses", "artifacts", "acceptance")
CHECK_NAMES = ("plan", "preflight", "retry")
TIE_BREAK = "wp_id-lexicographic"
HASH_EXCLUDED_KEYS = ("plan_hash", "slot_cap_requested", "slot_cap_ceiling")

PLAN_BEGIN = re.compile(r"<!--\s*wp-plan:begin\s+(.*?)-->")
PLAN_END = re.compile(r"<!--\s*wp-plan:end\s*-->")
AMENDMENT_BEGIN = re.compile(r"<!--\s*wp-plan-amendment:begin\s+(.*?)-->")
AMENDMENT_END = re.compile(r"<!--\s*wp-plan-amendment:end\s*-->")
LEDGER_BEGIN = re.compile(r"<!--\s*wp-ledger:begin\s*-->")
LEDGER_END = re.compile(r"<!--\s*wp-ledger:end\s*-->")
ATTRIBUTE = re.compile(r"([A-Za-z_][A-Za-z0-9_]*)=([^\s]+)")
HEX_HASH = re.compile(r"^sha256:[0-9a-f]{64}$")


class InputError(Exception):
    """Unreadable, unparseable, or incomplete input (exit 2)."""


class CheckUnavailable(Exception):
    """The requested check has no implementation in this build (exit 2)."""


def _read_text(path):
    try:
        with open(path, "r", encoding="utf-8") as handle:
            return handle.read()
    except OSError as exc:
        raise InputError("cannot read %s: %s" % (path, exc))


def _read_json_object(path, label):
    text = _read_text(path)
    try:
        value = json.loads(text)
    except ValueError as exc:
        raise InputError("%s is not valid JSON: %s" % (label, exc))
    if not isinstance(value, dict):
        raise InputError("%s must be a JSON object" % label)
    return value


def _attributes(header):
    return dict(ATTRIBUTE.findall(header or ""))


def _fence_body(text, begin_match, end_pattern, label):
    end_match = end_pattern.search(text, begin_match.end())
    if end_match is None:
        raise InputError("unterminated %s fence" % label)
    return text[begin_match.end():end_match.start()]


def parse_plan_fences(spine_text):
    fences = []
    for match in PLAN_BEGIN.finditer(spine_text or ""):
        attributes = _attributes(match.group(1))
        try:
            stage = attributes["stage"]
            stage_attempt = int(attributes["stage_attempt"])
        except (KeyError, ValueError):
            raise InputError("malformed wp-plan fence header: %r" % match.group(1))
        body = _fence_body(spine_text, match, PLAN_END, "wp-plan")
        try:
            plan = json.loads(body)
        except ValueError as exc:
            raise InputError("wp-plan fence body is not valid JSON: %s" % exc)
        if not isinstance(plan, dict):
            raise InputError("wp-plan fence body must be a JSON object")
        fences.append(
            {"stage": stage, "stage_attempt": stage_attempt, "plan": plan}
        )
    return fences


def parse_amendment_fences(spine_text):
    fences = []
    for match in AMENDMENT_BEGIN.finditer(spine_text or ""):
        attributes = _attributes(match.group(1))
        try:
            stage = attributes["stage"]
            stage_attempt = int(attributes["stage_attempt"])
            seq = int(attributes["seq"])
        except (KeyError, ValueError):
            raise InputError(
                "malformed wp-plan-amendment fence header: %r" % match.group(1)
            )
        body = _fence_body(spine_text, match, AMENDMENT_END, "wp-plan-amendment")
        try:
            amendment = json.loads(body)
        except ValueError as exc:
            raise InputError(
                "wp-plan-amendment fence body is not valid JSON: %s" % exc
            )
        if not isinstance(amendment, dict):
            raise InputError("wp-plan-amendment fence body must be a JSON object")
        fences.append(
            {
                "stage": stage,
                "stage_attempt": stage_attempt,
                "seq": seq,
                "amendment": amendment,
            }
        )
    return fences


def parse_ledger(spine_text):
    events = []
    for match in LEDGER_BEGIN.finditer(spine_text or ""):
        body = _fence_body(spine_text, match, LEDGER_END, "wp-ledger")
        for line in body.splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                event = json.loads(line)
            except ValueError as exc:
                raise InputError("wp-ledger line is not valid JSON: %s" % exc)
            if not isinstance(event, dict):
                raise InputError("wp-ledger line must be a JSON object")
            events.append(event)
    return events


def read_spine(path):
    text = _read_text(path)
    return {
        "text": text,
        "plan_fences": parse_plan_fences(text),
        "amendments": parse_amendment_fences(text),
        "ledger": parse_ledger(text),
    }


def _attempt_value(event):
    value = event.get("stage_attempt")
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, str) and value.isdigit():
        return int(value)
    return None


def highest_stage_attempt(document):
    attempts = []
    for fence in document.get("plan_fences", []):
        attempts.append(fence["stage_attempt"])
    for fence in document.get("amendments", []):
        attempts.append(fence["stage_attempt"])
    for event in document.get("ledger", []):
        value = _attempt_value(event)
        if value is not None:
            attempts.append(value)
    return max(attempts) if attempts else 0


def effective_plan(plan, amendments):
    """Apply amendment bodies (raw dicts) in ``seq`` order.

    A package record whose ``wp_id`` exists replaces that record; a new
    ``wp_id`` is appended. The latest amendment's ``plan_hash`` becomes the
    effective recorded hash.
    """
    effective = copy.deepcopy(plan)
    for amendment in sorted(amendments, key=lambda body: body.get("seq", 0)):
        packages = effective.get("packages") or []
        by_id = {package.get("wp_id"): package for package in packages}
        for record in amendment.get("packages", []):
            wp_id = record.get("wp_id")
            copied = copy.deepcopy(record)
            if wp_id in by_id:
                index = next(
                    offset
                    for offset, package in enumerate(packages)
                    if package.get("wp_id") == wp_id
                )
                packages[index] = copied
            else:
                packages.append(copied)
            by_id[wp_id] = copied
        effective["packages"] = packages
        effective["plan_hash"] = amendment.get("plan_hash")
    return effective


def _is_timestamp_key(key):
    return key == "at" or key.endswith("_at")


def _strip_hash_exclusions(value):
    if isinstance(value, dict):
        return {
            key: _strip_hash_exclusions(item)
            for key, item in value.items()
            if key not in HASH_EXCLUDED_KEYS and not _is_timestamp_key(key)
        }
    if isinstance(value, list):
        return [_strip_hash_exclusions(item) for item in value]
    return value


def canonical_plan_hash(plan):
    body = _strip_hash_exclusions(plan)
    encoded = json.dumps(
        body, sort_keys=True, ensure_ascii=False, separators=(",", ":")
    ).encode("utf-8")
    return "sha256:" + hashlib.sha256(encoded).hexdigest()


def _is_text(value):
    return isinstance(value, str) and value.strip() != ""


def _is_int(value):
    return isinstance(value, int) and not isinstance(value, bool)


def _is_string_list(value):
    return isinstance(value, list) and all(_is_text(item) for item in value)


def _finding(code, wp_id=None, detail=""):
    return {"code": code, "wp_id": wp_id, "detail": detail}


def _sort_findings(findings):
    return sorted(
        findings, key=lambda item: (item["code"], item["wp_id"] or "", item["detail"])
    )


def _schema_check_package(package, plan_stage, index):
    findings = []
    label = "packages[%d]" % index
    if not isinstance(package, dict):
        return [_finding("schema-missing", None, "%s is not an object" % label)]
    wp_id = package.get("wp_id")
    if not _is_text(wp_id):
        findings.append(_finding("schema-missing", None, "%s.wp_id" % label))
        wp_id = None
    expected = (
        ("objective", _is_text),
        ("stage", lambda value: _is_text(value) and value == plan_stage),
        ("kind", lambda value: value in KINDS),
        ("source_refs", _is_string_list),
        ("inputs", lambda value: isinstance(value, list) and _is_string_list(value)),
        ("outputs", lambda value: _is_string_list(value) and bool(value)),
        ("owned_paths", lambda value: isinstance(value, list) and _is_string_list(value)),
        (
            "read_only_paths",
            lambda value: isinstance(value, list) and _is_string_list(value),
        ),
        ("depends_on", lambda value: isinstance(value, list) and _is_string_list(value)),
        ("parallel_safe", lambda value: isinstance(value, bool)),
        ("max_turns", lambda value: _is_int(value) and value > 0),
        ("bounded_by", lambda value: isinstance(value, dict)),
        ("acceptance", lambda value: isinstance(value, list) and bool(value)),
        ("sentinel", _is_text),
        ("evidence", _is_text),
        ("seat", lambda value: isinstance(value, dict)),
        ("resources", lambda value: isinstance(value, dict)),
    )
    for field, predicate in expected:
        if field not in package or not predicate(package[field]):
            findings.append(
                _finding("schema-missing", wp_id, "%s.%s" % (label, field))
            )
    if "intermediate_outputs" in package and not (
        isinstance(package["intermediate_outputs"], list)
        and _is_string_list(package["intermediate_outputs"])
    ):
        findings.append(
            _finding(
                "schema-missing", wp_id, "%s.intermediate_outputs" % label
            )
        )
    bounded = package.get("bounded_by")
    if isinstance(bounded, dict):
        if bounded.get("unit") not in BOUNDED_UNITS:
            findings.append(
                _finding("schema-missing", wp_id, "%s.bounded_by.unit" % label)
            )
        count = bounded.get("count")
        if not (_is_int(count) and count > 0):
            findings.append(
                _finding("schema-missing", wp_id, "%s.bounded_by.count" % label)
            )
    acceptance = package.get("acceptance")
    if isinstance(acceptance, list) and acceptance:
        seen = set()
        for offset, criterion in enumerate(acceptance):
            if not isinstance(criterion, dict):
                findings.append(
                    _finding(
                        "schema-missing",
                        wp_id,
                        "%s.acceptance[%d]" % (label, offset),
                    )
                )
                continue
            for key in ("id", "check", "evidence"):
                if not _is_text(criterion.get(key)):
                    findings.append(
                        _finding(
                            "schema-missing",
                            wp_id,
                            "%s.acceptance[%d].%s" % (label, offset, key),
                        )
                    )
            criterion_id = criterion.get("id")
            if _is_text(criterion_id):
                if criterion_id in seen:
                    findings.append(
                        _finding(
                            "schema-missing",
                            wp_id,
                            "%s.acceptance duplicate id %s" % (label, criterion_id),
                        )
                    )
                seen.add(criterion_id)
    seat = package.get("seat")
    if isinstance(seat, dict):
        for key in ("role", "stage", "type"):
            if not _is_text(seat.get(key)):
                findings.append(
                    _finding("schema-missing", wp_id, "%s.seat.%s" % (label, key))
                )
    resources = package.get("resources")
    if isinstance(resources, dict):
        for key in ("ports", "tmp_dir", "cache_dir"):
            value = resources.get(key)
            if not _is_text(value):
                findings.append(
                    _finding(
                        "schema-missing", wp_id, "%s.resources.%s" % (label, key)
                    )
                )
        shared = resources.get("shared_readonly")
        if not (isinstance(shared, list) and _is_string_list(shared)):
            findings.append(
                _finding(
                    "schema-missing",
                    wp_id,
                    "%s.resources.shared_readonly" % label,
                )
            )
    superseded = package.get("superseded_by")
    if superseded is not None and not _is_string_list(superseded):
        findings.append(
            _finding("schema-missing", wp_id, "%s.superseded_by" % label)
        )
    return findings


def validate_plan_schema(plan, stage, stage_attempt=None):
    """Required-field, type, and closed-enum checks (WG-06, V-PLAN.1/2)."""
    findings = []
    if not isinstance(plan, dict):
        return [_finding("schema-missing", None, "plan is not an object")]

    required = (
        ("schema_version", lambda value: value == SCHEMA_VERSION),
        ("line_id", _is_text),
        ("run_id", _is_text),
        ("stage", lambda value: value in STAGES),
        ("stage_attempt", lambda value: _is_int(value) and value >= 1),
        ("decision", lambda value: value in DECISIONS),
        ("gate_verdict", lambda value: value in GATE_VERDICTS),
        ("reason", _is_text),
        ("rule", lambda value: value is None or value in RULES),
        (
            "source_artifacts",
            lambda value: isinstance(value, list) and _is_string_list(value),
        ),
        ("required_outputs", lambda value: _is_string_list(value)),
        ("integrator_outputs", lambda value: isinstance(value, list) and _is_string_list(value)),
        ("pattern", lambda value: value in PATTERNS),
        ("tie_break", lambda value: value == TIE_BREAK),
        ("slot_cap", lambda value: _is_int(value) and value >= 1),
        ("packages", lambda value: isinstance(value, list) and bool(value)),
        ("plan_hash", lambda value: _is_text(value) and bool(HEX_HASH.match(value))),
    )
    for field, predicate in required:
        if field not in plan or not predicate(plan[field]):
            findings.append(_finding("schema-missing", None, "plan.%s" % field))

    if plan.get("stage") != stage:
        findings.append(
            _finding(
                "schema-missing",
                None,
                "plan.stage %r does not match --stage %r" % (plan.get("stage"), stage),
            )
        )
    if stage_attempt is not None and plan.get("stage_attempt") != stage_attempt:
        findings.append(
            _finding(
                "schema-missing",
                None,
                "plan.stage_attempt %r does not match the selected attempt %r"
                % (plan.get("stage_attempt"), stage_attempt),
            )
        )

    pattern = plan.get("pattern")
    repair_loop = plan.get("repair_loop")
    if pattern == "iteration":
        if not isinstance(repair_loop, dict):
            findings.append(
                _finding("schema-missing", None, "plan.repair_loop is required")
            )
        else:
            if not (_is_int(repair_loop.get("max_iterations")) and repair_loop["max_iterations"] > 0):
                findings.append(
                    _finding(
                        "schema-missing",
                        None,
                        "plan.repair_loop.max_iterations",
                    )
                )
            for key in ("stop_condition", "findings_source"):
                if not _is_text(repair_loop.get(key)):
                    findings.append(
                        _finding(
                            "schema-missing", None, "plan.repair_loop.%s" % key
                        )
                    )
    elif repair_loop is not None:
        findings.append(
            _finding(
                "schema-missing",
                None,
                "plan.repair_loop is only valid with pattern=iteration",
            )
        )

    decision = plan.get("decision")
    packages = plan.get("packages")
    if isinstance(packages, list) and packages:
        if decision == "decomposed":
            if plan.get("rule") is None:
                findings.append(
                    _finding("schema-missing", None, "decomposed requires rule")
                )
            if len(packages) < 2:
                findings.append(
                    _finding(
                        "schema-missing",
                        None,
                        "decomposed requires at least two packages",
                    )
                )
            if not plan.get("source_artifacts"):
                findings.append(
                    _finding(
                        "schema-missing",
                        None,
                        "decomposed requires source_artifacts",
                    )
                )
            if not plan.get("required_outputs"):
                findings.append(
                    _finding(
                        "schema-missing",
                        None,
                        "decomposed requires required_outputs",
                    )
                )
            if plan.get("gate_verdict") != "admit":
                findings.append(
                    _finding(
                        "schema-missing",
                        None,
                        "decomposed requires gate_verdict=admit",
                    )
                )
        elif decision in ("single-package", "disabled", "fallback"):
            expected_verdict = (
                "single-package" if decision == "single-package" else "no-gate-run"
            )
            if plan.get("rule") is not None:
                findings.append(
                    _finding(
                        "schema-missing", None, "%s requires rule=null" % decision
                    )
                )
            if len(packages) != 1:
                findings.append(
                    _finding(
                        "schema-missing",
                        None,
                        "%s requires exactly one package" % decision,
                    )
                )
            if plan.get("integrator_outputs"):
                findings.append(
                    _finding(
                        "schema-missing",
                        None,
                        "%s requires integrator_outputs=[]" % decision,
                    )
                )
            if plan.get("gate_verdict") != expected_verdict:
                findings.append(
                    _finding(
                        "schema-missing",
                        None,
                        "%s requires gate_verdict=%s"
                        % (decision, expected_verdict),
                    )
                )

    if isinstance(packages, list):
        for index, package in enumerate(packages):
            findings.extend(_schema_check_package(package, stage, index))
    return findings


def _select_plan(document, stage, stage_attempt):
    matches = [
        fence
        for fence in document["plan_fences"]
        if fence["stage"] == stage and fence["stage_attempt"] == stage_attempt
    ]
    if not matches:
        raise InputError(
            "no wp-plan fence for stage '%s' stage_attempt %s"
            % (stage, stage_attempt)
        )
    if len(matches) > 1:
        raise InputError(
            "duplicate wp-plan fences for stage '%s' stage_attempt %s"
            % (stage, stage_attempt)
        )
    return matches[0]["plan"]


def _amendments_for(document, stage, stage_attempt):
    selected = [
        fence["amendment"]
        for fence in document["amendments"]
        if fence["stage"] == stage and fence["stage_attempt"] == stage_attempt
    ]
    seen = set()
    for amendment in selected:
        seq = amendment.get("seq")
        if not _is_int(seq) or seq < 1:
            raise InputError("wp-plan-amendment lacks a positive integer seq")
        if seq in seen:
            raise InputError("duplicate wp-plan-amendment seq %s" % seq)
        seen.add(seq)
    return sorted(selected, key=lambda body: body["seq"])


def _amendment_hash_findings(plan, amendments):
    findings = []
    current = plan.get("plan_hash")
    for amendment in sorted(amendments, key=lambda body: body["seq"]):
        recorded_supersedes = amendment.get("supersedes_plan_hash")
        if recorded_supersedes != current:
            findings.append(
                _finding(
                    "plan-hash-mismatch",
                    None,
                    "amendment seq %s supersedes %r, effective hash is %r"
                    % (amendment["seq"], recorded_supersedes, current),
                )
            )
        current = amendment.get("plan_hash")
    return findings


def _load_plan(args, document):
    stage = args.stage
    if args.plan_json:
        plan = _read_json_object(args.plan_json, "--plan-json")
        amendments = []
        if args.stage_attempt is not None:
            attempt = args.stage_attempt
        elif document is not None and highest_stage_attempt(document) > 0:
            attempt = highest_stage_attempt(document)
        else:
            attempt = plan.get("stage_attempt")
        return plan, [], attempt
    attempt = args.stage_attempt
    if attempt is None:
        attempt = highest_stage_attempt(document)
        if attempt <= 0:
            raise InputError("spine contains no plan fence or stage attempt")
    plan = _select_plan(document, stage, attempt)
    amendments = _amendments_for(document, stage, attempt)
    return effective_plan(plan, amendments), amendments, attempt


def _emit(record, json_out):
    text = json.dumps(record, ensure_ascii=False)
    if json_out:
        try:
            with open(json_out, "w", encoding="utf-8") as handle:
                handle.write(text + "\n")
        except OSError as exc:
            raise InputError("cannot write --json-out %s: %s" % (json_out, exc))
    print(text)


def run(args):
    if not args.spine and not args.plan_json:
        raise InputError("one of --spine or --plan-json is required")
    document = read_spine(args.spine) if args.spine else None

    plan, amendments, attempt = _load_plan(args, document)

    if args.check == "preflight":
        packages = plan.get("packages") if isinstance(plan, dict) else None
        if isinstance(packages, list) and any(
            isinstance(package, dict) and package.get("owned_paths")
            for package in packages
        ):
            if not args.manifest:
                raise InputError(
                    "--manifest is required by --check preflight when a package owns paths"
                )
        raise CheckUnavailable("check 'preflight' is not available in this build")

    if args.check == "retry":
        if not args.wp_id:
            raise InputError("--check retry requires --wp-id")
        if args.wp_attempt is None:
            raise InputError("--check retry requires --wp-attempt")
        raise CheckUnavailable("check 'retry' is not available in this build")

    findings = validate_plan_schema(plan, args.stage, attempt)
    recorded_hash = plan.get("plan_hash") if isinstance(plan, dict) else None
    recomputed = canonical_plan_hash(plan)
    if not findings:
        findings.extend(_amendment_hash_findings(plan, amendments))
        if recorded_hash != recomputed:
            findings.append(
                _finding(
                    "plan-hash-mismatch",
                    None,
                    "recorded %r, recomputed %r" % (recorded_hash, recomputed),
                )
            )
    findings = _sort_findings(findings)

    if findings:
        verdict = "reject"
    elif plan.get("decision") == "single-package":
        verdict = "single-package"
    else:
        verdict = "admit"

    record = {
        "schema_version": SCHEMA_VERSION,
        "check": args.check,
        "stage": args.stage,
        "verdict": verdict,
        "findings": findings,
        "plan_hash": recomputed,
        "checked_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "evidence_ptr": args.json_out or None,
    }
    _emit(record, args.json_out)
    return 0 if verdict in ("admit", "single-package") else 1


def build_parser():
    parser = argparse.ArgumentParser(
        description="Deterministic Work Package decomposition gate."
    )
    parser.add_argument("--spine", default="", help="line state spine path")
    parser.add_argument("--stage", required=True, help="canonical stage name")
    parser.add_argument("--check", required=True, choices=CHECK_NAMES)
    parser.add_argument("--plan-json", default="", help="plan body fixture path")
    parser.add_argument("--manifest", default="", help="064 Ownership Manifest path")
    parser.add_argument("--repo", default="", help="repository root for path normalization")
    parser.add_argument("--slot-cap-ceiling", type=int, default=4)
    parser.add_argument("--stage-attempt", type=int, default=None)
    parser.add_argument("--wp-id", default="")
    parser.add_argument("--wp-attempt", type=int, default=None)
    parser.add_argument("--json-out", default="")
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        return run(args)
    except InputError as exc:
        print("wp-gate: input error: %s" % exc, file=sys.stderr)
        return 2
    except CheckUnavailable as exc:
        print("wp-gate: %s" % exc, file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
