# Contract — Distribution and Entry Points

**Feature**: 109 Prompt Adherence Evaluation（提示遵从度评价）— Spec Kit port of the closed ai-harness spec 092
**Status**: design contract. Mirror pairs: the `MIRROR_PAIRS` declaration in
`scripts/python/sync-mirrors.py`; init copy: `src/specify_cli/__init__.py`; baseline channel:
`shared/workflow/feedback-step.md`.

## C-033 — Distribution rides publish → install → init

**Statement**: all artifacts are framework sources that ride the existing flow: the owner document under
`shared/definitions/`, the five facts under `shared/declarations/facts/`, the engine under
`scripts/python/`, projected by `sync-mirrors.py` `MIRROR_PAIRS` (`shared → .specify/shared`,
`scripts → .specify/scripts`) and copied into client projects by `specify init` (which installs the
`shared/` and `scripts/` trees). Mirrors are generated, never hand-edited. The framework map
(`shared/definitions/framework-map.md`) gains two rows — one for the owner document, one for the reading
entry — and a fresh init fixture contains every artifact. This feature introduces no new managed runtime
store, so it adds no `.specify/.gitignore` rule and no `runtime-store-layout.yaml` change. Tests and
fixtures are repo-internal development assets and do not ship.
**Red when**: a mirror differs from its source; a fresh init fixture lacks one of the artifacts; the
framework-map rows are missing or unresolvable; a new ignore rule or store-layout registration appears.
**Test carrier**: `tests/integration/test_prompt_adherence_init.py`;
`scripts/python/sync-mirrors.py --check` reports no NEW drift on the touched pairs;
`tests/contract/test_prompt_adherence_owner.py` (framework-map row leg).

**Serves**: (FR-020, FR-023)

## C-035 — Baseline reading lands through an existing channel

**Statement**: the feature line produces one dated baseline reading of this repository through an
existing channel — one feedback entry written by `feedback-utils.py --action record` under the
implementing stage's unit and run, carrying the reading's status, per-row states, the declaration-set
digest and source references. The entry is an ordinary feedback record; it creates no aggregate, no new
store and no query surface, and it is replayable by one engine run against its cited references.
**Red when**: the baseline lands in a new store or an aggregate; its source references are missing; it
is not replayable; it claims improvement without comparable before/after evidence.
**Test carrier**: `tests/contract/test_prompt_adherence_engine.py` (audit-replay leg over the recorded
baseline) + the baseline entry itself (dated record cited by the implementation's `verification.md`).

**Serves**: (FR-008, FR-026)

## C-037 — No new ambient instructions section, no new command

**Statement**: this version adds no ambient instructions section — the mechanism carries no per-session
agent obligation; discovery is the framework-map row plus the owner document's § Entry. No `/speckit.*`
command, skill wrapper, scheduled job or dashboard ships. A wrapper is a separate future decision.
**Red when**: `templates/instructions-template.md` or `.specify/instructions.md` gains a section for this
feature; a command or skill surface ships.
**Test carrier**: the full suite stays green (no instructions-section count moves);
`tests/integration/test_prompt_adherence_init.py` asserts the artifact inventory only.

**Serves**: (FR-023)