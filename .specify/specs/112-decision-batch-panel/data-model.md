# Data Model — Batch Decision Panel（批量决策面板）

**Feature**: 112-decision-batch-panel → Feature 112 Batch Decision Panel（批量决策面板）
**Owner boundary**: the runtime rules this model projects are owned by `shared/definitions/decision-definitions.md` (extended by this feature). This file is the design projection used by the plan and the guards; it does not become a second owner.

## 1. Entity inventory

| ID | Entity | One-line meaning | Source of truth |
|----|--------|------------------|-----------------|
| E-1 | Pending Source（待决策项来源） | One row of the closed two-source roster, with its candidate predicate and presence reading | Owner page § 待决策项来源清单 |
| E-2 | Source Candidate（来源候选） | A machine-found candidate produced by a source predicate, before any qualification | This model + owner § 候选与资格分层 |
| E-3 | Pending Item Block（待决策项块） | The `### PENDING —` block that carries a pending decision item; not a decision record | Owner page § 待决策项块 |
| E-4 | Source Reference（来源引用） | An address `(source id, carrier path, locator, position)` that points at one candidate | This model |
| E-5 | Pending Decision Item（待决策项） | One presented row of the batch: identity, sources, slots, qualification, grounding, disposal | Owner page § 批次呈现契约 |
| E-6 | Option（选项） | A member of the item's closed option set with the five elements | 107 owner § 选项集契约 |
| E-7 | Recommended Default & Grounding（建议默认值与依据） | The declared default label plus the closed-status grounding result and its resolvable pointers | Owner page § 建议默认值与依据 |
| E-8 | Decision Batch（决策批次） | One scan—present—reply—record session with its id, authorization, reply and digest | Owner page § 决策批次 |
| E-9 | Batch Record（批次记录） | The dated knowledge entry that carries the batch head, item rows, decision records and closing | Owner page § 批次记录 |
| E-10 | Batch Item Row（批次项行） | One row of the batch record's item table | Owner page § 批次记录 |
| E-11 | Batch Disposition（批次处置） | The closed disposition value of one item in one batch | Owner page § 批次处置 |
| E-12 | Batch-Family Record Fields（批次族记录字段） | The three conditional fields a batch-produced 107 record carries | 107 owner § 分层封闭（批次族，本特性加法） |
| E-13 | Completeness Bookkeeping（完备性记账） | The per-source counts, classification partition, absence list and completeness verdict | Owner page § 完备性与拒绝 |

### E-1 Pending Source

| Field | Type | Rule |
|-------|------|------|
| `source_id` | enum | `register-open-decision-row` \| `authored-pending-item` — closed; growth only by owner revision |
| `carrier` | path | `.specify/register.md` for S1; the four closed roots for S2 (`.specify/specs/`, `.specify/goals/`, `.specify/anchoring/`, `.specify/teams/`) |
| `predicate` | text | Machine-checkable candidate-existence predicate (below) |
| `presence` | enum | `read` \| `absent` \| `unreadable` — carrier-level only |

- S1 predicate: a row whose id cell, after de-emphasis, starts `OI-` or `D-`, and whose status cell, after de-emphasis and leading-space trim, starts with the word `open` (word boundary; `resolved-for-v1` and similar are not `open`).
- S2 predicate: a `### PENDING —` block outside fenced code under one of the four roots.

### E-2 Source Candidate

| Field | Type | Rule |
|-------|------|------|
| `candidate_id` | stable string | Deterministic address of the candidate (source id + carrier + locator) |
| `source_id` | enum | E-1's id |
| `carrier` | repo-relative path | Where it was found |
| `locator` | string | Register row id, or block heading occurrence |
| `position` | integer | Row order for S1; block start line for S2 |
| `block` | E-3 | Present iff the carrier resolves a block for this candidate |

Candidacy is existence only. Field completeness, block-level grammar defects and class judgement are **qualification** (E-5) or a named exclusion — never candidacy conditions (A-21).

### E-3 Pending Item Block

Grammar: heading `### PENDING — <full subject name>`; field lines `- **<lowercase field>**: <value>`; continuation lines indent ≥ 2 spaces. Field set (closed):

| Field | Level | Content |
|-------|-------|---------|
| `decision_class` | required | `human-interactive` \| `ai-autonomous`; missing → qualification `incomplete` (`class-missing`) |
| `subject` | required | Full name of the decision subject (107 R1) |
| `same_name_conflict` / `resource_locator` | conditional (same-name family) | Required together when a same-name conflict is possible |
| `context` | required | Situation and constraints |
| `options` | required | Declared count + option entries (five elements each, exactly one `default: yes`; `other` needs `path`; single viable option declares `forced`) |
| `basis` | required | One-line reason for the recommended default; never evidence |
| `origin` | required | Producer identity; for S1 it MUST contain the register row id verbatim as an independent token |
| `created_at` | required | ISO-8601 UTC |
| `resolution` | conditional (resolution family) | Appended after settlement: `<batch_id> -> <D-NNN>`; block content otherwise unchanged |

Block-level grammar defects (unknown field, duplicate field, malformed field line, declared count ≠ entry count) make the candidate `incomplete` with named defects; they never trigger a batch refusal and are never silently ignored. A pending block is not a decision record; the record grammar does not judge it, and it does not judge records (`### D-NNN` — different heading).

### E-4 Source Reference

`{source_id, carrier, locator, position}` with the same byte-literal semantics as identity. The set of references on one presented row is ordered by roster order → carrier path → position. Reference totality: every candidate appears exactly once as a reference — either on a presented row (primary or merged) or in the named-exclusion accounting.

### E-5 Pending Decision Item（presented row）

| Slot | Rule |
|------|------|
| `identity` | `subject` (trimmed, byte-equal) + `resource_locator` when the same-name family applies; never case-folded, never Unicode-normalised |
| `sources` | E-4 set (all references for this identity) |
| `decision_class` | From the block; a row exists only for class `human-interactive` or unknown-class `incomplete` |
| `context` | From the block; missing → `incomplete` (`missing-field`) with the slot shown empty and named |
| `options` | From the block; each option's five elements |
| `recommended_default` | The single declared default label; zero or multiple → `no-default` |
| `basis` | From the block; text only |
| `grounding` | E-7 |
| `qualification` | One state + named reasons (state domain 3) |
| `objection_instructions` | How to object or park for this item (batch context floor) |
| `disposition` | E-11 or absent (pending / ineligible) |
| `decision_id` | Present iff a decision record was produced |

### E-7 Recommended Default & Grounding

| Field | Type | Rule |
|-------|------|------|
| `default_label` | string | Exactly the declared default member's label; never invented |
| `status` | enum | `grounded` \| `no-evidence` (state domain 5) |
| `pointers` | list of resolvable pointers | Non-empty iff `grounded`; each entry is a path (plus anchor when given) in the closed prior-experience carrier set |
| `basis` | text | Copied from the block; never counted as evidence |

Grounding join (deterministic, no semantic search): (a) the default option's `evidence` pointers that resolve to a prior-experience carrier; (b) prior decision records whose `context` contains the subject string verbatim; (c) the `T-NNN` ids those records cite. Prior-experience carriers: decision-record carriers under the four scan roots, batch records in the knowledge store, `T-NNN` tension records, `.specify/history/` entries, `.specify/feedback/` entries, `.specify/knowledge/` entries. At least one resolvable pointer → `grounded`; otherwise `no-evidence`.

### E-8 Decision Batch

| Field | Type | Rule |
|-------|------|------|
| `batch_id` | `B-<YYYYMMDDTHHMMSSZ>-<8 lowercase hex>` | Minted only after every record precondition passes, before the first write |
| `scan_time` | ISO-8601 UTC | The only non-deterministic scan field |
| `authorization` | enum | `interactive` \| `unattended`; declared by the caller; missing → treated as unattended |
| `presentation_digest` | string | Deterministic digest over the presentation (excluding `scan_time`) |
| `reply_verbatim` | text | The user's explicit reply, preserved verbatim in the batch record |
| `items` | list of E-5 | The scan result |
| `bookkeeping` | E-13 | Per-source counts and the partition |

### E-9 Batch Record

One dated entry in `.specify/knowledge/`, written through the memory engine; recognised by the title prefix `decision-batch-<batch_id>`; never overwritten (a same-batch-id second write is refused before the write surface is called) — the sole exception to whole-file immutability is the I-16 `superseded_by` append (append-only; every pre-existing byte unchanged). A later batch reads a settled batch record only for the declared read-only purposes (already-resolved exclusion, grounding, prior-decision conflict, replay pointer resolution) and never writes another batch's record except through that single append.

| Section | Content |
|---------|---------|
| Frontmatter | Memory-engine fields (`id`, `scope=knowledge`, `source=/speckit.decide`, `tags` incl. `decision-batch`, `title`, `created`, `session_id`, `summary`) |
| Batch head | `batch_id`, scan time, tool version, source roster with presence + per-source candidate counts, completeness verdict (partition + absences), authorization, `reply_verbatim` in a blockquote |
| Item rows | E-10 table, one row per presented item |
| Decision records | One `### D-NNN — <subject>` block per settled item in the 107 grammar + E-12 fields |
| Closing | Items left pending with named reasons, source-update outcomes and disclosures |

### E-10 Batch Item Row

| Column | Content |
|--------|---------|
| Identity | `subject` + locator (when applicable) |
| Sources | E-4 reference set (compact) |
| Qualification | State + named reasons |
| Grounding | `grounded` / `no-evidence` + pointers (compact) |
| Recommended default | The default label |
| Disposition | E-11 or `pending` |
| Decision | `D-NNN` or `—` |

### E-11 Batch Disposition

Closed set: `accepted-default` \| `objected-alternative` \| `objected-parked`. Parked produces no decision record; the item stays pending and the row remains in the record. The human choice signal is derived by the owner-declared mapping (`accepted-default`→`approved-as-is`, `objected-alternative`→`modified`); parked emits none; no second signal vocabulary.

### E-12 Batch-Family Record Fields

| Field | Domain | Trigger |
|-------|--------|---------|
| `batch_id` | `B-…` shape, resolvable to a batch record carrier | Record produced by a batch |
| `batch_disposition` | `accepted-default` \| `objected-alternative` | Same |
| `recommendation_grounding` | `grounded` \| `no-evidence` | Same |

All three appear together or none; they join the 107 conditional layer (no parallel schema). The choice signal is not written into `chosen_option` (its value stays the exact member label).

### E-13 Completeness Bookkeeping

| Field | Content |
|-------|---------|
| `sources[]` | Per source: `source_id`, `presence`, candidate count, absence reason if any |
| `partition` | `presented_rows` + `duplicate_merged` + `not_human_held` + `already_resolved` |
| `identity` | `candidates = presented_rows + duplicate_merged + named_exclusions` (allowed delta empty) |
| `reference_total` | Sum of per-row reference counts = `presented candidates + duplicate_merged candidates` |
| `verdict` | `complete` (with absences listed) — or no verdict at all because the batch was refused |

## 2. State domains

**State domain 1 — source presence**: `read` · `absent` · `unreadable`. `unreadable` refuses the batch; `absent` is a named empty source that keeps the batch complete-with-disclosure.

**State domain 2 — candidate classification** (exactly one per candidate): `presented` · `duplicate-merged` · `not-human-held` · `already-resolved`.

**State domain 3 — presentation qualification** (exactly one per presented row; precedence left to right): `incomplete` → `source-conflict` → `no-default` → `irreversible-default` → `prior-decision-conflict` → `eligible`. `incomplete` reasons are a closed named set: `authority-unresolved`, `ambiguous-link`, `class-missing`, `malformed-field`, `unknown-field`, `duplicate-field`, `option-count-mismatch`, `missing-field`, `option-element-missing`, `evidence-unresolvable`.

**State domain 4 — disposition** (one per settled row): `accepted-default` · `objected-alternative` · `objected-parked`; `pending` is the absence of a disposition, not a fourth value.

**State domain 5 — grounding**: `grounded` · `no-evidence`.

## 3. Relationships

```text
Pending Source (E-1) 1 ─── N Source Candidate (E-2)
Source Candidate (E-2) N ─── 1 Pending Item Block (E-3)   (when resolvable)
Source Candidate (E-2) 1 ─── 0..1 Source Reference (E-4)
Source Reference (E-4) N ─── 1 Pending Decision Item (E-5)  (all refs of one identity)
Pending Decision Item (E-5) 1 ─── 1 Recommended Default & Grounding (E-7)
Pending Decision Item (E-5) 1 ─── 0..1 Option set (E-6)     (from the block)
Decision Batch (E-8) 1 ─── 1 Batch Record (E-9)
Batch Record (E-9) 1 ─── N Batch Item Row (E-10)
Batch Item Row (E-10) 0..1 ─── 1 Batch Disposition (E-11)
Settled item 1 ─── 1 Decision Record (107 `### D-NNN` block inside E-9) + E-12 fields
Decision Batch (E-8) 1 ─── 1 Completeness Bookkeeping (E-13)
```

## 4. Operations as state transitions

- **scan** (read-only): sources → candidates → classification/qualification → E-8 presentation payload (items + bookkeeping + digest). Refuses on `unreadable`; `nothing-pending` is a successful terminal state with no batch.
- **record**: re-scan → compare identity set + per-item content fingerprints against the presented payload (drift → refuse, zero writes, no id) → validate the reply (structure + membership; refusal leaves the presentation valid for retry) → mint `batch_id` → write batch record → append `superseded_by` to each overturned prior record (the sole sanctioned post-write mutation when that record sits inside a prior batch record; an unreadable/unwritable prior carrier refuses that item) → register rows/status cells → block `resolution` annotations → disclose any post-write failure.
- **replay** (read-only): batch record + resolvable pointers → item set, completeness, defaults/grounding, objections/dispositions, decision records; any unresolvable pointer is reported and the exit is non-zero; no skipping, no memory completion.

## 5. Invariants

| ID | Invariant |
|----|-----------|
| I-1 | The source roster is exactly the two ids of E-1; a third source never appears without an owner-page revision |
| I-2 | Candidacy is decided by the machine-checkable predicates alone; qualification never removes a candidate from enumeration |
| I-3 | Every candidate is classified exactly once (state domain 2); the partition sums to the candidate count |
| I-4 | The completeness claim's comparison unit is the per-candidate classification, referent = this scan, allowed delta = empty |
| I-5 | A present-but-unreadable carrier refuses the whole batch; no partial presentation and no record |
| I-6 | An absent carrier is a named empty source; it neither refuses the batch nor reads as "clean" |
| I-7 | Zero candidates yields `nothing-pending` with exit success and no batch record |
| I-8 | Identity comparison is byte-equal on the trimmed subject (plus locator in the same-name family); no case folding, Unicode normalisation or fuzzy matching |
| I-9 | A register row links to a block only through its explicit repository-relative path and an `origin` token naming that row; `同上`-style text is not a path |
| I-10 | A presentable row carries every slot of the 107 `human-interactive` template, the source pointers, class, basis, grounding, qualification and objection instructions; a missing slot is shown empty and named, never fabricated |
| I-11 | Only `eligible` rows can be settled by silence; the eligibility conjunction is class `human-interactive`, block complete, exactly one default, default reversible, no source conflict, no prior-decision conflict, not previously resolved |
| I-12 | Silence never settles an item absent a completed interactive batch with an explicit user reply; an abort or a follow-up-only conversation writes nothing |
| I-13 | The recommended default is the item's declared default; the panel never invents a default or an option |
| I-14 | `grounded` carries at least one resolvable prior-experience pointer; `no-evidence` is explicit; `basis` is never evidence |
| I-15 | Prior-decision conflict is detected by verbatim subject containment in a prior record's `context` and a different prior chosen option; such a row is never settled by silence |
| I-16 | Redecision adds a new record and appends `superseded_by` (with the carrier pointer) to the old record; the old content is never rewritten — every pre-existing byte stays unchanged; when the old record sits inside a batch record, this append is that batch record's sole sanctioned post-write mutation (the I-18 exception); an unwritable/unreadable old carrier refuses the redecision |
| I-17 | The three batch-family fields appear together on batch-produced records only, with values from their domains; existing records are untouched and keep passing |
| I-18 | The batch record is one file per batch, never overwritten; the same batch id is refused before the write surface runs; the sole exception to whole-file immutability is the I-16 `superseded_by` append (append-only, no other byte changes) |
| I-19 | `record` refuses on any candidate-set or per-item content drift between presentation and write, with zero writes and no minted id |
| I-20 | Register updates are limited to appended rows and status cells; settled rows are never deleted; parked rows stay `open`-prefixed and annotated |
| I-21 | Replay reconstructs the batch from the record and resolvable pointers only; any unresolvable pointer is reported with a non-zero exit |
| I-22 | No second store, schema, registry, network call, feedback-store write or automatic transmission exists in the mechanism |

## 6. The batch record layout (worker view)

```text
---
id: decision-batch-b-20261127t120000z-1a2b3c4d
scope: knowledge
source: /speckit.decide
feature: ""
tags: [decision-batch, b-20261127t120000z-1a2b3c4d]
title: decision-batch-B-20261127T120000Z-1a2b3c4d
created: 2026-11-27T12:00:00Z
...
---

# 决策批次记录 B-20261127T120000Z-1a2b3c4d

## 批次头
- batch_id / 扫描时点 / 工具版本
- 来源清单与逐来源候选计数（含缺席来源与原因）
- 完备性判定：分区恒等式成立、允许差集为空
- 授权级别与用户应答原文（逐字引用块）

## 逐项行表
| 主体 | 来源 | 资格 | 接地 | 建议默认 | 处置 | 决策 |
...

## 决策记录
### D-001 — <subject>
- **decision_class**: human-interactive
- **context**: ...
- **options**: <N> ...
- **chosen_option**: <exact label>
- **rationale**: <basis + reply key points>
- **evidence**: <grounding pointers>; <source item pointer>; <batch record pointer>
- **actor**: ...
- **created_at**: ...
- **transmission_status**: not-transmitted
- **batch_id**: B-...
- **batch_disposition**: accepted-default | objected-alternative
- **recommendation_grounding**: grounded | no-evidence

## 收尾
- 保持待定的项与具名原因
- 来源更新结果与披露
```

The layout is illustrative for guards and tasks; the normative field rules live in the extended owner page, and the record blocks are the ones `validate-decisions.py` judges.