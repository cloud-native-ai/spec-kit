---
id: "20261125T000000Z-run-determination-speckit-plan-multi-b"
scope: "session"
source: "/speckit.plan"
tags: ["run-determination", "r20261125T000000Z-multi-b"]
title: "run-determination /speckit.plan r20261125T000000Z-multi-b"
created: "2026-11-25T00:00:00Z"
summary: "multi-run fixture: determined_at falls exactly on the window since bound (included)"
---

/speckit.plan run=r20261125T000000Z-multi-b token=unchanged elapsed=unchanged artifact=ok satisfaction=accepted

```json
{
  "kind": "speckit.run-determination",
  "schema_version": 1,
  "unit_id": "/speckit.plan",
  "unit_type": "command",
  "run_id": "r20261125T000000Z-multi-b",
  "determined_at": "2026-11-25T00:00:00Z",
  "settled_at": null,
  "axes": {
    "token_consumption": {"verdict": "unchanged", "reason": null},
    "elapsed": {"verdict": "unchanged", "reason": null},
    "artifact_correctness": {"verdict": "ok", "reason": null},
    "satisfaction": {"verdict": "accepted", "reason": null}
  }
}
```