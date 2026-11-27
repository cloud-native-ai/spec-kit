---
id: "20261127T075943Z-run-determination-speckit-implement-r20261127t053750z-109a-p"
scope: "session"
source: "/speckit.implement"
feature: "109-prompt-adherence"
tags: ["run-determination", "r20261127t053750z-109a-p4"]
title: "run-determination /speckit.implement r20261127T053750Z-109a-p4"
created: "2026-11-27T07:59:43Z"
summary: "/speckit.implement run=r20261127T053750Z-109a-p4 token=not_evaluated elapsed=not_evaluated artifact=ok satisfaction=not_evaluated"
---

/speckit.implement run=r20261127T053750Z-109a-p4 token=not_evaluated elapsed=not_evaluated artifact=ok satisfaction=not_evaluated

```json
{
  "kind": "speckit.run-determination",
  "schema_version": 1,
  "unit_id": "/speckit.implement",
  "unit_type": "command",
  "run_id": "r20261127T053750Z-109a-p4",
  "feature": "109-prompt-adherence",
  "feature_id": "109",
  "determined_at": "2026-11-27T07:59:43Z",
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
      "verdict": "ok",
      "reason": null,
      "signal": {
        "key": "artifact_correctness",
        "direction": "improve"
      },
      "declared_checks": 4,
      "collected": 10587,
      "failed_set_diff": {
        "status": "empty",
        "added": [],
        "added_count": 0,
        "truncated": false
      },
      "green_evidence": {
        "status": "complete",
        "uncovered": []
      },
      "evidence_refs": [
        ".specify/specs/109-prompt-adherence/final-failed.txt",
        ".specify/specs/109-prompt-adherence/baseline-failed.txt",
        ".specify/specs/109-prompt-adherence/notes/red-first-evidence.md"
      ]
    },
    "satisfaction": {
      "verdict": "not_evaluated",
      "reason": "pending_next_turn",
      "user_turn_class": "no_user_input",
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
    "id": "cp-r20261127T053750Z-109a-p4",
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
        "axis": "satisfaction",
        "verdict": "not_evaluated",
        "reason": "pending_next_turn",
        "observation": "satisfaction not_evaluated: user_turn_class=no_user_input unresolved_red=unknown adjacent=False reason=pending_next_turn",
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
        "observation": "elapsed not_evaluated via source=unavailable: current=None baseline=None reason=source_unavailable",
        "parked_via": "none",
        "ref": null
      },
      {
        "observation": "satisfaction not_evaluated: user_turn_class=no_user_input unresolved_red=unknown adjacent=False reason=pending_next_turn",
        "parked_via": "none",
        "ref": null
      }
    ]
  }
}
```
