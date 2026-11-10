# Analyze Findings — Round 2 · Worker W2

**特性**: 097-speckit-migrate-command · **轮次**: round 2（修复后重过门，并发波） · **日期**: 2026-11-10
**读域（文件级、互斥）**: `plan.md`、`data-model.md`、`quickstart.md`、`contracts/migrate-cli.md`、`contracts/migrate-engine.md`、`contracts/migrate-template.md`
**性质**: 只读检测子报告，不做修复。round-1 findings 的重裁与 MEDIUM/LOW residue 清单由 round-2 合并报告（协调方）持有——本行读域不含任何 round-1 findings 文件，本文件不声称关闭 round-1 条目。

## 方法与机械读数

- 检测通道：A 重复 · B 歧义 · C 欠定 · D 宪法对齐 · E 覆盖 · F 不一致 · G 特性相关性 · I 决策张力记录，另加 Markdown 结构（表格/标题）与仓内路径存在性核查。
- 决策张力确定性校验（只读）：`validate-decision-tensions.py --spec .specify/specs/097-speckit-migrate-command --json` → `status: ok`；2 条记录；`dtr-anchor` / `dtr-section-missing` / `dtr-record-incomplete` / `dtr-tension-id` / `dtr-rejected-form` / `expected-sacrifice-unmapped` 六类标签全部 pass，0 findings。
- 传播面：下列 findings 均传播到 tasks/实现或回执/测试契约，无 `none` 行；severity 按该传播面的实际影响取 MEDIUM/LOW。
- C/H 验证波：本子报告未产出 CRITICAL/HIGH，无需为本行派发独立验证器；合并报告的全局验证波不受影响。

## Findings（14 行：0 CRITICAL / 0 HIGH / 6 MEDIUM / 8 LOW）

| ID | Severity | 锚点 | 一句话事实 | 建议归属 |
|----|----------|------|------------|----------|
| W2-01 | MEDIUM | `data-model.md:108`（E-6）、`data-model.md:113`（E-7）、`contracts/migrate-engine.md:15`（C-2）、`:43-50`（C-4） | E-6 的 `framework-source` 影响列称「模板/技能/代理参照面对照仍可用（见契约 C-4）」，但 C-4 是客户端参照树规则，E-7 又明确框架源不建参照树、资产期望态由 C-2 的 sync-mirrors 镜像对回答——框架源分支的期望态来源在两处互相抵触。 | data-model E-6 / migrate-engine C-2（统一为 C-2 口径并改正指针） |
| W2-02 | MEDIUM | `plan.md:151-166`（WP 表）、`plan.md:33`、`plan.md:200` | Work Packages 表 14 行合计只指派 23/25 个 FR：FR-004、FR-013 未出现在任何 WP 的 FR 列，FR-020 只挂在验收 WP12；与同文件两处「25/25 FR 覆盖」主张之间缺少 WP 级载体。 | plan § Work Packages（或 feature-ref 的 FR→WP 矩阵） |
| W2-03 | MEDIUM | `data-model.md:23`（E-1 mechanism）、`data-model.md:122`（E-8 锚点行）、`contracts/migrate-engine.md:32`（C-3 锚点行） | `mechanism` 值 `mirror-engine` 在 C-3 的处置映射中从不被指派；同一「锚点搬迁」的机制在 E-8 被钉为 `relocate`、在 C-3 又写成 `relocate / anchor-engine`——机制 token 映射不闭合。 | migrate-engine C-3 / data-model E-8 |
| W2-04 | MEDIUM | `data-model.md:41`（E-2 workspace）、`data-model.md:55-71`（E-3 字段表）、`contracts/migrate-cli.md:62-65`（C-4） | 回执 `workspace` 字段三处不一致：E-2 称「回执中记录」、C-4 把 `workspace` 绝对路径列为回执易变字段，E-3 的回执 schema 却无该字段；且 apply 模式下 stdout 包络 `receipt` 字段的内容未规定。 | data-model E-3 / migrate-cli C-4 |
| W2-05 | MEDIUM | `contracts/migrate-engine.md:80`（C-7 续跑）、`:36`（C-3 converged 行）、`data-model.md:26`（E-1 status）、`data-model.md:48`（E-2） | C-7 要求把「旧回执 done 且目标已等于期望」的项「记 `converged`」，但 C-3 说 converged 项不进入计划、E-1 的 `status` 枚举无该值，E-1 指向的 E-2 也不含该排除规则——该记录没有可落位的载体。 | migrate-engine C-7 / data-model E-1 |
| W2-06 | MEDIUM | `data-model.md:59`（E-3 status）、`data-model.md:85` 与 `:90`（E-4 change） | E-3 的 `status=aborted` 与 E-4 的 `change=removed-stale` 在六份文件内均无任何触发/指派规则（仅出现在枚举与列举中），实现与回执测试无法判定何时产出这两个值。 | data-model E-3 / E-4 |
| W2-07 | LOW | `data-model.md:48`（E-2 状态转移）、`data-model.md:86`（E-4 digest） | data-model 内两处内部引用不可解析：E-2 写「apply 计划随 E-4 回执固化」（回执是 E-3，E-4 是 ArchiveEntry），E-4 的 `digest` 写「见实现说明」但六份文件无该锚点。 | data-model（改为 E-3 与可解析锚点） |
| W2-08 | LOW | `data-model.md:119`（E-8 标题行） | E-8 二级标题与表头行粘连在同一行（`## E-8 … ｜ dimension ｜ … ｜`），下一行直接是分隔行——维度 token 的「唯一 owner」映射表不会渲染为表格。 | data-model E-8 |
| W2-09 | LOW | `contracts/migrate-engine.md:62-63`（C-5） | C-5 复用边界表被第 62 行的「链接修复的职责说明」正文打断，其后的镜像/生成副本、goal/team、周期治理三行脱离表体——「禁止第二实现」的边界表不完整渲染。 | migrate-engine C-5 |
| W2-10 | LOW | `quickstart.md:5`、`plan.md:199` | quickstart 开头称「四段旅程」，但页面含场景 0–5 六节、plan 按「6 个场景」登记，计数口径未声明（哪四段算旅程、0 与 5 为何不计）。 | quickstart.md 开头（对齐场景计数或写明口径） |
| W2-11 | LOW | `data-model.md:94-102`（E-5）、`contracts/migrate-cli.md:31-39`（C-3） | outcome→exitCode 五值封闭表在 E-5 与 C-3 各存一份完整副本，而两处都声明 FR-019 为 owner——按 OSOT 决策测试这是第三份非机器再生的手写副本，改动需同步两文件。 | data-model E-5 / migrate-cli C-3（保留一处、另一处改指针） |
| W2-12 | LOW | `contracts/migrate-cli.md:71`（C-5 第二把钥匙） | 交互确认只钉住非 TTY 分支（blocked/exit 3）；「一次单批确认」的接受/拒绝输入协议与提示形态未定义，RED-first 的交互拒绝测试缺少可钉住的输入契约。 | migrate-cli C-5 |
| W2-13 | LOW | `contracts/migrate-template.md:7-13`（T-1） | T-1 称 frontmatter「只有两个键（与既有命令模板一致）」，但仓内 29 个源命令模板中 23 个带第三键（handoffs/scripts/argument-hint），两键形态只与 sanitize 等 6 个模板一致——理由句与仓内事实不符。 | migrate-template T-1（改写为「与 sanitize 等两键模板一致」） |
| W2-14 | LOW | `contracts/migrate-engine.md:32`（C-3 归档列）、`:80`（C-7）、`data-model.md:83-84`（E-4） | 搬迁条目的回执字段命名漂移：C-3/C-7 用 from→to 并称搬迁类 `archiveTo` 即 `to`，而 E-4 的 ArchiveEntry 只有 `path` / `archiveTo`，不存在 `to` 字段。 | migrate-engine C-7 / data-model E-4 |

## 已检查且未发现问题的面（absence evidence）

- **决策张力（I 通道）**：T-001/T-002 的字段完整、双极约束、ID 唯一递增、节位置（Constitution Check 之后、Project Structure 之前）与 expected_sacrifice 映射全部通过确定性校验器（2 条记录，0 标签失败）。
- **计数一致性**：9 entities + 5 invariants（`data-model.md` ↔ `plan.md:197`）；契约节段 C-1…C-7 / C-1…C-8 / T-1…T-6（↔ `plan.md:198`）；14 个 WP（`plan.md:25` 与 WP 表行数一致）；5 个维度（E-8 五行）；6 值处置（C-3）；4 类结局（E-5/C-3/C-4）；4 份再生副本（`plan.md:111-114` ↔ T-4）；镜像对 4+2=6（E-8 ↔ `migrate-engine.md:15`）。
- **路径一致性**：回执 `.specify/memory/migrate/receipts/<run-id>.json` 与归档 `.specify/archive/migrate/<run-id>/<rel>` 在 `plan.md:19`、E-3、E-4、`migrate-engine.md:76-77` 之间一致；exit-code 映射在 E-5、C-3、C-4 之间一致。
- **仓内存在性核查**：`templates/commands/`、四个命令副本目录、`shared/definitions/framework-map.md` 及其镜像、`skills/internal/sanitize-materials/SKILL.md` 及其镜像、`tests/contract/test_migration_distribution.py`、`test_qoder_command_frontmatter.py`、`test_anchor_layout_migrate.py` 均存在；`.specify/templates/commands/` 不存在（与「该镜像面已退役」一致）；`.specify/memory/migrate/`、`.specify/archive/migrate/` 不存在（与「apply 时创建」一致）。
- **占位符扫描**：六份文件无 `TODO` / `TKTK` / `???`。
- **quickstart 场景**：标题 0–5 与 `plan.md:199` 的场景清单逐项对应；未实现示例均带前提清单与钉住测试，0 前置与清理步骤标注已实测。

## Systemic observations

- **修复后结构损伤簇**：W2-08 与 W2-09 同属今日修复后的结构破坏（表头粘连、表格被正文打断），建议修复流程增加一步 Markdown 结构/渲染校验；此处只记模式，不提升任何单行 severity。
- **data-model 指针卫生簇**：W2-05 与 W2-07 合计指向 3 处不可解析/指错的内部引用，建议对数据模型做一次指针可解析性检查。
- **枚举值指派缺口簇**：W2-03 与 W2-06 合计 4 个 schema 值（`mirror-engine`、`anchor-engine`、`aborted`、`removed-stale`）缺触发条件，建议在 C-3/E-8 补一张 token→触发条件映射。

## 证据边界（未覆盖项）

- 未读（超出本行读域）：`requirements.md`、`tasks.md`、`feature-ref.md`、`research.md`、`checklists/`、feature registry/detail、constitution、round-1 与并发 W1/W3 的 findings。
- 未运行：`account-clause-coverage.py`（合并报告的 fixed read-only step）；checklist H 通道（`checklists/` 不在读域）；`COMMAND_BASELINE` 当前取值未开箱核对（仅确认持有文件存在）。
- 本文件 finding 可被合并报告去重、重编号与重定级；round-2 的 rerun delta 与 MEDIUM/LOW residue 清单由协调方按 analyze-artifacts § Rounds 生成。

## Wrap-up 记账

- 唯一写面：本文件（新建）。检测期间六份工件及其余仓内文件全部只读；未运行写命令；未 push；既有脏文件未动。
- 写入前 `git status --porcelain` 快照：4 项 untracked（`checkpoints/` 2 项 + 并发 W1/W3 findings 2 项）；写入后应仅新增本文件 1 项。
- 异常：无（无 `ANOMALY` 触发）。引擎级 Wrap-up（Run Determination / Exec Quant / Feedback Record）需本轮 RUN_ID，由协调方记账；本环境未提供 RUN_ID。
