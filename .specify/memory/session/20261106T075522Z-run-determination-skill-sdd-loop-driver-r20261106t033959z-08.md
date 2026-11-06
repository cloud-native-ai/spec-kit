---
id: "20261106T075522Z-run-determination-skill-sdd-loop-driver-r20261106t033959z-08"
scope: "session"
source: "skill:sdd-loop-driver"
feature: "086-efficient-test-execution"
tags: ["run-determination", "r20261106t033959z-086a"]
title: "run-determination skill:sdd-loop-driver r20261106T033959Z-086a"
created: "2026-11-06T07:55:22Z"
summary: "skill:sdd-loop-driver run=r20261106T033959Z-086a token=not_evaluated elapsed=not_evaluated artifact=not_evaluated satisfaction=not_evaluated"
---

skill:sdd-loop-driver run=r20261106T033959Z-086a token=not_evaluated elapsed=not_evaluated artifact=not_evaluated satisfaction=not_evaluated

```json
{
  "kind": "speckit.run-determination",
  "schema_version": 1,
  "unit_id": "skill:sdd-loop-driver",
  "unit_type": "skill",
  "run_id": "r20261106T033959Z-086a",
  "feature": "086-efficient-test-execution",
  "feature_id": "086-efficient-test-execution",
  "determined_at": "2026-11-06T07:55:22Z",
  "settled_at": null,
  "complexity": "complex",
  "qualification": "qualified",
  "axes": {
    "token_consumption": {
      "verdict": "not_evaluated",
      "reason": "source_unavailable",
      "signal": {
        "key": "token_consumption",
        "direction": "reduce"
      },
      "measurement": {
        "source": "unavailable",
        "input_tokens": null,
        "output_tokens": null,
        "cache_read_input_tokens": null,
        "cache_creation_input_tokens": null,
        "total_tokens": null,
        "proxy_lines": null,
        "proxy_bytes": null,
        "note": null
      },
      "baseline": null,
      "evidence_refs": []
    },
    "elapsed": {
      "verdict": "not_evaluated",
      "reason": "not_comparable",
      "signal": {
        "key": "elapsed",
        "direction": "reduce"
      },
      "measurement": {
        "source": "caller_declared_ms",
        "ms": 15420000,
        "note": "run start 2026-11-06T03:39:59Z to closure 07:57Z, from the line-registry timestamps"
      },
      "baseline": {
        "run_id": "r20261105T074027Z-084a",
        "source": "unavailable",
        "value": null
      },
      "evidence_refs": []
    },
    "artifact_correctness": {
      "verdict": "not_evaluated",
      "reason": "green_unproven",
      "signal": {
        "key": "artifact_correctness",
        "direction": "improve"
      },
      "declared_checks": 1,
      "collected": 7554,
      "failed_set_diff": {
        "status": "empty",
        "added": [],
        "added_count": 0,
        "truncated": false
      },
      "green_evidence": {
        "status": "absent",
        "uncovered": [
          "closure-acceptance-check.py verdict=accept"
        ]
      },
      "evidence_refs": [
        ".specify/specs/086-efficient-test-execution/test-evidence/final-failed.txt",
        ".specify/specs/086-efficient-test-execution/test-evidence/baseline-failed.txt",
        ".specify/specs/086-efficient-test-execution/notes/red-first-evidence.md"
      ]
    },
    "satisfaction": {
      "verdict": "not_evaluated",
      "reason": "pending_next_turn",
      "user_turn_class": "no_user_input",
      "unresolved_red": {
        "present": "false",
        "source": "none"
      },
      "adjacent": false,
      "signal": {
        "key": "satisfaction",
        "direction": "improve"
      }
    }
  },
  "provenance": {
    "engine": "scripts/python/run-determination.py",
    "declared_by_caller": [
      "complexity",
      "user_turn_class",
      "unresolved_red",
      "qualification",
      "elapsed_ms",
      "names_current",
      "names_baseline",
      "declared_check",
      "green_check",
      "red_first_refs",
      "collected",
      "feature"
    ],
    "lanes_read": {
      "session": "available",
      "user_input": "in_context",
      "evidence": "stale"
    },
    "evidence_digests": [],
    "honesty_boundary": [
      "the unresolved-red state is declared by the caller, never derived (§ 5.4)",
      "a wrap-up that never called determine leaves no trace: absence of a record is not evidence of a clean run (§ 4)"
    ],
    "red_state_input": "caller-declaration"
  },
  "change_point": {
    "id": "cp-r20261106T033959Z-086a",
    "clean": false,
    "findings": [
      {
        "axis": "token_consumption",
        "verdict": "not_evaluated",
        "reason": "source_unavailable",
        "observation": "token_consumption not_evaluated via source=unavailable: current=None baseline=None reason=source_unavailable",
        "signal": {
          "key": "token_consumption",
          "direction": "reduce"
        },
        "evidence_refs": [],
        "status": "observed"
      },
      {
        "axis": "elapsed",
        "verdict": "not_evaluated",
        "reason": "not_comparable",
        "observation": "elapsed not_evaluated via source=caller_declared_ms: current=15420000 baseline=None reason=not_comparable",
        "signal": {
          "key": "elapsed",
          "direction": "reduce"
        },
        "evidence_refs": [],
        "status": "observed"
      },
      {
        "axis": "artifact_correctness",
        "verdict": "not_evaluated",
        "reason": "green_unproven",
        "observation": "artifact_correctness not_evaluated: failed-set diff empty added=0, green evidence absent uncovered=1 declared_checks=1 collected=7554 reason=green_unproven",
        "signal": {
          "key": "artifact_correctness",
          "direction": "improve"
        },
        "evidence_refs": [
          ".specify/specs/086-efficient-test-execution/test-evidence/final-failed.txt",
          ".specify/specs/086-efficient-test-execution/test-evidence/baseline-failed.txt",
          ".specify/specs/086-efficient-test-execution/notes/red-first-evidence.md"
        ],
        "status": "observed"
      },
      {
        "axis": "satisfaction",
        "verdict": "not_evaluated",
        "reason": "pending_next_turn",
        "observation": "satisfaction not_evaluated: user_turn_class=no_user_input unresolved_red=false adjacent=False reason=pending_next_turn",
        "signal": {
          "key": "satisfaction",
          "direction": "improve"
        },
        "evidence_refs": [],
        "status": "observed"
      }
    ]
  },
  "passive_trigger": {
    "trigger_feedback": false,
    "composes_with_should_prompt": true,
    "out_of_scope": [
      {
        "observation": "token_consumption not_evaluated via source=unavailable: current=None baseline=None reason=source_unavailable",
        "parked_via": "none",
        "ref": null
      },
      {
        "observation": "elapsed not_evaluated via source=caller_declared_ms: current=15420000 baseline=None reason=not_comparable",
        "parked_via": "none",
        "ref": null
      },
      {
        "observation": "artifact_correctness not_evaluated: failed-set diff empty added=0, green evidence absent uncovered=1 declared_checks=1 collected=7554 reason=green_unproven",
        "parked_via": "none",
        "ref": null
      },
      {
        "observation": "satisfaction not_evaluated: user_turn_class=no_user_input unresolved_red=false adjacent=False reason=pending_next_turn",
        "parked_via": "none",
        "ref": null
      }
    ]
  }
}
```
