---
id: "20261127T084422Z-run-determination-speckit-implement-r20261127t071500z-111a"
scope: "session"
source: "/speckit.implement"
feature: "111-general-best-practices"
tags: ["run-determination", "r20261127t071500z-111a"]
title: "run-determination /speckit.implement r20261127T071500Z-111a"
created: "2026-11-27T08:44:22Z"
summary: "/speckit.implement run=r20261127T071500Z-111a token=not_evaluated elapsed=not_evaluated artifact=regressed satisfaction=not_evaluated"
---

/speckit.implement run=r20261127T071500Z-111a token=not_evaluated elapsed=not_evaluated artifact=regressed satisfaction=not_evaluated

```json
{
  "kind": "speckit.run-determination",
  "schema_version": 1,
  "unit_id": "/speckit.implement",
  "unit_type": "command",
  "run_id": "r20261127T071500Z-111a",
  "feature": "111-general-best-practices",
  "feature_id": "111",
  "determined_at": "2026-11-27T08:44:22Z",
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
        "note": "token counts not exposed to the executor by the CLI; not evaluated here"
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
        "ms": 415000,
        "note": "P1 package span: workspace snapshot 08:36:51Z to wrap-up 08:43:46Z (executor wall clock)"
      },
      "baseline": {
        "run_id": "r20261030T110000Z-079a",
        "source": "unavailable",
        "value": null
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
      "declared_checks": 6,
      "collected": 5,
      "failed_set_diff": {
        "status": "non_empty",
        "added": [
          "tests/contract/test_mirror_parity_suite.py::test_mirror_file_byte_identical[shared/best-practices/README.md->.specify/shared/best-practices/README.md]"
        ],
        "added_count": 1,
        "truncated": false
      },
      "green_evidence": {
        "status": "complete",
        "uncovered": []
      },
      "evidence_refs": [
        ".specify/specs/111-general-best-practices/test-evidence/p1-parity-names.txt",
        ".specify/specs/111-general-best-practices/baseline-failed.txt",
        ".specify/specs/111-general-best-practices/notes/red-first-evidence.md"
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
      "elapsed_ms",
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
    "id": "cp-r20261127T071500Z-111a",
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
        "observation": "elapsed not_evaluated via source=caller_declared_ms: current=415000 baseline=None reason=not_comparable",
        "signal": {
          "key": "elapsed",
          "direction": "reduce"
        },
        "evidence_refs": [],
        "status": "observed"
      },
      {
        "axis": "artifact_correctness",
        "verdict": "regressed",
        "reason": null,
        "observation": "artifact_correctness regressed: failed-set diff non_empty added=1, green evidence complete uncovered=0 declared_checks=6 collected=5",
        "signal": {
          "key": "artifact_correctness",
          "direction": "improve"
        },
        "evidence_refs": [
          ".specify/specs/111-general-best-practices/test-evidence/p1-parity-names.txt",
          ".specify/specs/111-general-best-practices/baseline-failed.txt",
          ".specify/specs/111-general-best-practices/notes/red-first-evidence.md"
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
        "observation": "elapsed not_evaluated via source=caller_declared_ms: current=415000 baseline=None reason=not_comparable",
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
