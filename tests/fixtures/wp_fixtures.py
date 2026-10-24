"""Shared builders for Feature 070 (Work Package plan, spine fences, manifest).

Every builder takes the destination ``Path`` explicitly and writes only inside
the caller's temporary directory. Nothing here reads or writes the repository's
real line registry, state spines, or skill mirror.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

LINE_ID = "line-demo"
RUN_ID = "run-demo"
STAGE = "plan"

# Keys excluded from the canonical plan hash (WP-06 / V-PLAN.7). Any key named
# ``at`` or ending in ``_at`` is removed recursively as well.
HASH_EXCLUDED_KEYS = ("plan_hash", "slot_cap_requested", "slot_cap_ceiling")


def _is_timestamp_key(key: str) -> bool:
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


def canonical_hash_of(plan: dict) -> str:
    """Independent implementation of the WP-06 canonical plan hash."""
    body = _strip_hash_exclusions(plan)
    encoded = json.dumps(
        body, sort_keys=True, ensure_ascii=False, separators=(",", ":")
    ).encode("utf-8")
    return "sha256:" + hashlib.sha256(encoded).hexdigest()


def make_package(wp_id: str = "plan-wp01", stage: str = STAGE, **overrides) -> dict:
    package = {
        "wp_id": wp_id,
        "stage": stage,
        "objective": "Produce the bounded artifact for %s" % wp_id,
        "kind": "read-only",
        "source_refs": ["plan.md#Design Overview"],
        "inputs": ["plan.md"],
        "outputs": ["findings/%s.md" % wp_id],
        "intermediate_outputs": [],
        "owned_paths": [],
        "read_only_paths": ["plan.md"],
        "depends_on": [],
        "parallel_safe": True,
        "max_turns": 120,
        "bounded_by": {"unit": "tasks", "count": 2},
        "acceptance": [
            {
                "id": "A1",
                "check": "the declared output exists and states the bounded outcome",
                "evidence": "findings/%s.md" % wp_id,
            }
        ],
        "sentinel": sentinel_for(wp_id),
        "evidence": "wp/%s-%s" % (stage, wp_id),
        "seat": {"role": "stage-worker", "stage": "executor", "type": "Worker"},
        "resources": {
            "ports": "none",
            "tmp_dir": "none",
            "cache_dir": "none",
            "shared_readonly": [],
        },
    }
    package.update(overrides)
    return package


def sentinel_for(wp_id: str) -> str:
    return "WP-%s-DONE" % wp_id.upper()


def make_two_package_plan(stage: str = STAGE, **overrides) -> dict:
    plan = make_plan(
        packages=[
            make_package("plan-wp01", stage),
            make_package(
                "plan-wp02",
                stage,
                source_refs=["contracts/wp-gate.md#WG-01"],
                inputs=["contracts/wp-gate.md"],
                outputs=["findings/plan-wp02.md"],
                read_only_paths=["contracts/wp-gate.md"],
            ),
        ],
        stage=stage,
        **overrides,
    )
    return plan


def make_write_package(wp_id: str = "plan-wp03", stage: str = STAGE, **overrides) -> dict:
    package = make_package(
        wp_id,
        stage,
        kind="write",
        parallel_safe=False,
        owned_paths=["src/generated/"],
        outputs=["src/generated/notes.md"],
    )
    package.update(overrides)
    return package


def make_plan(packages=None, stage: str = STAGE, **overrides) -> dict:
    packages = packages if packages is not None else [make_package(stage=stage)]
    plan = {
        "schema_version": 1,
        "line_id": LINE_ID,
        "run_id": RUN_ID,
        "stage": stage,
        "stage_attempt": 1,
        "decision": "decomposed" if len(packages) > 1 else "single-package",
        "gate_verdict": "admit" if len(packages) > 1 else "single-package",
        "reason": "fixture plan",
        "rule": "decompose-plan-v1" if len(packages) > 1 else None,
        "source_artifacts": ["plan.md", "contracts/wp-gate.md"],
        "required_outputs": [
            output for package in packages for output in package["outputs"]
        ],
        "integrator_outputs": [],
        "pattern": "parallel"
        if len(packages) > 1 and all(p["kind"] == "read-only" for p in packages)
        else "serial",
        "tie_break": "wp_id-lexicographic",
        "slot_cap": 2 if len(packages) > 1 else 1,
        "packages": packages,
    }
    plan.update(overrides)
    plan["plan_hash"] = canonical_hash_of(plan)
    return plan


def write_plan_json(path: Path, plan: dict) -> Path:
    path.write_text(
        json.dumps(plan, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    return path


def plan_fence(plan: dict) -> str:
    return "\n".join(
        [
            "<!-- wp-plan:begin stage=%s stage_attempt=%s -->"
            % (plan["stage"], plan["stage_attempt"]),
            json.dumps(plan, indent=2, ensure_ascii=False),
            "<!-- wp-plan:end -->",
        ]
    )


def amendment_fence(amendment: dict) -> str:
    return "\n".join(
        [
            "<!-- wp-plan-amendment:begin stage=%s stage_attempt=%s seq=%s -->"
            % (
                amendment["stage"],
                amendment["stage_attempt"],
                amendment["seq"],
            ),
            json.dumps(amendment, indent=2, ensure_ascii=False),
            "<!-- wp-plan-amendment:end -->",
        ]
    )


def ledger_fence(events) -> str:
    lines = ["<!-- wp-ledger:begin -->"]
    lines += [json.dumps(event, ensure_ascii=False) for event in events]
    lines.append("<!-- wp-ledger:end -->")
    return "\n".join(lines)


def make_spine(
    path: Path,
    plan: dict | None = None,
    amendments=(),
    ledger=(),
    extra: str = "",
) -> Path:
    chunks = ["# Line state spine (fixture)", ""]
    if plan is not None:
        chunks += [plan_fence(plan), ""]
    for amendment in amendments:
        chunks += [amendment_fence(amendment), ""]
    if ledger:
        chunks += [ledger_fence(ledger), ""]
    if extra:
        chunks += [extra, ""]
    path.write_text("\n".join(chunks), encoding="utf-8")
    return path


def make_manifest(
    path: Path,
    line_id: str = LINE_ID,
    owned=(),
    read_only=(),
    forbidden=(),
) -> Path:
    path.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "line_id": line_id,
                "owned_paths": list(owned),
                "read_only_paths": list(read_only),
                "forbidden_paths": list(forbidden),
                "integration_depends_on": [],
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    return path


def plan_event(**overrides) -> dict:
    event = {
        "event": "plan",
        "stage": STAGE,
        "stage_attempt": 1,
        "plan_hash": "sha256:" + "0" * 64,
        "decision": "decomposed",
        "pattern": "parallel",
        "slot_cap": 2,
        "verdict": "admit",
        "gate_evidence": "wp/line-plan-a1-gate-plan.json",
        "at": 1790000000,
    }
    event.update(overrides)
    return event


def dispatch_event(**overrides) -> dict:
    event = {
        "event": "dispatch",
        "wp_id": "plan-wp01",
        "stage_attempt": 1,
        "wp_attempt": 1,
        "dispatch_order": 1,
        "started_at": 1790000100,
        "effective_concurrency": 2,
        "attempt_id": "plan-wp01-a1-w1",
    }
    event.update(overrides)
    return event


def settle_event(**overrides) -> dict:
    event = {
        "event": "settle",
        "wp_id": "plan-wp01",
        "ended_at": 1790000200,
        "runner_status": "DONE",
        "result_ptr": "wp/line-plan-plan-wp01-a1w1.result.json",
        "outputs": ["findings/plan-wp01.md"],
    }
    event.update(overrides)
    return event


def verdict_event(**overrides) -> dict:
    event = {
        "event": "verdict",
        "wp_id": "plan-wp01",
        "verdict": "pass",
        "verifier_execution": "verifier-1",
        "evidence_ptr": "wp/line-plan-plan-wp01-a1w1.verdict.json",
        "at": 1790000250,
    }
    event.update(overrides)
    return event


def ledger_sequence() -> list:
    """A minimal, deterministic happy-path event sequence for one package."""
    return [plan_event(), dispatch_event(), settle_event(), verdict_event()]


def attempt_scoped_evidence(
    state_dir: Path,
    line_id: str = LINE_ID,
    stage: str = STAGE,
    wp_id: str = "plan-wp01",
    stage_attempt: int = 1,
    wp_attempt: int = 1,
    check: str = "plan",
) -> dict:
    """Attempt-scoped evidence paths per WP-11 / DR1, rooted at ``state_dir``."""
    base = "%s-%s-%s-a%dw%d" % (line_id, stage, wp_id, stage_attempt, wp_attempt)
    gate = "%s-%s-a%d-gate-%s.json" % (line_id, stage, stage_attempt, check)
    report = "%s-%s-a%d-coordination" % (line_id, stage, stage_attempt)
    return {
        "result": state_dir / "wp" / (base + ".result.json"),
        "verdict": state_dir / "wp" / (base + ".verdict.json"),
        "gate": state_dir / "wp" / gate,
        "report_md": state_dir / "reports" / (report + ".md"),
        "report_json": state_dir / "reports" / (report + ".json"),
    }
