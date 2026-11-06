# Analyze Repair — Round 1 (087-arch-diagram-docs)

- Object: `.specify/specs/087-arch-diagram-docs/` @ worktree `line/087-arch-diagram-docs`, base `24cb4edc`
- Input: `test-evidence/analyze-report-round1.md` (verdict `fail`; 0 CRITICAL / 2 HIGH / 7 MEDIUM / 7 LOW)
- Mode: bounded repair round after the `analyze` quality gate — **not** a stage. No state-spine write, no stage wrap-up.
- Category quadruple: `flow_class=execution；source=declaration；marker=；error=-`
- Verdict: **both HIGH closed; 5 of 7 MEDIUM closed, 1 recorded as-is, 1 escalated; 7 of 7 LOW closed.** One item escalated (see § Escalated).

---

## HIGH — closed

### F-01 — clause → assertion/`green` binding rebuilt by actual clause subject

**Root cause found (and it changes the arithmetic the analyze report assumed).** The analyze report states the flow
contract has **24** clause ids (`C-001`…`C-023` + `C-008a`) and asks for 40 claims in total. `C-008a` is **not a
machine-decidable clause id**: the clause-syntax owner
(`.specify/shared/definitions/contract-clause-definitions.md` § 1) fixes the id form as `C-<digits>` with at most one
**decimal** suffix, and the canonical regex of § 2 is `\*\*C-\d+(?:\.\d+)*\*\*`. The contract writes
`- **C-008a — Reconcile 的收敛路径（P1-5，**MUST 可判定地收敛到零图 finding**）**`, whose digits run into ` —`, so the
marker does not match. Measured:

```text
clause_extract.form_of(flow-obligations.contract.md)  -> md-bold-closed
clause_extract.extract_clauses(...)                   -> 23 ids (C-001…C-023)
clause_extract.resolvable(..., "C-008a")              -> False
```

A `[green:]` claim on `C-008a` is therefore reported as `green-dangling` **and the report is correct** — no machine can
check the claim. The decidable universe is **39 ids** (16 diagram + 23 flow), not 40.

**What was rebuilt.**

| contract | claiming row | test file | clauses claimed |
|----------|--------------|-----------|-----------------|
| `diagram-obligation` | **T008** | `tests/unit/test_docs_utils_obligation.py` | `C-001`…`C-013` (13) |
| `diagram-obligation` | **T030** | `tests/integration/test_docs_obligation_scenarios.py` | `C-014`…`C-016` (3) |
| `flow-obligations` | **T035** | `tests/integration/test_docs_command_scenarios.py` | `C-001`…`C-023` (23) |

**40/40 requirement, restated honestly:** `39/39` decidable ids are each claimed **exactly once**;
`C-008a` carries no `[green:]` tag by design and its delivery is carried by named assertions instead
(`I::test_c008a_second_reconcile_zero_findings`, `I::test_c008a_exemption_does_not_block_convergence`,
`I::test_c008a_r3_r4_r5_wiring`) plus `plan.md` § Test Plan table B's own `C-008a` row. This is stated in
`tasks.md` § Clause-partition note and in `plan.md` § Test Plan preamble, so the boundary is visible rather than papered over.

Partition model: a claim belongs to the **test file**, and one file is one green point, so a single row may carry many
`[green:]` tags (all clauses that file's assertions pin). Three claiming rows, three test files — which is why
`validate-tasks.py` reports **zero** `green-clause-collision`, **zero** `green-path-divergence` and **zero**
`green-cross-phase` over this file.

**Table A (diagram, 16 rows) — misalignments fixed.** Each row was re-bound to its contract heading's true subject:

| clause | true subject | v1 table A said | now |
|--------|--------------|-----------------|-----|
| `C-002` | Read-only by construction | "只读 / 确定性 / 幂等" (determinism is `C-006`) | split: `C-002` = zero-write assertions |
| `C-006` | 确定性、幂等、零写 | "JSON 载荷与字段序" (that is `C-013`) | `I::test_c002_two_runs_identical_json`, `U::test_c002_two_runs_identical_payload`, `U::test_c006_field_order_stable` |
| `C-009` | `stale` 第二半（部分覆盖） | "单一落点" (that is flow `C-009`) | `U::test_c009_reference_unresolved_not_stale`, `U::test_c009_unrecorded_target_not_evaluated`, `U::test_c009_semantic_half_has_no_verdict` |
| `C-013` | Payload 形态（含 `converged`/`clean`） | "计数、`converged` 与 `clean`" | payload schema + `test_c006_payload_schema` + the five predicate assertions |
| `C-015` | 与既有 `validate` 的关系（不复用、不合并） | "退出码" | `U::test_c015_validate_not_merged`, `U::test_c015_validate_zero_new_violations`, `U::test_c015_judged_together_in_r6`; exit codes moved to `C-001` where the command surface actually defines them |

**Table B (flow, now 24 rows) — rebuilt.** v1 had 23 rows with `C-008` missing and every row from `C-003` onward
carrying the next clause's subject. Rebuilt as 24 rows, one per clause id, each with a named assertion and a `red-when`,
covering the analyze report's specifically named gaps: `C-004` (`F::test_c004_refusal_carried_through`, the three
`draw-diagram` refusal points), `C-005` (shared-diagram de-dup), `C-006` (engine stickiness), `C-008` (Authoring Flow
R2/R5/R6 wiring), `C-010` (tiered confirmation unchanged), `C-019` (no new command/tier), `C-021` (path unchanged),
`C-022` (report carries the four evidences).

**The 7 formerly-unclaimed clauses, now covered:** diagram `C-014` (table A row `C-014`, guard relations) and flow
`C-007`, `C-009`, `C-021`, `C-022`, `C-023` (table B rows of the same ids) are all bound; flow `C-008a` is bound by named
assertions and is deliberately untagged (see above) rather than falsely claimed.

**False preamble claim fixed.** `plan.md` § Test Plan preamble no longer says tables A/B cover "全部条目" unqualified;
it now states 16 + 24 = 40 rows, one per clause, and names the `C-008a` non-decidability boundary explicitly.

**Row count preserved.** An earlier draft of this repair added 15 assertion rows (T077–T091), which pushed
`decomposition-check.py --mode tasks` to `split-required` (`task rows=91 exceeds ceiling 80`). Those rows were folded
into the existing assertion row **T035**, whose description now enumerates one named assertion per flow clause by subject.
`tasks.md` is back to **76 rows (T001–T076, contiguous, no gaps)** and decomposition returns `proceed`.

### F-02 — "docs/ zero change" narrowed to "except `docs/concepts/documentation-model.md`"

Four sites narrowed consistently (FR-001's reader-projection requirement kept intact, not deleted):

| site | v1 | now |
|------|----|-----|
| `plan.md:46` § traceability table | `git diff --name-only … -- docs/` 为空 | 恰为一行 `docs/concepts/documentation-model.md`；该目录下任何第二行即违约 |
| `plan.md:~380` baseline table | `docs/` 树零改动 | 只改动该一个文件；计划期实测为空，交付后预期恰为一行 |
| `tasks.md` GATE-6 | `-- docs/` is empty | returns exactly one line, `docs/concepts/documentation-model.md`；a second path is the failure |
| `tasks.md` T073 / quickstart S8 | S8 为空 / `docs/` 零改动 | names at most `docs/concepts/documentation-model.md` and nothing else；另说明「多一行即违约」 |

`tasks.md` T044's end-to-end check was narrowed the same way. `DoD-7`, `plan.md` § Delivery Surfaces, `T064` and FR-001
itself were left alone, so the change is a narrowing of the negative constraint, not a weakening of the positive one.

---

## MEDIUM — dispositions

| id | disposition | where |
|----|-------------|-------|
| **E-01** FR-012 / FR-021 task rows + flow `C-004` assertion | **closed.** FR-012 now lives in `T040` (tagged `FR-012`; the three `draw-diagram` refusal points carried through verbatim) and `T048` on the authoring side; FR-021 lives in `T041` (tagged `FR-021`; dry-run plan + tolerance band + stop-and-confirm, no content-destroying reclassification) and in `F::test_c022_no_destructive_reclassification` inside `T035`; flow `C-004` has `F::test_c004_refusal_carried_through` | `tasks.md` T040, T041, T035 |
| **E-02** coverage baseline missing ⇒ exit 2 | **closed by freezing.** `coverage-baseline.txt` created from the freezer's own output (573 names, base-sha `47a59449c324`, 266 files). Re-run now reports `[clause-uncovered] pass (573) — 573 uncovered, **0 beyond the frozen baseline**` | `coverage-baseline.txt` |
| **F-03** `C-004` five-value order duplicates `C-016` | **closed.** The `recorded-exemption > missing > not-evaluated > stale > satisfied` sentence is deleted; `C-004` now states the order is not declared there and that `C-016`'s nine-row table is the single owner | `contracts/diagram-obligation.contract.md` |
| **C-01** fixture invariant vs E6 "deleted" states | **closed, one reading chosen.** "The repository copy is the pre-deletion green state" is replaced by "the repository copy == the state E6 registers for that fixture"; fixtures whose registered state is legitimately red (`deleted-rendered/`, `orphan-*`, `no-diagram/`, `no-trace/`, `trace-incomplete/`, `exempt-bad/`, `exempt-superseded/`) keep their red state as the fixture fact. Writing/deleting cases still `copytree` to `tmp_path`. Criterion in one line: **repo copy == E6 row; any test-induced difference exists only in `tmp_path`** | `data-model.md` § E6 |
| **F-04** T076 writes `tasks-stage-status.jsonl` | **closed.** renamed to `test-evidence/implement-stage-status.jsonl` | `tasks.md` T076 |
| **F-05** `feature-ref.md:30` non-existent mirror paths | **closed.** `.specify/skills/external/**` and `.specify/templates/**` replaced by the real `.specify/skills/<name>/**` + `.specify/templates/commands/docs.md` + the four per-tool copies, with an explicit note that the mirror has no `external/` layer (verified by `ls`) | `feature-ref.md` row 10 |
| **G-01** `register.md` OI-087-01 still `open` | **closed.** marked `resolved (2026-11-06, owner /speckit.checklist)` with the N6 evidence pointer; `plan.md` § Inherited Blockers and § Residual Risk prose synced to the resolved state | `register.md`, `plan.md` |

## LOW — dispositions (all closed)

| id | fix |
|----|-----|
| **G-02** feature detail stale | `Last Updated` and a new `Latest Review` entry record the checklist stage + tasks stage + this repair round; Feature stays `Planned` |
| **F-06** "6 处文本落点" vs "5 处落点" | `plan.md` now says **5 处文本落点 / 4 个文件**, matching `data-model.md` E7's five rows (verified by counting the table) |
| **C-02** `<BASE>` placeholder and spacing | all 5 occurrences → `--name-only 24cb4edc` |
| **F-07** table C merged three files | split into one row per guard file: `test_expression_compatibility.py` (`C5`), `test_expression_gate_wiring.py` (`A1/A3/A5`), `test_docs_command_template.py` (`C3/C4a`), `test_confirmation_gates_sweep.py` (`KEEP_LIST`), `test_directory_governance.py` |
| **F-08** trace record R5/R6 | `data-model.md` now reads "**R5 写**（产图的同一次运行），**R6 只读**" |
| **F-09** trace filename shape | pinned uniquely in `C-010`: `<UTC basic>-<8 hex>-diagram-trace.json`, with both segments defined; `data-model.md` E4 aligned |
| **A-01** 49 vs 74 denominators | new `plan.md` baseline row states **74 = 25 non-wiring templates + 49 non-wiring skills**, citing the guard's docstring and `assert len(manifest) == 74`; `FROZEN_SKILLS` is the 49 half |

---

## Gate readings (verbatim)

1. `python3 .specify/scripts/python/validate-tasks.py .specify/specs/087-arch-diagram-docs/tasks.md`
   → `PASS: … 0 error(s), 0 warning(s)` / **exit 0**
2. `python3 skills/external/sdd-loop-driver/scripts/decomposition-check.py --mode tasks --requirements .specify/specs/087-arch-diagram-docs/requirements.md --tasks .specify/specs/087-arch-diagram-docs/tasks.md`
   → `{"mode": "tasks", "decision": "proceed", "measured": {"fr_count": 23, "task_count": 76, "fr_ceiling": 60, "task_ceiling": 80}, "reasons": []}` / **exit 0**
3. `python3 skills/external/sdd-loop-driver/scripts/pre-analyze-check.py --spec-dir .specify/specs/087-arch-diagram-docs --stage tasks --repo .`
   → `stage=tasks decision=pass errors=0 advisories=84 waived=0` / **exit 0** (all 84 advisories are the single known class: paths that exist only at implementation time, plus the two deliberately-absent `diagrams/` counter-example directories)
4. `python3 .specify/scripts/python/validate-decision-tensions.py --spec .specify/specs/087-arch-diagram-docs`
   → `scanned: 577 lines, 5 record(s)` / `0 error(s), 0 warning(s)` / **exit 0**
5. `python3 .specify/scripts/python/validate-requirements.py .specify/specs/087-arch-diagram-docs/requirements.md`
   → `scanned: 314 lines, 33 definition rows` / `0 error(s), 0 warning(s)` / **exit 0** (unchanged; no FR/SC edited)
6. `python3 .specify/scripts/python/account-clause-coverage.py .specify/specs/087-arch-diagram-docs`
   → `[clause-uncovered] pass (573) — 573 uncovered, 0 beyond the frozen baseline` (**E-02 resolved**)
   → `[fr-uncovered] fail (7) — 16 of 23 FRs cited from citation groups`; `7 error(s)` / **exit 1**
   **Recorded as-is, not greened.** The 7 are `FR-005, FR-011, FR-012, FR-014, FR-016, FR-020, FR-021` — a *pre-existing*
   property of how FRs are cited from clause citation groups (the analyzer counts only the last parenthesised `FR-…` group
   per clause). It is **not** in F-01's scope (F-01 is clause↔assertion binding, which now passes at 0 beyond baseline),
   and the baseline deliberately excludes this feature's own spec, so the frozen baseline cannot mask it. Fixing it would
   mean rewriting contract citation groups — a contract-semantics change, so it is left visible.
7. `audit-plan-changes.py` → run post-commit; see the commit record.

## PLAN-EDIT declarations (plan-owned artifacts, all minor)

- `PLAN-EDIT: .specify/specs/087-arch-diagram-docs/plan.md — 表 A/B 按条款实际主体重建 + 前置声明改为如实的 16+24 行与 C-008a 边界 + 表 C 按文件分行 + F-02 收窄 + F-06/A-01/G-01 计数与散文订正；分类=minor`
- `PLAN-EDIT: .specify/specs/087-arch-diagram-docs/data-model.md — E6 夹具不变量定为「仓库副本 == E6 登记构成」+ E4 的 R5 写/R6 读与追溯记录文件名形态对齐 C-010；分类=minor`
- `PLAN-EDIT: .specify/specs/087-arch-diagram-docs/contracts/diagram-obligation.contract.md — 删除 C-004 的五值顺序句（顺序唯一归 C-016）+ C-010 钉死追溯记录文件名形态；分类=minor`
- `PLAN-EDIT: .specify/specs/087-arch-diagram-docs/quickstart.md — S8 的 docs/ 口径收窄为「除 documentation-model.md 外，多一行即违约」；分类=minor`
- `PLAN-EDIT: .specify/specs/087-arch-diagram-docs/feature-ref.md — 镜像路径订正为真实的 .specify/skills/<name> + 四家 per-tool 副本；分类=minor`

No FR/SC id, numbering or semantics was changed; no new `/speckit.*` command, no second engine, no second delivery
contract, no docs full diagram backfill.

## Escalated (one item, needs adjudication — not silently taken)

**`flow-obligations` `C-008a` cannot carry a machine-decidable claim.** The analyze report's F-01 asks for the 40-id
partition; `C-008a`'s letter suffix is outside the clause-syntax owner's id form, so 40 is not expressible. The repair
delivers 39/39 machine-decidable claims plus `C-008a`'s content via named assertions and an honestly-labelled table row.
Making it decidable requires either renaming the clause to an owner-legal id (e.g. `C-008.1`) or amending
`shared/definitions/contract-clause-definitions.md` to admit letter suffixes — both are contract-semantics changes and are
therefore **returned to the orchestrator rather than taken here**. Everything else in this round is closed.

## Evidence

- Analyzer findings: `test-evidence/analyze-report-round1.md`
- Coverage baseline: `coverage-baseline.txt` (573 names, base-sha `47a59449c324`, 266 files)
- Claims census (measured via the validator's own API): 39 claims, 39 unique — 16 `diagram-obligation`, 23 `flow-obligations`
- This file is the run's evidence pointer for the repair round.
