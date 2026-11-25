# Data Model — 107-decision-governance

**Feature**: 107-decision-governance → Feature 107 Decision Governance（AI Agent 决策项治理）
**Owner of every field's value domain named below**: `shared/definitions/decision-definitions.md` (the new owner page). This file is the plan-stage design projection; it MUST NOT become a second definition point. Where a value domain is owned by an adjacent owner, the row points at that owner and does not restate it.

## Entities

### E1 — Decision Item（决策项）

A single presented-or-held choice.

| Field | Type | Value domain | Owner |
|-------|------|--------------|-------|
| `subject` | text | full name of the object being decided (the record heading carries it) | owner page (text contract) |
| `decision_class` | enum | `human-interactive` / `ai-autonomous` (closed) | owner page |
| `context` | text | situation and constraints; content floor owned by the owner page | owner page |
| `options` | Option[] | closed set, ≥1 member or the `forced` declaration (E3) | owner page |
| `same_name_conflict` | bool | `true` / `false`; required where same-name risk exists | owner page (conditional field) |
| `resource_locator` | structured text | machine-parseable named dimensions; floor = business resource group + region id | owner page (conditional field) |
| `held_by` | identity | the holder (person or agent run identity) | `superagent-definitions.md` (edge/run identity) + owner page |

### E2 — Decision Record（决策记录）

The archive projection of one decision item in its producer's existing carrier. One decision item at completion ⇒ exactly one record (FR-014, [[STR-001]] owner).

| Field | Type | Value domain | Owner |
|-------|------|--------------|-------|
| `decision_id` | id | `D-NNN` (three digits); dense per carrier; never reused; registered | owner page (form) / `.specify/register.md` (registration) |
| `decision_class` | enum | `human-interactive` / `ai-autonomous` | owner page |
| `context` | text | content floor on the owner page | owner page |
| `options` | Option[] | see E3; closed set | owner page |
| `chosen_option` | option label | must be one named member of `options` | owner page |
| `rationale` | text / reference | general: text; load-bearing: `T-NNN` cross-reference, six fields NOT copied | owner page (general) / `decision-tension.md` (load-bearing six fields) |
| `evidence` | pointer[] | every pointer resolvable from the repository (or the carrier) | owner page |
| `actor` | identity | who held / implemented; identity form owned by `superagent-definitions.md` | `superagent-definitions.md` + run identity |
| `created_at` | timestamp | ISO-8601 UTC; mandatory value | owner page |
| `dispatched_at` | timestamp / literal | ISO-8601 UTC or `not-yet`; line presence mandatory | owner page |
| `acknowledged_at` | timestamp / literal | ISO-8601 UTC or `not-yet` | owner page |
| `implemented_at` | timestamp / literal | ISO-8601 UTC or `not-yet` | owner page |
| `transmission_status` | enum | see E9 state domain; carries the implementation-result dimension per the clarify ruling (not an 11th field) | owner page |
| `superseded_by` | id / conditional | `D-NNN` of the replacing record; required when superseded | owner page (conditional field) |

**Field-closure reading (authoritative)**: FR-014's ten fields are the mandatory closed set. `same_name_conflict`, `resource_locator` and `superseded_by` are conditional fields declared by the owner page and required exactly when their trigger holds (FR-007, A-6). No other field is admitted without revising the owner page.

**Serialization grammar**: a level-3 heading `### D-NNN — <one-line title>` carries the id once; each field is one line `- **<field>**: <value>`; options are indented sub-lines under `options`; continuations indent ≥2 spaces; fenced code blocks inside the carrier do not count (same rule as the tension grammar). Chosen in T-002.

### E3 — Option（选项）

| Field | Type | Value domain | Owner |
|-------|------|--------------|-------|
| `label` | text | full name (same full-name/locator rules as the subject) | owner page |
| `consequences` | text | for human-interactive: plain language; for ai-autonomous: formal predicate consequence | owner page (per-class template) |
| `reversibility` | text | reversible / irreversible with the condition | owner page |
| `default` | bool | exactly one member may be `default: yes` | owner page |
| `evidence` | pointer / text | the evidence selecting this option | owner page |
| `path` | text / conditional | required for the `other` option: who/when/how adds options and writes back | owner page |

Closed-set rules: no empty set; no duplicate labels; `other` without `path` is invalid; a single viable option requires the decision item's `forced` declaration with a reason; a decision with zero viable options is not a decision item (edge case).

### E4 — Decision Block（决策块，payload）

| Field | Type | Value domain | Owner |
|-------|------|--------------|-------|
| `decision_id` | id | `D-NNN` resolving to a record | owner page |
| `decision_class` | enum | closed | owner page |
| `chosen_option` | text | full label of the recorded choice | owner page |
| `implementation_constraints` | list | constraints the child must honor | owner page |
| `archive_pointer` | pointer | carrier path + heading anchor of the record | owner page |

Carried inside the existing dispatch payload; the seven role fields and the four injections keep their owners (`superagent-definitions.md`) and are unchanged (A-7). `decision_class` is copied from the source record unchanged — a human-held decision delegated for implementation stays `human-interactive`; transmission never re-classes a decision (A-4, P-09, FR-018).

### E5 — Acknowledgement（确认）

A child return item: echoes the `decision_id` and states that the block was accepted and will be implemented (or the anomaly escalation). It is part of the return, not a new message channel; message classes stay owned by `superagent-definitions.md`.

### E6 — Implementation Receipt（实施回执）

| Field | Type | Value domain | Owner |
|-------|------|--------------|-------|
| `decision_id` | id | must resolve; same id as the block | owner page |
| `implementation_summary` | text | what was done | owner page |
| `evidence` | pointer[] | resolvable implementation evidence | owner page |
| `divergence` | enum + reason | `none` / `diverged` + reason | owner page |

Receipt presence updates the record's `transmission_status` (implementation-result dimension). A receipt is not a second decision record: the decision item keeps exactly one record (I-01), and the receipt updates that record's state and the audit chain (FR-014, FR-019). Missing any item ⇒ the return is incomplete; the parent MUST NOT consume or backfill (existing uplink rule).

### E7 — Decision Producer（决策生产者）

A closed-inventory row: `producer_id` (`P-NN`), producer name, existing carrier, obligation (`record` / `record-when-decision` / `exempt`), class (by holder; may be "by holder" where both occur), fact owner. The normative table lives on the owner page; the requirements spec's table is the dated requirements-stage declaration. Expansion is a revision of the owner page/inventory, never a silent addition.

### E8 — Archive Projection（决策档案）

Not a store: the union of `{producer × existing carrier}` plus the register index. Properties: every closed-inventory producer maps to exactly one carrier; an id resolves to (carrier, heading); a decision is reconstructable from carriers + register alone; no conversation memory may fill a gap.

### E9 — Decision Class（决策类别）与 state domain

- Class closed set: `human-interactive` (held by a person) | `ai-autonomous` (held by an agent with no user present). Judged by holder, not by surface medium (A-4). Class selection correctness is a behavior rule (B-06), never machine-claimed.
- `transmission_status` closed domain (the record's transmission/implementation state): `not-transmitted` · `dispatched` · `acknowledged` · `implemented` · `diverged` · `blocked`. Transitions are append-only in the record's own lines: `not-transmitted → dispatched → acknowledged → implemented`; from `acknowledged` or later, `blocked` is legal when the child stops on an invalidated decision (fast-fail escalation); `diverged` is legal only with a receipt whose `divergence` is `diverged`. Backward transitions are not legal; a re-decision is a new record that supersedes the old one.

## Invariants

| ID | Invariant | Rule source |
|----|-----------|-------------|
| I-01 | One decision item at completion yields exactly one record in its producer's carrier; a record without a producer is a defect | FR-014, FR-003 |
| I-02 | `decision_id` matches `D-NNN`, is dense and unique within one carrier; cross-carrier references carry the carrier pointer; ids are never reused | FR-015, A-6 |
| I-03 | Every mandatory field (E2 ten) is present; conditional fields are present exactly when their trigger holds | FR-014, FR-007 |
| I-04 | `chosen_option` is a named member of `options`; `options` is non-empty; labels are unique; `other` carries a `path`; a single option carries `forced` + reason | FR-012, FR-013 |
| I-05 | Every evidence pointer resolves; a broken pointer is a defect (no memory backfill) | FR-016 |
| I-06 | A load-bearing decision's record cross-references its `T-NNN` and does not copy the six tension fields | FR-017 |
| I-07 | A human-interactive record carries the human choice signal in the existing signal vocabulary (pointer: `confirmation-gates.md`) | FR-013, A-4 |
| I-08 | An ai-autonomous record's chosen option is deterministically replayable from the recorded inputs + decision predicate | FR-013, M-… replay |
| I-09 | A decision block carries all five fields; a decision-backed dispatch without one is refused | FR-018, M-06 |
| I-10 | A receipt carries all four fields; a missing item makes the return incomplete and the parent must not consume it | FR-019, M-05 |
| I-11 | The audit chain record → dispatch attempt → receipt is fully resolvable; a broken link is an explicit anomaly | FR-021, M-07 |
| I-12 | Supersession preserves the old record and receipt; the old record gains `superseded_by`; nothing is deleted or rewritten | A-6, edge case |
| I-13 | Legacy records (pre-existing `### D-…` headings without the record field grammar; register rows that are not a new-form record's birth registration — including the id-shaped `D-001` row) are readable, reported `legacy`, never rewritten, never judged. New form = `^### D-\d{3}` heading **with** the field grammar; the id shape alone never qualifies | FR-028, A-10, C-206 |
| I-14 | No record, block, receipt or inventory lives outside the existing carriers + register; no second store exists | FR-004, A-3 |

## Relationships

```text
Decision Producer (E7) 1 ─── * Decision Item (E1)
Decision Item (E1)     1 ─── 1 Decision Record (E2)   [projection into the producer's carrier]
Decision Item (E1)     1 ─── 1..* Option (E3)
Decision Record (E2)   1 ─── 0..1 Decision Block (E4)  [when implementation is delegated]
Decision Block (E4)    1 ─── 1 Acknowledgement (E5)
Decision Block (E4)    1 ─── 1 Implementation Receipt (E6)
Decision Record (E2)   * ─── 1 Archive Projection (E8)  [carrier + register index]
Access policy: read E2/E8 only; write E2 at its carrier, E4/E5/E6 at the dispatch/return carriers.
```
