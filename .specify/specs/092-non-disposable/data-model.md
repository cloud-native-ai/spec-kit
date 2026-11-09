# Data Model — Non-Disposable

**Feature**: 092-non-disposable | **Date**: 2026-11-09 | **Plan**: [`plan.md`](plan.md) § Phase 1

This file owns the **shapes**: the entities, their fields, the entry state machine, the expiry model, and the
reader-facing output shape. It does **not** own a rule: the detection categories, the disposition set, the
disposition bridge, the review-surface definition, the supersede protocol and the renumber predicate face are owned
by `shared/definitions/non-disposable-definitions.md` (the owner page, FR-001); their machine-readable members are
owned by `shared/declarations/facts/*.yaml` where a fact exists; a field's closed value domain is stated here **only
when no other owner states it**, and then this file says so.

## E-1 NonDisposableEntry — the review finding

The unit a review produces and a disposition closes. **Owns**: the field set. **Does not own**: the members of
`category` (owner page § Detection Categories), of `disposition` (owner page § Disposition Set), of `detection`
(owner page § Detection Subject), of `state` (this file, § Entry State Machine).

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `entry_id` | string | yes | stable across re-reviews: `<category>/<normalised path>:<line>`; two entries with the same id are the same defect seen twice and MUST be merged, never appended |
| `category` | enum | yes | a member of the owner page's closed detection-category set |
| `detection` | enum `deterministic` \| `semantic` | yes | the assertion's subject, not the tool that happened to find it (owner page § Detection Subject); a `semantic` entry MUST also carry `evidence_refs` with ≥ 2 resolutions |
| `path` | repo-relative path | yes | the carrier; normalised per `declaration_reader.normalize_path` (one optional leading `.specify/` stripped) |
| `line` | integer | yes | 1-based; `0` is reserved for "the whole file" (a missing machine-readable block is a file-level fact, not a line fact) |
| `evidence_refs` | list of `{path, line, quote?}` | yes (≥1) | the readings that make the entry independently re-checkable; a `semantic` entry needs ≥ 2 |
| `severity` | enum `high` \| `medium` \| `low` | yes | carried from the corpus where the entry comes from one; otherwise the owner page's per-category default |
| `state` | enum | yes | § Entry State Machine |
| `disposition` | enum or null | required when `state` = `disposed` | a member of the owner page's closed disposition set; empty/`null`/a free-text value is a finding (FR-009) |
| `disposition_evidence` | path | required when `state` = `disposed` | the repair-lane evidence file that records this disposal (§ E-7) |
| `exemption` | object or null | required when `disposition` = `exempt` | § E-3 |
| `source_entry` | string or null | no | the corpus id (`A1`…`H3`) when the entry reproduces a corpus row; a review entry that names no source is still valid |
| `suggested_disposition` | enum | yes | what the design segment proposes; advisory only — the confirmed value in `disposition` is what closes the entry |

**Two-valued invariant.** `state = disposed` ⟺ `disposition` is a set member. Every other state has
`disposition = null`. There is no third form, and in particular no "kept as is" value (FR-009).

## E-2 DetectionRun — one review pass and its coverage declaration

**Owns**: the run-level fields and the coverage-declaration shape (FR-011). One run = one file on disk only when
the execute segment writes evidence; a review-only run leaves nothing behind (FR-031).

| Field | Type | Notes |
|-------|------|-------|
| `run_id` | string | `<UTC timestamp>-<short hash>`, unique per run |
| `roots` | list of `{root, present, count, excluded_reason}` | one row per declared root, **in the declared order** (the declaration's statement order is part of the value) |
| `candidates` | integer | the sum of `count` over present roots; **never** a hand-written number |
| `missing_roots` | list of strings | declared but absent from the tree — reported and excluded, **not** counted as zero (FR-040) |
| `unregistered_siblings` | list of strings | directories under `.specify/` shaped like a declared root but not declared — a hint only; the candidate set does not grow (FR-041) |
| `declaration` | `{path, kind, status}` | the declaration file the run read; `status` is `ok` / `absent` / `invalid` |
| `shards` | list of `{shard_id, paths, verdict}` | the semantic-face partition; `verdict` ∈ `evaluated` / `unevaluated` (§ E-6) |
| `counts` | mapping category → integer | derived, never stored independently |
| `entries` | list of E-1 | the findings |
| `closed` | boolean | **derived**: `false` when any entry is `open` / `unevaluated` / `unconfirmed`, or any shard is `unevaluated` |

**The one prohibition.** An empty candidate set produces `candidates: 0` with a coverage declaration, and the run
reports "no candidates" — it MUST NOT report `closed: true` on an empty surface (the Edge Case "无输入不是干净").

## E-3 Exemption — the only way to keep something without repairing it

**Owns**: the four required fields and their composition rule (FR-006 / FR-007 / D-4). **Does not own**: the
per-`expiry_kind` semantics of "what re-opens the entry" — that is the owner page's § Exemption.

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `reason` | string | yes | why the entry is not being repaired now; a bare negation is not a reason (`N/A`, `n/a`, `none`, `-` are rejected) |
| `expiry_kind` | enum `on-date` \| `on-condition` \| `on-review` | yes | closed three-value set; there is no fourth value and no "permanent" |
| `expiry_value` | string | yes | `on-date` / `on-review`: absolute `YYYY-MM-DD`; `on-condition`: a named predicate plus the pointer to the declaration or owner entry that defines it |
| `expiry_recheck` | date `YYYY-MM-DD` | yes | the forced re-check date, absolute; its upper bound is owned by the owner page, not by this file |

**Expiry model.** Three transitions, each with a deterministic reading:

| Kind | Re-opens the entry when | Reading |
|------|------------------------|---------|
| `on-date` | today ≥ `expiry_value` | date comparison |
| `on-review` | today ≥ `expiry_recheck` **even if the condition still holds** | date comparison — this is the anti-tautology leg |
| `on-condition` | the predicate evaluates to `false` **or the predicate cannot be evaluated at all** | the engine evaluates; an unevaluable predicate yields `state = unevaluated`, never "still valid" |

A constant-true predicate (`condition: true` and its synonyms) is an **invalid** expiry condition and the entry is a
finding, not an exemption (FR-006). An entry whose `exemption` misses any of the four fields is not an exemption at
all: the entry stays `open` and the missing field names are reported (SC-017).

## E-4 DispositionRecord — what the execute segment wrote for one entry

**Owns**: the record shape. **Does not own** the disposition semantics (owner page) nor the evidence file layout
(§ E-7).

| Field | Type | Notes |
|-------|------|-------|
| `entry_id` | string | E-1's id |
| `disposition` | enum | the confirmed value |
| `group` | string | the category group the user confirmed (the confirmation granularity is `group` / `item` / `none-of`, owner page § Confirmation) |
| `moved` | `{from, to}` or null | `archive` only: the explicit source → archive path mapping (a `git mv` rename pair, not a delete) |
| `superseded_by` | path or null | `supersede` only: the new carrier the old text now points at |
| `reverted_by` | string | the exact revert command the user could run (`git checkout -- <path>` for `correct` / `supersede`; the inverse rename for `archive`) |
| `irreversible` | boolean | `true` only where the move cannot be undone from the record alone; the plans segment must have declared it before the confirmation (FR-034) |

**Invariant.** `moved` and `superseded_by` are mutually exclusive; `archive` sets `moved`, `supersede` sets
`superseded_by`, `correct` sets neither, `exempt` sets neither and writes an `exemption` instead.

## E-5 DispositionBridge — the two closed tables and the adjudication rule

**Shape only here; content is the owner page's.** This entity exists in the data model so the guard can address it
mechanically: the bridge is a table of `(nd_disposition, sanitize_disposition) → relation` rows covering the
**Cartesian product** of the two closed sets (SC-015: "uncovered pair = 0"), plus one adjudication rule row ("the
detecting engine decides the vocabulary"), plus the receiving-surface rows for the unmappable values.

| Field | Type | Notes |
|-------|------|-------|
| `nd_disposition` | enum | member of the owner page's disposition set |
| `sanitize_disposition` | enum | member of `sanitize-utils.DISPOSITIONS` — read from the engine, never re-spelled |
| `relation` | enum `maps-to` \| `unmappable` | `unmappable` rows carry the receiving surface instead of a mapping |
| `receiving_surface` | string | required when `relation = unmappable` |
| `rule` | string | the single adjudication rule, present exactly once |

The **count** of pairs is not written here: it is `len(nd set) × len(sanitize set)` by construction, and both
factors are owned elsewhere.

## E-6 Shard — the semantic-face partition unit

| Field | Type | Notes |
|-------|------|-------|
| `shard_id` | string | `<run_id>-s<NN>`, assigned deterministically by sorted path order then sequential numbering |
| `paths` | list of strings | disjoint from every other shard; the union equals the candidate set; **no shard is empty** (FR-047) |
| `verdict` | enum `evaluated` \| `unevaluated` | `unevaluated` when the subagent's return is missing or malformed — the shard is then **not** "clean" (FR-048) |
| `entries` | list of E-1 | the shard's findings, all `detection = semantic`, each with ≥ 2 evidence refs |

**Order-independence invariant.** The union of `entries` over shards, compared **by entry id**, is identical for
every concurrency degree (FR-049 / SC-009). A shard whose verdict is `unevaluated` contributes a visible mark and
**not** an empty list read as "no findings".

## E-7 RepairEvidence — the four segments one execute-segment group writes

**Owns**: the file shape; the **location** is owned by FR-035
(`.specify/specs/<spec-dir>/test-evidence/`, one file per run).

| Segment | Content |
|---------|---------|
| `readings` | the before and after `--json` digest of the same scope(s) — the two readings are what "repair happened" means |
| `paths` | the changed-path list (`git diff --name-only` scope), including every rename pair |
| `corpus` | the corpus entry ids this group disposes (`A1`…`H3`), empty when the group has no corpus row |
| `dispositions` | one row per entry: E-4's record |

A file missing any of the four segments does not make a repair valid (FR-054 / SC-010), even when the change itself
looks correct.

## E-8 ReviewSurfaceRoot — the declared root set

**Owns** neither the member list nor the count: the members are
`shared/declarations/facts/non-disposable-review-surface.yaml#/statement` (consumed through
`declaration_reader.py`), and the count is `len(statement)` — not a second statement of the number (FR-038).

| Field | Type | Notes |
|-------|------|-------|
| `root` | string | repo-relative directory, e.g. `.specify/specs`; the declared order is the report's order |
| `present` | boolean | measured, never assumed |
| `count` | integer or null | `null` when absent — an absent root is **not** `0` (FR-040) |
| `excluded_reason` | string or null | required exactly when `present` is false |

## E-9 SupersedeRecord — the supersede registry row

**Owns**: the row shape (FR-017); the registry's location and protocol are the owner page's § Supersede Protocol.

| Field | Type | Notes |
|-------|------|-------|
| `superseded` | `{path, line}` | the old carrier |
| `superseded_by` | `{path, line}` | the new carrier — resolvable, or the row is a dangling-pointer finding |
| `disposition` | enum | `supersede` in every row of this entity by definition |
| `evidence` | path | the repair evidence that shows the three landing zones were recovered (body / guard / evidence path) |
| `guard_status` | enum `retired` \| `replaced` \| `unchanged-with-reason` | the guard leg: a superseded body whose guard still demands the old behaviour is a finding (FR-016) |

## Entry State Machine

```text
                    (review produces it)
                             |
                             v
                        +---------+        detector input missing/unparseable
                        |   open  |-------------------------------+
                        +---------+                               |
                          |   |                                   v
       user confirmed     |   |  user did not confirm     +-------------+
       a disposition      |   |  this round               | unevaluated |
                          |   +-------------------------> +-------------+
                          v                                     ^
                    +----------+                                |
                    | disposed |                    (re-check: still not closed)
                    +----------+                                |
                          ^                                     |
                          |        expiry reached / predicate   |
                          |        false / predicate unevaluable|
                    +----------+ -------------------------------+
                    |  exempt  |  (a disposed sub-state: the entry is closed
                    +----------+   only until the expiry reading re-opens it)
```

| State | Meaning | Counted as closed? | Entered by |
|-------|---------|--------------------|-----------|
| `open` | detected, no confirmed disposition | no | the review |
| `unevaluated` | the detector could not judge (deterministic input missing / unparseable / engine failure; or a semantic shard returned nothing usable) | **no** — and it is visible, never silently "clean" | FR-005 / FR-048 |
| `unconfirmed` | the user saw the design and did not confirm this entry (or confirmed another group) | **no**; not retried next round, not dropped | FR-033 |
| `disposed` | a disposition value plus its evidence | **yes** | the execute segment |
| `exempt` | `disposed` with an `exemption` whose expiry is still in the future and whose predicate (if any) evaluates true | yes, **for now** — it returns to `open` at the expiry reading | FR-006 / FR-007 |

**Illegal transitions** (each is a finding, not an error to be smoothed): `open → disposed` without a confirmation;
`unconfirmed → disposed` inside the same run (a re-confirmation is a new run); `exempt → exempt` with a fresh date
that was not re-confirmed (**no silent renewal**, Edge Case "豁免积累"); any state `→` absent (an entry never
disappears — a defect that no longer exists is `disposed` with a `correct` record, never a deletion).

## Human-Facing Output Shape

The report and the design segment are read by someone who did not take part in the run
(`shared/guidelines/user-facing-comprehension.md`). They MUST let that reader answer four questions without opening
another artifact:

1. **What did you look at?** — the coverage declaration, in the declared root order, with absent roots named.
2. **What did you find?** — per entry: where (path:line), which class, how strong the evidence, and whether it was
   judged by a program or by a reading.
3. **What do you propose?** — per entry a disposition, the paths it touches, and whether it can be undone.
4. **What is not done?** — the `open` / `unconfirmed` / `unevaluated` counts, stated as **not closed**, never folded
   into a single "done" line.

The machine form (`--json`) carries the same fields; the human form is a projection of it, not a second model.

## Fact Owners

*Each fact has exactly one owner. Two rows owning the same fact is `owner-duplicate`; an owner path that does not
exist in the repository is `owner-path-missing`; an empty anchor is `owner-anchor-missing`.*

| 事实 | owner 路径 | 章节锚 |
|------|------------|--------|
| 理念定义、封闭处置集、豁免形态、检测类别封闭集、回顾面定义、取代协议、重编号判据面、报告 schema、与 sanitize/history 的边界 | `shared/definitions/non-disposable-definitions.md` | `## Disposition Set` |
| 十个回顾面根目录（成员与顺序） | `shared/declarations/facts/non-disposable-review-surface.yaml` | `/statement` |
| 材料卫生的类别 / 处置 / 状态 / 判定主体四个封闭集 | 既有 owner `sanitize-utils.py` 的 `CATEGORIES` / `DISPOSITIONS` / `STATES` / `DETECTIONS`（契约 `045-sanitize-command`） | 模块常量 |
| 闭环裁决、reason code 词表、验证词表与 smoke 记录 | `shared/workflow/acceptance-hardening.md` | `## Closure Verdict` / `## Verification Vocabulary` |
| 活绑定 / 历史记录的判据面 | 本特性 owner 页引用既有 `scripts/python/renumber-utils.py` 的谓词（`EXCLUDED_PREFIXES` / `MACHINE_PREFIXES` / `EVIDENCE_SEGMENTS` / `DATED_RE`） | 模块常量 |
| 检查入口的判定（退出码 0/1/2 与三个动作） | `scripts/python/non-disposable-check.py`（本特性交付的引擎常量） | 模块头部 |
| 条目状态集（`open` / `unevaluated` / `unconfirmed` / `disposed` / `exempt`） | **本文件** § Entry State Machine | `## Entry State Machine` |
| `exempt` 四字段与到期三值 | 本文件 § E-3（字段与组合规则）+ owner 页 § Exemption（每个取值的重开语义） | `## E-3 Exemption` |
| 执行段证据的落点与四段 | `requirements.md` FR-035 | `#### 命令执行形态：回顾 → 设计 → 确认 → 执行` |
| `detection` 两值在本特性侧的拼写 | owner 页 § Detection Subject | `## Detection Subject` |
