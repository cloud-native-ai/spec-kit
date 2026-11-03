# Analyze r2 — slice 081c (verification of the C/H repair)

**Stage**: `/speckit.analyze` round 2 — read-only verification that the C/H findings of `notes/analyze-081c.md` are repaired and that the repair introduced no new C/H.
**Repo / branch / HEAD**: `spec-kit`, `081-acceptance-hardening`, `af43a4a4` (`fix(081c): repair the analyze C/H findings`).
**Round-1 input**: `notes/analyze-081c.md`, `test-evidence/analyze-081c.jsonl` (24 rows: C=1, H=8, M=11, L=4).
**Output**: `test-evidence/analyze-081c-r2.jsonl` (16 rows: 9 resolved, 4 new M, 3 new L).
**Scope discipline**: no artifact was edited. The only files written are this report and the r2 JSONL. The two fixture payloads were measured on a throw-away copy under a system temp directory, not in the repo, and the copy was deleted.

## Gate verdict

**`pass`** — 0 open C, 0 open H. All nine round-1 C/H findings are resolved on the text **and** on the machine readings, not merely reworded. Six new findings were raised (4 M, 3 L); none is gate-blocking.

## F-01 … F-09 — repair verification

| ID | R1 sev | Status | Repair and rule it now satisfies |
|---|---|---|---|
| F-01 | C | **resolved** | Composition ownership is split by layer instead of merged. Contract header (`contracts/review-composition.contract.md:4`) now names the **content** owner (`shared/workflow/acceptance-hardening.md` § Review Composition) and the **command-side declaration** owner (`templates/commands/review.md` § Composition, "the four segment headings and the five per-segment fields **by anchor** … restates none of its content"). FR-013 (`requirements.md:153`) carries the same split ("组合内容 … 唯一内容定义点" / "命令侧声明的 owner … MUST NOT 复写 owner 的段内容、顺序理由或边界句 … 命令模板不是组合内容的第二个定义点"); A3 (`requirements.md:28`) gained the two-layer owner-rewrite clause in the same commit; T002 (`tasks.md:102`) claims content only and adds an explicit "Scope of \"only\"" paragraph; `data-model.md:173` names both layers with their qualifiers; `tasks.md:278` states the split is load-bearing. **Rule satisfied**: Constitution XIV — one owner per fact — with FR-013's two-layer mandate now satisfiable. |
| F-02 | H | **resolved** | SC-002's review-site leg has a reachable input. T015 (`tasks.md:88`) authors `review-implemented-clean`; the measurement is routed to it at `tasks.md:243` (slice boundary), `:119` (leg (i)), `:140` (T013), `:34` (DoD-8) and `data-model.md:198`, and the `positive`-on-`Planned` drive is explicitly forbidden as a substitute. **Measured this pass** (temp copy, read-only): `positive` with the claim moved to `Implemented` → `accept`, exit 0, `claimed_status` `Implemented`, `final_path {pass:1,total:1}`, all four `completion_conditions` true — the exact payload T015 specifies. Baseline re-measured: `positive` alone → `accept`, `claimed_status` `Planned` (condition inapplicable), matching round 1. |
| F-03 | H | **resolved** | RC-15's conjunction has a fixture. T016 (`tasks.md:89`) authors `review-implemented-blocked`; leg (f) (`tasks.md:119`) and GATE-7 (`tasks.md:45`) drive the refusal on it instead of `negative`; `data-model.md:199` records why no other case satisfies both conjuncts. **Measured this pass**: `negative` with the claim moved to `Implemented` → `block`, exit 1, `claimed_status` `Implemented`, `final_path {blocked:1,deferred:1,pass:0,total:2}`, reasons `[zero-final-path-pass, status-claims-implemented-but-blocked]`. `smoke-mutation` re-measured: `block`, `pass:1`, reasons `[status-claims-implemented-but-blocked]` — the round-1 correction still holds. |
| F-04 | H | **resolved** | The requirement was amended, not the contract. FR-015 (`requirements.md:155`) now requires the seven-key record verbatim (7/7, "缺任一键即未满足本条", "MUST NOT 把记录收窄为三计数摘要——「三计数齐备」不是本条的满足形态"); SC-006 (`:208`) requires 7/7 and says a three-count report is **not** satisfied; SC-006 Source (`:220`) reads "七键记录行及其键名/键数"; `verification.md:67` rewritten; US3 acceptance scenario 3 (`requirements.md:98`) — a site round 1 did not cite — moved to the seven-key record as well. A repo-wide grep for `三计数` / `three counts` / `three-count` in the spec dir now returns only prohibition phrasing. |
| F-05 | H | **resolved** | The locator MUST is restored with one decidable escape in every carrier: FR-013 (`requirements.md:153`), RC-06 (`contracts/review-composition.contract.md:16`), `plan.md:289`, `data-model.md:175`, SC-006 (`requirements.md:208`), T006 (`tasks.md:124`) and the new leg (j) (`tasks.md:119`), which asserts the field set in both `### 2.2` and `### 2.3` and that a reasonless omission on a line-addressable artifact fails. grep: the only remaining `optional` strings are `SC-NNN_value` / `SC-NNN_note` (`data-model.md:36-37`) and the phrase "never an optional field" — no carrier marks `line` optional. |
| F-06 | H | **resolved** | FR-013's missing-artifact clause now meets an input that can distinguish the readings. T017 (`tasks.md:90`) authors `expected-artifact-missing` (plan lists seven, directory holds six, `quickstart.md` absent) and requires both readings recorded side by side; leg (d) (`tasks.md:119`) applies the declared derivation to it and asserts `6 / 7`, one finding per missing member, and the `6 / 6` contrast that makes the "ones that exist" reading fail the leg; DoD-5 (`tasks.md:31`) upgraded to "falsified, not accepted on prose"; `data-model.md:187` carries the measured basis and `:200` the honest limit (the closure checker does not read § Project Structure). |
| F-07 | H | **resolved** | RC-12 has a counting leg and a corrected traceability cell. Leg (k) (`tasks.md:119`) requires **exactly one** `- **Judgment object**:` marker in `skills/internal/review-sdd-process/SKILL.md`; T003 (`tasks.md:103`) makes that true by construction; the T003 cell (`tasks.md:208`) now names leg k. Verified on disk: `## Input Contract` at `skills/internal/review-sdd-process/SKILL.md:25`, `- **Subject**:` at `:31`, and the marker occurs 0 times in that body today (the only such markers in the tree are `templates/commands/review.md:44,52`), so the post-T003 count is 1. |
| F-08 | H | **resolved** | Both census pins are enumerated and the enumeration is closed. RC-19 (`contracts/review-composition.contract.md:38`) names `tests/contract/test_review_feedback_boundary.py` (C-58) and `tests/contract/test_client_guard_sweep.py` with the verbatim message; T009 (`tasks.md:127`) now lists **four** modules including the sweep; GATE-2 runs it; T003 ties the skill sentence to its re-pin. Verified on disk: `test_client_guard_sweep.py:348` asserts `一次运行的单元普查为**三个单元**` with message `the per-run three-unit census MUST be preserved verbatim (C-53)`; `skills/internal/code-review/SKILL.md:111` carries the sentence; C-58's assertions (`test_review_feedback_boundary.py:501,622`) read `templates/commands/review.md:117`. A tree-wide grep for the census wording returns exactly those two carriers plus the command heading — no third pin exists. |
| F-09 | H | **resolved** | T010 (`tasks.md:128`) now points the checklist at `templates/feature-details-template.md` § Canonical Status State Machine and records why not § Gates, which is what the owner doc itself says (`shared/workflow/acceptance-hardening.md:111`). The cited guard exists (`tests/contract/test_status_gate_owner.py:542 test_c48_the_checklist_command_keeps_its_pointer_and_gains_no_criteria`); its body requires exactly one mention, keeps `Feature Integration Protocol`, and bans `CRITERIA_COPY_TOKENS` (`test_status_gate_owner.py:100-106`) — adding the anchor trips none of them, and `templates/commands/checklist.md:44` is the single mention. |

Regressions looked for and **not** found in the repaired artifacts: a second owner for the same fact (contract/FR-013/T002/§ Notes/`data-model` all agree on the layer split, apart from the two unswept sentences in R2-F-12); a broken cross-reference (T004's `[blockedBy: T015,T016,T017]` all exist; T003's `## Input Contract` / `- **Subject**:` anchors exist; T010's test id exists; RC-19's two modules and quoted message exist; T002's `## Extension Points` bullet exists at `shared/workflow/acceptance-hardening.md:454`); a task without a carrier (every one of T015–T017 names a fixture path *and* a task row, and every 081c row of `data-model.md` § Fixture set — three — has exactly one authoring task); a fixture row without a task (none: the corpus table's 081c slice assigns exactly `review-implemented-clean`, `review-implemented-blocked`, `expected-artifact-missing`); a dropped MUST (line-level diff of `requirements.md` / `contracts/review-composition.contract.md` shows strengthened obligations only — FR-013's locator, FR-015's seven-key copy, SC-006's 7/7; FR-015's "统计" verb was deliberately replaced by "抄录" per F-04/F-10, and RC-02's order ownership moved to the content layer per F-01); a traceability cell pointing at a nonexistent leg (every leg letter cited exists in T004; the two new legs with no cell are R2-F-14, L).

## New findings (raised in this round)

| ID | Sev | Status | Location | Finding |
|---|---|---|---|---|
| R2-F-10 | M | new | `tasks.md:119(d),278` | Leg (d) does not name which carrier it reads for the derivation rule, while § Notes makes "a second statement of the derivation rule" a defect of this slice — the leg is satisfiable either by creating that defect or by leaving the segment's own text unasserted. |
| R2-F-11 | M | new | `tasks.md:119(k)` | Leg (k)'s second conjunct ("dimension lists count 0 under the process skill") names no countable token; the decidable half (marker count = 1) does not discriminate plan § T-004's rejected antithesis. |
| R2-F-12 | M | new | `tasks.md:238`; `plan.md:252` | Two pre-repair sole-ownership sentences survive unqualified (neither was in F-01's evidence list); § Notes resolves the reading, but the sweep for F-01's own fact is incomplete. |
| R2-F-13 | M | new | `contracts/review-composition.contract.md:4`; `tasks.md:102,124,125,278` | The content list now includes "the ARC clause and the unit census", while T006/T007 and legs (f)/(h) require the command and template to state both; the layer split was written for the four headings and five fields only, and § Notes' permitted list mentions neither. |
| R2-F-14 | L | new | `tasks.md:210,211,212` | Legs (j) and (k) were added without pointing the rows whose carriers they judge (T005/T006 cells still name leg g / no leg). |
| R2-F-15 | L | new | `tasks.md:32` | DoD-6 still says "the guard that pins the census" (singular) while RC-19 names two pins. |
| R2-F-16 | L | new | `tasks.md:281` | The recorded post-correction gate reading (`advisories=56`) no longer reproduces; re-running the same command after the repair yields 69 (T015–T017 add thirteen missing-path advisories), and the 69 reading lives only in `test-evidence/analyze-fix-081c-validators.txt`. |

## Machine readings (re-run this pass, read-only)

```
$ python3 scripts/python/validate-requirements.py .specify/specs/081-acceptance-hardening/requirements.md
status: ok
  [id-contiguous] pass (0)   [doc-order] pass (0)   [ref-resolvable] pass (0)
  [marker-count] pass (0)    [dup-id] pass (0)      [path-marker] pass (0)
scanned: 272 lines, 34 definition rows, 17 shared strings
0 error(s), 0 warning(s)                                     EXIT=0

$ python3 scripts/python/validate-tasks.py .specify/specs/081-acceptance-hardening/tasks.md
PASS: — 0 error(s), 0 warning(s)                             EXIT=0

$ python3 skills/external/sdd-loop-driver/scripts/pre-analyze-check.py --stage tasks --repo . \
    --spec-dir .specify/specs/081-acceptance-hardening
decision=pass  errors=0  advisories=69  waived=0
summary: fr=25 sc=9 tasks=17 clauses=66 files=16                EXIT=0

$ python3 skills/external/sdd-loop-driver/scripts/decomposition-check.py --mode tasks \
    --requirements …/requirements.md --tasks …/tasks.md
decision=proceed  fr_count=25 (ceiling 30)  task_count=17 (ceiling 40)  reasons=[]   EXIT=0
```

All four reproduce the repair commit's own record (`test-evidence/analyze-fix-081c-validators.txt`, written at 14:41) line for line — including `advisories=69` and `task_count=17`. The only divergence in the artifact set is `tasks.md:281`'s pre-repair `advisories=56`, which is a dated reading of the tasks-stage correction (its verbatim block is in `test-evidence/tasks-081c-pre-analyze.txt`, `checked_at 2026-11-03T06:14:09Z`) and is tracked as R2-F-16 (L).

Additional read-only measurements used above (not part of the four required checks):

```
closure-acceptance-check.py --spec-dir tests/fixtures/acceptance-hardening/positive        → accept, claimed Planned, pass 1/1, exit 0
closure-acceptance-check.py --spec-dir tests/fixtures/acceptance-hardening/negative        → block,  claimed Planned, blocked 1/deferred 1/pass 0, [zero-final-path-pass], exit 1
closure-acceptance-check.py --spec-dir tests/fixtures/acceptance-hardening/smoke-mutation  → block,  claimed Implemented, pass 1/1, [status-claims-implemented-but-blocked], exit 1
temp copy: positive + claim → Implemented   → accept, claimed Implemented, pass 1/1, all four conditions true, exit 0
temp copy: negative + claim → Implemented   → block,  claimed Implemented, pass 0/total 2, [zero-final-path-pass, status-claims-implemented-but-blocked], exit 1
```

The last two lines are the empirical proof that F-02 and F-03 are repaired rather than re-described: the two fixtures the repair adds are reachable exactly as T015/T016 specify.

## Round-1 M/L items — status note

Round 2's gate is C/H only, so the eleven M and four L rows of round 1 were not re-adjudicated. Two observations from spot checks: the round-1 M items F-13 (`two segments` still present in `.venv/.../specify-cli` copies and dated 071/080 records, 23 files) and F-19 (T014's closure excludes T003) are unchanged by this repair and remain open as M; the revised T003 does not widen either. `checklists/081c-2026-11-03.md` still records its 22 FAIL cells — checked and found by design: the checklist's own header hands FAIL items to `/speckit.analyze`, and `notes/analyze-081c.md` + this report are that adjudication record.

## Verdict

Zero open C, zero open H. Nine of nine round-1 C/H findings resolved. The slice may proceed; the six new M/L rows are improvements to make while implementing (R2-F-10 and R2-F-11 are the two that decide whether two of the new legs can actually go red, and are the ones worth fixing before T004 is authored).
