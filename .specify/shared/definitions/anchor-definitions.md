# Anchor Definitions Reference

Canonical definition of the **Anchor** (锚点) concept in Spec Kit. This file is the **sole owner** of five facts, and every other surface reaches them here by path instead of restating them:

1. **the Anchor concept** — the project-level, long-horizon, cross-deliverable authored end state, and its composition;
2. **the archive layers** — where each definition store lives, which filename each layer carries, and the closed `--scope` member set;
3. **the binding record** — the shared three-key ownership record every Anchor, every action-level Goal and every team carries;
4. **the lifecycle** — the shared value set and its transition discipline;
5. **Target decomposition and the Anchor–Team binding** — the two mechanics that hang off an Anchor.

The **action-level Goal** is a different concept with its own owner: `shared/definitions/goal-definitions.md`. That file defines what a Goal is, how it is composed and where it lives; it cites this file by path for the binding record and the lifecycle and MUST NOT restate either. The engine's action signatures and exit codes are owned by `scripts/python/goal-utils.py` and are cited, never restated here. The **team side** of the model — the team's application of the binding, its lifecycle value pair, `handoff_ref`, and the construction-crew notion — is owned by `skills/internal/create-team/references/conceptual-model.md`; this file cites it by path and section. It sits alongside the other concept owners: `tool-definitions.md`, `agent-definitions.md`, `subagent-definitions.md`.

## What an Anchor Is

An **Anchor** is a **project-level, long-horizon, cross-deliverable authored end state** that the project keeps pursuing across many deliverables and many runs. It is a **first-class concept** — an authored fact source, never a derived artifact — and it answers the question *whither*: toward what end state, and to what degree it has been reached.

Its composition is exactly three parts:

1. **Objective narrative** — the desired end **outcome** (north star). Shape is governed by GD-2 below: an outcome, never a task list, an implementation plan, or a sequence of phases.
2. **Verifiable success criteria** — at least one threshold / satisfaction condition an evaluator (a program or a scoring agent) can measure progress against. A definition carrying zero verifiable criteria is not an Anchor.
3. **Lifecycle state** — `active` / `achieved` / `abandoned`, owned below. Terminal Anchors are retained, never deleted.

An Anchor MAY additionally carry, as **annexes** on the same footing — optional, never composition parts:

- **Targets** — the run-assignable decomposition (see Target Decomposition below). Targets are an annex, never a fourth part.
- **A readable title** — a presentation-layer heading. **Identity stays the directory slug**: a title is never a second identifier, never takes part in resolution, binding, or reference, and its absence leaves the slug as the heading.
- **Boundaries** — the exclusions the author states as out of scope. They narrow *interpretation*, never the objective, and never substitute for a Target: an exclusion is what the Anchor is not, a Target is a slice of what it is. An absent Boundaries annex records that no exclusion was stated — not that nothing is excluded.
- **Timestamps** — `created` / `updated` bookkeeping.

Two operating properties follow:

- **Measured by degree**: an Anchor is *pursued*; its verification is progress-shaped (percentage, threshold attainment, evaluator scores) — not a per-clause pass/fail.
- **Modified deliberately**: changing an Anchor is a strategic act — the change is recorded and history is preserved; silent drift is prohibited.

### Shape Rules (GD-2 / GD-3) — owner

**GD-2 — Outcome, not steps.** An Anchor's objective narrative states **where the project ends up**, never how a worker gets there. A task list, an implementation plan, and a phase sequence are all forbidden shapes: they name work, and work belongs to a deliverable's spec, plan and tasks. The executable form lives in the engine (`_reject_bad_objective`, `_reject_bad_target_statement`: tasklist / phased / composite shapes), which rejects a violating statement with exit 2. GD-2 binds the Anchor objective **and** every Target statement.

**GD-3 — Subordinate, not independent.** A decomposition candidate must be a slice of its parent objective. A candidate that would stand as a meaningful end state of its own is a separate Anchor — split it, do not nest it.

**Scope of GD-2**: it binds the Anchor only. An action-level Goal carries executable guidance and MAY be step-shaped; its owner (`shared/definitions/goal-definitions.md`) declares that difference and no GD-2 check runs on a Goal's guidance.

### Archive Layers

A definition lives in exactly one of three **archive layers** — never in a spec subdirectory:

| Layer | Definition file | Store |
|-------|-----------------|-------|
| **Anchor archive** | `anchor.md` ([[STR-001]]) | `.specify/anchoring/<anchor-slug>/anchor.md` |
| **Goal archive** | `goal.md` ([[STR-002]]) | `.specify/goals/<goal-slug>/goal.md` |
| **Team archive** | `team.md` (team side owned by `skills/internal/create-team/references/conceptual-model.md`) | `.specify/teams/<slug>/team.md` |

- **Position is not ownership.** A definition's owner is answered by the binding record below, never by the directory it sits in. `.specify/specs/` carries no definition subdirectory as a current store; a leftover spec-local tree is a migration source, not a layer.
- **The run scratch area is not an archive layer.** `.specify/.tmp/` is the timed work area owned by `shared/guidelines/temp-directory-discipline.md`; no definition ever lands there.
- **The scope value set.** The values the engine accepts for `--scope` are the **closed four members** `anchor` / `teams` / `goals` / `auto` ([[STR-004]]). `anchor`, `teams` and `goals` name the three archive rows above (not directories, which is why each member keeps its definition-file name after any directory rename); `auto` is the read-only resolver that picks the single layer containing the requested identity and exits 2 (`scope-ambiguous` / `not-found`) when that is not decidable. This list is the sole enumeration of that set: the engine's parser domain is its execution projection and its `--help` cites this section by path, and no second document enumerates it. The retired member `goal` is an **invalid value** (exit 2), not an alias — no silent fallback exists. The same holds for the historical members `global` / `spec`.
- **Creation timing is declared, not restated.** Whether a run creates an Anchor or a team, and when, is read from `shared/declarations/facts/goal-team-handoff-threshold.yaml`: a direct run creates none, a handoff run creates both after `tasks` U4, and a command run declares its own creation moment in its command template (`templates/commands/<command>.md`). This file does not carry the threshold or the timing labels.

### The Binding Record

Every Anchor, every action-level Goal and every team carries exactly one **binding record** in its YAML frontmatter under the key `binding`, with exactly three keys. This section is its **sole owner**; the Goal owner cites it by path. It is the only answer to "who owns this definition":

- **`owner`** — who created it, from the closed set `sdd-run` / `command-run` / `human`. Any other value is an input error naming the value and the set.
- **`owner_id`** — which run: a token in the state-spine `run_id` shape (grammar owner: `skills/external/sdd-loop-driver/references/state-awareness.md`; the engine validates the shape only). `owner: human` may use `owner_id: human`.
- **`origin`** — `null`, or the basename of the spec directory the definition directly came from. The migration action sets it to the direct source; a definition that was deliberately authored outside a spec carries `null`. `origin` records the direct source only — it never rebuilds a cross-definition lineage. It is also the **only** cross-reference between an action-level Goal and anything upstream: no other key may name an Anchor.

The record is **written only by the engine** (`scripts/python/goal-utils.py`); no command template, skill or driver instructs a direct edit, and a hand-edited block is reported rather than trusted. A definition without a complete record is **uninterpretable** — the engine refuses it instead of defaulting an ownership. Writability follows from the record and the archive layer, not from a prohibition text: a team definition is writable by its own owner; an Anchor definition is writable by `human` always, and by any other owner only while no team in any layer names it; an action-level Goal definition is never writable by a team, because no team can name it.

### Lifecycle

This section is the **sole owner** of the lifecycle value set and the transition discipline; both concepts share it.

| State | Meaning |
|-------|---------|
| `active` | being pursued / in effect |
| `achieved` | the end state or completion condition has been reached |
| `abandoned` | deliberately given up |

Transitions: `active` → `achieved` | `abandoned`. Both terminal states are **absorbing** for ordinary actions and **retained on disk**: never deleted, never relocated. Re-opening a terminal definition back to `active` requires the explicit `reopen` lifecycle action, is permitted only for `owner: human`, and appends a history line — it is never a side effect of another action. The **team lifecycle is a different value pair**, owned by `skills/internal/create-team/references/conceptual-model.md`; these three values MUST NOT be imposed on a team.

## Anchor Dimensions (illustrative, not a closed taxonomy)

Anchors and Requirements live on **different planes** (decided 2026-08-04): a Requirement describes what the **current project's source code or configuration** must implement (a feature); an Anchor may target **any dimension** of desired outcome that the project pursues across deliverables, including ones no Requirement could ever express. Illustrative dimensions:

| Dimension | Example anchor objective | Why it is not a Requirement |
|-----------|--------------------------|-----------------------------|
| **Framework / harness itself** | "The spec-kit framework this project uses stays continuously updated" | Its object is the toolchain, not this project's code — no FR on this repo can implement it |
| **Codebase-wide convention convergence** | "All project source code is standard-idiomatic Golang" | A cross-cutting end state pursued by degree across the whole codebase, not a per-feature clause |
| **Delivered-capability outcome** | "Feature X runs on platform Y" | An outcome about a capability in a target environment; Requirements specify the implementation, the Anchor states the environmental end state being pursued |

Boundary note: when a dimension-2-style desire is frozen into a **binding rule** enforced by gates, it belongs to the **Constitution** (a governance principle); when it binds one deliverable as a testable clause, it is a **Requirement**; when it is a desired end state pursued and measured **by degree**, it is an **Anchor**. The same sentence can move between the three homes only by deliberately changing its nature.

## Anchor vs Requirement

**Anchor** and **Requirement** are independent, parallel first-class concepts on **different planes** — **there is no necessary hierarchy between them** (decided 2026-08-04). A Requirement's object is fixed: this project's source code / configuration and the feature they implement. An Anchor's object is free: any dimension of desired outcome the project pursues across deliverables.

| Dimension | Anchor (锚点) | Requirement (需求) |
|-----------|---------------|--------------------|
| Object (作用对象) | Unrestricted — framework/harness, codebase conventions, delivered-capability outcomes, … (any dimension) | The project's source code / configuration — what feature they must implement |
| Essence | Desired end state + attainment criteria | Binding clauses on a deliverable |
| Question answered | *why / whither* — toward what, to what degree | *what / how-correct* — what MUST hold, what counts as done right |
| Home | Anchor archive: `.specify/anchoring/<anchor-slug>/anchor.md` (authored fact source) | `.specify/specs/<ID>-<slug>/requirements.md` (bound to one Feature) |
| Shape | Singular narrative + criteria per Anchor | Enumerated clauses (FR-xxx / SC-xxx) |
| Verification | By degree — progress, thresholds, evaluator scoring | Binary — per-clause pass/fail against tests and acceptance scenarios |
| Change discipline | Deliberate modification with recorded history (no silent drift) | Clarification/revision flow (Clarifications sessions, re-gated spec) |
| Failure semantics | Not yet attained → keep iterating / adjust strategy / deliberately re-scope | Not satisfied → implementation non-conforming, delivery blocked |
| Anti-pattern | Written as a task list / implementation steps | Written as an untestable aspiration |

**No structural link (decided)**: a requirements spec carries **no** Anchor field — `requirements.md` does not reference an `anchor-slug`, and an Anchor never enumerates the FRs "under" it. When work on a Feature happens to advance an Anchor, that connection surfaces **observationally** — in evaluation results, team summaries, and run reports — never as a mandatory field in either artifact. Neither concept derives from, contains, or validates the other.

**Litmus tests** (when writing a sentence, decide where it belongs):

1. **Deletion test** — deleting it loses *direction* → Anchor; loses a *contract* → Requirement.
2. **Verification test** — verifying it needs scoring/progress → Anchor criterion; needs a pass/fail check → Requirement clause.
3. **Change test** — changing it is a strategic decision with history → Anchor; a clarification + spec revision → Requirement.
4. **Subject test** — the sentence's subject is an executing subject ("the team reaches …") → Anchor; a system/deliverable ("the system MUST …") → Requirement.
5. **Object test** — it constrains what this project's source/config implements → Requirement; its object lies beyond the implementation surface (the framework itself, codebase-wide convergence, runtime/platform outcomes) → Anchor.

## Criteria Authority Boundary

Success-shaped statements exist in both worlds; their authority is disjoint (decided 2026-08-04):

- **SC-xxx** (Success Criteria in a requirements spec) serve **only their own Feature** — they measure that Feature's delivery and nothing broader.
- **Anchor success criteria** are **cross-feature** — they measure the end state regardless of which Features contributed.
- Criteria MUST NOT be copied between the two stores. Cross-feature aggregation happens at the **evaluation/summary layer** (evaluators, team summaries), with each side citing its own source — never by restating one store's criteria inside the other.

## 判据主体指代形 (Criterion Subject Reference)

一条锚点成功判据常常是对**一组同类制品**的断言(「每个绘图技能都……」)。把成员逐个打进判据文本,判据就会随目录增删而失真:本仓唯一真实的枚举型判据正是这样被反复改写的——锚点 `draw-two-layer-structure` 的 `anchor.md` 的 `## History` 里留着「六个绘图技能」与「七个绘图技能」两个前值,改的都是同一条判据。故判据 MAY 改用**指代形**,让主体集合在**解析那一刻**由仓库现状导出,而不是取自判据文本里的成员枚举:

`[subjects: <glob>]`

- **相对仓根**解析,命中集 = 各命中路径相对仓根的名字,已排序去重。
- 指代形写在判据文本内、位置不限;一条判据 MAY 含零个或一个指代形(含两个即落入下面的冲突档)。
- **纯枚举判据的解析行为完全不变**:不含指代形的判据不导出任何集合,解析器对其返回值与引入本节前逐字段一致,既有锚点定义无需迁移即可继续解析。
- 导出是**解析期的只读动作**:它读仓库现状,不写任何文件,也不改判据文本。

### 两档失败,互相可区分

导出为空**不是**通过——「零个主体全部满足」是空真,故两档都报错;而两档报的**不是同一件事**,修法相反,所以 MUST 分档而不是合并成一个「无主体」:

| 档 | 触发条件 | 报告前缀 | 通常的修法 |
|---|---|---|---|
| 路径不存在 | 字面前缀(第一个通配段之前的那段路径)在仓内不存在 | `SUBJECT MISSING:` | 多半是写错或目录已迁移——改指代形 |
| 导出集为空 | 字面前缀存在,但命中 0 条 | `SUBJECT EMPTY:` | 目录真的空了,或指代形过窄——去看目录 |

两档都使 `goal-utils.py validate` 判为不通过(退出码 `4`)。把它们分开的是**报告前缀**,不是退出码:退出码相同而前缀不同,作者据此知道该改指代形还是该去补目录。

### 冲突,与其不可机械判定的边界

一条判据同时携带指代形与**花括号展开记号**(`{a,b}` 一类)时 MUST 报 `SUBJECT CONFLICT:`——同一主体集既有导出来源又有手打副本,静默择一会让二者悄悄分叉,而分叉是不可见的。

**诚实边界**:判据里的**散文枚举**(「所有绘图技能」「draw-diagram 与其余六个」)不带任何机器可辨记号,与指代形同现时**检不出**,因为自由散文里的枚举不可机械判定。故本节的冲突规则**只**覆盖花括号展开记号这一种可判定形态,MUST NOT 被读成「枚举与指代形共存已被守卫」。散文枚举与指代形同现时,以指代形导出的集合为准,散文部分只是给人读的叙述——这不是守卫,是取舍。

### 第二个解析器的处置

`skills/internal/create-team/scripts/build-summary-input.py` 有自己的**本地**判据读取器,其 `load_goal_definition` 的注释明写:该脚本与 `scripts/python/goal-utils.py` 分属两棵镜像树(`skills/` 与 `scripts/`)且相对深度不同,跨树 import 在安装到消费项目后即断,故刻意本地解析。**处置:让它同样理解指代形**——就地做同一导出,并把指代形渲染成成员名再交给总结,使读者不会看到一个自己无从解析的裸标记;MUST NOT 靠加一个 import 来解决。**代价明示**:于是仓内并存两处导出实现,二者的一致性由 `tests/contract/test_criterion_subject.py` 对同一输入断言两侧成员一致来钉住,而不是靠人记得同步——把同步交给记忆,正是本节要消灭的失效模式。

### 退出码约定在本仓并不统一

同一份 `build-summary-input.py` 另有自己的退出码表(`EXIT_OK, EXIT_INPUT_ERROR, EXIT_NO_MATERIAL = 0, 2, 3` 与 `EXIT_SERIALIZED = 4`),其 `3` / `4` 与 `goal-utils.py` 的 `EXIT_NOT_FOUND` / `EXIT_INVALID` **语义相左**——即仓内并存第五套退出码约定。本节记录该分歧而**不**统一它(统一超出本概念文档的职权,且会改动一个已安装脚本的对外契约):读某一处退出码表 MUST NOT 被当作通吃全仓。

## Singularity Rule

One Anchor = one objective (decided 2026-08-04):

- **Per anchor definition**: an Anchor MUST NOT bundle several objectives into one composite definition — split them into separate `anchor-slug`s, each with its own directory and lifecycle.
- **Per executing subject**: a team binds to exactly **one** Anchor at a time (see Anchor–Team Binding below). A team that "pursues two anchors" is either two teams or an Anchor that needs deliberate re-scoping.
- The **project** may hold multiple `active` Anchors concurrently — each is its own `anchor-slug`, each advanced by its own team(s).
- Decomposing one objective into **Targets** (see below) does not breach singularity: Targets are slices of the same objective, never additional objectives.

## Target Decomposition (目标切片)

A **Target** is a **sub-outcome under exactly one Anchor**: an independently advanceable, completion-judgeable **scope slice** of the same end state (decided 2026-08-11; operational surface specified by requirement `038-goal-target`). Targets give the Anchor — a large, slow-moving concept — a **run-sized control point**: a team run can be pointed at one Target without touching the Anchor–Team binding, the Anchor's identity, or the summary delivery directory.

```
Anchor (authored end state)  1 ── N  Target (run-assignable scope slice)  1 ── N  runs / work items (TI-xxxx)
```

Four defining properties:

1. **An annex, never a fourth part.** The decomposition is optional: an Anchor without Targets is fully valid and behaves exactly as if the mechanism did not exist. Adding Targets changes neither the narrative, nor the criteria, nor the lifecycle.
2. **Outcome-shaped, recursively.** GD-2 applies at Target scale: each Target states a sub-**outcome** ("log component split complete"), never a step. The Target set is an **unordered set** — identity ordinals carry no execution-order semantics; an ordered target list is an implementation plan wearing an anchor's clothes.
3. **Subordinate, not independent.** GD-3 litmus at this boundary: a Target must be a slice of its parent objective. A candidate that would stand as a meaningful end state of its own is a separate Anchor — split it, do not nest it.
4. **A tree, not a graph.** A Target belongs to exactly one Anchor; 1 Anchor : N Targets; N runs : 1 Target. Cross-anchor Targets do not exist, and Targets carry no dependency edges between them.

**Identity.** Local form `T-<nnn>` — issued monotonically within the Anchor, never reused. Qualified form `<anchor-slug>.T-<nnn>`, dot-namespaced after the `<team-slug>.TI-<nnnn>` precedent and legal under the shared identity grammar (which admits `.` but not `#` or `/`). Lifecycle is exactly `open` / `done` / `dropped`; terminal Targets are retained with their state, never deleted.

**Two progress axes — never conflate.** Success criteria measure **end-state attainment** and remain the sole authority for `achieved`. Targets measure **scope coverage** (n of m slices done). All Targets complete does NOT make an Anchor achieved; criteria are never derived from Targets, and Targets never restate criteria (the criteria authority rule extends to Target statements). At the summary layer, milestones (`MS-<nnnn>`) remain criteria projections; completed Targets MAY additionally feed milestone entries under a distinct source marker — a presentation-layer concern owned by the summary mapping, not by this definition.

**Write model — authored lifecycle, derived progress.**

- *Authored*: a Target's statement and its deliberate lifecycle live inside the Anchor's definition file (a `## Targets` section in `anchor.md`; exact layout owned by the implementing feature) and are written **only via the engine's anchor actions** (`/speckit.anchor`) — the sole-authoring-entry rule. Teams and runs may **propose** Targets or completions; a human ratifies through the anchor surface (propose → ratify, as in `coordinate`).
- *Derived*: per-Target execution progress is folded from team ledgers (`items.jsonl` rows carrying a `target_ref`) at summary time and is never written back into `anchor.md`. When authored state and evidence disagree (state `open`, yet every attributed item is complete), the discrepancy is surfaced for ratification — never auto-flipped.

**Run assignment.** A team run MAY name one Target under the team's **bound** Anchor. The reference is validated — a dangling or terminal Target is reported, never silently accepted — and a run that names no Target runs against the Anchor broadly, exactly the pre-Target behavior. Work items attribute to the Target through the ledger's `target_ref`.

### Target concurrency (目标并发 — the only concurrency paragraph this file adds)

Independent **Targets** are advanced **concurrently by default**: when two or more Targets are independent — their work's write domains (file-level path sets) do not intersect and none of FR-005's other conditions binds them — they MUST be advanced concurrently; a serial advancement MUST name a reason code from the closed vocabulary owned by `shared/declarations/facts/serial-reason.yaml`, with that code's declared evidence form, and the run records the `requested` / `effective` / `effective_reason` reading (fields owned by `shared/declarations/facts/effective-concurrency.yaml`; `not_evaluated` where intervals are absent). Anchor completion stays "all Targets reached" — concurrency never relaxes it — and a failed Target leaves unrelated sibling Targets uncancelled while dependents stay blocked with a recorded reason. Anchor slices belong to the `partition-required` class, whose obligation text and condition set are owned by `shared/declarations/facts/concurrency-class.yaml` and FR-005/FR-006; this section restates neither, and it changes no part of the Anchor/Target model above (Targets still carry no dependency edges between them).

## Anchoring Archive

- **Anchoring Archive** = the whole `.specify/anchoring/` tree: the materialized "current & historical anchoring list" of the project. Terminal (`achieved` / `abandoned`) entries stay archived — never deleted.
- The definition filename inside a slug directory is `anchor.md` ([[STR-001]]). The earlier filename `goal.md` in this store is retired: it is a migration source, and a current store entry that still carries it is a defect, not an alternative layout.
- This document fixes the **location and semantics**; the rest of the file layout inside `<slug>/` (receipts, the derived summary tree) is owned by the implementing feature. `summary/` is a **derived** tree — regenerated by the summary flow, never hand-edited.

## Anchor–Team Binding

- A team references its Anchor by **one-way identity**: the team frontmatter declares **`anchor_slug`** ([[STR-003]]); the binding is **N teams : 1 Anchor**. The team side stores the identity only — never a copy of the Anchor's objective or criteria.
- **Resolution**: the named slug MUST exist as `.specify/anchoring/<anchor_slug>/anchor.md`. A slug that exists only under `.specify/goals/` MUST NOT resolve — an action-level Goal never becomes an Anchor identity, and no team may bind it.
- **Anchor–Team binding** therefore means *the reference* — which Anchor this team serves. Team evaluators measure progress against the referenced Anchor's criteria. The team's own side of this record (its binding application, its lifecycle value pair, `handoff_ref`, and the construction-crew notion) is owned by `skills/internal/create-team/references/conceptual-model.md` § The Team Definition and the Binding Model; this file cites it and does not restate it.
- **Field rename**: the retired team key `goal_slug` ([[STR-008]]) is replaced by `anchor_slug`. The rename is a structural, one-line edit; every other byte of `team.md` is preserved. The retired key MUST NOT survive in any live team definition, frontmatter or body.
- **Migration fallback**: teams created before Anchor management existed may still carry an inline goal in `team.md`; wherever an Anchor definition exists, the definition is authoritative and the inline copy is legacy.
- **Run-level Target assignment**: the binding axis stays team ↔ Anchor and stays static. The run-sized variable is the **Target**: a run may select one Target **inside the bound Anchor** — this never rebinds the team, never alters Anchor identity resolution, and never relocates the summary delivery directory. See Target Decomposition.

## Terminology Boundaries

Four terms are close enough to be confused and MUST stay distinct in every live surface (glossary, both concept owners, and the Re-Anchoring definition):

| Term | Refers to | NOT |
|------|-----------|-----|
| **Anchor** (锚点) | The persistent project-level entity defined in this file | not a run-ephemeral note; not the directory; not an action-level Goal |
| **anchoring archive** (锚点档案) | The `.specify/anchoring/` **directory** holding Anchor definitions | not the entity; not the Re-Anchoring discipline |
| **Re-Anchoring** (重新锚定) | The in-run discipline by which an agent reloads its direction anchor and the rules in force (`shared/definitions/re-anchoring-definitions.md`) | not an Anchor; not a directory; it defines no entity |
| **action-level Goal** (行动级目标) | The short-horizon executable guidance defined by `shared/definitions/goal-definitions.md`, stored under `.specify/goals/` | not an Anchor; not project-level; not a control-hierarchy member |

The bare word "anchoring" MUST NOT be used to mean an action-level Goal, and the bare word "goal" MUST NOT be used to mean an Anchor.

**Retired wording (historical record — mapped forward, never reused):**

- "Temporary Goal" / "临时 goal" → an Anchor in the anchor archive (earlier spellings: "temporary goal", "run-scoped goal"). No Anchor carries a lifetime property; the archive position is not an ownership either.
- "Global Goal" → an Anchor in `.specify/anchoring/`.
- "Temporary Team" / "临时 team" → a team in the **team archive**. The team lifecycle pair is owned by `skills/internal/create-team/references/conceptual-model.md`.
- The retired scope values `global` / `spec` / `goal` → the closed scope value set `anchor` / `teams` / `goals` / `auto` defined in § Archive Layers. There is no alias.
- The retired definition filename `goal.md` **inside `.specify/anchoring/`** → `anchor.md` ([[STR-001]]). The filename `goal.md` remains correct in the Goal archive — the two are different layers.

**Legacy state-spine keys (one-time alias, declared removal point):** `temp_goal_slug` / `temp_team_slug` / `temp_scope_spec_dir` remain readable only through the engine's migration alias (read the old key, write `anchor_slug` / `team_slug` / `origin_spec_dir`). **The alias is removed at the first minor release after 094.** A legacy key that does not resolve fails as `legacy-key-dangling` — never silently ignored, never treated as absent.

**Action signatures are not here.** The engine's actions, flags and exit codes (`scripts/python/goal-utils.py`) are owned by the engine; this document defines what the words mean and cites the engine for how to call it.

| Term | Meaning | Where defined |
|------|---------|---------------|
| **Anchor** (锚点, this document) | Project-level, long-horizon, cross-deliverable authored end state — narrative + criteria + lifecycle; the former project-level "Global Goal" | here; store `.specify/anchoring/<anchor-slug>/anchor.md` |
| **Binding record** (this document) | The three-key ownership record (`owner` / `owner_id` / `origin`) every Anchor, action-level Goal and team carries; the only answer to "who owns this definition" | here; § The Binding Record |
| **Lifecycle** (this document) | The shared `active` / `achieved` / `abandoned` value set and its transition discipline | here; § Lifecycle |
| **Archive layer** (this document) | One of the three definition stores (`anchor archive`, `goal archive`, `team archive`); the run scratch area is not one | here; § Archive Layers |
| **`--scope` value set** (this document) | The closed four members `anchor` / `teams` / `goals` / `auto` the engine accepts | here; § Archive Layers |
| **Anchoring Archive** | The `.specify/anchoring/` tree — current & historical Anchor entries, terminal ones retained | here |
| **Anchor–Team Binding** | One-way `anchor_slug` reference, N teams : 1 Anchor, identity-only | here |
| **Team Anchor** | A team's reference to the Anchor it serves | here; declared in `.specify/teams/<slug>/team.md` |
| **Re-Anchoring** | In-run reload of the direction anchor and the rules in force | `shared/definitions/re-anchoring-definitions.md` |
| **Action-level Goal** | Short-horizon executable guidance with completion conditions; parallel to SDD and Team, not a control-hierarchy member | `shared/definitions/goal-definitions.md` |
| **Requirement** | Feature-bound spec of testable clauses (FR/SC) driving plan → tasks → implement → verification | `.specify/specs/<ID>-<slug>/requirements.md`; `/speckit.requirements` |
| **Feature** | Long-lived capability entry in the feature index | `.specify/features.md` |
| **Success Criteria (SC-xxx)** | Per-feature measurable outcomes — authority limited to their Feature | requirements spec of that Feature |
| **Team** | Multi-agent structure organized around (exactly one) Anchor; its own concept side is the team owner's | `skills/internal/create-team/references/conceptual-model.md` |
| **Target** (this document) | Run-assignable sub-outcome (scope slice) under exactly one Anchor — an annex to the definition, unordered, authored via the anchor actions | here; persisted in that Anchor's `anchor.md` (`## Targets`) |
| **`target_ref`** | A ledger work item's attribution to a Target (`T-<nnn>`) | `items.jsonl` contract (`skills/internal/create-team`, summary mapping) |
| **"target" elsewhere** | `optimization_target` / `co_targets` (the artifact an iteration loop mutates), a territory entry's `target` field, the `--target` flags of the evidence/interview engines — all **unrelated** to Anchor Targets | their owning docs; glossary disambiguation |
