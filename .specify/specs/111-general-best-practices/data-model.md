# Data Model — General Best Practices (111-general-best-practices)

**Owner statement**: this file owns the **document-set model, the closed category set, the entry/placeholder model, the promotion path and the registration/mirror records** added by 111. It does not own: the accumulation rules — the feedback record shape, store and disposal belong to `scripts/python/feedback-utils.py`; the promotion procedure, the generality criterion and the traceability shape belong to the module manifest `shared/best-practices/README.md` § 逐步积累机制 (A-22); the knowledge-recording obligation belongs to `shared/guidelines/knowledge-promotion.md`; nor the distribution mechanism (`src/specify_cli/__init__.py` + `scripts/python/sync-mirrors.py`), the framework-map table schema (`shared/definitions/framework-map.md`), or the guard's assertion list (live owner `contracts/distribution-guard.contract.md` C-404). Upstream semantics are cited, never restated.

## Entities

### E1 — Module Document Set

The five documents at the module root, in source and mirror.

| Field | Type | Source | Rule |
|-------|------|--------|------|
| `root` | path | fixed | `shared/best-practices/` (source); `.specify/shared/best-practices/` (mirror) |
| `documents` | set of names | directory listing | Exactly `README.md` + [[STR-002]] + [[STR-003]] + [[STR-004]] + [[STR-005]]; no other top-level file or subdirectory (C-101) |
| `manifest` | name | fixed | `README.md` |
| `owner_files` | set of names | fixed | The four category files (E3) |
| `mirror_names` | set of names | derived | Identical five names in the mirror (E11) |

### E2 — Manifest

`shared/best-practices/README.md`, the module's single declaration surface.

| Field | Type | Rule |
|-------|------|------|
| `category_table` | table | The manifest's **only** table: three columns 模块 / 文件 / 内容, exactly four data rows, exactly one relative link per row, link-target set = the four owner files, literal 封闭集 present (C-102, C-103) |
| `readers_scope` | prose | Declares the module readers and scope: reusable classic daily-development lessons, accumulated progressively rather than a one-time list (C-104) |
| `entry_shape_pointer` | pointer | Points at `contracts/entry-shape.contract.md` and recalls the shape triple 标题 + 实践 + 反例/证据 (optional 延伸) (C-104, C-201) |
| `accumulation_pointer` | pointer + own rule | Names the feedback `record` action (pointer) and the [[STR-001]] marker convention written to `--review` text (C-301); declares the module's own promotion procedure, generality criterion and `**来源**` shape (the manifest is their owner, C-302/C-305); cites the knowledge-recording obligation owner by path (C-305) |
| `seed_pointer` | pointer | Names [[STR-005]] § [[STR-007]] as the seed (C-204) |

### E3 — Category (closed set)

| Field | Type | Rule |
|-------|------|------|
| `name` | literal | 编程语言 / 系统接口 / 编程框架 / 编程工具 — exactly four (C-102) |
| `owner_file` | name | 编程语言 → [[STR-002]], 系统接口 → [[STR-003]], 编程框架 → [[STR-004]], 编程工具 → [[STR-005]] |
| `scope` | prose | Owned by the manifest's 内容 cell for this category; owner files do not restate it, except the one-sentence echo beside an empty category's placeholder (C-105) |
| `closed` | invariant | Adding / removing / renaming a category requires the same-change trio — manifest revision + owner file creation/migration + guard update (C-106) |

### E4 — Owner File

One file per category, carrying its entries or its placeholder.

| Field | Type | Rule |
|-------|------|------|
| `h1` | heading | Exactly one H1 naming the category (C-202) |
| `accumulation_block` | blockquote | Link to `README.md` + literal 积累机制 + the entry-shape triple; a pointer, never a rules restatement (C-202) |
| `entries` | list of E5 | Ordered as accrued; each entry obeys C-201 |
| `placeholder` | E6 or null | Present iff `entries` is empty (C-203) |

### E5 — Entry

| Field | Type | Rule |
|-------|------|------|
| `heading` | `## ` heading | One per entry; the title is the practice's name (C-201) |
| `practice` | `**实践**` bullet | Operable practice: default plus exception (C-201) |
| `counter_evidence` | `**反例 / 证据**` bullet | The real defect or observation that justifies the practice (C-201) |
| `extension` | `**延伸**` bullet \| absent | Optional boundary case (C-201) |
| `source_line` | `**来源**` bullet \| absent | Required for promoted entries (C-303); exempt for the seed (C-204) |
| `origin` | `seed` \| `promoted` | The seed is [[STR-007]] in [[STR-005]]; promoted entries arrive through E7 → E8 |

### E6 — Placeholder State

| Field | Type | Rule |
|-------|------|------|
| `line` | italic line | Exactly one italic line containing [[STR-006]] plus one scope sentence (C-203) |
| `entry_count` | int | Must be 0 while the placeholder is present (C-203) |
| `delivery_count` | int | 3 at delivery (the three empty categories); the guard MUST NOT freeze this number (C-203) |

### E7 — Observation

An existing feedback record used as the accumulation input.

| Field | Type | Rule |
|-------|------|------|
| `store` | existing feedback store | Written through `feedback-utils.py --action record`; no new field, action or store (C-301) |
| `review_marker` | literal | Carries [[STR-001]] in the record's `--review` text (C-301) |
| `review_stem` | literal | Exactly one owner-file stem in the same text, without `.md`: `programming-languages` / `system-interfaces` / `programming-frameworks` / `programming-tools` (C-301) |
| `unit_convention` | ids | The command/skill run's unit id and run id, or `custom:best-practices/observation` + `--unit-type custom-unit` with a `bp-<yyyy-mm-dd>-<slug>` run id; a registry-carrying workspace first gets the custom unit's external probe from the probe system (C-301) |
| `module_write` | none | The observation is never written into the module before promotion (C-301) |

### E8 — Promotion Record

The traceability carried by a promoted entry's `**来源**` bullet.

| Field | Type | Rule |
|-------|------|------|
| `evidence_ref` | id \| commit \| quote | At least one of: feedback entry ID, hex commit ≥7, quoted session utterance (C-303) |
| `generality_basis` | prose | Recurrence, or one explicit user correction; the criterion is owned by the manifest's 逐步积累机制 section (C-302, C-303) |
| `observation_rewrite` | none | Promotion does not rewrite E7 and adds no feedback status (C-302) |

### E9 — Guard

`tests/contract/test_general_best_practices.py`, the feature's only new test file.

| Field | Type | Rule |
|-------|------|------|
| `legs` | six assertions | (a) document set / sole table / 封闭集; (b) owner identity / accumulation block / placeholder equivalence / entry shape; (c) seed facts; (d) pointer chain + no second engine file; (e) map rows in source and mirror; (f) relative links resolve (C-404) |
| `marker` | `pytest.mark.contract` | Registered as a contract test (C-404) |
| `entry` | `scripts/bash/run-tests.sh` | The only execution entry (C-404) |
| `boundaries` | prohibitions | No mirror comparison, no frozen placeholder count, no semantic-truth claim (C-404, C-205) |

### E10 — Framework-Map Registration Row

| Field | Type | Rule |
|-------|------|------|
| `table` | the single layout table | In `shared/definitions/framework-map.md` and its mirror (C-403) |
| `where` | literal | `.specify/shared/best-practices/` (C-403) |
| `notes` | prose | Contains Feature 111, a `README.md` pointer and `(framework source: shared/best-practices/)` (C-403) |
| `row_count` | int | Exactly one such row per table, source and mirror alike (C-403) |
| `instructions` | none | No new pointer section in `.specify/instructions.md` or the instructions template (C-403) |

### E11 — Mirror Pair Record

| Field | Type | Rule |
|-------|------|------|
| `pairs` | two mappings | `shared/best-practices/` → `.specify/shared/best-practices/`; `shared/definitions/framework-map.md` → `.specify/shared/definitions/framework-map.md` (C-401, C-402) |
| `generation` | command | `python3 scripts/python/sync-mirrors.py` write mode in the same change; never hand-edited (C-402) |
| `adjudicator` | existing suite | `tests/contract/test_mirror_parity_suite.py` alone decides byte identity (C-402) |

## State transitions

| ID | From → To | Trigger | Effects |
|----|-----------|---------|---------|
| T1 | Empty category → first entry | One promoted entry lands in an empty owner file | The placeholder line is removed in the same change; the entry is appended; the manifest's category table is unchanged (the category set did not change); the guard stays green because it judges equivalence, not a count (C-203) |
| T2 | Observation → promoted entry | The observation is proven general (recurrence or one explicit user correction) | An entry obeying C-201 lands in the owner file named by the observation's stem and carries a `**来源**` bullet (C-303); the observation record is unchanged (C-302) |
| T3 | Category set change | A category is added, removed or renamed | Manifest table revision + owner file creation/migration + guard update must land in one change; any missing leg is red (C-106) |

## Invariants

| ID | Invariant | Checked by |
|----|-----------|------------|
| INV-01 | The module root holds exactly the five documents; the mirror holds the same five names | Guard leg (a) + mirror parity suite |
| INV-02 | The category set is exactly four, each with exactly one owner file | Guard leg (a) |
| INV-03 | The manifest's only table is the category table: three columns, four data rows, one relative link per row, link targets = the four owner files, literal 封闭集 present | Guard leg (a) |
| INV-04 | Every relative link between the manifest and the four owner files resolves | Guard leg (f) |
| INV-05 | Placeholder present ⇔ zero entries; the guard never freezes the count 3 | Guard leg (b) |
| INV-06 | Every entry has `**实践**` and `**反例 / 证据**`; `**延伸**` is optional; promoted entries have `**来源**` | Guard leg (b) |
| INV-07 | The seed carries the three git-clone facts and the SSH extension; the seed has no fabricated source line | Guard leg (c) |
| INV-08 | Accumulation reuses the feedback engine by pointer and declares the manifest's own promotion procedure and criterion; the observation form is marker + stem in `--review`; no second engine file exists | Guard leg (d) + review (textual claims) |
| INV-09 | The map registration row exists exactly once in source and once in mirror, carrying both `.specify/shared/best-practices/` and Feature 111 | Guard leg (e) |
| INV-10 | Source and mirror are byte-identical, generated by write mode, never hand-edited | Existing mirror parity suite (sole adjudicator) |
| INV-11 | Module text contains zero `ai-harness` / `.ah/` / `/ah.` occurrences; every cited repository path exists | Guard module-read prelude (C-404, FR-008 / SC-005) |
| INV-12 | Changed paths relative to `0419adae5` stay inside FR-009's set plus per-entry accounting records with the feature key or run id | FR-009 procedure at review; `git diff --name-only` reading |

## FR → entity / invariant map

| FR | Entities | Invariants |
|----|----------|-----------|
| FR-001 | E1, E2, E3 | INV-01…INV-04 |
| FR-002 | E3, E4, E6 | INV-05 |
| FR-003 | E5 | INV-06, INV-07 |
| FR-004 | E2, E7, E8 | INV-08 |
| FR-005 | E10 | INV-09 |
| FR-006 | E11 | INV-10 |
| FR-007 | E9 | INV-01…INV-09 |
| FR-008 | E1, E5 | INV-11 |
| FR-009 | — (containment predicate) | INV-12 |