# Contract — Memory system and super-agent → sub-agent injection preservation

**Spec**: `requirements.md` FR-006…FR-012, FR-026 (US3) · **Plan**: `plan.md` WP03/WP12 · **Date**: 2026-11-25

The user request names two mechanisms that must survive the move: the temporary-memory system (the memory system's `session` tier) and the dynamic context injection from a super agent to a sub agent. This contract fixes "behaviorally identical except for the storage roots". The memory scope set is owned by `shared/declarations/facts/memory-types.yaml` and the dispatch contract by `shared/definitions/subagent-definitions.md`; this document references both and restates neither value domain.

## P-1 Memory engine contract (unchanged except roots)

- Scope set: exactly `{session, knowledge}` (owner: memory-types fact). No member is added, renamed, or removed.
- Actions: `record`, `recall`, `list`, `prune`, `reindex`, and `--scope all` — semantics unchanged.
- `record` still requires a `--source` of the form `/speckit.<command>` or `skill:<name>`; no new source class.
- Entry format: one Markdown file with the existing frontmatter fields; the derived index remains scan-on-demand; no shared aggregate, no lockstep index file.
- Roots move: `session` → `.specify/session/`, `knowledge` → `.specify/knowledge/`. `memory-utils.py` resolves both from the store declaration (C-6); callers MUST NOT hardcode either path (FR-006).
- `memory-recall` searches only the two memory roots. It MUST NOT traverse or return entries from any runtime store (feedback/evidence/exec-quant/trigger/retention/renumber/sanitize/housekeeping/coaching/todo/tools/migrate). This boundary is asserted by a reverse fixture: a unique token written only to the feedback and exec-quant stores is not returned by any memory recall query (FR-008/SC-003).

## P-2 Temporary-memory persistence (`run-determination`)

- The persistence adapter remains `memory-utils-session`; `run-determination.py` writes its determination record through the memory engine into the session tier's new root.
- The record schema, the settled/amend semantics and the history read (`--action history`) are unchanged.
- Acceptance reading: one completed determination persists an entry under `.specify/session/`, `memory-utils.py --action recall --scope session` finds it, and the schema keys equal the pre-move schema (FR-007/SC-002).

## P-3 Dispatch payload (unchanged field sets)

- Downlink: the seven fields `parent_identity, child_label, role_declaration, dispatch_duty, depth_position, authority_ref, return_channel` — unchanged names, order and meaning.
- Injections: the four existing injections (fast-fail clause, concurrency obligation, reporting obligation, re-anchoring) — unchanged.
- Uplink: the five-element return — unchanged.
- Memory context remains sourced only from the memory system through `memory-recall`; no other store may contribute injected "memory" (FR-010, FR-012).
- An agent template that declares `memory-recall` continues to work without changing its declaration form; only the resolved paths are new (FR-011).

## P-4 No second mechanism

- MUST NOT introduce a second context-injection mechanism, a second memory source, or a new injection store (FR-012).
- The dispatch fixture asserts the payload and the source paths; it MUST NOT assert a new payload field or a second retrieval path.

## P-5 Acceptance readings (one per SC-002/SC-003 clause)

| Reading | Command / fixture | Pass condition |
|---|---|---|
| session record → recall | `memory-utils.py --action record --scope session …` then `--action recall --query …` on a fixture workspace | entry file under `.specify/session/`, recall hits it, content equal |
| knowledge record → recall | same with `--scope knowledge` | entry under `.specify/knowledge/`, upsert-by-slug preserved |
| prune / reindex | `--action prune --scope session`, `--action reindex --scope all` | age/count bound and legacy-index retirement unchanged |
| determination persistence | `run-determination.py --action determine` on the fixture | record via memory engine under `.specify/session/`; `--action history` retrieves it |
| boundary reverse | write token T to feedback + exec-quant; recall with T | T is not returned |
| dispatch injection | dispatch fixture with a `memory-recall`-declaring child | injected refs all resolve under `.specify/session/` or `.specify/knowledge/`; seven/four/five sets present |
| no-second-mechanism | structural test over the skill/template set | no new payload field, no new retrieval source |

## P-6 Execution surface

The behavior is verified through the existing engines and the existing test entry (`scripts/bash/run-tests.sh`); no new engine, action, or storage is created. The capture is one run per reading, retained under the feature's `test-evidence/`.
