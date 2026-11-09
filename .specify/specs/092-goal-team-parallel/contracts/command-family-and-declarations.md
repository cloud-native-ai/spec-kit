# Contract — Command Family, Declaration Facts and Ownership Routing

Owner of the two declarations: `shared/declarations/facts/` (one file per fact, the path is the identity) and
`shared/declarations/contract.yaml` (value domains and registration). Owner of the class axis this contract reads:
`shared/definitions/flow-class-definitions.md` and `shared/declarations/facts/flow-class-classes.yaml`.

## 1. The command family (FR-005, FR-006)

- **C-71**: Whether a `/speckit.*` command run may own a goal/team MUST be decided by a declared class, never by a
  per-command hardcoded list. The predicate MUST be: "the command's carrier `templates/commands/<command>.md` exists
  and `flow-class-check.py --action lookup --unit-id command:<command>` exits 0 with a registered class".
- **C-72**: A command whose carrier is absent, or whose lookup exits 2 (`owner-unavailable`), MUST be treated as
  **not in the family** (A9) — never guessed, never defaulted into the family. The lookup's own exit codes are the
  only inputs; the engine MUST NOT re-implement the class table.
- **C-73**: The first evidence command MUST be `/speckit.feedback`; its carrier `templates/commands/feedback.md`
  MUST declare its goal/team creation moment (FR-040) and MUST NOT require a spec directory to exist.
- **C-74**: The family predicate MUST be consumed by the engine `goal-utils.py` (a read-only action
  `command-family --command <name>`) and by `create-team`; neither may add a second whitelist. `flow-class-check.py`
  MUST NOT be modified by this feature.
- **C-75**: A command NOT in the family MUST still be able to *read* a definition it was handed; the family decides
  creation and ownership, never readability.

## 2. Declaration fact 1 — command family

- **C-76**: The fact file `shared/declarations/facts/goal-team-command-family.yaml` MUST declare
  `fact: goal-team-command-family`, `kind: closed-set`, and a `statement` holding the command names that are
  explicitly enabled **in addition to** the class predicate. The empty statement is legal and means "class predicate
  only".
- **C-77**: The statement MUST NOT be treated as the whole family: the class predicate (C-71) is the primary
  decision and the statement is an explicit addition list. A name in the statement whose carrier does not exist MUST
  be an input error at read time.
- **C-78**: The file MUST carry the mandatory keys `fact`, `kind`, `statement`, `consumers`, `former_carriers` and
  MUST parse under the layer's YAML subset (R-06 note: it is a declaration, parsed by
  `declaration_reader.parse_subset`).

## 3. Declaration fact 2 — handoff threshold and creation timing

- **C-79**: The fact file `shared/declarations/facts/goal-team-handoff-threshold.yaml` MUST declare
  `fact: goal-team-handoff-threshold`, `kind: threshold`, and a `statement` mapping with `metric: task-count`,
  `threshold: <integer>`, and `boundary: exclusive` ("complex iff task count > threshold"; equality is simple, per
  Edge Cases).
- **C-80**: The same statement MUST carry the creation-timing pair `on_direct: none` and
  `on_handoff: after-tasks-u4`, because one decision answers both questions (T-005, FR-039).
- **C-81**: The decision action `goal-utils.py handoff-decision --tasks <path>` MUST return `direct` or `handoff`
  plus the measured task count and the declared threshold; it MUST exit 2 when the fact is unavailable
  (`owner-unavailable`) and MUST NOT fall back to a built-in number.
- **C-82**: Changing either value MUST be a one-file edit; no engine constant, driver sentence or command template
  may carry the number (FR-031). A contract test asserts the absence of the literal outside the fact file.

## 4. Registration (FR-031, Clarifications Q9)

- **C-83**: Both facts MUST be registered in `shared/declarations/contract.yaml` before any consumer reads them:
  one entry per fact under a `registered_facts:` sequence carrying `fact`, `subset_id`, `value_domain`, and
  `statement_keys`. An unregistered fact MUST read as `owner-unavailable` at the consumer, never as a default.
- **C-84**: The `subset_id` value MUST name the grammar the fact file is written in (`declaration-subset/v1` for
  both). A fact written in any other grammar MUST be refused at load.
- **C-85**: `value_domain` MUST enumerate the closed value domain the consumer validates against (`closed-set` for
  C-76, `threshold+timing-map` for C-79). The consumer MUST validate against the registered domain and MUST NOT
  hardcode a second copy.
- **C-86**: The registration MUST be additive: existing `contract.yaml` keys MUST NOT be renamed, reordered
  destructively or removed, and the file MUST keep parsing under the layer's subset grammar.
- **C-87**: Both consumption points MUST live in engines this feature creates or modifies (`goal-utils.py` actions
  C-74/C-81 and the `create-team` skill), never in `flow-class-check.py`, `run-stage.sh`, `stage-runner.sh` or any
  other pre-existing driver script.

## 5. Ownership of the concept, not the rules

- **C-88**: `shared/definitions/goal-definitions.md` MUST be rewritten to own: what a binding record means, the
  archive-layer vocabulary, the lifecycle names, and the `origin` semantics. It MUST NOT restate `goal-utils.py`'s
  action signatures (they stay owned by the engine).
- **C-89**: `skills/internal/create-team/references/conceptual-model.md` MUST be rewritten to own the team side:
  binding, `active | archived`, `handoff_ref`, and the crew notion. It MUST NOT restate the goal-side table.
- **C-90**: Neither owner may restate the other's closed value domain; each MUST cite the other by path and
  section. A cross-owner duplicate is a defect reported by the owner-rewrite contract test.

## Requirement coverage

FR-005, FR-006, FR-018, FR-024, FR-031, FR-039, FR-040; SC-006.
