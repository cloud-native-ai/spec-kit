# SDD Review — 090-re-anchoring

**Stage**: review · **Run**: `r20261108T220214Z-8647` · **Branch**: `master` at `fef46f43`
**Authority**: `.specify/specs/090-re-anchoring/{requirements.md,plan.md,tasks.md,verification.md,contracts/,checklists/,checkpoints/}`
**Composition owner**: `.specify/shared/workflow/acceptance-hardening.md` § Review Composition (four segments, one fixed order, then ARC)
**Review mode**: read-only. Nothing under implementation, `requirements.md`, `plan.md` or `tasks.md` was edited by this stage; the write surface is this file, `test-evidence/` and the wrap-up bookkeeping.
**Code-segment base**: `25d5fe13` (`base_source=feature-first-commit`) → head `fef46f43`; `triage=run`, 114 changed files
**Verification of this stage**: every reading below is reproduced in `.specify/specs/090-re-anchoring/test-evidence/review-gates.txt`; the red-first re-run is in `test-evidence/review-red-first-order.txt`.

---

## 1. Portable project context

| Field | Value |
|---|---|
| Requirement | 090 / `090-re-anchoring` / Re-Anchoring（不忘初心 · 温故而知新） |
| Repository | spec-kit (`specify-cli`), root `/cws_data/cloud-native-ai/spec-kit` |
| Remotes | `origin git@gitlab.alibaba-inc.com:cloud-native-ai/spec-kit.git` (SSH only) |
| Reachability of `fef46f43` | **UNRESOLVABLE** — `git branch -r --contains HEAD` is empty, so no URL citation resolves; every citation below is a repo-relative path plus line number |
| Environment | Linux x86_64; `/usr/bin/python3` = CPython 3.11.0rc1 with `pytest 9.0.3`; the `PATH` `python3` has **no** pytest (`ModuleNotFoundError`), hence `SPECKIT_PYTHON=/usr/bin/python3` on every test invocation (same finding as `tasks.md` § Environment Prerequisites) |
| Reviewer | SDD review coordinator (read-only; four segments executed in the owner's fixed order) |

### Artifact inventory

| Artifact | Lines | Path | One-line summary |
|---|---:|---|---|
| requirements.md | 96 | `.specify/specs/090-re-anchoring/requirements.md` | 10 FR / 4 SC / 2 RS rows, clarify settled 2026-11-09 |
| plan.md | 290 | `.specify/specs/090-re-anchoring/plan.md` | describes and anchors the pre-landed tree; EP-001…EP-004 |
| tasks.md | 312 | `.specify/specs/090-re-anchoring/tasks.md` | 39 rows, all `[X]`; GATE-1…GATE-6, DoD-1…DoD-7 |
| verification.md | 115 | `.specify/specs/090-re-anchoring/verification.md` | SC readings, five GATE rows, one waiver, five anomalies |
| contracts/ (4 pages) | 252 | `.specify/specs/090-re-anchoring/contracts/*.contract.md` | 31 clauses (8 / 9 / 6 / 8) |
| checklists/ (1 file) | 1 | `.specify/specs/090-re-anchoring/checklists/2026-11-09-requirements-quality.md` | requirements-quality checklist |
| checkpoints/ (6 files) | 6 | `.specify/specs/090-re-anchoring/checkpoints/0N-*.md` | one per closed stage |
| review.md | — | `.specify/specs/090-re-anchoring/review.md` | this record (first run; archive path `none`) |

---

## 2. Segment results

### 2.1 Process segment — verdict `pass`

Judgment object: the SDD process that produced the slice. Method owner: `.specify/skills/internal/review-sdd-process/SKILL.md`.

| # | Step / event | Evidence | Deviation from the prescribed flow |
|---|---|---|---|
| 1 | Implementation pre-landed **before** the spec chain existed | `137adb7f feat(090): pre-land RE-ANCHORING on top of the script-interface trunk`; `requirements.md` § Note records the same | yes — the chain ran against an already-built tree; disclosed, not improvised |
| 2 | clarify → plan → tasks → checklist → analyze-repair → implement, each closed by a checkpoint | `checkpoints/01…06`; commits `41457d6e`, `419fe9a3`, `b2d7612b`, `66bb1ff5`, `52d0700d`, `95b7d071` | no |
| 3 | The analyze gate raised three HIGH findings and they were repaired **in the tasks artifact**, not by rewriting requirements | `52d0700d`; `tasks.md` § Repair provenance names F-01/F-02/F-03 and F-05 | no |
| 4 | The implement stage opened with a gate-criterion repair driven by a driver ruling | `b13768f7 fix(090): judge the two guard suites by zero new failures` | no (a disclosed ruling, recorded in `verification.md` § Waivers) |
| 5 | Two guard collisions surfaced at implement and were closed by a **driver-side** commit, not by the executor | `9df034a3` touching `tests/contract/test_goal_migration.py` and `tests/contract/test_script_interface_contract.py` | acceptable; the executor returned them as rulings rather than patching local (F-3 records the residue) |
| 6 | An unrelated feature's state spine was rewritten on the 090 line | `git diff 25d5fe13 fef46f43 -- .specify/state/089-script-interface-contract.md` → `spine_state: stalled → completed`, `slice: 086 → 089` | **finding F-2** |
| 7 | The stage produced its own contract-page edits while closing the SC-002 gap | `95b7d071` on `contracts/direction-audit.contract.md` and `contracts/guard-tests.contract.md` | no — both edits are status annotations appended to the dated record; the original reading is preserved |
| 8 | Every close reported against a machine reading rather than prose | `test-evidence/implement-gates.txt`, `closure-guards.txt`, `contract-baseline-comparison.txt` | no |

Process verdict `pass`: no stage was skipped, every checkpoint carries a direction audit, the U4→next-stage rule held (no turn asked to continue), and each drift that did occur was disclosed at the point of occurrence. The two process defects below are defects of **mechanism**, not of discipline.

**Findings**

| Severity | Category | Path | Line | Finding |
|---|---|---:|---|
| P1 | Workflow | `.specify/state/089-script-interface-contract.md` | 4-6 | another feature's loop state was rewritten on this line (`stalled/086` → `completed/089`); issue found only below |
| P1 | Automation | `scripts/python/validate-tasks.py` | — | `--strict` does not exist though `implement-gates.txt` records the assumption; all three "machine check" gates are satisfied by an output shape that this reviewer reproduced identically, so the gate text is safe, but the note itself is a false claim about a CLI (see F-6) |

### 2.2 Artifact segment — verdict `pass`

Method owner: `.specify/skills/internal/review-feature-quality/SKILL.md` § Segment A. Severity family: `P0`/`P1`/`P2` from `review-sdd-process` § Severity Vocabulary.

**Expected set (denominator)**: `.specify/specs/090-re-anchoring`'s standard spec stage product, extended by what `plan.md` § Project Structure declares this feature owns — `requirements.md`, `plan.md`, `tasks.md`, `verification.md`, `contracts/`, `data-model.md`, `quickstart.md`, `research.md`, `feature-ref.md`, `checklists/`, `checkpoints/`, `coverage-baseline.txt` = **12 members**.
**Coverage line**: **12 / 12**. **Missing members**: `none`.

| Dimension | Verdict | Evidence |
|---|---|---|
| Completeness | pass | 12/12 present and non-empty; each carries the sections its template requires |
| Internal consistency | **blocked** (F-1) | the five-question rule set is spelled in two incompatible forms; `test-evidence/sc002-ordering.txt:39` cites the owner page as carrying "the eight rules inline", which it does not |
| Traceability FR → task → SC → evidence | pass | `account-clause-coverage.py --spec-dir .specify/specs/090-re-anchoring` → `fr.claimed 10 / fr.uncovered []`, `clause-uncovered pass (598, 0 beyond baseline)`, `0 error(s), 0 warning(s)`; every SC's declared `Source` names a `test-evidence/` file that exists and carries the reading |
| Dependency / premise ownership | pass | `requirements.md` RS-001/RS-002 name `EP-001`, `plan.md` defines EP-001…EP-004; `tasks.md` § Environment Prerequisites pins each probe with a command and an ISO date and defers the verdict to that section |
| Acceptance honesty | **blocked** (F-1, F-3) | `verification.md` SC-002 pass rests on a guard whose "verdict precedes the goal" leg is not falsifiable (§ 2.4), and the `sc002-ordering.txt` citation overstates the owner page |

**Findings**

| Severity | Artifact path | Line | Why the line is absent | Finding |
|---|---|---:|---|---|
| P1 | `.specify/specs/090-re-anchoring/verification.md` | 26 | none | SC-002 recorded `pass` from a guard whose ordering leg stays green on a goal-before-verdict rewrite: the claim outruns the measurement (F-1) |
| P2 | `.specify/specs/090-re-anchoring/test-evidence/sc002-ordering.txt` | 39 | none | the C-4 reading cites `re-anchoring-definitions.md` as naming the eight rules "inline, first numbered item"; the owner page's equivalent list is six-plus-one under §1.1 and appears nowhere in the protocol (F-1) |
| P2 | `.specify/specs/090-re-anchoring/requirements.md` | 45-48 | none | `**Path**: final` markers were appended inline to the SC bullets — correct per `validate-requirements.py` (0 errors) but the marker reads as part of the sentence in three SCs (cosmetic; no traceability loss) |

### 2.3 Implementation segment — verdict `fail`

Method owner: `.specify/skills/internal/review-feature-quality/SKILL.md` § Segment B.

| Field | Value |
|---|---|
| Base / head | `25d5fe13` → `fef46f43` (`base_source=feature-first-commit`, `git-delta-review.sh base --spec .specify/specs/090-re-anchoring`) |
| Smoke command | `SPECKIT_PYTHON=/usr/bin/python3 /usr/bin/python3 -m pytest tests/contract/test_reanchoring_contract.py tests/contract/test_sdd_loop_driver_reanchor.py tests/contract/test_constitution_double_landing.py tests/contract/test_fast_fail_discipline.py -q --tb=no -rA` |
| Smoke exit code | `1` |
| Smoke evidence path | `.specify/specs/090-re-anchoring/test-evidence/review-gates.txt` (exists, non-empty) |
| Scope and regression verdict | scope clean; regression clean against the feature's own criterion (`LC_ALL=C comm -13 tasks-baseline-failed.txt review-now-failed.txt` prints nothing), see below |

**Readings**

- Four guard modules: `2 failed, 130 passed in 1.84s`; the two failures are exactly the frozen pair (`test_fast_fail_discipline.py::test_i11_channel_two_mirrors_and_per_tool_copies`, `::test_g9_total_equals_frozen_baseline`) — **no NEW failure** (`test-evidence/review-now-failed.txt` vs `test-evidence/tasks-baseline-failed.txt`).
- Feature PLUS the two guards the implement stage edited: six modules → `3 failed, 160 passed`; the third is `test_goal_migration.py::TestHistoricalFacesArePreserved::test_the_user_directive_quoting_the_old_path_survives_verbatim`, inside the frozen 49-name baseline, and the 090 lane's `test_no_live_face_file_retains_the_old_path` is green because `9df034a3` added `.specify/specs/090-re-anchoring/test-evidence/` to `RUNTIME_CACHE_PREFIXES`.
- `verification.md` SC readings: SC-001 / SC-003 / SC-004 reproduce; **SC-002 does not** (§ 2.4, F-1).
- `sync-mirrors.py --check` → exit 0, six pairs byte-identical.

Correction to the object under judgement: `verification.md` § GATE-5 reports the 090 delta at `1 new failure` and waives the literal gate. After `9df034a3` that number is **0**; the waived condition is now satisfied in substance and the `1 new` figure survives only in the historical commit message. Per the write boundary this record reports the correction and does not edit `verification.md`.

**Findings**

| Severity | Diff path | Line | Why the line is absent | Finding |
|---|---|---:|---|---|
| P1 | `tests/contract/test_sdd_loop_driver_reanchor.py` | 145 | none | `assert verdict_at < q3_at or "implicit in it" in audit` — the second operand is what actually decides; a goal statement inserted before the verdict leaves the guard green (probe in `review-gates.txt`) (F-1) |
| P2 | `tests/contract/test_sdd_loop_driver_reanchor.py` | 117-118 | none | `first_no = "1"` followed by `assert first_no == "1"` can never fail; a dead assertion inside the guard that SC-002 cites |

### 2.4 Code segment — verdict `pass` (merge gate: `open-findings`)

Method owner: `.specify/skills/internal/code-review/SKILL.md`; the six-level family (`blocking` / `important` / `suggestion` / `nitpick` / `question` / `praise`) is that skill's and is **not** converted or weighted against `P0`/`P1`/`P2`.

| Field | Value |
|---|---|
| Base / head | `25d5fe13` → `fef46f43`; `base_source=feature-first-commit`; `triage=run` |
| Renderer mode | `renderer: text` — the reviewer is non-interactive, so the two-condition rule selects text mode |
| Changed / judged / skipped / gap | **114 / 114 / 0 / 0** |
| Segment verdict | `pass` — no defect at `blocking`; one `important` and two findings below `important` |
| Merge gate | **refused as "clean"**: one `important` item remains open; nothing at `blocking`, so the delta is not rejected outright |
| Uncommitted scope | `.specify/specs/081-acceptance-hardening/test-evidence/smoke-081.txt` is dirty at run start; it is outside this delta and outside this review — disclosed, not concluded over |

**Findings**

| Severity | File | Line | Finding |
|---|---|---:|---|
| **important** | `shared/definitions/re-anchoring-definitions.md` | 30-36 | The owner page's five-question rule list and the protocol's Q1 name **two different rule sets**, and the closed-eight paragraph added by `95b7d071` contradicts the page's own fourteen-line-older list. Details in F-1. |
| suggestion | `tests/contract/test_reanchoring_contract.py` | 9-32 | Four presence tests, no pointer assertion and no failure-mode arm, although `re-anchoring-faces` C-7 (the "no consumer restates the tier table" clause) and `guard-tests` C-4 ("each clause a guard asserts MUST have a demonstrated failure mode") both claim them (F-5) |
| nitpick | `scripts/bash/generate-instructions.sh` | 92-100 | The raise record is stale on two lines (F-4) |

**One structural observation, recorded for ARC and not repaired here**: `closure-acceptance-check.py` returns `final_path.unknown = 4` for this feature. The checker counts status rows only from `<SC-NNN>_status=` fields (`closure-acceptance-check.py:301`), and `verification.md` carries its readings in a markdown table. This is the counter's contract, not a defect of the artifact — and it is why ARC below reports a `blocked` verdict on a feature whose four criteria are all measurably `pass`.

---

## 3. Findings (consolidated, ordered by severity)

### F-1 — The rule-anchor member set has two owners and the SC-002 ordering pin is not falsifiable

- **Severity**: **P1** (artifact) + **important** (code). One defect, two segments.
- **Category**: Documentation / Workflow
- **Location**: `shared/definitions/re-anchoring-definitions.md:30-36` and `:56-59`; `skills/external/sdd-loop-driver/references/checkpoint-protocol.md:50-51`; `templates/constitution-template.md:393-395`; `templates/instructions-template.md:108`; `tests/contract/test_sdd_loop_driver_reanchor.py:142-145`
- **Evidence** (verbatim):

  ```
  # owner page §1.2, the five questions' Q1
    1. 本核心步骤受哪些规则约束？逐条是否仍然生效（无人值守 / 不征求继续 / U4→下一阶段 / 先写脊后行动 /
       workspace guard / fast-fail / 确认门 / 预算纪律）？

  # owner page §3, added by 95b7d071
  - **规则锚的成员是封闭集合，owner 是本文件 §1.1**：八项——无人值守（不征求继续）、U4 通过即派发下一阶段、
    状态脊先写后动（含 workspace guard）、fast-fail 的纠正/裁定二分、确认门、**预算纪律**（token 与时间预算）、
    **报告纪律**（进度报告与回传形态）。消费面（两侧宪法、两侧指令面、生成器条目）以**指针**接入并与本集合一致，

  # owner page §1.1 rule anchor
    - **规则锚**：当前生效的**操作规则集**——无人值守（不征求继续）、U4 通过即派发下一阶段、状态脊先写后动、
      workspace guard、fast-fail 的纠正/裁定二分、确认门、预算与报告纪律等。

  # the protocol's Q1
    1. Which rules govern this step, and is each still in force (`unattended` / no approval request / U4 -> next
       stage / spine written before acting / `workspace-guard --check` / fast-fail / the gate discipline / budget)?

  # constitution, both surfaces
    workspace guard / fast-fail / the gate discipline / budget and report discipline). A compaction, handoff or reentry MUST resume

  # the guard's ordering leg
    verdict_at = audit.index(verdicts)
    q3_at = audit.index("3. Is the next action")
    assert verdict_at < q3_at or "implicit in it" in audit, (
  ```

- **Why it is a problem**: `SC-001` licenses the claim "no consumer restates the tier table or the question list", yet the four consumer faces carry a `gates / budget and report discipline` pair that the **procedure** (protocol Q1) does not have — it says `the gate discipline / budget`. So the two sides of the same five questions enumerate different rules: the owner page's own copy of Q1 has no `gates` at all, and the closed-eight paragraph calls `budget` and `report discipline` two members while every consumer joins them with "and" into one entry. This is exactly the One-Source-of-Truth failure the feature exists to prevent, one level up from the rule it documents. The second half is worse: `SC-002`'s tightened criterion asks the same test to assert that "the verdict/action precedes any goal statement". In the landed guard the second operand (`"implicit in it" in audit`) is a flat substring over the whole block, so the first operand never decides. I built a scratch mutant that inserts a goal statement immediately **before** the verdict sentence and keeps Q1 and the primary-object sentence byte-identical, and the ordering test stayed **green** (5 passed; `review-gates.txt`, probe section). SC-002 is therefore satisfied on the leg that is testable (Q1 asks the rules) and unverified on the leg it was tightened to require.
- **Proposed fix**: (a) name the closed set **once**, in the owner page §1.1, in the exact member form the protocol's Q1 uses, and make §1.2's Q1 and §3 both point at it instead of re-listing; then re-project the four consumer faces from that one list. (b) Replace the ordering leg with a positional assertion — `audit.index(GOAL_STATEMENT_RE) > audit.index(VERDICT_STATEMENT)` where the goal operand is a required literal (e.g. the word `goal` in an answer line), and add a fourth mutant arm that inserts a goal line before the verdict, so the arm fails until the leg is real.

### F-2 — Another feature's loop state was rewritten on this line

- **Severity**: **P1**
- **Category**: Workflow
- **Location**: `.specify/state/089-script-interface-contract.md:4-6`
- **Evidence** (verbatim from `git diff 25d5fe13 fef46f43`):

  ```
  -spine_state: stalled
  +spine_state: completed
   run_id: r20261106T090000Z-086a
  -slice: 086
  +slice: 089
  ```

- **Why it is a problem**: `090`'s direction contract forbids drift on the state spine, and "a line closes its own spine" is the driver's model. `bdadae85 chore(089): close the state spine on the merged trunk` was picked up after the 089 line merged and rides inside 090's first-parent history, so the 090 delta now contains a write to a different feature's state — which is exactly the shape a future reader will misattribute. It is not destructive (the 089 line really had completed) but it makes the delta's scope unreadable and it means a 090 revert would reopen another line.
- **Proposed fix**: leave the 089 content as is (it is true), and record the boundary in this feature's own record: the 090 stage commits must not touch another line's spine; if a cross-line close is needed, it belongs in a commit named after that line, not in the 090 feature commit. Owner of the rule: the driver's HR set in `.specify/state/090-re-anchoring.md` `driver_contract`.

### F-3 — Two tests belonging to feature 089 were edited inside a 090 patch commit, and the second edit narrows a guard

- **Severity**: **P1**
- **Category**: Automation
- **Location**: `tests/contract/test_goal_migration.py:79-82`; `tests/contract/test_script_interface_contract.py:4211-4245`
- **Evidence** (verbatim, `9df034a3`):

  ```
      ".specify/specs/089-script-interface-contract/test-evidence/",
  +    # 2026-11-09 Feature 090: the same rule again — a full-suite capture quotes this guard's
  +    # own failure text, so the needle is present by construction. Generated evidence, not a
  +    # live surface that forgot the migration.
  +    ".specify/specs/090-re-anchoring/test-evidence/",
  ```

  ```
  -    assert measured, (
  -        "C-32: the feature ADDED executable artifacts, so the comparison below is not vacuous; "
  -        f"base={base[:12]}"
  -    )
  ...
  +    base_paths = set(tree.stdout.splitlines()) if tree.returncode == 0 else set()
  +    integrated = bool(declared_with_mirrors) and declared_with_mirrors <= base_paths
  +    if integrated:
  +        pass
  +    else:
  +        assert measured, (
  ```

- **Why it is a problem**: both edits are defensible on their merits, and both are in another feature's guard. The first is the identical-rationale extension of a lane prefix (fine in kind). The second is different: when `git ls-tree` succeeds **and** the declared artifacts happen to sit in the base, the whole C-32 comparison — the non-vacuity leg, the "declared ⊆ measured" leg **and** the equality leg against `C32_MEASURED_BEYOND_DECLARATION` — is skipped, on the reasoning that the trunk has already integrated the line. `git ls-tree` needs no network, so the `integrated` branch is reachable on any clone whose base carries the artifacts, and the only trace of the skip is a `pass` statement in a comment. Worse, the *reported* basis does not match the code: the implement evidence says the error is `CARGO_BUILD_TARGET=<dir> python3 -m pytest tests/contract/test_build_profiles_invalid_target.py` while the actual failing node id is `test_script_interface_contract.py::test_t078_...` — two different subjects, so a reader auditing the claim cannot follow it from the evidence.
- **Proposed fix**: (a) make the `integrated` path assert something — at minimum `assert not measured or addition == ...`, or `pytest.skip` with an explicit reason so the skip shows in the summary instead of hiding as a pass; (b) correct the implement evidence line to name the node id that failed; (c) land future guard edits for a foreign feature as their own commit named after that feature, so `git log` attributes them.

### F-4 — The instructions-budget raise record's self-consistency check fails

- **Severity**: **P2**
- **Category**: Automation
- **Location**: `scripts/bash/generate-instructions.sh:92-100` (mirrored at `.specify/scripts/bash/generate-instructions.sh:155-163`)
- **Evidence** (verbatim):

  ```
      #   new value: 37888
      #   measured live size after injection: 35790 B (this repository, 2026-11-09)
      #   reason: the new `## Re-Anchoring (不忘初心 · 温故而知新)` ambient section.
      #   rule: the same rule — the smallest N*1024 with (N*1024 - 1) - 35790 >= 1024.
      #     36864 fails (73 B); 37888 leaves 2097 B and is the first that passes.
  INSTRUCTIONS_BUDGET_BYTES=38400
  ```

- **Why it is a problem**: the block documents a raise to `37888` and then declares `38400`, and two of its own numbers are contradictions: `36864 - 35790 = 1074`, not the stated `73 B`; and `37888 - 35790 = 2098`, not `2097 B`. The live file is now **35821 B** (`wc -c .specify/instructions.md`), so the recorded measurement is 31 B stale as well. Nothing breaks today — `test_instructions_size_budget.py::test_c17_real_tree_live_size_is_within_the_raised_budget` derives the budget from the script and passes — but the recorded reason is the only place a maintainer can re-derive *why* 38400, and it does not reproduce.
- **Proposed fix**: recompute and restate the block against the current live size, or point the block at the rule instead of re-deriving it inline (the rule already has an owner).

### F-5 — The feature's own face guard carries no failure-mode arm and no pointer assertion

- **Severity**: **suggestion** (code) / **P2** (artifact, informational)
- **Category**: Automation / Documentation
- **Location**: `tests/contract/test_reanchoring_contract.py:9-32`; claimed by `.specify/specs/090-re-anchoring/contracts/guard-tests.contract.md:30-33` (C-4) and `:36-39` (C-5)
- **Evidence** (verbatim):

  ```
  def test_owner_document_carries_both_concepts_and_the_tiers():
      owner = (ROOT / "shared/definitions/re-anchoring-definitions.md").read_text(encoding="utf-8")
      for token in ("不忘初心", "温故而知新", "规则锚", "T0", "T1", "T2",
                    "on-track", "correction-applied", "decision-needed"):
          assert token in owner, token
  ```

  ```
  **C-4** — A guard must red when its subject breaks
  Each clause a guard asserts MUST have a demonstrated failure mode: deleting the surface, renaming the title, or
  dropping the part must make the module fail.
  ```

- **Why it is a problem**: `test_evidence/sc001-faces.txt` reports that "the owner page plus the five consumer faces exist, all point at `shared/definitions/re-anchoring-definitions.md`, no consumer restates the tier table or the five questions", but the module asserts a token set — it never asserts a pointer, and it never asserts the *absence* of a restated tier table. `guard-tests.contract.md` C-4 asks every asserted clause to have a demonstrated failure mode; only the protocol module has red-control arms. So the SC-001 half of the guard surface is entirely presence-shaped, and the same criticism clarify C-4 levelled at SC-002 ("presence of `Q1` is not ordering") applies to it unaddressed.
- **Proposed fix**: add one arm per face that deletes the section and asserts the module fails, plus a positive pointer assertion for each of the five consumer faces; or amend C-4/C-7 to state which clauses are presence-only and why.

### F-6 — The gate evidence cites a `--strict` flag the engine does not have

- **Severity**: **P2**
- **Category**: Documentation
- **Location**: `.specify/specs/090-re-anchoring/test-evidence/implement-gates.txt:12-14`
- **Evidence** (verbatim):

  ```
  # note: --strict is not an option of this engine (its documented surface is [--json]); the
  # default invocation above is the strictest form the engine offers.
  ```

- **Why it is a problem**: the note is false about `validate-tasks.py` as it ships. This reviewer ran every gate the note protects and each one reproduces (`PASS: ... 0 error(s), 0 warning(s)`; `fr.uncovered []`; mirror exit 0), so the *conclusion* holds and nothing rides on the claim — but a downstream reader who trusts the note will believe an option exists that does not, and the note's purpose ("we ran the strictest form") is exactly the kind of assertion that must be derived, not asserted.
- **Proposed fix**: delete the note or replace it with the engine's actual output contract; if a stricter mode is wanted, that is a feature request for `validate-tasks.py`, not a note in an evidence file.

---

## 4. What worked — preserve

- **Rules-first drift control.** The line did not ask "shall I continue" once across seven stages; the checkpoints' § 5 carry a real verdict every time, and the driver answered rulings (n-5, the C-32 collision) with its own commits instead of letting the executor smooth them into green.
- **Red-first, then prove the red.** T013/T014/T016–T018 captured the pre-change tree, landed one test, and then re-ran against three mutants through `SPECKIT_CONTRACT_ROOT`. That is the right instrument, and it is what let this review find the remaining dead leg so precisely.
- **The judge-by-no-new-failure move.** `b13768f7` replaced a "must be green" gate with a set comparison over frozen node ids — reproducible with one `comm`, and it survived a baseline that was red before the feature began.
- **Two disjoint coverage lanes.** FR-by-citation-group vs clause-by-`[green:]` tag removed the analyze-stage contradiction (F-03) rather than arguing around it; `account-clause-coverage.py` now proves both in one run.

---

## 5. Improvement recommendations

### 5.1 Template improvements
- **REC-T1 — one member list per rule anchor** — Target: `shared/definitions/re-anchoring-definitions.md` §1.1. Change: make §1.1 the only place the rule-anchor members are enumerated and have §1.2's Q1 and §3 cite it; re-project the four consumer faces from it. Source: F-1. Expected impact: the feature's own One-Source-of-Truth claim becomes decidable.
- **REC-T2 — status blocks carry a validity check** — Target: `templates/review-template.md` § 2.2. Change: require the artifact segment to name, per SC, the falsifiable arm or record "presence-only" explicitly. Source: F-1, F-5.

### 5.2 Command prompt improvements
- **REC-C1 — review reads the guard's own failure modes** — Target: `.specify/skills/internal/review-feature-quality/SKILL.md` § Segment B. Change: add "for every guard an SC cites, name one rewrite that must turn it red; if you cannot, the SC is unverified" as an explicit step. Source: F-1.

### 5.3 Automation / scripts
- **REC-A1 — `integrated` must skip visibly** — Target: `tests/contract/test_script_interface_contract.py` (`test_t078_...`). Change: replace the `if integrated: pass` branch with `pytest.skip(reason=...)` so the skip appears in the summary. Source: F-3.
- **REC-A2 — positional assertion helper** — Target: `tests/contract/test_sdd_loop_driver_reanchor.py`. Change: add a `_assert_precedes(before, after, text)` helper and use it for the verdict-vs-goal leg, so an `or` short-circuit cannot stand in for an order. Source: F-1.

### 5.4 Workflow
- **REC-W1 — one line, one spine** — Target: `.specify/state/090-re-anchoring.md` `driver_contract`. Change: add "a stage commit MUST NOT rewrite another line's spine; a cross-line close lands in a commit named after that line". Source: F-2.
- **REC-W2 — foreign-guard edits get their own commit** — Target: the same contract block. Change: an edit to a test owned by another feature lands as `<that-feature>(fix):`, never inside this feature's `fix(...)`. Source: F-3.

### 5.5 Documentation
- **REC-D1 — re-derivable raise records** — Target: `scripts/bash/generate-instructions.sh:92-100`. Change: restate the block against the measured size, or drop the inline derivation and point at the rule's owner. Source: F-4.

---

## 6. Priority roadmap

| Priority | Recommendation | Target | Source |
|---|---|---|---|
| P1 | Define the rule-anchor member set once | `shared/definitions/re-anchoring-definitions.md` | F-1 |
| P1 | Bind the verdict-before-goal leg positionally | `tests/contract/test_sdd_loop_driver_reanchor.py` | F-1 |
| P1 | Make C-32's integrated branch skip visibly | `tests/contract/test_script_interface_contract.py` | F-3 |
| P1 | One line, one spine | `.specify/state/090-re-anchoring.md` `driver_contract` | F-2 |
| P2 | Give the face guard failure-mode arms | `tests/contract/test_reanchoring_contract.py` | F-5 |
| P2 | Re-derive the instructions raise record | `scripts/bash/generate-instructions.sh` | F-4 |
| P2 | Retire the `--strict` note | `test-evidence/implement-gates.txt` | F-6 |

---

## 7. Acceptance Reality Check

Owner of the record's key set and verdict values: `.specify/shared/declarations/facts/arc-verdict-mapping.yaml#/statement`, read through `scripts/python/closure-acceptance-check.py`. Copied verbatim, never recomputed:

| Field | Value | Source |
|---|---|---|
| Claimed status (read, never written) | `Planned` | `.specify/memory/features.md:98` |
| `final_path` record (7/7) | pass **0** · blocked **0** · deferred **0** · partial **0** · fail **0** · unknown **4** · total **4** | `closure-acceptance-check.py --json`, `review-gates.txt` |
| Comparison verdict | **refused** — a `Planned` claim is itself legal, but the record is non-trivial only as `unknown`; see the condition below | `verdict: block`, `reasons: [{code: zero-final-path-pass}]` |
| Failed condition | `zero-final-path-pass` — the `pass` bucket is 0, and completion condition `status_row_per_criterion` is `false` alongside it | same |
| Fixed item | `F-ACCEPTANCE` at `P0` | same |

Additional conditions the same record reports: `no_open_rows: true` (39 closed / 0 open / 0 claimed), `smoke_record_pass: false` (`smoke_exit_code=1`), `every_final_path_pass: false`.

**What the refusal means, and what it does not.** The zero-`pass` bucket is a counter contract, not a delivery fact: `closure-acceptance-check.py:301` recognises only `<SC-NNN>_status=` lines, and `verification.md` carries its readings as a four-column markdown table, so all four criteria read back as `unknown` even though three of them are measurably `pass` and the fourth is measurably `fail` (§ 2.4). The ARC therefore refuses the transition to `Implemented` on **two** grounds, and both are honest: the record genuinely has no `pass` in it, and SC-002 genuinely does not hold. The feature stays `Planned`. Nothing in this review moves it, and the claimed status is left untouched.
