# Analyze Repair Record — Round 1 (111-general-best-practices)

**Stage**: analyze-repair · **Baseline**: `4f6905a95` · **Run**: `r20261127T071500Z-111a` · **Date**: 2026-11-27
**Brief**: `.specify/.tmp/sdd-loop/tmp/general-best-practices/brief-analyze-repair.md` · **Findings**: [`analyze-round1-findings.jsonl`](./analyze-round1-findings.jsonl) (1 CRITICAL / 2 HIGH / 3 MEDIUM / 6 LOW)
**Scope**: the three blocking findings only — AR1-02 (CRITICAL), AR1-01 (HIGH), AR1-03 (HIGH). Non-blocking findings AR1-04…AR1-12 are outside this assignment; their routing stays with the driver.

## 0. Verdict

All three blocking findings resolved by repairing the cause, not by weakening a contract:

| Finding | Sev | Resolution (one line) | Recorded as |
|---------|-----|----------------------|-------------|
| AR1-02 | CRITICAL | The module manifest's 逐步积累机制 section is declared the **owner of the promotion procedure, the generality criterion and the `**来源**` shape**; `knowledge-promotion.md` is cited only for the knowledge-recording obligation it actually owns; C-305 no longer forbids what C-302/T009 require. | A-22 |
| AR1-01 | HIGH | The observation form now uses the engine's real carrier — the [[STR-001]] marker and owner-file stem travel in the record's `--review` text — and declares a legal ad-hoc identity (`custom:best-practices/observation` + `--unit-type custom-unit` + `bp-<yyyy-mm-dd>-<slug>` run id, with the probe-system external-probe prerequisite). | A-23 (form rules in A-17) |
| AR1-03 | HIGH | The task graph now creates the mirror **before** the US1 green checkpoint (new row T007A after T007, before T008); C-404's module-read prelude is preserved unchanged, so the citation-existence assertion is satisfied rather than relaxed. | A-24 |

## 1. Engine measurements behind AR1-01 (taken this stage)

All probes were read-only against the working tree; the one recording exercise targeted a scratch workspace under the sanctioned `.specify/.tmp/` root and was deleted afterwards.

1. `python3 .specify/scripts/python/feedback-utils.py --action args-manifest` → `record` required `["--unit-id","--run-id","--review","--points"]`, `source: []`; the parser declares `--notes` but `action_record` never reads it (`feedback-utils.py:832-961`) and `compose_entry` writes only frontmatter + `## Review` + `## Optimization Points` (`:345-351`).
2. Scratch record, no probe registry (legacy path): `--unit-id custom:best-practices/observation --unit-type custom-unit --run-id bp-2026-11-27-clone-proto --review '[best-practice] programming-tools — ...' --points '...'` → rc 0; the entry's `## Review` section carries the marker and stem verbatim; no `notes` key exists in the frontmatter.
3. Same record with a probe registry present → rc 2, `error: no probe object for unit: custom:best-practices/observation` — the ad-hoc convention needs the custom unit's external probe (`probe-utils.py --action probe-inject`, class `external-custom`; `probe-utils.py:1427,1469,619-668`).
4. Same registry, `--unit-id /speckit.implement --unit-type command` → rc 0 — a command/skill run's own unit resolves through its wrap-up probe object, which is why A-17 prefers that identity when the friction arises inside a framework run.
5. `shared/guidelines/knowledge-promotion.md` sections are `1 记录义务` / `2 强调升级:2+ → 主流程` / `3 反模式`; both the target copy and the source copy (`ai-harness/shared/guidelines/knowledge-promotion.md`, identical except the `/ah.` → `/speckit.` adaptations) define **no** feedback → category-owner-file promotion and no "recurrence or one explicit user correction" criterion. Source 087's own requirements/plan/contract only cite the path (requirements.md:36, plan.md:11-12,28, best-practices.contract.md:4,22), so the source never declared a different owner — the target declares the manifest.

## 2. Finding → resolution → files changed

### AR1-02 — promotion-rule ownership (CRITICAL)

- **Cause repaired**: the spec attributed a rule to an owner that does not define it, while forbidding the only surface that could carry it. Ownership now lives where the shipped rule actually lives: the manifest received by every client project.
- **Ownership split now stated everywhere**: manifest (`shared/best-practices/README.md` § 逐步积累机制) owns the promotion procedure + generality criterion + `**来源**` shape; `scripts/python/feedback-utils.py` owns the record shape/store/disposal; `shared/guidelines/knowledge-promotion.md` owns the knowledge-recording obligation and emphasis escalation — cited by pointer only.
- **C-305 rewritten** so its MUST NOT list names exactly the owners' rules the module may not restate (feedback disposal, knowledge-promotion emphasis threshold, owner enumerations) and states that declaring the module's own promotion rules is ownership, not restatement.
- **Files**: `requirements.md` (A-4, A-17, A-22 new, binding basis, 不做什么, US2 goal/why/test/scenario 2-3, FR-004, Key Entities, RS-002, SC-003, Clarifications session), `contracts/accumulation.contract.md` (header, C-301 context, C-302, C-304, C-305), `contracts/manifest.contract.md` (C-104(c)), `plan.md` (Summary, Constitution Check row XIV, Decision Tensions, EP-002), `research.md` (M3, R-5), `data-model.md` (owner statement, E2, E7, E8, INV-08), `tasks.md` (US2 goal/test, T009, Notes), `quickstart.md` (S-4), `feature-ref.md` (binding basis, delivery row 1, FR-004 row, SC-003 row, hand-off).

### AR1-01 — non-executable observation form (HIGH)

- **Cause repaired**: the declared carrier (`notes`) does not exist in the engine; the declared identity had no ad-hoc convention.
- **New form**: `--review` text carries [[STR-001]] + exactly one owner-file stem; record shape and remaining arguments stay with the engine's `--help`; identity = the command/skill run's unit id + run id, or `custom:best-practices/observation` + `--unit-type custom-unit` + `bp-<yyyy-mm-dd>-<slug>`, with the probe-inject prerequisite owned by the probe system.
- **Files**: `requirements.md` (A-17 rewrite, A-23 new, FR-004, Key Entities Observation, US2 scenario 1, Clarifications), `contracts/accumulation.contract.md` (C-301), `data-model.md` (E7 rows `review_marker` / `review_stem` / `unit_convention`), `tasks.md` (T009), `plan.md` (Summary, EP-002), `research.md` (M3 addition, R-5), `feature-ref.md` (no form text — inherits).

### AR1-03 — impossible task order (HIGH)

- **Cause repaired**: the guard's prelude requires `.specify/shared/best-practices/` to exist, but the mirror was created after the green checkpoints. The repair moves mirror creation earlier instead of weakening C-404.
- **Task graph**: inserted `T007A` (write-mode `sync-mirrors.py` after T005/T006/T007, before T008; no `[green:]` claim), `T008` blockedBy now `T005, T006, T007, T007A`; T012 stays the final fan-out after the accumulation section and map row; T013's 122-file reading still closes the mirror.
- **Files**: `tasks.md` (T007A new, T008 blockedBy, US1 dependency line, doc-feature flow line, Requirement Coverage Map FR-006 row), `requirements.md` (A-24 new, Clarifications), `feature-ref.md` (work packages). `contracts/distribution-guard.contract.md` C-404 and T004's prelude text are **unchanged**.

## 3. Gates re-run (real output, this stage)

| Gate | Command | Result | Evidence |
|------|---------|--------|----------|
| Requirements validator | `python3 .specify/scripts/python/validate-requirements.py .specify/specs/111-general-best-practices/requirements.md` | `status: ok`, 0 error / 0 warning, 229 lines, 16 definition rows, 7 shared strings, exit 0 | [`analyze-repair-requirements-validator.txt`](./analyze-repair-requirements-validator.txt) |
| Pre-analyze (tasks) | `python3 .specify/skills/sdd-loop-driver/scripts/pre-analyze-check.py --spec-dir .specify/specs/111-general-best-practices --stage tasks --repo .` | `decision=pass`, errors 0, advisories 150 (all the expected pre-implementation missing-path / external-clause class), tasks 20, clauses 24, FR 9, SC 7, exit 0 | [`analyze-repair-pre-analyze.txt`](./analyze-repair-pre-analyze.txt), [`analyze-repair-pre-analyze.json`](./analyze-repair-pre-analyze.json) |
| Tasks validator | `python3 .specify/scripts/python/validate-tasks.py .specify/specs/111-general-best-practices/tasks.md` | PASS, 0 error / 0 warning, exit 0 | [`analyze-repair-tasks-validator.txt`](./analyze-repair-tasks-validator.txt) |
| Workspace guard (stage signature) | `workspace-guard.py --snapshot …/workspace-analyze-repair.json` then `--check …` | `status: clean`, `changed: []`, exit 0 | [`workspace-analyze-repair.json`](./workspace-analyze-repair.json), [`workspace-analyze-repair-check.json`](./workspace-analyze-repair-check.json) |
| Workspace guard (cross-stage, checklist → now) | `workspace-guard.py --check …/workspace-checklist.json` | `status: drift`, `changed: ["refs"]` — `refs/heads/109-prompt-adherence` removed and `refs/heads/112-decision-batch-panel` added by a **parallel line**; branch, HEAD and the `.specify/specs` listing unchanged (specs identical, refs count 215 both sides). Not caused by this stage; disclosed, and the fresh stage signature above reads clean. | [`workspace-analyze-repair-vs-checklist.json`](./workspace-analyze-repair-vs-checklist.json) |

## 4. Containment reading for this stage

Writes of this stage: this feature's spec artifacts (`requirements.md`, `plan.md`, `research.md`, `data-model.md`, `contracts/*.md`, `quickstart.md`, `feature-ref.md`, `tasks.md`, `test-evidence/analyze-repair-*`, this record) plus the committed accounting records the driver's engines produce — all inside FR-009's declared set. The scratch feedback drill lived under the sanctioned git-ignored `.specify/.tmp/` root and was removed; no engine, template, skill, agent, command, constitution/instruction, store-layout or decision-governance path changed; no registry edit; no push.

**Anomaly line**: `ANOMALY: workspace-guard cross-stage check reports external ref drift (refs/heads/109 removed, refs/heads/112 added by a parallel line) — disclosed, not caused by this stage; fresh stage signature is clean.`