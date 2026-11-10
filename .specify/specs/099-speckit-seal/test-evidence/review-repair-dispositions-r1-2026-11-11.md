# Review 修复轮 r1 — 处置记录（099-speckit-seal）

> 输入：`.specify/specs/099-speckit-seal/review.md`（1 P0 + 2 P1；7 条 P2 不在本轮范围，见 §4）。
> 运行：`r20261110T121314Z-b099` · stage=review（修复回环）· 四元组：flow_class=execution；source=declaration；marker=；error=-
> 纪律：`review.md` / `code-review.md` / 既有 test-evidence 均为 dated record，**未改写**；修复落在引擎（`scripts/python/`）、框架 owner 文档（`shared/workflow/`）、099 需求/合同与测试面；框架源与 `.specify/` 镜像同批同步。

## 1. 复核方法与计数

- 复核形态：F1 采用 review 记录内的独立只读验证（review §3 F1「independently validated … `confirm` at P0」）；F2、F3 按锚点直读复测（file:line + 实测命令），判据为「锚点事实成立且缺陷类别可复现」。
- 复核计数：**confirm 3 / reject 0 / downgrade 0**。
- 严重度不变：F1 P0、F2 P1、F3 P1（本轮不重判严重度）。

| ID | 类别 | 复核 | 一句话结论 |
|----|------|------|-----------|
| F1 | Automation / Scripts | **confirm** | split 父级的 seal P0/blocking 门只读合并指针视图，未处置的分片 P0 可被静默放行；已改为读取原始分片记录，红先 4 例（2 拒绝 / 2 放行/载体反证）。 |
| F2 | Documentation | **confirm** | FR-006「P0 处置按原记录判定」与 C-013/C-021「指针视图」措辞冲突；以修复后的引擎行为为准收敛两处。 |
| F3 | Workflow | **confirm** | C-022 的 `> ` 引用行使 67 条 `[green:]` 认领从核算面消失；已加 supersede-aware 认领，T050 复跑 67 → 0。 |

## 2. 逐条处置

### F1（confirm）— split-parent seal P0 gate reads the original slice records

- **锚点复测**：`scripts/python/seal-utils.py:2597`（原 `evaluate_seal` P0 门）只把父 `review.md` 文本交给 `_p0_findings`；父级合并视图实测为 pointer-only（`.specify/specs/074-goal-team-sdd-unification/review.md` 仅两行指针）；`074b-nested-governance/review.md:115-140` 的 P0 `F1` 只有驱动者记录的「显式豁免（P0 waiver）」叙述，无 `- **Fix**:` 可解析指向、无 C-044 两载体用户豁免。
- **根因**：`_p0_findings` / `_review_summary` / `BLOCKING_HEADING_RE` 扫描都只吃父视图；指针视图不承载 finding 块 → 分片 P0/blocking 不可见，`unaccounted` 也恒为 0。
- **修复**（`scripts/python/seal-utils.py`）：
  - `evaluate_seal` 在 P0 判定前先 `_discover_slices` + `_derive_order`，构造 `review_records` = 父视图 + 各分片原始 `review.md`；`code_review_records` 同构（分片 `code-review.md`）。
  - P0 findings 按来源收集，finding id 以 `<slice-slug>:F1` 限定；`_p0_findings` 新增 `carrier` / `review_label` 参数，waiver 仍按 C-044 两载体判定（分片 review 的 code 小节 + 父特性详情 `## Latest Review`；驱动者叙事不计）。
  - summary 的 P0/P1/P2 按来源聚合；`unaccounted` 逐来源计算（分片 summary 声称 P0 但无可解析块同样阻断）。
  - `code-review-blocking` 扫描分片原始 code-review 记录。
  - receipt：`review.paths` 追加实际读取的分片 review/code-review；`counts` 反映聚合值；`waivers[].source` 指向 finding 所属载体（分片记录或父记录）+ 特性详情。
  - 镜像：`.specify/scripts/python/seal-utils.py` 同步（`sync-mirrors.py --check` ok）。
- **红先**（`test-evidence/f1-red-first-20261111.txt`）：4 个新用例在修复前引擎上 4 failed —— 未豁免分片 P0 直接 sealed（exit 0）、slice waiver 放行但 receipt 不引用分片记录、单载体豁免被放行、分片 blocking 未点名；修复后 4 passed。
- **验收用例重跑**（`test-evidence/074-round-repair-r1-20261111.txt`）：对真实 074 树两次只读 `seal` 运行——exit 2、writes 0、`seal.md` 未创建、`git status` 前后一致、两次清单逐字节相同；**引擎条件新增 `p0-unresolved: 074b-nested-governance:F1 (line 115 of .specify/specs/074b-nested-governance/review.md)`**——FR-027(d) 由引擎自己点名，不再依赖人工裁决段。

### F2（confirm）— FR-006 与 C-013/C-021 措辞收敛

- **锚点复测**：`requirements.md:132`（FR-006）与 `:223`（Clarifications）；`contracts/merge-back.contract.md` C-013 / C-021；引擎修复后的行为 = 父视图保持指针形态、判定读取原始分片记录。
- **修复**（以修复后引擎行为为准）：
  - `requirements.md` FR-006：补「拆分 spec 的当前记录集合 MUST 包含合并父级视图与各分片原始 `review.md`/`code-review.md`；父级视图是指针视图（不承载 finding 块），**指针视图不改变 P0 判定读取面**——P0 与 `blocking` 判定 MUST 读取各分片原始记录」。
  - `requirements.md` Clarifications 同题答案同步同一口径（父级指针视图 + 分片原始记录）。
  - `contracts/merge-back.contract.md` C-013：补一句「该汇总指针视图（逐分片汇总行 + 指针）不承载 finding 块，且**不改变 seal 的 P0 / `blocking` 判定读取面**——判定 MUST 读取各分片原始 `review.md` / `code-review.md`（waiver 形态见 records-and-boundaries.contract.md C-044）」。
  - `contracts/records-and-boundaries.contract.md` C-044：补「拆分 spec 的分片 P0，其 review 载体是该分片**原始** `review.md` 的 code 小节（合并父级指针视图不承载 finding，也不承载 waiver）；特性详情载体不变」——把引擎行为落回 waiver 判据的唯一 owner。
- **复核**：`validate-requirements.py` 0 error / 0 warning；099 契约条款数不变（45 = 13+14+10+8）；`account-clause-coverage` 读数 45/45。

### F3（confirm）— superseded 记录的条款认领保留

- **锚点复测**：`074-goal-team-sdd-unification/tasks.md` § Superseded pre-split record 内 **67** 个 `[green:]` 标签；`test-evidence/coverage-final.txt` 的 `uncovered_beyond_baseline=67` 全部为五份 074 父契约条款。
- **根因**：C-022 用 `> ` 引用前缀保留拆前行 → `^- \[` 任务行正则不再命中 → `validate-tasks.py` 的 `claims_out` 不含这些认领 → 核算引擎把它们读成未覆盖。
- **修复**：
  - `scripts/python/validate-tasks.py`：识别 `## Superseded pre-split record` 块；块内 `> - [...]` 行按同一 `_strip_claims`（fence/code-span 规则唯一实现）解析为 **retained claims**，只进入 `claims_out`，不参与当前计划的四项 `green-*` 检查；全部行都被 supersede 的文件（无活跃行）也不丢认领。
  - `shared/workflow/acceptance-hardening.md` § Gates 新增 **唯一 owner 规则**「Superseded pre-split records retain their claims」（引用行不进入当前计划，但不作废认领；核算 MUST 同活跃行对待）。
  - `scripts/python/account-clause-coverage.py` docstring 的 `claimed` 车道补指针（消费面不变：仍经 validate-tasks 的单一实现）。
  - 镜像：三份脚本 + 一份 shared 文档同步（`--check` ok）。
- **红绿**（`test-evidence/f3-supersede-claims-20261111.txt`，同一 hermetic 夹具）：修复前 `claimed=0 / uncovered=3 / delta=3`（mirror 旧引擎）→ 修复后 `claimed=3 / uncovered=[] / status=ok`。
- **真实语料**（`test-evidence/t050-replay-repair-r1-20261111.txt/.json`）：T050 复跑 `status=ok`、`uncovered_beyond_baseline=0`（原 67）、本 spec 45/45、FR 28/28；074 自身车道 `074-*` 未覆盖 = 0、`claimed=144`（77 活跃 + 67 保留）。`coverage-final.txt` 与 `t050-rerun-20261111.*` 作为 dated record 原样保留。
- **新增合同测试**：`tests/contract/test_clause_coverage.py::test_superseded_pre_split_rows_retain_their_claims`。

## 3. 复跑读数（受影响套件）

| 套件 / 命令 | 读数 | 证据 |
|---|---|---|
| `test_seal_seal.py` | **25 passed**（含 4 个新用例） | `review-repair-r1-required-suites-20261111.txt` |
| `test_seal_074_round.py` | **5 passed** | 同上 |
| seal 家族（10 文件：contract + integration） | **137 passed**（P8b 基线 133 + 新 4） | 同上 |
| `test_clause_coverage.py` + `test_validate_tasks_green_semantics.py` + `test_validate_tasks_parallel_safety.py` + `test_green_point_claim.py` | **161 passed / 2 failed（均为 HEAD 预存红，见 §4）** | `review-repair-r1-suites-20261111.txt` |
| `account-clause-coverage.py`（099 / 074） | 099: ok / 0 beyond / 45 / 28；074: 0 residual | `t050-replay-repair-r1-20261111.*`、`review-repair-r1-required-suites-20261111.txt` |
| 镜像一致性（4 个修复文件） | `sync-mirrors.py --check` 两对均 ok | `review-repair-r1-required-suites-20261111.txt` |

## 4. 边界与残留

- **本轮范围外（未处置）**：review 的 P2 F4–F10（features.md/详情刷新、plan 写面、verification 130→133、state spine、宪法出带、`_write_seal_batch` 原子性 F9、`green-cross-phase` F10）。其中 F9 与 F1 同文件但属不同缺陷，本轮未改动。
- **预存红（非本修复引入）**：在 HEAD `99af8cb3b` 的干净快照（`git archive` → /tmp）复现同一红——`test_clause_coverage.py::test_c5_gate_budget_is_unchanged_by_the_owner_document`（gate total 28 vs pin 27）与 `::test_c10_openapi_clauses_are_method_keys_and_the_total_matches_the_census`（yaml-openapi 30 vs census pin 39）。未修、未掩。
- **一次自致观察**：首次套件捕获把 stdout 重定向进 `.specify/specs/...`，让 `test_c20`（核算前后语料哈希）读红；改在树外捕获后通过。这是捕获方式问题，不是引擎写入。
- **行为变化披露**：074 回合的引擎条件清单比 P8b 记录多一条 `p0-unresolved`（修复目标行为）；旧回合证据保持原样，作为前一引擎的 dated reading。
- **未伪造豁免**：074b 的 P0 没有写入任何 `- **User waiver**:` 行；074 的 status pair 保持 `Ready for Review`，零写入。

## 5. 证据索引（均在 `.specify/specs/099-speckit-seal/test-evidence/`）

| 文件 | 内容 |
|---|---|
| `f1-red-first-20261111.txt` | F1 红先：修复前 4 failed → 修复后 4 passed |
| `074-round-repair-r1-20261111.txt` | 074 只读重跑：两次 exit 2、零写入、`p0-unresolved` 点名 `074b-nested-governance:F1` |
| `f3-supersede-claims-20261111.txt` | F3 红绿：同夹具 claimed 0→3 / uncovered 3→0 |
| `t050-replay-repair-r1-20261111.txt` / `.json` | T050 复跑：099 读数 ok、beyond_baseline 67→0；074 0 残留 |
| `review-repair-r1-required-suites-20261111.txt` | 指定套件复跑（seal / 074 round / accountant）+ 镜像检查 + seal 家族 137 passed |
| `review-repair-r1-suites-20261111.txt` | 扩展受影响套件读数与 HEAD 预存红的快照复现 |
