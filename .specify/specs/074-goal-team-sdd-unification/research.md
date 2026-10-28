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
