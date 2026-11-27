---
id: "20261126T000030Z-run-determination-speckit-review-rdev"
scope: "session"
source: "/speckit.review"
tags: ["run-determination", "r20261126T000030Z-deviant"]
title: "run-determination /speckit.review r20261126T000030Z-deviant"
created: "2026-11-26T00:00:30Z"
summary: "fixture run-determination entry carrying both deviation-class derivations"
---

/speckit.review run=r20261126T000030Z-deviant token=regressed artifact=not_evaluated

```json
{
  "kind": "speckit.run-determination",
  "schema_version": 1,
  "unit_id": "/speckit.review",
  "unit_type": "command",
  "run_id": "r20261126T000030Z-deviant",
  "determined_at": "2026-11-26T00:00:30Z",
  "settled_at": null,
  "axes": {
    "token_consumption": {"verdict": "regressed", "reason": null},
    "elapsed": {"verdict": "unchanged", "reason": null},
    "artifact_correctness": {"verdict": "not_evaluated", "reason": "green_unproven"},
    "satisfaction": {"verdict": "accepted", "reason": null}
  }
}
```