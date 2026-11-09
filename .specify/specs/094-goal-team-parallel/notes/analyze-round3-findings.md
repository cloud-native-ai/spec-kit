# Analyze round 3 — consolidated verdict and repair brief (2026-11-09)

Driver consolidation of three concurrent fork workers (W1 closures / W2 traceability+gates / W3 trunk reconciliation), each writing its own fragment under `notes/analyze-round3/`.

## Verdict

**NOT-READY — 2 HIGH** (H-1 clause-id collision, H-2 GATE-6 coverage claim contradicted) **+ 4 MEDIUM + 5 LOW**, plus the trunk reconciliation whose Option A was executed during this round (renumber 092→094, commit `29c3aa08`).

The six round-2 repair targets are **genuinely closed** (W1: file-level `git show --stat d03fca61` covers all 7 claimed files; round 2's prose-only closure did not recur). The HIGH findings are new defects introduced or exposed by that repair, not closures.

## Findings (merged; each has a fragment anchor)

### HIGH
- **H-1 duplicated clause ids** — 113 `**C-NNN**` marker lines but 111 distinct ids: the backfill clauses added on the archive page duplicate `C-53`/`C-54` of the handoff page (`unified-archive-and-migration.md:124,134` vs `handoff-contract.md:9,13`). The declared namespace "C-1…C-111 contiguous" is false; `feature-ref.md` prints bare ids, so FR-016/FR-035 and FR-043 both read "C-53, C-54" and are indistinguishable without the page name. Green tags stay sound (page-qualified). Evidence: `analyze-round3/w2-traceability.md` §2, `w1-closures.md` COUNT-CLAUSES.
- **H-2 GATE-6 coverage claim contradicted by the tree** — `tasks.md:52` claims all three coverage lanes pass; measured exit 1: `clause-uncovered` fail 599 (1 beyond the frozen baseline: `085-sdd-temporary-goal-team/contracts/checkpoint-and-agents.md#C-014`, added by upstream `8edd955d` after the baseline freeze), `clause-unparsable` 115 (1 parse-doubt file: `067-loop-efficiency-hardening/contracts/runner-contract.md`, blockquote cross-reference), `coverage-baseline-delta` fail 1; only `fr-uncovered` passes (43/43). Also `fr: 42` is stale (now 43), and `tasks.md:478-484` cites `test-evidence/coverage-tasks.txt` for an all-pass reading while that file holds the pre-repair `fr-uncovered fail (26) — 16 of 42`. Evidence: `w2-traceability.md` §3–§4.

### MEDIUM
- **M-1** `tasks.md:87/88`: premises table says FR 42 / SC 11 (now 43 / 12).
- **M-2** `tasks.md:7`: archive page counted as 22 and breakdown sums to 111; archive page has 24 markers, total 113.
- **M-3** `tasks.md` FR→row trace: FR-005 misses T022, FR-009 misses T029, FR-019 lists T062, FR-035 lists T060; FR-043 row is malformed (2 cells in a 4-column table).
- **M-4** registry detail file stale (`features/094.md` + the features.md row still carry pre-round-2 numbers).

### LOW (fix with date caveats, not rewrites of dated records)
- **L-1** historical 42/111 mentions in `requirements.md:263,295` (dated records; add a pre-FR-043 caveat only where they read as current).
- **L-2** `plan.md:53,258` spec-local denominator 14 (7+7); measured 16 (8+8 — both 092 lineages added one each); `tasks.md:474` already discloses 8/8.
- **L-3** `feature-ref.md` regeneration is membership-exact but 5 rows differ in order; "43 map rows" means 43 FR entries over 22 physical rows.
- **L-4** "44 baseline ids" in `plan.md:262` / `owner-rewrites-and-tests.md:84` vs the evidence's 46 (`plan-baseline-names.txt`).
- **L-5** `tasks.md:485` evidence pointers hold pre-repair readings (fr 42 / sc 11 / tasks 80) — add date caveats or re-point.
- **W1 extras**: T014 cites `:1416/:166/:1418`; measured `:1447/:185/:1449` (correct in passing). `SC-001…SC-011` survives as a live range at `requirements.md:9` and `tasks.md:328` although SC-012 exists.

## Trunk reconciliation (W3; Option A already executed)

- Renumber executed: spec dir, state spine, feature detail, registry row and goal/team slug dirs are now `094-goal-team-parallel` (commit `29c3aa08`); the trunk keeps `092` for the Non-Disposable archive pointer.
- FR accounting (of 43): 2 landed (FR-024, FR-026) · 10 partial (substrate only) · 28 pure delta · 3 superseded as written (FR-007 names the removed `.specify/goal/`; FR-025 member names clash with the renamed archive; FR-028 names a nonexistent driver path). Upstream landed the concept statement, not the executable surface (no binding record among 12 team.md, no migration, no residual probe, no handoff.md, no declaration entries, no tests).
- Trunk rename is PARTIAL: `.specify/anchoring/` exists (6 entries, file still `goal.md`), engine `resolve_scope()` still returns `global|spec|auto`, and several live framework files still carry pre-rename vocabulary. Only 094's own artifacts are in this repair's scope; the 150 live-pointer hits W4 measured belong to the 090 line (report only).
- Caution: bare `092` denotes three lineages on this trunk (092-non-disposable, our former 092, and an unrelated "092 handoff" lineage in agents/harness/non-disposable files). Never run a bare-token sweep; only the full `092-goal-team-parallel` token was renamed.

## Decision sheet (binding for both repair writers)

- **D1 clause ids**: the two backfill clauses move to **C-112** and **C-113**; the declared namespace becomes `C-1…C-113`; 113 markers = 113 distinct ids. Update every page-qualified green tag (`unified-archive-and-migration#C-53/#C-54` → `#C-112/#C-113`) and make `feature-ref.md` page-qualified where bare ids are ambiguous (FR-016, FR-035, FR-043 at minimum).
- **D2 counts**: FR 43 · SC 12 · clauses 113 · tasks 83 (T001–T083) · packages 7 (15+17+19+8+16+6+2) · serial baseline 46 ids · spec-local definitions 9 goal + 9 team.
- **D3 coverage baseline**: re-freeze **once**, after the edits, with the rationale recorded in `tasks.md` § GATE-6 and the repair note: the freeze covers exactly the one new upstream name (`085#C-014`); the `067` parse-doubt is a named owner-grammar finding, not a coverage item, and is never read as covered.
- **D4 anchoring vocabulary**: global store `.specify/anchoring/<slug>/goal.md` (filename unchanged); spec-local `<spec>/goal/<slug>/goal.md`; teams `.specify/teams/<slug>/team.md`. Re-scope FR-007 / FR-025 / FR-028 per W3 §2–3 with the rationale recorded in the artifact (decision-tension shape where load-bearing); the engine's current `global|spec|auto` scope values are facts to state, not to silently redefine.
- **D5 dated records**: historical counts keep their values with a `(pre-FR-043)` caveat where they could read as current; do not rewrite dated session records.

## Territories

- **R1**: `contracts/*.md` + `tasks.md` + `coverage-baseline.txt` (D1, H-2, M-1..M-3, L-4, L-5, T014 anchors, SC range in tasks).
- **R2**: `requirements.md` + `plan.md` + `feature-ref.md` + `quickstart.md` + `.specify/memory/features.md` row + `.specify/memory/features/094.md` + `.specify/memory/register.md` rows (D4, M-4, L-1..L-3, SC range in requirements).

Both writers: no commits (driver integrates), no gate weakening, no baseline freeze except D3 by R1.
