# Analyze 修复轮 r1 — 处置记录（099-speckit-seal）

> 输入：`test-evidence/analyze-merged-2026-11-10.md`（Round 1：0 CRITICAL / 7 HIGH / 5 MEDIUM / 0 LOW；7 HIGH 全部 `proposed`）。本轮只处置 7 条 HIGH；MEDIUM 5 条不在本轮范围（见 §5）。
> 运行：`r20261110T121314Z-b099` · stage=analyze（修复回环）· 四元组：flow_class=execution；source=declaration；marker=；error=-
> 纪律：分析报告与 checklist 是 dated record，**未修改**；全部修复落在 requirements / contracts / data-model / plan / quickstart / tasks 的语义面上。

## 1. 复核方法与计数

- 复核形态：**自证（self-verified）**。7 条 HIGH 均为 `proposed`（首轮未派发独立复核波）；本轮为派发的修复轮，按任务指令对每条锚点做直读复测（file:line + 实测命令），判据为「锚点事实成立且缺陷类别可复现」→ `confirm`；否则 `reject`。
- 复核计数：**confirm 7 / reject 0 / downgrade 0**。全部 confirm 项已做最小修复并全链同步。
- 严重度不变：7 条均维持 HIGH（缺陷类别与传播面在修复前均成立；本记录不重判严重度）。

| ID | 类别 | 复核 | 一句话结论 |
|----|------|------|-----------|
| B-01 | Ambiguity | **confirm** | SC-006「与五项一一对应」把合法阻断面收窄为恰五项；074 实测存在五项之外阻断。 |
| C-03 | Underspecification | **confirm** | 目录型候选无文件级合并单位与同名三态；074 三侧同名文件实测存在。 |
| C-04 | Underspecification | **confirm** | `[[STR-NNN]]` 是文档局部记号；未声明登记处的引用无绑定/解析规则。 |
| E-01 | Coverage Gaps | **confirm** | SC-002「分片未闭合」类无 FR 判据、无封闭拒绝码。 |
| F-01 | Inconsistency | **confirm** | dated-record 目录的目录级 `merge` 无合法语义（复制=第二份测量）。 |
| F-02 | Inconsistency | **confirm** | 必选下限缺父 `code-review.md`；缺失语义未定义。 |
| F-04 | Inconsistency | **confirm** | FR-027(b) 只列 074b；074a `STR-010` 同号不同义实测遗漏。 |

## 2. 逐条锚点自证

### B-01（confirm）

- 报告锚点复测：`requirements.md:191`（SC-006「seal 终态为 `Sealed` 或与 FR-027 五项实测输入**一一对应**的具名阻断清单」——原文成立）；`:69`（US3「完整裁决」段）；`:73`（US3 Independent Test 同形「一一对应」）；`:162`（FR-027 五项枚举）。附带落点实测：`contracts/records-and-boundaries.contract.md` C-043「一一对应」；`plan.md:31`、`:145`（T-005）；`quickstart.md:171`；`tasks.md:218`、DoD-6、T043。
- 缺陷成立依据：「一一对应」是封闭清单声明（owner `shared/guidelines/closed-set-claims.md`），会把五项之外的合法 `conflict-open` 阻断读成不合规；五项之外的确定性阻断来源实测存在——F-04 的两组额外同号不同义（074a `STR-010`、074b `STR-007`）与 C-03/F-01 的目录同名产物冲突。
- 修复：
  - `requirements.md:191`（SC-006）：终态改为「**至少逐条覆盖 FR-027 五项实测输入**的具名阻断清单——五项之外的实测阻断只需逐条点名即合规」，并加**验收断言**：回合记录对五项逐项呈 resolved/blocked，拒绝清单每条阻断可解析到回合证据（多出条目不判违规）。
  - `requirements.md:203`（SC-006 Source）：对照口径加「（下限）+ 额外阻断逐条点名」。
  - `requirements.md:69`（US3 段）与 `:73`（Independent Test）：同步「下限而非上限」表述。
  - `requirements.md:162`（FR-027）：尾部加「五项是**下限**：回合实测新增的具名阻断（含五项之外的同号不同义、目录同名产物冲突）MUST 同样逐条点名」。
  - 契约 `C-043`：「一一对应」→「五项是下限，额外具名阻断逐条点名」。
  - `plan.md` Summary 与 T-005、`quickstart.md` S-7、`tasks.md` Phase 6 Independent Test / DoD-6 / T043 / T044：同口径同步。

### C-03（confirm）

- 报告锚点复测：`requirements.md:141`（FR-012：候选宇宙含 `contracts/`、`checklists/`、`checkpoints/`、`test-evidence/`、`notes/`，动作按「同名输出件」）；`contracts/merge-back.contract.md` C-013（原 `:23`）、C-021（原 `:99`）。原件均无「目录内文件级单位」规则。
- 实测（本轮复现，与 analyze-gates §8 一致）：`checklists/requirements.md` ×3 侧；`checklists/readiness-2026-10-29.md` ×2 侧；`test-evidence/{plan-stage-checks.md,tasks-stage-checks.md,targeted-set-v1-baseline.txt}` ×3 侧；`contracts/nested-invocation.md`（父+074a）；`contracts/report-and-attribution.md`（父+074b）。这些输入上 FR-013 确定性 / FR-017 冲突显式性无可适用判据。
- 修复：
  - `requirements.md:141`（FR-012）：新增**目录型候选**段——合并单位为**文件**（按文件名取并集），同名三态：两侧同名 → 文件级 `merge`（无法确定性归并/双端编辑 → 冲突）；仅分片有 → `create`；仅父级有 → `keep`。
  - `contracts/merge-back.contract.md` C-013（现 `:27` 起）：同规则落契约；C-021：散文类合并视图清单加入 `code-review.md`（与 F-02 同批）。
  - `data-model.md` E5 + V9：目录型候选逐文件成行（`name` = `<dir>/<file>`）。
  - `tasks.md` T018（夹具：目录同名文件三态）、T019/T020/T021/T023（文件级单位与同名三态断言/实现）、T040（回合逐文件处置）。

### C-04（confirm）

- 报告锚点复测：`requirements.md:145`（FR-016 只要求「解析到合并后的父级唯一注册表」，未给 token→注册表绑定规则）；`contracts/merge-back.contract.md` C-017（原 `:63`）；`shared/definitions/sdd-routing-definitions.md:16`「字面量登记处：`[[STR-001]]`…`[[STR-010]]` 的取值与语义 owner 是本特性切片的 `requirements.md` § Shared Strings」——文档局部登记处口径成立；`skills/internal/create-team/SKILL.md:99,101` 使用 `[[STR-004]]`/`[[STR-005]]`/`[[STR-006]]`，该文件无 § Shared Strings 声明（`grep -n "Shared Strings"` 零命中）——未声明登记处的引用实测存在。
- 修复：
  - `requirements.md:145`（FR-016）：新增 **token→注册表绑定**——spec 文档以自身 `requirements.md` § Shared Strings 为登记处（口径 owner 指针，不复述）；spec 之外的文档 MUST 显式声明登记处（spec 路径 + 节锚）；未声明登记处的引用 MUST 做跨登记处解析：恰一分片注册表命中且字面量一致 → 按分片本地 ID 检出并记录解决；零命中/多处命中且字面量不同 → 冲突，禁止猜测归属。
  - `contracts/merge-back.contract.md` C-017（现 `:72` 起）：同规则落契约。
  - 冲突夹具：`tasks.md` T018 `conflict-injections/` 增「未声明登记处的 `[[STR-NNN]]`（跨登记处歧义）」；T019/T020/T023 增绑定检查与检出断言。

### E-01（confirm）

- 报告锚点复测：`requirements.md:187`（SC-002 八类失败含「分片未闭合」）；`:107`（Edge Cases「一片已闭合、另一片仍有未勾选行或未决冲突」）；E12 原表（`data-model.md:168-184`）无对应码，`merge-incomplete` 只覆盖「manifest 缺失/覆盖不全/`not-applicable` 依据缺失」；C-042 封闭集无对应码；全仓 FR 文本检索「分片未闭合」零 FR 定义。
- 修复（采用报告的「新增判据 + 封闭码」分支，不新增 FR 编号——判据并入 FR-008 的「合并回写完成」语义，避免 FR 计数与全链计数声明漂移）：
  - `requirements.md:134`（FR-008）：「完成」新增**分片已闭合**判据——分片 `tasks.md` 未勾选行（`- [ ]`/`- [>]`）计数为 0；`- [~]` 行须在分片 `verification.md` 的 `deferred_tasks=` 逐项有名（行形态与计数来源：与父 `tasks.md` 同一任务行正则）；未闭合 → `slice-unclosed` 具名阻断并点名分片与行，禁止补完/伪勾选。
  - `requirements.md:107`（Edge Case）：补码名与判据指针。
  - `contracts/records-and-boundaries.contract.md` C-042：封闭集加入 `slice-unclosed`。
  - `data-model.md` E12（现 `:180`）：新增 `slice-unclosed` 行（来源 FR-008）。
  - `tasks.md` T026（夹具点名码）、T028（只读判定段含该判据）；`quickstart.md` S-5 补码名。

### F-01（confirm）

- 报告锚点复测：`requirements.md:141`（FR-012「两侧皆有 → `merge`」）；`:148`（FR-019 dated-record 红线）；`contracts/merge-back.contract.md` C-013、C-020；实测 `test-evidence/` 三侧全有（`plan-stage-checks.md`、`tasks-stage-checks.md`、`targeted-set-v1-baseline.txt`）。
- 缺陷成立依据：目录级 `merge` 在 dated-record 目录无合法语义——复制即第二份测量（违 FR-019），不复制则动作名不实。
- 修复（与 C-03 同段落盘）：
  - `requirements.md:141`（FR-012）：`test-evidence/`、`checkpoints/` 内的既有日期化测量文件属 dated record——MUST NOT 复制或改写原件；同名时父级维持 `keep` + 合并清单指针；仅分片有时以父级**指针视图**（汇总行 + 指针）`create`，分片原件字节不变。
  - `requirements.md:148`（FR-019）：补「按 FR-012 的指针纳入动作处置」。
  - `contracts/merge-back.contract.md` C-013 与 C-020（现 `:106` 起）：指针纳入语义与「禁止父级副本」。
  - `data-model.md` E5/V9：dated-record 文件动作语义 = 指针纳入（无文件副本）。
  - `tasks.md` T019/T021/T023/T040：指针纳入断言与实现。

### F-02（confirm）

- 报告锚点复测：`requirements.md:141`（FR-012 必选下限只含父 `verification.md`、父 `review.md`、合并清单）；`:161`（FR-026 要求回合产出「两片 `review.md` + `code-review.md` 的汇总视图与指针」）；`:132`（FR-006 以「当前 `code-review.md`」为前置，但缺失语义未定义）；C-013 同缺；`tasks.md:221`（T040 只列父 `review.md` 汇总视图）。实测父 `074-goal-team-sdd-unification/` 无 `code-review.md`（analyze-gates §6 `parent_code_review_present: no`）。
- 修复：
  - `requirements.md:141`（FR-012）必选下限：加入「父 `code-review.md`（分片 code-review 记录的汇总指针视图，缺席则新建）」。
  - `requirements.md:132`（FR-006）：`review.md` **或** `code-review.md` 缺失 → `review-missing` 具名阻断（exit `1`）并点名 `/speckit.review`。
  - `contracts/merge-back.contract.md` C-013（必选下限）与 C-021（合并视图清单）。
  - `data-model.md` E12：`review-missing` 触发面扩展为两文件。
  - `tasks.md` T028（缺失判定）、T040（父 code-review.md 汇总指针视图）。

### F-04（confirm）

- 报告锚点复测（逐项实测）：
  - `074a-authorized-routing/requirements.md:90`：Parent Mapping `STR-010 | STR-011`（席位策略键名 `"seats"`）；同文件 `:430` 本地 `STR-010` = `"seats"`。
  - `074b-nested-governance/requirements.md:72`：Parent Mapping `STR-007 | STR-010`；同文件 `:237` 本地 `STR-007` = `"## Nested SDD Runs"`。
  - 父 `074-goal-team-sdd-unification/requirements.md:444-451`：`STR-007` = `"completed"`、`STR-010` = `"## Nested SDD Runs"`（另 `STR-004`–`STR-006` = `sdd`/`direct`/`adjudicate`）。
  - 结论：两组「同号不同义 + 已声明映射」成立；原 FR-027(b) 只写「074b 本地 STR 编号」，遗漏 074a `STR-010`。
- 修复：
  - `requirements.md:162`（FR-027(b)）：枚举实测两组（074a `STR-010`→父 `STR-011`；074b `STR-004`–`STR-007`→父 `STR-007`–`STR-010`），并加「回合实测新增同号不同义逐条点名」下限条款（与 B-01 共用终态口径）。
  - `requirements.md:191`（SC-006）：由 B-01 的「至少五项 + 额外阻断逐条点名」覆盖。
  - `tasks.md` T039：merge-plan 冲突处置加两组声明映射核验，引用补 FR-027(b)；T044 增「五项之外阻断同样逐条落承载」。
  - `quickstart.md` S-2：已知合并冲突清单补 074a `STR-010` 与 074b 007。

## 3. 修复面清单（全链同步）

| 制品 | 变更点 |
|------|--------|
| `requirements.md` | FR-006、FR-008、FR-012、FR-016、FR-019、FR-027、US3 段/IT、SC-006、SC-006 Source、Edge Cases |
| `contracts/merge-back.contract.md` | C-013（文件级单位/同名三态/dated-record 指针/必选下限）、C-017（token 绑定）、C-020（指针纳入）、C-021（视图清单） |
| `contracts/records-and-boundaries.contract.md` | C-042（`slice-unclosed`）、C-043（五项下限口径） |
| `data-model.md` | E5、V9、E12（`review-missing` 扩展 + `slice-unclosed` 行） |
| `plan.md` | Summary 终态口径、T-005 discriminating_evidence |
| `quickstart.md` | S-2（STR 冲突清单）、S-5（码名）、S-7（终态口径） |
| `tasks.md` | T018、T019、T020、T021、T023、T026、T028、T039、T040、T043、T044、DoD-6、Phase 6 Independent Test |

**未改动**：`checklists/*`（dated 评估记录）、`research.md`（dated 实测记录）、`feature-ref.md`（由 `clause_extract.py` 从契约引用组再生——本轮修复后重跑生成脚本，28/28 映射与文件内表格逐项一致，无需改写）、analyze 报告与 analyze-gates（只读输入）。

## 4. 门禁复跑

证据文件：`test-evidence/analyze-repair-gates-r1-2026-11-10.txt`。摘要：

| 门禁 | 结果 |
|------|------|
| `validate-requirements.py` | exit 0；6 检查项全 pass（id-contiguous / doc-order / ref-resolvable / marker-count / dup-id / path-marker）；251 行 / 37 定义行 / 3 共享字符串 |
| `pre-analyze-check.py --stage requirements` | `decision=pass`，errors=0，advisories=101（全部为未来路径与模板占位符，属 do-not-flag 类） |
| `pre-analyze-check.py --stage plan` | `decision=pass`，errors=0 |
| `pre-analyze-check.py --stage tasks` | `decision=pass`，errors=0 |
| `decomposition-check.py --mode tasks` | `decision=proceed`（FR 28 / tasks 51，均在 ceiling 内） |
| `validate-tasks.py`（支撑） | PASS，0 error / 0 warning |
| `validate-decision-tensions.py --spec plan`（支撑） | exit 0；6 记录，六标签全 pass，high=0 |
| `clause_extract` 引用组复核（支撑） | 28/28 FR→C 映射与 `feature-ref.md` 表格逐项一致（修复未改变引用组） |

## 5. 范围外残留（不在本轮处置）

- MEDIUM 5 条按 analyze 报告保留，待 Round 2 复核：C-01（审计更正证据最小形态）、C-02（review「当前集合」派生规则）、F-03（dirty 判定范围措辞收敛）、E-02（`coverage-baseline.txt` 缺席 → 条款差量仍不可判）、G-01（特性注册表阶段注记陈旧）。
- **E-02 仍为 Round 2 复跑前提**：本修复轮未改条款宇宙（无新增/删除契约条款），但 analyze 覆盖步骤在 baseline 缺席时仍会报 `baseline-missing`（exit 2）；该状态是「不可判」而非「通过」，MUST NOT 被读作回归。
- 无 CRITICAL；本轮未引入新 finding。

## 6. Fast-fail 与异常声明

- 本轮未发现需上送的 fast-fail 异常；无「以假设完成修复」的决策——全部修复由锚点实测与已记录 owner 规则（C-011…C-023、FR-027 实测值、C-042 闭集、`sdd-routing-definitions.md` § 字面量登记处）推出。
- 无可修补的「顺带修正」事项遗留：route 中发现的 `quickstart.md` S-2 STR 清单不完整属于 F-04 的链式同步，已随修复落盘。

## 7. 提交

- 单一修复提交，commit message：`099 analyze repair r1`。内容 = 上述 7 个制品文件 + 本处置记录 + 门禁证据文件。
