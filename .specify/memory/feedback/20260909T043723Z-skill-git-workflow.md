---
id: "20260909T043723Z-skill-git-workflow"
unit_id: "skill:git-workflow"
unit_type: "skill"
run_id: "git-workflow-bootstrap-20260909"
scope: "local"
probe: "skill-git-workflow-wrapup"
kind: "internal"
slice: "skills"
partial: false
created: "2026-09-09T04:37:23Z"
summary: "Bootstrap run on a repository whose managed block had never been initialized ('None yet.' since 2026-08-17) despite AGENTS.md declaring that block the single source of truth for every git operation — "
---

## Review
Bootstrap run on a repository whose managed block had never been initialized ('None yet.' since 2026-08-17) despite AGENTS.md declaring that block the single source of truth for every git operation — the gap was exposed when a merge had to resolve branch roles from git config instead. Confirmed no legacy sources (docs/git-workflow.md and .specify/memory/git-workflow.md absent; instructions.md carries only a pointer, no markers), detected the real topology, and confirmed MAIN with the user rather than fabricating it — which mattered because this repo has both master and main on DIFFERENT lineages (main tracks the upstream project, 539 ahead / 1507 behind master), so guessing would have corrupted every future sync. The user then declared PRE/DEV inapplicable under the project's SDD branch convention, so the block records MAIN=master with PRE/DEV marked not-applicable plus the feature-branch convention, the two remote-role hazards (origin is upstream and must never be pushed; remote.origin.url is not the fork, so URL@SHA citations do not resolve), and an explicit note that .gitexcludes has no consumer without tier sync. Replaced only the marker-bounded region and asserted the bytes outside it were unchanged; verified the placeholder row is gone so future runs enter Maintain rather than Bootstrap.

## Optimization Points
- **Bootstrap assumes a three-tier workflow exists; this project has none, and the skill has no vocabulary for recording that.** Steps 1.2/1.3 ask for MAIN/PRE/DEV names and offer to create missing branches, and the asset template has exactly three rows plus a sync/merge chain. When the user's real convention is trunk + short-lived feature branches, the only faithful outcomes are (a) create two branches nobody uses, or (b) write "不适用" into a template shaped for branch names. I chose (b) and had to hand-adapt the Sync chain / Merge chain lines, which the template does not anticipate. Optimization: let the block express a tier count of 1 (a `Not applicable` row shape plus a `Feature branch convention` line as a first-class field), so bootstrap can record reality instead of forcing a shape.
- **`.gitexcludes` initialization (step 1.5) has no consumer when there is no tier sync, but the skill still instructs asking about it.** Its entire purpose is protecting branch-exclusive files during rebase/merge between tiers. Optimization: gate step 1.5 on PRE/DEV actually existing, and record the skip reason in the block — otherwise the next health check reports missing `.gitexcludes` as a residual and someone creates dead machinery.
- **The `None yet.` placeholder string appears in the template's own instructional comment, so a naive "is bootstrap still needed?" check gives a false positive.** The real criterion is the placeholder *row* (`| None yet. | - | - | - |`) plus presence of MAIN/PRE/DEV rows. My first verification used a substring test and reported the placeholder as still present when the block was correctly filled. Optimization: state the detection predicate as the row pattern, not the bare string, in instructions-lookup.md.
- **What worked:** Phase 0's legacy-source sweep (docs/git-workflow.md, .specify/memory/git-workflow.md, markers inside instructions.md) correctly established there was nothing to migrate and that instructions.md holds only a pointer — that check is cheap and prevents creating a second data source. Keeping the write to marker-bounded replacement, with a byte-equality assertion on the content outside the markers, is the right discipline for a machine-maintained block.
