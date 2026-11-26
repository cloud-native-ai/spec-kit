#!/usr/bin/env python3
"""check-run-record.py — keep execution and acceptance axes from collapsing.

A drawing run produces evidence on several distinct axes. A process exit, an
HTTP 2xx, a correct model alias, an empty permission counter, a completed step
and a correct diagram are NOT interchangeable, and no one axis may stand in for
another. This checker validates a small JSON run record with exactly five axes:

  transport           completed | failed | not_started, with evidence
  runtime_identity    executor/model/context_window/reasoning_effort/config_root/
                      session_id values (or not_provided) + evidence; it is an
                      identity record, never a verdict — verdict keys are refused
  permission_events   status none | blocked_by_permission | not_assessed, scoped
                      events (read_only | deliverable_write | unknown) and their
                      assessment text; any denial keeps blocked_by_permission,
                      even when the transport completed and artifacts exist
  required_steps      per-step completed | failed | blocked | skipped | not_started
                      with evidence; a non-completed step means at least one
                      business axis must be non-pass
  business_result     semantic / visual / interaction / reproducibility /
                      satisfaction, each with its own status and evidence;
                      satisfaction is only not_evaluated or user_provided

Refused collapses include a top-level status/overall verdict, semantic pass on
partial/unsupported extraction, an unsupported parser claimed as graph
corruption, a denied event recorded as "none", a fabricated block, and a
completed step without evidence.

Exit codes: 0 record consistent; 1 one or more violations; 2 usage or I/O error.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

VERSION = "1.0.0"
MAX_BYTES = 1_000_000

TOP_KEYS = ("run_id", "axes", "anomalies")
OPTIONAL_TOP = ("notes",)
COLLAPSE_KEYS = ("status", "overall", "result", "success", "verdict", "pass", "accepted", "satisfied")
AXIS_KEYS = ("transport", "runtime_identity", "permission_events", "required_steps", "business_result")
TRANSPORT_STATUS = ("completed", "failed", "not_started")
PERMISSION_STATUS = ("none", "blocked_by_permission", "not_assessed")
PERMISSION_SCOPE = ("read_only", "deliverable_write", "unknown")
PERMISSION_OUTCOME = ("denied", "allowed", "not_observed")
STEP_STATUS = ("completed", "failed", "blocked", "skipped", "not_started")
SEMANTIC_STATUS = ("pass", "partial", "fail", "unsupported", "not_evaluated")
EXTRACTION_STATUS = ("complete", "partial", "unsupported", "not_attempted")
VISUAL_STATUS = ("pass", "partial", "fail", "not_evaluated")
INTERACTION_STATUS = ("pass", "partial", "fail", "not_applicable", "not_evaluated")
REPRO_STATUS = ("pass", "partial", "fail", "not_evaluated")
SATISFACTION_STATUS = ("not_evaluated", "user_provided")
SATISFACTION_CLAIMS = ("satisfied", "pass", "accepted", "approved", "happy")
IDENTITY_KEYS = ("executor", "model", "context_window", "reasoning_effort", "config_root", "session_id", "evidence")
BUSINESS_KEYS = ("semantic", "visual", "interaction", "reproducibility", "satisfaction")


class RecordError(ValueError):
    pass


def fail(violations, code, detail):
    violations.append({"code": code, "detail": detail})


def text(value):
    return isinstance(value, str) and value.strip() != ""


def require(condition, message):
    if not condition:
        raise RecordError(message)


def closed_keys(obj, expected, field, violations):
    if not isinstance(obj, dict):
        fail(violations, "schema-type", f"{field}: expected an object")
        return False
    missing = [key for key in expected if key not in obj]
    if missing:
        fail(violations, "schema-missing", f"{field}: missing {missing}")
    extra = sorted(set(obj) - set(expected))
    if extra:
        fail(violations, "schema-extra", f"{field}: unknown fields {extra}")
    return not missing and not extra


def check_text_field(obj, key, field, violations):
    if not isinstance(obj.get(key), str) or not obj.get(key, "").strip():
        fail(violations, "schema-type", f"{field}.{key} must be a non-empty string")


def check_transport(axis, violations):
    if not closed_keys(axis, ("status", "evidence"), "axes.transport", violations):
        return
    if axis["status"] not in TRANSPORT_STATUS:
        fail(violations, "enum", f"axes.transport.status {axis['status']!r} not in {TRANSPORT_STATUS}")
    check_text_field(axis, "evidence", "axes.transport", violations)


def check_identity(axis, violations):
    if not isinstance(axis, dict):
        fail(violations, "schema-type", "axes.runtime_identity: expected an object")
        return
    for forbidden in ("status", "verdict", "pass", "result", "success", "score", "verdict_status"):
        if forbidden in axis:
            fail(violations, "identity-verdict",
                 f"axes.runtime_identity.{forbidden}: identity is a record, not a verdict")
    if not closed_keys(axis, IDENTITY_KEYS, "axes.runtime_identity", violations):
        return
    for key in IDENTITY_KEYS:
        check_text_field(axis, key, "axes.runtime_identity", violations)


def check_permission_events(axis, violations):
    if not closed_keys(axis, ("status", "events", "assessment"), "axes.permission_events", violations):
        return
    status = axis.get("status")
    if status not in PERMISSION_STATUS:
        fail(violations, "enum", f"axes.permission_events.status {status!r} not in {PERMISSION_STATUS}")
    check_text_field(axis, "assessment", "axes.permission_events", violations)
    events = axis.get("events")
    if not isinstance(events, list):
        fail(violations, "schema-type", "axes.permission_events.events: expected a list")
        return
    denied = 0
    for index, event in enumerate(events):
        field = f"axes.permission_events.events[{index}]"
        if not closed_keys(event, ("tool", "scope", "outcome", "purpose", "evidence"), field, violations):
            continue
        for key in ("tool", "purpose", "evidence"):
            check_text_field(event, key, field, violations)
        if event.get("scope") not in PERMISSION_SCOPE:
            fail(violations, "enum", f"{field}.scope {event.get('scope')!r} not in {PERMISSION_SCOPE}")
        if event.get("outcome") not in PERMISSION_OUTCOME:
            fail(violations, "enum", f"{field}.outcome {event.get('outcome')!r} not in {PERMISSION_OUTCOME}")
        if event.get("outcome") == "denied":
            denied += 1
    if status == "none" and events:
        fail(violations, "permission-status-mismatch",
             "axes.permission_events.status is 'none' but events are recorded")
    if status == "blocked_by_permission" and denied == 0:
        fail(violations, "fabricated-block",
             "axes.permission_events.status is 'blocked_by_permission' without a denied event")
    if denied and status != "blocked_by_permission":
        fail(violations, "permission-status-mismatch",
             f"{denied} denied event(s) require status 'blocked_by_permission', got {status!r}")


def check_steps(axis, violations):
    if not closed_keys(axis, ("steps",), "axes.required_steps", violations):
        return False
    steps = axis.get("steps")
    if not isinstance(steps, list) or not steps:
        fail(violations, "schema-type", "axes.required_steps.steps: expected a non-empty list")
        return False
    all_completed = True
    for index, step in enumerate(steps):
        field = f"axes.required_steps.steps[{index}]"
        if not closed_keys(step, ("id", "status", "evidence"), field, violations):
            all_completed = False
            continue
        check_text_field(step, "id", field, violations)
        check_text_field(step, "evidence", field, violations)
        if step.get("status") not in STEP_STATUS:
            fail(violations, "enum", f"{field}.status {step.get('status')!r} not in {STEP_STATUS}")
        if step.get("status") != "completed":
            all_completed = False
        if step.get("status") == "completed" and not text(step.get("evidence")):
            fail(violations, "step-evidence", f"{field}: a completed step needs evidence")
    return all_completed


def check_semantic(axis, violations):
    if not isinstance(axis, dict):
        fail(violations, "schema-type", "axes.business_result.semantic: expected an object")
        return
    allowed = ("status", "extraction", "evidence", "reason")
    unknown = sorted(set(axis) - set(allowed))
    if unknown:
        fail(violations, "schema-extra", f"axes.business_result.semantic: unknown fields {unknown}")
    for key in ("status", "extraction", "evidence"):
        if key not in axis:
            fail(violations, "schema-missing", f"axes.business_result.semantic: missing {key}")
    status = axis.get("status")
    extraction = axis.get("extraction")
    if status not in SEMANTIC_STATUS:
        fail(violations, "enum", f"axes.business_result.semantic.status {status!r} not in {SEMANTIC_STATUS}")
    if extraction not in EXTRACTION_STATUS:
        fail(violations, "enum", f"axes.business_result.semantic.extraction {extraction!r} not in {EXTRACTION_STATUS}")
    check_text_field(axis, "evidence", "axes.business_result.semantic", violations)
    if status == "pass" and extraction != "complete":
        fail(violations, "semantic-pass-partial",
             f"semantic pass requires extraction=complete, got {extraction!r}")
    if extraction in ("partial", "unsupported", "not_attempted") and status == "pass":
        fail(violations, "semantic-pass-partial", "unsupported/partial extraction cannot be a semantic pass")
    if status == "unsupported" and extraction not in ("unsupported", "not_attempted"):
        fail(violations, "semantic-unsupported-mismatch",
             f"semantic status 'unsupported' needs extraction unsupported/not_attempted, got {extraction!r}")
    reason = str(axis.get("reason", "")).strip().lower().replace("_", "-").replace(" ", "-")
    if status == "fail" and reason in ("graph-corruption", "corruption", "graph-delta"):
        if extraction != "complete":
            fail(violations, "unsupported-corruption",
                 f"graph corruption cannot be claimed with extraction={extraction!r}; record it as partial/unsupported")


def check_simple_axis(axis, field, statuses, violations):
    if not closed_keys(axis, ("status", "evidence"), field, violations):
        return None
    status = axis.get("status")
    if status not in statuses:
        fail(violations, "enum", f"{field}.status {status!r} not in {statuses}")
    check_text_field(axis, "evidence", field, violations)
    if status == "pass" and not text(axis.get("evidence")):
        fail(violations, "axis-evidence", f"{field}: pass needs evidence")
    return status


def check_interaction(axis, violations):
    if not closed_keys(axis, ("status", "exercised", "evidence"), "axes.business_result.interaction", violations):
        return None
    status = axis.get("status")
    if status not in INTERACTION_STATUS:
        fail(violations, "enum", f"axes.business_result.interaction.status {status!r} not in {INTERACTION_STATUS}")
    if not isinstance(axis.get("exercised"), bool):
        fail(violations, "schema-type", "axes.business_result.interaction.exercised must be true or false")
    check_text_field(axis, "evidence", "axes.business_result.interaction", violations)
    if status == "pass" and axis.get("exercised") is not True:
        fail(violations, "interaction-not-exercised",
             "interaction pass requires exercised=true with actual input evidence")
    return status


def check_satisfaction(axis, violations):
    if not closed_keys(axis, ("status", "evidence"), "axes.business_result.satisfaction", violations):
        return
    status = axis.get("status")
    if status not in SATISFACTION_STATUS:
        code = "satisfaction-claim" if str(status).strip().lower() in SATISFACTION_CLAIMS else "enum"
        fail(violations, code, f"axes.business_result.satisfaction.status {status!r} is not an evidence state")
    check_text_field(axis, "evidence", "axes.business_result.satisfaction", violations)
    if status == "user_provided" and not text(axis.get("evidence")):
        fail(violations, "satisfaction-claim", "user_provided satisfaction needs the user's evidence reference")


def check_business(axis, violations):
    if not closed_keys(axis, BUSINESS_KEYS, "axes.business_result", violations):
        return []
    statuses = []
    if "semantic" in axis:
        check_semantic(axis["semantic"], violations)
        if isinstance(axis["semantic"], dict):
            statuses.append(axis["semantic"].get("status"))
    if "visual" in axis:
        statuses.append(check_simple_axis(axis["visual"], "axes.business_result.visual", VISUAL_STATUS, violations))
    if "interaction" in axis:
        statuses.append(check_interaction(axis["interaction"], violations))
    if "reproducibility" in axis:
        statuses.append(check_simple_axis(axis["reproducibility"], "axes.business_result.reproducibility", REPRO_STATUS, violations))
    if "satisfaction" in axis:
        check_satisfaction(axis["satisfaction"], violations)
    return [status for status in statuses if status is not None]


def inspect(record, violations):
    if not isinstance(record, dict):
        fail(violations, "schema-type", "record: expected a JSON object")
        return
    for key in COLLAPSE_KEYS:
        if key in record:
            fail(violations, "collapsed-verdict",
                 f"top-level {key!r} collapses the axes; report each axis instead")
    expected = list(TOP_KEYS) + list(OPTIONAL_TOP)
    missing = [key for key in TOP_KEYS if key not in record]
    if missing:
        fail(violations, "schema-missing", f"record: missing {missing}")
    extra = sorted(set(record) - set(expected) - set(COLLAPSE_KEYS))
    if extra:
        fail(violations, "schema-extra", f"record: unknown fields {extra}")
    check_text_field(record, "run_id", "record", violations)
    anomalies = record.get("anomalies")
    if not isinstance(anomalies, list) or not all(isinstance(item, str) and item.strip() for item in anomalies):
        fail(violations, "schema-type", "record.anomalies must be a list of non-empty strings")
        anomalies = []
    if "notes" in record and (not isinstance(record["notes"], list)
                              or not all(isinstance(item, str) for item in record["notes"])):
        fail(violations, "schema-type", "record.notes must be a list of strings")
    axes = record.get("axes")
    if not isinstance(axes, dict):
        fail(violations, "schema-type", "record.axes: expected an object")
        return
    missing_axes = [key for key in AXIS_KEYS if key not in axes]
    if missing_axes:
        fail(violations, "schema-missing", f"record.axes: missing {missing_axes}")
    extra_axes = sorted(set(axes) - set(AXIS_KEYS))
    if extra_axes:
        fail(violations, "schema-extra", f"record.axes: unknown fields {extra_axes}")
    if "transport" in axes:
        check_transport(axes["transport"], violations)
    if "runtime_identity" in axes:
        check_identity(axes["runtime_identity"], violations)
    if "permission_events" in axes:
        check_permission_events(axes["permission_events"], violations)
    all_steps_completed = True
    if "required_steps" in axes:
        all_steps_completed = check_steps(axes["required_steps"], violations)
    business = axes.get("business_result")
    business_statuses = check_business(business, violations) if isinstance(business, dict) else []
    if not all_steps_completed and business_statuses and all(status == "pass" for status in business_statuses):
        fail(violations, "steps-vs-business",
             "a required step did not complete, yet every business axis is pass")
    permission_status = None
    if isinstance(axes.get("permission_events"), dict):
        permission_status = axes["permission_events"].get("status")
    if permission_status == "blocked_by_permission" and not anomalies:
        fail(violations, "blocked-without-anomaly",
             "a blocked_by_permission run must list the anomaly explicitly")


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Validate a five-axis draw-diagram run record (transport, runtime identity, permission "
        "events, required steps, business result) and refuse cross-axis collapses. Exit 0 consistent, "
        "1 violations, 2 usage/I-O error.",
        allow_abbrev=False,
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {VERSION}")
    parser.add_argument("--record", type=Path, required=True, help="run-record JSON path")
    parser.add_argument("--json", action="store_true", help="print the machine verdict as JSON")
    args = parser.parse_args(argv)
    violations = []
    try:
        require(args.record.is_file(), f"record not found: {args.record}")
        require(args.record.stat().st_size <= MAX_BYTES, "record exceeds 1 MB")
        try:
            record = json.loads(args.record.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise RecordError(f"record is not valid JSON: {exc}") from exc
        inspect(record, violations)
    except RecordError as exc:
        print(f"record error: {exc}", file=sys.stderr)
        return 2
    except OSError as exc:
        print(f"I/O error: {exc}", file=sys.stderr)
        return 2
    verdict = {
        "status": "pass" if not violations else "fail",
        "violations": violations,
        "violation_count": len(violations),
    }
    if isinstance(record, dict) and isinstance(record.get("axes"), dict):
        verdict["axis_status"] = {
            key: (record["axes"].get(key, {}).get("status")
                  if isinstance(record["axes"].get(key), dict) else None)
            for key in AXIS_KEYS
        }
    if args.json:
        print(json.dumps(verdict, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print(f"run record: {args.record}")
        print(f"verdict: {verdict['status']} ({verdict['violation_count']} violation(s))")
        for item in violations:
            print(f"  - [{item['code']}] {item['detail']}")
    return 0 if not violations else 1


if __name__ == "__main__":
    raise SystemExit(main())
