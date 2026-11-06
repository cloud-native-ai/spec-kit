# Feature Reference — Feature 087

## 1. Binding

| Field | Value |
|-------|-------|
| Feature ID | 087 |
| Feature name | 架构图为核心的文档空间（Architecture-Diagram-Centric Documentation Space） |
| Requirement branch | `line/087-arch-diagram-docs` |
| Requirements | [`requirements.md`](requirements.md) |
| Feature detail | `.specify/memory/features/087.md` |
| Feature index row | `.specify/memory/features.md` (Draft → Planned at this stage) |
| Flow class | execution（`flow-class-check.py --action lookup --unit-id "spec:087-arch-diagram-docs"`） |
| FR / SC | 23 / 10 |
| Runtime stack | RS-001…RS-007，全部 `Premises = EP-001` |

## 2. Delivery Surface

| # | Surface | Change |
|---|---------|--------|
| 1 | `skills/external/create-docs/scripts/docs-utils.py` | 新增只读动作 `obligation`（`C-001`…`C-016`） |
| 2 | `skills/external/create-docs/SKILL.md` § Desired-State Baseline（并在**该节内新建** `#### Assets` 小节，当前不在盘） | 配套图义务的基线条目（义务的定义点）+ **图的落点区域**（T-005，`docs/assets/`） |
| 3 | 同上 § Reconcile Loop R3/R4/R5/R6 · § Authoring Flow R2/R5/R6 | 图作为交付物、两面具名报告、检查器并列执行；**R5 内的产图/重渲染闭环**（`C-008a`） |
| 4 | `skills/external/improve-docs/SKILL.md` § Workflow | 命名分类行 + 最小编辑规则（不改图时明说） |
| 5 | `templates/commands/docs.md` § Outline | 义务指针（新增小节，W1 接线小节原样保留） |
| 6 | `docs/concepts/documentation-model.md` | 读者面投影一段（不定义规则） |
| 7 | `skills/external/draw-diagram/**` | **零改动**：只被引用（FR-011）——本表登记为「不交付面」以防误改 |
| 8 | `tests/unit/test_docs_utils_obligation.py` + `tests/integration/test_docs_obligation_scenarios.py` | 封闭 verdict / reason 集、只读、确定性、负向档位、收敛回路（`plan.md` § Test Plan 表 A/B） |
| 9 | `tests/fixtures/docs-obligation/**` | **11 段夹具**（`data-model.md` E6 的逐档表：8 段判定 + 3 段豁免） |
| 10 | `.specify/skills/create-docs/**`、`.specify/skills/improve-docs/**`、`.specify/templates/commands/docs.md`，加四家 per-tool 命令副本 `.claude/commands/speckit.docs.md`、`.github/prompts/speckit.docs.prompt.md`、`.opencode/command/speckit.docs.md`、`.qoder/commands/speckit.docs.md` | 由 `sync-mirrors.py` / `regen-command-copies.py` 生成，手不改（镜像路径是 `.specify/skills/<name>`，**没有** `external/` 这一层；源目录才有 `skills/external/<name>`） |

## 3. FR → Contract / Slice Map

| FR group | FRs | Contract / slice |
|----------|-----|------------------|
| A 结构基线 | FR-001…FR-004 | `flow-obligations.contract.md` C-001…C-006；`diagram-obligation.contract.md` C-003、C-011 |
| B 义务落地到两条流程 | FR-005…FR-010 | `flow-obligations.contract.md` C-002…C-017（含 `C-008a` 收敛） |
| C 能力复用 | FR-011…FR-013 | `diagram-obligation.contract.md` C-010；`draw-diagram` 只被引用 |
| D 可判定检查 | FR-014…FR-017 | `diagram-obligation.contract.md` C-001、C-002、C-004…C-009、C-012、C-013、C-015、**C-016**（唯一落档裁决） |
| E 边界与非回归 | FR-018…FR-021 | `flow-obligations.contract.md` C-016…C-021；`diagram-obligation.contract.md` C-014 |
| F 证据与负向可观测 | FR-022…FR-023 | `flow-obligations.contract.md` C-022…C-023；`quickstart.md` S3 |

## 4. SC → Measurement

| SC | Path | Measurement source |
|----|------|--------------------|
| SC-001 | final | `clean/` 夹具的四件产物 + `--action obligation` 报 `satisfied` |
| SC-002 | final | 失面逐面**具名**且**不互换**：`orphan-rendered` / `orphan-source` / `reference-unresolved` 三段独立夹具（`quickstart.md` S3 的 premises 表 + `U::test_c005_faces_not_swapped`） |
| SC-003 | final | reconcile 两次运行（`quickstart.md` S9 + `I::test_c008a_second_reconcile_zero_findings`）：首次逐文档报 `missing`，R5 按 `C-008a` 产图后**第二次运行 `converged=true`**（`missing`/`stale`/`not_evaluated` 三档全零）且 `git status` 无 cosmetic 变化。**「零图 finding」判的是 `converged`，不是 `clean`**（两谓词定义点 `diagram-obligation.contract.md` `C-013`）：带有效豁免的文档是 `FR-004` 的合法终态，其 `converged=true` + `clean=false` 同样满足本条（`I::test_c008a_exemption_does_not_block_convergence`） |
| SC-004 | final | 改名夹具：文档与图一致或留下具名 `stale`；文档与图源字节前后比较 |
| SC-005 | final | `skills/` `templates/` `shared/` `scripts/` 的引擎名 / 路由表搜索命令与输出 |
| SC-006 | final | `cmp a.json b.json`（S4）+ 干净空间 `clean=true`（该夹具无豁免，故 `converged=true` 与 `clean=true` 同时成立）+ `not-evaluated` 夹具（`converged=false`、`clean=false`） |
| SC-007 | supporting | 追溯记录的四个必填面（`C-010`）；缺一即 `trace-incomplete` |
| SC-008 | supporting | `exempt-ok` / `exempt-superseded` 两段夹具的 verdict 与计数（S5） |
| SC-009 | supporting | 精确 node id `test_protected_gate_preserved[templates/commands/docs.md-stop-and-confirm]`（1 个实例）；16 项是更宽守卫，不构成本行判据；分区定义前后对读 |
| SC-010 | supporting | 未刷新运行时项目上的 `not-evaluated` 表现（`C-012` 第 1 项） |

## 5. Disclosed Rulings

- **A7 → T-001**：追加一条 `ALLOWED_POST_BASELINE_CHANGES` 条目（`improve-docs` 在 74 条冻结清单内），
  `create-docs` / `docs.md` 不在清单内故不需条目，`documentation-model.md` 既不在清单也不在不可触路径内故不需条目。
  **不另立**本特性自己的基线记录：另立会让同一基线的处置散成两套判据。
- **A4 → T-002**：扩展 `docs-utils.py` 的新动作，按**调用方形态**选（与 `skill:create-docs` 的两处 R6 同形），
  不新增顶层脚本、不给 `doc-consistency-check.py` 加第六面。
- **A12 → T-003 + D-001**：`stale` 取并；左半（两面互不一致）用 mtime + sha256 判到；右半（图与文档就同一事实不一致）
  只判到「引用仍在且解析」，**语义一致性显式登记为未覆盖**（`D-001`），不发明一条不可判的 verdict。
- **FR-011 → T-004**：`draw-diagram` 只被引用、零改动；文档侧不出现引擎名 / 路由 / 交付契约的第二份副本。
- **图的落点 → T-005**：**全局单一落点** `<root>/docs/assets/<slug>.<ext>`（本仓先例 `docs/assets/quickstart-workflow.{puml,svg,png}`），
  源与渲染产物同置一处、文档内联或用可解析相对引用；**反题**是按文档类型的 `docs/<类型>/diagrams/` 子树，
  判别证据 `find docs -type d \( -name assets -o -name diagrams \)`（实测：`docs/assets` 在、`diagrams/` 0 个）。
  不新增文档类型目录、不改保留根文件语义。
- 本特性**不改**本仓 `docs/` 的内容（Two Hats：框架改动）；`.specify/` 只接受生成。
- **收敛归属 → T-005 之外的 `C-008a`**：Reconcile 的 R5 **必须**能产图/重渲染，否则 `SC-003` 的「第二次运行零 finding」
  在文本上不可达（「永久 missing」接线）。`missing` **不**被路由到 Authoring Flow 去收敛——那会让 reconcile 永远报残留。
- `checklists/requirements.md` 的派生计数漂移**本阶段不改**，登记为未决项（`OI-087-01`）：owner 是 `/speckit.checklist`。
- **恢复行（P2-3）**：`docs/tutorials/quickstart.md` 的图 alt text 写 "Core Development"、正文写 "Develop"；
  `C-009` 只判引用**可解析**，不判 alt 文本语义——该不一致归 `D-001`（`register.md` 已登记）。
