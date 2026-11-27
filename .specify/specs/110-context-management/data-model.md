# Data Model — Context Management (上下文的声明、组合与只读审计)

**Spec**: `.specify/specs/110-context-management/requirements.md`
**Feature**: 110 Context Management（上下文管理）
**Status**: Phase 1 design (this file is the design record; after implementation the meanings are owned
by `shared/definitions/context-management-definitions.md` and the value domains by the four
`shared/declarations/facts/context-*.yaml` facts; nothing here may be read as an additional definition
point once the owner document exists)

All tokens below are the plan-stage design; the implementation writes them into the owner document, the
declarations and the engine, and the guards assert the three faces agree. Layout sources are
workspace-relative and use the installed (`.specify/…`) shape, which resolves on both the framework source
tree and a client project.

## E-1 — Context category (上下文类别)

The task-dependence classification of a layer.

| Field | Content | Rule |
|-------|---------|------|
| token | `invariant` or `variable` | closed set, owned by `context-categories.yaml` |
| bilingual definition site | `Invariant(不变)` / `Variable(可变)` | owner document definition site ([[STR-002]] / [[STR-003]]) |
| membership test | "would this fact change if the task changed but the environment and the project did not?" | owner document, stated once |
| derivation | the layer decides the category: `system`/`project` → `invariant`, `task` → `variable` | never a layout-row column (I-1) |

## E-2 — Context layer (上下文层级)

| Field | Content | Rule |
|-------|---------|------|
| token | `system`, `project`, `task` | closed set, owned by `context-layers.yaml`, ordered system → project → task (composition order) |
| bilingual definition site | `System(系统级)` / `Project(项目级)` / `Task(任务级)` | owner document definition site ([[STR-004]] / [[STR-005]] / [[STR-006]]) |
| definitional criterion | where the fact's owner lives: the execution environment / the project's `.specify/` workspace / the current work item | owner document |
| category | derived (E-1) | exactly one per layer |

## E-3 — Context fact class / layout row (上下文事实类)

One row of the owner document's layout table; the unit the audit checks and the manifest prints.

| Field | Content | Rule |
|-------|---------|------|
| class id | kebab-case identifier (e.g. `runtime-environment`) | unique across all layers (I-3); membership and order owned by `context-classes.yaml` (this column is that roster's projection); the per-row data is this table's own home (C-004) |
| layer | `system` / `project` / `task` | member of `context-layers.yaml` |
| form | one of the five form tokens | member of `context-forms.yaml`; legal for the layer per the matrix (I-5) |
| source(s) | workspace-relative path list, or a `runtime-discovery:<probe-id>` form plus optional constraint-owner pointers | resolves against the workspace root; the row's presence witness (E-11) |
| owner | the document or engine that owns the fact's meaning | one line; never the layout table itself |
| cap reference | `<path> § <section>` where the form is capped (`bounded-index`), or the content-bearing exception owner (`read-in-full`, `inline-digest`) | no numeric value ever (I-6) |

The table carries no category column (I-1); the category is derived from the layer.

## E-4 — Context source (上下文来源)

| Field | Content | Rule |
|-------|---------|------|
| standing form | one or more workspace-relative paths separated by `, ` | resolved against the workspace root |
| discovery form | `runtime-discovery:<probe-id>` where `<probe-id>` ∈ the engine's declared probe set (`platform`, `path-tools`, `fs-access`) | read-only, side-effect-free probe; the observed values are never printed |
| ephemeral part | the current interaction input, the current task's selection | not a standing source; never turns a row absent (PA-2) |

## E-5 — Materialization form (物化形态)

| Token | Meaning | Legal layers | Cap linkage |
|-------|---------|--------------|-------------|
| `pointer` | a path reference opened on demand; no content carried | system, project, task | — |
| `read-in-full` | a canonical pointer whose consumer complete-loads the document; zero copied bytes | project only | content-bearing exception owner: `shared/guidelines/token-efficiency.md` § 摘要优先(Summary-First) |
| `bounded-index` | per-entry path plus one-line relevance, within the cap its owner declares | project, task | cap owner path + section, cited per row (same owner) |
| `runtime-discovery` | a read-only observation at use time; never stored | system only | — |
| `inline-digest` | bounded content carried when the pointer form is unreachable | task only | content-bearing exception owner: `shared/guidelines/token-efficiency.md` § 摘要优先(Summary-First) |

The form-by-layer legality matrix is I-5; the closed set is owned by `context-forms.yaml`.

## E-6 — Layer landing cell (层级落点)

One legal (category, layer) pair.

| Cell | Definition | Carriers | Allowed forms (by reference to E-5) | Content vs pointer |
|------|------------|----------|--------------------------------------|--------------------|
| `invariant` × `system` | environment and reality facts; discovered at use time or pointed at their constraint owners; never authored, never persisted | root session's baseline rows; acting agent's use-time probes | `runtime-discovery`, `pointer` | observation or pointer only; zero content copied |
| `invariant` × `project` | facts authored or generated inside the project's `.specify/`, invariant within a task cycle | baseline rows; on dispatch, the project-layer pointers carried through the existing payload's `authority_ref` field and the child's ambient Documentation Map | `read-in-full`, `pointer`, `bounded-index` | governance baseline is a read-in-full canonical pointer with zero copied bytes; everything else pointer or bounded index |
| `variable` × `task` | the current work item's facts, selected per task and discarded at task end | task-layer rows; on dispatch, the dispatch brief plus the `task-delta` refresh at stage boundaries | `bounded-index`, `pointer`, `inline-digest` | selection by task scope and keywords; invariant sources cited by pointer only |

Forbidden combinations, named and outside every layout row: `invariant` × `task`, `variable` × `system`,
`variable` × `project`.

## E-7 — Composition trigger (组合触发)

| Field | Content | Rule |
|-------|---------|------|
| trigger id | one of the closed seven: `session-entry`, `task-entry`, `task-switch`, `pre-dispatch`, `stage-boundary`, `source-drift`, `reentry` | closed set; adding or removing is an owner revision |
| composer | the composer role (E-8) that acts at this trigger | root session for baseline-scope triggers; superagent for dispatch edges |
| scope | `baseline` or `task` (the `task-delta` refresh for `stage-boundary`) | never widens a form |
| evidence | the dispatch brief on a dispatch edge; the manifest otherwise; the re-anchoring statement for `reentry` | recorded, not inferred |

`source-drift` is an observable condition, never a poll: a recorded change to a baseline source
(constitution amendment, instructions refresh, glossary or feature-status change, git-workflow change, a
discovery contradicting a recorded project fact) triggers exactly one baseline refresh at the next
declared trigger point. No watcher, daemon or background check exists (FR-016).

## E-8 — Composer role (组合者角色)

| Role | Scope it composes | Boundary |
|------|-------------------|----------|
| root session | the invariant baseline at `session-entry`; baseline refresh at `source-drift`; re-citation at `reentry` | the relative role model is owned by `shared/definitions/superagent-definitions.md`; this table adds no role value |
| superagent | each dispatch's task layer as the dispatch brief plus the baseline pointers | the seven-field / four-injection payload stays the carrier (FR-017); no field, injection, cap, identifier or self-check item is added |
| dispatched executor | none — complete-loads the pointers it receives | MUST NOT re-gather context, inherit from sibling transcripts or compose from conversation history (FR-015) |

## E-9 — Concept-pointer slot (概念指针槽位)

The non-omittable pointer-only triple: `glossary` → `.specify/glossary.md` (registered by the glossary
protocol `shared/workflow/glossary.md`); `definitions` → the concept-definition owner documents under the
installed `shared/definitions/` tree as a bounded index; `explanations` → `.specify/skills.md` /
`.specify/tools.md` plus the project's explanation-type documentation reached through the Documentation
Map (`docs/concepts/documentation-model.md`).

| Structure (closed set) | Carrier | Pointer form |
|------------------------|---------|--------------|
| root/superagent turn | the baseline's three project-layer rows (`project-vocabulary`, `concept-definitions`, `concept-explanations`) | pointer / bounded-index |
| subagent dispatch payload with its temporary-memory package | the existing `authority_ref` pointer field + the child's ambient Documentation Map glossary row + the dispatch brief's reading list; zero new fields, injections, caps, identifiers or self-check items | pointer / bounded-index |
| memory-recall projection | the composing session's baseline rows travel with the projection by pointer; `memory-utils.py` is unchanged | pointer / bounded-index |
| recovery / re-anchoring re-entry surface | the `reentry` trigger's baseline re-citation plus the re-anchoring statement | pointer |

Absence reading: a missing or unresolvable entry reads one of the absence tokens in the manifest; a
consistency claim derived from that structure reads `Unobserved` under the evidence-state owner — never
`present`, never agreement. Each structure's slot presence is read from a named surface: the manifest's
three project-layer rows serve the root/superagent turn, the memory-recall projection and the
recovery/re-entry surface (their carrier is the composing session's baseline rows); the dispatch payload
reads through the pinned channels — the instructions Documentation Map's glossary entry and the brief's
reading list — plus the protocol-boundary assertion. The slot is member-stable.

## E-10 — Context manifest (上下文清单)

The audit reading for one layer.

| Field | Content |
|-------|---------|
| action / layer | `manifest` / the requested layer |
| roots | the resolved workspace root and layer root the reading used (workspace-relative paths only); the layer root is the audited workspace's own declaration layer — `<workspace-root>/shared/` when that framework-source layer (owner document plus the four facts) is present, else `<workspace-root>/.specify/shared/` (installed shape) — so the repository tree, a fresh init tree and a seeded fixture are each read against their own owner document and facts |
| rows | one per roster class of the layer, in roster order — the roster declared by `context-classes.yaml` is the stable row-set expectation, never the current layout rows: class id, layer, form, resolved source(s), presence token, reason (on absence), cap reference; a roster class whose layout row is missing still prints its row — its layer comes from the roster, its form / source(s) / cap fields read `—` (undeclared), its token is `not-evaluated`, and its reason names the missing layout row (FR-028) |
| counts | per-token row counts |
| source reading | one `source-reading: <digest>` line (text) / `source_reading` (JSON): a SHA-256 over the declared sources of the printed layer in row order, computed from `(class id, workspace-relative resolved path, presence token, file size or directory entry count, mtime_ns)` tuples; content bytes never enter it |

The JSON form carries the same fields with ordered keys — `action`, `layer`, `rows` (each `class`,
`layer`, `form`, `sources`, `token`, `reason`, `cap`), `counts`, `source_reading`; the text form prints
one line per row in the same order. No timestamps, no host values, no document content (I-9, I-10).

## E-11 — Presence reading (在场读数)

The manifest's row set is the roster (E-10): a roster class with no layout row is still evaluated and
reads `not-evaluated`; the layout-versus-roster mismatch itself is the `check` roster-mismatch finding,
never a reason to omit a manifest row — the two readings are separate and may co-occur.

| Token | When emitted | Owner |
|-------|--------------|-------|
| `present` | every standing source of the row resolves, is readable and non-empty; a runtime-discovery row's declared probe succeeds | defined once in the new owner document |
| `absent` | a standing source path does not exist | same owner document (defined once; no prior framework owner, A-8) |
| `unreachable` | a standing source path exists but cannot be read — a dangling symlink (entry exists, target does not resolve), or an actual type that is neither a regular file nor a directory | same owner document |
| `empty` | every standing source resolves but the row's store is empty (0-byte file, empty directory) | same owner document |
| `not-evaluated` | no standing source is available to read: the row's only source is ephemeral/use-time, the roster class has no layout row (the reason names the missing layout row), or a runtime-discovery probe failed (the reason names the probe) | same owner document |

Presence is judged by the source's actual type — a regular file by size, a directory by entry count —
using metadata only; the audit never opens a file's content. Multi-source rows report the first failing
source in the declared source order; a single failing source makes the row's token that failure's token.
Absence always carries a reason naming the source — or, for a roster class with no layout row, the
missing row; a silent omission and an invented default are both defects (FR-020).

## Seed layout (design record; the owner document owns it after implementation)

The roster membership is fixed by FR-004; the source/form/cap values below are the plan's proposed seed
that the owner document writes once. Paths are workspace-relative; the installed (`.specify/…`) shape
resolves on the framework source tree and on client projects alike.

| Class | Layer | Form | Source(s) | Owner | Cap reference |
|-------|-------|------|-----------|-------|---------------|
| `runtime-environment` | system | runtime-discovery | `runtime-discovery:platform` | engine probe (`context-audit.py`) | — |
| `available-commands` | system | runtime-discovery | `runtime-discovery:path-tools`; prefer a Tool record under `.specify/tools/` where one exists | engine probe; Tool records | — |
| `operation-permissions` | system | runtime-discovery | `runtime-discovery:fs-access` | engine probe | — |
| `reality-constraints` | system | pointer | `.specify/shared/guidelines/confirmation-gates.md`, `.specify/shared/guidelines/fast-fail.md`, `.specify/shared/guidelines/temp-directory-discipline.md`, `.specify/workflow/git.md` | each owner document | — |
| `governance-baseline` | project | read-in-full | `.specify/constitution.md`, `.specify/instructions.md` | the governance generators | `.specify/shared/guidelines/token-efficiency.md` § 摘要优先(Summary-First) |
| `project-vocabulary` | project | pointer | `.specify/glossary.md` | `shared/workflow/glossary.md` (glossary protocol) | — |
| `concept-definitions` | project | bounded-index | `.specify/shared/definitions/` | the definition owners | `.specify/shared/guidelines/token-efficiency.md` § 摘要优先(Summary-First) |
| `concept-explanations` | project | pointer | `.specify/skills.md`, `.specify/tools.md` | each guide; `docs/concepts/documentation-model.md` names the explanation type | — |
| `capability-inventories` | project | bounded-index | `.specify/skills/`, `.specify/agents/templates/`, `.specify/agents/instances/`, `.specify/tools/`, `.specify/skills.md`, `.specify/tools.md` | each owner | `.specify/shared/guidelines/token-efficiency.md` § 摘要优先(Summary-First) |
| `project-state-anchors` | project | pointer | `.specify/features.md`, `.specify/features/`, `.specify/register.md`, `.specify/workflow/git.md`, `.specify/shared/declarations/facts/runtime-store-layout.yaml` | each owner | — |
| `workspace-map` | project | pointer | `.specify/shared/definitions/framework-map.md`, `.specify/shared/guidelines/directory-governance.md` | each owner | — |
| `task-artifacts` | task | bounded-index | `.specify/specs/`, `.specify/features/` | the spec artifacts | `.specify/shared/guidelines/token-efficiency.md` § 摘要优先(Summary-First) |
| `task-capabilities` | task | bounded-index | `.specify/skills/`, `.specify/agents/templates/` | each owner | `.specify/shared/guidelines/token-efficiency.md` § 摘要优先(Summary-First) |
| `task-shared-docs` | task | bounded-index | `.specify/shared/` | the shared owners | `.specify/shared/guidelines/token-efficiency.md` § 摘要优先(Summary-First) |
| `task-docs` | task | bounded-index | `docs/` | the documentation space | `.specify/shared/guidelines/token-efficiency.md` § 摘要优先(Summary-First) |
| `task-memory` | task | bounded-index | `.specify/session/`, `.specify/knowledge/` | `scripts/python/memory-utils.py` | `.specify/shared/guidelines/token-efficiency.md` § 摘要优先(Summary-First) |
| `task-statement` | task | inline-digest | `.specify/shared/workflow/user-input-protocol.md` (standing owner) + the ephemeral interaction input | `.specify/shared/workflow/user-input-protocol.md` | `.specify/shared/guidelines/token-efficiency.md` § 摘要优先(Summary-First) |
| `task-delta` | task | inline-digest | `.specify/register.md`, `.specify/state/` (standing witnesses) + the ephemeral delta records | each owner | `.specify/shared/guidelines/token-efficiency.md` § 摘要优先(Summary-First) |

## Cross-entity invariants

- **I-1 — Category is derived, never a column**: the layout table carries no category column; each row's category is the layer's derived category (E-1, E-6).
- **I-2 — Every layer is non-empty and ordered**: the layout carries at least one row per declared layer, and rows appear in the layer order `system → project → task`, each layer's rows in the roster order declared by `context-classes.yaml`.
- **I-3 — Class ids are unique**: no class id appears twice across the layout.
- **I-4 — Token domains are closed**: every layer and form token in the table is a member of its declaration; an unknown or missing **declaration** member is refused with exit `2`, while a layout-table token outside its domain is the `unknown-layer` / `unknown-form` finding (exit `1`) — never defaulted in either case.
- **I-5 — Form legality holds per layer**: system rows use `runtime-discovery` or `pointer`; project rows use `read-in-full`, `pointer` or `bounded-index`; task rows use `bounded-index`, `pointer` or `inline-digest`; any other combination is a finding.
- **I-6 — Caps are references, never values**: every `bounded-index` row names a cap owner path plus section; every content-bearing row (`read-in-full`, `inline-digest`) names the same section as its exception owner; the feature's artifacts carry no numeric cap.
- **I-7 — Read-in-full is project-bound and zero-copy**: only project rows use `read-in-full`, and the governance baseline is a canonical pointer with zero copied bytes.
- **I-8 — No invariant content in the task layer**: a task row touching an invariant source cites it by `pointer`; it never carries the source's text, its read-in-full form or an inline digest of it.
- **I-9 — Presence tokens are honest**: every row reports `present` or exactly one of the four absence tokens with a reason; no row is silently omitted and no absent source is filled with a default.
- **I-10 — Determinism**: two runs over an unchanged tree are byte-identical; rows print in roster order; no timestamps or discovered host values enter the output.
- **I-11 — Read-only containment**: no audit action writes a file, creates a cache or opens a network socket; only paths, metadata and presence states are consumed.
- **I-12 — Concept-pointer triple**: the three project-layer rows exist in the layout; their absence reads an absence token and a derived consistency claim reads `Unobserved`, never agreement.
- **I-13 — Exit-code discipline**: `check` exits `0` clean / `1` findings / `2` usage, unreadable input or an unknown/missing declaration member; `manifest` exits `0` whenever a manifest is emitted (absence rows included) and `2` on usage or declaration failure.
- **I-14 — No persistence**: compositions and manifests are ephemeral; the only durable artifacts are the owner document, the four facts, the engine, the guards and the ambient section.