# Analyze round 3 — repair ledger R1 (fork writer R1)

Date: 2026-11-09. Tree: MAIN `/storage/project/cloud-native-ai/spec-kit`, branch `master` @ `abfc12d1`.
No commits, no push, no subagents. Territory: `contracts/*.md`, `tasks.md`, `coverage-baseline.txt`.
Sibling R2 owns `requirements.md` / `plan.md` / `feature-ref.md` / `quickstart.md` / registry — untouched here.

## Closed ids

### D1 — duplicated clause ids (H-1)

- `contracts/unified-archive-and-migration.md:124` — `C-53` → `C-112`; `:134` — `C-54` → `C-113`. Handoff page untouched (`handoff-contract.md:9,13` keep `C-53`/`C-54`).
- `contracts/binding-and-lifecycle.md:10` — namespace statement `(C-1…C-111)` → `(C-1…C-113)`.
- `tasks.md:329` (T082) — green tags `unified-archive-and-migration#C-53` / `#C-54` → `#C-112` / `#C-113`; the row's own cross-reference "idempotency as in C-54" → "C-113".
- `tasks.md:314` — Phase-8 note `C-53/C-54 → T082` → `C-112/C-113 → T082`.
- `tasks.md:344` — Green Partition archive row `C-53, C-54 → T082` → `C-112, C-113 → T082`.
- `tasks.md:382` — FR lane note `C-53 scopes the backfill` → `C-112`.
- Adjacent corrections inside the same Green Partition export (in-passing, disclosed): `tasks.md:343` `C-1 … C-29 → T005 · C-30 → T067` → `C-1 … C-30 → T005` (measured: T005 carries all 30 binding tags `#C-1…#C-30`; T067 carries zero green tags), and `tasks.md:351` `(C-30 → T067, …, C-54/C-55 → T081)` → `(C-51 → T079, C-52 → T080, C-111 → T080, C-112/C-113 → T082)` (T081 carries no green tag; the archive tail maps to T082).
- Verification (script over `contracts/*.md`): **113 `**C-NNN**` marker lines = 113 distinct ids**, 0 duplicates, contiguous `C-1…C-113` (missing set empty); per page binding 30 / archive 24 / handoff 18 / command-family 20 / owner-rewrites 21.
- Remaining `C-53`/`C-54` mentions are handoff-page-owned and untouched: `handoff-contract.md:9,13`; `tasks.md:261` (T049 tags), `:345` (handoff Green Partition row), `:473` (N-3).

### H-2 — GATE-6 true reading + one baseline re-freeze (D3)

- `tasks.md:52` GATE-6 rewritten to the measured truth, the D3 rationale, and the post-freeze verbatim reading (below). The stale `fr: 42` and the "all three lanes pass" claim are gone; the "do not loosen to the two-lane version" intent is kept with `113` clauses.
- `coverage-baseline.txt` re-frozen **once**, after the round-3 edits. `--freeze` only prints, so the mandated command was redirected (as the script's own usage documents):
  `python3 .specify/scripts/python/account-clause-coverage.py .specify/specs/094-goal-team-parallel --corpus-root /storage/project/cloud-native-ai/spec-kit/.specify/specs --freeze > .specify/specs/094-goal-team-parallel/coverage-baseline.txt` (exit 0).
- Baseline diff vs the prior frozen file: **+1 name, −0** — exactly `085-sdd-temporary-goal-team/contracts/checkpoint-and-agents.md#C-014`. New baseline holds 599 names; header `base-sha: abfc12d19412`, `files: 308 (parsed 193 + named 115)`.
- Rationale (also recorded at `tasks.md:52`): the freeze covers exactly the one new upstream name (`085#C-014`, introduced by the upstream merge `8edd955d` after the prior freeze); the `067` parse-doubt (`067-loop-efficiency-hardening/contracts/runner-contract.md`, form `md-bold-closed`, 0 clauses, indented blockquote cross-reference) is a named owner-grammar finding, **not a coverage item**, and enters no baseline. Nothing was removed from the baseline; no gate was weakened.
- L-5 cluster: `tasks.md:478-486` — the round-2 "all three lanes pass" bullet is now marked `round-2 recorded reading (2026-11-09, pre-round-3; historical, not the current reading)`, and records that `test-evidence/coverage-tasks.txt` in fact holds the pre-repair reading (`fr-uncovered fail (26) — 16 of 42`) while the round-2 all-pass reading lives in `test-evidence/analyze-repair2-gates-requirements.txt`; points to § GATE-6 for the current reading. `tasks.md:485 (now :488)` — `(pre-repair reading, 2026-11-09: fr 42 / sc 11 / tasks 80)` caveat added, with a pointer to `notes/analyze-round3/w2-traceability.md` § 3 for the round-3 readings. History retained, nothing deleted.

### M-1 — premises table counts
- `tasks.md:87` FR definitions **42** → **43**; `tasks.md:88` SC definitions **11** → **12**.

### M-2 — prerequisites contract accounting
- `tasks.md:7` — `contracts/ (5 files, C-1…C-111 = binding 30 + archive 22 + …)` → `contracts/ (5 files, C-1…C-113 = 113 marker lines / 113 distinct ids: binding 30 + archive 24 + handoff 18 + command-family 20 + owner-rewrites 21)`.

### M-3 — FR → row trace table
- `tasks.md:363` FR-005 + T022; `:367` FR-009 + T029; `:372` FR-035 − T060; `:377` FR-019 − T062; `:380` the malformed 2-cell `| FR-043 | T081, T082, T083 |` fixed to the 4-column shape `| FR-043 | T081, T082, T083 | | |`.
- Re-derived from the task rows' own FR quotes (script over all 83 `- [ ] TNNN` rows vs the table): **43 table FR rows, 83 task rows, drift 0** (membership both directions).

### L-4 — baseline id count
- `contracts/owner-rewrites-and-tests.md:84` — "44 ids already fail" → "**46** ids" (evidence: `test-evidence/plan-baseline-names.txt`, 46 unique ids; `tasks.md`/`quickstart.md` already said 46).

### L-5 — pre-repair evidence pointers
- Covered under H-2 above: `tasks.md:478-486` (round-2 bullet marked historical) and `tasks.md:488` (pre-repair caveat + re-point). Nothing deleted.

### T014 anchors
- `tasks.md:165` — `goal-utils.py:1416` → `:1447`; `:166` → `:185`; `:1418` → `:1449`. Measured on both `scripts/python/goal-utils.py` (source) and `.specify/scripts/python/goal-utils.py` (mirror); the two agree line-for-line on all three anchors.

### SC range
- `tasks.md:328` (T080) — `(SC-001…SC-011)` → `(SC-001…SC-012)`.

## Gate readings

### validate-tasks.py (only input: this repair's own tasks.md)
Command: `python3 .specify/scripts/python/validate-tasks.py .specify/specs/094-goal-team-parallel/tasks.md`
```
WARN  239: blockedBy: T043 references later task T054 (forward dependency — verify this is intentional)
PASS (with warnings): .specify/specs/094-goal-team-parallel/tasks.md — 0 error(s), 1 warning(s)
```
Exit 0. The single warning is the long-disclosed `T043 → T054` forward edge; `green-dangling`, `green-clause-collision`, `green-cross-phase`, `green-path-divergence` are all silent.

### account-clause-coverage — pre-freeze (the TRUE reading now stated in GATE-6)
Command: `python3 .specify/scripts/python/account-clause-coverage.py .specify/specs/094-goal-team-parallel --corpus-root /storage/project/cloud-native-ai/spec-kit/.specify/specs`
```
scanned 313 files: parsed 198 + named-unparseable 115 == 313  [relational sentinel OK]
  zero-clause-but-parseable (parse doubt): 1
named-unparseable: 115 (use --list-named to expand)
clause universe: 2116 distinct names over 198 parsed files (2140 ids extracted)
BEYOND-BASELINE: 085-sdd-temporary-goal-team/contracts/checkpoint-and-agents.md#C-014
companion (must be non-empty on a green run): claimed clauses 113, scanned files 313, clause universe 2116, FR universe 43
  [clause-uncovered] fail (599) — 599 uncovered, 1 beyond the frozen baseline
  [fr-uncovered] pass (0) — 43 of 43 FRs cited from citation groups
  [clause-unparsable] fail (115) — 115 files yield no clause id under the owner's forms; 1 of them declare a positive form, which is parse doubt and is never read as zero-and-covered
  [coverage-baseline-delta] fail (1) — baseline holds 598 names; 598 uncovered items are baseline-internal and do not block
1 error(s), 1 warning(s)
status: uncovered
```
Exit 1.

### account-clause-coverage — post-freeze (verbatim, same invocation)
```
companion (must be non-empty on a green run): claimed clauses 113, scanned files 313, clause universe 2116, FR universe 43
  [clause-uncovered] pass (599) — 599 uncovered, 0 beyond the frozen baseline
  [fr-uncovered] pass (0) — 43 of 43 FRs cited from citation groups
  [clause-unparsable] fail (115) — 115 files yield no clause id under the owner's forms; 1 of them declare a positive form, which is parse doubt and is never read as zero-and-covered
  [coverage-baseline-delta] pass (0) — baseline holds 599 names; 599 uncovered items are baseline-internal and do not block
0 error(s), 1 warning(s)
status: ok
```
Exit 0; `uncovered beyond baseline: 0`; `zero-clause-but-parseable (parse doubt): 1` (the `067` file — a named warning, never read as covered). A final re-run after the last text edits produced an identical summary block.

## Residual risks

1. **D4 lands on R2's artifacts only this wave.** The contract pages (my territory) still write the archive home as `.specify/goal/` (C-31, C-112) while W1 ANOMALY-1 measures the live store at `.specify/anchoring/`. If R2's D4 re-scope of FR-007/FR-025 renames the vocabulary, the archive page may need a follow-up alignment; no such contract-page instruction was issued to R1, so it is untouched.
2. **`feature-ref.md` bare-id ambiguity** (`C-53`/`C-54` on FR-016/FR-035 vs FR-043) is D1's R2 half and remains until R2 page-qualifies those rows.
3. **Adjacent defect not repaired:** `tasks.md:166` (T015) carries a stray duplicated evidence fragment (`— evidence: test-evidence/validate-tasks.txt — evidence: scripts/python/goal-utils.py …`). Outside the assigned id set; deleting a pointer would risk a silent record loss, so it is flagged, not edited.
4. `clause-unparsable` remains a red lane line (`fail`) while overall status is `ok`/exit 0, by the script's own design (`zero_positive` feeds warnings, not errors). A future reviewer reading lane lines alone will see red — that is the intended owner-grammar finding for `067-loop-efficiency-hardening/contracts/runner-contract.md`, not a coverage gap.
5. The re-frozen `coverage-baseline.txt` header now records the corpus state at `abfc12d1` (`files: 308`, `base-sha: abfc12d19412`), superseding the prior `66e5b8e369e0 / files: 292` header; the prior file is a generated artifact and was regenerated in full by design (its name-set delta is `+085#C-014`, `−0`, recorded above).
6. Historical 42/111 readings in `requirements.md` (L-1) remain until R2 adds the `(pre-FR-043)` caveats.

## Fast-fail / anomaly statement

One disclosed in-passing correction beyond the literal instruction set: the Green Partition export's binding row and its "own row's tag" parenthetical were false against the rows' own tags (`C-30 → T067` — T067 has no tag; `C-54/C-55 → T081` — T081 has no tag), corrected in the same edit pass that D1 renamed the archive tail. Nothing else was silently changed; no dated record was deleted; no gate was loosened.
