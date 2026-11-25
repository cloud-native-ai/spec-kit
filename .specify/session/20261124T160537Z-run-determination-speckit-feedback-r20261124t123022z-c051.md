---
id: "20261124T160537Z-run-determination-speckit-feedback-r20261124t123022z-c051"
scope: "session"
source: "/speckit.feedback"
tags: ["run-determination", "r20261124t123022z-c051"]
title: "run-determination /speckit.feedback r20261124T123022Z-c051"
created: "2026-11-24T16:05:37Z"
summary: "/speckit.feedback run=r20261124T123022Z-c051 token=not_evaluated elapsed=regressed artifact=not_evaluated satisfaction=not_evaluated"
---

/speckit.feedback run=r20261124T123022Z-c051 token=not_evaluated elapsed=regressed artifact=not_evaluated satisfaction=not_evaluated

```json
{
  "kind": "speckit.run-determination",
  "schema_version": 1,
  "unit_id": "/speckit.feedback",
  "unit_type": "command",
  "run_id": "r20261124T123022Z-c051",
  "feature": null,
  "feature_id": null,
  "determined_at": "2026-11-24T16:05:37Z",
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
        "note": "total session token consumption unavailable; subagent usage was not substituted for a total"
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
        "ms": 11661210,
        "note": "measured from first concurrency-check checked_at=2026-11-24T12:30:22Z to wrap-up"
      },
      "baseline": {
        "run_id": "r20261123T121000Z-consume01",
        "source": "caller_declared_ms",
        "value": 2243000
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
      "declared_checks": 6,
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
    "engine": ".specify/scripts/python/run-determination.py",
    "declared_by_caller": [
      "complexity",
      "user_turn_class",
      "unresolved_red",
      "qualification",
      "elapsed_ms",
      "declared_check",
      "green_check"
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
    "id": "cp-r20261124T123022Z-c051",
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
        "observation": "elapsed regressed via source=caller_declared_ms: current=11661210 baseline=2243000",
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
        "observation": "artifact_correctness not_evaluated: failed-set diff not_evaluated added=None, green evidence not_evaluated uncovered=0 declared_checks=6 collected=None reason=no_baseline",
        "signal": {
          "key": "artifact_correctness",
          "direction": "improve"
        },
        "evidence_refs": [],
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
        "observation": "artifact_correctness not_evaluated: failed-set diff not_evaluated added=None, green evidence not_evaluated uncovered=0 declared_checks=6 collected=None reason=no_baseline",
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
