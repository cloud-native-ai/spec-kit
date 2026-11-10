# Analyze Findings — Round 2 — W1

**Feature**: 097-speckit-migrate-command
**Stage**: analyze 第二轮（修复后重过门；并发波 W1）
**Date**: 2026-11-10
**Read domain**: `.specify/specs/097-speckit-migrate-command/requirements.md`；`.specify/specs/097-speckit-migrate-command/checklists/requirements-quality-2026-11-10.md`
**Method**: analyze-artifacts 检测通道 A（重复）/ B（歧义）/ C（欠指定）/ E（覆盖缺口）/ F（不一致）+ H（checklist 问责）；D（宪法对齐）在 W1 读域内只核对 requirements 自身对宪法条款的引用与声明，不跨文件复核；G/I、clause coverage accountant、plan/tasks/registry 交叉检查不在 W1 读域。
**Round-2 declaration**: 本轮为**全严重度重裁**（round-1 W1 的 24 条 + 当前文本全量检测），不是 C/H-only；因此同时给出 round-1 C/H 复核、M/L 残差行与 round-2 新发现。
**Same-author**: 两份输入由本轮 SDD 线前序阶段代理撰写；本波次为驱动派发的独立只读上下文，未参与撰写，满足 same-author 委派条件。本轮新增 C/H 为 0，不触发本波次自我验证；既有 HIGH 修复的独立验证仍由验证波次承担。
**Boundary**: 产物只读；唯一写面为本文件（含 Wrap-up 记账）。未修改 requirements.md、checklist 或任何其他文件。

## 1. Round-1 C/H 复核（W1 读域，6/6 已修复）

| ID | 原严重度 | 复核结论 | 当前证据锚点 | 复核事实 |
|---|---|---|---|---|
| W1-01 | HIGH | fixed | requirements.md:134 §FR-018；:116 §FR-006 | FR-018 已明示「干跑回执 MUST 以输出流承载、不落盘（FR-006 零写入的适用形态）」，与 FR-006 的零写入 MUST 不再冲突。 |
| W1-02 | HIGH | fixed | requirements.md:134 §FR-018；:139 §FR-020 | FR-018 字段清单已含「源版本与目标版本、运行状态、续跑标识（续跑时指向被接续的运行）」；FR-020 已定义源版本读 `.specify/source.json`、缺失/不可读记 `unavailable` 并写明原因。 |
| W1-03 | HIGH | fixed | requirements.md:145 §FR-023；:172 §SC-001 | FR-023 的构成清单已补「已编辑的模板文件、被删除的镜像脚本文件、缺失或断链的兼容链接」，并 MUST 覆盖 SC-001 的全部五类维度。 |
| W1-04 | HIGH | fixed | requirements.md:135 §FR-019 | FR-019 已要求结局以机器可读 token 载明（文本输出与 `--format json` 包络均含），clean 与 applied 共用退出 0 不再使结局不可判定。 |
| W1-05 | HIGH | fixed | requirements.md:135 §FR-019 | FR-019 已给优先级聚合规则：存在任一 `refuse` / `blocked` 项或执行期 I/O 失败 → `blocked`（退出 3），否则 `applied`（退出 0）；干跑按计划空/非空取 `clean` / `planned`。 |
| W1-06 | HIGH | fixed | requirements.md:115 §FR-005 | FR-005 已把「当前已安装版本」判定为运行本命令的 CLI 进程所加载的包资源（`get_resource_path()`），并区分框架源工作区（`skills/external/` 为目录，以自身声明与脚本副本为源）与客户端模式（MUST NOT 读工作区可能过期的副本）。 |

## 2. Round-2 新发现

| ID | Severity | Anchor | 一句话事实 | 建议归属 |
|---|---|---|---|---|
| W1-25 | MEDIUM | requirements.md:125 §FR-012；:178 §SC-007；checklist:37 CHK015 | FR-012 要求在同一变更内把 sanitize Migration lane 的定位声明收敛为「周期复检兜底」，但 9 条 SC 与 Measurement Sources 都没有该声明的验收面（SC-007 只断言迁移残留零发现与 goal/team 静止指针），round-1 的 `covered-by FR-012` 处置构成循环引用。 | requirements.md（扩 SC-007 或新增 Measurement Source；若定为评审型验收，须在 requirements 明示）。 |
| W1-26 | MEDIUM | requirements.md:130 §FR-014；:116 §FR-006 | FR-014 把 `converged`（已收敛，零写入）列为差异项的处置结果，但需求未定义差异项在何种情形下零写入即算收敛，也未声明 FR-006 计划中的「拟处置」是否必须取自同一六值集，实现可把未处置差异标为 `converged` 而计划与回执仍自洽。 | requirements.md（clarify：定义 `converged` 的触发条件与计划/回执的处置词表关系，或从执行性处置集移除该值）。 |
| W1-27 | MEDIUM | requirements.md:116 §FR-006；:172 §SC-001；:182–192 Measurement Sources | FR-006 要求同一棵树的重复干跑产出逐项相同的计划，但 9 条 SC 与 Measurement Sources 均未给出该确定性的验收断言（SC-001 只测干跑零写入与应用后第二次运行 `clean`），稳定排序无从判红。 | requirements.md（在 SC-001/SC-003 或 Measurement Sources 补「重复干跑逐项一致」断言）。 |
| W1-28 | LOW | checklist:6 | checklist 头部的机械读数与需求现状不符：requirements.md 实为 236 行 / 36,445 B（清单记 35,235 B，修复轮后未更新），Clarifications 实为 6 + 5 问（清单记 6 + 4，且 Clarifications 节自 clarify 提交后未改动）。 | checklist（重生成或更正头部读数）。 |
| W1-29 | LOW | checklist:11 | checklist 的 Detection path 声明三路「作用域不相交」，但同段枚举的 Detector B 与 Detector C 重叠于 FR-024/FR-025 与 SC-003…SC-005，且后文又记录「2 组双检测器重叠合并」，不相交声明与自身枚举矛盾。 | checklist（更正检测路径记录）。 |

## 3. Round-1 M/L 残差（全量列举，18 条）

| ID | 原严重度 | Status | Disposition | 理由 / 当前锚点 |
|---|---|---|---|---|
| W1-07 | MEDIUM | open | deferred | 钉名 owner 缺席/执行报错或维度不可评估时的降级语义仍未定义；Edge Cases 只有符号链接一例（requirements.md:99）。 |
| W1-08 | MEDIUM | open | deferred | FR-015（:131）未定义单批确认的覆盖范围/拒绝粒度，也未定义交互终端下 EOF、空回车、取消的结局。 |
| W1-09 | MEDIUM | open | deferred | FR-015（:131）钉名唯一 owner，但未要求从 confirmation-gates 派生/导入并以漂移测试钉住；命令内复制清单仍可通过现有验收。 |
| W1-10 | MEDIUM | open | deferred | 「零写入/哈希不变/逐项零差异」的比较单元（内容哈希、模式/可执行位、符号链接目标、空目录、权限变更）仍未钉名；SC-001（:172）「应用前后文件树哈希对照」措辞与干跑零写入的测量点不一致。 |
| W1-11 | MEDIUM | fixed | fixed | 修复轮 W1-05 的 FR-019（:135）已把「执行期 I/O 失败」并入 `blocked`（退出 3）；六值处置层的 I/O 失败细分仍由设计层承载。 |
| W1-12 | MEDIUM | open | deferred | FR-007（:117）维度①与④对同一镜像文件仍可能双重命中；归属、去重与处置优先级未定义。 |
| W1-13 | MEDIUM | open | deferred | FR-005（:115）owner 清单仍不含 init 的 `copy_local_templates` / `rewrite_paths` / `generate_commands`；FR-007 未定义平台资产变体（sh/ps、工具命令目录交集）的选择规则。 |
| W1-14 | MEDIUM | fixed | fixed | 修复轮 W1-06 的 FR-005（:115）已补「框架源工作区（`skills/external/` 为目录）以自身声明与脚本副本为源（宪法 XI）」与客户端副本禁令。 |
| W1-15 | MEDIUM | open | deferred | FR-017（:133）/SC-006（:177）仍只操作化「已归档未写」与「已归档且已写」；写入中、回执未更新及中断后工作区被用户改动的续跑判定未定义。 |
| W1-16 | MEDIUM | open | deferred | FR-023（:145）已补齐七类构成并绑定五维，但构成类到具名注册表条目/检查器发现的逐项映射、构建时实时派生机制、以及 SC-004 的「类/代」计量单位仍开放。 |
| W1-17 | MEDIUM | open | deferred | FR-023（:145）/SC-003（:174）未定义「已最新夹具」的构造基（init 现场投影树还是 migrate 收敛后的树）。 |
| W1-18 | MEDIUM | open | deferred | 两写者并发回执测试仍只落在 Edge Cases（:100）与 A6（:231）；FR-018（:134）只要求一文一件，无对应 SC/Measurement Source 的可转红断言。 |
| W1-19 | MEDIUM | open | deferred | SC-007（:178）仍未指名 sanitize 迁移类检查器/动作集合；FR-013（:126）的「静止指针」无字段/固定文本形态。 |
| W1-20 | MEDIUM | open | deferred | FR-003（:110）缺 `.specify/` 的拒绝路径与 FR-019 的输入错误退出 2 仍无 SC 或 Measurement Source。 |
| W1-21 | MEDIUM | open | deferred | FR-005（:115）三禁令中仅「按源版本号选择路径」经 SC-004 变异转红；「不读 `.specify/version`」「不按模板指纹猜测」无负向断言。 |
| W1-22 | MEDIUM | open | deferred | FR-010（:123）的「MUST NOT 读写 sanitize 发现台账」仍无 SC/Measurement Source；文件树哈希无法证明未读台账或未触发 `--action collect`。 |
| W1-23 | MEDIUM | open | deferred | Runtime Stack（:153–158）Premises 列引用 EP-001…EP-004，requirements.md 内仍无 Premises 定义或 owner 指针。 |
| W1-24 | LOW | open | deferred | FR-001（:108）/STR-003（:200）仍未定义显式 `--dry-run` 与裸默认的等价性，以及 `--dry-run` 与 `--apply` 并用时的结局。 |

## 4. Checklist Accountability (H 通道)

`unchecked=39; dispositioned=39 (raised-as-finding=23, covered-by=16); undispositioned=0; 39 − (23 + 16) = 0`
`[Gap] subset: unchecked=16, raised=10, covered-by=6, undispositioned=0`

**计数更正**：round-1 W1 报告 `[Gap] 15/15`；本轮机械重数（`grep '^- \[ \] CHK' | grep -c 'Gap'`）为 **16** 条（CHK003/008/009/012/015/019/020/021/022/023/025/026/028/036/037/038），全部已处置；round-1 的 15 为计数错误，记于此不静默。

```
CHK001 disposition: covered-by requirements.md § FR-005
CHK002 disposition: covered-by requirements.md § FR-005
CHK003 disposition: raised-as-finding W1-07
CHK004 disposition: raised-as-finding W1-21
CHK005 disposition: raised-as-finding W1-12
CHK006 disposition: raised-as-finding W1-24
CHK007 disposition: raised-as-finding W1-08
CHK008 disposition: raised-as-finding W1-08
CHK009 disposition: raised-as-finding W1-09
CHK010 disposition: covered-by requirements.md § FR-019
CHK011 disposition: covered-by requirements.md § FR-019
CHK012 disposition: covered-by requirements.md § FR-019
CHK013 disposition: raised-as-finding W1-10
CHK014 disposition: covered-by requirements.md § FR-018
CHK015 disposition: raised-as-finding W1-25
CHK016 disposition: covered-by requirements.md § SC-007
CHK017 disposition: raised-as-finding W1-19
CHK018 disposition: raised-as-finding W1-10
CHK019 disposition: raised-as-finding W1-13
CHK020 disposition: covered-by requirements.md § FR-005
CHK021 disposition: raised-as-finding W1-07
CHK022 disposition: raised-as-finding W1-13
CHK023 disposition: raised-as-finding W1-10
CHK024 disposition: covered-by requirements.md § SC-001
CHK025 disposition: covered-by requirements.md § FR-020
CHK026 disposition: covered-by requirements.md § FR-018
CHK027 disposition: raised-as-finding W1-15
CHK028 disposition: raised-as-finding W1-15
CHK029 disposition: covered-by requirements.md § FR-016, § FR-017
CHK030 disposition: raised-as-finding W1-16
CHK031 disposition: raised-as-finding W1-16
CHK032 disposition: covered-by requirements.md § FR-023
CHK033 disposition: raised-as-finding W1-17
CHK034 disposition: raised-as-finding W1-16
CHK035 disposition: covered-by requirements.md § Measurement Sources & Collection Methods
CHK036 disposition: raised-as-finding W1-18
CHK037 disposition: covered-by requirements.md § FR-002, § FR-025
CHK038 disposition: covered-by requirements.md § FR-022, § SC-009
CHK039 disposition: raised-as-finding W1-19
```

## 5. Coverage Summary（W1 读域）

| Item | Reading |
|---|---|
| FR | 25（FR-001…FR-025） |
| SC | 9（SC-001…SC-009） |
| STR | 4（STR-001…STR-004；全部 `[[STR-NNN]]` 引用可解析） |
| User Stories / Edge Cases / Assumptions | 4 / 10 / 11（A1–A11） |
| Clarifications | 2 场，**6 + 5 = 11 问**（checklist 头部记 6 + 4，见 W1-28） |
| requirements.md | 236 行 / 36,445 B（`wc -lc`，2026-11-10） |
| checklist | 80 行 / 14,779 B；39 条全部未勾选；[Gap] 16 条 |
| SC→FR 映射 | 9 条 SC 均可回指 FR，无孤立 SC |
| 无专属 SC / Measurement Source 的 FR 分支 | W1-20（FR-003 输入错误）、W1-22（FR-010 台账不可变）、W1-25（FR-012 lane 定位声明）、W1-27（FR-006 重复干跑确定性）；FR-002/FR-022 由 FR-025/FR-022 自身的验收断言覆盖 |

## 6. Feature Linkage Summary（W1 读域）

- 绑定：Feature 024（Specification Workspace Versioning，Draft），见 requirements.md:14-17 与 checklist 头部；requirements 明示本规格是 024 的首个子规格。
- 024 原设想的 `.specify/version`、版本→迁移注册表与 `specify upgrade` 由本规格的「声明驱动期望态 + 一次直达」取代（FR-005、FR-020）。
- registry 集成（024 详情 related-specifications、索引行 Last Updated）在 requirements.md:17、:218 仍记为待办恢复点；索引/详情实际对齐状态不在 W1 读域，G 通道归其他波次。

## 7. Constitution Alignment（W1 域内）

- 在读域内未发现新的 CRITICAL 级宪法冲突。
- FR-001 / FR-022 显式绑定宪法 XXI；FR-005 显式引用宪法 XI（自举）；FR-015 的确认清单唯一 owner 与宪法 XIV 方向一致；FR-018 的目录登记要求与宪法 XVII 方向一致。
- 跨文件 D 通道复核（constitution.md 原文逐条比对）不在 W1 读域，由驱动侧或其他波次承载。

## 8. Metrics

- Round-1 W1：24 条（CRITICAL 0 / HIGH 6 / MEDIUM 17 / LOW 1）。
- Round-2 复核：6/6 HIGH 复核为 fixed，0 条 open HIGH；0 条 CRITICAL。
- Round-2 新发现：5 条（0 CRITICAL / 0 HIGH / 3 MEDIUM / 2 LOW）。
- Round-1 M/L 残差：18 条中 2 条 incidental fixed（W1-11 经 FR-019、W1-14 经 FR-005），16 条 open（15 MEDIUM + 1 LOW），deferred 出 C/H 修复轮。
- W1 读域当前开放项合计：21 条（18 MEDIUM + 3 LOW），全部不阻断 analyze 门（无 C/H）。
- Detection pass mapping：A=0；B=W1-26、W1-29；C=W1-25、W1-27；E=W1-25、W1-27；F=W1-28、W1-29；H=39/39（[Gap] 16/16）。
- HIGH validation：本轮无新增 HIGH；既有 HIGH 的修复由修复轮确认（11/11 confirm），独立验证仍归验证波次。
- Rerun delta vs round-1 W1：6 HIGH fixed；2 MEDIUM incidental fixed；16 MEDIUM/LOW open；新增 5 条（3 MEDIUM / 2 LOW）；[Gap] 计数由 15 更正为 16。

## 9. Wrap-up 记账

- 单元：analyze wave W1，round 2（unit: skill:analyze-artifacts@097）。
- 输入：requirements.md 236 行 / 36,445 B；checklist 80 行 / 14,779 B（checklist 头部对 requirements.md 的读数已过时——W1-28）。
- 检测通道：A、B、C、E、F、H（D 在读域内有限核对）。
- 产物：本文件（唯一写面）；未修改 requirements.md、checklist 或其他文件。
- 结果：0 CRITICAL / 0 open HIGH；5 条新发现（3 MEDIUM / 2 LOW）；16 条 round-1 M/L 残差 open（deferred）。
- 验证：本轮无新增 C/H，不生成 C/H 验证请求；既有 HIGH 修复状态见 § 1。
- 运行判定 / exec-quant / feedback：本波次未获得 RUN_ID 与复杂度参数，按 round-1 W1 先例由驱动侧统一记账，未生成独立引擎记录。
- 异常：无异常；无即修（nothing to report is something to say）。
