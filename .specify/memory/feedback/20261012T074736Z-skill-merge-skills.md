---
id: "20261012T074736Z-skill-merge-skills"
unit_id: "skill:merge-skills"
unit_type: "skill"
run_id: "merge-skills-draw-six-into-one-20261012T0730"
scope: "local"
probe: "skill-merge-skills-wrapup"
kind: "internal"
slice: "skills"
partial: false
created: "2026-10-12T07:47:36Z"
summary: "Ran the full 8-phase merge of six draw-* engine skills into draw-diagram, and this was the first real use of the provenance mechanism added a day earlier. Both directions of the coverage gate proved t"
---

## Review
Ran the full 8-phase merge of six draw-* engine skills into draw-diagram, and this was the first real use of the provenance mechanism added a day earlier. Both directions of the coverage gate proved their worth: the forward probe classified 37 residual tokens (all verified false positives with reasons, each destination asserted to exist before the reason was written), and the reverse probe caught two genuine losses in my own rewrite of the target — the SDS handoff term and the measured file-divergence examples — which I restored rather than allow-listed. A separate byte-level comparison accounted for all 160 relocated files (91 identical, 69 intentionally rewritten, 0 missing, 0 non-text touched), covering the scripts the token probe cannot see. Phase 8 cleanup ran only after the record and six baselines were committed and the checker was green.

## Optimization Points
- The reverse-direction probe is the load-bearing half and the skill under-sells it. It caught two real content losses in my own target rewrite that the forward probe structurally cannot see, because the forward direction only asks "did the source's facts survive?" and never "did the target lose its own while I was editing it?". Phase 5 lists it as one bullet among four; on evidence from this run it deserves to be stated as mandatory-with-its-own-allow-file, since its misses are a different species (my own authoring errors, not source omissions) and mixing the two allow files makes the reasons unreadable.
- Phase 7's decommission checklist has no slot for a governance artifact that enumerates the retired skills. An active goal (.specify/goal/draw-two-layer-structure) named all seven draw skills in its success criterion and had registered this exact move as a dropped target. Nothing in the skill's cleanup surfaces (symlinks, registries, declarations, topology docs) covers "a goal or criterion whose subject set you just invalidated", and goal-utils.py enforces subject-set shape, so hand-editing it would have been the wrong route. The checklist should name machine-enumerated governance artifacts as a surface, and say to amend them through their own engine.
- Pinned census literals are scattered and none of them are discoverable from the skill. Retiring six skills required finding 17->11 in test_skill_layer_visibility_guards.py, 32->26 in test_shared_reference_rewrite.py, four contract tests holding literal path constants into the sources, 12 probe-registry rows, and a generated probe-map. Each was found by running the suite and reading failures, not by following the skill. Phase 7 should say plainly: expect pinned counts and literal paths in tests, and enumerate them by grepping the retired slug across tests/ before deleting anything, rather than discovering them one red suite at a time.
- A blanket slug rename is unsafe in two specific ways that cost a repair pass each. Word-boundary matching rewrote draw-plantuml inside the team name draw-plantuml-optimizer, dangling a real directory path; and a skills: frontmatter list holding four retired slugs becomes four copies of the successor unless it is deduped. Both are mechanical and worth naming in the decommission playbook as the two rename hazards, since neither shows up as a test failure — the team path only dangles at runtime.
- token-efficiency: no raw dump of machine-managed data (probe output consumed as MISSING-line projections and counts, findings.json as a field projection, the 207MB dependency tree deleted before any copy step rather than moved); deterministic work stayed in programs (one relocation script did 496 link re-resolutions, 58 slug rewrites and 13 section removals, and one re-point script did 29 files with hazard handling); the one repeated read was re-running the six per-engine probes three times across rewrite iterations, which was deliberate re-verification rather than accidental duplication.
