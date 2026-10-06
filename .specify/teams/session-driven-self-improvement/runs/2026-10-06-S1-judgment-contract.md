# 运行判定契约 (Run Determination Contract) — S1

**Stage**: S1 `judgment-contract-designer` · **Team**: `session-driven-self-improvement` · **Date**: 2026-10-06
**Status**: design patch in run workspace. NOT canonical. Landing is the Meta supervisor's act.

> **Ownership (declared per `shared/guidelines/one-source-of-truth.md`).** This file is the
> design-time owner of exactly six facts, and only until S3/S4 land: (1) the four quantities'
> 判定口径 and value domains; (2) the three evidence lanes' read surfaces and projections;
> (3) the `run_determination` output record schema; (4) the 改点 shape and its boundary against
> `intervention.json`; (5) the two consumption points; (6) the SI-4 routing conclusion for
> commands and memory. After landing, ownership of (1)(2)(5)(6) migrates to the landed framework
> source (`shared/workflow/feedback-step.md`, `shared/workflow/self-improvement-workflow.md`,
> `templates/instructions-template.md`), and ownership of (3)(4) migrates to **code** —
> `scripts/python/run-determination.py` — per the owner-selection tier 1 rule. This file then
> becomes a dated record and MUST NOT be cited as current reality.
>
> Everything else named here reaches its owner by path. No table, threshold, or enumeration
> that already has an owner is restated.

---

## 0. Naming

| Surface | Form | Note |
|---|---|---|
| Prose (zh) | **运行判定** | ratified through the user approval channel 2026-10-06 |
| Prose (en) | **Run Determination** | deliberately avoids *assessment* — 情境评估 (Situational Assessment) already owns it |
| Identifiers / paths | `run-determination` | engine file, action names, CLI flags |
| Record fields | `run_determination`, `snake_case` | matches `feedback-utils.py`'s existing field style (`unit_id`, `run_id`, `should_prompt`) so the two records join without a translation layer |
| Record kind string | `speckit.run-determination` | mirrors `speckit.evidence-findings` |

**Retired forms, MUST NOT appear in any landed text**: 「断言」 (collides with contract-test
assertion throughout this repo, including Feature 053's subject matter; deliberately *not*
registered as a glossary variant) and 「判断逻辑」 (a description, not a term; survives only as a
glossary variant). Owner of the naming history and both retirements:
`.specify/memory/glossary.md` → `运行判定` entry (`origin=user`, `status=confirmed`).

**Known terminology divergence (recorded, not repaired here)**: `.specify/goal/session-driven-self-improvement/goal.md`
still reads 「判断逻辑」 in both `## Objective` and `## Success Criteria`. That file is in this
team's `territory.forbidden` and `/speckit.goal` is its only authoring entry, so this contract
does not touch it. Per `.specify/teams/session-driven-self-improvement/team.md` § 四量口径裁定,
that section's user adjudication supersedes the goal's wording until `/speckit.goal modify`
adopts the new name. See `## Open items` OI-5.

---

## 1. Relationship to 情境评估 (proactive-trigger) — read this before confusing them

The two mechanisms are **structural siblings with disjoint jobs**. A reader who has met one will
assume the other; this section exists to stop that.

| | 情境评估 (Situational Assessment) | 运行判定 (Run Determination) |
|---|---|---|
| Question asked | 「现在处于什么情境、可执行哪个流程」 | 「刚跑完的这一轮跑得怎么样」 |
| Cadence | every user turn | once per completed run, at wrap-up |
| Object judged | project state (lifecycle stage, pending signals) | the run itself (four measured quantities) |
| Output | one non-blocking suggestion line, or silence | one `run_determination` record (the 改点) |
| Durable state | rule set + promotion counters + one telemetry row per turn | the determination record only |
| Owner | `shared/guidelines/proactive-trigger.md` | this contract → landed surfaces named in § 14 |

**Shared structural trait, deliberately reused**: both are *program-side* judgments in which the
caller passes coarse signals it already holds from context and the program performs the fixed-rule
resolution. The precedent for that split is `proactive-trigger.md` § Evidence Budget & Escalation
and its `--compliance-done` clause ("declared by the caller, never inferred").

**Hard separation clauses** (all three are MUST NOT):

1. 运行判定 MUST NOT call, extend, or reuse the `assess` action, and MUST NOT write a telemetry
   row. Telemetry's row schema is a closed key set owned by
   `.specify/specs/050-proactive-flow-trigger/contracts/trigger-engine.md` (C-14) — adding a key
   there is out of this team's territory.
2. 运行判定 MUST NOT add a situation, a signal word, or a rule. That vocabulary grows only through
   the user approval channel (`proactive-trigger.md` § Maintenance Duties item 2), and
   `shared/guidelines/proactive-trigger.md` is in this team's `territory.forbidden`.
3. 情境评估 MUST NOT be made to carry run-quality semantics. It has no measurement surface and its
   evidence budget forbids opening artifact files.

---

## 2. Engine identity, actions, exit codes

**Canonical home** (from `territory.write`, which authorizes exactly one new engine):
`scripts/python/run-determination.py`. Existing engines MUST NOT be modified except where § 14
names the change. Tool-reuse gate was applied first (`shared/workflow/tool-reuse-gate.md`): no
existing engine owns this capability — `feedback-utils.py` owns the feedback store, `evidence-utils.py`
owns evidence collection/comparison, `trigger-utils.py` owns per-turn situational assessment,
`memory-utils.py` owns the memory store. The determination is a fifth, distinct job.

**Actions (closed set for v1)**:

| Action | Write? | Purpose |
|---|---|---|
| `determine` | yes (one record, § 7) | Evaluate the four quantities for the run that just reached wrap-up; emit and persist the record. Also settles the latest unsettled record for the same `unit_id` when `--prev-user-turn-class` is supplied (§ 4). |
| `settle` | yes (amends one record) | Resolve the `satisfaction` axis of an already-persisted record whose verdict is `not_evaluated / pending_next_turn`, given the next user turn's class. Used when the settling turn belongs to a later session or a different unit. |
| `history` | no | Projection of past records for the active flow's *why* step (§ 11). Never returns record bodies wholesale. |

`--json` MUST be provided by a shared parent parser and every action MUST end on the same
emit path — the shape defect documented at `.specify/specs/053-machine-decidable-artifacts/contracts/run-checks.md`
C-11 (a per-action `--json` flag silently loses to argparse defaults) MUST NOT be reproduced.

**Exit codes**: reuse the house table `0 = ok / 2 = input-error / 3 = not-found / 4 = invalid`
(optionally `1 = usage`). Owner is **code** — the `EXIT_*` module constants shared by
`scripts/python/derive-utils.py`, `goal-utils.py`, `interview-utils.py`, `trigger-utils.py`;
the authored statement of the same table is STR-007 in
`.specify/specs/053-machine-decidable-artifacts/requirements.md` § Shared Strings. One code MUST
NOT carry two meanings across actions of this binary.

**Non-zero engine exit is load-bearing elsewhere**: any engine the run invokes reports through
that same table, and a non-zero exit is one of the two producers of `unresolved_red` for the
satisfaction axis (§ 5.4). This is the only way B2's "退出码表全仓一致" enters this contract.

---

## 3. Determination unit, key, and scope gate

- **Key**: `(unit_id, run_id)`, byte-identical in vocabulary to `feedback-step.md` § Reflection
  procedure step 4 and step 5's `--unit-id` / `--run-id`. `unit_id` ∈ {`/speckit.<command>`,
  `skill:<name>`, `custom:<owner>/<name>`}. This is what makes the passive handoff (§ 10) a join
  rather than a translation.
- **Nesting**: one determination per qualifying unit, mirroring `feedback-step.md` § Nesting rule.
  A command that invokes a skill produces two determinations, each scoped to its own unit. The
  same `(unit_id, run_id)` MUST NOT be determined twice — the engine no-ops on a repeat, exactly
  as the feedback engine does.
- **Scope gate (complexity)**: `complexity` is a **caller-declared input**
  (`--complexity complex|simple`), not an engine derivation. Rationale (One Source of Truth): the
  criterion is owned by the `feedback-step.md` header, and the derived per-command classification
  is already pinned by `.specify/specs/027-feedback-mechanism/contracts/command-classification.md`
  and `tests/contract/test_feedback_command_classification.py`. A second derivation inside this
  engine would be a drifting copy. The engine's only job here is enforcement: `simple` ⇒ emit
  `{"skipped": "simple-unit"}`, exit 0, write nothing.

---

## 4. Invocation model (this is what makes default-accept work at all)

The satisfaction axis needs information that does not exist at wrap-up: whether the *next* user
turn continues the topic, changes it, or ends the session. Two-invocation model, one call site:

1. **At wrap-up of run N** — `--action determine`. Quantities 1–3 are fully evaluated. Quantity 4
   gets `verdict: not_evaluated`, `reason: pending_next_turn`, and the record is persisted
   unsettled. In the same call, if `--prev-user-turn-class` is supplied, the engine first settles
   the latest unsettled record for this `unit_id` using the **current** turn's class — so run N−1's
   satisfaction is resolved by run N's wrap-up, with no extra call site.
2. **Late settlement** — `--action settle` when the settling turn arrives in a later session or
   under a different unit (including `session_end` observed after the fact).

**Default-accept therefore fires normally**, because settlement rides on the next determination
call rather than on a separate hook. If settlement never happens (session abandoned mid-run), the
axis stays `not_evaluated / pending_next_turn` — honest, never a fabricated `accepted`.

**Honesty boundary (declared, mirroring `proactive-trigger.md` § Telemetry & Retention 度量边界)**:
the engine cannot prove that a wrap-up which never called `determine` did not exist. Unsettled
records are visible via `--action history --unsettled`; absence of a record is not evidence of a
clean run.

---

## 5. The four quantities

All four are named in `.specify/goal/session-driven-self-improvement/goal.md` § Success Criteria
and adjudicated in `.specify/teams/session-driven-self-improvement/team.md` § 四量口径裁定
(B1–B4, 2026-10-06, user ruling). This section implements that ruling and MUST NOT be re-derived
downstream.

### 5.0 Shared value domains and the closed reason set

Comparison words `improved / unchanged / regressed` are **borrowed, not defined** — owner:
`shared/workflow/self-improvement-workflow.md` SI-8. `not_evaluated` is **borrowed, not defined** —
owner: STR-004 in `.specify/specs/053-machine-decidable-artifacts/requirements.md` § Shared
Strings, whose rule is the one this contract enforces everywhere: *a quantity that was not
evaluated MUST report `not_evaluated`, MUST NOT report `ok`, and MUST NOT report zero.*

SI-8's fourth word `Unobserved` is deliberately **not** reused: it would create a second literal
for the same state. It collapses into `not_evaluated` + `reason: no_baseline`.

`reason` is a **closed enumeration** (grows only by revising this contract, then the landed owner):

`source_unavailable` · `not_comparable` · `no_baseline` · `no_declared_checks` · `green_unproven` ·
`red_adjacent` · `red_state_undeclared` · `no_user_input` · `pending_next_turn` · `unqualified_run`

| Axis | Value domain |
|---|---|
| `token_consumption.verdict` | `improved` \| `unchanged` \| `regressed` \| `not_evaluated` |
| `elapsed.verdict` | `improved` \| `unchanged` \| `regressed` \| `not_evaluated` |
| `artifact_correctness.verdict` | `ok` \| `regressed` \| `not_evaluated` |
| `satisfaction.verdict` | `accepted` \| `rejected` \| `not_evaluated` |

`improved`/`unchanged`/`regressed` do not appear on `artifact_correctness` (a failed-set difference
is not a trend) and `ok` does not appear on the two comparison axes (`unchanged` already means it).

**No aggregate score — hard constraint.** This contract defines **no** scalar roll-up, no weighted
sum, no severity number. Two owners forbid it: `shared/guidelines/fast-fail.md` § 范围限制 item 2
rejects a scoring-and-threshold device because a continuous quantity is not reproducible between
two reviewers, and B2 rejects mixing 制品正确性 with 语义正确性 into one number because a mixed
number cannot be scored. The only roll-up is the boolean `passive_trigger.trigger_feedback`,
derived by the enumerated rule in § 10 — a routing bit, not a score.

### 5.1 `token_consumption` (token 消耗)

**Ruling**: program-measurable — but `shared/guidelines/token-efficiency.md` § 消耗观察 states
that exact token counts are often unavailable and MUST NOT be fabricated, prescribing qualitative
description or line/byte proxy metrics instead. This contract therefore fixes an explicit source
hierarchy rather than assuming a counter exists.

`measurement.source` is a closed enumeration, tried in order:

| # | `source` | Where it comes from | Comparability |
|---|---|---|---|
| 1 | `tool_session_usage` | `message.usage` on assistant rows of the AI-tool session JSONL (`input_tokens`, `output_tokens`, `cache_read_input_tokens`, `cache_creation_input_tokens`), summed over the run's row span. Store path resolution reuses the existing `STORE_RESOLVERS` in `scripts/python/history-utils.py` — that dict is the owner of *which* agent CLIs are resolvable today, and `UNSUPPORTED_TOOL_HINTS` in the same file is the owner of which are not. Neither list is restated here. | exact |
| 2 | `line_byte_proxy` | Lines/bytes of a caller-declared read set (`--proxy-paths`), the proxy form `token-efficiency.md` § 消耗观察 authorizes ("行/字节,仅用于同一流程前后对比"). | proxy, same-unit comparisons only |
| 3 | `unavailable` | Neither of the above obtainable. | — |

**Unavailable-source behaviour (normative)**: `source = unavailable` ⇒ `verdict: not_evaluated`,
`reason: source_unavailable`. MUST NOT report `ok`. MUST NOT report `0`. MUST NOT substitute an
estimate, a training-knowledge figure, or a value carried over from another unit's run. This is
the joint requirement of `token-efficiency.md` (不编造具体数值) and `fast-fail.md` § 生长闭环 两条红线
(MUST NOT 编造数值;取不到就如实写"不可得").

`source = line_byte_proxy` compared against a baseline measured with `tool_session_usage` ⇒
`verdict: not_evaluated`, `reason: not_comparable`. Mixing an exact count with a byte proxy in one
trend is exactly the "two reviewers, two verdicts" failure the house disciplines exist to prevent.
The record carries `baseline.source` so the mismatch is visible rather than silent.

A free-text `note` (the qualitative description `token-efficiency.md` also authorizes) MAY be
carried on any source value. It is echoed, never parsed, and MUST NOT influence the verdict —
`token-efficiency.md` § 判定边界 assigns semantic judgement to the model and forbids the program
from pretending to decide it.

**Baseline**: the same `unit_id`'s most recent **settled** record's measurement. No baseline ⇒
`not_evaluated / no_baseline`. **No absolute threshold exists anywhere and this contract MUST NOT
invent one**: the goal's `## History` records that the "各定一个经验值作为目标" criterion was
deliberately deleted. Should an absolute target ever be wanted, that is a user decision (OI-3).

**Noise control is already owned**: a one-unit regression is `regressed` and that is fine, because
`shared/workflow/evidence-step.md` § Positioning & Red Lines item 3 (计数只路由) forbids a count
signal from generating an optimization point or candidate by itself. The comparison verdict routes;
it does not conclude. § 10's trigger rule adds a second, structural guard.

### 5.2 `elapsed` (耗时)

Same shape as 5.1, different source hierarchy:

| # | `source` | Where it comes from |
|---|---|---|
| 1 | `tool_session_timestamps` | Per-row `timestamp` in the same AI-tool session JSONL; run span = last row of the run minus first row of the run, in milliseconds. Availability owned by the same `STORE_RESOLVERS` / `UNSUPPORTED_TOOL_HINTS` pair as 5.1. |
| 2 | `caller_declared_ms` | `--elapsed-ms <int>`, a wall-clock span the caller measured itself. |
| 3 | `unavailable` | — |

**Unavailable-source behaviour**: identical to 5.1 — `not_evaluated / source_unavailable`; never
`ok`, never `0`, never an estimate.

**Declared, not inferred**: `caller_declared_ms` is a caller declaration in exactly the sense of
`trigger-utils.py`'s `--compliance-done`. The record carries `measurement.source` so a declared
span is distinguishable from a measured one; § 11's active flow MUST surface that difference
rather than presenting both as measurements.

**Baseline / threshold / noise**: as 5.1. Direction is `reduce`.

### 5.3 `artifact_correctness` (正确性 — 制品正确性 ONLY)

**Scope statement (normative, and the axis says so explicitly)**: this axis covers **制品正确性
(artifact correctness) only**. **语义正确性 (semantic correctness — did the agent answer the
user's question correctly) is out of scope for this contract and no axis, placeholder or
otherwise, is defined for it.** Per B2, semantic correctness is not program-decidable; both
candidate routes (LLM review, named human review) are legitimate but break Program-First, and if
it is ever added it MUST be declared as an **independent axis** and MUST NOT be folded into this
one, because a mixed number cannot be scored. Recorded as OI-4 rather than designed.

**口径 (B2, verbatim in substance)**: `ok` requires the conjunction of
(a) the name-level failed-set difference is empty, **and**
(b) every check that returned green carries red-first evidence or a mutation-drill record.

All three pieces of machinery already exist; the engine wires them and invents none:

| Piece | Existing owner | Engine use |
|---|---|---|
| Sorted FAILED nodeid list | `scripts/bash/run-tests.sh --names-out <file>` | consumed as `--names-current <file>` / `--names-baseline <file>` |
| Name-level difference | `名字级基线` glossary entry; `comm -13 baseline current` | computed program-side; **names only**, never pytest output bodies |
| Red-first evidence | `Red-First 取证` glossary entry; live instances at `.specify/specs/{051,052,053}-*/notes/red-first-evidence.md` | literal-substring search for each declared green check name inside `--red-first-refs <paths>` — the Program-First positive example `token-efficiency.md` § 程序优先 names (`grep` for a literal, not "paste the doc and let the model look") |
| Mutation drill | `变异演练` glossary entry | same search, accepted as an alternative to red-first |
| Per-check exit reporting | STR-007 table (§ 2) | a non-zero engine exit inside the run also feeds § 5.4 |

**Sub-signals (both always present; no information is collapsed away)**:

- `failed_set_diff`: `{status: empty | non_empty | not_evaluated, added: [<nodeid>…], added_count, truncated}`.
  `added` is bounded — name list only, capped, with `truncated: true` when the cap binds
  (Summary-First: a projection, never a pytest transcript).
- `green_evidence`: `{status: complete | partial | absent | not_evaluated, uncovered: [<check name>…]}`.

**Verdict mapping (fixed rule, engine-side)**:

| Condition | `verdict` | `reason` |
|---|---|---|
| run declared zero checks | `not_evaluated` | `no_declared_checks` |
| baseline names file missing | `not_evaluated` | `no_baseline` |
| `failed_set_diff.status = non_empty` | `regressed` | — |
| diff `empty` **and** `green_evidence = complete` | `ok` | — |
| diff `empty` **and** `green_evidence ∈ {partial, absent}` | `not_evaluated` | `green_unproven` |
| `qualification ≠ qualified` | `not_evaluated` | `unqualified_run` |

The last-but-one row is a **contract interpretation of B2, not a literal quote** — B2 states the
口径 for `ok` but not the verdict when only the second conjunct fails. The reading chosen here
follows `shared/guidelines/fast-fail.md` § 判据同样覆盖机器给出的绿 ("a green that would not go red
when its subject breaks is not evidence") plus the 盲检 glossary entry: an unproven green means the
axis was not validly evaluated, not that something regressed — nothing did regress, and the
regression axis is the diff, which stays separately visible. The alternative reading (`regressed`)
was rejected because it would make "new failure" and "old green never proven" indistinguishable in
the record. Listed for ratification as OI-1.

**Boundary (B2's 诚实声明, restated as a MUST because it is the axis's own scope rule)**: only runs
that **declared checks** are covered. An undeclared run reports `not_evaluated`, MUST NOT report
`ok`. Consistent with STR-004's rationale and with `run-checks`' treatment of short-circuited
checks (`.specify/specs/053-machine-decidable-artifacts/contracts/run-checks.md` C-13).

**Mandatory anti-vacuity sentinel** (the check that would not go red when its subject breaks proves
nothing — `fast-fail.md` § 判据同样覆盖机器给出的绿; term owner: `反空真哨兵` glossary entry):
an `empty` diff MUST be accompanied by an assertion that the comparison was meaningful. The engine
MUST assert at least one of: `added_count`-source `current` file is non-empty, the baseline file is
non-empty, or the run declares `--collected <n>` with `n > 0`. If none holds, the axis reports
`not_evaluated / no_declared_checks`, **not** `ok`. Without this, "pytest collected nothing" and
"pytest passed everything" produce the same empty diff — the FF-2/FF-3 blind-check class.

### 5.4 `satisfaction` (满意度)

The pre-existing rule (recorded as a dated prior value in `goal.md` § History) survives with the
**two user-mandated modifications from B3**, both applied here:

**(a) The hedge 「大部分情况」 is deleted.** A program needs a decision rule, not a probability.
The rule below is a total function over a closed input domain: there is no "usually", no
confidence, and no residual case.

**(b) Default-accept is KEPT, with one narrow exception.** Topic change or session end ⇒
`accepted`, because that is what holds the noise floor low enough for passive triggering to be
usable at all; replacing it wholesale with `not_evaluated` would leave the axis permanently without
input and the mechanism would never fire. The single exception: a topic change or session end
**immediately adjacent to an unresolved red** records `not_evaluated`, not `accepted`.

**Inputs** (both closed enumerations):

- `--user-turn-class ∈ {continuation_negative, continuation_non_negative, topic_change, session_end, no_user_input}`.
  The **classification** is a semantic judgment — whether a turn continues the previous topic and
  whether it is negative — so it belongs to the model per `token-efficiency.md` § 判定边界. The
  **mapping** from classification to verdict is a fixed rule and belongs to the engine per
  § 程序优先. This is the same split `proactive-trigger.md` already uses (`--stage` / `--signals`
  caller-supplied, resolution deterministic).
- `--unresolved-red ∈ {true, false, unknown}` with `--red-source ∈ {engine_nonzero_exit, surfaced_anomaly_unanswered, none, undeclared}`.
  "Unresolved red" means exactly B3's two producers: a non-zero engine exit (STR-007 table, § 2),
  or an anomaly the agent surfaced and the user never responded to (`fast-fail.md` § 上送件与披露).

**Decision rule (total, no default fallthrough)**:

| `user_turn_class` | `unresolved_red` | `verdict` | `reason` |
|---|---|---|---|
| `continuation_negative` | any | `rejected` | — |
| `continuation_non_negative` | any | `accepted` | — |
| `no_user_input` | any | `not_evaluated` | `no_user_input` |
| `topic_change` \| `session_end` | `false` | `accepted` | — (default-accept) |
| `topic_change` \| `session_end` | `true` | `not_evaluated` | `red_adjacent` |
| `topic_change` \| `session_end` | `unknown` | `accepted` | `red_state_undeclared` |

**"Immediately adjacent" — decidable definition**: the red belongs to the run being determined, and
the `topic_change` / `session_end` turn is the **first** user turn after that run's wrap-up. Because
`determine` runs at wrap-up and § 4's settlement passes the *next* turn's class, adjacency is
exactly "the class being settled is the class of the turn right after the red's run". No timestamp
window, no tunable span.

**Where the red state comes from — and why B3's stated source cannot supply it.** B3 rules that
"本回合是否存在未解决的红" is derivable from `proactive-trigger`'s per-turn telemetry and that no new
store may be built for it. **The derivability premise is falsified by the shipped schema**: rows in
`.specify/memory/trigger/telemetry.jsonl` carry exactly seven keys (`turnId`, `assessed`,
`escalated`, `suggested`, `complianceDone`, `visibleOutput`, `ts`), pinned as a *closed* set by
`.specify/specs/050-proactive-flow-trigger/contracts/trigger-engine.md` C-14 and shaped by
`trigger-utils.py:shape_telemetry_row`. None expresses an engine exit code or a surfaced anomaly,
and neither `shared/guidelines/proactive-trigger.md` nor that contract is in this team's write
territory. **The no-new-store half of the ruling is honored** — nothing here creates one — by making
the red state a **caller declaration** (`--unresolved-red` / `--red-source`) in exactly the sense of
`trigger-utils.py`'s `--compliance-done` ("declared by the caller, never inferred"), and by
recording it in the determination record itself, which is this mechanism's own artifact. Surfaced as
ANOMALY-1; the alternative resolutions are OI-9.

**`unknown` row — why it is `accepted` and not `not_evaluated`, and what that costs.** B3 forbids
collapsing the axis into `not_evaluated`, and the paragraph above establishes that the red state is
not derivable from any existing per-turn store. So `unknown` must not disable default-accept, or the
axis dies. The cost is that the exception's reach depends on caller honesty — the same accepted
limitation `proactive-trigger.md` declares for its own caller-supplied ordering flag. The record
carries `reason: red_state_undeclared` so an honest reader can tell a *derived* accept from an
*undeclared* one, and `--action history` MUST be able to count them separately.

**Known coupling (user accepted knowingly, B3)**: the exception makes `satisfaction` depend on the
correctness axis, so the four quantities are not mutually independent. Owner of that acceptance:
`.specify/teams/session-driven-self-improvement/team.md` § 四量口径裁定 B3 (dated adjudication
record). B3 also names the decoupling option — narrow the trigger to `engine_nonzero_exit` only —
and its cost. This contract does not take that option; it is OI-2.

**No user text is stored.** The record carries the classification only. Raw user input MUST NOT be
persisted into a determination record: it is user data (red line 2 of `feedback-step.md` §
Positioning & Red Lines) and it would be carried into a package path that was never designed for
it (red line 3). If a note is genuinely needed it belongs in the feedback entry's `## Review`,
owned by `feedback-step.md`.

---

## 6. The three evidence sources and their read surfaces

Summary-First is binding (`shared/guidelines/token-efficiency.md` § 摘要优先): machine-managed
data files MUST NOT be injected wholesale into model context. The **program** reads originals
freely; the **model** receives projections. Each lane below states the projection concretely enough
for S2 to implement it as a field list.

### Lane 1 — session history records, `.specify/memory/session/`

- **Read surface**: `scripts/python/memory-utils.py --action list --scope session` or
  `--action recall --scope session --query <q> --limit <n>`. Both already return **index entries,
  not bodies** — `recall` returns `{count, matches[]}` where each match is an index row plus
  `score` and `path`. That is the projection; no new one is needed.
- **Field projection**: `id`, `source`, `feature`, `tags`, `title`, `created`, `summary`, `path`.
  Entry bodies are opened only by walking the escalation ladder in `token-efficiency.md` § 升级阶梯
  with a recorded reason, or when the body qualifies under § 小文件阈值 (that section owns the
  numbers; they are not restated here).
- **Role in the determination**: this lane is also the record's own durable home (§ 7), which is
  why the active flow's *why* step can read past determinations through the same surface.

### Lane 2 — user input

- **Read surface**: **the current turn's user text already in context — zero additional reads.**
  This is the same evidence budget `proactive-trigger.md` § Evidence Budget & Escalation sets:
  rely on what is already in context, escalate only on declared conditions.
- **What crosses into the program**: only the closed-enumeration `--user-turn-class` (§ 5.4) and,
  for the *why* of an active run, at most a caller-written topic label. **Never the raw text.**
- **Program-side corroboration available but not wired by default**: the AI-tool session store
  carries machine-readable user-action signals (a `toolDenialKind` field with values including a
  user-rejection form, and rows with an error `level`). Whether S2 reads them is a tool-availability
  question, since the store schema is per-agent-CLI and only the resolvable tools are reachable.
  Recorded as OI-6 — this contract neither requires nor forbids it, and MUST NOT be read as
  authorizing a schema assumption about a tool the resolvers do not cover.

### Lane 3 — LLM investigation conclusions, `.specify/memory/evidence/`

- **Read surface**: `scripts/python/evidence-utils.py --action latest --target <unit-id>` (returns
  `runId`, `path`, `created`, `ageDays`, `stale`, plus a freshness `warning`) and
  `--action list --target <unit-id> --limit <n>` (returns index entries: `runId`, `target`,
  `created`, `lanesSummary`, `file`). Freshness is gated by `stale`; an over-age run MUST NOT be
  consumed silently.
- **Per-finding field projection** (the concrete bound S2 implements): from `findings.json`, take
  `evidence[] | {id, lane, evidenceState, summary, signals}` and the top-level `findingsDigest`.
  **Excluded**: `evidenceRefs` bodies, `lanes/*` raw files, `manifest.json` engine block, and the
  `findings.json` file as a whole. The store holds over a hundred files across its run
  directories; wholesale injection is the exact failure `token-efficiency.md` § 摘要优先 names, and
  it is also the failure mode the feedback reflection step's own Token 三问 asks about.
- **`findingsDigest`** (a sha256 over the findings) is the identity/freshness key: the
  determination record stores it so a later reader can tell whether the evidence it cited has
  since been recollected.
- **Red lines inherited, not restated**: `evidenceState` semantics are not redefinable, `Unobserved`
  evidence MUST NOT be turned into a defect candidate, and counts only route — all three owned by
  `shared/workflow/evidence-step.md` § Positioning & Red Lines.

---

## 7. Output record schema (field names in `run_determination` form)

One determination produces exactly one record. **The record IS the 改点** — `.specify/memory/glossary.md`'s
`改点` entry defines it as "运行判定每判定一次即产出的一条记录", so the two are one artifact, not
two, and no second store or second file kind is introduced.

```jsonc
{
  "kind": "speckit.run-determination",
  "schema_version": 1,
  "unit_id": "/speckit.plan",              // § 3 vocabulary, joins to feedback
  "unit_type": "command",                   // command | skill | custom-unit
  "run_id": "<stable-run-id>",              // feedback-step step 4 convention
  "feature": "<requirement-key-if-any>",    // NEVER overloaded with the registry ID
  "feature_id": "<Feature-registry-ID-if-any>",
  "determined_at": "<UTC ISO-8601>",
  "settled_at": null,                       // non-null once satisfaction is resolved
  "complexity": "complex",                  // caller-declared (§ 3)
  "qualification": "qualified",             // qualified | trivial | aborted | partial

  "axes": {
    "token_consumption": {
      "verdict": "regressed",               // § 5.0 domain
      "reason": null,                       // closed set, § 5.0; null when verdict is substantive
      "measurement": { "source": "tool_session_usage", "input_tokens": 0,
                       "output_tokens": 0, "cache_read_input_tokens": 0,
                       "proxy_lines": null, "proxy_bytes": null, "note": null },
      "baseline": { "run_id": "<prev>", "source": "tool_session_usage", "value": 0 },
      "signal": { "key": "token_consumption", "direction": "reduce" }
    },
    "elapsed": {
      "verdict": "unchanged", "reason": null,
      "measurement": { "source": "tool_session_timestamps", "ms": 0, "note": null },
      "baseline": { "run_id": "<prev>", "source": "tool_session_timestamps", "value": 0 },
      "signal": { "key": "elapsed", "direction": "reduce" }
    },
    "artifact_correctness": {
      "verdict": "not_evaluated", "reason": "green_unproven",
      "declared_checks": 0, "collected": 0,
      "failed_set_diff": { "status": "empty", "added": [], "added_count": 0, "truncated": false },
      "green_evidence": { "status": "absent", "uncovered": [] },
      "evidence_refs": [],                  // paths only, bounded
      "signal": { "key": "artifact_correctness", "direction": "improve" }
    },
    "satisfaction": {
      "verdict": "not_evaluated", "reason": "pending_next_turn",
      "user_turn_class": "no_user_input",
      "unresolved_red": { "present": "unknown", "source": "undeclared" },
      "adjacent": false,
      "signal": { "key": "satisfaction", "direction": "improve" }
    }
  },

  "change_point": {                         // § 8; ALWAYS present
    "id": "cp-<run_id>",
    "clean": false,                         // true <=> findings == []  (anti-vacuity sentinel)
    "findings": [
      { "axis": "artifact_correctness", "verdict": "not_evaluated", "reason": "green_unproven",
        "observation": "<one bounded line: what was measured, never what to fix>",
        "signal": { "key": "artifact_correctness", "direction": "improve" },
        "evidence_refs": ["<path>"],
        "status": "observed" }              // ALWAYS "observed" — see § 8
    ]
  },

  "passive_trigger": {
    "trigger_feedback": false,              // § 10 derivation
    "composes_with_should_prompt": true,    // constant; documents § 10's composition
    "out_of_scope": [                       // § 12; recorded, never acted on this turn
      { "observation": "<one line>", "parked_via": "todo|spec|none", "ref": "<path-or-id>" }
    ]
  },

  "provenance": {
    "engine": "scripts/python/run-determination.py",
    "declared_by_caller": ["complexity", "user_turn_class", "unresolved_red", "qualification"],
    "lanes_read": { "session": "available", "user_input": "in_context", "evidence": "stale" },
    "evidence_digests": ["sha256:…"],
    "honesty_boundary": ["red state is caller-declared, not derived (§ 5.4)",
                          "unsettled records are invisible to absence (§ 4)"]
  }
}
```

**Schema rules S2 MUST enforce**:

1. Every axis object is present in every record. An axis with no source is `not_evaluated` with a
   `reason` — never omitted, never `null`, never zero-valued.
2. `reason` is non-null **iff** `verdict` is `not_evaluated`. That biconditional is a contract test.
3. `change_point.clean == true` **iff** `change_point.findings == []`. A clean record still exists;
   a record whose findings are empty because nothing looked is forbidden. This is 反空真哨兵 applied
   to the record itself.
4. `findings[].status` is the constant `observed`. No other value is representable (§ 8).
5. `signal` reuses the `{key, direction}` shape of `expectedSignal` in
   `shared/workflow/evidence-step.md` § Step E, so a finding can become a ledger entry without a
   translation layer.
6. Records are bounded: no field carries a transcript, a file body, an evidence-ref body, or raw
   user text. `--action history` returns projections only.

**Durable landing (normative default, ratification requested as OI-2)**: the record is persisted
through the **existing** memory engine — `memory-utils.py --action record --scope session
--source <unit_id> --tags run-determination,<run_id>` — into `.specify/memory/session/`. The chain
that makes this the non-invented choice:

- `goal.md` § History (D1) states the active flow's *why* is obtained **from session history**;
  landing the record there is what makes that literally true rather than aspirational.
- `memory-utils.py` already owns `record / recall / list / prune / reindex` and the index
  projection; the store's `session` scope is defined as ephemeral in-flight working state, which is
  precisely what an unsettled determination is.
- Its enforced `--source` contract accepts exactly `/speckit.<command>` and `skill:<name>`, i.e.
  this mechanism's `unit_id` — no boundary is stretched.
- It adds **no new store**, satisfying SI-7's "do not create a parallel self-improvement database"
  and `fast-fail.md` § 范围限制 item 4.

The body of the memory entry is the JSON record; the `summary` frontmatter field carries one line
(`unit_id` + the four verdicts), which is what lane 1's projection then exposes.

---

## 8. 改点 (Change Point): shape and boundary against SI-7

**Identity** (owner: `.specify/memory/glossary.md` → `改点` entry): an observation **sensor inside
the improve flow**. Two boundaries are constitutive, and both are enforced by the schema:

1. **Not a standalone feedback entry.** The record has no `disposition`, no threshold, no package
   path, and it is never written under `.specify/memory/feedback/`. It therefore never enters the
   feedback counter and never influences `should_prompt`.
2. **Not an intervention ledger.** `findings[].status` is the constant `observed`. There is no
   `change` field, no `targetFinding`, no `baselineRunId`, no outcome state, and no mutation
   authority anywhere in the record.

**The distinction against `intervention.json`, stated so it cannot be collapsed later**:

| | 改点 (`change_point`) | `intervention.json` |
|---|---|---|
| Workflow moment | SI-1 observation | SI-7 record, after a targeted change |
| Written by | `run-determination.py` | the improve flow executing `evidence-step.md` Step E |
| Lands in | `.specify/memory/session/` (§ 7) | the **baseline evidence run directory** |
| Keyed by | `(unit_id, run_id)` | `targetFinding` / `baselineRunId` / `expectedSignal` |
| Resolved by | `--action history` (active flow's *why*) | SI-8 `evidence-utils.py --action compare` |
| Can it authorize a mutation | **no** | it records one that already happened |

**Direction of the join is one-way**: a 改点 finding's `signal.key` is the vocabulary that later
becomes `intervention.json.expectedSignal.signalKey`, and its `evidence_refs` are candidate
`targetFinding` ids. The 改点 **feeds** the ledger. It never replaces it, and the ledger never
reads back into it.

**Why the anti-fork rule is about the join, not about turf** (owner: the `改点` glossary entry):
`intervention.json` must sit beside the baseline evidence in the same run directory or SI-8's
`--action compare` cannot resolve it. Moving or duplicating that ledger would break the comparison
chain. The three structural reasons a wholesale self-improvement→feedback merge is **not** done are
recorded in `territory.non_path` (`type: framework-convention`) of the team definition; this
contract adopts them and does not restate them.

**Clean runs**: `change_point.clean == true` with `findings == []`. The passive consumer then
records the single line `feedback-step.md` § Reflection procedure step 2 already owns
(`No significant optimization points identified this run.`) — no hollow finding is invented to fill
the array, per `fast-fail.md` § 生长闭环 两条红线 and § 干净运行也要显式说一句.

---

## 9. Generalizing `feedback-step.md`'s three unnamed judgment layers

**The user's ruling is that this is a generalization of an existing mechanism, not a new one.**
Precisely what that means, layer by layer — what is reused verbatim, and what is new:

| # | Existing layer (owner: `shared/workflow/feedback-step.md`) | Today | Under 运行判定 | Reused | New |
|---|---|---|---|---|---|
| L1 | header: "a command is complex iff it invokes scripts/CLI tools, produces an artifact another flow consumes, or consumes another flow's artifact" | prose criterion; the per-command list is *derived* and re-derived by hand (§ Notes for embedders) | becomes the record's `complexity` field and the engine's scope gate (§ 3) | the criterion text and its owner stay put; the derived list stays pinned by `contracts/command-classification.md` + `test_feedback_command_classification.py` | an enumerated **field** with a value domain, and enforcement (`simple` ⇒ no determination) instead of re-derivation prose |
| L2 | step 1: "Gate on qualification & completion" | a binary prose judgment ("reached wrap-up and did substantial work") performed by the agent each time | becomes `qualification ∈ {qualified, trivial, aborted, partial}` | the trivial-skip rule, the Abort/partial-run rule, and the `--partial` flag semantics are all consumed as-is | an enumerated field that **feeds the axes**: `qualification ≠ qualified` forces `not_evaluated / unqualified_run` on every axis, so an aborted run can no longer be reported green |
| L3 | step 6: `should_prompt` | a store-level threshold judgment, `feedback-utils.py:should_prompt(count, threshold)` | unchanged and **not re-implemented** | ownership stays entirely with the feedback engine, including the threshold and `SPECKIT_FEEDBACK_THRESHOLD` | a second, orthogonal boolean `passive_trigger.trigger_feedback` that composes with it (§ 10) |

**The generalization claim, stated exactly**: 运行判定 is the **conjunction of L1 + L2 + L3 plus
four measured axes, evaluated once per run by one program**, replacing three separately-performed
prose judgments that today each cost an agent a fresh reading of the same file. It generalizes them
in *shape* — from "one binary judgment, re-derived by a model at each wrap-up" to "one enumerated
record, computed by a program at each wrap-up". It does **not** absorb their owners: each layer's
criterion text stays in `feedback-step.md`, the derived command list stays pinned by its existing
contract test, and `should_prompt` stays in the feedback engine. Nothing here creates a second
definition point for any of the three.

**What is genuinely new** (and this is the whole of it): the two comparison axes and their
measurement sources; the `artifact_correctness` conjunction and its anti-vacuity sentinel; the
`satisfaction` decision table; the durable record; and the boolean that composes with `should_prompt`.

---

## 10. Consumption point A — the passive trigger

**One concrete point**: `shared/workflow/feedback-step.md` § Reflection procedure, at the
**step 1 → step 2 boundary**.

- The `--action determine` call is inserted at **step 1**. Its `qualification` field *is* step 1's
  answer, so step 1's prose gate becomes a reference to the engine's verdict rather than a fresh
  agent judgment (L2 in § 9).
- Its four axis verdicts and `change_point.findings` become **step 2's grounded input**: the review
  prose and the "≥1 concrete, unit-specific optimization point" are written from measured axes
  instead of impression. Step 2's existing Token 三问 self-check is unchanged and now has a measured
  `token_consumption` axis to cite rather than a guess.
- Steps 3 (scope guard), 4 (dedup), 5 (persist via the feedback engine) are unchanged. The
  determination record is **not** a feedback entry (§ 8), so it never enters the step-5 call.

**Handoff to the feedback flow — the composition rule (fixed, engine-side)**:

```
trigger_feedback =
     qualification == qualified
 AND (   artifact_correctness.verdict == regressed
      OR satisfaction.verdict        == rejected
      OR ( token_consumption.verdict == regressed AND elapsed.verdict == regressed ) )
```

The prompt at **step 6** fires only when `trigger_feedback` **and** the feedback engine's own
`should_prompt` are both true. Neither replaces the other: `should_prompt` remains the store-level
threshold owned by `feedback-utils.py`; `trigger_feedback` is this run's routing bit. Requiring both
is what keeps the noise floor where red line 2 needs it.

The deliberate asymmetry — a single regressed comparison axis does **not** trigger — is the
structural noise guard that replaces a tolerance band (§ 5.1): one slow run is recorded and left for
the active flow; only a run that is both slower and heavier, or that broke something, or that the
user rejected, reaches the feedback flow. It also directly serves § 12.

**Red-line check (all four, `feedback-step.md` § Positioning & Red Lines)**:

1. *Target = the framework.* The record's `unit_id` is always a Spec Kit command or skill, and a
   finding's `observation` describes framework friction. Tool-session telemetry is a **meter read**,
   not a subject: the engine MUST NOT emit a finding whose object is the LLM, the agent CLI, or the
   user's project code.
2. *User data, fully optional.* Nothing in the record solicits anything, and no flow blocks on it.
   `trigger_feedback` only feeds a non-blocking notification.
3. *Zero automated transmission.* The determination writes one local memory record and nothing
   else. It has no network path and MUST NOT gain one.
4. *Local workaround value.* `--action history` is a read-only aid for the active flow; it never
   gates execution.

**Never-solicit line**: the passive path **infers** from user input; it does not ask the user for
feedback content. `--user-turn-class` is a classification of a turn that already happened, produced
by the agent from context it already holds (§ 6, lane 2). No question is put to the user, no prompt
is added, and no new user-facing surface class is created. That is why this wiring clears the line.

---

## 11. Consumption point B — the active trigger

**One concrete point**: `templates/commands/improve.md` (created by S4) delegates — as a thin
entry-plus-delegation shell per the `command-logic-as-classified-skills` T-003 convention — to the
improve skill, whose **`why` step** is the consumption point.

Mapping onto D9 detail 2's `why → what → how` (that three-part shape is the *flow's* internal
structure, not this team's stage plan):

| Segment | What it consumes | Read surface |
|---|---|---|
| **why** — what is the current problem | past `run_determination` records for the target unit: the four verdicts, their `reason`s, and the `signal`s | `run-determination.py --action history --target <unit-id>` (projection: verdicts + reasons + signals + `settled_at` + `provenance.declared_by_caller`; never record bodies wholesale), corroborated by lane 1 `memory-utils.py --action recall` |
| **what** — which aspects need improving | `change_point.findings` of those records, then SI-2 evidence qualification | `evidence-utils.py --action latest/list` + the § 6 lane-3 projection |
| **how** — analyze, explore, implement | SI-3 diagnosis → SI-4 routing (§ 13) → SI-5 apply → SI-6 validate → SI-7 ledger | `shared/workflow/self-improvement-workflow.md`, referenced not copied |

Two MUSTs for the *why* step: it MUST surface whether a figure was measured or caller-declared
(`provenance.declared_by_caller`, `measurement.source`) rather than presenting both as
measurements; and it MUST report `not_evaluated` axes as **not evaluated**, never as fine.

---

## 12. Passive non-exhaustiveness (D9 detail 3)

The passive path MUST NOT be exhaustive: acting on everything it can see would interfere with the
current flow, which is the whole reason the constraint exists.

- **In scope for the passive turn**: findings whose `unit_id` equals the current unit and whose axis
  was actually evaluated in this run. Those, and only those, feed `trigger_feedback`.
- **Everything else is recorded, not acted on**: written to `passive_trigger.out_of_scope[]` in the
  same record, one bounded line each, with the mechanism that will carry it forward.
- **The two concrete carry-forward mechanisms**:
  - **`/speckit.todo` Park Mode** — a free-floating improvement idea, parked into
    `.specify/memory/todo/` and listed later by `/speckit.todo --list`. Owner of the mode, the store
    path, and the frontmatter projection: `templates/commands/todo.md`. This is the default.
  - **A new spec via `/speckit.requirements`** — when the finding constrains *what this project's
    source must implement*, it belongs to the Requirement plane rather than to a parked idea. The
    litmus test and the plane boundary are recorded in the team definition's `territory.non_path`
    (`type: cross-goal`); this contract cites them and does not restate them.
- `parked_via ∈ {todo, spec, none}`. `none` is legal and means "recorded, no carrier assigned yet";
  it is the active flow's job to assign one.

Nothing in this section authorizes the passive path to widen the current turn, to open a second
flow, or to emit more than the single non-blocking notification `feedback-step.md` step 6 already
owns.

---

## 13. SI-4 routing for commands and memory

`shared/workflow/self-improvement-workflow.md` SI-4 today names an improver for four subject kinds
only. Both gaps this contract was asked about are answered below — one concluded, one concluded
with an explicitly named pending improver and a named decider. Neither is left silent.

### 13.1 Command templates — **subject: concluded. Improver: pending, decider named.**

Applying the five criteria of `shared/definitions/self-improvement-definitions.md` § Execution
Subject to `templates/commands/<name>.md`:

| Criterion | Holds? | Evidence |
|---|---|---|
| 1. invoked repeatedly | yes | every `/speckit.*` invocation |
| 2. owns or references an execution contract | yes | the template *is* the execution contract |
| 3. produces observable run evidence | yes | feedback entries keyed `/speckit.<command>`; evidence lane `target` uses the same vocabulary (`evidence-step.md` Step A) |
| 4. one canonical editable definition | yes | `templates/commands/<name>.md`, with per-tool copies regenerated by `scripts/python/regen-command-copies.py` — mirrors, not subjects |
| 5. can route a durable change for a later execution | yes | edit the template, regenerate copies, next invocation carries it |

**Conclusion**: a command template **is** an Execution Subject. The definitions table simply does
not list the kind; the criteria do, and all five hold. SI-4 therefore needs a row.

**But no improver exists**: `skills/` has `improve-agent`, `improve-skills`, `improve-tools`,
`improve-team`, `improve-docs` — and no `improve-commands`. A command template is not a document, so
`improve-docs` is the wrong route.

**Interim routing — taken from an existing owned rule, not invented**: SI-4 leaves the subject
without an authorized mutation route, and `self-improvement-workflow.md` § Failure and Degradation
already prescribes the response to exactly that condition — *degrade to Assisted Improvement*. So
until an improver exists, a command subject routes to its normal assisted flow: edit
`templates/commands/<name>.md`, then `regen-command-copies.py`, then SI-6 validation.

**SI-4 row to add** (S3 lands it):

```
| Command template | pending — no `improve-commands` improver exists; degrade to Assisted
  Improvement per § Failure and Degradation. Canonical owner `templates/commands/<name>.md`
  + `scripts/python/regen-command-copies.py`. |
```

**Decider for closing the pending**: the **user**, through `/speckit.team` modify authorizing a
named `skills/improve-commands/` directory. That is the same authorization path S4's skill-side
landing already requires (S4 quality gate in the team definition), because `territory.write`
deliberately excludes `skills/**` — the 13687-file scale risk recorded in the team's granularity
declaration. This contract MUST NOT pre-create that directory name into anyone's territory.

### 13.2 Memory — **concluded: not an Execution Subject; no SI-4 row.**

Applying the same five criteria to the memory store (`.specify/memory/session/`,
`.specify/memory/knowledge/`):

| Criterion | Holds? | Why |
|---|---|---|
| 1. invoked repeatedly | **no** | a store is not invoked; the *skills* `memory-record` / `memory-recall` and the *engine* `memory-utils.py` are |
| 2. owns or references an execution contract | **no** | it is data. Its shape is described by `docs/reference/skills/memory.md`, which is documentation about it, not a contract it executes |
| 3. produces observable run evidence | **no** | it *is* evidence — § 6 lane 1 consumes it as such |
| 4. one canonical editable definition | **no** | many independent entries, appended and pruned; there is no single definition to edit |
| 5. routes a durable change to that definition | **no** | a change is an entry add/prune performed by the owning skill, not a mutation of a definition |

**Conclusion**: memory is **not** an Execution Subject. It matches the definitions table's existing
row for artifacts that fail the criteria — an improvement *target* or Harness asset, routed to its
normal assisted flow. So SI-4 needs **no memory row**, and adding one would misclassify a store as a
subject.

D9 detail 4 lists memory among the open set of improvement objects; that is satisfied without an
SI-4 row, by routing memory-domain findings to the artifacts that *are* subjects or that have
owners:

| Memory-domain finding | Route | Status |
|---|---|---|
| `memory-record` / `memory-recall` skill behaviour | SI-4's existing **Skill** row → `improve-skills` | concluded |
| `memory-utils.py` engine behaviour | non-subject artifact → its normal assisted flow (SI-4's existing closing sentence) | concluded |
| store shape / retention / scope boundary | `docs/reference/skills/memory.md` owner workflow | concluded |
| registry content (`.specify/memory/features.md`, `glossary.md`, `tools.md`, `constitution.md`) | each file's own owning command (`/speckit.feature`, `/speckit.instructions`, `/speckit.tools`, `/speckit.constitution`) | concluded |

### 13.3 Two related notes

- **The 运行判定 engine itself is not a subject.** A script is a non-subject artifact; its
  definition record would be a Tool record if one is ever authored (`/speckit.tools`). The
  determination *record* is evidence, not a subject.
- **SI-2's `/better-harness` reference is dangling.** No `templates/commands/better-harness.md`
  exists, yet `self-improvement-workflow.md` SI-2 names `/better-harness` as an escalation target.
  This contract does not repair it — the disposition belongs to S3/S4 under the team's write
  territory and is one of S5's named checks. Recorded as OI-7 so it is not lost.

---

## 14. Landing constraints (S3 / S4 / Meta — all binding)

1. **Confirmation-gate budget is at ceiling with zero margin.** `scan-confirmation-gates.py`
   `SCAN_DIRS` covers `templates/commands`, `skills`, `shared`; `SCAN_ROOT_FILES` covers
   `templates/*.md`. Three of this team's write targets sit inside those surfaces
   (`shared/workflow/feedback-step.md`, `shared/workflow/self-improvement-workflow.md`,
   `templates/instructions-template.md`, plus the new `templates/commands/improve.md`).
   **No landed text may introduce a new match of the scanner's `BLOCKING_PATTERNS` tuple.** The
   tuple is owned by `scripts/python/scan-confirmation-gates.py` and is **not restated here** —
   read it there. Run the scanner before landing and attach the `total` reading; the ceiling value
   is recorded in the team definition's `territory.non_path` (`type: ceiling`), which is a dated
   record, so the live reading is the scanner's, not that note's.
   - **Specific drift trap**: `feedback-step.md` step 6 currently reads
     "inviting the user to **run** the `/speckit.feedback` command". The pattern tuple contains a
     nearby form differing only in verb and object. That clause MUST be preserved verbatim; any
     rewording of it MUST be re-scanned. Owner of the safe wording: `feedback-step.md`
     § Threshold prompt protocol.
   - **Reusable guard shape**: `tests/contract/test_confirmation_gates_sweep.py` already
     parametrizes a "this surface adds nothing to the gate count" assertion. S3/S4 SHOULD extend
     that parametrization to the new surfaces rather than write a second guard.
   - **Precedent for the accepted cost**: `shared/guidelines/fast-fail.md` § 已接受的代价 records
     that this budget forces *wording-level* design avoidance, and that avoidance MUST NOT be
     achieved by changing the semantics of a rule. The same limit applies here.
2. **Two hats.** Land in framework source at the repository root. `.specify/` is a generated
   mirror; regenerate through `scripts/python/sync-mirrors.py`, never hand-edit
   (`shared/definitions/dogfooding-definitions.md` § 2.1). Note the path-resolution trap that file
   names: a walk-up heuristic self-matches in this repo.
3. **Instructions size and propagation.** A new ambient `## Run Determination` section in
   `templates/instructions-template.md` carries **summary + pointer only**, in the pointer shape
   `one-source-of-truth.md` § Reference, don't copy permits — never the value domains, reason set,
   or decision table. Two existing tests bound it: `tests/contract/test_instructions_size_budget.py`
   and `tests/contract/test_instructions_section_propagation.py`.
4. **Contract tests, red first.** New structural tests land in `tests/contract/` with red-first
   evidence or a mutation-drill record — the same standard § 5.3 measures other runs by. A test
   whose subject could break without the test going red is a 盲检 and MUST be fixed before it is
   cited as evidence.
5. **One Source of Truth on landing.** After S3/S4 land, this contract's six owned facts have new
   owners (§ header). The landed surfaces MUST cite each other by path; none may restate a value
   domain, a threshold, or an enumeration that another surface owns. If changing one of these facts
   would require editing more than one landed file, the landing is already broken.

---

## 15. Verification hooks for S5

Stated so S5 can check without re-deriving:

- **Value-domain closure**: every axis object present in every record; `reason` non-null iff
  `not_evaluated` (§ 7 rules 1–2). Mutation drill: drop an axis → the guard MUST go red.
- **Unavailable-source honesty**: for each of the four axes, a run with no source yields
  `not_evaluated`, never `ok` and never `0` (§ 5.1–5.4). Mutation drill: force a zero → red.
- **Anti-vacuity sentinel on the diff**: an empty diff with nothing collected yields
  `not_evaluated`, not `ok` (§ 5.3). Mutation drill: feed an empty names file → red.
- **Anti-vacuity sentinel on the record**: `clean == true` iff `findings == []` (§ 7 rule 3).
- **Satisfaction table totality**: the § 5.4 table covers the full cross-product of
  `user_turn_class × unresolved_red` with no fallthrough. Guard: exhaust the product.
- **改点 / ledger separation**: no `change`, `targetFinding`, `baselineRunId`, or outcome field
  anywhere in the record; `findings[].status` is the constant `observed` (§ 8).
- **No new store**: the engine writes only through `memory-utils.py`; no new directory appears
  under `.specify/memory/` (§ 7).
- **Red lines**: the four checks in § 10, plus "never solicit" — no landed text asks the user for
  feedback content on the passive path.
- **Gate budget**: scanner `total` reading attached, unchanged from the pre-write baseline captured
  in `.specify/teams/.work/session-driven-self-improvement/progress.md`.
- **SI-4**: the command row exists with the pending improver and the named decider; **no** memory
  row was added (§ 13).

---

## Open items

> Each item names its options and its decider. None was resolved silently. Items marked
> **blocking** must be answered before the affected stage lands; the rest are recorded for later.

**OI-1 — Ratify the `green_unproven` verdict mapping (§ 5.3).** *Blocking S2's contract tests, not
its code.* B2 fixes the 口径 for `ok` but not the verdict when the diff is empty and red-first /
mutation evidence is missing. Options: (a) `not_evaluated / green_unproven` — chosen here, follows
`fast-fail.md` § 判据同样覆盖机器给出的绿 and keeps "new failure" distinguishable from "old green
never proven"; (b) `regressed` — simpler domain, but conflates the two. **Decider**: user, via the
team supervisor; S2 may implement (a) now because both sub-signals stay visible in the record, so
switching to (b) later is a mapping change, not a schema change.

**OI-2 — Ratify the record's durable landing point (§ 7).** *Blocking S3.* Options: (a) through
`memory-utils.py` into `.specify/memory/session/` — chosen here, because `goal.md` D1 says the
active flow's *why* comes from session history, the `session` scope is defined as ephemeral
in-flight state, the enforced `--source` contract already accepts `unit_id`, and it adds no new
store; (b) into the evidence run directory beside `findings.json` / `intervention.json` — stronger
co-location with SI-7/SI-8, but evidence run ids (`ev-<ts>-<target>`) are minted by
`evidence-utils.py --action collect` and do not match feedback's `run_id`, so the join to
`(unit_id, run_id)` would need a second key; (c) a new store — **rejected**, it is the parallel
database SI-7 forbids and `fast-fail.md` § 范围限制 item 4 rejects. **Decider**: user, via the team
supervisor. S2 is not blocked: only the persistence adapter changes.

**OI-3 — Absolute targets for token and elapsed (§ 5.1, § 5.2).** *Not blocking.* This contract
defines only relative comparison, because `goal.md` § History records that the empirical-threshold
criterion was deliberately deleted and no artifact owns a threshold today. If an absolute target is
ever wanted, options are: (a) keep relative-only; (b) a user-configured per-unit target. **Decider**:
user, through `/speckit.goal modify` (the criterion is goal-plane text) — this contract MUST NOT
invent a number.

**OI-4 — 语义正确性 as a future independent axis (§ 5.3).** *Not blocking; explicitly not designed.*
B2 rules it out of scope for this round and requires that, if added, it be an independent axis and
never folded into 制品正确性. Both candidate routes (LLM review, named human review) break
Program-First, so adding it is a discipline decision, not a design one. **This contract defines no
placeholder axis for it** — a placeholder that reports `not_evaluated` forever is indistinguishable
from an axis nobody built, which is the exact confusion STR-004 exists to prevent. **Decider**: user.

**OI-5 — goal.md still carries the retired term (§ 0).** *Not blocking; not repairable here.*
`goal.md` § Objective and § Success Criteria still read 「判断逻辑」, and § Success Criteria still
says 「正确性」 without B2's split. Only `/speckit.goal modify` may write that file, and it is in
`territory.forbidden`. The team definition already records this as a to-do outside the team's
authority. **Decider**: user, via `/speckit.goal modify`.

**OI-6 — Whether to read tool-session user-action signals (§ 6, lane 2).** *Not blocking.* The
AI-tool session store carries machine-readable signals of user rejection and error-level rows.
Options: (a) do not read them — chosen for v1, because the schema is per-agent-CLI and only the
tools in `history-utils.py STORE_RESOLVERS` are reachable, so a v1 read would silently work for two
agents and silently return nothing for the rest; (b) read them where resolvable and record
`red_source` provenance per tool. **Decider**: S2 proposes, supervisor rules; escalate to the user
if (b) is chosen, since it makes the satisfaction axis's reach tool-dependent.

**OI-7 — SI-2's dangling `/better-harness` reference (§ 13.3).** *Not blocking this contract;
blocking S5's checklist.* No such command template exists. Disposition is inside S3/S4's write
territory and is already one of S5's named checks. **Decider**: team supervisor at S3/S4 dispatch.

**OI-8 — Tolerance band for the comparison axes (§ 5.1).** *Not blocking; likely never needed.*
Exact comparison means a one-token increase reads as `regressed`. v1 handles the noise
structurally rather than numerically: `evidence-step.md` red line 3 (计数只路由) forbids a count
from generating a candidate, and § 10's trigger rule requires both comparison axes to regress
before the passive path fires. If empirical noise still shows up, the options are (a) keep exact
comparison, (b) add a user-configured tolerance. **Decider**: user — a tolerance is a threshold and
no artifact owns one.

**OI-9 — How the `unresolved_red` input is produced (§ 5.4).** *Blocking S3's wiring text, not S2's
code.* B3 ruled the red state derivable from `proactive-trigger` telemetry; the shipped seven-key
closed row schema does not carry it, and the files that own that schema are outside this team's
territory. Options: (a) **caller declaration** — chosen here, mirrors the existing
`--compliance-done` precedent, honors B3's no-new-store clause, and costs caller honesty (mitigated
by `reason: red_state_undeclared` being countable); (b) extend the telemetry row schema with a red
key — makes the exception machine-derived, but requires revising `trigger-engine.md` C-14's closed
set and `proactive-trigger.md`, both forbidden to this team, so it needs a user-authorized territory
change; (c) narrow the exception to `engine_nonzero_exit` only, which B3 itself names as the
weaker-coupling alternative — but it does not cover "an anomaly was surfaced and the user never
responded". **Decider**: user, via the team supervisor. S2 implements (a) behind a single input flag,
so (b) or (c) is a producer change, not a schema change.

---

## Appendix — facts this contract verified rather than assumed

Recorded so S2 does not re-derive them, and so a reviewer can check the derivations:

- `scripts/bash/run-tests.sh` implements `--names-out <file>` and writes a sorted FAILED-nodeid
  list; the `comm -13` name-level comparison is the house form (`名字级基线` glossary entry).
- Live `red-first-evidence.md` instances exist under `.specify/specs/{051,052,053}-*/notes/`;
  `baseline-failed.txt` instances exist under multiple `.specify/specs/<feature>/` directories.
- The exit-code table `0 / (1) / 2 / 3 / 4` is implemented as `EXIT_*` module constants in
  `derive-utils.py`, `goal-utils.py`, `interview-utils.py`, `trigger-utils.py`; `goal-utils.py`
  additionally defines `EXIT_BLOCKED = 5` for `run-checks`.
- `not_evaluated` is an established literal (STR-004) with the "short-circuited check MUST NOT
  report green" rule already contracted at `run-checks.md` C-13.
- `.specify/memory/trigger/telemetry.jsonl` rows carry exactly seven keys
  (`turnId`, `assessed`, `escalated`, `suggested`, `complianceDone`, `visibleOutput`, `ts`), pinned
  as a closed set by `trigger-engine.md` C-14 and shaped by `trigger-utils.py:shape_telemetry_row`.
  **No key expresses an engine exit or an unresolved anomaly** — consequence and options at § 5.4
  and OI-9.
- The AI-tool session JSONL for resolvable agents carries `message.usage` token fields and per-row
  `timestamp`, which is what makes § 5.1 source 1 and § 5.2 source 1 real rather than aspirational.
- `evidence-utils.py` already returns index-level projections (`--action list`, `--action latest`)
  and `findings.json` already carries a `findingsDigest`; `memory-utils.py --action recall` already
  returns index rows with `score` and `path` and no bodies. Both lanes' Summary-First projections
  therefore exist and need no new machinery.
- `templates/commands/improve.md` does not exist yet; `skills/` contains no `improve-commands`.
- 22 of the 25 command templates carry `## Feedback`; the derived simple set is pinned by
  `tests/contract/test_feedback_command_classification.py` (this contract cites the owner rather
  than the list).
