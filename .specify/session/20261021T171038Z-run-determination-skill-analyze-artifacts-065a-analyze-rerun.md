---
id: "20261021T171038Z-run-determination-skill-analyze-artifacts-065a-analyze-rerun"
scope: "session"
source: "skill:analyze-artifacts"
tags: ["run-determination", "065a-analyze-rerun-20261022"]
title: "run-determination skill:analyze-artifacts 065a-analyze-rerun-20261022"
created: "2026-10-21T17:10:38Z"
summary: "skill:analyze-artifacts run=065a-analyze-rerun-20261022 token=not_evaluated elapsed=not_evaluated artifact=ok satisfaction=not_evaluated"
---

skill:analyze-artifacts run=065a-analyze-rerun-20261022 token=not_evaluated elapsed=not_evaluated artifact=ok satisfaction=not_evaluated

```json
{
  "kind": "speckit.run-determination",
  "schema_version": 1,
  "unit_id": "skill:analyze-artifacts",
  "unit_type": "skill",
  "run_id": "065a-analyze-rerun-20261022",
  "feature": null,
  "feature_id": null,
  "determined_at": "2026-10-21T17:10:38Z",
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
      "declared_checks": 1,
      "collected": 60,
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
        "/tmp/analyze-065a-green/current-failed.txt",
        "/tmp/analyze-065a-green/baseline-failed.txt",
        "/tmp/analyze-065a-green/evidence.txt"
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
      "tool",
      "names_current",
      "names_baseline",
      "declared_check",
      "green_check",
      "red_first_refs",
      "collected"
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
      "supported": true,
      "note": "Qoder CLI JSONL session store.",
      "session_store": "/Users/liuqiming.lqm/.qoder/projects/-Users-liuqiming-lqm-project-cloud-native-ai-spec-kit"
    }
  },
  "change_point": {
    "id": "cp-065a-analyze-rerun-20261022",
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
        "observation": "satisfaction not_evaluated: user_turn_class=no_user_input unresolved_red=false adjacent=False reason=pending_next_turn",
        "parked_via": "none",
        "ref": null
      }
    ]
  }
}
```
