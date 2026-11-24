# Data Model — /speckit.agents run（104-agents-run）

This model names the objects the run intent produces or consumes. It **adds no entity, store or schema**: every object below is either a parsed view of the command input, a projection over an existing carrier, or a payload assembled at dispatch time. The owners of the underlying semantics stay where they are:

- Relative role, seven-field downlink, five-element uplink, depth, edge record: `.specify/shared/definitions/superagent-definitions.md`.
- Subagent, execution modes, visibility contract, dispatch-time governance: `.specify/shared/definitions/subagent-definitions.md`.
- Three-layer Agent taxonomy and definition fields: `.specify/shared/definitions/agent-definitions.md`.
- Attribution of stale returns: `.specify/skills/sdd-loop-driver/references/watch-model.md` § 11.
- Config resolution and its disclosure fields: `scripts/python/execution-config.py` (sole resolver).

## E1 — Run Request（解析后的命令输入）

| Field | Meaning | Values / rules |
|-------|---------|----------------|
| `raw_arguments` | The command's `$ARGUMENTS` text | Free text; shell quoting is the user's responsibility; task text is never parsed as options |
| `verb` | Leading explicit verb or its absence | `run` / `create` / `refine` / `empty` / `none` / `other` (team intent text) |
| `agent_name` | Resolved name token after the verb | Optional; absent on `run` → `missing-agent-name` stop |
| `task_text` | The remainder | Optional at parse; required before dispatch |
| `parse_outcome` | Closed outcome set | `explicit-run` / `missing-agent-name` / `team-intent` / `empty` / `ambiguous` / `create` / `refine` / `unsupported` |

**Rules**: an explicit verb wins over context inference (FR-002); `team-intent` never routes to run — it reports the `/speckit.team` redirect; `empty` executes the no-argument listing behaviour; `ambiguous` reports three capabilities (create / refine / run) and requests the intent; `--target` inside a run request is a team parameter and is reported as a mode/parameter conflict, never silently dropped (Edge Cases).

## E2 — Agent Resolution Result（定义解析结果）

| Field | Meaning | Values / rules |
|-------|---------|----------------|
| `name` | Requested name | Required |
| `layer` | Which layer won | `instance` / `template` (instance wins on collision) |
| `layer_path` | Absolute definition path | `.specify/agents/{instances,templates}/<name>.agent.md` |
| `description` | Frontmatter description | From the definition |
| `shadowed_sibling` | The losing same-name definition | Path or `none`; disclosed, never silently dropped |
| `config_path` | Execution config if present | `.specify/agents/execution/configs/<name>.yaml` or `none` |
| `resolution_status` | Closed status | `resolved` / `not-found` / `corrupt` |

**Rules**: `not-found` → [[STR-002]] + bounded available list (omission count declared) + create suggestion, no dispatch; `corrupt` (directory exists, `.agent.md` missing or unreadable) reports a named-path "定义损坏/不可读" verdict and is never merged with `not-found` (FR-005). Resolution is read-only: a run never modifies the resolved definition and shares no mutable state across executions (FR-013).

## E3 — Role Edge Projection（角色边投影，七字段）

| Field | Meaning | Rule |
|-------|---------|------|
| `parent_identity` | This session's identity on the edge | status-spine `run_id` → line-registry `line_id` → owner literal `root` |
| `child_label` | Dispatch-attempt identifier | Equals E7's label; unique per dispatch |
| `role_declaration` | The declared role for this edge | `subagent` for the child; `dual-role` never appears in a carrier declaration |
| `dispatch_duty` | Independent grant | `granted` / `not-granted` |
| `depth_position` | Computed depth | Child of a root = 1 |
| `authority_ref` | Authorization reference | The existing authorization surface (SDD probe verdict when applicable) |
| `return_channel` | Where the child returns | The parent session's relay channel for this dispatch |

**Rules**: the seven fields are carried in the dispatch payload **by pointer** to the owner's protocol section; their semantics are not restated in this model. A missing field blocks the dispatch (FR-008, FR-009).

## E4 — Dispatch Payload（派发载荷）

| Component | Content | Rule |
|-----------|---------|------|
| `role_edge` | All seven E3 fields | Presence is checked item-by-item before dispatch |
| `fast_fail_clause` | The owner literal | Injected verbatim from `shared/guidelines/fast-fail.md` § 子代理派发注入 |
| `concurrency_obligation` | Pointer to the owner section | By pointer |
| `reporting_duty` | Pointer to `reporting-obligations.md` | By pointer |
| `reanchoring_digest` | Anchor digest per the owner | By pointer |
| `role_transition` | Stable identifier + nine item-id slugs | Required only when `dispatch_duty: granted`; each slug checked |
| `prohibitions` | Anti-nesting red lines | No driver skill reference, no skill-load instruction, no loop logic |

**Rules**: the pre-dispatch self-check requires the `role-transition` identifier and each of the nine slugs (granted dispatches) **and** the seven edge fields; a missing identifier, slug or field is a payload-construction defect and blocks the dispatch before it starts (FR-008, FR-009).

## E5 — Presentation Disclosure（派发前呈现）

| Group | Content |
|-------|---------|
| Identity & task | Agent `name`, `layer`, `description`; the task brief |
| Role relation | This session = the edge's **superagent (root)**; child label; return channel |
| Config disclosure | `config_id`, `mode`, `cli`, effective `model` / `reasoning_effort` / `context_window`, `source_chain`, `skipped_layers`, `quantification`, `requires_external` (existing discipline, sole resolver `execution-config.py`) |

**Rules**: disclosure, not a blocking gate — the user may stop the dispatch; the role and protocol details are referenced by pointer, never restated (FR-007). This clause is behavior-class: evidenced by the truth-source text and review, not by a contract test (FR-023).

## E6 — Return Record（回传记录，五要素上行）

| Element | Meaning | Missing → |
|---------|---------|-----------|
| `result_or_deliverable_path` | Result text or declared output path | `incomplete` |
| `evidence_pointers` | Paths/commands backing the result | `incomplete` |
| `anomaly_line` | Explicit anomaly line; `未发现异常` when none | `incomplete` (silence is not clean) |
| `concurrency_reading` | `requested` / `effective` / `effective_reason` | `incomplete` |
| `returning_executor_identity` | The child's identity/label | `incomplete` |

**Rules**: any missing element makes the return **incomplete**; the parent MUST NOT consume its conclusion and MUST NOT backfill the missing fields (FR-010). Behavior-class (FR-023).

## E7 — Child Label（派发尝试标识）

| Field | Meaning | Rule |
|-------|---------|------|
| `label` | The dispatch label | `dispatch.sh <label>` value; used verbatim as `run_id` |
| `run_id` | Quantification join key | `exec-quant.py --action collect-dispatch --run-id <label>` |
| `triplet` | External artifact names | `<label>.live.log` / `<label>.jsonl` / `<label>.status` |
| `attempt` | Attempt identity | Every run is a new attempt; a retry is a new label |
| `prior_artifacts` | Old attempts' artifacts | Kept, never overwritten |

**Rules**: labels are unique within one superagent's dispatches; a retried task uses a new label; a stale attempt's late return is attributed per the watch model and MUST NOT be consumed as the current result; no label generator, child list or registry is added (FR-011, A-6).

## E8 — Visibility Surface（多子代可见性面，既有载体）

| Carrier | What it shows | Owner |
|---------|---------------|-------|
| External artifact triplet | Liveness and completion per child | `subagent-definitions.md` § External Dispatch Visibility Contract |
| `exec-quant` dispatch record (`unit_type=agent`, `unit_id=agent:<parent>`, `run_id=<label>`) | Quantification and parent linkage | `exec-quant.py` |
| `status-digest.py` role view (`parent` / `roles` / `role_set_marker` / `depth`) | Parent row + one row per child, truncation declared | `superagent-definitions.md` § Visualization & Tracking |

**Rules**: this feature adds none of these; it only points the dispatch surface at them. Multiple children are read from the same digest run (FR-012, SC-002).

## E9 — Governance Check（治理判定）

| Field | Meaning | Rule |
|-------|---------|------|
| `applies` | Whether the SDD authorization probe runs | `true` only when the payload assigns or names an SDD driver under the narrowed predicate |
| `engine` | The probe | `sdd-route.py --action authorize` |
| `verdict` | The engine's record | Dispatch only on the owner's allowed verdict; any other value blocks an SDD-driver dispatch |
| `refusal_record` | Named refusal | Failing half (`agent` / `seat` / `both`), resolved values, both source paths, seat slug |

**Rules**: a normal run assignment (no SDD driver named) does **not** invoke the probe and is not blocked by a missing team/seat; a refusal is never dispatched and keeps the existing named-refusal shape (FR-016, A-7).

## State transitions — one dispatch attempt

| From | Event | To |
|------|-------|----|
| `resolved` | presentation rendered | `presented` |
| `presented` | payload self-check passes | `dispatching` |
| `dispatching` | child starts | `running` |
| `running` | return with all five elements | `returned-complete` |
| `running` | return missing any element / failure / timeout | `returned-incomplete` |
| `returned-complete` | parent consumes | `consumed` |
| `returned-incomplete` | parent refuses to consume | `not-consumed` |
| any state | retry requested | a **new attempt** with a new label; the old attempt's artifacts stay |

A stale return from a superseded attempt never transitions the current attempt; it is attributed per `.specify/skills/sdd-loop-driver/references/watch-model.md` § 11 and ignored as a current result.

## Invariants

- **INV-01** Role is decided only by the dispatch edge; never by executor type, model, tool list, prompt wording or self-description (FR-006).
- **INV-02** Every dispatch payload carries all seven E3 fields; a missing field blocks dispatch (FR-008, FR-009).
- **INV-03** A `dispatch_duty: granted` payload carries the `role-transition` identifier **and** each of the nine slugs; a missing one blocks dispatch (FR-008, FR-009).
- **INV-04** The four pre-existing injections are present in the payload by pointer; the fast-fail clause is injected verbatim (FR-008).
- **INV-05** Every return carries the five E6 elements; an incomplete return is never consumed and never backfilled (FR-010).
- **INV-06** Every dispatch uses a unique child label; a retry is a new attempt; old artifacts are kept (FR-011).
- **INV-07** One run = one edge = one child; a run never fans out multiple agents (FR-014, FR-017, A-13).
- **INV-08** Multi-child visibility uses only the three E8 carriers; no new store, registry or renderer (FR-012).
- **INV-09** The SDD probe applies only to SDD-driver assignments; a normal run is never blocked by a missing team/seat (FR-016).
- **INV-10** The concurrency reading triple is complete on every run; this dispatch is `single-unit`; absent intervals record `not_evaluated`, never 0 or an estimate (FR-017).
- **INV-11** The command reference has exactly one body; the stale-literal set is empty across the seven named files; the three syntax faces carry [[STR-001]] (FR-018…FR-020, SC-004).
- **INV-12** No new persistence root, registry, renderer, scheduler or queue; no probe or flow-class row is added (FR-015, SC-005).

## Entity → FR map

| Entity | FRs |
|--------|-----|
| E1 Run Request | FR-001, FR-002, FR-003, FR-004, FR-014 |
| E2 Resolution Result | FR-005, FR-013 |
| E3 Role Edge | FR-006, FR-008, FR-009 |
| E4 Dispatch Payload | FR-008, FR-009 |
| E5 Presentation | FR-007 |
| E6 Return Record | FR-010 |
| E7 Child Label | FR-011 |
| E8 Visibility Surface | FR-012 |
| E9 Governance Check | FR-016 |
| All entities' reading/text pins | FR-017, FR-021, FR-022, FR-023, FR-024 |
