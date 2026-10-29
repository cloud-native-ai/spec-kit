---
id: "20261028T160359Z-run-determination-speckit-requirements-r20261028t132000z-074"
scope: "session"
source: "/speckit.requirements"
feature: "074a-authorized-routing"
tags: ["run-determination", "r20261028t132000z-074d"]
title: "run-determination /speckit.requirements r20261028T132000Z-074d"
created: "2026-10-28T16:03:59Z"
summary: "/speckit.requirements run=r20261028T132000Z-074d token=not_evaluated elapsed=not_evaluated artifact=not_evaluated satisfaction=not_evaluated"
---

/speckit.requirements run=r20261028T132000Z-074d token=not_evaluated elapsed=not_evaluated artifact=not_evaluated satisfaction=not_evaluated

```json
{
  "kind": "speckit.run-determination",
  "schema_version": 1,
  "unit_id": "/speckit.requirements",
  "unit_type": "command",
  "run_id": "r20261028T132000Z-074d",
  "feature": "074a-authorized-routing",
  "feature_id": "074",
  "determined_at": "2026-10-28T16:03:59Z",
  "settled_at": null,
  "complexity": "complex",
  "qualification": "partial",
  "axes": {
    "token_consumption": {
      "verdict": "not_evaluated",
      "reason": "unqualified_run",
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
        "note": "not measured: no session store access from this run"
      },
      "baseline": null,
      "evidence_refs": []
    },
    "elapsed": {
      "verdict": "not_evaluated",
      "reason": "unqualified_run",
      "signal": {
        "key": "elapsed",
        "direction": "reduce"
      },
      "measurement": {
        "source": "caller_declared_ms",
        "ms": 309000,
        "note": "unattended slice requirements stage: dispatch to commit-attempt"
      },
      "baseline": {
        "run_id": "r20261027T061144Z-a3ec",
        "source": "unavailable",
        "value": null
      },
      "evidence_refs": []
    },
    "artifact_correctness": {
      "verdict": "not_evaluated",
      "reason": "unqualified_run",
      "signal": {
        "key": "artifact_correctness",
        "direction": "improve"
      },
      "declared_checks": 2,
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
      "reason": "unqualified_run",
      "user_turn_class": "no_user_input",
      "unresolved_red": {
        "present": "true",
        "source": "surfaced_anomaly_unanswered"
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
      "declared_check",
      "green_check",
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
    "id": "cp-r20261028T132000Z-074d",
    "clean": false,
    "findings": [
      {
        "axis": "token_consumption",
        "verdict": "not_evaluated",
        "reason": "unqualified_run",
        "observation": "token_consumption not_evaluated via source=unavailable: current=None baseline=None reason=unqualified_run",
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
        "reason": "unqualified_run",
        "observation": "elapsed not_evaluated via source=caller_declared_ms: current=309000 baseline=None reason=unqualified_run",
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
        "reason": "unqualified_run",
        "observation": "artifact_correctness not_evaluated: failed-set diff not_evaluated added=None, green evidence not_evaluated uncovered=0 declared_checks=2 collected=None reason=unqualified_run",
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
        "reason": "unqualified_run",
        "observation": "satisfaction not_evaluated: user_turn_class=no_user_input unresolved_red=true adjacent=False reason=unqualified_run",
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
        "observation": "token_consumption not_evaluated via source=unavailable: current=None baseline=None reason=unqualified_run",
        "parked_via": "none",
        "ref": null
      },
      {
        "observation": "elapsed not_evaluated via source=caller_declared_ms: current=309000 baseline=None reason=unqualified_run",
        "parked_via": "none",
        "ref": null
      },
      {
        "observation": "artifact_correctness not_evaluated: failed-set diff not_evaluated added=None, green evidence not_evaluated uncovered=0 declared_checks=2 collected=None reason=unqualified_run",
        "parked_via": "none",
        "ref": null
      },
      {
        "observation": "satisfaction not_evaluated: user_turn_class=no_user_input unresolved_red=true adjacent=False reason=unqualified_run",
        "parked_via": "none",
        "ref": null
      }
    ]
  }
}
```
