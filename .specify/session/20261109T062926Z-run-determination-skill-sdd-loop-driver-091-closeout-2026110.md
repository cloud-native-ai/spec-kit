---
id: "20261109T062926Z-run-determination-skill-sdd-loop-driver-091-closeout-2026110"
scope: "session"
source: "skill:sdd-loop-driver"
tags: ["run-determination", "091-closeout-20261109t062926z"]
title: "run-determination skill:sdd-loop-driver 091-closeout-20261109T062926Z"
created: "2026-11-09T06:29:26Z"
summary: "skill:sdd-loop-driver run=091-closeout-20261109T062926Z token=not_evaluated elapsed=not_evaluated artifact=regressed satisfaction=accepted"
---

skill:sdd-loop-driver run=091-closeout-20261109T062926Z token=not_evaluated elapsed=not_evaluated artifact=regressed satisfaction=accepted

```json
{
  "kind": "speckit.run-determination",
  "schema_version": 1,
  "unit_id": "skill:sdd-loop-driver",
  "unit_type": "skill",
  "run_id": "091-closeout-20261109T062926Z",
  "feature": null,
  "feature_id": null,
  "determined_at": "2026-11-09T06:29:26Z",
  "settled_at": "2026-11-09T08:23:26Z",
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
        "note": "token usage not instrumented; the 091 run spans the SDD chain + a 3-package concurrent worktree fix loop"
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
        "note": "wall clock not instrumented; final serial suite 580s"
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
      "declared_checks": 3,
      "collected": 8110,
      "failed_set_diff": {
        "status": "non_empty",
        "added": [
          "FAILED tests/contract/test_compile_embeds.py::test_compile_embeds_check_clean_and_drift",
          "FAILED tests/contract/test_compile_embeds.py::test_compile_embeds_determinism",
          "FAILED tests/contract/test_compile_embeds.py::test_compile_embeds_zero_handler_no_section",
          "FAILED tests/contract/test_compile_embeds.py::test_compiled_form_contract - j...",
          "FAILED tests/contract/test_compile_reconcile_guards.py::test_clean_tree_check_is_green",
          "FAILED tests/contract/test_compile_reconcile_guards.py::test_illegal_action_exits_2_naming_handler",
          "FAILED tests/contract/test_compile_reconcile_guards.py::test_missing_handler_line_is_structural_exit_2",
          "FAILED tests/contract/test_compile_reconcile_guards.py::test_order_conflict_exits_2",
          "FAILED tests/contract/test_compile_reconcile_guards.py::test_orphan_handler_line_is_structural_exit_2",
          "FAILED tests/contract/test_compile_reconcile_guards.py::test_stale_render_after_registry_change_is_exit_1",
          "FAILED tests/contract/test_compile_reconcile_guards.py::test_wording_hit_refuses_the_write",
          "FAILED tests/contract/test_engine_face_contract.py::test_c20_convention_line_rendered_once_verbatim",
          "FAILED tests/contract/test_engine_face_contract.py::test_c20_face_renders_required_and_source_placeholders",
          "FAILED tests/contract/test_engine_face_contract.py::test_c20_no_placeholder_free_section_carries_no_convention",
          "FAILED tests/contract/test_engine_face_contract.py::test_c21_rendered_flags_are_exactly_the_manifest_set",
          "FAILED tests/contract/test_engine_face_contract.py::test_c22_missing_manifest_fails_the_compile_loudly"
        ],
        "added_count": 16,
        "truncated": false
      },
      "green_evidence": {
        "status": "absent",
        "uncovered": [
          "closure-acceptance-check",
          "closeout-contract-tests"
        ]
      },
      "evidence_refs": [
        ".specify/specs/091-auto-git-closeout/test-evidence/closure-final-failed.txt",
        ".specify/specs/091-auto-git-closeout/test-evidence/baseline-failed.txt"
      ]
    },
    "satisfaction": {
      "verdict": "accepted",
      "reason": null,
      "user_turn_class": "continuation_non_negative",
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
      "names_current",
      "names_baseline",
      "declared_check",
      "green_check",
      "collected"
    ],
    "lanes_read": {
      "session": "available",
      "user_input": "in_context",
      "evidence": "stale"
    },
    "evidence_digests": [],
    "honesty_boundary": [
      "the unresolved-red state is declared by the caller, never derived (§ 5.4)",
      "a wrap-up that never called determine leaves no trace: absence of a record is not evidence of a clean run (§ 4)"
    ],
    "red_state_input": "caller-declaration"
  },
  "change_point": {
    "id": "cp-091-closeout-20261109T062926Z",
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
        "observation": "artifact_correctness regressed: failed-set diff non_empty added=16, green evidence absent uncovered=2 declared_checks=3 collected=8110",
        "signal": {
          "key": "artifact_correctness",
          "direction": "improve"
        },
        "evidence_refs": [
          ".specify/specs/091-auto-git-closeout/test-evidence/closure-final-failed.txt",
          ".specify/specs/091-auto-git-closeout/test-evidence/baseline-failed.txt"
        ],
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
      }
    ]
  }
}
```
