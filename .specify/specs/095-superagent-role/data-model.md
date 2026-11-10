# Data Model — Super Agent Role (095-superagent-role)

All entities below are **projections over existing carriers** (FR-003, FR-025, FR-035). None of them is a new store; the field shapes are what the read-only engine (`scripts/python/role-edge-check.py`) and the digest role view parse.

## 1. Role (role set)

| Field | Domain | Notes |
|-------|--------|-------|
| `role` | `superagent` \| `subagent` (machine identifiers, [[STR-001]]) | Relative to one dispatch edge; never an entity type |
| role set | subset of `{superagent, subagent}` | Output as a **set**; the both-roles machine marker is `dual-role` ([[STR-002]]) |
| owner | `.specify/shared/definitions/superagent-definitions.md` ([[STR-004]]) | This model only fixes the field names the engine consumes |

Validation: a role is decided **only** by edge endpoints (FR-001). Records that classify by executor type, model or prompt wording are a defect; the contract test's type-based-classification mutation must turn red. `dual-role` is a set-state marker that appears only in role-set **output**: it is never a third role value and never a carrier declaration value. The dispatch-duty grant is a separate declaration (`dispatch_duty`, § 2), not a role claim.

## 2. Role Edge (record kind `role-edge`, [[STR-005]])

| Field | Type | Resolution rule |
|-------|------|-----------------|
| `parent` | executor identity | The parent's own dispatch label; for a root: status-spine `run_id`, else line-registry `line_id`, else the owner-declared fallback literal `root` (FR-003) |
| `child` | dispatch label | Existing label forms: team/dispatch convention, `run-agent` label, driver stage `<line_id>-<stage>` |
| `attempt` | string | Existing dispatch-attempt / iteration identifier; a retry is a new attempt, never an overwrite (FR-013) |
| `role_declaration` | `subagent` \| `superagent` | Declared role claim for this edge's child: `subagent` (the edge-relative role) or `superagent` (an explicit superagent assertion, judged by `unbacked-role-claim` in § 5); `dual-role` is never a declaration value |
| `dispatch_duty` | `granted` \| `not-granted` | Declared grant fact, independent of the role claim: `granted` iff the dispatch granted dispatch duty (the payload carried the [[STR-003]] role-transition injection); projected as an engine output key (contract C-3). Never derived from `role_declaration`, never a superagent claim |
| `depth` | integer ≥ 0 | Computed: shortest edge distance from a root; roots are depth 0 |
| `source` | `{carrier, path, line}` | Primary carrier of the record; `carrier` ∈ `team-report` \| `driver-spine` \| `run-agent-label` |
| `conflicts` | list of `{field, paths[2+], edge}` | Same field disagreeing between two carriers; both paths named; emitted as a top-level `conflicts` row carrying the edge identity (`parent` / `child` / `attempt`); never a silent pick (FR-003) |

Invariants: one dispatch produces exactly one edge; `parent == child` (after identity resolution) is `self-dispatch`; an unresolvable `parent` is `dangling-parent`.

### 2.1 Carrier row shapes (the only forms the engine parses)

**(a) Team run report — dispatch mapping table** inside `## Execution Detail` of `.specify/teams/<slug>/runs/<stamp>-report.md` (owner of the report contract: `skills/internal/create-team/SKILL.md` § Report contract):

```markdown
| label | role | dispatch_duty | workspace | parent |
|-------|------|---------------|-----------|--------|
| <dispatch-label> | subagent \| superagent | granted \| not-granted | <workspace path> | <parent identity> |
```

A row declaring `role = superagent` for an executor is an **explicit superagent assertion**: legal only while the engine finds ≥1 edge that executor parents; otherwise it is `unbacked-role-claim` (§ 5). Declared-role values are exactly `subagent` / `superagent`, so a `superagent` claim is known-domain input (never a malformed record); the grant is recorded separately in `dispatch_duty`, and `dual-role` never appears in either column.

**(b) Driver stage envelope sidecar** — `prompt-<line_id>-<stage>.md.meta.json` under the driver's state directory gains a `role_edge` object carrying the seven downlink fields (below). The engine also derives the edge from the existing four-piece artifact set (`pid-` / `status-` / `log-` / `heartbeat-<line_id>-<stage>`) when the sidecar is absent: child = `<line_id>-<stage>`, parent = spine `run_id`.

**(c) `run-agent` dispatch record** — the existing `exec-quant.py --action collect-dispatch` record pairs the dispatching unit (`unit_id`) with the child label (`run_id`). Identity resolution maps `unit_id` per § 3; the artifact triplet `<label>.status` confirms child existence.

## 3. Executor identity resolution (deterministic order)

1. Exact match against a known **child dispatch label** → that executor.
2. Exact match against a **line id** (line-registry entry `line_id`) → that line's executor.
3. Exact match against a **status-spine `run_id`** → that root executor.
4. The literal `root` → the root marker declared by the owner page.
5. No match → the referencing edge is `dangling-parent`, naming the unresolvable identity and the carrier path.

## 4. Executor node

| Field | Type | Source |
|-------|------|--------|
| `id` | string | Identity resolution above |
| `parent` | string \| null | Its incoming edge's parent (roots: null) |
| `roles` | set | Derived: `superagent` iff it parents ≥1 edge; `subagent` iff it is a child on ≥1 edge |
| `depth` | integer \| null | Shortest distance from a root; `null` when a cycle makes it unresolvable |
| `sources` | list of `{carrier, path, line}` | Carriers where this executor was observed (union over its edge records); an engine output key (contract C-3) |
| `state` / `last_activity` / `age` / `stale` | enum / timestamp / duration / boolean | **Digest-view fields, not engine output keys**: the engine emits `id` / `parent` / `roles` / `depth` / `sources`; the digest renders these from its existing sources (artifact triplet `.status`, spine stage verdict, report outcome, watch model) |

## 5. Violation (closed four-kind set)

| Kind | Predicate | Requirement |
|------|-----------|-------------|
| `self-dispatch` | resolved `parent == child` | FR-002, SC-001 |
| `dangling-parent` | parent identity unresolvable (§3 rule 5) | FR-005, FR-006, SC-001 |
| `unbacked-role-claim` | an executor carries an **explicit recorded `superagent` role assertion** (a carrier's declared-role field taking the value `superagent` — a mapping row or a `role_edge` declaration) while the judgement finds no edge where it is the parent. `superagent` is a legal declared-role value, so this kind is reachable and is the **single** classification for such a row (never a C-9 malformed record). A `dispatch_duty: granted` declaration marks granted dispatch duty, is **not** a superagent claim, and never triggers this kind — granted-but-not-yet-dispatched stays legal; the `dual-role` set marker is output-side and appears in no carrier declaration | FR-005, SC-001 |
| `depth-inconsistent` | a recorded `depth_position` disagrees with the computed depth, or the graph contains a cycle making depth unresolvable | FR-004, FR-005 (operationalizes "深度越界"; see plan D-6) |

Not violations here (owners elsewhere, referenced only): SDD license-chain depth 2, one-run-per-member, virtual cannot host (`subagent-definitions.md` § Dispatch-Time Governance Obligation); authorization refusals (`sdd-route.py --action authorize`); stale-attempt consumption (attribution values owned by `watch-model.md`).

## 6. Downlink role fields (FR-008, seven fields)

| Field | Content |
|-------|---------|
| `parent_identity` | The dispatching executor's identity (§3 resolution domain) |
| `child_label` | This dispatch's label |
| `role_declaration` | `subagent` \| `superagent` for this edge (`superagent` is the explicit assertion judged by § 5; `dual-role` is never a declaration value) |
| `dispatch_duty` | `granted` \| `not-granted` — the grant fact, declared independently of the role claim |
| `depth_position` | The child's declared depth (integer) |
| `authority_ref` | Pointer to the authorization basis (`sdd-route.py --action authorize` record, team territory, or `none`) |
| `return_channel` | The declared return path (structured return + evidence pointer channel) |

The four pre-existing injections (fast-fail clause, concurrency obligation, reporting duty, re-anchoring anchor digest) continue to travel **by pointer to their owners**; this model adds the seven fields and restates none of those rules.

## 7. Role-transition injection ([[STR-003]]) — closed nine-item list

Record marker: the literal `role-transition` present in the dispatch payload. The **content** of the nine items (what each points at) is owned by the owner page and by FR-017 items (a)–(i); this model fixes only the **item-id slugs** the payload self-check matches and the tests assert — the slugs are the machine handles, not a second definition of the list:

`role-activation-scope` · `self-identity-parent-edge` · `downward-obligation-checklist` · `concurrency-budget-ref` · `reporting-path` · `state-carriers-writer-boundary` · `attention-classes-escalation` · `depth-remaining-prohibitions` · `aggregate-return-contract`

The nine-item list is closed (FR-017); each item is carried as a pointer to its owner, never as rule text. The red lines that bound the payload (no skill-load instruction, no driver-skill reference, no loop logic, no full driver manual) are owned by FR-017 and `subagent-definitions.md` § Dispatch-Time Governance Obligation — referenced here, not restated.

## 8. In-edge message classes (closed set)

The closed class set is declared once by the owner page (FR-010); this model consumes the four machine tokens `ack` · `answer` · `result` · `attention-escalation`, which the guarding test pins against the owner page. Unclassified "progress" MUST NOT travel up an edge; activity is carried by the existing liveness carriers. This closes no new channel.

## 9. Edge lifecycle

`open` (edge recorded) → `completed` \| `failed` \| `cancelled` (written into the edge's existing carrier, making the parent's judgement possible). Silent orphaning is a defect (FR-015); cancel/terminate follow existing confirmation gates (no new gate). Retries are new attempts with new labels; stale-attempt returns are not consumable (FR-013).

## 10. State derivation (three fact layers, FR-026)

| Layer | Carrier | Used for |
|-------|---------|----------|
| State layer | status spine / line-registry entry | Identity, run/line ids, stage verdicts |
| Assignment layer | artifact triplet `.status`, return record, run report | Edge state, attempt, result presence |
| Host-event layer | watch model pid/heartbeat/liveness | Liveness, stale marking, interrupted/attention |

No derivation from conversation memory, child session transcripts or process scans (SC-005 structural assertion). Recovery rebuilds edges from these three layers and marks still-running children `interrupted` / `attention` (FR-027, FR-028).
