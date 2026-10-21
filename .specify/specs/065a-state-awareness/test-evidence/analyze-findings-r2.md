# Analyze Findings Round 2 — Feature 065 / Slice `065a-state-awareness`

**Date**: 2026-10-21
**Branch**: `065-loop-interruption-recovery` (HEAD `2c2b0be1`)
**Scope**: delta verification only. Round-1 baseline `.specify/specs/065a-state-awareness/test-evidence/analyze-findings.md`; remediation commits `f90fc9ef` and `daac5081`; changed files `requirements.md`, `contracts/*` ×4, `data-model.md`, `plan.md`, `research.md`, `tasks.md`, `feature-ref.md`, `quickstart.md`, `coverage-baseline.txt`, `.specify/memory/features.md`, `.specify/memory/features/065.md`.
**Mode**: strictly read-only. The only write is this report. No repository artifact, feature registry, state spine, feedback store, session store, or commit was touched. No `--freeze` was run. No fresh-context validation subagent was dispatched (per stage instruction; delta verification was judged directly).
**Rerun delta**: Round 1 reported **1 CRITICAL + 6 HIGH + 12 MEDIUM + 1 LOW** (20 findings, I-03 rejected). This round verifies those IDs against `f90fc9ef`/`daac5081` and scans the changed files for regressions/new contradictions.

## Overall verdict

**NOT READY — 1 CRITICAL + 1 HIGH remain.**

`C-01` (CRITICAL) is only partially fixed: the slice now pins FR-004 as the derived-table owner and the contracts/data-model agree, but the unchanged FR-043, the unchanged parent FR-004, and `research.md` R-13 still assign ownership of the same table/rules to the reference document. The remediation relocated the conflict instead of resolving it.

The G-03 fix introduced a new HIGH (`N-01`): action-matrix row 6 is over-broad and makes the terminal-state rows 11/12 unreachable whenever artifacts are complete and the commit baseline is unknown.

All other Round-1 CRITICAL/HIGH IDs (`I-01`, `G-01`, `I-02`, `F-01`, `G-03`'s original gaps, `A-01`) are fixed. The MEDIUMs are fixed except `I-04` and `I-05`, which remain MEDIUM residuals, and `G-04`, which is fixed with a LOW ambiguity.

## Delta verification

| ID | R1 severity | R2 status | Evidence (current tree) | Note |
|----|-------------|-----------|-------------------------|------|
| **C-01** | **CRITICAL** | **partially-fixed — CRITICAL remains** | `requirements.md:139` FR-004 now says "本表的唯一 owner 是本条（parent #FR-004）；`references/state-awareness.md §Derived Mapping` 与 `loop-state.py` 的映射 MUST 仅为该表的镜像…除本条外任何位置 MUST NOT 声称拥有该表"; `data-model.md:71` and all four contract owner notes agree. **But** `requirements.md:156` FR-043 is unchanged: "状态感知/中断/恢复规则 MUST 在技能内有一个唯一 owner 文档（references 下的专门文件或章节）…引用而非复述判定表"; parent `065-loop-interruption-recovery/requirements.md:186` FR-004 is unchanged: "映射表由 FR-043 的唯一 owner 文档定义，代码与测试引用它"; `research.md:188` R-13 still says the new owner reference **"拥有：… derived 映射 … 动作建议表"**; `tasks.md:175` T018 says the reference must contain only a mirror and "不得声称拥有该表"; `plan.md:44` says reference and code are mirrors, while `plan.md:99` calls it the "owner reference". | The chosen direction (FR-004 owns) was not propagated to FR-043, the parent, or research R-13. Slice and parent now contradict each other, and research contradicts T018. Constitution Principle XIV conflict is unresolved. |
| **I-01** | HIGH | **fixed** | `requirements.md:46` A-1: "`recover` 由 `065c` 承接，`check-spine` 由 `065b` 承接"; `contracts/loop-state-cli.md:25` C-2 pins `check-spine → owner=065b`, `recover → owner=065c`; `tasks.md:142` T003 and `:143` T004 assert both; `research.md:37`, `feature-ref.md:19`, `plan.md:9` agree with `notes/decomposition-gate.md`. | Per-action pinning is explicit and testable. |
| **G-01** | HIGH | **fixed** | Four contracts renumbered to canonical `C-1`…`C-60` with alias tables (`loop-state-cli` C-1–C-18, `snapshot-envelope` C-19–C-32, `interruption-and-action` C-33–C-49, `stage-artifact-map` C-50–C-60). Re-run: `account-clause-coverage.py` → `claimed clauses 60`, `FR claimed 25 / uncovered 0`, `status: ok`, exit 0; SC-001…SC-006 all cited. `tasks.md:20` DoD-3 and `:52` now use the canonical form and the accountant. | Machine-decidable under the owner syntax. Residual LOW `N-02`: `pre-analyze-check` prints `clauses: 0` (see below). |
| **I-02** | HIGH | **fixed** | `requirements.md:138` FR-003 removed "watcher 不可用" from the `unknown` examples; `:140` FR-005 defines the three states; `data-model.md:124` explicitly excludes unavailable from `unknown`; `:160-166` §4.3 table; `contracts/snapshot-envelope.md:49-56` C-25 table; Q2/Q5 ledger at `requirements.md:275,327`. | One MUST-level mapping for unavailable: `present=false`, `status=missing`, `value_state=na`, `reason=unavailable`. |
| **F-01** | HIGH | **fixed** | `requirements.md:15` and `:250` now say no new Feature ID/row and that plan owns Draft→Planned per Feature Integration; no absolute "MUST NOT 改写注册状态" remains. `plan.md:32,171`, `feature-ref.md:64` align; registry is `Planned`. | Registry not rolled back; the stale requirements sentence is repaired. |
| **G-03** | HIGH | **fixed for the original gaps; new HIGH N-01 introduced** | `contracts/interruption-and-action.md:49-56` C-46 owns the `提交齐备` predicate and adds rows 5/6; `contracts/stage-artifact-map.md:43` C-53 analyze vacuous `artifacts.complete=true`; `:53` C-57 unknown baseline; `:56` C-60 implement; `tasks.md:161` T007 tests analyze DONE, commit-required=false DONE, unknown baseline, clarify no-change. | The original analyze/clarify/unknown-baseline gaps are closed. The new row 6 is over-broad; see `N-01`. |
| **A-01** | HIGH | **fixed** | `requirements.md:137` FR-002 defines required input (`--line-id`, explicitly supplied `--probe`) vs evidence source and pins probe/local mutual exclusion + exit 2; `:147` FR-012; `contracts/loop-state-cli.md:32-39` C-6 table; `:44` C-8; `data-model.md:183`; `tasks.md:162` T008 matrix. | Unreadable evidence source → `missing` + exit 0; unreadable required argument/probe → exit 2. |
| **G-02** | MEDIUM | **fixed** | `coverage-baseline.txt` committed (497 lines; header `frozen-from: .specify/specs/*/contracts/* excluding 065a-state-awareness`, `base-sha: 095c291ae2ab`, 495 names). Re-run accountant: `baseline … (495 names)`, `[coverage-baseline-delta] pass (0)`, status ok. | Baseline is present and consumed; no `--freeze` was run by this analyze. |
| **I-04** | MEDIUM | **partially-fixed — MEDIUM residual** | `requirements.md:64` SA-1 now explicitly defers `stale-unisolated → stop` to 065c and says 065a "不因单纯 stale 改变候选动作"; `contracts/interruption-and-action.md:43` C-43 matches; `tasks.md:161` T007 tests it. **Residual**: `requirements.md:126` Edge Cases still says combined forms "动作按父 C 区优先级裁决", and the parent C-area priority includes `stale-signal` unisolatable → `stop`. That conflicts with C-43's stale exclusion. | Align the Edge Case sentence with SA-1/C-43 or scope the parent-priority reference to non-stale forms. |
| **A-02** | MEDIUM | **fixed** | `requirements.md:56` A-14 adds the deterministic not-dispatched criteria, `--stage` as intent, `na` for four-piece/watchbeat/artifacts/commits, and the "spine exists with non-empty `spine_state`" exclusion; `contracts/interruption-and-action.md:29` C-35; `contracts/loop-state-cli.md:40` C-7 defines `stage=null` and artifacts `value_state=unknown`/`missing`; `data-model.md:125,266`. | The stage-source gap is resolved by explicitly choosing `stage=null` + unknown artifacts rather than a spine stage source. |
| **A-03** | MEDIUM | **fixed** | `requirements.md:137` FR-002 pins `--probe` mutual exclusion with `--spine/--state-dir/--spec-dir/--repo/--watch-script`, exit 2, no local evidence; `contracts/loop-state-cli.md:62` C-13; `quickstart.md:84`; `tasks.md:162` T008. | Explicit rejection, not precedence. |
| **A-04** | MEDIUM | **fixed** | `requirements.md:139` FR-004 defines the completion sentinel as "日志最后非空行 `== <STAGE>-DONE`"; `contracts/interruption-and-action.md:40` C-40, `:42` C-42, `contracts/snapshot-envelope.md:69` C-31, `data-model.md:136,257`; `tasks.md:161` T007 adds the sentinel + live process + later `ANOMALY:` case. | `false_completion` is defined as the exclusive other side of `artifacts-without-completion`, not as an inexact inverse. |
| **U-01** | MEDIUM | **fixed** | `contracts/loop-state-cli.md:49` C-10 requires target and parent `realpath`/`Path.resolve` before any temp file, comparison before creation, exit 2 with no file; `quickstart.md:125`; `tasks.md:142` T003 includes symlink/relative/state_dir-symlink tests. | No-write boundary is now canonicalized. |
| **G-04** | MEDIUM | **fixed (LOW residual N-04)** | `contracts/stage-artifact-map.md:47` C-54 requires a checklist file added/modified since `stage_base_commit`; pre-existing files do not satisfy; `research.md:116`; `tasks.md:168` T011. Residual: C-54 does not define `artifacts.complete` when `stage_base_commit` is unknown. | See `N-04`. |
| **G-05** | MEDIUM | **fixed** | `requirements.md:143` FR-008 now points to AM-09; `contracts/stage-artifact-map.md:54` C-58 enumerates `src/ skills/ scripts/ tests/ templates/ agents/` and excludes docs/`.specify`; `:56` C-60; `tasks.md:168` T011. | Doc-only commits are excluded from implement evidence. |
| **G-06** | MEDIUM | **fixed** | `tasks.md:214` T026 now drills both the `unwatched` removal and the `C-48` salvage-gate removal, with byte-restore and sha256 checks; `requirements.md:190` FR-046 mapping notes the slice split. | The salvage-gate drill is no longer deferred without evidence. |
| **I-05** | MEDIUM | **partially-fixed — MEDIUM residual** | Within the slice, `spine.consistent` (nested) is unified: `requirements.md:48` A-3, `:58` A-16, `:139` FR-004; `data-model.md:72`; `contracts/snapshot-envelope.md:26` C-20 and `:36` C-39 forbid a top-level alias; `tasks.md:142` T003. **Residual**: parent `065-loop-interruption-recovery/requirements.md:186` FR-004 still mandates flat `spine_consistent=false`. | Child forbids what the authoritative parent mandates. Amend the parent or record an explicit parent-level waiver. |
| **F-02** | MEDIUM | **fixed** | `.specify/memory/features.md` row 065 and `.specify/memory/features/065.md` Latest Review now contain a dated 2026-10-21 065a tasks-stage entry (30 tasks, validate-tasks pass, decomposition proceed); status stays `Planned`. | Tasks-stage record is present. |
| **F-03** | MEDIUM | **fixed** | The same notes now say the user decision is "拆三片，先 065a"; `065a-state-awareness` is the current active basis, `065b`/`065c` queued, `066` recorded as a parallel early split attempt and retained as history. | The older 066 entry uses dated present-tense wording but is superseded by the later dated decision; no further action required. |
| **L-01** | LOW | **fixed** | `tasks.md:103` maps T020 to FR-042; `:116` maps it to SC-005. | Coverage map is complete. |
| **I-03** | rejected in R1 | **no action** | Round-1 rejection stands; CHK014 is covered by the probe shape (b) predicate (`data-model.md` §6.2, `contracts/loop-state-cli.md` C-11–C-13, C-44). | Not a finding. |

## New findings (delta scan)

| ID | Severity | Category | Location(s) | Summary | Recommendation |
|----|----------|----------|-------------|---------|----------------|
| **N-01** | **HIGH** | inconsistency | `contracts/interruption-and-action.md:65` (row 6); `:70` (row 11), `:71` (row 12); `contracts/stage-artifact-map.md:53` C-57; `research.md:146`; `plan.md:136`; `tasks.md:161` T007 | Action-matrix row 6 is `(loop_state=DONE ∨ 产物齐备) ∧ commits.value_state=unknown → verify`. Because row 6 precedes rows 11 and 12, any line with complete artifacts and an unknown commit baseline is routed to `verify` regardless of state. `STALLED`/`REENTRY_REQUIRED` therefore never reach row 11 `stop`, and `ANOMALY`/`FAILED`/`DEAD`/`TIMEOUT`/`NO_SIGNAL` never reach row 12 `retry`. This contradicts C-46's own terminal rows and the parent C-area priority; it is most likely for legacy spines, where `stage_base_commit` is explicitly allowed to be `unknown` (A-11, C-57). T007 does not test any terminal-state + unknown-baseline combination. | Constrain row 6 to `loop_state=DONE` (the `产物齐备` disjunct is redundant for DONE, because FR-004 requires artifacts complete for DONE), or move it after rows 11/12 with explicit terminal-state exceptions. Update C-57/research/plan wording and add tests for `STALLED`/`ANOMALY`/`DEAD` + artifacts complete + unknown baseline. |
| **N-02** | LOW | tooling divergence | `test-evidence/remediation-account-coverage.txt`; re-run `pre-analyze-check.py` JSON summary | `pre-analyze-check` now reports `"clauses": 0` for canonical `C-N` contracts, while the owner accountant reports `claimed clauses 60`. No current artifact relies on the pre-analyze count (DoD-3 and tasks §Format use `account-clause-coverage.py`), so no coverage claim is false, but the gate field is misleading. | Treat the accountant as authoritative; do not use `pre-analyze-check`'s `clauses` field as coverage evidence. A framework-side regex fix is outside this slice. |
| **N-03** | LOW | duplicate-owner risk | `data-model.md:265` §8.14; `contracts/snapshot-envelope.md:44` C-23; `contracts/interruption-and-action.md:49-56` C-46; `contracts/snapshot-envelope.md:36` C-39 | `data-model.md:265` restates C-46's commit-ready predicate without citing C-46, and `snapshot-envelope.md:44` says the consistency criterion is defined in "`requirements.md` FR-004 与 `IA-07`", while C-39 is the detailed owner. These are summaries that a reader could act on without opening the owner. | Replace the restatements with references to C-46/C-39, or add an explicit "summary only, owner is C-46/C-39" marker. Non-blocking. |
| **N-04** | LOW | ambiguity | `contracts/stage-artifact-map.md:47` C-54 | When `stage_base_commit` is unknown for the `checklist` stage, "不猜完整" does not say whether `artifacts.complete` is `false` or `null`. If `false` and a sentinel is present, `false_completion=true` and the line is driven to `retry` on evidence that is actually unjudgeable. | Define `artifacts.complete=null` + `value_state=unknown` for an unknown base, or state that the conservative `false` reading is intentional and exclude it from `false_completion`. Non-blocking. |

## Load-bearing evidence (verbatim)

### C-01 — ownership conflict persists

- Slice FR-004 (`requirements.md:139`) now claims sole ownership: "本表的唯一 owner 是本条（parent #FR-004）；`references/state-awareness.md §Derived Mapping` 与 `loop-state.py` 的映射 MUST 仅为该表的镜像，并由契约测试验证逐项一致；除本条外任何位置 MUST NOT 声称拥有该表。"
- Slice FR-043 (`requirements.md:156`) is unchanged: "状态感知/中断/恢复规则 MUST 在技能内有一个唯一 owner 文档（references 下的专门文件或章节），SKILL.md 与各 references MUST 引用而非复述判定表".
- Parent FR-004 (`.specify/specs/065-loop-interruption-recovery/requirements.md:186`) is unchanged: "映射表由 FR-043 的唯一 owner 文档定义，代码与测试引用它。"
- `research.md:188` R-13 is unchanged: "新增 owner reference `references/state-awareness.md`，拥有：快照入口、六类检测表…、**derived 映射**、产物映射章节、probe 契约、**动作建议表**。"
- `tasks.md:175` T018 requires the reference to contain a mirror of FR-004 and "不得声称拥有该表"; `plan.md:44` calls reference/code mirrors, while `plan.md:99` calls the same file the "owner reference".
- Net result: FR-004 (slice), FR-043 (slice + parent), and research R-13 make three incompatible ownership statements about the same derived table. The remediation removed the data-model/contract duplicate but did not touch FR-043, the parent, or research.

### N-01 — row 6 preempts terminal rows

```
| 6 | （`loop_state=DONE` ∨ 产物齐备）∧ `commits.value_state=unknown` | `verify`（`reason=commit-baseline-unknown`） |
...
| 11 | `STALLED` ∨ `REENTRY_REQUIRED` | `stop` |
| 12 | 其余终态（`INCOMPLETE/ANOMALY/FAILED/DEAD/TIMEOUT/NO_SIGNAL`） | `retry` |
```

`产物齐备` is not restricted to DONE; it is a normal condition for `INCOMPLETE`, `FAILED`, `ANOMALY`, `DEAD`, `STALLED`, and `REENTRY_REQUIRED`. With `commits.value_state=unknown` (legacy/missing `stage_base_commit`, explicitly supported by A-11/C-57), row 6 wins before rows 11/12. The same rule is repeated in `research.md:146` and `plan.md:136`, and reinforced by `stage-artifact-map.md:53` C-57 ("动作路由按 C-46 的 `commit-baseline-unknown` 分支进入 `verify`"). T007 tests only non-terminal unknown-baseline cases.

## Deterministic evidence run (this round)

All commands were read-only; no `--freeze`, no writes to the slice other than this report.

- `python3 .specify/scripts/python/account-clause-coverage.py .specify/specs/065a-state-awareness` → exit 0; `claimed clauses 60`; `FR claimed 25 / uncovered 0`; `[coverage-baseline-delta] pass (0)`; `status: ok`.
- `python3 .specify/scripts/python/validate-tasks.py .specify/specs/065a-state-awareness/tasks.md` → `PASS — 0 error(s), 0 warning(s)`.
- `python3 .specify/scripts/python/validate-requirements.py .specify/specs/065a-state-awareness/requirements.md` → exit 1, **27 errors, all `id-contiguous`** (gaps FR-013–FR-037, FR-045, FR-048); `doc-order`, `ref-resolvable`, `marker-count`, `dup-id` all pass. SA-2 (`requirements.md:65`) explicitly declares only `id-contiguous` inapplicable to this slice; this is a documented waiver, not a new finding.
- `python3 skills/external/sdd-loop-driver/scripts/pre-analyze-check.py --spec-dir .specify/specs/065a-state-awareness --stage tasks --repo .` → `decision=pass errors=0 advisories=42 waived=0`; JSON summary `"clauses": 0` (see `N-02`); all advisories are expected missing implementation paths.
- `git status --short -- .specify/specs/065a-state-awareness` → no uncommitted slice changes before this report; `git show --stat f90fc9ef daac5081` confirms the 14-file remediation plus the one-line plan wording commit.

## Coverage and feature-link notes

- **Clause coverage**: 60/60 claimed under the owner syntax; FR 25/25; SC-001…SC-006 all cited. The 60 clauses are continuous C-1…C-60 with alias tables in each contract.
- **Coverage baseline**: present (495 names; base SHA `095c291a`; 065a excluded). G-02 closed.
- **Checklist**: `checklists/snapshot-contract.md` is unchanged (37 unchecked). Analyze does not edit it; CHK008/C-01 and CHK021/I-04 remain consistent with the open/residual findings. No checklist-accountability finding was added.
- **Feature linkage**: Feature 065 remains `Planned`; no new Feature ID or row. The 065a tasks-stage record and the active-basis decision are present in both `features.md` and `features/065.md`. F-01/F-02/F-03 closed.

## Recommended remediation order (not applied)

1. **C-01 (CRITICAL)**: pick one owner and propagate it everywhere. If FR-004 is the owner (the direction chosen by the remediation), amend slice FR-043 and parent FR-004 to make the reference a pointer/mirror, remove "拥有…derived 映射" from `research.md:188`, and align `plan.md:99`/T018 wording. Add a contract test that fails if any artifact claims a different owner. If the reference is to own the table, revert FR-004's owner sentence and update data-model/contracts. Do not leave three claims.
2. **N-01 (HIGH)**: constrain row 6 to `loop_state=DONE`, or move it after rows 11/12 with explicit terminal-state exceptions; update C-57/research/plan wording; add terminal-state + unknown-baseline tests.
3. **I-04 (MEDIUM)**: align `requirements.md:126` with SA-1/C-43 so combined forms do not claim the parent's stale→stop priority for 065a.
4. **I-05 (MEDIUM)**: amend the parent FR-004's flat `spine_consistent` to nested `spine.consistent`, or record an explicit parent-level waiver.
5. **LOWs (N-02/N-03/N-04)**: optional; fix N-03/N-04 in the next artifact pass; N-02 is framework-side and can be recorded as feedback, not edited here.
6. Re-run analyze after remediation. **READY only when CRITICAL/HIGH == 0.**

## Boundaries observed

- Only `.specify/specs/065a-state-awareness/test-evidence/analyze-findings-r2.md` was written by this analyze.
- No repository artifact, feature registry, state spine, feedback store, session store, or git index/commit was modified.
- No `git push`, no remote branch, no merge, no deletion, no process kill.
- No fresh-context validator subagents were dispatched; the delta verification was performed directly, per the stage instruction.
- The skill's feedback/session wrap-up steps were not executed; the stage instruction permits only the analyze report write in transport mode.

## Verdict summary

- **Round-2 findings**: `C-01` CRITICAL (partially fixed, remains); `N-01` HIGH (new); `I-04` and `I-05` MEDIUM residuals; `N-02`, `N-03`, `N-04` LOW.
- **Closed from Round 1**: `I-01`, `G-01`, `I-02`, `F-01`, `A-01`, `G-02`, `A-02`, `A-03`, `A-04`, `U-01`, `G-04` (with LOW residual), `G-05`, `G-06`, `F-02`, `F-03`, `L-01`.
- **Partially fixed**: `C-01` (CRITICAL), `I-04` (MEDIUM), `I-05` (MEDIUM).
- **New**: `N-01` (HIGH), `N-02` (LOW), `N-03` (LOW), `N-04` (LOW).
- **Overall**: **NOT READY** — 1 CRITICAL + 1 HIGH must be closed and the changed rows revalidated before `/speckit.implement`.
