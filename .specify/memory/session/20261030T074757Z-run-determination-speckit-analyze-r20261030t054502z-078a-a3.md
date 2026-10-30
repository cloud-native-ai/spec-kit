---
id: "20261030T074757Z-run-determination-speckit-analyze-r20261030t054502z-078a-a3"
scope: "session"
source: "/speckit.analyze"
feature: "078-coaching-skills"
tags: ["run-determination", "r20261030t054502z-078a-a3"]
title: "run-determination /speckit.analyze r20261030T054502Z-078a-a3"
created: "2026-10-30T07:47:57Z"
summary: "/speckit.analyze run=r20261030T054502Z-078a-a3 token=not_evaluated elapsed=regressed artifact=not_evaluated satisfaction=accepted"
---

/speckit.analyze run=r20261030T054502Z-078a-a3 token=not_evaluated elapsed=regressed artifact=not_evaluated satisfaction=accepted

```json
{
  "kind": "speckit.run-determination",
  "schema_version": 1,
  "unit_id": "/speckit.analyze",
  "unit_type": "command",
  "run_id": "r20261030T054502Z-078a-a3",
  "feature": "078-coaching-skills",
  "feature_id": null,
  "determined_at": "2026-10-30T07:47:57Z",
  "settled_at": "2026-10-30T11:32:08Z",
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
      "verdict": "regressed",
      "reason": null,
      "signal": {
        "key": "elapsed",
        "direction": "reduce"
      },
      "measurement": {
        "source": "caller_declared_ms",
        "ms": 532000,
        "note": "derived from .specify/state/078-coaching-skills.md stage_started_at=1793345940 to 1793346472 UTC; no per-run timer sensor"
      },
      "baseline": {
        "run_id": "r20261030T054502Z-078a-a2",
        "source": "caller_declared_ms",
        "value": 467000
      },
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
      "feature"
    ],
    "lanes_read": {
      "session": "available",
      "user_input": "in_context",
      "evidence": "unavailable"
    },
    "evidence_digests": [],
    "honesty_boundary": [
      "the unresolved-red state is declared by the caller, never derived (§ 5.4)",
      "a wrap-up that never called determine leaves no trace: absence of a record is not evidence of a clean run (§ 4)"
    ],
    "red_state_input": "caller-declaration"
  },
  "change_point": {
    "id": "cp-r20261030T054502Z-078a-a3",
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
        "verdict": "regressed",
        "reason": null,
        "observation": "elapsed regressed via source=caller_declared_ms: current=532000 baseline=467000",
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
        "observation": "artifact_correctness not_evaluated: failed-set diff not_evaluated added=None, green evidence not_evaluated uncovered=0 declared_checks=None collected=None reason=no_declared_checks",
        "parked_via": "none",
        "ref": null
      }
    ]
  }
}
```
