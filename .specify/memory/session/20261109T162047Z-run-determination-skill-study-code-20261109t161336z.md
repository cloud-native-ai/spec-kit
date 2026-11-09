---
id: "20261109T162047Z-run-determination-skill-study-code-20261109t161336z"
scope: "session"
source: "skill:study-code"
tags: ["run-determination", "20261109t161336z"]
title: "run-determination skill:study-code 20261109T161336Z"
created: "2026-11-09T16:20:47Z"
summary: "skill:study-code run=20261109T161336Z token=not_evaluated elapsed=not_evaluated artifact=regressed satisfaction=accepted"
---

skill:study-code run=20261109T161336Z token=not_evaluated elapsed=not_evaluated artifact=regressed satisfaction=accepted

```json
{
  "kind": "speckit.run-determination",
  "schema_version": 1,
  "unit_id": "skill:study-code",
  "unit_type": "skill",
  "run_id": "20261109T161336Z",
  "feature": null,
  "feature_id": null,
  "determined_at": "2026-11-09T16:20:47Z",
  "settled_at": "2026-11-09T16:21:17Z",
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
      "evidence_refs": [
        "/home/agent/.qoder/projects/-storage-project-cloud-native-ai-spec-kit/111683d8-20e5-4ebc-ad31-8949e7cf8a78.jsonl"
      ]
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
        "note": "approx 45-60 min wall clock; single-session interactive run"
      },
      "baseline": null,
      "evidence_refs": [
        "/home/agent/.qoder/projects/-storage-project-cloud-native-ai-spec-kit/111683d8-20e5-4ebc-ad31-8949e7cf8a78.jsonl"
      ]
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
          "references/architect-analysis-guide.md",
          "references/deployment-analysis-guide.md",
          "references/git-analysis-guide.md",
          "references/module-analysis-guide.md",
          "references/tech-stack-analysis-guide.md",
          "references/uml-visualization-guide.md",
          "skills/external/study-code/SKILL.md"
        ],
        "added_count": 7,
        "truncated": false
      },
      "green_evidence": {
        "status": "absent",
        "uncovered": [
          "self-check over docs/overview.md (paths+anchors)"
        ]
      },
      "evidence_refs": [
        ".specify/.tmp/study-code/names-current.txt",
        ".specify/.tmp/study-code/names-baseline.txt",
        ".specify/.tmp/study-code/red-first.txt"
      ]
    },
    "satisfaction": {
      "verdict": "accepted",
      "reason": null,
      "user_turn_class": "topic_change",
      "unresolved_red": {
        "present": "false",
        "source": "none"
      },
      "adjacent": true,
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
      "session_file",
      "tool",
      "names_current",
      "names_baseline",
      "declared_check",
      "green_check",
      "red_first_refs"
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
    "id": "cp-20261109T161336Z",
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
        "evidence_refs": [
          "/home/agent/.qoder/projects/-storage-project-cloud-native-ai-spec-kit/111683d8-20e5-4ebc-ad31-8949e7cf8a78.jsonl"
        ],
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
        "evidence_refs": [
          "/home/agent/.qoder/projects/-storage-project-cloud-native-ai-spec-kit/111683d8-20e5-4ebc-ad31-8949e7cf8a78.jsonl"
        ],
        "status": "observed"
      },
      {
        "axis": "artifact_correctness",
        "verdict": "regressed",
        "reason": null,
        "observation": "artifact_correctness regressed: failed-set diff non_empty added=7, green evidence absent uncovered=1 declared_checks=1 collected=None",
        "signal": {
          "key": "artifact_correctness",
          "direction": "improve"
        },
        "evidence_refs": [
          ".specify/.tmp/study-code/names-current.txt",
          ".specify/.tmp/study-code/names-baseline.txt",
          ".specify/.tmp/study-code/red-first.txt"
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
