---
id: "20260911T074642Z-speckit-feedback"
unit_id: "/speckit.feedback"
unit_type: "command"
run_id: "speckit-feedback-consume-2026-09-11"
scope: "local"
probe: "speckit-feedback-wrapup"
kind: "internal"
slice: "commands"
partial: false
created: "2026-09-11T07:46:42Z"
summary: "Mode 4 consume run over 4 inbound bundles. Batch discipline paid for itself immediately: the 68 entry slots deduped to 59 distinct, of which 13 were already consumed by the 2026-08-18 run and 9 of tho"
---

## Review
Mode 4 consume run over 4 inbound bundles. Batch discipline paid for itself immediately: the 68 entry slots deduped to 59 distinct, of which 13 were already consumed by the 2026-08-18 run and 9 of those had been re-packaged into a later bundle. Git history proved the intake defect rather than inferring it — feedback-20260813T103513Z.zip was consumed and deleted at 6dcf974f then re-committed at 35f48b5c, and Step 1 was a bare ls with no consume-log cross-check. Four parallel read-only verifiers adjudicated 107 points against current framework source (two-hats respected: source dirs, never .specify/ mirrors) into 55 findings with path:line anchors — 64 STILL-VALID, 28 ALREADY-FIXED, 15 NOT-OURS, 0 unverifiable — and five inter-entry conflicts were resolved toward source, including one entry whose premise had already been refuted on 2026-08-31 yet travelled again in a bundle generated after the refutation, which is direct proof for the missing receipt path. User approved all 30 direct fixes; they were executed in five disjoint clusters and integrated centrally. Validation: full suite 42 failed / 2846 passed against a 41-failure baseline captured in a clean worktree at d79b585e, so the single delta is an environmental failure from 17 untracked .migration-backups leftovers written by a concurrently running external process — zero regressions from these edits; mirrors and all four per-tool command copies regenerated and --check clean; confirmation gates 23 with 0 violations under the 23.25 cap; shape gates exit 0 on every SKILL.md touched. Cleanup removed all 4 bundles after verifying the untracked one was the sole copy of its 19 entries and preserving all four out-of-repo. Two defects were reported rather than fixed to avoid unilateral architectural calls inside a consume run: the 10 red test_skill_home_workdir_template tests demanding sections that no longer exist in templates/commands/skills.md (red at HEAD before this run), and the .migration-backups leftovers already routed as R-13.

## Optimization Points
- # Optimization points — /speckit.feedback Mode 4 consume run (2026-09-11)
- ## Point 1 — Mode 4 has no deterministic intake projection, so the consumer hand-rolls one
- **Observed.** Step 1 is a bare `ls feedback/feedback-*.zip` and Step 2 says "extract and read".
- This batch was 4 bundles / 68 entry slots. To make it tractable I had to write four separate
- ad-hoc Python passes: (a) dedup slots → distinct entries by id, (b) split distinct entries into
- new vs already-consumed by cross-referencing `consume-log.md`, (c) project each entry's frontmatter
- plus `## Review` / `## Optimization Points` into a compact digest, (d) partition the digest into
- balanced per-unit group files for parallel verification. Every one of those is a fixed-rule
- text/data operation — exactly what `shared/guidelines/token-efficiency.md` § Program-First says
- MUST go to a deterministic program and MUST NOT be improvised per run.
- This is a Program-First violation *inside the command that preaches Program-First*, and F-E02
- (fixed this run) only adds the **instruction** to cross-check the log; it still leaves the
- cross-check, the dedup and the projection to the agent.
- **Proposed.** One engine action, e.g.
- `feedback-utils.py --action consume-scan --intake feedback/`, emitting per bundle: entry ids,
- cross-bundle duplicate groups, `consume-log.md` hits (already-consumed mark), git tracked/untracked
- status, MANIFEST `Install source @ sha` and `Generated`, and whether each entry id is present in
- the local store. The consumer then reads a verdict table instead of writing four scripts. This
- subsumes the F-E02 marks and makes R-12's "deterministic dedup projection" ask (logged 2026-08-31,
- recurring) concrete.
- ## Point 2 — Step 2's small-batch threshold has no large-batch counterpart
- **Observed.** Step 2 branches on "≤3 bundles, ≤20 entries → read inline" vs "larger → extract to a
- temp directory". The larger branch stops at extraction and says nothing about how to *read* 68
- entries. Reading them serially would have blown the context budget; the Summary-First discipline
- forbids injecting the raw corpus anyway. I invented the partition myself: group entries by
- `unit_id`, balance groups by review+points character volume rather than entry count (one entry
- carried 2.5 KB while another carried 200 B), write one digest file per group, dispatch one
- read-only verifier per group with disjoint file sets.
- That worked — 107 points adjudicated into 55 findings with evidence anchors — but it is
- undocumented craft that the next run will have to reinvent, and the naive reading of Step 2
- ("extract, then read files with standard file-reading tools") actively invites the context-overflow
- path.
- **Proposed.** Codify the large-batch partition rule in Step 2: project to a digest first (never
- read raw entries), group by unit, balance by text volume, one read-only verifier per group, and
- require each verifier to return per-point verdicts with `path:line` anchors so the consumer's job
- is reconciliation and conflict adjudication rather than re-reading.
- ## Point 3 — Cleanup has no orphan-safety precondition
- **Observed.** Step 4 deletes every bundle in the batch atomically, on the stated rationale that
- "the durable record is the consume-log row, never the zips". That is sound for a bundle whose
- entries also live in the local store or in git history. It is unsound for an **orphan**:
- `feedback-20260907T134039Z.zip` was untracked (no history copy) and I verified that **0 of its 19
- entries** existed in `.specify/memory/feedback/`. Deleting it would have destroyed the only copy of
- 19 entries, and the log row records routings, not the reporters' original evidence.
- I caught this only because I checked the store before deleting. Nothing in Step 4 asks for that
- check.
- **Proposed.** Add a precondition to Step 4: before removing a bundle, confirm at least one of —
- (a) tracked in git history, (b) every entry id present in the local store, (c) contents preserved
- outside the repo. If none holds, preserve first and say so in the cleanup column. This is one
- sentence and it converts an irreversible loss into a recoverable one.
