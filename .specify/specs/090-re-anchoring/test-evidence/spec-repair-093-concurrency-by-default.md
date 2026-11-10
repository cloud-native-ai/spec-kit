# Spec Repair — 093-concurrency-by-default

**Date**: 2026-11-10
**Target**: `.specify/specs/093-concurrency-by-default/` (live — not archived)
**Sources read**:
- `.specify/specs/090-re-anchoring/test-evidence/spec-audit-live-batch-6.md` § `093-concurrency-by-default` (census: 319 refs → 272 alive / 47 dead)
- `.specify/specs/090-re-anchoring/test-evidence/spec-audit-settled.json` → `.specify/specs/093-concurrency-by-default` (`refs=256, alive=206, dead=50`, `dead_list` = 20 distinct tokens)
**Registry**: row `.specify/features.md:102` resolves (Status `Blocked`; detail `.specify/features/093-concurrency-by-default.md` exists; spec path exists) — **no registry edit needed**.

## Counts

| Metric | Value |
|---|---|
| Dead occurrences (settled scan) | 50 |
| Dead occurrences (batch-6 census) | 47 |
| Dead tokens after reconciliation (distinct) | **34** = 20 settled `dead_list` + 13 named only in batch-6 + 1 found during transcription |
| **live-fixed** | **9 tokens / 14 occurrences / 5 files** |
| **dated-kept** (exclusive) | **17 tokens** (+ dated occurrences of 5 mixed tokens) |
| **non-reference** (primary) | **8 tokens** (+ non-reference occurrences of 2 mixed tokens) |

The 34 reconciled tokens are classified below; mixed tokens (live/dated/non-reference occurrences) are named in every class they touch, so class rows do not sum to 34 by design. Occurrences inside `test-evidence/` suite logs (raw pytest output) and `notes/` are evidence of past runs and were not rewritten — only their token is counted once here.

## Live-fixed — before → after

| # | Before | Anchor(s) | After | Why |
|---|---|---|---|---|
| 1 | `.specify/memory/constitution.md` | `plan.md:58`, `research.md:5` | `.specify/constitution.md` | Anchor rename 090 (`6fb8093c4`); target exists |
| 2 | `.specify/memory/features/064.md` | `plan.md:290` | `.specify/features/064-subagent-concurrency.md` | Anchor rename; target exists |
| 3 | `.specify/memory/features/070.md` | `plan.md:291` | `.specify/features/070-subagent-task-teams.md` | Anchor rename; target exists |
| 4 | `.specify/memory/features/086.md` | `plan.md:292` | `.specify/features/086-efficient-test-execution.md` | Anchor rename; target exists |
| 5 | `.specify/memory/features/092.md` | `plan.md:293` | `.specify/features/094-goal-team-parallel.md` | Goal/Team Parallel feature was renumbered 092 → 094; current 092 is Non-Disposable. The dependency-block label `092:` → `094:` in the same entry |
| 6 | `.specify/memory/features/093.md` | `plan.md:63`, `tasks.md:5`, `research.md:8`, `feature-ref.md:6` | `.specify/features/093-concurrency-by-default.md` | Anchor rename; target exists |
| 7 | `.specify/memory/register.md` | `requirements.md:335` (amend session "落点"), `tasks.md:369` (WP1 write domain) | `.specify/register.md` | Anchor rename; the `FR-036@093` row exists at `.specify/register.md:210` |
| 8 | `.specify/specs/092-goal-team-parallel/verification.md` | `plan.md:293` | `.specify/specs/094-goal-team-parallel/verification.md` | Spec renumbered; directory `092-goal-team-parallel` does not exist, `094-goal-team-parallel` does |
| 9 | `specs/092-goal-team-parallel/notes/execution-lessons-2026-11-09.md` | `research.md:8` | `specs/094-goal-team-parallel/notes/execution-lessons-2026-11-09.md` | Bare-`specs/` form missed by both audit scans; `094-goal-team-parallel/notes/execution-lessons-2026-11-09.md` exists |

Validators re-run after these edits: see § Validator readings.

Files touched: `requirements.md` (1 line), `plan.md` (6 lines), `tasks.md` (2 lines), `research.md` (2 lines), `feature-ref.md` (1 line). No file outside the spec directory was edited; no registry edit was needed.

## Dated-kept — left unchanged

Transient `.specify/.tmp/` run/worktree paths (recorded evidence of past runs):

| Token | Representative anchor(s) |
|---|---|
| `.specify/.tmp/sdd-loop/worktrees/093-clarify` | `feature-ref.md:136`, `notes/analyze-*.md` |
| `.specify/.tmp/sdd-loop/worktrees/093-wp2` | `test-evidence/wp*` logs |
| `.specify/.tmp/sdd-loop/worktrees/093-wp4` | `test-evidence/wp*` logs |
| `.specify/.tmp/sdd-loop/worktrees/093-wp5` | `test-evidence/wp5-closure-reading.json:34` |
| `.specify/.tmp/sdd-loop/worktrees/093-enginefix` | `notes/engine-fix.md` |
| `.specify/.tmp/sdd-loop/worktrees/093-` (prefix mention) | `notes/*` worktree listings |
| `.specify/.tmp/sdd-loop/tmp/concurrency-by-default/design.md` | `research.md:9` (explicitly a design brief read from the main tree) |
| `.specify/.tmp/wp5/quickstart/serial-bad.yaml` | `test-evidence/wp5-*` |
| `.specify/.tmp/wp5/quickstart/cap-record.yaml` | `test-evidence/wp5-*` |
| `.specify/.tmp/wp5/quickstart/reading-missing.json` | `test-evidence/wp5-*` |
| `.specify/.tmp/wp5/quickstart/serial-empty.json` | `test-evidence/wp5-*` |

Dated prose/readings (notes, checkpoints, checklists, test-evidence):

| Token | Representative anchor(s) |
|---|---|
| `.specify/memory/features` (directory) | `checkpoints/03-plan.md:40`, `notes/review-*.md` |
| `.specify/memory/features.md` | `notes/review-arc.md:11,20,72`, `notes/review-process-artifacts.md:227` |
| `.specify/memory/glossary.md` | `notes/analyze-findings.md:49` |
| `scripts/stage-runner.sh` | `notes/analyze-repair3.md:14,26` |
| `skills/sdd-loop-driver/references/checkpoint-protocol.md` | `notes/analyze-round2/v3-trunk-reconciliation.md:18` (live copy is `skills/external/sdd-loop-driver/references/checkpoint-protocol.md`) |
| `shared/declarations/non-disposable-review-surface.yaml` | `notes/analyze-round3/v3b-consistency.md:138` (live copy is `shared/declarations/facts/non-disposable-review-surface.yaml`) |
| `tests/contract/test_concurrency_check_engine.py` | `notes/review-implementation-code.md:72,87` (self-disclosed; module lives at `tests/unit/test_concurrency_check_engine.py`) |

Mixed tokens — live occurrences fixed, dated occurrences kept:

| Token | Fixed anchors | Kept anchors |
|---|---|---|
| `.specify/memory/constitution.md` | `plan.md:58`, `research.md:5` | `notes/analyze-findings.md:7` |
| `.specify/memory/features/093.md` | `plan.md:63`, `tasks.md:5`, `research.md:8`, `feature-ref.md:6` | `checklists/2026-11-09-requirements-quality.md:5`, `notes/serial-baseline.md:20`, `test-evidence/wp5-*` |
| `.specify/memory/register.md` | `requirements.md:335`, `tasks.md:369` | `notes/amend-fr036.md:22`, `notes/review-process-artifacts.md:187`, `test-evidence/wp5-*` |
| `.specify/goal` | — | `requirements.md:295,309` — Clarify records explicitly preserved as dated by the erratum at `requirements.md:311` |
| `.specify/templates/commands/` | — | `checkpoints/03-plan.md:9` (advisory listing this feature creates), `notes/analyze-findings.md:169`, `notes/implement-wp5.md:56` |
| `tests/contract/test_coaching_run_contract` | — | `notes/analyze-round2/v2-gates-directive.md:53,62` |
| `scripts/wp-gate.py` | — | `notes/review-implementation-code.md:114` |
| `templates/stage-team-preset.md` | — | `notes/review-implementation-code.md:114` |

## Non-reference — ignored

| Token | Anchor(s) | Kind |
|---|---|---|
| `src/generated/` | `notes/engine-fix.md:39` | Illustrative fixture write domain (audit: illustrative) |
| `src/generated/wp02.md` | `notes/engine-fix.md:86` | Illustrative fixture write domain |
| `.specify/goal` | `requirements.md:185,311`, `tasks.md:76`, `research.md:100`, `quickstart.md:45` | Historical-name annotation ("renamed by 090") in text that already states the current `.specify/anchoring/<slug>/goal.md`; not a pointer |
| `.specify/templates/commands/` | `plan.md:261`, `feature-ref.md:100`, `contracts/existing-semantics-disposal.contract.md:45` | Retirement statements ("NO mirror (retired)"; C-090 forbids reviving it) — the path is named in order to stay absent |
| `tests/contract/test_coaching_run_contract` | `plan.md:235,442`, `tasks.md:325,372` | Tokenization artifact of the settled scan: every live occurrence uses `tests/contract/test_coaching_run_contract.py`, which exists |
| `scripts/wp-gate.py` | `research.md:7` | Audit false positive: the token sits inside the brace group `skills/external/sdd-loop-driver/{…,scripts/wp-gate.py}`; the expanded path exists |
| `templates/stage-team-preset.md` | `research.md:7` | Same brace group — `skills/external/sdd-loop-driver/templates/stage-team-preset.md` exists |
| `test-evidence/suite-after-implement.txt` | `tasks.md:31` | Redirect destination inside the GATE-1 check command, not a citation of an existing artifact; no successor is claimed, none invented |

## Boundary notes

- **`.specify/memory/history` in the FR-036 exemption set** (`requirements.md:196`, `plan.md:409`, `tasks.md:332`): the live history store is `.specify/history/`. Left unchanged in this bounded repair because the normative set mirrors the guard's own allow-list (`tests/contract/test_test_entry_guard.py:46`) — a machine surface outside this spec's directory — so editing one side alone would desynchronize clause from guard. Flagged for a separate, two-sided repair.
- **Prose feature numbers** `064/070/086/092` at `plan.md:63`, `requirements.md:185`, `feature-ref.md:106` still use `092` for the goal/team feature; not a path reference, left as written. Only the dependency-block entry (`plan.md:293`) carried paths and was fixed to 094.
- **Feature detail file** `.specify/features/093-concurrency-by-default.md` (outside the spec directory) still records "36 FR / 12 SC" vs the spec's 33 FR — pre-existing drift noted by batch-6; not touched per scope.

## Validator readings

| Command | Reading | Exit |
|---|---|---|
| `python3 .specify/scripts/python/validate-requirements.py requirements.md` | `status: ok`; `id-contiguous / doc-order / ref-resolvable / marker-count / dup-id / path-marker` all `pass (0)`; 345 lines, 48 definition rows, 11 shared strings; 0 error / 0 warning | 0 |
| `python3 .specify/scripts/python/validate-tasks.py tasks.md` | `PASS — 0 error(s), 0 warning(s)` | 0 |
| `python3 scripts/python/closure-acceptance-check.py --spec-dir .specify/specs/093-concurrency-by-default --repo .` (read-only, no `--json-out`) | `verdict: block`; `final-path: pass=5 blocked=1 … total=6`; reasons: `final-path-not-pass: SC-006` (pre-existing), plus `inherited-blocker-undisposed: 094:SC-001_status` and `094:SC-010_status` — newly readable because the repaired dependency pointer now resolves to the live 094 spec, whose own verification records both as `partial` (supporting path) | 1 (documented verdict, not a check crash) |

## Anomaly

The closure re-run now resolves the repaired `094` dependency and adds two `inherited-blocker-undisposed` reasons (`094:SC-001_status`, `094:SC-010_status`, both `partial` in `094/verification.md`); the verdict remains `block` and the pre-existing `SC-006` reason is unchanged — the repaired pointer made a real inherited state visible, it did not create it.

SPEC-REPAIR-2-DONE
