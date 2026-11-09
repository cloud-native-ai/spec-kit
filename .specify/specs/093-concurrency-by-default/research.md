# Research — 093-concurrency-by-default (Phase 0)

**Purpose**: turn the spec's assumptions into measured facts before any design artifact is written. Every section
below carries the reading it rests on; the command that produced it is named so a later reader re-measures instead
of inheriting a number. **Inputs read** (summary-first): `requirements.md`; `.specify/memory/constitution.md`;
`shared/declarations/contract.yaml` + `shared/declarations/facts/`; `shared/definitions/subagent-definitions.md`;
`shared/definitions/goal-definitions.md`; `skills/external/sdd-loop-driver/{SKILL.md,references/decomposition-model.md,templates/stage-team-preset.md,scripts/wp-gate.py}`; `skills/internal/create-team/**`; `agents/**`;
`.specify/memory/features/093.md`; `specs/092-goal-team-parallel/notes/execution-lessons-2026-11-09.md`; the
design brief at `.specify/.tmp/sdd-loop/tmp/concurrency-by-default/design.md` (read from the main tree — the file
lives outside the worktree by construction, so it was read where it sits and nothing was written there).

All measurements below are dated **2026-11-09** on this worktree (`093-clarify`, branch
`093-concurrency-by-default`, base `1150f31e`). A number that could not be measured is written as
`not_evaluated`, never as zero or an estimate.

## R-1 — The declaration layer's real read surface (registration vs file existence)

Measured:
- `python3 .specify/scripts/python/declaration_reader.py --action list --repo .` → JSON with three top-level keys:
  `contract` (nine keys straight out of `shared/declarations/contract.yaml`: `completeness_states`,
  `exclusion_reasons`, `exit_codes`, `fact_kinds`, `gate_call_sites`, `required_exclusion_keys`,
  `required_fact_keys`, `schema`, `yaml_subset`), `exclusions` (entries from `shared/declarations/exclusions/`), and
  `facts` (**23** entries, each `{path, stem, body}` from `shared/declarations/facts/*.yaml`).
- `--action get --fact success-criterion-path-values` → exit `0`, full body.
- `--action get --fact concurrency-class` → exit `1`, `no declaration for fact 'concurrency-class'`.

**Ruling**: SC-009's "registration" is a **read behaviour**: a slug is registered when `--action get` resolves it
and it appears in `--action list`'s `facts` array. Deleting the file and hiding the slug from the list are the same
failure to a consumer, so the contract clause states the consumer-visible form, and the mutation test mutates the
read result (a renamed file, or a `fact:` key that no longer matches the stem), never the file's presence alone.

**Consequence for planning**: the six facts must be probed *after* writing and *before* the tests are declared
green; a fact written in the wrong YAML subset silently disappears from the list rather than erroring, so
`test_concurrency_declarations.py` compares the list against the directory listing (V-3 in `data-model.md`).

## R-2 — The YAML subset the facts must live in

Measured: `contract.yaml` declares `schema: harness-declarations/v1` and `yaml_subset: block-subset/v1`, and
`required_fact_keys` fixes the mandatory key set (with `note` the only optional key). The 23 existing facts all use
block mappings, block sequences and scalars only — no flow collections, no anchors, no aliases, no tags, no
multiple documents, no block scalars.

**Ruling**: all six new facts stay inside that subset. A nested list of mappings (needed for the class table and
the reason-code table) is expressible as block sequences of block mappings — the `arc-verdict-mapping.yaml` fact
already does exactly this with `statement: {mapping}` of scalars.

## R-3 — Slot cap: four restatements, no single owner

Measured (`grep -n "slot_cap_ceiling\|slot-cap-ceiling"` over `skills/`, `.specify/skills/`, `scripts/`, `shared/`):

| Restatement | Where | Value |
|---|---|---|
| preset ceiling | `skills/external/sdd-loop-driver/templates/stage-team-preset.md` (and its `.specify/` mirror) line 49 | `min(6, the line's remaining concurrency allowance owned by Feature 064)` |
| preset default | same file, `slot_cap_default: 6` | `6` |
| gate default + enforcement | `skills/external/sdd-loop-driver/scripts/wp-gate.py` line 1865 | `--slot-cap-ceiling` default `4`; `WG-16` checks `1 <= slot_cap <= ceiling` |
| temporary-team mode | `skills/external/sdd-loop-driver/references/decomposition-model.md` § 22 (line 365) | `min(effective_concurrency, 24)`, with `min(4, line remaining)` "unchanged for all other runs" |
| default map | `concurrency-slot-and-reserve.yaml` + `decomposition-model.md` § 20.1 | `decomposition_slot_cap` default `6` |

**Ruling** (carried as T-001): the *value* moves to `concurrency-slot-and-reserve.yaml`; the *ceiling* stays owned
by `wp-gate.py --slot-cap-ceiling` because it is an enforced runtime bound, not a configuration; the three prose
sites become projections that name those two owners. `decomposition_slot_cap` (already a state-spine key, 093's
own spine carries it) is declared a **projection** of the fact, not a fourth owner.

## R-4 — Agent definitions carry no dispatch tool, and 14 of 17 forbid dispatching in prose

Measured over `agents/*.md` (17 files): `capability-tools` values split 9 × `[Read, Grep, Glob, Bash]`,
7 × `[…, Write, Edit]`, 1 × `[Read, Grep, Glob, Write]`. None lists a dispatch tool. `grep -c "Never dispatch
another agent"` → `1` in 14 files; `0` in `reporter.agent.md`, `skill-verifier.agent.md`,
`structure-adjuster.agent.md`.

Also measured: the same sentence appears verbatim in `agents/sdd-plan-coordinator.agent.md` — the very definition
this planning stage was executed under — while 092's plan declared six concurrent packages. The static capability
field and the prose ban agree with each other and disagree with the 092 run record.

**Ruling**: this is F-093-003 and it is **not** adjudicated here. The single adjudication lives in
`shared/declarations/facts/coordinator-dispatch-verdict.yaml` ([[STR-011]]), whose `statement.verdict` takes one of
`allow` / `forbid`; T-004 records why the plan refuses to choose.

## R-5 — `capability-tools` is an existing neutral metadata key with a consumer surface

Measured: `src/specify_cli/__init__.py` declares it (`"capability-tools": ("str-list", [], True)` at the schema
table and per-tool emitters at four sites), and eight contract modules assert on it
(`test_agent_render.py`, `test_roster_reporter_seat.py`, `test_render_trigger_cli.py`, `test_role_templates.py`,
`test_project_custom_template.py`, `test_reporting_obligations.py`, `test_agent_chain_guards.py`,
`test_shipped_agent_presets.py`, `test_neutral_metadata_schema.py`, `test_agent_dispatch_mechanism.py`).

**Ruling**: FR-022's judgement reads the **existing** key; no new frontmatter key is introduced, and the eight
modules above are read-only inputs to `P3` (none may be weakened — that would be symptom suppression,
Constitution VI).

## R-6 — Enumeration roots: measured members

| Root | Members measured | Notes |
|---|---|---|
| `skills/internal/<name>/` | 38 | every directory carries `SKILL.md` |
| `skills/external/<name>/` | 16 | same |
| `templates/commands/<stem>.md` | 29 | fan out to per-tool copies (29 in `.claude/commands`, 29 in `.qoder/commands`) |
| `agents/*.md` | 17 | `.specify/agents/templates/` holds 17, name-identical |
| `.specify/teams/<slug>/` | 12 | 10 carry `territory`, 2 do not (EP-007) |
| `.specify/anchoring/<slug>/` | 6 | anchoring entries (the former `.specify/goal/` tree, renamed by 090 and merged 2026-11-09); the spec-local `/.specify/specs/<id>/goal/<slug>/` layer is a 085 projection and is **not** a root |

**Ruling**: the class mapping is a function of root + produced shape; the counts are recorded here as a dated
measurement and MUST NOT be frozen into a fact as constants (a fact carrying `38` would go stale on the next skill
added). Fact `executor-enumeration-roots.yaml` carries the five root *patterns*, never the counts.

## R-7 — Existing concurrency vocabulary occupancy is near-zero

Measured: of 29 command templates, exactly **1** (`templates/commands/sanitize.md`) matches `并行|concurren|串行`;
of 54 skills, **11** match (`create-team`, `manage-constitution`, `manage-history`, `run-agent`, `run-team`,
`sanitize-materials`, `git-utils`, `sdd-loop-driver`, plus three whose hits are incidental). Repository-wide grep
for the seven new slug literals outside `specs/093-*` and `memory/features/093*` returns one unrelated hit
(`specs/085-…/tasks.md` uses the prose words).

**Ruling**: this feature adds obligation on a **blank surface**. It therefore cannot claim credit for "fixing"
existing wording, and SC-010's per-entry disposal is unavoidable rather than optional — the disposal table records
*what each related feature asserted*, not "we changed a sentence".

## R-8 — Work Package substrate this feature reuses rather than rebuilds

Measured from `decomposition-model.md`: deterministic id assignment (layer + lexicographic tie-break, § 2),
`plan_hash` replay (§ 4), retry/split with split depth one (§ 5), attempt-scoped evidence files (§ 6), readiness
from a recorded `verdict=pass` (§ 13.1), the slot cap and the serial fallback on a non-parallel host (§ 13.2),
settlement + independent verifier + failure isolation (§ 13.3), re-entry that never redispatches a completed
package (§ 13.5), declared-order integration (§ 16), and per-stage decomposition decision (§ 20.4).

**Ruling**: FR-010…FR-020 are already **implemented** for `plan` / `implement` / `review`. The gap the spec names
is coverage and ownership, not capability: FR-029's per-stage coverage (`requirements` / `tasks` default `off`) and
FR-014's owner collapse are the actual deltas. The plan therefore writes contracts that *cite* these sections and
change only what FR-033 disposition requires.

## R-9 — The two traps this pipeline already hit, re-measured

1. **`id-contiguous` rejects letter-suffixed ids** — the clarify session folded four rows to keep FR ids dense and
   renumbered the tail (36 → 33). This plan's clause ids `C-001…C-092` are therefore allocated in a single dense
   pass with no subdivision suffixes.
2. **`overlap-check.py --repo <worktree>` relativizes the spec dir to `..`-prefixed paths**, so every declared path
   is filtered by `startswith(spec_rel)` and the engine answers "no declaration artifact" → vacuous `clear`
   (F-093-002). The plan's adjudication therefore runs the engine against the **main repository root** (where the
   spec dir relativizes cleanly) and, independently, adjudicates the declared surface by reading the other
   features' `feature-ref.md` and git history — never relying on the vacuous verdict.

## R-10 — What "real run" evidence can honestly be produced here

Measured: this planning stage ran in one agent with `Read, Grep, Glob, Bash, Write, Edit` — no dispatch tool.
Spec Assumption A4 anticipates exactly this and FR-033 requires the record `mechanism-not-yet-landed`
([[STR-010]]).

**Ruling**: SC-006 stays `not_evaluated` with the carrier named (a later real run), and the plan states it in
§ Concurrency plan for this run. The 092 run record remains the *reproduction* case, never the proof.

## R-11 — Published-vs-projected text: what the `.specify/` tree may and may not carry

Measured: `sync-mirrors.py --check` → exit `0`, zero drift on six pairs (`templates/` 22, `skills/external/` 417,
`skills/internal/` 139, `agents/` 17, `scripts/` 121, `shared/` 98; five projected pairs ok; per-tool copies ok) —
recorded in `test-evidence/mirror-baseline-plan.txt`. `shared/declarations/` was created in the framework source
(`shared/`) and reaches `.specify/shared/` through the mirror, so facts are authored once.

**Ruling**: every fact and every owner rewrite lands in the framework source only; the `.specify/` copy is
regenerated. A hand edit to `.specify/shared/` would be severed on the next mirror run (Constitution XI).

## R-12 — Template neutrality constraint on the command surfaces

Measured: `templates/commands/*.md` are shipped to every downstream project; three of them (`plan`, `tasks`,
`implement`) already reference the decomposition layer by name.

**Ruling**: the command-surface change names the **fact slugs and the clause ids**, never this repository's
paths. `templates/` therefore gains obligation text but zero repo-specific path facts (Constitution XIV + the
template-neutrality rule).

## R-13 — The three loop executors advance on three different grains

Measured: `sdd-loop-driver` advances by stage and Work Package (`decomposition-model.md` § 13, § 20); the
`sdd-house-keeping` skill's subject is **record entries** under a retention policy (`record-retention.py`,
`shared/guidelines/…` retention thresholds) — there is no "round"; `sdd-project-setup` advances by **setup
steps** with dependency edges between some of them.

**Ruling** (spec FR-028 already requires it, this is the measurement behind it): the record surface is the
**advancing unit**, not a round. A "per-round" record makes two of the three executors unable to book anything,
which is how "no rounds" silently becomes "no record".

## R-14 — Reproduction shape for the 092 defect (the red-first fixture)

Measured from the 092 record and this run: six declared packages, one coordinator, no dispatch tool, no
per-package verdict pointers, no interval overlap. The static half is fully checkable without any live dispatch
(declaration without capability and without a declared handoff), and the record half is checkable from a ledger
whose dispatch events all name the same `executor_id` with no overlapping intervals.

**Ruling**: `test_concurrency_reproduction_092.py` asserts both halves; the first must be red on today's tree and
green after `P1`+`P3`, and the second is a pure function over a synthetic ledger. No live dispatch is needed, so
the fixture is deterministic and can run in CI.

## Decisions taken in this phase (pointing at the plan, not restating it)

| Decision | Record |
|---|---|
| Slot cap / ceiling ownership collapse | plan § Decision Tensions T-001 |
| Effective concurrency = maximum interval overlap | T-002 |
| File-level write domains | T-003 |
| No self-adjudication of the coordinator verdict | T-004 |
| Declaration layer carries the five judgement faces | T-005 |
| Registration is a read behaviour | this file R-1, contract `C-009`…`C-012` |
| Enumeration roots carry patterns, never counts | this file R-6, contract `C-005` |
| Real-run evidence deferred with a named carrier | this file R-10, contract `C-088` |

## Re-measure list for `/speckit.tasks` (numbers that will move)

1. Member counts of the five enumeration roots (R-6) — re-run the enumeration, never inherit the numbers above.
2. The 23-entry `facts` array (R-1) — after the six new facts land it is 29; a mismatch means a fact fell outside
   the YAML subset.
3. The 9/7/1 split of `capability-tools` (R-4) — `P3` changes at most the coordinator definitions, and only if the
   verdict says `allow`.
4. Mirror pair file counts (R-11) — `shared/` grows by six facts; every other pair must be unchanged in file count.
5. The serial failing-name baseline — capture at implement entry, compare by name (R-9, 092 lesson 3).
