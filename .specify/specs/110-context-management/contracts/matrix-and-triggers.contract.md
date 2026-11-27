# Contract — Composition Protocol, Triggers, Composer Roles and the Dispatch Mapping

**Feature**: 110 Context Management（上下文管理）(spec 110)
**Status**: design contract. Payload owner: `shared/definitions/superagent-definitions.md` § The super↔sub
Protocol; re-anchoring owner: `shared/definitions/re-anchoring-definitions.md`; user-input owner:
`shared/workflow/user-input-protocol.md`.

## C-020 — Baseline composition happens once per session or line

**Statement**: at `session-entry` the root session composes the invariant baseline once — the system and
project layers with their declared forms — reads the governance documents in full from their canonical
paths, performs the system-layer discoveries, and keeps the composed baseline for the session. A task
change never triggers a baseline recomposition; only a declared baseline-refresh trigger does. Session =
one agent session's context-window lifetime (a compaction or re-entry does not create a new session; it
goes through `reentry`); line = the continuous stage series under one state spine (a cross-stage commit is
still the same line).
**Red when**: a task switch recomposes the baseline; the governance baseline is carried as copied content;
a session composes the baseline more than once without a refresh trigger.
**Test carrier**: `tests/contract/test_context_management_owner.py` (protocol legs);
the fixture legs of `tests/contract/test_context_management_engine.py` (source-digest change under
`source-drift`).

**Serves**: (FR-006, FR-007, FR-012)

## C-021 — Task composition selects per task, under the owned caps, without widening a form

**Statement**: at `task-entry`, `task-switch` and `pre-dispatch` the composer selects the task layer for
that task: artifacts in scope, task-relevant skills and commands, task-relevant shared-docs and docs
indexes, the memory selection, the distilled `[task]` and the delta facts. Each selection cites invariant
sources by pointer and stays within the cap its owner declares; a pointer row is never opened wholesale
into a payload; switching tasks recomposes the task layer only.
**Red when**: a task selection restates invariant content; a pointer row is expanded into a payload; a
selection exceeds its owner's cap; a task switch touches the baseline.
**Test carrier**: `tests/contract/test_context_management_owner.py` (protocol legs);
`tests/contract/test_context_management_engine.py` (cap-reference legs).

**Serves**: (FR-007, FR-008, FR-013)

## C-022 — The trigger set is closed at seven, each with composer, scope and evidence

**Statement**: the owner document declares exactly these triggers, each naming its composer, its scope and
its evidence: `session-entry` (root session; compose baseline; the manifest or the session's composition
record), `task-entry` (the composer of the current work; compose the task layer; the manifest's task
rows), `task-switch` (the composer of the current work; recompose the task layer only; the manifest's task rows),
`pre-dispatch` (superagent; compose the per-dispatch
task layer plus the baseline pointers; the dispatch brief), `stage-boundary` (the composer of the current
work; refresh `task-delta`; the manifest's task rows), `source-drift` (root session; recompose the baseline
exactly once; the manifest's source reading), and `reentry` (a resumed session acting in the root-session
role after a compaction, a handoff or a stall re-read; re-cite
the baseline by pointer, refresh `task-delta`, record the re-anchoring statement as evidence). Adding or
removing a trigger is an owner revision.
**Red when**: a trigger outside the seven fires; a trigger names no composer, scope or evidence; the
`reentry` semantics drift from C-028.
**Test carrier**: `tests/contract/test_context_management_owner.py` (trigger-set legs).

**Serves**: (FR-014)

## C-023 — Composer roles resolve through the existing relative role model

**Statement**: the root session composes the baseline; the superagent composes each dispatch's task layer
as the dispatch brief plus the baseline pointers; the composer of the current work — whichever existing
role holds the work item — selects or refreshes the task layer at `task-entry`, `task-switch` and
`stage-boundary`, a holder resolution rather than a new role value; a dispatched executor complete-loads
the pointers it receives and MUST NOT re-gather context, inherit from sibling transcripts or compose from
conversation history. The role model is owned by `shared/definitions/superagent-definitions.md`; this
contract adds no role value, no depth rule and no grant.
**Red when**: a composer role outside the model appears; a dispatched executor re-gathers context; a
second role enumeration is introduced.
**Test carrier**: `tests/contract/test_context_management_owner.py` (role-legs).

**Serves**: (FR-015)

## C-024 — Source drift is an observed record change, never a poll

**Statement**: a change to a recorded baseline source — a constitution amendment, an instructions refresh,
a glossary or feature-status change, a git-workflow change, or a discovery that contradicts a recorded
project fact — triggers exactly one baseline refresh at the next declared trigger point. The mechanism
adds no watcher, daemon or background check; the evidence is the changed record already kept by the
project plus the manifest's source reading (a deterministic digest over declared sources' metadata, never
their content).
**Red when**: a refresh runs on a timer or a poll; one change causes two refreshes; a recorded change
triggers none.
**Test carrier**: `tests/contract/test_context_management_engine.py` (source-reading fixture legs);
`tests/contract/test_context_management_owner.py` (drift-definition legs).

**Serves**: (FR-016)

## C-025 — On dispatch edges the existing payload remains the carrier

**Statement**: on a dispatch edge the task layer travels in the existing payload: the seven role fields
(`parent_identity`, `child_label`, `role_declaration`, `dispatch_duty`, `depth_position`, `authority_ref`,
`return_channel`), the four pre-existing injections (fast-fail clause, concurrency obligation, reporting
duty, re-anchoring anchor digest) and the uplink return, all owned by
`shared/definitions/superagent-definitions.md` § The super↔sub Protocol and cited, never restated. The
owner document states this mapping by pointer only and changes no field, no injection, no cap and no
payload rule; it adds no identifier or self-check item. Outside dispatch, the same layers compose through
the same declared rows without the payload.
**Red when**: a new role field, injection, cap, identifier or self-check item appears; a payload rule is
restated; the mapping is implemented as a second payload channel.
**Test carrier**: `tests/contract/test_context_management_owner.py` (mapping legs; package-boundary leg in
C-042).

**Serves**: (FR-005, FR-017, FR-028)

## C-026 — The concept-pointer slot maps onto existing channels per structure

**Statement**: the owner document declares, for each structure of the closed set, the slot's carrier and
pointer form: on a root/superagent turn, the baseline's three project-layer rows; on a dispatch payload,
the existing `authority_ref` pointer field plus the child's ambient Documentation Map glossary row plus
the dispatch brief's reading list; on a memory-recall projection, the composing session's baseline rows
travelling with the projection by pointer while `memory-utils.py` stays unchanged; on a
recovery/re-anchoring re-entry surface, the `reentry` trigger's baseline re-citation plus the re-anchoring
statement. Each carrier resolves to a named presence surface the mechanism can read: the manifest's three
project-layer rows for the turn, the memory projection and the re-entry surface (one reading serves all
three), and the pinned dispatch channels — the Documentation Map glossary entry and the brief's reading
list — for a dispatch payload.
**Red when**: a structure lacks a declared carrier or a named presence surface; a carrier grows a new
field or output; a structure claims presence without the baseline or the pinned channels.
**Test carrier**: `tests/contract/test_context_management_owner.py` (structure legs);
`tests/contract/test_context_management_engine.py` (concept-row presence legs).

**Serves**: (FR-028)

## C-027 — Invariant content is never restated in the variable layer

**Statement**: a task-layer row that concerns an invariant source cites it by `pointer`; it carries none of
its text, its read-in-full form or an inline digest of it. The audit reports the duplication where the row
shape makes it decidable — exactly two shapes: a task row using `read-in-full` over a source an invariant
row declares, and a task row using `inline-digest` over a source an invariant row materializes as
`read-in-full`; the remaining cases are reported by review against this clause.
**Red when**: a task row carries invariant content; the same source is cited at two layers in a
content-bearing form; the audit silently passes a decidable duplication.
**Test carrier**: `tests/contract/test_context_management_engine.py` (decidable-shape legs);
review of the owner document's protocol section.

**Serves**: (FR-008, FR-010)

## C-028 — Reentry re-cites, refreshes only the delta, and records its statement

**Statement**: a session resuming after a compaction, a handoff or a stall re-read re-establishes its
context through the `reentry` trigger: it re-cites the baseline by pointer, recomposes the baseline only
when a baseline-refresh trigger also fired, refreshes `task-delta`, and records the re-anchoring statement
as its evidence. The re-anchoring tiers are owned by `shared/definitions/re-anchoring-definitions.md` and
are referenced, never restated.
**Red when**: reentry recomposes the baseline without a refresh trigger; reentry skips the delta refresh;
the re-anchoring statement is not recorded.
**Test carrier**: `tests/contract/test_context_management_owner.py` (reentry legs).

**Serves**: (FR-014)

## C-029 — No composition is persisted

**Statement**: a composition is ephemeral and dies with its work item; the mechanism creates no store,
cache, index, rendered context artifact or database and changes no existing store's schema. The only
durable artifacts this feature adds are the owner document, the four declaration facts (plus their four
registration keys), the audit engine, the guards and fixtures, the ambient instructions section and the
three framework-map rows.
**Red when**: a composition or manifest is written to disk; a cache or index appears; an existing store's
schema changes.
**Test carrier**: `tests/contract/test_context_management_readonly.py` (zero-write legs);
`tests/contract/test_context_management_owner.py` (red-line legs).

**Serves**: (FR-011)