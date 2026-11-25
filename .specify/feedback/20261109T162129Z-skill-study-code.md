---
id: "20261109T162129Z-skill-study-code"
unit_id: "skill:study-code"
unit_type: "skill"
run_id: "20261109T161336Z-c2"
scope: "local"
probe: "skill-study-code-wrapup"
kind: "internal"
slice: "skills"
disposition: "ignored"
partial: false
created: "2026-11-09T16:21:29Z"
summary: "Study-code executed a full five-step run against a research-prototype TypeScript repo (120 files after strip). Core concepts, architecture, components and implementation were grounded in file:line evi"
disposition_reason: "Superseded by the final c3 record; points file used a malformed tag and temp evidence refs"
---

## Review
Study-code executed a full five-step run against a research-prototype TypeScript repo (120 files after strip). Core concepts, architecture, components and implementation were grounded in file:line evidence; the final report passed its self-check (42 evidence paths, 29 anchors). Friction concentrated in Step 1 workspace setup (unwritable default study root; damaged git refs in the target) and in the Wrap-up flag semantics; the target repository itself was never modified.

## Optimization Points
- [token-efficiency] Step 1 materialization path: the prescribed `git clone --depth 1 file://$WORK_DIR` cannot serve a repo whose `refs/heads/main` is zeroed; the run fell back to `cp -a` of the working tree (no `.git` kept), losing the documented "keep a .git for traceability" affordance. SKILL.md Step 1.1 should state the fallback order (clone → `git archive` → working-tree copy) and record the commit hash as the minimum provenance.
- [token-efficiency] Step 1 pre-flight: `$STUDY_DIR = $WORK_DIR/../study-code/` was not writable (parent root-owned) and the failure surfaced only at `mkdir`; add one pre-flight writability probe of `$WORK_DIR/..` before choosing the default root.
- [token-efficiency] Step 2 data gathering: per-file LOC/bytes were collected twice (an initial wc/stat pass, then a printf table); a single collection should feed both outline-code.md and strip-manifest.md.
- Wrap-up Run Determination: `--names-current` / `--names-baseline` are pytest failed-nodeid lists, but with no explicit statement in the skill's Wrap-up text the first call filled them with skill filenames, and the engine recorded `artifact_correctness: regressed` from added=7; a second corrected record (c2) was required. The Wrap-up section should name the two flags as failed-test-name baselines (or say "omit when no failed-set baseline exists").
