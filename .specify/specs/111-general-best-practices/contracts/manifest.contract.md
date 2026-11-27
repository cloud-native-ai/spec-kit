# Contract — Best-Practices Manifest and Document Set

**Path**: `shared/best-practices/README.md` (source) + `.specify/shared/best-practices/README.md` (mirror). Guard pinning: `tests/contract/test_general_best_practices.py` legs (a), (b), (f).
**Rule owners cited, never restated**: entry shape and placeholder invariant — `contracts/entry-shape.contract.md`; accumulation — `contracts/accumulation.contract.md`; distribution, registration and guard legs — `contracts/distribution-guard.contract.md`; the directory's registration obligation — `shared/guidelines/directory-governance.md` § 3.

**C-101** Document set.

The module root MUST contain exactly five top-level regular files: `README.md`, [[STR-002]], [[STR-003]], [[STR-004]] and [[STR-005]]. No other file or subdirectory belongs at this level. The mirror directory MUST carry the same five names. (FR-001, FR-007(a))

**C-102** Closed category set.

The categories are exactly 编程语言 / 系统接口 / 编程框架 / 编程工具 — four, no more, no fewer. Each category has exactly one owner file: 编程语言 → [[STR-002]], 系统接口 → [[STR-003]], 编程框架 → [[STR-004]], 编程工具 → [[STR-005]]. The manifest MUST contain the literal 封闭集. (FR-001, FR-007(a))

**C-103** Manifest's sole table.

The category declarations MUST be carried by the manifest's only Markdown table, with exactly three columns (模块 / 文件 / 内容) and exactly four data rows. Each data row MUST contain exactly one relative link; the set of link targets MUST equal the four owner files and MUST resolve from the manifest's directory. A second table, a fifth data row, a row with zero or two links, or a target outside the four is red. (FR-001, FR-007(a)(f))

**C-104** Reader, scope and pointers declared.

Outside the table, the manifest MUST declare: (a) the module's readers and scope — reusable classic daily-development lessons, accumulated progressively rather than a one-time list; (b) the unified entry shape by pointing at `contracts/entry-shape.contract.md` and recalling the shape triple 标题 + 实践 + 反例/证据 (optional 延伸); (c) the accumulation mechanism by pointer to the feedback engine action and the knowledge-promotion owner (C-301…C-305); (d) the seed pointer to [[STR-005]] § [[STR-007]]. (FR-001, FR-004, FR-007(b)(d))

**C-105** Scope single ownership.

Each category's scope sentence is owned by the manifest's 内容 cell for that category. Owner files MUST NOT restate their scope, with one exception: an empty category's placeholder may echo one scope sentence beside the placeholder. (FR-002)

**C-106** Closed-set change process.

Adding, removing or renaming a category MUST land in one change that (1) revises this manifest table, (2) creates or migrates the corresponding owner file, and (3) updates the guard legs. A new file without the manifest revision, or a manifest revision without the file, is red. (FR-001, FR-007)