---
id: "20261011T135050Z-run-determination-skill-improve-skills-improve-skills-merge"
scope: "session"
source: "skill:improve-skills"
tags: ["run-determination", "improve-skills-merge-skills-provenance-20261011t1320"]
title: "run-determination skill:improve-skills improve-skills-merge-skills-provenance-20261011T1320"
created: "2026-10-11T13:50:50Z"
summary: "skill:improve-skills run=improve-skills-merge-skills-provenance-20261011T1320 token=not_evaluated elapsed=not_evaluated artifact=not_evaluated satisfaction=not_evaluated"
---

skill:improve-skills run=improve-skills-merge-skills-provenance-20261011T1320 token=not_evaluated elapsed=not_evaluated artifact=not_evaluated satisfaction=not_evaluated

```json
{
  "kind": "speckit.run-determination",
  "schema_version": 1,
  "unit_id": "skill:improve-skills",
  "unit_type": "skill",
  "run_id": "improve-skills-merge-skills-provenance-20261011T1320",
  "feature": null,
  "feature_id": null,
  "determined_at": "2026-10-11T13:50:50Z",
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
        "note": "no token counter available; proxy = 612 insertions across 8 tracked files plus 485 new lines (provenance_check.py, provenance-record.md). findings.json consumed via field projection, never raw-dumped; the 1.1KB allow file read in full as direct evidence; no artifact re-read in full twice."
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
        "note": "wall clock not measured this run; no timer source available"
      },
      "baseline": null,
      "evidence_refs": []
    },
    "artifact_correctness": {
      "verdict": "not_evaluated",
      "reason": "green_unproven",
      "signal": {
        "key": "artifact_correctness",
        "direction": "improve"
      },
      "declared_checks": 7,
      "collected": 2627,
      "failed_set_diff": {
        "status": "empty",
        "added": [],
        "added_count": 0,
        "truncated": false
      },
      "green_evidence": {
        "status": "absent",
        "uncovered": [
          "skill-shape.py exit 0 on merge-skills/SKILL.md",
          "redline-check.py exit 0 on merge-skills/SKILL.md",
          "contract-suite failure-set diff vs clean HEAD worktree = zero regression",
          "provenance_check.py 19-case pressure matrix",
          "coverage_probe.py 12-case legacy regression matrix",
          "baseline round-trip fidelity on 4 real merged sources (807 tokens)",
          "sync-mirrors --check reports no drift"
        ]
      },
      "evidence_refs": [
        "/tmp/names_current.txt",
        "/tmp/names_baseline.txt",
        "/tmp/pv/run_matrix.sh"
      ]
    },
    "satisfaction": {
      "verdict": "not_evaluated",
      "reason": "pending_next_turn",
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
    "id": "cp-improve-skills-merge-skills-provenance-20261011T1320",
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
        "reason": "green_unproven",
        "observation": "artifact_correctness not_evaluated: failed-set diff empty added=0, green evidence absent uncovered=7 declared_checks=7 collected=2627 reason=green_unproven",
        "signal": {
          "key": "artifact_correctness",
          "direction": "improve"
        },
        "evidence_refs": [
          "/tmp/names_current.txt",
          "/tmp/names_baseline.txt",
          "/tmp/pv/run_matrix.sh"
        ],
        "status": "observed"
      },
      {
        "axis": "satisfaction",
        "verdict": "not_evaluated",
        "reason": "pending_next_turn",
        "observation": "satisfaction not_evaluated: user_turn_class=no_user_input unresolved_red=unknown adjacent=False reason=pending_next_turn",
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
        "observation": "artifact_correctness not_evaluated: failed-set diff empty added=0, green evidence absent uncovered=7 declared_checks=7 collected=2627 reason=green_unproven",
        "parked_via": "none",
        "ref": null
      },
      {
        "observation": "satisfaction not_evaluated: user_turn_class=no_user_input unresolved_red=unknown adjacent=False reason=pending_next_turn",
        "parked_via": "none",
        "ref": null
      }
    ]
  }
}
```
