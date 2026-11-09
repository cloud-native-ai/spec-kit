---
id: "20261109T162201Z-skill-study-code"
unit_id: "skill:study-code"
unit_type: "skill"
run_id: "20261109T161336Z-c3"
scope: "local"
probe: "skill-study-code-wrapup"
kind: "internal"
slice: "skills"
partial: false
created: "2026-11-09T16:22:01Z"
summary: "Five-step study-code run completed on a 120-file TypeScript research prototype. Core concepts, architecture, components and key implementations are grounded in file:line evidence; the final report pas"
---

## Review
Five-step study-code run completed on a 120-file TypeScript research prototype. Core concepts, architecture, components and key implementations are grounded in file:line evidence; the final report passed its self-check (42 evidence paths, 29 anchors, 21 index rows). Friction was concentrated in Step 1 workspace setup (unwritable default study root; damaged git refs in the target) and in the Wrap-up determination flag semantics; the target repository was never modified.

## Optimization Points
- token-efficiency — Step 1 materialization: the prescribed `git clone --depth 1 file://$WORK_DIR` cannot serve a repo whose `refs/heads/main` is zeroed (clone returns an empty repository); the run fell back to `cp -a` of the working tree, losing the documented `keep a .git for traceability` affordance. SKILL.md Step 1.1 should state the fallback order (clone → `git archive <commit>` → working-tree copy) and require recording the commit hash as minimum provenance.
- token-efficiency — Step 1 pre-flight: the default `$STUDY_DIR = $WORK_DIR/../study-code/` was not writable (parent root-owned) and the failure surfaced only at `mkdir`; add one pre-flight writability probe of `$WORK_DIR/..` before choosing the default root.
- token-efficiency — Step 2 data gathering: per-file LOC/bytes were collected twice (an initial wc/stat pass, then a printf table); one collection should feed both outline-code.md and strip-manifest.md.
- Wrap-up Run Determination: `--names-current` / `--names-baseline` are pytest failed-nodeid baselines; the skill's Wrap-up text does not say so, and the first call filled them with skill filenames, producing a spurious `artifact_correctness: regressed` (added=7) that required two corrective records. The Wrap-up section should (a) name the two flags as failed-test-name baselines and (b) state "omit both when no failed-set baseline exists".
