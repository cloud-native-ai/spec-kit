---
id: "20261110T160035Z-run-determination-speckit-review-r20261110t055657z-b095-revi"
scope: "session"
source: "/speckit.review"
feature: "095-superagent-role"
tags: ["run-determination", "r20261110t055657z-b095-review-r2"]
title: "run-determination /speckit.review r20261110T055657Z-b095-review-r2"
created: "2026-11-10T16:00:35Z"
summary: "/speckit.review run=r20261110T055657Z-b095-review-r2 token=not_evaluated elapsed=improved artifact=regressed satisfaction=not_evaluated"
---

/speckit.review run=r20261110T055657Z-b095-review-r2 token=not_evaluated elapsed=improved artifact=regressed satisfaction=not_evaluated

```json
{
  "kind": "speckit.run-determination",
  "schema_version": 1,
  "unit_id": "/speckit.review",
  "unit_type": "command",
  "run_id": "r20261110T055657Z-b095-review-r2",
  "feature": "095-superagent-role",
  "feature_id": "095",
  "determined_at": "2026-11-10T16:00:35Z",
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
      "verdict": "improved",
      "reason": null,
      "signal": {
        "key": "elapsed",
        "direction": "reduce"
      },
      "measurement": {
        "source": "caller_declared_ms",
        "ms": 765000,
        "note": "round-2 review: first review capture 15:47:49Z to wrap-up"
      },
      "baseline": {
        "run_id": "r20261110T055657Z-b095-review",
        "source": "caller_declared_ms",
        "value": 1392000
      },
      "evidence_refs": []
    },
    "artifact_correctness": {
      "verdict": "regressed",
      "reason": null,
      "signal": {
        "key": "artifact_correctness",
        "direction": "improve"
      },
      "declared_checks": 1,
      "collected": null,
      "failed_set_diff": {
        "status": "non_empty",
        "added": [
          "tests/contract/test_goal_migration.py::TestHistoricalFacesArePreserved::test_historical_face_is_not_empty",
          "tests/contract/test_isomorphism_map.py::test_no_second_document_claims_map_ownership",
          "tests/contract/test_script_interface_contract.py::test_c15_the_engine_writes_nothing_inside_the_repository"
        ],
        "added_count": 3,
        "truncated": false
      },
      "green_evidence": {
        "status": "absent",
        "uncovered": [
          "smoke-six-modules"
        ]
      },
      "evidence_refs": [
        ".specify/specs/095-superagent-role/test-evidence/review-r2-closure-suite-names.txt",
        ".specify/specs/095-superagent-role/notes/baseline-failed-names.txt"
      ]
    },
    "satisfaction": {
      "verdict": "not_evaluated",
      "reason": "pending_next_turn",
      "user_turn_class": "no_user_input",
      "unresolved_red": {
        "present": "true",
        "source": "engine_nonzero_exit"
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
      "names_current",
      "names_baseline",
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
    "red_state_input": "caller-declaration",
    "session_store": {
      "tool": "qodercli",
      "supported": false,
      "note": "no resolver exists for this agent CLI"
    }
  },
  "change_point": {
    "id": "cp-r20261110T055657Z-b095-review-r2",
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
        "axis": "artifact_correctness",
        "verdict": "regressed",
        "reason": null,
        "observation": "artifact_correctness regressed: failed-set diff non_empty added=3, green evidence absent uncovered=1 declared_checks=1 collected=None",
        "signal": {
          "key": "artifact_correctness",
          "direction": "improve"
        },
        "evidence_refs": [
          ".specify/specs/095-superagent-role/test-evidence/review-r2-closure-suite-names.txt",
          ".specify/specs/095-superagent-role/notes/baseline-failed-names.txt"
        ],
        "status": "observed"
      },
      {
        "axis": "satisfaction",
        "verdict": "not_evaluated",
        "reason": "pending_next_turn",
        "observation": "satisfaction not_evaluated: user_turn_class=no_user_input unresolved_red=true adjacent=False reason=pending_next_turn",
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
    "trigger_feedback": true,
    "composes_with_should_prompt": true,
    "out_of_scope": [
      {
        "observation": "token_consumption not_evaluated via source=unavailable: current=None baseline=None reason=source_unavailable",
        "parked_via": "none",
        "ref": null
      },
      {
        "observation": "satisfaction not_evaluated: user_turn_class=no_user_input unresolved_red=true adjacent=False reason=pending_next_turn",
        "parked_via": "none",
        "ref": null
      }
    ]
  }
}
```
