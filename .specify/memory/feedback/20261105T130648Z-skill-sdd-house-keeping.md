---
id: "20261105T130648Z-skill-sdd-house-keeping"
unit_id: "skill:sdd-house-keeping"
unit_type: "skill"
run_id: "r20261105T131500Z-0a01"
scope: "local"
probe: "skill-sdd-house-keeping-wrapup"
kind: "internal"
slice: "skills"
partial: false
created: "2026-11-05T13:06:48Z"
summary: "sdd-house-keeping check on the spec-kit repo: H1 physical complete / logical ready; sanitize materials 2492 pending (2491 dead-reference / 1 high stale-residue); retention 696 scanned / 0 eligible / 6"
---

## Review
sdd-house-keeping check on the spec-kit repo: H1 physical complete / logical ready; sanitize materials 2492 pending (2491 dead-reference / 1 high stale-residue); retention 696 scanned / 0 eligible / 696 blocked; features 78 (17 non-Completed); feedback 264 (>threshold); docs root entry absent; history manifest 2026-08-15 behind; hook-health 10 (8 vendor-managed); no structural writes.

## Optimization Points
- 1) sanitize materials has 2492 pending (mostly dead references across 79 specs) — a bounded but large cleanup task; 2) the history manifest is months behind while sessions continue; 3) the docs root entry is absent; 4) hook-health reports 8 vendor-managed hooks (not auto-fixable); 5) search-todo excluded symlinked instruction aliases with encoding_error (observed; zero TODO blocks).
