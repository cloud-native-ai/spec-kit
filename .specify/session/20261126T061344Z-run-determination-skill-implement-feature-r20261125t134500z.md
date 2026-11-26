---
id: "20261126T061344Z-run-determination-skill-implement-feature-r20261125t134500z"
scope: "session"
source: "skill:implement-feature"
feature: "107-decision-governance"
tags: ["run-determination", "r20261125t134500z-107a"]
title: "run-determination skill:implement-feature r20261125T134500Z-107a"
created: "2026-11-26T06:13:44Z"
summary: "skill:implement-feature run=r20261125T134500Z-107a token=not_evaluated elapsed=regressed artifact=ok satisfaction=not_evaluated"
---

skill:implement-feature run=r20261125T134500Z-107a token=not_evaluated elapsed=regressed artifact=ok satisfaction=not_evaluated

```json
{
  "kind": "speckit.run-determination",
  "schema_version": 1,
  "unit_id": "skill:implement-feature",
  "unit_type": "skill",
  "run_id": "r20261125T134500Z-107a",
  "feature": "107-decision-governance",
  "feature_id": "107",
  "determined_at": "2026-11-26T06:13:44Z",
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
        "note": "qualitative only: five package verdict JSONs read in full (~78 KB) for coverage; no session-store resolver for qodercli; no numeric count fabricated"
      },
      "baseline": null,
      "evidence_refs": []
    },
    "elapsed": {
      "verdict": "regressed",
      "reason": null,
      "signal": {
        "key": "elapsed",
        "direction": "reduce"
      },
      "measurement": {
        "source": "caller_declared_ms",
        "ms": 6268542,
        "note": "measured from the stage's first commit 98bf3328a (2026-11-26T04:29:16Z) to this integrate close-out"
      },
      "baseline": {
        "run_id": "r20261125T022857Z-06dd",
        "source": "caller_declared_ms",
        "value": 1078000
      },
      "evidence_refs": []
    },
    "artifact_correctness": {
      "verdict": "ok",
      "reason": null,
      "signal": {
        "key": "artifact_correctness",
        "direction": "improve"
      },
      "declared_checks": 12,
      "collected": 246,
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
        ".specify/specs/107-decision-governance/test-evidence/closure-failed-names-preservation-sweep.txt",
        ".specify/specs/107-decision-governance/baseline-failed.txt",
        ".specify/specs/107-decision-governance/notes/red-first-evidence.md",
        ".specify/specs/107-decision-governance/test-evidence/us1-red-first.txt",
        ".specify/specs/107-decision-governance/test-evidence/us2-red-first.txt",
        ".specify/specs/107-decision-governance/test-evidence/us3-red-first.txt",
        ".specify/specs/107-decision-governance/test-evidence/us4-red-first.txt",
        ".specify/specs/107-decision-governance/test-evidence/us5-red-first.txt",
        ".specify/specs/107-decision-governance/test-evidence/us6-red-first.txt"
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
      "tool",
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
        "verdict": "regressed",
        "reason": null,
        "observation": "elapsed regressed via source=caller_declared_ms: current=6268542 baseline=1078000",
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
        "observation": "satisfaction not_evaluated: user_turn_class=no_user_input unresolved_red=false adjacent=False reason=pending_next_turn",
        "parked_via": "none",
        "ref": null
      }
    ]
  }
}
```
