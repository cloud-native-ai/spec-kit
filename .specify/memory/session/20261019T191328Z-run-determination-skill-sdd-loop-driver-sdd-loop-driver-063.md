---
id: "20261019T191328Z-run-determination-skill-sdd-loop-driver-sdd-loop-driver-063"
scope: "session"
source: "skill:sdd-loop-driver"
feature: "063-review-p1-governance"
tags: ["run-determination", "sdd-loop-driver-063-p1-governance-20261020"]
title: "run-determination skill:sdd-loop-driver sdd-loop-driver-063-p1-governance-20261020"
created: "2026-10-19T19:13:28Z"
summary: "skill:sdd-loop-driver run=sdd-loop-driver-063-p1-governance-20261020 token=not_evaluated elapsed=not_evaluated artifact=not_evaluated satisfaction=accepted"
---

skill:sdd-loop-driver run=sdd-loop-driver-063-p1-governance-20261020 token=not_evaluated elapsed=not_evaluated artifact=not_evaluated satisfaction=accepted

```json
{
  "kind": "speckit.run-determination",
  "schema_version": 1,
  "unit_id": "skill:sdd-loop-driver",
  "unit_type": "skill",
  "run_id": "sdd-loop-driver-063-p1-governance-20261020",
  "feature": "063-review-p1-governance",
  "feature_id": "063",
  "determined_at": "2026-10-19T19:13:28Z",
  "settled_at": "2026-10-22T10:04:59Z",
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
      "reason": "source_unavailable",
      "signal": {
        "key": "elapsed",
        "direction": "reduce"
      },
      "measurement": {
        "source": "unavailable",
        "ms": null,
        "note": null
      },
      "baseline": null,
      "evidence_refs": []
    },
    "artifact_correctness": {
      "verdict": "not_evaluated",
      "reason": "no_declared_checks",
      "signal": {
        "key": "artifact_correctness",
        "direction": "improve"
      },
      "declared_checks": null,
      "collected": null,
      "failed_set_diff": {
        "status": "not_evaluated",
        "added": [],
        "added_count": null,
        "truncated": false
      },
      "green_evidence": {
        "status": "not_evaluated",
        "uncovered": []
      },
      "evidence_refs": []
    },
    "satisfaction": {
      "verdict": "accepted",
      "reason": null,
      "user_turn_class": "continuation_non_negative",
      "unresolved_red": {
        "present": "unknown",
        "source": "undeclared"
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
      "feature"
    ],
    "lanes_read": {
      "session": "available",
      "user_input": "in_context",
      "evidence": "available"
    },
    "evidence_digests": [
      "sha256:30617792316a720359985031c7455b376b16a08f6967fd1680c90a8f7a39c557"
    ],
    "honesty_boundary": [
      "the unresolved-red state is declared by the caller, never derived (§ 5.4)",
      "a wrap-up that never called determine leaves no trace: absence of a record is not evidence of a clean run (§ 4)"
    ],
    "red_state_input": "caller-declaration"
  },
  "change_point": {
    "id": "cp-sdd-loop-driver-063-p1-governance-20261020",
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
        "reason": "source_unavailable",
        "observation": "elapsed not_evaluated via source=unavailable: current=None baseline=None reason=source_unavailable",
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
        "reason": "no_declared_checks",
        "observation": "artifact_correctness not_evaluated: failed-set diff not_evaluated added=None, green evidence not_evaluated uncovered=0 declared_checks=None collected=None reason=no_declared_checks",
        "signal": {
          "key": "artifact_correctness",
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
        "observation": "elapsed not_evaluated via source=unavailable: current=None baseline=None reason=source_unavailable",
        "parked_via": "none",
        "ref": null
      },
      {
        "observation": "artifact_correctness not_evaluated: failed-set diff not_evaluated added=None, green evidence not_evaluated uncovered=0 declared_checks=None collected=None reason=no_declared_checks",
        "parked_via": "none",
        "ref": null
      }
    ]
  }
}
```
