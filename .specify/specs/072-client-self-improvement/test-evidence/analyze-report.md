# Analyze Report: 072-client-self-improvement

**Stage**: analyze（Feature 072，断点续跑：checklist 072 已落盘，40 项）
**Mode**: 严格只读分析；本目录两份证据文件为唯一写入
**HEAD**: 7d225480（checklist 072 提交）；工作树分析前干净
**测试预算**: `status=not-run-docs-only`——未运行任何测试套件；只运行确定性门与只读实测命令

## 1. 确定性门结果（本次实跑）

| 门 / 命令 | 结果 |
|---|---|
| `account-clause-coverage.py --spec-dir .specify/specs/072-client-self-improvement` | `status: ok`，exit 0；claimed=62/62，beyond baseline=0，FR lane 29/29；clause-uncovered pass(495 全在冻结基线内)，coverage-baseline-delta pass(0) |
| `validate-tasks.py tasks.md` | PASS，0 error / 0 warning，exit 0 |
| `validate-requirements.py requirements.md` | `status: ok`，0 error / 0 warning（36 定义行、10 shared strings、id 连续、ref 可解析） |
| `clause_extract.py contracts/*.md` | 62 条款 C-1…C-62，六文件全部 `form=md-bold-closed`（9+15+8+7+11+12） |
| plan 约束审计（`git diff 6dca65a5..HEAD` + `git status`） | plan 属主制品（plan/requirements/research/data-model/contracts/quickstart/feature-ref）**零改动**；工作树干净——无 substantive/undeclared 改动 |

## 2. 重点核查（简报第②段第 4 条，逐项实测）

| 重点 | 结论 | 证据 |
|---|---|---|
| 客户项目夹具与帽子判定 | 通过 | 帽子谓词实测存在于 `skills/internal/manage-feedback/SKILL.md`（= `.specify` 镜像）Routing flow 第 2 步：根级拥有 `templates/skills/shared/scripts/src/specify_cli` 五目录 → 框架项目；明确禁止以 `feedback/` 参与判定；与 FR-001 / C-1 / E10 / T003 五目录枚举一致。框架帽孪生夹具（C-59）按同一谓词构造。另见 A-3（owner 引证链瑕疵） |
| 三值武装态 / 五值披露闭集 | 通过 | 武装态三值（FR-002 / C-2 / E4）：armed/unarmed/ambiguous，解析顺序封闭（显式单元 > 唯一外部探针 > 其余），解析一次全程复用。披露五值（FR-009 / C-22 / E5-V20）：四非采集 token（STR-003/004/009/010）+ armed token（STR-007），与 Shared Strings 表逐项一致；无"第六值"泄漏路径（框架帽走 `skipped:` 形态，C-13/R6，不混入闭集） |
| 第五步采集契约 | 通过 | 071 现状实测：SKILL § 非交互路径为四步（base/start/note/receipt+report），071 FR-021 封闭四步——修订靶面真实。C-10 声明唯一修订（四步→五步）并附理由+代价；C-11 落为 `capture` 子命令；C-18 运行标识 = 记录头日期戳，`REVIEW_RUN_TIMESTAMP` 覆写点实测在 `git-delta-review.sh:529`；幂等键 `(unit, run)` 实测 `feedback-utils.py:783-793` 邻域（duplicate 不新增） |
| 打包排除 | 通过 | `feedback-utils.py:1871-1892` 实测：`kind: external` 无条件排除、计入 `excluded_external` 并无任何开关/环境变量可绕过；与 FR-010 / C-25 / SC-003 一致 |
| SI 客户主体 fail-closed | 通过 | `run-determination.py:1228-1246` 实测：对 `custom:` 单元返回 `persisted: False` + reason，不丢弃、不加宽契约；既有钉 `test_run_determination_engine.py::test_custom_unit_reports_honestly_instead_of_dropping`（≈:1393）在树。FR-015 / C-34 / C-36 与代码事实一致 |
| 四指标分母 | 通过（一处契约级精化，见 A-5） | C-43…C-50 / E9 逐项与 FR-021 对齐：捕获覆盖分母以武装时刻为界（C-49）、闭环只认 owner 文件 mtime 证据（C-44）、重复率 = (文件,严重度) 对粗代理（C-45）；`not-evaluated`=STR-006 零分母语义（C-48 / FR-023）。六项严重度词汇实测 `git-delta-review.sh:28`（blocking/important/suggestion/nitpick/question/praise），与 C-16 一一对应 |
| 071 闭合面不回退 | 通过 | 071 requirements 实测：FR-016 收尾六步、FR-018 三单元普查、FR-021 四步枚举、FR-011 过程报告代码段小节封闭清单、回执退出码字母表——072 侧 FR-025 / C-53 / SC-007 全部声明逐字保留，唯一授权修订 = 步骤枚举。C-61 守护清单（071 六套件 161 测试 + expression-compat C-5 + review-P1 + feedback/probe 族）与 tasks DoD-3 / T026 一致 |
| 命令面无新增 | 通过 | FR-026 / C-55 / C-62 封闭新增面：仅 `capture` 子命令 + `--format json` + `--client-unit` 参数 + `client-metrics` 只读动作；`--client-unit` 字面量由 plan R5 / C-6 裁决（feature-ref §5 留痕）。`templates/commands/improve.md` 实测已承认 `custom:` 目标路由（:23/:25），`docs/reference/commands/improve.md` 实测缺失（T018 新建，premise 成立） |

## 3. Checklist 消费账（40/40，无未处置项）

| 处置 | 项 | 说明 |
|---|---|---|
| 满足 | CHK001–CHK014、CHK017–CHK024、CHK026–CHK037、CHK039、CHK040（36 项） | 逐项对照 requirements 原文确认（详见 §5 逐条账） |
| 满足（带注记） | CHK015、CHK025、CHK038（3 项） | CHK015：单元命名实际由 FR-003+C-7 钉住（CHK 引文写 FR-004，属引文过宽，无缺陷）；CHK025：三分支场景齐备，"non-blocking exit" 措辞见 A-2；CHK038：运行标识源在 plan 层封闭（C-18/R2，feature-ref §5.1 留痕），需求层不重复守卫属设计内裁决，无缺陷 |
| 升格为 finding | CHK016（1 项） | → A-2（SC-002 退出码措辞歧义，plan 层 C-19 已消解，LOW） |

## 4. 跨制品漂移 / 覆盖 / 一致性检查（29 FR / 7 SC / 62 条款）

- **覆盖**：29/29 FR 有契约条款引用组与 tasks 行；7/7 SC 有条款 + 验证载体；62/62 条款被 tasks `[green:]` 恰认领一次（分区表 9+15+8+7+11+12 与 validate-tasks 双验证）。无需求无行、无行无需求。
- **漂移**：发现 4 处 LOW 级文档漂移（A-1、A-2、A-3、A-4）+ 2 项 INFO（A-5、A-6）；未发现 requirements↔plan↔contracts↔tasks 间的语义级矛盾，无宪法冲突（plan Constitution Check 十六原则 ✅ 行的声称与本次只读复核一致）。
- **重复**：无重复条款或重复需求；shared strings 引用规约（`[[STR-NNN]]` 不复制字面量）在 contracts / tasks / data-model 中一致执行。

## 5. Findings

### A-1（LOW，correction-class）data-model / plan 计数漂移（V 规则与状态迁移图数量）
- **位置**: `data-model.md:5`（"校验规则 V1–V24"）；`plan.md:27,69` 与 Constitution 复核查（"33 validation rules"、"2 state-transition diagrams"）
- **证据**: data-model 实有 V1…V32（grep 实测最大 V32，共 32 条）；状态迁移图实有 3 则（武装态解析 / 采集执行 / 条目生命周期），plan 写 2
- **影响**: 纯元数据计数，不影响任何条款语义或实现行为
- **建议**: implement 期以 `PLAN-EDIT: …；分类=minor` 一次性修正两处计数（plan.md 与 data-model.md 均属 plan 属主冻结面，minor 类可就地声明修订；不重写其余内容）。upstream-repair: 无（非阻塞）

### A-2（LOW，correction-class）SC-002"运行退出码为 0"缺限定词
- **位置**: `requirements.md` §SC-002（及 Measurement Source"各次运行的退出码"）
- **证据**: 非交互路径的合入门禁退出码字母表为 0/1/2（071 FR-008 / C-17），门禁拒绝时汇总命令退出 1；而采集步骤恒退出 0（C-19 / V23）。SC-002 的"运行退出码为 0"未限定是"采集步骤"还是"整次评审运行"，在含 blocking 条目的夹具里两种读法结论相反
- **影响**: plan 层已消解：C-19 钉死"capture step always exits 0"，SC-002 判定源取自采集步骤输出；实现与测试按 C-19 走不会产生错误行为，属措辞级歧义
- **建议**: implement 期 `PLAN-EDIT: requirements.md — SC-002 退出码限定为采集步骤；分类=minor`（可选；不做也不阻塞，C-19 已覆盖）

### A-3（LOW，correction-class）帽子五目录枚举的 owner 引证链断一格
- **位置**: FR-001 / C-1 / E10 / tasks T003 均引 `.specify/shared/definitions/dogfooding-definitions.md` § 2.1 为枚举 owner；`manage-feedback/SKILL.md` Routing flow 第 2 步亦称"enumeration owned by … § 2.1"
- **证据**: 实测 § 2.1（`shared/definitions/dogfooding-definitions.md:100-131`）通篇为编辑侧纪律与路径解析陷阱，**不含**五目录枚举；枚举的实际可运行形态在 manage-feedback SKILL 路由第 2 步（含"不得 gate 于 feedback/"、"目录名不带尾部斜杠"两条操作规则）
- **影响**: 实现 capture 的帽子判读时，按 C-1 打开 § 2.1 找不到判据，需落到 SKILL——语义正确但 owner 链与 One Source Of Truth 不符（枚举事实有两处文本：SKILL 源 + `.specify` 镜像，无真正的 owner 文档段落）
- **建议**: implement 期以 minor PLAN-EDIT（或在 T006 行内声明）把引证改为"§ 2.1 + manage-feedback 路由第 2 步"双指，或推动把枚举补进 § 2.1（后者超出本特性编辑面，记为回抛编排者的可选项）。upstream-repair: 无（非阻塞）

### A-4（LOW，correction-class）tasks.md T016 小节标题笔误
- **位置**: `tasks.md:230` "### Tests for User Story 6-4"
- **证据**: 该节为 US4 测试段（Phase 6: User Story 4，T016 [US4]），"6-4"为笔误
- **影响**: 无（validate-tasks 不检标题文本；区块与 blockedBy 拓扑正确）
- **建议**: implement 期随手修正（tasks.md 不属 plan 属主冻结清单，DoD-6 未列，无需 PLAN-EDIT）

### A-5（INFO）重复发现率分母的契约级精化未回填需求层
- **位置**: FR-021（分母 = 客户条目总数）vs `data-model.md` E9（分母 = 外部条目总数 − 不可读记录排除数）/ C-50
- **证据**: 所指记录不可读的条目从分子分母同排除并披露（C-50 / V31），FR-021 原文未写该排除；FR-023 的"不省略该行 + 口径披露"由 C-50 落地
- **影响**: 无矛盾——契约收窄是 FR-023 诚实性义务的精化，不构成第二读法
- **建议**: 无需动作；若 A-2 的 PLAN-EDIT 发生，可顺带一句，不做亦可

### A-6（INFO）运行标识源（CHK038）在 plan 层封闭，需求层无守卫
- **位置**: FR-007 字段集含"本次运行的标识"但未钉来源；C-18 / R2 钉为记录头日期戳（可用 `REVIEW_RUN_TIMESTAMP` 覆写）
- **证据**: 实测覆写点存在（`git-delta-review.sh:529`）；feature-ref §5.1 记为已披露 plan 裁决
- **影响**: 无——与 FR-026"参数字面名归 plan 裁决"同型，属设计内分层；CHK038 按"plan 层已封闭、可追溯"销项
- **建议**: 无需动作

## 6. 上游修复需求

- **CRITICAL/HIGH: 0** —— 无 upstream-repair-required 项，analyze 门可放行 implement。
- A-1 / A-2 / A-3 触及 plan 属主冻结面，均为 minor 级 correction-class，可在 implement 期按 DoD-6 的 `PLAN-EDIT` 协议就地声明修订；不修订也不阻塞任何任务行。A-4 在 tasks.md，随手可修。
- 其余全部制品（requirements 语义面、六份契约、tasks 拓扑、quickstart 豁免措辞、checklist 40 项）未发现需要回抛编排者裁定的事项。

## 7. 裁决

```
GATE: CRITICAL=0 HIGH=0
```

## 8. 逐条 checklist 处置账（40 项）

| 项 | 处置 | 依据 |
|---|---|---|
| CHK001 | 满足 | FR-001：owner 引证 + 禁第二判据 + `feedback/` 不参与；实测 manage-feedback 路由第 2 步谓词在树（A-3 仅为引证链瑕疵，不改变满足判定） |
| CHK002 | 满足 | FR-006 合取触发 + FR-009 全情形披露 |
| CHK003 | 满足 | FR-007 封闭字段集（5 项）+ 禁止内容（意见正文/逐文件清单/回执逐文件字段/文件计数）双半俱在 |
| CHK004 | 满足 | FR-024 四红线逐条同等覆盖客户侧条目 |
| CHK005 | 满足 | FR-009 四 token 闭集 + 零条目 + 禁零填充逐情形挂载 |
| CHK006 | 满足 | FR-029 模拟客户项目夹具定义 + 排除框架仓自测 |
| CHK007 | 满足 | FR-011 三载体闭集 + 恰好一 + 禁第四载体 |
| CHK008 | 满足 | FR-013 三项既有事实 + 不改原子清理语义 |
| CHK009 | 满足 | FR-002 三值 + 封闭解析顺序 + 一次解析全程复用 |
| CHK010 | 满足 | FR-006 明确"不按意见条数、按文件数或按严重度各写一条" |
| CHK011 | 满足 | FR-007 + clarify 裁决（六项含零、不省不并）；实测六级词汇于脚本 :28 |
| CHK012 | 满足 | FR-002/FR-009 未武装两子情形（无探针对象 → 注入指引；注册表不可用 → 重初始化/升级指引） |
| CHK013 | 满足 | FR-009"与适用性取值同时可见"；C-22 同 |
| CHK014 | 满足 | FR-021 第三条：owner 文件变更证据 + 具名非证据（processed/ignored、carried-by-spec-*、open-unverified） |
| CHK015 | 满足（带注记） | `custom:<owner>/<name>`+`custom-unit` 由 FR-003 + C-7 钉住；CHK 引文点名 FR-004 属过宽，无实质缺口 |
| CHK016 | 升格 A-2 | 披露字面量两侧一致；歧义在"运行退出码"限定词（plan C-19 已消解） |
| CHK017 | 满足 | FR-005 唯一修订 + FR-025 修订面封闭 |
| CHK018 | 满足 | FR-026 三入口分工 + 不可承载时报缺口不加命令 |
| CHK019 | 满足 | FR-023 与 US5.2 同为 STR-006 `not-evaluated` + 原因 |
| CHK020 | 满足 | SC-001 确定性命令输出比对、不读条目正文 |
| CHK021 | 满足 | SC-005 路径集合比对 + 两次呈报同读数 |
| CHK022 | 满足 | SC-007 逐字文本/结构断言判据明列 |
| CHK023 | 满足 | FR-021 每条分子/分母/来源 + C-43；全为既有记录派生 |
| CHK024 | 满足 | SC-006 + tasks 四字段（命令行/真实输出/退出码/失败计数）落 `notes/red-first-evidence.md` |
| CHK025 | 满足（带注记） | US2 场景 1-3 + SC-002 覆盖三分支；exit 措辞见 A-2 |
| CHK026 | 满足 | FR-008 三不变量逐条独立成句 |
| CHK027 | 满足 | SC-003.3 + Edge Case vendored + C-13 skipped 形态（R6） |
| CHK028 | 满足 | Edge Cases：exit 1 照常采集 / exit 2 零条目+counts-unavailable / 引擎拒绝写盘同披露；同秒幂等；单元消失 |
| CHK029 | 满足 | Edge Case + FR-020：不回填、遗留可读不重写、口径只覆盖落地后 |
| CHK030 | 满足 | Edge Case：仅显式指定单元被采集 |
| CHK031 | 满足 | FR-019 显式定义"持续"三组合 + 禁调度器/常驻/定时器/后台 |
| CHK032 | 满足 | FR-027 编辑面封闭 + 再生成/镜像产出 + 探针重编译顺序 |
| CHK033 | 满足 | FR-028 客户中立 + 两条既有负向断言逐字保留 + 断言净增 |
| CHK034 | 满足 | FR-001/002/015 全部 by-reference（本次实测四类依赖均在树：帽子谓词、探针注册面、fail-closed 引擎、打包排除） |
| CHK035 | 满足 | Assumptions A3 记录客户项目形态，形态外属范围外 |
| CHK036 | 满足 | FR-025：开放项保持开放、意见级计数不依赖回执区分 |
| CHK037 | 满足 | FR-002 + clarify Q5：显式指定只消解歧义、MUST NOT 豁免探针检查；C-3/C-6 同 |
| CHK038 | 满足（带注记） | plan C-18/R2 钉死确定性来源（记录头日期戳），feature-ref §5 留痕；→ A-6 |
| CHK039 | 满足 | FR-021/FR-023 粗代理标注随行、不得表述为复现率 |
| CHK040 | 满足 | Edge Case + C-28：只可框架向移动、移动须呈报 |
