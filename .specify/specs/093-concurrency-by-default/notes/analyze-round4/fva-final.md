# FVA — final verification of repair round 3 (093-concurrency-by-default)

**Worker**: FVA (read-only final verification). Worktree: `.specify/.tmp/sdd-loop/worktrees/093-clarify`, branch `093-concurrency-by-default`, HEAD `132bedba` (verified by `git rev-parse --short HEAD`). No edits, no commits, no push, no subagents; the only file written is this note.
**Subject**: `notes/analyze-repair3.md`; commits `03d19361` (repair) + `132bedba` (spine record).
**Date**: 2026-11-09.

---

## 1. Per-item verification

| # | Item | Evidence (measured) | Verdict |
|---|------|---------------------|---------|
| 1 | V1B-F1: a tasks row names `skills/external/sdd-loop-driver/references/decomposition-model.md` § 13.4 explicitly and requires fork/subprocess carrier + in-process ban (not only § 20.1) | `tasks.md:326` **T153** names the file and "§ 13.4 (~L184)", quotes the native-local sentence, requires the fork carrier ("same-family `qodercli` child processes through `scripts/stage-runner.sh`") and the subprocess carrier ("independent child process of the agent's own CLI"), and states "the host-internal in-process subagent path is BANNED as a concurrency carrier". `tasks.md:313` T140 remains § 20.1-only, so the two sections no longer share one row. `plan.md:404` manifest row 4 → `T140, T153`, severity "MEDIUM (round-3 re-measure)". | **PASS** |
| 2 | V1B-F2: a row names `templates/stage-team-preset.md` (L74 native-local carrier) and requires the same | `tasks.md:327` **T154** names `skills/external/sdd-loop-driver/templates/stage-team-preset.md` and the `stage-worker` fill sentence (~L74 "a native subagent locally, one detached runner remotely"); requires the fork carrier as the local form and the subprocess carrier for heterogeneous agents; states "the host-internal in-process subagent path is BANNED as a carrier". `plan.md:406` manifest row 6 → `T116, T133, T154`. | **PASS** |
| 3 | V1B-F3: a row names `shared/definitions/subagent-definitions.md`, requires the carriers and bans "native first" | `tasks.md:328` **T155** names the file and both sections (`## Three Execution Modes` with the "**Native** is the default…" note; `## Mode Selection` with "native parallel calls" and "When in doubt: **native first** …"); the rewrite makes the parallel forms the fork + subprocess carriers and states "the host-internal in-process subagent path is BANNED as a concurrency carrier". `plan.md:416` manifest row 16 → `T037, T060, T099, T132, T155`. | **PASS** |
| 4 | V3B-F1: T006 states the measured 94 | `tasks.md:79` T006: "confirm **94** clauses … (measured 2026-11-09: 18 declaration-facts + 22 judgement-engine + 22 executor-obligations + 18 high-order-executors + 14 existing-semantics-disposal = 94 …)", with the instruction to re-read the count in the same command. **My re-measure with T006's own grep** (`grep -c '^- \*\*C-[0-9][0-9][0-9]\*\*'` over the five clause-bearing files): declaration-facts 18, judgement-engine 22, executor-obligations 22, high-order-executors 18, existing-semantics-disposal 14, **TOTAL 94**. Matches exactly. See observation O-1 for the trap-form aside. | **PASS** |
| 5 | V3B-F2: quickstart's S-9 reference fixed, or S-9 exists | `quickstart.md:8` now reads "…that is the point of S-0 and S-1"; both scenarios exist (`## S-0` at L12, `## S-1` at L30). No "S-9" occurs anywhere in `quickstart.md`; `plan.md:331` still declares "7 scenarios (S-0…S-6)", so not adding S-9 is consistent. | **PASS** |
| 6 | Rerun the gates | All five gate families green — verbatim readings in § 2. | **PASS** |
| 7 | `git show --stat 03d19361` covers the claimed files | 24 files: `tasks.md` (+14/−), `plan.md` (12), `quickstart.md` (2), `notes/analyze-repair3.md` (99), `notes/analyze-round3/{v1b-manifest,v2b-fixes-gates,v3b-consistency}.md`, `register.md` (+1), and `test-evidence/analyze-repair3-*` (8 files). No script, validator or test file touched — no gate weakening by edit. `132bedba` touches only `.specify/state/093-concurrency-by-default.md`. | **PASS** |

Supplementary checks: 155 task rows (`T001`…`T155`), contiguous and unique; package partition exact — WP1 16 + WP2 26 + WP3 27 + WP4 37 + WP5 49 = 155, 0 missing / 0 extra / 0 duplicate; T153–T155 sit under `## Phase 8` (L281) and inside `WP3-owners`, whose declared write domain already lists all three surfaces (no new package, no write-domain change); `coverage-baseline.txt` does not exist (no `--freeze` was run); no stale live count remains — the only "152" readings are the T152 row id and the dated round-2 run record, which is annotated, not rewritten.

## 2. Gate readings (rerun today, verbatim)

| Gate | Command | Reading | Verdict |
|---|---|---|---|
| G1 validate-requirements | `python3 .specify/scripts/python/validate-requirements.py .specify/specs/093-concurrency-by-default/requirements.md` | `status: ok`; `[id-contiguous]` `[doc-order]` `[ref-resolvable]` `[marker-count]` `[dup-id]` `[path-marker]` all `pass (0)`; `scanned: 337 lines, 47 definition rows, 11 shared strings`; `0 error(s), 0 warning(s)`; EXIT 0 | PASS |
| G3 validate-tasks | `python3 .specify/scripts/python/validate-tasks.py .specify/specs/093-concurrency-by-default/tasks.md` | `PASS: .specify/specs/093-concurrency-by-default/tasks.md — 0 error(s), 0 warning(s)`; EXIT 0; own row count 155 (contiguous T001…T155) | PASS |
| G5a pre-analyze (requirements) | `python3 .specify/skills/sdd-loop-driver/scripts/pre-analyze-check.py --repo <worktree> --spec-dir .specify/specs/093-concurrency-by-default --stage requirements` | `pre-analyze-check: stage=requirements decision=pass errors=0 advisories=112 waived=0`; summary `{"errors": 0, "advisories": 112, "waived": 0, "fr": 35, "sc": 12, "tasks": 155, "clauses": 0, "files": 15}`; EXIT 0 | PASS |
| G5b pre-analyze (plan) | same, `--stage plan` | `pre-analyze-check: stage=plan decision=pass errors=0 advisories=112 waived=0`; same summary (`fr=35 sc=12 tasks=155`); EXIT 0 | PASS |
| G5c pre-analyze (tasks) | same, `--stage tasks` | `pre-analyze-check: stage=tasks decision=pass errors=0 advisories=112 waived=0`; same summary (`fr=35 sc=12 tasks=155`); EXIT 0 | PASS |
| G6 decomposition | `python3 .specify/skills/sdd-loop-driver/scripts/decomposition-check.py --mode tasks --requirements …/requirements.md --tasks …/tasks.md` | `{"mode": "tasks", "decision": "proceed", "measured": {"fr_count": 35, "task_count": 155, "fr_ceiling": 120, "task_ceiling": 160}, "reasons": [], "checked_at": "2026-11-09T10:34:23Z"}`; EXIT 0 — 155 ≤ 160 | PASS |
| G4 decision-tensions | `python3 .specify/scripts/python/validate-decision-tensions.py --spec .specify/specs/093-concurrency-by-default` | `status: ok`; `[dtr-anchor]` `[dtr-section-missing]` `[dtr-record-incomplete]` `[dtr-tension-id]` `[dtr-rejected-form]` `[expected-sacrifice-unmapped]` all `pass (0)`; `scanned: 468 lines, 5 record(s)`; `channel: value_domain=HIGH-or-0, high=0`; `0 error(s), 0 warning(s)`; EXIT 0 | PASS |

Clause re-measure (T006's command, § 1 item 4): 18 / 22 / 22 / 18 / 14 = **94**, EXIT 0.

## 3. Observations

- **O-1 (LOW, wording only)**: T006's trap-form parenthetical — "the same grep without the `^- ` anchor also matches ids cited inside prose and returns a larger number" — does not reproduce on today's corpus: the bold pattern without the anchor still returns **94** over the five files. The inflation only appears when the bold markers are dropped (`grep -c 'C-[0-9][0-9][0-9]'` → 135 lines / 144 occurrences). The operative instruction ("re-read it in the same command rather than trusting this figure") and the count itself are correct; the example is imprecise.
- No other anomaly, no in-passing repair made by this worker (read-only throughout).

**ANOMALY: O-1 only — T006's trap-form example is not reproducible as literally worded (anchored vs bold-unanchored grep both yield 94; un-bolded grep yields 135/144); the stated count 94 is correct and re-verified. No gate, row, or manifest defect found.**

FVA: PASS
