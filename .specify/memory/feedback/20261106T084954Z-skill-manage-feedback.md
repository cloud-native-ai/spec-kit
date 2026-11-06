---
id: "20261106T084954Z-skill-manage-feedback"
unit_id: "skill:manage-feedback"
unit_type: "skill"
run_id: "r20261106T084500Z-feedback"
scope: "local"
probe: "skill-manage-feedback-wrapup"
kind: "internal"
slice: "skills"
partial: false
created: "2026-11-06T08:49:54Z"
summary: "Digest execution: framework hat, Path A; two introspection reports (5 + 33 entries), 22 processed, 11 ignored, 16 backlog rows; the engine actions the skill names (probes/map) were absent and the defa"
---

## Review
Digest execution: framework hat, Path A; two introspection reports (5 + 33 entries), 22 processed, 11 ignored, 16 backlog rows; the engine actions the skill names (probes/map) were absent and the default list page truncated the first scope.

## Optimization Points
- feedback-utils.py --action list --disposition open defaults to a 5-row page and the routing flow / A3 text does not pin --limit 0, so a digest can silently scope 5 of 38 open entries (this run did, then recovered).
- manage-feedback's routing flow calls --action probes and --action map, which feedback-utils.py does not implement; the probe truth source lives in probe-utils.py, so the documented inventory step fails on the engine it names.
- The introspection report schema has no disposition channel for Excluded entries; closing them after --confirm requires one dispose call per entry (11 in this run), and a missed one leaves the store open with a confirmed report.
- introspect-register validates structural violations one at a time in places, so fixing a report can take several round trips; a single consolidated verdict would shorten the loop.
- The report parser rejects any non-field line inside a finding block, so evidence anchors must be crammed into one line per field; a bounded notes field would keep the strict schema while improving readability.
