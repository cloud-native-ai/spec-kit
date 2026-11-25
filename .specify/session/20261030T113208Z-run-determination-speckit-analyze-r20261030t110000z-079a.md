---
id: "20261030T113208Z-run-determination-speckit-analyze-r20261030t110000z-079a"
scope: "session"
source: "/speckit.analyze"
feature: "079-humanize-run-output"
tags: ["run-determination", "r20261030t110000z-079a"]
title: "run-determination /speckit.analyze r20261030T110000Z-079a"
created: "2026-10-30T11:32:08Z"
summary: "/speckit.analyze run=r20261030T110000Z-079a token=not_evaluated elapsed=regressed artifact=not_evaluated satisfaction=accepted"
---

/speckit.analyze run=r20261030T110000Z-079a token=not_evaluated elapsed=regressed artifact=not_evaluated satisfaction=accepted

```json
{
  "kind": "speckit.run-determination",
  "schema_version": 1,
  "unit_id": "/speckit.analyze",
  "unit_type": "command",
  "run_id": "r20261030T110000Z-079a",
  "feature": "079-humanize-run-output",
  "feature_id": null,
  "determined_at": "2026-10-30T11:32:08Z",
  "settled_at": "2026-10-30T15:22:39Z",
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
        "note": "not measured; no session-file supplied"
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
        "ms": 589000,
        "note": "analyze stage wall clock from state stage_started_at"
      },
      "baseline": {
        "run_id": "r20261030T054502Z-078a-a3",
        "source": "caller_declared_ms",
        "value": 532000
      },
      "evidence_refs": []
    },
    "artifact_correctness": {
      "verdict": "not_evaluated",
      "reason": "no_baseline",
      "signal": {
        "key": "artifact_correctness",
        "direction": "improve"
      },
      "declared_checks": 1,
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
      "tool",
      "elapsed_ms",
      "declared_check",
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
    "red_state_input": "caller-declaration",
    "session_store": {
      "tool": "qodercli",
      "supported": false,
      "note": "no resolver exists for this agent CLI"
    }
  },
  "change_point": {
    "id": "cp-r20261030T110000Z-079a",
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
        "observation": "elapsed regressed via source=caller_declared_ms: current=589000 baseline=532000",
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
        "reason": "no_baseline",
        "observation": "artifact_correctness not_evaluated: failed-set diff not_evaluated added=None, green evidence not_evaluated uncovered=0 declared_checks=1 collected=None reason=no_baseline",
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
        "observation": "artifact_correctness not_evaluated: failed-set diff not_evaluated added=None, green evidence not_evaluated uncovered=0 declared_checks=1 collected=None reason=no_baseline",
        "parked_via": "none",
        "ref": null
      }
    ]
  }
}
```
