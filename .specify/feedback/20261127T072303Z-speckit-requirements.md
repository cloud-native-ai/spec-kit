---
id: "20261127T072303Z-speckit-requirements"
unit_id: "/speckit.requirements"
unit_type: "command"
run_id: "r20261127T071500Z-111a"
scope: "local"
probe: "speckit-requirements-wrapup"
kind: "internal"
slice: "commands"
feature: "111-general-best-practices"
partial: false
created: "2026-11-27T07:23:03Z"
summary: "Requirements stage for 111-general-best-practices ported the closed ai-harness 087 general best-practices capability into spec-kit: five documents (manifest + four category owner files, three empty st"
---

## Review
Requirements stage for 111-general-best-practices ported the closed ai-harness 087 general best-practices capability into spec-kit: five documents (manifest + four category owner files, three empty stubs + the git clone HTTPS-vs-HTTP seed), accumulation declared by pointer to the existing feedback + knowledge-promotion owners, a framework-map registration row required by target directory governance, and a red-first contract guard plan; docs-only, no engine/runtime/store/decision-governance change. Structurally: 9 FR / 7 SC / 7 shared strings; validate-requirements status ok (0 error / 0 warning; one repair iteration on Shared-Strings Consumed-by reverse consistency); pre-analyze --stage requirements decision=pass errors=0 advisories=28 (all the not-yet-created deliverable paths); decomposition-check --mode plan decision=proceed fr_count=9; requirements-quality checklist green on its first stamped pass. Source verification preceded wiring: the source shipped no framework-map row and no instructions pointer (measured), yet the target's directory-governance section 3 requires same-change map registration, so exactly one map row was added to the design and instructions stayed untouched. Disclosed deviation: the scaffold script counts branches 109/110/111 and would derive 112 and a second branch; the spec was scaffolded manually per the 108 A-16 precedent. No user questions asked by design; worktree guard shows only the intended new spec directory (refs unchanged); no in-passing repair beyond the validator fix.

## Optimization Points
- token-efficiency: verifying the target surface (init shared copy, sync-mirrors pair, framework-map ownership, directory-governance registration, mirror-parity suite) required many overlapping greps/reads across src/, scripts/, shared/ and tests/; a deterministic 'port target surface' probe that takes the source references and reports each target path's existence plus the governing registration owner would cut those rounds to one engine call. Repeated friction: the create-new-requirements numbering trap (parallel line branches counted as used numbers, forcing manual scaffolding) has now recurred on 107/108/111 lines; a '--number/--stay-on-branch' option owned by the scaffold script would remove the manual deviation entirely.
