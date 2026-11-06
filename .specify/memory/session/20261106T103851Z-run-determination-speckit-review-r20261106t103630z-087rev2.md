---
id: "20261106T103851Z-run-determination-speckit-review-r20261106t103630z-087rev2"
scope: "session"
source: "/speckit.review"
feature: "087-arch-diagram-docs"
tags: ["run-determination", "r20261106t103630z-087rev2"]
title: "run-determination /speckit.review r20261106t103630z-087rev2"
created: "2026-11-06T10:38:51Z"
summary: "/speckit.review run=r20261106t103630z-087rev2 token=not_evaluated elapsed=not_evaluated artifact=ok satisfaction=not_evaluated"
---

/speckit.review run=r20261106t103630z-087rev2 token=not_evaluated elapsed=not_evaluated artifact=ok satisfaction=not_evaluated

```json
{
  "kind": "speckit.run-determination",
  "schema_version": 1,
  "unit_id": "/speckit.review",
  "unit_type": "command",
  "run_id": "r20261106t103630z-087rev2",
  "feature": "087-arch-diagram-docs",
  "feature_id": "087",
  "determined_at": "2026-11-06T10:38:51Z",
  "settled_at": "2026-11-06T10:54:36Z",
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
      "declared_checks": 6,
      "collected": 124,
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
        ".specify/.tmp/087-review2/current-failed.txt",
        ".specify/specs/087-arch-diagram-docs/baseline-failed.txt",
        ".specify/specs/087-arch-diagram-docs/test-evidence/review-round2.txt"
      ]
    },
    "satisfaction": {
      "verdict": "not_evaluated",
      "reason": "no_user_input",
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
      "tool",
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
    "red_state_input": "caller-declaration",
    "session_store": {
      "tool": "qoder",
      "supported": false,
      "note": "Expected Qoder history at /home/agent/.qoder/projects/-home-agent--local-state-spec-kit-worktrees-087-arch-diagram-docs, but it does not exist.",
      "session_store": "/home/agent/.qoder/projects/-home-agent--local-state-spec-kit-worktrees-087-arch-diagram-docs"
    }
  },
  "change_point": {
    "id": "cp-r20261106t103630z-087rev2",
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
        "reason": "no_user_input",
        "observation": "satisfaction not_evaluated: user_turn_class=no_user_input unresolved_red=false adjacent=False reason=no_user_input",
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
        "observation": "satisfaction not_evaluated: user_turn_class=no_user_input unresolved_red=false adjacent=False reason=no_user_input",
        "parked_via": "none",
        "ref": null
      }
    ]
  }
}
```
