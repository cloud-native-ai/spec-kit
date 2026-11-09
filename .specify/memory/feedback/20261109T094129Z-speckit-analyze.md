---
id: "20261109T094129Z-speckit-analyze"
unit_id: "/speckit.analyze"
unit_type: "command"
run_id: "r20261109T080000Z-093-analyze-repair"
scope: "local"
probe: "speckit-analyze-wrapup"
kind: "internal"
slice: "commands"
feature: "093-concurrency-by-default"
partial: false
created: "2026-11-09T09:41:29Z"
summary: "analyze-repair closed the CRITICAL and all three HIGH findings in one mechanical pass (FR lane 25/33 -> 35/35) and encoded two dated user rulings as first-class requirements (FR-034 analyze-stage conc"
---

## Review
analyze-repair closed the CRITICAL and all three HIGH findings in one mechanical pass (FR lane 25/33 -> 35/35) and encoded two dated user rulings as first-class requirements (FR-034 analyze-stage concurrency, FR-035 FORK mechanism) with clause/plan/task attribution. Friction: validate-requirements strips code spans so the FR-031 corruption validated silently for three stages - the same filter-not-totality family as the blockquote observation; pre-analyze-check and validate-requirements disagree on the definition-row syntax (annotation before the colon invisible to one), so a new FR needed two format passes; pre-analyze count-claim flags dated records that legitimately hold pre-ruling counts, forcing a historical-marker rewrite of a checklist header.

## Optimization Points
- validate-requirements should recognise its own blind spot (code-span-stripped definition rows) or at least warn when a definition line contains concatenation-like token sequences; pre-analyze-check's count-claim rule should skip dated sections (it already skips historical lines, but file-level dated headers such as checklists still trip it); the two validators should share one definition-row regex owner - the observed divergence (FR_DEF requires '**FR-NNN**:' while validate-requirements accepts more) is a second-owner drift.
