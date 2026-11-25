---
id: "20261019T164352Z-run-determination-speckit-instructions-speckit-instructions"
scope: "session"
source: "/speckit.instructions"
feature: "063-review-p1-governance"
tags: ["run-determination", "speckit-instructions-20261019t164340z"]
title: "run-determination /speckit.instructions speckit-instructions-20261019T164340Z"
created: "2026-10-19T16:43:52Z"
summary: "/speckit.instructions run=speckit-instructions-20261019T164340Z token=not_evaluated elapsed=not_evaluated artifact=not_evaluated satisfaction=not_evaluated"
---

/speckit.instructions run=speckit-instructions-20261019T164340Z token=not_evaluated elapsed=not_evaluated artifact=not_evaluated satisfaction=not_evaluated

```json
{
  "kind": "speckit.run-determination",
  "schema_version": 1,
  "unit_id": "/speckit.instructions",
  "unit_type": "command",
  "run_id": "speckit-instructions-20261019T164340Z",
  "feature": "063-review-p1-governance",
  "feature_id": null,
  "determined_at": "2026-10-19T16:43:52Z",
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
      "verdict": "not_evaluated",
      "reason": "no_baseline",
      "signal": {
        "key": "artifact_correctness",
        "direction": "improve"
      },
      "declared_checks": 1,
      "collected": 12,
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
      "evidence_refs": [
        ".specify/specs/063-review-p1-governance/verification.md"
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
    "engine": ".specify/scripts/python/run-determination.py",
    "declared_by_caller": [
      "complexity",
      "user_turn_class",
      "unresolved_red",
      "qualification",
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
    "id": "cp-speckit-instructions-20261019T164340Z",
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
        "reason": "no_baseline",
        "observation": "artifact_correctness not_evaluated: failed-set diff not_evaluated added=None, green evidence not_evaluated uncovered=0 declared_checks=1 collected=12 reason=no_baseline",
        "signal": {
          "key": "artifact_correctness",
          "direction": "improve"
        },
        "evidence_refs": [
          ".specify/specs/063-review-p1-governance/verification.md"
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
        "observation": "elapsed not_evaluated via source=unavailable: current=None baseline=None reason=source_unavailable",
        "parked_via": "none",
        "ref": null
      },
      {
        "observation": "artifact_correctness not_evaluated: failed-set diff not_evaluated added=None, green evidence not_evaluated uncovered=0 declared_checks=1 collected=12 reason=no_baseline",
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
