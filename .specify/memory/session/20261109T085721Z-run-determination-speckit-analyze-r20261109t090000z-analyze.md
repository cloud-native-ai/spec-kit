---
id: "20261109T085721Z-run-determination-speckit-analyze-r20261109t090000z-analyze"
scope: "session"
source: "/speckit.analyze"
feature: "092-goal-team-parallel"
tags: ["run-determination", "r20261109t090000z-analyze-repair2"]
title: "run-determination /speckit.analyze r20261109T090000Z-analyze-repair2"
created: "2026-11-09T08:57:21Z"
summary: "/speckit.analyze run=r20261109T090000Z-analyze-repair2 token=not_evaluated elapsed=not_evaluated artifact=not_evaluated satisfaction=not_evaluated"
---

/speckit.analyze run=r20261109T090000Z-analyze-repair2 token=not_evaluated elapsed=not_evaluated artifact=not_evaluated satisfaction=not_evaluated

```json
{
  "kind": "speckit.run-determination",
  "schema_version": 1,
  "unit_id": "/speckit.analyze",
  "unit_type": "command",
  "run_id": "r20261109T090000Z-analyze-repair2",
  "feature": "092-goal-team-parallel",
  "feature_id": "092",
  "determined_at": "2026-11-09T08:57:21Z",
  "settled_at": "2026-11-10T14:07:06Z",
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
        "note": "not measurable from this subagent: no token sensor in scope; subagent run"
      },
      "baseline": null,
      "evidence_refs": [
        ".specify/specs/092-goal-team-parallel/test-evidence/analyze-repair2-gates-tasks.txt"
      ]
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
        "ms": 0,
        "note": "not measured by this subagent; wall clock not instrumented"
      },
      "baseline": {
        "run_id": "r20261106T090000Z-086a-r3",
        "source": "unavailable",
        "value": null
      },
      "evidence_refs": [
        ".specify/specs/092-goal-team-parallel/test-evidence/analyze-repair2-gates-tasks.txt"
      ]
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
      "evidence_refs": [
        ".specify/specs/092-goal-team-parallel/test-evidence/analyze-repair2-gates-tasks.txt"
      ]
    },
    "satisfaction": {
      "verdict": "not_evaluated",
      "reason": "no_user_input",
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
      "session_file",
      "declared_check",
      "green_check",
      "red_first_refs",
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
    "id": "cp-r20261109T090000Z-analyze-repair2",
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
        "evidence_refs": [
          ".specify/specs/092-goal-team-parallel/test-evidence/analyze-repair2-gates-tasks.txt"
        ],
        "status": "observed"
      },
      {
        "axis": "elapsed",
        "verdict": "not_evaluated",
        "reason": "not_comparable",
        "observation": "elapsed not_evaluated via source=caller_declared_ms: current=0 baseline=None reason=not_comparable",
        "signal": {
          "key": "elapsed",
          "direction": "reduce"
        },
        "evidence_refs": [
          ".specify/specs/092-goal-team-parallel/test-evidence/analyze-repair2-gates-tasks.txt"
        ],
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
        "evidence_refs": [
          ".specify/specs/092-goal-team-parallel/test-evidence/analyze-repair2-gates-tasks.txt"
        ],
        "status": "observed"
      },
      {
        "axis": "satisfaction",
        "verdict": "not_evaluated",
        "reason": "no_user_input",
        "observation": "satisfaction not_evaluated: user_turn_class=no_user_input unresolved_red=unknown adjacent=False reason=no_user_input",
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
        "observation": "elapsed not_evaluated via source=caller_declared_ms: current=0 baseline=None reason=not_comparable",
        "parked_via": "none",
        "ref": null
      },
      {
        "observation": "artifact_correctness not_evaluated: failed-set diff not_evaluated added=None, green evidence not_evaluated uncovered=0 declared_checks=6 collected=None reason=no_baseline",
        "parked_via": "none",
        "ref": null
      },
      {
        "observation": "satisfaction not_evaluated: user_turn_class=no_user_input unresolved_red=unknown adjacent=False reason=no_user_input",
        "parked_via": "none",
        "ref": null
      }
    ]
  }
}
```
