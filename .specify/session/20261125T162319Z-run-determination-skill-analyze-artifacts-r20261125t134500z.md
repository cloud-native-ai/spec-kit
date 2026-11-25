---
id: "20261125T162319Z-run-determination-skill-analyze-artifacts-r20261125t134500z"
scope: "session"
source: "skill:analyze-artifacts"
feature: "107-decision-governance"
tags: ["run-determination", "r20261125t134500z-107a"]
title: "run-determination skill:analyze-artifacts r20261125T134500Z-107a"
created: "2026-11-25T16:23:19Z"
summary: "skill:analyze-artifacts run=r20261125T134500Z-107a token=not_evaluated elapsed=not_evaluated artifact=not_evaluated satisfaction=not_evaluated"
---

skill:analyze-artifacts run=r20261125T134500Z-107a token=not_evaluated elapsed=not_evaluated artifact=not_evaluated satisfaction=not_evaluated

```json
{
  "kind": "speckit.run-determination",
  "schema_version": 1,
  "unit_id": "skill:analyze-artifacts",
  "unit_type": "skill",
  "run_id": "r20261125T134500Z-107a",
  "feature": "107-decision-governance",
  "feature_id": "107",
  "determined_at": "2026-11-25T16:23:19Z",
  "settled_at": "2026-11-25T16:37:48Z",
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
        "note": "session JSONL not exposed to this dispatch; token axis not evaluated"
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
        "note": "caller did not measure a wall-clock start; elapsed not evaluated"
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
        ".specify/specs/107-decision-governance/test-evidence/analyze-repair-validate-requirements.txt",
        ".specify/specs/107-decision-governance/test-evidence/analyze-repair-pre-analyze-requirements.txt",
        ".specify/specs/107-decision-governance/test-evidence/analyze-repair-pre-analyze-plan.txt",
        ".specify/specs/107-decision-governance/test-evidence/analyze-repair-pre-analyze-tasks.txt",
        ".specify/specs/107-decision-governance/test-evidence/analyze-repair-validate-tasks.txt",
        ".specify/specs/107-decision-governance/test-evidence/analyze-repair-decomposition.txt"
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
      "tool",
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
    "red_state_input": "caller-declaration",
    "session_store": {
      "tool": "qodercli",
      "supported": false,
      "note": "no resolver exists for this agent CLI"
    }
  },
  "change_point": {
    "id": "cp-r20261125T134500Z-107a",
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
        "observation": "artifact_correctness not_evaluated: failed-set diff not_evaluated added=None, green evidence not_evaluated uncovered=0 declared_checks=6 collected=None reason=no_baseline",
        "signal": {
          "key": "artifact_correctness",
          "direction": "improve"
        },
        "evidence_refs": [
          ".specify/specs/107-decision-governance/test-evidence/analyze-repair-validate-requirements.txt",
          ".specify/specs/107-decision-governance/test-evidence/analyze-repair-pre-analyze-requirements.txt",
          ".specify/specs/107-decision-governance/test-evidence/analyze-repair-pre-analyze-plan.txt",
          ".specify/specs/107-decision-governance/test-evidence/analyze-repair-pre-analyze-tasks.txt",
          ".specify/specs/107-decision-governance/test-evidence/analyze-repair-validate-tasks.txt",
          ".specify/specs/107-decision-governance/test-evidence/analyze-repair-decomposition.txt"
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
        "observation": "elapsed not_evaluated via source=unavailable: current=None baseline=None reason=source_unavailable",
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
