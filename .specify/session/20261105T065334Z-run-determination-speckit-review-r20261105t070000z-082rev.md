---
id: "20261105T065334Z-run-determination-speckit-review-r20261105t070000z-082rev"
scope: "session"
source: "/speckit.review"
feature: "082-self-explanatory-integration"
tags: ["run-determination", "r20261105t070000z-082rev"]
title: "run-determination /speckit.review r20261105t070000z-082rev"
created: "2026-11-05T06:53:34Z"
summary: "/speckit.review run=r20261105t070000z-082rev token=not_evaluated elapsed=not_evaluated artifact=regressed satisfaction=not_evaluated"
---

/speckit.review run=r20261105t070000z-082rev token=not_evaluated elapsed=not_evaluated artifact=regressed satisfaction=not_evaluated

```json
{
  "kind": "speckit.run-determination",
  "schema_version": 1,
  "unit_id": "/speckit.review",
  "unit_type": "command",
  "run_id": "r20261105t070000z-082rev",
  "feature": "082-self-explanatory-integration",
  "feature_id": "082",
  "determined_at": "2026-11-05T06:53:34Z",
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
      "verdict": "regressed",
      "reason": null,
      "signal": {
        "key": "artifact_correctness",
        "direction": "improve"
      },
      "declared_checks": 1,
      "collected": 129,
      "failed_set_diff": {
        "status": "non_empty",
        "added": [
          "# Review-stage targeted test evidence — 2026-11-05",
          "## baseline cross-check",
          "## run 1 — the three modules this stage repaired/touches",
          "## run 2 — the feature's four guard classes + the budget carrier (smoke set + 1)",
          "$ python3 -m pytest tests/contract/test_fast_fail_discipline.py tests/contract/test_constitution_double_landing.py tests/contract/test_instructions_section_propagation.py -q --tb=no",
          "$ python3 -m pytest tests/contract/test_self_explanatory_constitution.py tests/contract/test_instructions_section_propagation.py tests/contract/test_self_explanatory_distribution.py tests/contract/test_self_explanatory_glossary.py tests/contract/test_instructions_size_budget.py -q",
          ".......................................................                  [100%]",
          ".......................F.................................                [100%]",
          "0",
          "1",
          "1 failed, 128 passed in 3.36s",
          "55 passed in 15.99s",
          "=========================== short test summary info ============================",
          "FAILED tests/contract/test_fast_fail_discipline.py::test_g9_total_equals_frozen_baseline",
          "failure name in baseline-failed.txt?",
          "review_stage=review (continuation)",
          "stage_base=b2880fa0",
          "test_a7 present in baseline-failed.txt (must be 0 — it was GREEN at base, so its HEAD failure is NEW)?"
        ],
        "added_count": 18,
        "truncated": false
      },
      "green_evidence": {
        "status": "absent",
        "uncovered": [
          "python3 -m pytest tests/contract/test_fast_fail_discipline.py tests/contract/test_constitution_double_landing.py tests/contract/test_instructions_section_propagation.py -q"
        ]
      },
      "evidence_refs": [
        ".specify/specs/082-self-explanatory-integration/test-evidence/review-stage-checks.md",
        ".specify/specs/082-self-explanatory-integration/baseline-failed.txt",
        ".specify/specs/082-self-explanatory-integration/notes/red-first-evidence.md"
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
    "id": "cp-r20261105t070000z-082rev",
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
        "verdict": "regressed",
        "reason": null,
        "observation": "artifact_correctness regressed: failed-set diff non_empty added=18, green evidence absent uncovered=1 declared_checks=1 collected=129",
        "signal": {
          "key": "artifact_correctness",
          "direction": "improve"
        },
        "evidence_refs": [
          ".specify/specs/082-self-explanatory-integration/test-evidence/review-stage-checks.md",
          ".specify/specs/082-self-explanatory-integration/baseline-failed.txt",
          ".specify/specs/082-self-explanatory-integration/notes/red-first-evidence.md"
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
    "trigger_feedback": true,
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
        "observation": "satisfaction not_evaluated: user_turn_class=no_user_input unresolved_red=false adjacent=False reason=pending_next_turn",
        "parked_via": "none",
        "ref": null
      }
    ]
  }
}
```
