# Analyze findings — 093-concurrency-by-default

**Stage**: analyze (S6 of `requirements, clarify, plan, tasks, checklist, analyze, implement, review`)
**Branch / worktree**: `093-concurrency-by-default` @ `.specify/.tmp/sdd-loop/worktrees/093-clarify`
**Base commit**: `dbe172a4` (checklist stage)
**Date**: 2026-11-09
**Inputs read**: `requirements.md` (33 FR / 12 SC / 11 STR), `plan.md`, `tasks.md` (137 rows), `checklists/2026-11-09-requirements-quality.md` (44 items), `checkpoints/01…05`, `feature-ref.md`, `contracts/*.md` (92 clauses), spine `.specify/state/093-concurrency-by-default.md`, `.specify/memory/register.md` § F-093-*, `templates/tasks-template.md`, `.specify/templates/tasks-template.md`, `.specify/scripts/python/validate-tasks.py`, `templates/commands/tasks.md`, `.specify/memory/constitution.md` (§ XIV, XVI, XX).
**Execution shape of this stage**: serial, one executor, `mechanism-not-yet-landed` ([[STR-010]]) for the *feature's own* mechanism. Recorded as an instance of the feature's subject, not presented as concurrency. SC-006 stays `not_evaluated` (F-093-011).

---

## 0. Verdict

**NOT-READY** — CRITICAL = 1, HIGH = 3, MEDIUM = 8, LOW = 2.

Only CRITICAL and HIGH block. All four are requirement-text / clause-annotation defects with exactly one recorded reading each, so the repair brief in § 6 is an `analyze-repair` dispatch, not a return to the user.

---

## 1. Gate readings (evidence: `test-evidence/analyze-gates-2026-11-09.txt`)

Every command line, its complete stdout/stderr, exit status and wall time are retained in that one file (single-run evidence).

| # | Gate | Reading | Verdict |
|---|---|---|---|
| G1 | `validate-requirements.py requirements.md` | 319 lines, 45 definition rows, 11 shared strings, **0 error / 0 warning**, EXIT 0 | PASS |
| G2 | `account-clause-coverage.py <spec-dir> --corpus-root <worktree>/.specify/specs` (no `--freeze`) | `status: baseline-missing`, EXIT 2 — **FR lane 25 / 33 cited, 8 uncited**: `FR-011`, `FR-013`, `FR-016`, `FR-017`, `FR-025`, `FR-027`, `FR-028`, `FR-033`; clause lane 35 claimed, 655 uncovered beyond an absent baseline; 108 named-unparseable files (zero of them declare a positive form) | **RED, honestly reported.** The FR lane is the discriminating number and it is unchanged from the last reading — F-093-005 gives the root cause. `baseline-missing` is expected (T006 has not run) and was **not** converted into coverage by freezing: `--freeze` narrows the corpus to everything *but* this spec, so it answers a different question and would have turned a red FR lane into baseline-internal noise. No `--freeze` was run. |
| G3 | `validate-tasks.py tasks.md` | `PASS — 0 error(s), 0 warning(s)`, EXIT 0 | PASS |
| G4 | `validate-decision-tensions.py --spec <spec-dir>` | EXIT 0 — 5 records T-001…T-005 intact | PASS |
| G5a | `pre-analyze-check.py --stage requirements` | `decision=pass errors=0 advisories=0`, EXIT 0 | PASS |
| G5b | `pre-analyze-check.py --stage plan` | `decision=pass errors=0 advisories=0`, EXIT 0 | PASS |
| G5c | `pre-analyze-check.py --stage tasks` | `decision=pass errors=0 advisories=101 waived=0`, EXIT 0 — every advisory is a creation-target path (`shared/declarations/facts/…`, `tests/contract/test_concurrency_*.py`, …) which this feature creates | PASS (advisory-only) |
| G6 | `decomposition-check.py --mode tasks` | `proceed` — 33 FR / 137 tasks against ceilings 120 / 160, no reason | PASS |

**Gate blindness carried forward, not repaired here** (routing in § 5): the two `doc-consistency-check.py` faces recorded in the spine's `framework_observations` — the duplicate face is a constant pass for any `.specify/` subject, and the reader face judges only declaration markers. Both are stage-external framework scripts; repair is outside this stage's territory.

---

## 2. FIRST RULING — F-093-004, the `[green: <contract>#<clause>]` marker

### 2.1 The disagreement, stated exactly

| Location | What it says | Shape |
|---|---|---|
| `templates/tasks-template.md:110` | "green-point attribution tag — **this row is the one that turns that contract clause green** … reports: `green-clause-collision` (WARN) [when] **one clause claimed by two rows** … **Partition a contract's clauses across the rows that own them so each clause is claimed exactly once**" | marker **plus** a partition invariant over every clause |
| `.specify/templates/tasks-template.md:110` (runtime mirror) | byte-identical to the line above (`diff` empty) | same |
| `.specify/scripts/python/validate-tasks.py:44-46, 501-516` | `green-clause-collision` = "two rows claim the same contract clause, i.e. the **clause partition** was cut over the same clause twice" | partition invariant only; it never asserts a clause must be claimed at all |
| `.specify/skills/internal/create-tasks/SKILL.md:327-339` | the tag exists for the case where one test file is claimed by verification rows in more than one phase: "Declare the partition with the `[green: …]` attribution tag … and **let the validator judge it**: its `green-path-divergence` check … so this is one machine criterion and MUST NOT also be carried as a second, hand-run one." | marker as the **discharge** of a shared-file obligation; defers the criterion to the validator |
| `.specify/memory/glossary.md:139` 绿点归属 | "**真源 templates/tasks-template.md 的定义行** + 需求 053 的 contracts/green-point-claim.md" | names the owner explicitly |
| `requirements.md` / SC-009 | does not reference a clause registry; requires one definition point per judgement surface and no second value | silent on which reading |

**The disagreement is not binary.** Both pole documents carry *both* readings: the template carries the marker sentence **and** the partition invariant; the skill's operative clause is a pointer to the validator ("let the validator judge it") while its narrative is marker-shaped. What is genuinely contested is the *scope* of the partition invariant — a totality obligation over the clause space, or only over clauses that are claimed at all.

### 2.2 The ruler that decides it

The glossary row for 绿点归属 — the project's vocabulary anchor for exactly this concept — names the owner with no ambiguity: **"真源 templates/tasks-template.md 的定义行"** (with 053's `contracts/green-point-claim.md`). Constitution XIV's owner-selection order is code → machine-generated artifact → **authored document**; `validate-tasks.py` is a *check on* the artefact, not a **definition** of the tag's semantics, and it cites the glossary's clause partition rather than redefining the marker.

**Ruling: the skill/template definition is authoritative.** `[green:]` is a **red-first marker** — the row that first turns a named contract clause green. It is legitimate for a feature to claim a strict subset of its contract clauses (093 claims 35 of 92: the red-first rows for ten test modules and eight fact files).

Corollary, and the part the ruling must record carefully: **the partition invariant survives, scoped to claimed clauses.** The template's normative sentence is literally "Partition a contract's clauses across the rows that own them so each clause is claimed exactly once" — read as a totality obligation it is incompatible with the marker reading (a 92-clause contract cannot be claimed exactly once by 35 rows); read beside the marker sentence it means *the clauses you claim, you claim exactly once*. The marker reading is the only one under which both sentences of the owner document hold together.

### 2.3 What this makes `validate-tasks.py` — and the implement task

`validate-tasks.py` is **behaviourally consistent with the ruling** (it warns on double-claims and never demands a claim), but its *rule text* is drifted in two ways that both matter:

1. It pins the semantics to a totality claim: "the clause partition … was cut over the same clause twice" reads as if a partition over the whole clause space is expected.
2. Its `--help` advertises "the four green-point attribution checks" and says nothing about the clause-space ceiling — so a reader who takes the validator's own text as the definition (which is how F-093-004 arose) is told the opposite of the ruling.

Recorded as an implement-stage row (no framework source is edited in analyze):

> **T138 [US5] (implement, to be added by analyze-repair)** — Repair the `[green:]` semantics in the framework source only: word `green-clause-collision` in `scripts/python/validate-tasks.py` (docstring rule block ~L44-46 and the emitted message ~L501-516) to state the marker reading ("a claimed clause belongs to one row; a feature MAY claim a strict subset of its contract clauses"), and mirror it into the module's `--help` banner. Target files: `scripts/python/validate-tasks.py`, `.specify/scripts/python/validate-tasks.py` (mirror), plus a contract test `tests/contract/test_validate_tasks_green_semantics.py` that goes red if the message or docstring re-acquires a totality claim, and a green-partition assertion on 093's own file (≥1 claim, 0 double-claimed, 0 dangling). The tag's *definition* stays where the glossary puts it (`templates/tasks-template.md`); this row removes only the drifted *description*, per Constitution XIV ("repair converts the copy into a reference rather than re-wording it to agree").
>
> This row is **not** in `tasks.md` yet: adding it is part of the `analyze-repair` dispatch (§ 6), because it is a new row in a gates-green file.

Owner declaration (the ruling's home, so it is not re-derived next time): `templates/tasks-template.md` line 110 is the **owner of the tag's semantics**; `glossary.md` 绿点归属 already declares it; `.specify/templates/tasks-template.md` is its machine-mirrored copy (currently byte-identical — a legitimate duplicate under XIV's mirror rule); `validate-tasks.py` is a **consumer** and its rule text MUST be a pointer, not a second definition.

**F-093-004 → RESOLVED (2026-11-09, analyze).** Evidence: this section + the 35-claimed / 92-clause measurement in G2.

---

## 3. ADJUDICATION — F-093-003, the coordinator dispatch verdict

**The question.** Every one of the 17 agent definitions says, verbatim, "Never dispatch another agent" in § Responsibilities while its frontmatter `capability-tools` omits a dispatch tool; static capability and prose prohibition agree — yet 092 declared six-package parallelism. Is a coordinator allowed to dispatch?

**They are two questions, and only the second one belongs to someone else.**

- **(A) Is `coordinator-dispatch-verdict` a work item of this feature? — yes, implement-stage, and it already is one.** `requirements.md` FR-021 + Clarifications Q&A (2026-11-09) + [[STR-011]] say the owner entry MUST carry *one* verdict reachable within a run, and the spec **MUST NOT presuppose the result** — "两条读法都与已记录意图相容：禁止派发 ⇒ 派发责任归驱动者/主代理；允许派发 ⇒ 协调者能力集须增派发工具". `plan.md` T-004 records the same refusal with two poles and a discriminating evidence pointer (`declaration_reader.py --action get --fact coordinator-dispatch-verdict` before/after). `tasks.md` T096 / T098 / T101 / T105 deliver the *surface* — the fact file, the reader, the routing, the pass-down — none of which depends on which value wins.
  **Therefore F-093-003 does not block implement.** Contract clause **C-072** already gives the fail-closed behaviour for the open window: "the coordinator MUST behave identically when the verdict is absent: refuse to claim concurrency, declare serial with the `mechanism-not-yet-landed` string." Implement can run to completion with the verdict still open, and every downstream reader gets a decidable answer.

- **(B) What value does it carry? — an owner decision, and no instrument this stage holds can settle it.** The verdict turns on a fact about the *host*: whether the coordinator surfaces (`agents/*.md`, the loop driver, the stage seats) are *given* a dispatch tool at run time. Choosing "allow" writes a capability the host may not provide; choosing "forbid" contradicts 092's declared six-package partition and would make T099–T105's routing work unnecessary. Fast-fail's mechanical test applies: explaining a pick needs the word "assumed". **Surfaced, not ruled** — and it is not an ask-for-approval: C-072 makes the open window safe, so the user is naming a fact, not granting permission.

**Disclosure bearing on (B), measured this run.** The five checkpoints, `plan.md` and `tasks.md` § Environment Prerequisites all assert "the planning executor of this line holds `Read, Grep, Glob, Bash, Write, Edit` — no dispatch tool". That is **not the shape of the executor that actually ran those stages**: this analyze stage — the same native host, every stage dispatched as a subagent by the driver — holds the dispatch tool as well as the six, and has opened subagent tasks at the driver's instruction. The recorded premise is false in one direction, and it is the *same* premise whose truth decides (B). Two consequences, both absorbed without inventing intent:

  - **SC-006 stays `not_evaluated`, unchanged.** Whether *this* stage could dispatch is a different unit from whether the feature's own mechanism landed; the mechanism (`effective >= 2` recorded on a real run with per-unit intervals) is still this feature's deliverable and is absent. The feature's own discipline says the honest value is `not_evaluated` — never `0`, never "concurrency proven by a fixture" — and this stage honours it. Do **not** read this disclosure as an attempt to close SC-006.
  - **The premise dispute is a requirements-quality defect**, filed as F-093-012: the stage statement records a tool *set* rather than a runtime *capability*, and its own affected-task pointer is wrong.

---

## 4. Findings

Severity is derived from `propagation_surface` (owner `.specify/skills/internal/analyze-artifacts/references/detection-and-severity.md` § Severity assignment): a row whose surface is `none` is capped at MEDIUM; a row backing an SC / DoD / gate is HIGH.

### CRITICAL

**F-093-009 — `requirements.md` FR-031 carries a literal JavaScript concatenation instead of its normative text.**
The definition row reads: `…concurrency-class 五条条目中 `"+'+'+"serial-reason 五条条目中 `"+'+'+"effective-concurrency 五条条目中 `"+'+'+"decomposition-coverage 五条条目中 `"+'+'+"executor-enumeration-roots 由 [[STR-006]] 记录其落点…`. Four `"+'+'+"` tokens stand where a noun phrase ("在该 fact 文件里落 X 条条目") belongs. Introduced in `11d49f18` (clarify stage) by the quoting accident the project's own "YAML CJK escaping" lesson warns about, and carried through the requirements, plan, tasks and checklist gates because `validate-requirements.py` strips inline code spans before inspecting a row: the corruption sits inside a backtick pair, so every span between backticks is invisible to the validator and the row still reads as a valid 33-FR definition row.
- **Why CRITICAL**: FR-031 is the owner of the land-in-framework-source-and-mirror discipline ([[STR-006]]) — the clause that decides whether every other delivery row edits `shared/`, `skills/`, `scripts/` or their `.specify/` projections. With its text destroyed a reader cannot tell what STR-006 requires, and it backs SC-path artefacts through `feature-ref.md`'s delivery map (FR-031 → declaration-facts C-001…C-003, C-010…C-013).
- **propagation_surface**: `feature-ref.md` § Delivery map, `tasks.md` T099–T105 / T137, `contracts/declaration-facts.contract.md` C-017.
- **Repair (one reading, no new intent)**: FR-031's surviving second paragraph (requirements.md line 182) already states the landing discipline in full sentences, and the corrupted fragment's only content is the per-fact landing locus that FR-033 states as "`shared/declarations/facts/`". Re-express the fragment as a plain sentence naming the five facts and pointing at the fact-layer directory — **invent no clause counts or owner paths the spec does not already state**. No other artefact changes.
- Routed to `analyze-repair`.

### HIGH

**F-093-005 — The FR lane is red, and the delivery map's clauses carry no resolvable FR citation.**
Measured twice (G2 here; the checklist stage's reading): `FR claimed: 25`, `UNCOVERED-FR` = FR-011, FR-013, FR-016, FR-017, FR-025, FR-027, FR-028, FR-033. Root cause measured, not inferred: `_fr_claimed()` in `account-clause-coverage.py` counts ids from *clause citation groups* (the last parenthetical of a clause block containing an FR/SC id — `clause_extract.clause_citations`, owner `shared/definitions/contract-clause-definitions.md` § 4.2), and `grep -c 'FR-0NN\b' contracts/*.md` is **0 for all eight** missing ids. `feature-ref.md`'s delivery map *claims* these FRs are delivered — e.g. FR-011 → "judgement-engine C-029"; C-029's actual citation group is `(FR-007)`, and the FR-011 sentence appears in C-029's **body** as prose, not in its citation group. Seven of the eight are in that state; FR-025 → "high-order-executors C-078" points at a clause with **no citation group at all**, and C-078 is also claimed by no task row anywhere.
- **Why HIGH**: the FR lane is the acceptance link between intent and delivery; a citation the owner's own extractor cannot resolve is an untestable acceptance link, and the map reads green while the lane is red.
- **propagation_surface**: SC-001 / SC-005 / SC-010 sourcing, `tasks.md` DoD-1 ("each FR row resolves to at least one implementation row"), `feature-ref.md` § Delivery map.
- **Repair (mechanical)**: for each of the eight, put the FR id into the *citation group* of the clause the delivery map already names (that is what a citation group is for), or re-point the delivery map at a clause that already cites it. Verified-mechanical part: FR-011 and FR-013 → C-029 (`dependency-edge` / `write-conflict` evidence clauses, whose bodies already say it), FR-016 → C-040, FR-017 → C-069, FR-028 → C-069…C-071, FR-033 → C-085…C-092. FR-025 (C-078 has no group) and FR-027 (C-066 / C-067 groups are `FR-020`, `FR-021/FR-022`) also need the group written, not just extended.
- Routed to `analyze-repair`. Repair target is `contracts/`, not `requirements.md`.

**F-093-006 — Checklist FAIL CHK002: the three derived projection trees are not excluded from the enumeration roots in the requirements text.**
FR-001 names the five roots and excludes exactly one projection ("`agents/`（其 `.specify/agents/templates/` 投影由 FR-032 的镜像纪律覆盖）"). `templates/commands/`'s per-tool copies (`.claude/commands/`, `.qoder/commands/`, `.opencode/command/`, …) and `.specify/skills/`'s 16 flat external projections are excluded **nowhere in `requirements.md`**. Measured: `ls -d skills/internal/*/` = 38, `ls -d .specify/skills/*/` = 16 — treating a projection as a root double-counts the same body. The exclusion reading *does* exist, in two downstream places that are not the requirement: `contracts/declaration-facts.contract.md` C-005's `excluded_layers` (which lists only the spec-local `goal/` / `team/` layers) and `tasks.md` T003's trap-form measurement.
- **Why HIGH**: FR-001 is the scope closed set (SC-001's referent); a root definition that cannot judge its own projection trees out leaves the closed set undecidable at the requirement layer.
- **propagation_surface**: SC-001, C-005, T003, DoD-1.
- **Repair (one reading)**: add the exclusion sentence for the two missing trees to FR-001, in the grammatical shape FR-001 already uses for `agents/`, pointing at the mirror discipline rather than restating it. Then extend C-005's `excluded_layers` to name them (it is the machine face and currently names two of the four).
- Routed to `analyze-repair`.

**F-093-007 — Checklist FAIL CHK008: FR-006's condition↔code bijection is contradicted by its own vocabulary members, and the exemption lives only in a Clarification answer.**
FR-006 requires "FR-005 的每一条件各有且仅有一个同名理由码，FR-006 的每一理由码各对应且仅对应 FR-005 的一个条件，双向缺口数 MUST 为零——一个条件没有理由码，或**一个理由码没有触发条件**，都是缺陷". [[STR-009]] (`single-unit`) and [[STR-010]] (`mechanism-not-yet-landed`) bound no FR-005 condition. The exemption is recorded in the 2026-11-09 Clarifications Q&A ("二者不在『一一映射』约束内 … 由 [[STR-003]] 条目分 `condition-bound` / `factual` 两组成员表达") and in `contracts/declaration-facts.contract.md` C-006 ("`single-unit` … and `mechanism-not-yet-landed` … MUST be `factual` members") — and in **neither** FR-006 nor SC-003, the two normative rows that own the constraint.
- **Why HIGH**: a requirement that literally red-flags two of its own vocabulary members, with the exemption only in a dated record, is a contradictory requirement; SC-003 (the success criterion carrying the bijection) inherits the same hole.
- **propagation_surface**: SC-003, `judgement-engine.contract.md` C-028 / C-029, `declaration-facts.contract.md` C-006, T042.
- **Repair (one reading)**: state the `condition-bound` / `factual` partition inside FR-006's own text ("一一映射约束只覆盖 `condition-bound` 组；`factual` 组成员不对应任何条件，且 MUST NOT 被计为缺口"), and add the same qualifier to SC-003's red-count sentence. The Clarifications answer stays as the dated record and is not edited.
- Routed to `analyze-repair`.

### MEDIUM

**F-093-008 — Checklist FAIL CHK009: the serial-reason vocabulary's member count has no requirement-layer owner, and the two places it appears disagree.**
FR-006 and FR-009 both say the member set belongs to [[STR-003]] and the body MUST NOT restate it, and [[STR-003]]'s `Consumed by` lists FR-006 / FR-007 / FR-009 / FR-031 / SC-003 — none of which is `requirements.md`'s own Clarifications. Clarifications line 287 says "原文列出 6 个理由码" and line 270 names six members; the *measured* body names exactly one (`host-no-parallel`, in 287's question). Nothing in the body says "成员数量与成员清单只以 [[STR-003]] 条目为准，本段是历史记录", so the only count a reader can reach from `requirements.md` sits inside a dated record — which Constitution XIV forbids citing as current reality.
- **propagation_surface**: SC-003, C-006, T042. Capped below the SC tier because SC-003 already names [[STR-003]] as owner and no SC sentence restates a count: the defect is a dangling pointer, not an untestable criterion.
- **Repair (one reading)**: add one pointer sentence under `### Shared Strings`: "`STR-003` 的成员数量与成员清单只以该条目为准；Clarifications 中的数字是历史记录，MUST NOT 被引用为现行取值." Do not edit the dated record.
- Routed to `analyze-repair`.

**F-093-010 — Contract clauses with no citation group are invisible to the FR lane, so their FR coupling is asserted only by `feature-ref.md`.**
Measured: 18 of 92 clauses carry an empty FR set under the owner's extractor — C-011, C-012, C-013, C-018, C-019–C-022, C-026, C-039, C-048, C-062, C-072, C-078, C-080–C-090 (a contiguous run in `existing-semantics-disposal.contract.md`). Several carry a Constitution / requirement coupling in prose ("Constitution XIV", "Constitution IX, R-3"), and `feature-ref.md` maps FR-032 → C-079…C-081, FR-033 → C-085…C-092 anyway — so the lane reads the coupling as absent where the delivery map asserts it.
- **propagation_surface**: FR-032 / FR-033 delivery, DoD-1. MEDIUM, not HIGH: the clauses *are* delivered (84 of them are named by task rows), so this is an accounting defect, not a missing deliverable.
- **Repair**: same mechanical move as F-093-005 on the clause side — C-018 → FR-031, C-062 → FR-032, C-072 → FR-021 / FR-023, C-078 → FR-025, C-080…C-090 → FR-032 / FR-033 per the delivery map. Do **not** invent couplings for C-019–C-022 (engine interface, covered through C-060 / FR-030), C-026 (covered via C-025) or C-048 / C-039 (covered via siblings).
- Routed to `analyze-repair`.

**F-093-011 — SC-006 is `not_evaluated` and this stage cannot close it. Confirmed, not repaired.**
The acceptance mechanism (`effective >= 2` from per-unit dispatch intervals on a real run, `SC-006 Source`) does not exist; the resolver (`concurrency-check.py`) is T021–T025. A stage executor cannot conjure the reading, and `requirements.md` A4 already sanctions post-hoc delivery with a named source. **Stays `not_evaluated`.** Recorded so the next stage does not re-litigate it: the only thing that closes SC-006 is the feature's own engine running on the feature's own implement run.

**F-093-012 — The "host parallel dispatch capability" probe records a tool list rather than a capability, and its affected-task pointer is wrong.**
`tasks.md` § Environment Prerequisites: "the planning executor of this line holds `Read, Grep, Glob, Bash, Write, Edit`, i.e. **no dispatch tool** … affected phases/tasks: T102 and the FR-005(d) condition."
Two measured problems, one factual and one structural: (a) the executor that actually ran the plan / tasks / checklist stages also holds a dispatch tool (§ 3 disclosure), so the probe's verdict is false as recorded; (b) `T102` is "Require the coordinator to report the real execution shape even when serial" — it does not depend on FR-005(d); the rows that do are T101 / T103 / T105 and the SC-006 evidence plan.
- **Why MEDIUM, not HIGH**: FR-005's own text is correct — it routes the runtime fact through `RS-005` ("能力探针结果在运行期记录，MUST NOT 固化在文件里"), so the probe has a legitimate owner and form; what is broken is this file's *recorded instance*.
- **propagation_surface**: SC-006's `not_evaluated` reason code ([[STR-010]]), F-093-003's pole choice.
- **Repair (one reading for (b); (a) is a disclosure, not an edit)**: rewrite the probe's affected-tasks clause to name T101 / T103 / T105 / the SC-006 evidence plan; restate (a) as "the capability is a per-run probe owned by RS-005; this line's stages did not dispatch, and the `mechanism-not-yet-landed` code rides on the feature's own deliverable, not on the host's tool set." That is the fact and it changes no FR or SC.
- Routed to `analyze-repair`.

**F-093-013 — The delivery map's closing claim is a hand count presented as a totality assertion.**
`feature-ref.md` § Delivery map ends with "Count: 33 map rows, 33 distinct FR ids — every requirement reaches at least one clause." The count is true; the *claim* is the thing F-093-005 falsifies — "reaches" is asserted by the map itself and checked by no machine, while the owner's extractor says 8 of 33 do not reach. Repair: after F-093-005 lands, reword the sentence to point at the account-clause-coverage reading as its evidence rather than asserting totality from the table.

**F-093-014 — CHK042's `blocked-by F-093-004` is now resolvable, and the checklist's verdict distribution is stale.**
CHK042 asked whether the *requirements side* presupposes either `[green:]` reading. § 2 answers the upstream question, and the item's own body already records the requirements-side answer (SC-009 does not reference a clause registry → pass). **Not edited in-stage**: `create-checklist` § Recheck forbids refreshing an existing checklist file; the correct form is a `recheck-<date>-<topic>.md`. Recorded so the next checklist pass applies a delta rather than re-reading 44 items.

**F-093-015 — `templates/tasks-template.md` (the green tag's owner) names a one-line-per-task owner that does not exist.**
Line 110: "the one-line-per-task rule is owned by `.specify/templates/commands/tasks.md` § 'One line per task (mechanical-validation contract)'". Measured: `.specify/templates/commands/` does not exist in this worktree; `grep -rn 'One line per task' templates/ .specify/` finds two hits — the pointer itself and `.specify/skills/internal/create-tasks/SKILL.md:274`, **the actual owner** (its heading is literally "**One line per task (mechanical-validation contract)**"). The framework source `templates/commands/tasks.md` does not contain the section either, so this is not a stale-mirror artefact — the pointer is wrong in the source. Downstream: three earlier features repeat the dead path (`063-review-p1-governance/tasks.md:51`, `053-machine-decidable-artifacts/tasks.md:53`, plus this feature's own copy at `tasks.md:110`).
- **propagation_surface**: `none` downstream in 093 (the rule is enforced by `validate-tasks.py` regardless of who owns the text), so MEDIUM under the `none` cap — but it lives in the same owner document as the F-093-004 ruling, so repairing it in the same pass is cheaper than a second round.
- **Repair**: point at `.specify/skills/internal/create-tasks/SKILL.md` § "One line per task (mechanical-validation contract)" in `templates/tasks-template.md` (source) and its `.specify/` mirror.

**F-093-018 — `agents/` citations name a section anchor the files may not carry.**
`requirements.md` FR-021's visibility counter-example, the Clarifications answer and the register's F-093-003 row all say the "Never dispatch another agent" sentence sits in each agent definition's "§ Responsibilities". The load-bearing object is the sentence, not the heading, and a reader who greps the named anchor is sent to a heading rather than to the probe. **propagation_surface**: the F-093-003 evidence chain and T086 / T089 (whose fixtures must read the same sentence the requirement quotes); MEDIUM under the `none` cap because no SC depends on the section name. **Repair**: cite the sentence (`grep -n 'Never dispatch another agent' agents/*.md`), or confirm the heading and correct the three citations.

### LOW

**F-093-016 — FR-001's Clarifications answer routes the projection-mirroring discipline to FR-031 while the body routes it to FR-032.**
Clarifications line 285 says "`agents/`（其 `.specify/` 投影归 FR-031 的镜像纪律）"; FR-001's body and FR-032 both put it at FR-032. The body is the authority and the Clarifications line is a dated record (append-only), so this note stands instead of an edit. Impact: a reader who lands first on the Clarifications mis-routes one citation.

**F-093-017 — `tasks.md` DoD-1 restates a tag count that is wrong and that the F-093-004 ruling removes the need for.**
DoD-1 says the tag "appears on the 34 rows that introduce a test module or a fact file". Measured: `grep -o '\[green: ' tasks.md | wc -l` = 38, of which 3 are the `<contract>#<clause>` placeholder in the format legend / DoD text, leaving 35 tag-bearing rows. The count is a restated fact with no owner *and* it is off by one; under the ruling it should not be restated at all. **Repair**: replace with the machine-checkable property ("every row carrying the tag claims a distinct clause; `validate-tasks.py` exits 0 with 0 WARN"), which DoD-1 already states in its next sentence.

---

## 5. Framework observations routed (not repaired in-stage)

Carried into the spine's `framework_observations`; each is a stage-external script or template, so repair belongs to a framework pass, not to this feature.

1. **`validate-requirements.py` strips inline code spans before reading a definition row, so a row whose normative text is corrupted inside a backtick pair still validates.** F-093-009 is the live instance; the checklist stage's "blockquote-wrapped text is invisible" observation is the sibling failure mode. The validator is a filter, not a totality assertion.
2. **`account-clause-coverage.py`'s FR lane counts citation *groups*, not clause bodies** — an FR mentioned in a clause's prose counts as uncovered even though a human reading the contract sees the coupling. Correct per the owner's § 4.2 definition, and useful: it surfaced F-093-005. The actionable form — "a delivery map MUST cite from a citation group" — is stated by no owner today.
3. **`doc-consistency-check.py` duplicate face is a constant pass for any `.specify/` subject** (`is_excluded_path` filters before `--path` is honoured) — recurrence 2 (092, 093); a green from it carries no information. Fix shape: honour an explicit `--path` even inside an excluded tree.
4. **`doc-consistency-check.py` reader face judges only `READER_MARKERS`** — it never resolves CHK anchors; `reader=pass` means "the file declared its readers", never "the items are good".
5. **A framework source template can name an owner that does not exist and nothing notices** (F-093-015). A pointer-resolution check over `templates/` would catch it; three prior features copied the dead path.
6. **The stage record's "executor tool set" is not a property of the host** (F-093-012): five consecutive stages asserted "no dispatch tool" from one probe, while the executor running them held one. A capability recorded as a constant is exactly what `requirements.md` RS-005 forbids — the framework's own stage protocol commits the defect the feature exists to fix.

---

## 6. Repair brief — CRITICAL + HIGH only (dispatch `analyze-repair`)

Repair is a **specification-text edit authoritative in the requirement / contract layer only**; no framework source is edited in analyze or in the repair.

| id | file | one-line change | done when |
|---|---|---|---|
| F-093-009 | `requirements.md` FR-031 | replace the `"+'+'+"` fragment with a plain sentence naming the five facts and pointing at `shared/declarations/facts/`; reuse FR-033's wording, invent nothing | the concatenation token count is 0; the FR row is still exactly one definition row; `validate-requirements.py` 0/0 |
| F-093-005 | `contracts/*.md` citation groups (6 places) + `feature-ref.md` if an FR must be re-pointed | FR-011 / FR-013 → C-029's group; FR-016 → C-040; FR-017 → C-069; FR-028 → C-069…C-071; FR-033 → C-085…C-092; FR-025 / FR-027 need the group created on C-078 / C-066-C-067 | `account-clause-coverage.py --corpus-root …` reports `FR claimed: 33` and an empty `UNCOVERED-FR` list |
| F-093-006 | `requirements.md` FR-001 + `contracts/declaration-facts.contract.md` C-005 | add the two missing projection exclusions in FR-001's existing grammatical shape; extend `excluded_layers` to the same four | a reader can judge `.specify/skills/*/` out of the roots from `requirements.md` alone |
| F-093-007 | `requirements.md` FR-006 + SC-003 | state the `condition-bound` / `factual` partition in FR-006's own text; add the same qualifier to SC-003's red-count sentence | no vocabulary member is red-flagged by its own FR; SC-003's count is group-scoped |
| also | `tasks.md` | add T138 (the `[green:]` rule-text repair row, § 2.3) and apply F-093-012 / F-093-017 (both DoD / Environment-Prerequisites text) | `validate-tasks.py` 0/0 with 138 rows; `decomposition-check --mode tasks` still `proceed` |

Everything else in § 4 is MEDIUM / LOW and may ride the same pass or be left; each has its one-reading repair stated above. **Do not** touch the dated Clarifications records, `coverage-baseline.txt` (T006 owns it), or any framework script.

After repair: re-run G1 / G2 / G3 and the three `pre-analyze-check` stages; the verdict flips to READY-TO-IMPLEMENT iff CRITICAL = HIGH = 0.

---

## 7. Coverage summary (FR → task → SC → evidence)

| lane | reading | state |
|---|---|---|
| FR → contract clause (citation groups) | 25 / 33 | red — F-093-005 (repair listed) |
| FR → implementation row (task text by id) | FR-011 / FR-016 / FR-025 / FR-027 appear only through their clause and DoD-1's row, never by id | red — same root cause; DoD-1's "each FR resolves to at least one implementation row" is the sentence that must be true |
| clause → row (`[green:]`) | 35 / 92 claimed, 0 double-claimed, 0 dangling | **correct under the F-093-004 ruling** (marker reading); the totality reading was the wrong pole |
| SC → red-first module | 12 / 12 mapped in `feature-ref.md` § Measurement map | green (static) |
| SC-001…SC-006 (`final`) | SC-006 `not_evaluated` by design (F-093-011); SC-001…SC-005 rest on modules that do not exist yet | as designed — the modules are T027 / T042 / T066 / T086 / T090 |
| DoD-1…DoD-9 → GATE-1…GATE-7 | consistent, one reading each (after F-093-017) | green |
| constitution | IV (test-first: DoD-3 + nine contract modules + one unit module), XIV (one source of truth: F-093-015 is the live drift, § 2.2 is the repair direction), XVI (fast-fail injection for subagents: T103 + C-042), XX (concurrent-by-default: the feature's subject) | no unmet MUST outside F-093-009 / F-093-015 |

---

## 8. Final verdict

**NOT-READY** — CRITICAL 1 (F-093-009), HIGH 3 (F-093-005, F-093-006, F-093-007). The brief in § 6 is short, mechanical, and every change has exactly one reading already recorded in the artefacts. `next_action`: **dispatch analyze-repair**.
