# Implement Package P4 Stage Evidence — 2026-11-27

Line `decision-batch-panel`; run `r20261127T081500Z-112a`; stage `implement` package **P4 (final)** (tasks T046–T058); baseline `8d5aafb37`; branch `112-decision-batch-panel` (worktree `.specify/.tmp/sdd-loop/worktrees/decision-batch-panel`).

## Scope executed

| Task | Result |
|------|--------|
| T046 | US5 red-first unit tests authored: `test_supersession_append_only`（prior-conflict）and `test_supersession_unwritable_prior_refused`（new `unwritable-old-record` fixture）; red run `6 failed` recorded with `--names-out notes/red-first-names-us5.txt` |
| T047 | US5 contract tests authored: `test_transmission_reuses_107_chain` (C-509), `test_owner_extension_single_owner` (C-511), `test_red_lines_and_boundary` (C-512), `test_behavior_surfaces_named` (C-208) — all red at authoring, green at T052 |
| T048 | Owner page § 重决与取代（Redecision & Supersession）: add-a-record-never-overwrite, the single `superseded_by` append (old bytes byte-identical, already-superseded records skipped, the in-batch-record append as the sole sanctioned post-write mutation), named refusal on unreadable/unwritable prior carriers, transmission reuse, red lines and the machine/behaviour boundary; § 强制边界 extended to sixteen M rules (M-10…M-16 with positional judge actions and reverse-sample directories) and nine B rules (B-08 presentation readability/consequence truthfulness, B-09 basis sufficiency), table–guard parity duty now naming both judge-action forms; dependent pin `test_decision_governance_contracts.py` B-row set 7 → 9 moved in the same change |
| T049 | Guard module extended: `LEGACY_GUARD_ROSTER` (nine 107 entries byte-identical) + `BATCH_GUARD_ROSTER` (M-10…M-16), union `GUARD_ROSTER`, `M_RULES` M-01…M-16 / `B_RULES` B-01…B-09; reverse samples `m10`…`m16` created (m10 unparseable register; m11 duplicate field; m12 autonomous+human mix; m13 prior conflict; m14 unknown-identity reply; m15 recorded-then-duplicate; m16 recorded-then-corrupted pointer), each driven through the batch engine's documented positional actions with exit-code + needle + zero-mutation assertions; parity test asserts the nine `--action` rows and the seven positional rows; added `test_m12_batch_scan_deterministic_and_autonomous_zero` |
| T050 | `record` supersession in `scripts/python/decision-batch.py`: `plan_supersession`/`build_supersession_updates` (pre-write validation over the re-scanned prior index, unreadable/unwritable carrier → named `prior-carrier` refusal, zero writes) and `insert_superseded_by` (single-line append, block-scoped, idempotent), block+supersession texts composed per carrier (no lost update), disclosures and the batch-record 收尾 `取代追加` lines; help/docstring updated |
| T051 | US5 mirror pairs regenerated and verified: `sync-mirrors.py --write` then `--check` rc 0 (shared 123 / scripts 135 byte-identical); `cmp` owner page + engine byte-identical; gate scan 30 blocking / 0 violations — zero NEW hits vs `test-evidence/scan-confirmation-gates-baseline.txt` |
| T052 | US5 phase tests green: three-module run `76 passed`; evidence in `notes/us5-green.txt`; S6/S7 slots and executed-run records filled in `notes/red-first-evidence.md` |
| T053 | `docs/reference/commands/decide.md`: entry, closed actions, flags, exit semantics copied from the engine's `--help` face, owner-page pointer, boundaries, related surfaces — no restated criteria table |
| T054 | `shared/definitions/framework-map.md` decision-governance row: seventeen-term vocabulary, P-01…P-13, the batch faces, sixteen/nine M/B boundary, consumer list (`validate-decisions.py`, `decision-batch.py`, the command, the skill, the command doc, 107/112 suites) |
| T055 | `test_distribution_init_contains_decide` added: throwaway fresh `specify init` receives the decide command copy, the decide-batch skill and the engine (`--version` healthy); the four per-tool copies each carry the edit — `1 passed` |
| T056 | Delivery closure: sync `--check` rc 0, regen `--check` rc 0, both engine copies answer `--version` (`decision-batch.py 0.0.22`) and `--help`, `## Decision Items` = **1,276 B**, protected-path diff vs baseline empty |
| T057 | Every quickstart scenario executed as written; commands, decisive output, exit status and teardown recorded in `notes/quickstart-run.md`（S3 workspace carries two settle-able human items so the declared expected result — one `accepted-default` + one `objected-alternative` — is reachable; disclosed in the run record） |
| T058 | Targeted regression set `108 passed`, 0 failing names; governance contracts `17 passed`; full-suite reading (fast tier) `229 failed / 10,412 passed / 3 skipped` with the 229-name failure set **identical** to the base-commit run (0 new, 0 fixed; +8 newly passing); `test-evidence/verification-input.md` assembled for the spec-side `verification.md` derivation |

Task states closed in `tasks.md`: T046–T058 all `[X]` (13 rows); the file now carries 58/58 closed, 0 open. `validate-tasks.py` → 0 errors / 0 warnings (rc 0).

## Gate readings (all executed this package)

| Check | Command | Result |
|-------|---------|--------|
| GATE-1 | `validate-tasks.py …/tasks.md` | 0 errors / 0 warnings, rc 0 (`test-evidence/tasks-validator-p4.txt`) |
| GATE-2 | `pre-analyze-check.py --stage tasks` | `decision=pass errors=0 advisories=3` (`test-evidence/pre-analyze-tasks-p4.txt`); advisories adjudicated below |
| GATE-3 | § Requirement Coverage Map + pre-analyze `runtime-stack-row` | 45 FR / 10 SC covered; runtime-stack errors=0 in the same run |
| GATE-4 | `verification.md` | **hand-off**: the rows author `test-evidence/verification-input.md` instead; the driver derives `verification.md` spec-side. Input carries all ten SC `pass` rows and the feature-level smoke record (`smoke_command` / `smoke_exit_code=0` / `smoke_evidence_path` present) |
| GATE-5 | mirrors / copies / instruction section / protected paths | `sync-mirrors.py --check` rc 0; `regen-command-copies.py --check` rc 0; `## Decision Items` = 1,276 B; `git diff --stat 8d5aafb37 -- .specify/.gitignore .specify/register.md .specify/instructions.md` empty (`test-evidence/implement-p4-gates.txt`) |
| GATE-6 | `scan-confirmation-gates.py --summary` | 30 blocking (22/7/1) / 0 violations — zero NEW hits vs baseline |
| GATE-7 | migration/probe census tests | green in the T058 targeted run (`test_migration_distribution.py`, `test_probe_nonentity_catalog.py`) |
| GATE-8 | open tasks | `grep -cE '^- \[[ >]\]'` → **0** |

GATE-2 advisories (adjudicated, all expected-by-design): (1) `plan.md:136` `.specify/templates/commands/` — the plan states that path is retired and carries **no** mirror; (2) `quickstart.md:44` `.specify/.tmp/decide-demo/` — the sanctioned scratch workspace, created and torn down during T057; (3) `research.md:4` worktree path — recorded relative to the main repository, not resolvable from inside the worktree.

## Red/green pointers

- Red-first: `notes/red-first-evidence.md` § S6 (6 red names in `notes/red-first-names-us5.txt`) and § S7 (M-10…M-16 execution table + executed-run records).
- Green: `notes/us5-green.txt`; clause green points C-208, C-509…C-512 — 54/54 clauses now claimed.
- Regression: `test-evidence/implement-p4-full-suite.txt`（targeted 108 passed; full-suite name-level zero-new-failure vs `implement-p4-full-suite-baseline-names.txt`）.

## Corrections applied (in passing)

- `tests/contract/test_decision_governance_contracts.py`: the B-row equality pin moved `range(1, 8)` → `range(1, 10)` with the owner page's B table (T048) — the pin's owner is the owner page; leaving 7 would pin a stale roster. Disclosed, not a new test.
- `test_red_lines_and_boundary` initially required the literal `零网络` in § 重决与取代; the owner section said「MUST NOT 访问网络」in prose — the section now carries the spec's own phrase（零网络、零反馈存储写入、零自动传输）, aligning wording rather than weakening the test.
- Quickstart S3 reading: the scenario's expected result names both an `accepted-default` and an `objected-alternative`, so the demo workspace carries two settle-able human items plus the irreversible and autonomous ones; recorded in `notes/quickstart-run.md`.
- `m15`/`m16` reverse samples were produced by one real `record` run each over their own fixture workspace (the recorded batch is the sample's subject; `m16`'s option-evidence pointer was then corrupted); presentation payloads come from the engine's own `scan`. No fixture is hand-copied from expected output.

## Boundaries held

- **A-26**: distinct batch ids → distinct knowledge paths; a batch writes only its own record; reads of another batch's settled record only for the declared read-only purposes (the m15/m16 fixtures and the unit concurrency test pin this).
- **A-27**: the only post-write mutation of any prior record is the single `superseded_by` line; the `diff` in `notes/us5-green.txt` § 3 is an addition-only line and every pre-existing byte is unchanged; an unwritable prior carrier refuses the whole record with zero writes.
- No edit to the state spine, `.specify/register.md`, `.specify/instructions.md`, `.specify/.gitignore`, `.specify/glossary.md`, `.specify/features.md`, other specs or the main tree; no push.
- No new runtime store root; every demo workspace stayed under `.specify/.tmp/` and was torn down.
- Zero network access; zero feedback-store write by the mechanism; zero automatic transmission; zero `ai-autonomous` presentation.

## Wrap-up accounting

- Run Determination — `.specify/scripts/python/run-determination.py --action determine --unit-id "/speckit.implement" --unit-type command --run-id r20261127T081500Z-112a` → `duplicate: … was already determined`（one record per run, P1-owned）· `test-evidence/implement-p4-run-determination.txt`
- Exec Quant — `--action collect --unit-id "/speckit.implement" …` → `duplicate record`, no second row · `test-evidence/implement-p4-exec-quant.txt`
- Feedback Record — `feedback-utils.py --action record --unit-id "/speckit.implement" …` → `duplicate: true`（entry `20261127T100546Z-speckit-implement`）· `test-evidence/implement-p4-feedback-record.txt`
- Workspace guard — `workspace-guard.py --snapshot …/workspace-implement-p4.json`; `--check` after the final commit → reading in `test-evidence/workspace-implement-p4-check.txt`

## Concurrency

`requested=1`; `effective=1`; `effective_reason=write-conflict` — the owner page, engine, guard module, fixtures and evidence sinks are single-writer surfaces; the package is one serial unit.