# Research: 074-goal-team-sdd-unification

**Requirement → Feature**: `074-goal-team-sdd-unification` → Feature 074 Goal/Team/Agent 与 SDD 开发流程统一

Phase 0 rulings R1–R14. Each ruling states the decision, the measured evidence it rests on
(command output or file:line), and the alternatives rejected. Nothing here restates a fact
owned elsewhere: the input domains, verdict table, precedence, and reason codes are owned by
`shared/definitions/sdd-routing-definitions.md` (created by this feature's implementation);
this file records only *why* the design around that owner has the shape it has.

**Phase 0 evidence path (degraded, disclosed)**: this environment exposes no subagent
dispatch capability and the stage brief forbids dispatching subagents, so the codebase
exploration pass ran as a bounded manual probe (grep for headings/symbols + targeted excerpt
reads under the token-efficiency discipline) rather than as an Explore-subagent pass. Every
ruling below therefore carries a re-runnable command or a `file:line` anchor instead of a
subagent digest.

---

## R1 — The routing decision is one new stdlib-only engine, not a prompt rule and not a data file

**Decision**: create `scripts/python/sdd-route.py`, a read-only, stdlib-only engine with three
actions — `route` (classify one declared change), `authorize` (resolve effective
authorization for a recipient), `golden` (judge the owner document's golden case table). The
verb table, input value domains, precedence, and the reason-code vocabulary live in the owner
document `shared/definitions/sdd-routing-definitions.md`; the engine parses that document and
never carries a second copy of those tables.

**Evidence**:
- Precedent for the shape: `scripts/python/flow-class-check.py` (29 engine files under
  `scripts/python/`, measured `ls scripts/python/*.py | wc -l`) — an owner document holding
  the criteria plus a read-only engine exposing `check` / `lookup` with a documented exit
  alphabet. Feature 069/069b established exactly this split for a classification axis, and
  `shared/definitions/flow-class-definitions.md` opens with the owner declaration this
  feature's owner document must also carry.
- SC-002 demands a checked-in golden table judged row by row and idempotence over repeated
  evaluation. That is not decidable from prose: a prompt-level rule cannot be run twice and
  compared, so FR-007's "returns the same verdict for the same inputs" would be unprovable.
- OSoT (Constitution XIV): a golden table in a separate data file would be a second copy of
  the verdict table. The table therefore lives in the owner document and the engine and the
  unit tests both reach it there — one table, one place.

**Rejected**: (a) the rule as prose only in the owner document — fails SC-002's determinism
and idempotence assertions; (b) two engines, one for routing and one for authorization — the
two predicates share one owner document and one failure vocabulary, and splitting them would
create the "second mechanism" FR-018 forbids in spirit; (c) a YAML/JSON data table beside the
owner document — a duplicate of the verdict table, stale-in-waiting.

## R2 — Authorization reads the Agent half through the CLI's neutral key set and parses the seat half itself

**Decision**: the agent half of the AND resolves through the existing neutral metadata
contract (`NEUTRAL_AGENT_METADATA_KEYS` in `src/specify_cli/__init__.py`); the engine imports
`specify_cli` rather than re-declaring the key set. The seat half resolves through a block-map
parser inside `sdd-route.py`, because no existing reader can see a nested map.

**Evidence**:
- `src/specify_cli/__init__.py:116-144` — `NEUTRAL_AGENT_METADATA_KEYS` is a
  `key -> (value_domain, default, renders_to_tools)` map. Adding one entry with
  `value_domain={"allowed","forbidden"}`, `default="forbidden"`, `renders_to_tools=False`
  makes the key validated, defaulted, and excluded from host rendering in one edit.
- `src/specify_cli/__init__.py:224-229` — `parse_agent_frontmatter` raises on any indented
  frontmatter line ("nested/multi-line YAML is not supported"). The Agent half must therefore
  be a flat scalar (`sdd-invocation: allowed`), which is exactly what FR-003 specifies.
- `scripts/python/goal-utils.py:325-336` — `_split_frontmatter` reads team.md with
  `line.partition(":")` per line and keeps the raw right-hand side as a string; it is a flat
  scanner. It is the only team.md reader among the 29 engines (`grep -rn "team.md"
  scripts/python/` returns `goal-utils.py` and `run-determination.py` only). A nested `seats:`
  map is invisible to both, so the seat parser is new work and belongs where the predicate
  lives.
- `scripts/python/regen-command-copies.py:33-36` — the established pattern for a `scripts/`
  engine that needs the CLI package: `sys.path.insert(0, REPO_ROOT / "src")` then
  `import specify_cli`. In a client project the same import resolves through the installed
  `specify-cli` distribution, so one import covers both hats.

**Rejected**: (a) re-declaring the allowed set in the new engine — a second definition point
for the neutral vocabulary, precisely the drift `tests/contract/test_neutral_metadata_schema.py`
exists to prevent; (b) extending `goal-utils.py` with a nested parser — that engine owns goal
identity and target resolution, and authorization is not a goal fact; (c) storing the seat
policy as a flat key (`sdd-invocation-<seat>`) to reuse the flat scanner — it would make every
seat a frontmatter key, unbounded, and FR-004 fixes the map-under-`seats` shape.

## R3 — The seat map is block-style only; a flow-style map is rejected as malformed

**Decision**: the canonical form is

```yaml
seats:
  <seat-slug>:
    sdd-invocation: allowed | forbidden
```

Flow-style (`seats: {a: {sdd-invocation: allowed}}`) is reported as malformed input with the
seat named, never parsed best-effort.

**Evidence**: measured across every `team.md` in the tree (25 files —
`find . -name team.md | wc -l`, of which 4 are `tests/fixtures/teams/` fixtures and 1 is the
`templates/commands/team.md` schema carrier): all use block style
for every nested structure (`territory:` with `write:`/`read:`/`forbidden:`, `members:` as a
sequence, `config:` as a nested block). Zero flow-style nested maps exist, so supporting two
syntaxes buys compatibility with nothing and costs a second parser path whose disagreement
with the first would be undetectable.

**Rejected**: accepting both forms (two syntaxes for one fact is an OSoT violation in the
small), and a permissive "parse what you can" fallback (a silent partial resolution of an
authorization input is the fail-open failure FR-005 forbids).

## R4 — Narrowing the anti-nesting obligation keeps every pre-change case's verdict

**Decision**: amend `shared/definitions/subagent-definitions.md` § Dispatch-Time Governance
Obligation once — the prohibition becomes the three-condition predicate of FR-005 plus the
depth-2 chain and virtual-mode prohibition of FR-006 — and amend the mirror of the obligation
in `skills/internal/run-agent/SKILL.md` (the pre-dispatch probe) to enforce it fail-closed.

**Evidence** (the pre-change case set, measured before any edit):
- `tests/contract/test_agent_dispatch_mechanism.py:107-114` (`test_c6_...`) asserts that the
  governance section contains `反嵌套` or `嵌套` and mentions `run-agent`.
- `tests/contract/test_agent_dispatch_mechanism.py:305-310` (`test_c20_...`) asserts the
  run-agent skill contains `反嵌套`/`嵌套`, `循环层级`/`层级`, and `派发前`.
- `tests/contract/test_sdd_loop_driver_skill.py:484` asserts `反嵌套` is present in the
  run-agent skill.
- All five assertions are *presence* assertions, so an amendment that keeps those terms keeps
  every case's verdict. What the amendment removes is the exclusivity claim ("depth is always
  1"), which no test asserts in that form — verified by grepping the three files for `层级恒为`
  and `loop depth`: the only occurrences are in the source documents, not in assertions.
- The baseline targeted suite ran green before this plan: 191 passed, 0 failed
  (`test-evidence/targeted-set-v1-baseline.txt`).

**Rejected**: deleting the obligation and replacing it with a new section elsewhere — FR-006
requires the amendment to state the depth-2 chain in the anti-nesting owner, and moving it
would leave the old prohibition in place, which is a contradiction rather than a narrowing.

## R5 — The pre-dispatch probe is instruction-level plus an engine call; it is not a probe-registry entry

**Decision**: `run-agent`'s dispatch governance section states the predicate and calls
`sdd-route.py --action authorize`; the probe fails closed and names the failing half. No entry
is added to `shared/definitions/probe-definitions.md`.

**Evidence**: `shared/definitions/probe-definitions.md` sections are `## Slices`, `## Classes`,
`## Objects`, `## Handler`, `## HandlerBinding`, and the generated faces are `## Wrap-up`
steps compiled by `probe-utils.py --action compile-embeds` (fingerprint `7877db82c58c` on all
three skills this feature touches). Those faces are wrap-up steps with a bound handler. A
dispatch-time content check has no wrap-up face and no handler, so registering it would create
an object with no consumer — and FR-005 asks for enforcement, not registration.

**Rejected**: a new probe class (no handler to bind), and a shell-only check inside
`create-team/scripts/dispatch.sh` (the wrapper is deliberately generic and CLI-agnostic — see
`subagent-definitions.md` § Dispatch-Time Governance Obligation last paragraph — and the
obligation is a caller-side *content* duty by design).

## R6 — The nested entry form is additive inside the driver, with the handoff schema in a reference

**Decision**: `skills/external/sdd-loop-driver/SKILL.md` gains one § Invoked-from-Team Entry
section placed before § The Loop (entry validation, the five accepted inputs, the stop-at-review
boundary) plus one line in Hard Requirements; the handoff schema and its required-field list
live in a new `references/nested-invocation.md`.

**Evidence**: the driver's own U0 table (`skills/external/sdd-loop-driver/SKILL.md:31-42`)
resolves defaults for target project / topology / authority document / breakpoint / slice. The
invoked-from-team form supplies facts that table has no column for (goal reference, optional
Target, team slug, invoking seat, authorized scope, routing verdict), so it is a *new entry
form*, and the existing default table must stay byte-identical (FR-027: additive on the
standalone entry contract).

**Rejected**: (a) a second skill that hosts nested runs — that is SDD-within-SDD under another
name and duplicates U0–U6; (b) folding the nested form into the existing U0 default table — the
table's semantics are "resolve a missing parameter", while a nested entry *validates* supplied
parameters and refuses on failure, which is the opposite direction and would blur the fail-closed
boundary.

## R7 — The handoff is a returned-message block; the tracked surface is the team run report

**Decision**: the canonical handoff is a fenced block in the invoking member's return
(`handoff` with the FR-016 fields). The tracked artifact that carries it is the team run
report's `## Nested SDD Runs` section, written by the team supervisor. The nested run itself
writes no tracked artifact.

**Evidence**: FR-020/A13 fix the writer (team supervisor is the sole writer of tracked
artifacts); `skills/internal/create-team/SKILL.md:53-63` fixes the report path and the existing
mandatory section set; `goal-definitions.md:138` fixes Target attribution as a *derived* fold
from team ledgers (`items.jsonl` rows carrying a `target_ref`) written at summary time, never
back into `goal.md`. A handoff file under the spec or team directory would be a third written
surface with no declared owner.

**Rejected**: a handoff file per nested run under `.specify/teams/<slug>/runs/` — it would be a
tracked artifact written by the nested run, contradicting FR-020; and a goal-archive write, which
`goal-definitions.md` forbids outside `/speckit.goal`.

## R8 — The instructions pointer is one additive ambient section, injected by the existing generator

**Decision**: add one section to `templates/instructions-template.md` (a pointer to the routing
owner plus the conjunction rule for proactive promotion), then regenerate
`.specify/instructions.md` with `scripts/bash/generate-instructions.sh`; the compatibility
symlinks follow because they point at the file.

**Evidence**:
- `scripts/bash/generate-instructions.sh:177-232` — the additive section reconcile injects
  template sections missing from the live file and never rewrites existing ones; guarded by
  `tests/contract/test_instructions_section_propagation.py` (part of the 191-case baseline).
- Symlink topology measured: `AGENTS.md`, `CLAUDE.md`, `QODER.md` → `.specify/instructions.md`,
  `.github/copilot-instructions.md` → `../.specify/instructions.md`. Regenerating the file needs
  no link repair.
- **Size budget, measured at plan time**: `INSTRUCTIONS_BUDGET_BYTES=32768`
  (`scripts/bash/generate-instructions.sh:38`); `.specify/instructions.md` is 41,948 B and
  `templates/instructions-template.md` is 34,666 B — both already over budget before this
  feature. The criterion for this feature is therefore "the new section stays within a declared
  byte ceiling and its delta is measured", not "the file fits the budget": the overage predates
  the feature and attributing it here would be a false accusation, while silently ignoring the
  growth would hide a real regression.
- `shared/guidelines/proactive-trigger.md` (118 lines, sections `## Ownership` … `## Tuning
  Protocol`) owns situation promotion; FR-024's conjunction is stated once in the routing owner
  and reached from there, not restated in the trigger discipline.

**Rejected**: writing the pointer straight into `.specify/instructions.md` — a client-side
instance fix under the two-hats rule; and putting the section into the trigger guideline only —
the trigger layer is not read by an agent that is about to write.

## R9 — No new shipped Agent preset; FR-023 is a conditional conformance rule

**Decision**: ship no `sdd-invocation`-bearing Agent template. FR-023 is implemented as a
conformance rule validated against whatever declares the key (fixtures under `tests/fixtures/`,
plus any authored instance), and as a negative assertion that `agents/sdd-executor.agent.md`
does not declare `allowed`.

**Evidence**: `ls agents/` → 3 presets (`sdd-executor`, `skill-verifier`,
`structure-adjuster`); none declares the key, and none of the 28 FRs names a preset to create.
FR-023's grammar is conditional ("An Agent Template or Instance that hosts SDD MUST…"), and its
second sentence is the binding one for the shipped roster: the stage-executor capacity stays a
leaf.

**Rejected**: shipping an "SDD host" preset — a new product surface no FR authorizes, against
Principle IX, and it would have to be reconciled with the 070 stage-team preset in the same
change.

## R10 — The golden case table lives in the owner document; tests call the engine

**Decision**: the golden table is a Markdown table inside
`shared/definitions/sdd-routing-definitions.md`; `sdd-route.py --action golden` parses and
judges it; the unit test asserts the engine's verdict and also evaluates each row twice to
prove idempotence. No second copy of the rows exists in test code.

**Evidence**: SC-002 requires the documented verdict and reason code "for every row of a
golden case table" plus identical verdicts on re-evaluation. A table duplicated in test code
would let the engine and the table disagree while both suites stay green — the exact failure
`shared/guidelines/one-source-of-truth.md` § Reference, don't copy names.

**Rejected**: rows parametrised in test code (second copy), and rows in a separate JSON fixture
(same problem plus a second file format to keep in sync).

## R11 — The containment claims are made decidable by node-id case sets, not by test counts

**Decision**: FR-026 / FR-027 / SC-005 are discharged by collecting the *node id* set of the
named suites at the pre-change commit (`7831bb4bb`) and at the post-change tree, then asserting
set containment plus equality of verdicts for the shared ids. The baseline artifacts are frozen
into `test-evidence/` at the start of implementation, before any edit.

**Evidence**: `docs/reference/history/00-cross-cutting-lessons.md` records the failure mode of
absolute-count criteria and the `comm -13` failure-set technique; the repo's own recent
precedent (Feature 072) uses a frozen `coverage-baseline.txt` for the same shape of claim. A
count is not a case set: one renamed case and one new case net to zero.

**Rejected**: "the suite stays green" as the criterion — a green suite says nothing about
whether a case was silently dropped, which is precisely what FR-027's containment clause exists
to forbid.

## R12 — One intentional pin change, declared

**Decision**: `tests/contract/test_neutral_metadata_schema.py::test_c6_framework_keys_are_marked_non_rendering`
pins `NEUTRAL_AGENT_FRAMEWORK_KEYS` by exact set equality
(`tests/contract/test_neutral_metadata_schema.py:130-136`). The literal gains exactly one
member, `sdd-invocation`, in the same change that adds the key. This is the feature's only
intentional change to an existing assertion.

**Why it is not a weakened guard**: the assertion still fails when any framework key renders,
and still fails when a rendering key is smuggled into the framework set. What changes is the
set's membership — which is the fact under amendment, not the proposition being guarded.

**Evidence**: `tests/contract/test_neutral_metadata_schema.py:137-140` cross-checks membership
against `NEUTRAL_AGENT_METADATA_KEYS`, so a code-side addition without the test edit is red, and
a test edit without the code addition is red. `tests/contract/test_tool_mapping.py:58-70`
(`test_m4_...`) requires every *rendering* key to appear in each tool's `fields` map and forbids
framework keys there — so `renders_to_tools=False` is also asserted from the tool side.

**Rejected**: keeping the key out of `NEUTRAL_AGENT_FRAMEWORK_KEYS` and relying on
`renders_to_tools=False` alone — the frozenset is the declared meaning ("reserved for framework
assembly"), and a framework key outside it would be a second, contradictory classification.

## R13 — Same-author scoring is disclosed, not delegated

**Decision**: every Constitution Check row carries `(direct read, subagent unavailable)`, and
the program-derivable checks were executed instead: `pre-analyze-check.py --stage plan`,
`clause_extract.py`, `account-clause-coverage.py`, `sync-mirrors.py --check`,
`regen-command-copies.py --check`, and the 191-case targeted baseline.

**Evidence**: `shared/workflow/objective-analysis-gate.md` delegates scoring when the analyzed
artifacts were authored in the same pass; this environment exposes no subagent tool, and the
stage brief fixes `decomposition=single-package` with no subagent dispatch. Delegation is
therefore impossible, and a self-scored row presented as independent evidence would be worse
than a disclosed one.

**Rejected**: claiming delegated scoring (false), and skipping the Constitution Check (it is a
gate).

## R14 — Test plan: what is new, what is reused, and why the baseline matters

**Decision**: six new contract/unit test files, one new fixture module, and zero changes to
existing test *propositions* except R12's declared pin:

| Surface | New test file | Behaviour group |
|---------|---------------|-----------------|
| Routing engine + golden table | `tests/contract/test_sdd_routing_engine.py` | deterministic verdicts, precedence, reason codes, idempotence, ambiguity/conflict never `direct` |
| Owner document shape | `tests/contract/test_sdd_routing_definitions.py` | owner declaration, closed domains, one-declaration-point (no second table) |
| Authorization predicate | `tests/contract/test_sdd_authorization.py` | agent half, seat half, AND, defaults, malformed seat map, failed half named |
| Pre-dispatch probe | `tests/contract/test_sdd_invocation_governance.py` | depth-2 chain, virtual prohibition, stage-executor refusal, superset + same-verdict containment |
| Nested invocation + handoff | `tests/contract/test_nested_sdd_invocation.py` | entry validation, stop-at-review, handoff field set, no merge/push, stall handoff |
| Report and attribution | `tests/contract/test_nested_run_report.py` | `## Nested SDD Runs` mandatory, no-invocation explicit, ledger attribution by supervisor only, no new Goal field |

**Evidence**: `tests/fixtures/` already carries team fixtures (`tests/fixtures/teams/`) and a
git-repo fixture precedent (`tests/fixtures/review_git_repo.py`, Feature 071); the new fixture
follows that shape — a temporary repository with a minimal `.specify/` runtime, two team seats
(one `allowed`, one `forbidden`), two agent definitions, and one goal with an open Target.

**Rejected**: extending `test_agent_dispatch_mechanism.py` with the new predicate cases — the
containment claim in FR-026 is stated over the *suite's* case set, and adding cases to the same
file would make the pre/post comparison opaque; a separate file keeps the superset relation
mechanical.

## Merged from slices

<!-- source: 074a-authorized-routing -->

### RA1 — The slice re-derives per requirement entry, and its ids are local projections


**Decision**: the slice's design set covers local FR-001–FR-025 and SC-001–SC-007. Clauses are
re-derived per requirement entry regardless of which parent contract file physically carries them,
numbered consecutively `C-1`…`C-47` across four slice files, each tagged `父 C-nn` for its source
(parent C-1…C-14 → slice C-17…C-30; parent C-58/C-59/C-67 and the FR-014/FR-018 facets of C-64/C-66
→ slice C-30/C-43/C-44/C-46/C-47). Entities are renumbered `E1`…`E9` with the two deferred parent
entities named rather than renumbered; validation rules keep `V-1`…`V-29` unchanged because all 29
fall inside the slice and a renumbering would create a second id space for an identical set.

**Evidence**:
- `.specify/specs/074a-authorized-routing/requirements.md` § Parent Mapping (20 FR / 6 SC / 10 STR
  mapped one-by-one) and § Cross-Slice Design Attribution D-1.
- `.specify/state/074-goal-team-sdd-unification.md` § 拆分记录（tasks U4，2026-10-28）: the two slices'
  FR sets are declared mutually exclusive and their union is the parent's 28; that declaration is
  `confirmed-user`.
- `python3 scripts/python/clause_extract.py .specify/specs/074a-authorized-routing/contracts/*.md`
  (executed; output in `test-evidence/plan-stage-checks.md`) — 47 clauses, ids contiguous
  `C-1`…`C-47`, every file canonical `md-bold-closed`.

**Rejected**: (a) grouping the slice's contracts to mirror the parent's five file names — it would
force the deferred clauses' requirement entries (parent FR 020–024, FR 026–028) back into the slice,
contradicting the recorded split; (b) reusing the parent's clause ids with 20 holes — a 47-element
sequence with holes reads as "something was dropped", while the slice's own consecutive numbering plus
the `父 C-nn` tag keeps the derivation auditable in one table; (c) referring to the parent's contract
files as the operative design without re-deriving — the slice would then have no design set of its
own, and the parent's clauses for deferred requirements would be indistinguishable from the ones the
slice must implement.

### RA2 — One owner document, one engine, and both are created in this slice


**Decision**: inherit the parent ruling unchanged. The routing rule's single owner is
`shared/definitions/sdd-routing-definitions.md`; the decision is implemented by one read-only,
stdlib-only engine `scripts/python/sdd-route.py` with three actions (`route`, `authorize`,
`golden`) that parses the owner document at run time. Scope difference from the parent: this slice
implements all three actions, because authorization (`authorize`) is the slice's US1 and routing
(`route` / `golden`) is its US2.

**Evidence**:
- `ls shared/definitions/sdd-routing-definitions.md` → *No such file or directory*;
  `ls scripts/python/sdd-route.py` → *No such file or directory* (both are new, neither exists today).
- Precedent for the shape: `scripts/python/flow-class-check.py` — an owner document holding the
  criteria plus a read-only engine exposing actions with a documented exit alphabet.
- `python3 scripts/python/flow-class-check.py --action check` → 79 units scanned, 0 findings
  (the slice's FR-025 negative check: no new flow unit is introduced by adding an engine action).

**Rejected**: a second engine split by predicate (parent research R1 rejects it for the same reason
FR-018's spirit gives: one owner, one failure vocabulary); a gold table in a data file (a second copy
of the verdict table).

### RA3 — The two authorization halves keep their measured read paths


**Decision**: the Agent half resolves through the CLI's neutral key set; the seat half through a
block-map parser inside the engine, because no existing reader can see a nested map.

**Evidence (re-measured 2026-10-29)**:
- `grep -n 'NEUTRAL_AGENT_METADATA_KEYS\|NEUTRAL_AGENT_FRAMEWORK_KEYS' src/specify_cli/__init__.py`
  → `119`, `149`: one key→(domain, default, renders_to_tools) map plus one framework-key frozenset.
- `grep -c 'sdd-invocation' src/specify_cli/__init__.py` → `0`: the key is genuinely new, so the
  single declared pin change (RA8) is a *gain* of exactly one member, not a relaxed guard.
- `src/specify_cli/__init__.py:227` → the parser raises `nested/multi-line YAML is not supported in
  agent metadata`, so the Agent half must be a flat scalar.
- `scripts/python/goal-utils.py:325` (`_split_frontmatter`) and `:762` (the `team.md` path) — the only
  team.md reader among the engines is a flat per-line scanner; a nested `seats:` map is invisible to
  it, so the seat parser is new work and belongs where the predicate lives.

**Rejected**: extending `goal-utils.py` with a nested parser (that engine owns goal identity, not
authorization); a flattened per-seat key (`sdd-invocation-<seat>`) reusing the flat scanner — FR-004
fixes the map-under-`seats` shape and a per-seat key would grow the frontmatter without bound.

### RA4 — The anti-nesting narrowing lands once, at its owner site


**Decision**: amend `shared/definitions/subagent-definitions.md` § Dispatch-Time Governance
Obligation once — replacing the unqualified "loop depth is always 1" sentence with the depth-2 chain,
the three-condition predicate, and the virtual prohibition — and amend the pre-dispatch probe in
`skills/internal/run-agent/SKILL.md` to enforce it fail-closed by calling the engine's `authorize`
action.

**Evidence (re-measured 2026-10-29)**:
- `grep -n '^## ' shared/definitions/subagent-definitions.md` → `## Dispatch-Time Governance
  Obligation` at line `98`; the exclusivity sentence sits at line `104`.
- `skills/internal/run-agent/SKILL.md:119` carries the pre-dispatch anti-nesting obligation that the
  probe amends.
- The pre-change case set that must stay green is the 13-file targeted suite: `191 passed` at
  `stage_base=939766891` (`test-evidence/targeted-set-v1-baseline.txt`). Its anti-nesting assertions
  are *presence* assertions (`反嵌套` / `嵌套` / `派发前` / `循环层级`), so an amendment that keeps those
  terms keeps every case's verdict; the removed exclusivity claim is asserted nowhere in that form.

**Rejected**: deleting the obligation and re-stating it elsewhere (the old prohibition would survive
in the old place, which is a contradiction rather than a narrowing); registering the probe in
`shared/definitions/probe-definitions.md` (a dispatch-time content check has no wrap-up face and no
handler to bind — an object with no consumer).

### RA5 — The nested entry is additive inside the driver; the handoff is a returned block


**Decision**: `sdd-loop-driver` gains one § Invoked-from-Team Entry section plus one Hard Requirement
line; the handoff schema and its closed field set live in a new
`skills/external/sdd-loop-driver/references/nested-invocation.md`. The nested run stops at review
(after the driver's existing review-repair loop settles) and performs no merge and no push.

**Evidence**:
- `ls skills/external/sdd-loop-driver/references/` → `cli`, `decomposition-model.md`,
  `dispatch-recipes.md`, `efficiency-model.md`, `stage-prompts.md`, `state-awareness.md`,
  `watch-model.md` — no handoff schema exists today, so the new reference has no predecessor to
  amend and duplicates nothing.
- The driver's own U0 default table resolves *missing* parameters; a nested entry *validates
  supplied* parameters and refuses on failure, which is the opposite direction, so the two forms
  cannot be folded together without blurring the fail-closed boundary (parent research R6's measured
  reasoning, re-read against `skills/external/sdd-loop-driver/SKILL.md` this run).

**Rejected**: a second skill hosting nested runs (SDD-within-SDD under another name, duplicating
U0–U6); folding the nested form into the U0 default table (semantics collide: resolve-vs-validate).

### RA6 — D-2: the verdict record's carrier in this slice is the Agent execution evidence


**Decision**: local FR-013's "team run report **or** Agent execution evidence" is discharged here by
the **Agent execution evidence**: the five inputs, the verdict, the reason code, the actor, and any
user override are recorded there, and the handoff plus the invoking Agent's result reach that record
by stable path (slice contract C-27). The team report's nested section — and the verdict reference it
will carry — arrives with `074b-nested-governance` and reads the same record without recomputation.

**Evidence**: the slice defines no fixed report section (parent STR-011's heading literal is parent
parent FR 021, deferred), so the only record surface this slice can deliver is the execution evidence;
`requirements.md` § Requirements FR-013 already admits that reading through its own "or". The ruling
is recorded in `requirements.md` § Clarifications `### Session 2026-10-29` as an unattended
self-adjudication.

**Rejected**: building the report section here (it would pull 074b's contract into this slice, and
`requirements.md` § Out of Scope explicitly places it there); recording the verdict in no durable
place (the outer layer could then not read the verdict the duty acted on).

### RA7 — D-3: SC-003 is delivered on its content face; the fixtures do not assert the section heading


**Decision**: local SC-003 is discharged by asserting (a) the nested run reaches review and produces
the complete SDD artifact chain, (b) `git log` / `git status` show zero merge and zero push, and
(c) every artifact and evidence path is referenced from the invoking Agent's result and from the team
run report written under its existing contract. The `## Nested SDD Runs` heading literal and its
mandatory-and-explicit-when-empty semantics are `074b-nested-governance`'s, so this slice's fixture
never asserts that literal.

**Evidence**: local FR-017 already requires the invoking Agent to carry the handoff into its own
result and the run report; the three content-fact assertions are mechanical over that deliverable.
`requirements.md` § Out of Scope lists "team report 嵌套段" as out of scope — the sentence names the
*section*, i.e. its heading and section semantics, not the path references it will contain; D-3
records exactly that reading.

**Rejected**: implementing the section to satisfy SC-003 literally (a 074b contract delivered twice);
declaring SC-003 undeliverable in this slice (its three content facts are mechanically assertable
here, and § Out of Scope is silent on them).

### RA8 — Test surface split, and the one declared pin change


**Decision**: the slice carries five of the parent plan's six new contract suites plus the fixture and
the single declared pin change; the sixth (`test_nested_run_report.py`) belongs to the
`074b-nested-governance` report-section contract.

| Surface | Test file (new unless noted) | Behaviour group |
|---------|------------------------------|-----------------|
| Owner document shape | `tests/contract/test_sdd_routing_definitions.py` | owner declaration, closed domains, one declaration point, invocation-kind classification |
| Routing engine + golden table | `tests/contract/test_sdd_routing_engine.py` | deterministic verdicts, precedence, reason codes, idempotence, ambiguity/conflict never `direct` |
| Authorization | `tests/contract/test_sdd_authorization.py` | agent half, seat half, AND, defaults, malformed seat map, failed half named |
| Pre-dispatch governance | `tests/contract/test_sdd_invocation_governance.py` | predicate, depth-2 chain, virtual prohibition, stage-executor refusal, pre-existing cases green |
| Nested invocation + handoff | `tests/contract/test_nested_sdd_invocation.py` | entry validation, stop at review, handoff field set, zero merge/push, stall handoff, path references (D-3) |
| Fixture | `tests/fixtures/nested_sdd.py` | temp repo: minimal `.specify/`, one authorized and one unauthorized seat, two agent definitions, one goal with an open Target |
| Pin change (edit) | `tests/contract/test_neutral_metadata_schema.py` | the framework-key frozenset gains exactly one member, in the same change as the code edit |

**Evidence**: `grep -n 'NEUTRAL_AGENT_FRAMEWORK_KEYS' tests/contract/test_neutral_metadata_schema.py`
→ lines `17`, `130`, `137`: line `130` is the exact-set-equality pin and line `137` cross-checks the
set against `NEUTRAL_AGENT_METADATA_KEYS`, so a code-side addition without the test edit is red and
the reverse is red too — the assertion still guards what it guarded.
`ls tests/fixtures/` shows the precedents the new fixture imitates (`teams/`, `review_git_repo.py`,
`line_fixtures.py`).

**Rejected**: adding the predicate cases to `test_agent_dispatch_mechanism.py` (SC-004's "pre-existing
anti-nesting cases stay green" is a statement over that suite's case set; keeping the new cases in a
separate file keeps the relation legible); a sixth new file for the report section (a 074b contract).

### RA9 — Same-author scoring and the stage's mechanical evidence


**Decision**: the Constitution Check table and the Post-Generation Quality Gate are scored by the same
agent that wrote the artifacts, and delegation is impossible in this environment, so every row is
marked `(direct read, subagent unavailable)`; the program-derivable checks were executed instead and
their real output is pasted into `test-evidence/plan-stage-checks.md`.

**Evidence**: `.specify/shared/workflow/objective-analysis-gate.md` delegates the scoring when the
analyzed artifacts were authored in the same pass; the stage brief fixes `decomposition=single-package`
with no subagent dispatch. Executed this stage: `clause_extract.py` (47 clauses), `pre-analyze-check.py
--stage plan`, `account-clause-coverage.py` (FR lane), `sync-mirrors.py --check` (no drift),
`regen-command-copies.py --check` (clean), `flow-class-check.py` (79 units, 0 findings), and the
13-file targeted suite (191 passed).

**Rejected**: claiming delegated scoring (false), and skipping the gate (it is a gate).

<!-- source: 074b-nested-governance -->

### RB1 — Projection with a local id space, tagged to the parent clause it projects


**Decision**: the slice owns a continuous local clause set `C-1`…`C-30` across three contract files,
a local entity set `E1`…`E8`, and a local validation set `V-1`…`V-12`; every clause, entity and rule
that projects a parent clause carries its source tag (`parent C-nn` / `父 E-n` / `parent V-nn`). Only
the 30 parent clauses that serve this slice's eight requirement entries are claimed; the rest stay
`074a`'s and are cited by path.

**Evidence**:
- `074a-authorized-routing/plan.md:266-290` is the authority for the split. Its table names the
  parent clauses deferred to this slice (C-25, C-26, C-27, C-33, C-43, C-44, C-47, C-48, C-49, C-50,
  C-51, C-52, C-53, C-54, C-55, C-56, C-57, C-61, C-62, C-63, C-65) grouped by the parent FR each
  serves, and its prose records the two partial facets (parent C-54's report-section facet, parent
  C-66's Stage-vocabulary facet) that `074a` deliberately left here.
- **Disclosed inconsistency in the read-only sibling, recorded not repaired**: that table lists 21
  clause ids while its opening sentence says "20"; and the Stage-vocabulary facet of parent C-66 is
  named in the prose but absent from the table. This slice claims per the prose and the parent's own
  FR→clause rows (parent C-66 serves parent FR 022, which is this slice's FR-022), and does not edit
  `074a`'s artifact to reconcile the count — a correction there would touch another slice's committed
  plan, while nothing downstream depends on the integer.
- The parent's own FR→clause rows confirm the grouping: parent FR 020 → C-50…C-52, FR 021 →
  C-47…C-49 + C-53 + C-54, FR 022 → C-55 + C-66, FR 023 → C-25 + C-26 (+ C-60, claimed by `074a`),
  FR 024 → C-56 + C-57, FR 026 → C-27 + C-65, FR 027 → C-33 + C-43 + C-44 + C-61 + C-62, FR 028 →
  C-63 + C-67 (parent `feature-ref.md:62-91`).
- `074a` already claimed parent C-15/C-16/C-30/C-60 and the parent FR 013 / parent FR 018 facets of C-54/C-66
  (`074a-authorized-routing/feature-ref.md:63-89`), so this slice references them instead of
  re-claiming them.

**Rejected**: (a) inheriting all 67 parent clauses — 37 of them serve requirement entries this slice
does not carry, and re-claiming them would make two slices the owner of one obligation; (b) reusing
the parent ids verbatim with gaps — the slice's FR/SC/STR space is already local (requirements
§ 编号口径), and a gapped C-space reads as a deletion rather than a projection; (c) mirroring the
parent's five contract files — their grouping is by theme, while this slice's attribution is per
requirement entry (D-1), so the file set follows this slice's three behaviour groups.

### RB2 — The report section lands in the report contract's single owner; `run-team` is not edited


**Decision**: the one mandatory `## Nested SDD Runs` section is added to
`skills/internal/create-team/SKILL.md` § Report contract, and to no other document. The `run-team`
skill keeps delegating its report duty to that owner.

**Evidence**:
- `skills/internal/create-team/SKILL.md:53-63` is the report contract: the report path, the mandatory
  section list as one line (`## Result Summary ## Deliverables ## Verification ## Execution Detail ##
  Run Workspace ## Summary`), the summary vocabulary, and the first-activation line.
- `skills/internal/run-team/SKILL.md:66` already carries the delegation — "报告契约真源:
  create-team SKILL.md → Report" — plus the ledger field the attribution row uses
  (`"target_ref": "T-<nnn>"`), so the supervisor-side obligation already exists and needs no second
  statement.
- `grep -rn "Nested SDD Runs" skills/ templates/ shared/` returns zero hits in shipped surfaces at
  plan time; the only occurrences are `074a`'s test negative
  (`tests/contract/test_nested_sdd_invocation.py:560`) and specification text, which is exactly the
  D-3 hand-over.

**Rejected**: (a) editing both `create-team` and `run-team` — the second edit would restate one
section in two owners, the duplication the one-source-of-truth principle forbids; (b) a new
`references/` file carrying the section — the contract grammar is a fenced report skeleton inside the
owner, and a second carrier would split one obligation; (c) putting the section into the driver's
`nested-invocation.md` — that reference owns the handoff, not the consumer's report shape.

### RB3 — The routing-verdict reference is a reference; the section never re-derives a verdict (D-2)


**Decision**: the section's per-invocation field carries a *reference* to the verdict `074a` recorded
in the Agent execution evidence, and the section states that the input set, verdict table and reason
codes are reached at the owner's path. When the record cannot be located, the section records the
reference as missing and the outer layer MUST NOT re-derive it.

**Evidence**:
- `074a-authorized-routing/feature-ref.md:108-110` (ruling 3, RA6/D-2): the verdict is recorded in the
  Agent execution evidence, and "the report section that will reference it is parent FR 021's and
  lands with `074b-nested-governance`".
- `shared/definitions/sdd-routing-definitions.md` is the single owner of the input domains, verdict
  table, precedence and reason codes (212 lines, delivered by `074a`); `scripts/python/sdd-route.py`
  (1,045 lines) computes a verdict and never stores one in a report.
- The requirements' edge case fixes the failure direction: a missing reference is recorded as missing,
  and a fabricated or recomputed reference is a contract violation (local C-8).

**Rejected**: (a) re-running `sdd-route.py route` from the report-writing step — it would produce a
second verdict for one duty and could disagree with the one the duty acted on; (b) inlining the
verdict's inputs and reason code into the section — a second copy of a table the owner defines, and
the reverse-count audit would flag it; (c) widening the handoff's field set — the handoff is `074a`'s
closed set and this slice adds no field to it.

### RB4 — The hosting-responsibility rule lands in the authoring baseline, and is asserted against the shipped leaf preset


**Decision**: the three responsibility statements an `[[STR-002]]` declaration must carry (hosts the
driver, does not execute stage commands itself, ends at review) are added to
`skills/internal/run-agent/SKILL.md` § Authoring Baseline, immediately after the existing
`sdd-invocation` paragraph; the leaf prohibition is asserted against the shipped
`agents/sdd-executor.agent.md`, which declares no such key.

**Evidence**:
- `skills/internal/run-agent/SKILL.md:171-181` opens the authoring baseline and fixes it as the
  vocabulary the authoring skills enforce; `:193` lists the supported fields including
  `sdd-invocation`; `:195-205` is the existing key paragraph, which already points at
  `src/specify_cli/__init__.py` for the closed values.
- `agents/sdd-executor.agent.md:1-13` (frontmatter) declares `name`, `description`,
  `user-invocable`, `disable-model-invocation`, `supervisor`, `model-tier`, `capability-tools`,
  `skills`, `run-turn-budget`, `display-color` — no `sdd-invocation` (`grep -c sdd-invocation
  agents/*.agent.md` → 0). The leaf rule is therefore checkable against a delivered artifact rather
  than a convention.
- `shared/definitions/agent-definitions.md` owns the three-layer taxonomy (Template / Instance /
  Execution) and is the right place for *what an agent is*, not for *what an author must state*; the
  authoring baseline is the surface an author reads while writing (parent C-26's "conformance check
  reads the declaration and the responsibility text together").

**Rejected**: (a) a new section in `agent-definitions.md` — that file owns the taxonomy, and the rule
is an authoring obligation, not a layer definition; (b) shipping an SDD-host preset so the rule has a
subject in the repo — no requirement names one (parent ruling R9, already applied by `074a`), and a
new product surface is out of scope; (c) enforcing the rule only in the contract test — the rule must
be readable where it is obeyed, not only where it is checked.

### RB5 — The Stage-vocabulary disambiguation is one sentence at the existing bullet, not a new section


**Decision**: `skills/internal/create-team/references/conceptual-model.md` gains one statement at its
`Stage` bullet: the Stage dimension (`executor` / `evaluator` / `optimizer`) is not the SDD stage
roster, the roster stays the driver's, no value is renamed, and no SDD stage name may be used as a
Stage value.

**Evidence**:
- `skills/internal/create-team/references/conceptual-model.md:1-3` declares the file's ownership;
  `:10` is the Stage bullet with the three canonical values and the removal note for the deprecated
  names — the exact site where a reader could mistake the dimension for a stage list.
- `tests/contract/test_single_conceptual_model.py:26` pins that the file defines the Role × Stage ×
  Type model; the file's section structure (`## The three orthogonal dimensions`, `## Type criterion`,
  `## Static vs Dynamic structure`, `## The Team Supervisor`, `## Collaboration patterns`,
  `## Lifecycle`, `## Template home`) is the shape sibling suites navigate, so an added top-level
  section would have no consumer.
- The SDD stage roster's only owner is the driver (`skills/external/sdd-loop-driver/SKILL.md` § The
  Loop and its state-spine format); the parent clause C-66's negative shape (no roster enumeration in
  new text) is what keeps the sentence from becoming a second roster.

**Rejected**: (a) a comparison table of team stages vs SDD stages — it would enumerate the roster
outside its owner, the exact duplication C-66 forbids; (b) renaming a team Stage value to clear the
collision — FR-022 forbids renaming and the rename would break every persisted team; (c) a new
`stages.md` reference — a fifth carrier of one vocabulary.

### RB6 — The instructions pointer is one additive section, and its acceptance is a declared ceiling plus a measured delta


**Decision**: `templates/instructions-template.md` gains exactly one pointer-level `## ` section for
the routing surface; `.specify/instructions.md` is regenerated by
`scripts/bash/generate-instructions.sh` and never hand-edited; the acceptance criterion is the
section's own byte ceiling plus a measured delta, because both files were over the generator's budget
before this slice.

**Evidence** (measured at plan time, `test-evidence/plan-stage-checks.md` § 5):
- `wc -c` → `.specify/instructions.md` 41,948 B, `templates/instructions-template.md` 34,666 B;
  `INSTRUCTIONS_BUDGET_BYTES=32768` (`scripts/bash/generate-instructions.sh:38`). The overage
  predates the slice by several features.
- Section counts: template 29 top-level `## ` headings, live file 30 — the additive reconcile has
  already injected one section the template no longer carries, and it never rewrites existing
  sections.
- `tests/contract/test_instructions_section_propagation.py:11-17` states the C-1/C-2 propositions:
  every template `## ` section MUST exist verbatim in the live file (C-1) and the generator injects
  additively and idempotently (C-2). Adding the section without regenerating therefore turns C-1 red,
  which is the mechanical reason the regeneration is part of the same change.
- `tests/contract/test_instructions_size_budget.py` reports size against the budget and never restates
  the number in the command template, so the ceiling this slice declares lives in its own plan and
  contract, not in the budget owner.

**Rejected**: (a) writing the pointer straight into `.specify/instructions.md` — a client-side
instance fix under the two-hats rule, lost on the next regeneration; (b) putting the pointer only into
`shared/guidelines/proactive-trigger.md` — the trigger layer is not read by an agent that is about to
write; (c) claiming "fits the budget" — unpassable before the slice and a false accusation after it.

### RB7 — The trigger edit is one sentence inside an existing section, and it adds no gate-scannable declaration


**Decision**: `shared/guidelines/proactive-trigger.md` gains one pointer sentence inside its existing
§ Promotion & Safety Boundary stating that promoting an SDD run requires both a routing verdict of the
SDD kind and an effective authorization of `[[STR-002]]`, with the conjunction stated once at the
routing owner. No new `## ` section is created, and the sentence restates no destructive-action class.

**Evidence**:
- `shared/guidelines/proactive-trigger.md` has exactly 10 top-level `## ` sections
  (`## Ownership` … `## Maintenance Duties`), and `tests/contract/test_proactive_trigger_section.py`
  C-2 pins that set as closed and ordered — a new section would break a delivered contract.
- `:68-79` is § Promotion & Safety Boundary, which already carries the promotion threshold, the
  destructive-never-promotes rule and the execution-report duty; the new conjunction belongs beside
  them and must point at the owner rather than re-derive the classification.
- **Pre-existing red, measured and disclosed**: `tests/contract/test_proactive_trigger_section.py::
  test_c11_gate_scan_total_unchanged` fails at the stage base — `gate total moved from the frozen 23
  to 27` (targeted-set run, `test-evidence/targeted-set-v1-baseline.txt`). The four added gates
  predate this slice. The criterion for this slice's edit is therefore "the scan total measured after
  the edit equals the pre-change total", not "the frozen budget is met", and the pre-existing failure
  is recorded rather than repaired here (repairing it would mean editing another feature's
  declarations or its frozen baseline — outside this slice's scope and a decision, not a correction).

**Rejected**: (a) a new `## SDD Invocation` section in the trigger doc — breaks the pinned closed
ordered section set for no reader's benefit; (b) restating the routing verdict table in the trigger
doc so the sentence is self-contained — the duplication C-56/C-57 forbid; (c) repairing the frozen
gate baseline in this slice — it would silently absorb four other features' drifts into this commit
and turn a recorded anomaly into an unrecorded one.

### RB8 — The containment claims are discharged by frozen node-id sets at verification time, not by a permanent ratchet test


**Decision**: FR-026/FR-027/SC-005 are discharged by collecting each named suite's
`pytest --collect-only` node-id set, freezing it at the baseline commit named in the verification
record (captured at plan time into `test-evidence/compat-baseline-nodeids.txt`, 266 cases across 17
files in 7 named sets), and asserting after the change that each post-change set is a superset and
that every shared id keeps its verdict. The permanent guard in the new compat suite asserts the
*structural* negatives and that the frozen carrier exists and parses non-empty per set; it does not
re-collect other suites.

**Evidence**:
- Parent C-62 fixes the method (case set, not count) and its reason: "one renamed case and one added
  case net to zero". Parent ruling R11 records the `comm -13` failure-set precedent and the
  absolute-count anti-pattern.
- The baseline is measurable today and was measured: S1 pre-dispatch governance 49 cases,
  S2 standalone driver entry 25, S3 070 preset 24, S4 064 line/worktree/ownership 40, S5 058 U0–U6 36,
  S6 team suites 54, S7 Agent suites 38.
- `docs/reference/history/00-cross-cutting-lessons.md` records both the absolute-count lesson and the
  "a green check is a claim" lesson; a permanent superset ratchet over *other* features' suites would
  convert a per-change claim into an invariant nobody granted — legitimate case removals (a wording
  pin replaced by an engine test, as `test_proactive_trigger_section.py` documents for its own former
  C-8…C-16) would then fail for reasons unrelated to this feature.

**Rejected**: (a) a count comparison — non-conforming by C-62; (b) a permanent test that re-collects
the sibling suites and compares with a checked-in set — it would fire on every future legitimate case
rename and would make the claim's scope ("relative to the baseline commit in the verification
record") unrepresentable; (c) trusting "the suites stay green" — a green suite says nothing about a
dropped case.

### RB9 — Test plan: three new files, one edited suite, one reused fixture, no new fixture


**Decision**:

| Surface | File | Behaviour group |
|---------|------|-----------------|
| Report section + attribution | `tests/contract/test_nested_run_report.py` (NEW) | `[[STR-010]]` literal and mandatory-ness, per-invocation fields, explicit-when-empty, supervisor-only write, one ledger row with `target_ref`, no new Goal field, verdict reference by reference |
| Diffusion | `tests/contract/test_sdd_diffusion.py` (NEW) | Stage disambiguation, host responsibility statement, leaf preset negative, instructions pointer with no restatement, trigger conjunction pointer, no roster enumeration |
| Compatibility + safety | `tests/contract/test_sdd_compat_containment.py` (NEW) | default-`forbidden` resolution cases, containment carrier shape, four-surface additivity, no new command/skill, no merge/push/scheduler/gate, gate-scan total stability |
| Pre-dispatch governance (edit) | `tests/contract/test_sdd_invocation_governance.py` (EDIT) | the absent-declaration default-resolution cases that make the superset relation non-trivial |
| Fixture | `tests/fixtures/nested_sdd.py` (reused, unchanged) | temp repo with two seats, two agent definitions, one goal with an open Target |

**Evidence**:
- `tests/fixtures/nested_sdd.py` (369 lines, `074a`) already builds the repository shape every 074b
  assertion needs; a second fixture would duplicate it and drift.
- `tests/contract/test_sdd_invocation_governance.py` collects 17 cases today; the eleven
  `default-resolution` propositions FR-026 adds have no home there yet, and adding them is the
  superset direction the containment claim requires.
- The parent's own test assignment (`074-goal-team-sdd-unification/research.md:303-320`, R14) named
  `test_nested_run_report.py` for exactly this slice, so the file name is grounded in the parent
  design rather than chosen here.
- Sibling naming for the two other new files follows `test_sdd_authorization.py`,
  `test_sdd_invocation_governance.py`, `test_sdd_routing_definitions.py`.

**Rejected**: (a) a new fixture module — duplicate repository scaffolding; (b) putting the report
cases into `test_nested_sdd_invocation.py` — that file is `074a`'s handoff suite and its D-3
assertion is explicitly a negative about this section; (c) one catch-all suite for all three behaviour
groups — the disjoint-owner convention used by the sibling slice.

### RB10 — Same-author scoring disclosed, not delegated; the feature status is already at its ceiling


**Decision**: every Constitution Check row carries `(direct read, subagent unavailable)`, and the
program-derivable checks were executed instead (`clause_extract.py`, `account-clause-coverage.py`,
`pre-analyze-check.py --stage plan`, `sync-mirrors.py --check`, `regen-command-copies.py --check`,
`flow-class-check.py`, the targeted suite). The Feature 074 registry row stays `Planned`: no
`Draft → Planned` transition exists for a slice whose parent row is already `Planned`, and
`Implemented` is `/speckit.implement`'s transition over the whole Feature.

**Evidence**:
- `shared/workflow/objective-analysis-gate.md` delegates scoring when the artifacts under analysis
  were authored in the same pass; this environment exposes no subagent tool and the stage brief fixes
  `decomposition=single-package`, so delegation is impossible and a self-scored row presented as
  independent evidence would be worse than a disclosed one.
- `.specify/memory/features.md` row 074 reads `Planned`, and
  `074a-authorized-routing/feature-ref.md:104-105` records the same reading for the first slice ("no
  new Feature row — the slice reuses Feature 074, status stays Planned"). This stage therefore
  appends its entry to `.specify/memory/features/074.md` § Latest Review and updates `Last Updated`;
  it flips nothing.

**Rejected**: (a) claiming delegated scoring (false); (b) skipping the Constitution Check (it is a
gate); (c) advancing the row to `Planned` as if it were a new feature — a no-op that would imply a
transition which did not happen.
