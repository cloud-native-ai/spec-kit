---
id: "20261126T131433Z-run-determination-speckit-review-r20261126t071500z-108a"
scope: "session"
source: "/speckit.review"
feature: "108-team-view-degradation"
tags: ["run-determination", "r20261126t071500z-108a"]
title: "run-determination /speckit.review r20261126T071500Z-108a"
created: "2026-11-26T13:14:33Z"
summary: "/speckit.review run=r20261126T071500Z-108a token=not_evaluated elapsed=not_evaluated artifact=not_evaluated satisfaction=accepted"
---

/speckit.review run=r20261126T071500Z-108a token=not_evaluated elapsed=not_evaluated artifact=not_evaluated satisfaction=accepted

```json
{
  "kind": "speckit.run-determination",
  "schema_version": 1,
  "unit_id": "/speckit.review",
  "unit_type": "command",
  "run_id": "r20261126T071500Z-108a",
  "feature": "108-team-view-degradation",
  "feature_id": "108",
  "determined_at": "2026-11-26T13:14:33Z",
  "settled_at": "2026-11-27T10:29:00Z",
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
        "ms": 584000,
        "note": "review span: first review artifact 2026-11-26T13:04:49Z to this wrap-up; the state spine's stage field still reads implement, so no stage-start anchor exists"
      },
      "baseline": {
        "run_id": "r20261125T022857Z-06dd",
        "source": "unavailable",
        "value": null
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
      "declared_checks": 0,
      "collected": 149,
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
        ".specify/specs/108-team-view-degradation/test-evidence/review-targeted-failed.txt",
        ".specify/specs/108-team-view-degradation/baseline-failed.txt"
      ]
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
      "names_current",
      "names_baseline",
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
    "id": "cp-r20261126T071500Z-108a",
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
        "observation": "elapsed not_evaluated via source=caller_declared_ms: current=584000 baseline=None reason=not_comparable",
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
        "observation": "artifact_correctness not_evaluated: failed-set diff not_evaluated added=None, green evidence not_evaluated uncovered=0 declared_checks=0 collected=149 reason=no_declared_checks",
        "signal": {
          "key": "artifact_correctness",
          "direction": "improve"
        },
        "evidence_refs": [
          ".specify/specs/108-team-view-degradation/test-evidence/review-targeted-failed.txt",
          ".specify/specs/108-team-view-degradation/baseline-failed.txt"
        ],
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
        "observation": "elapsed not_evaluated via source=caller_declared_ms: current=584000 baseline=None reason=not_comparable",
        "parked_via": "none",
        "ref": null
      },
      {
        "observation": "artifact_correctness not_evaluated: failed-set diff not_evaluated added=None, green evidence not_evaluated uncovered=0 declared_checks=0 collected=149 reason=no_declared_checks",
        "parked_via": "none",
        "ref": null
      }
    ]
  }
}
```
