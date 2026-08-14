# Contract: Render Pipeline

契约对象:`src/specify_cli/__init__.py` 的 agent 渲染路径(init 时替代 `ensure_per_file_agent_links()`)。

## R-1 输入与输出

输入:`.specify/agents/{templates,instances}/*.agent.md`(中立源)+ `_AGENT_METADATA_MAPPING` 的 render 行。输出:目标目录下的真实常规文件(MUST NOT 为符号链接,FR-011)+ `.render-manifest.json`(E4)。annotated 行工具与 FR-014 情形 MUST 静默跳过:不报错、不产生空目录。

## R-2 渲染语义

- frontmatter:按 M-4 转换;无对应物字段按 M-5 跳过并汇总;`supervisor`/`capacity-scope` 不落盘(C-6)。
- body:原样承载,不做任何改写(Feature 033 的正文渲染是独立后续,不在本管线)。
- 仅 `*.agent.md` 进入渲染;`execution/` 层与子目录 MUST NOT 分发。

## R-3 同名与优先级

templates 与 instances 同名时,instances 胜出,只产出一份(FR-017)。清单 `entries` 的 `source` 字段 MUST 记录实际来源层。

## R-4 确定性

相同中立源 + 相同工具 MUST 产出逐字节一致的产物(FR-015)。清单中仅 `rendered_at` 允许随时间变化;产物内容 MUST 不含时间戳、随机量或环境相关值。集成测试以"连续渲染两次 + 逐字节比对"钉住(SC-005)。

## R-5 漂移处理(FR-021,状态机见 data-model.md §状态迁移)

再渲染时对目标目录中每个与本次渲染同名的既有文件:

| 情形 | 行为 |
|------|------|
| 在清单 且 哈希一致 | 直接覆盖刷新 |
| 在清单 且 哈希不一致(手改) | 备份至 `.specify/agents/.backups/<tool>/<name>.<UTC-compact>.agent.md`,覆盖新渲染,备份路径进 init 反馈 |
| 不在清单 且 无中立源对应 | 视为用户资产,MUST NOT 触碰 |
| 不在清单 但 有中立源对应(新增 agent) | 正常渲染落盘 |

## R-6 失效清理(FR-020)

清单中存在、但中立源已删除的条目:其产物 MUST 被删除;删除前若文件哈希与清单不一致(曾被手改),MUST 先按 R-5 备份。

## R-7 工具切换(FR-022)

以工具 B 初始化曾以工具 A 初始化的项目时,A 的产物位于 A 的目录,B 只写 B 的目录;MUST NOT 出现跨目录读写。A 目录的残留由用户或后续清理命令处置,本管线不静默删除其他工具的目录。

## R-8 迁移路径(FR-019)

升级路径 MUST 将既有逐文件 agent 软链接(含历史整目录链接)替换为渲染产物:先解除链接,再按本契约渲染;不得残留悬空链接。集成测试以"旧布局项目 → init → 断言零符号链接"钉住(SC-002/SC-006)。

## R-9 反馈(FR-018)

init tracker MUST 输出:目标工具、渲染的 agent 数、备份数、未承载意图汇总(按 agent)。

## R-10 占位符闸(FR-026)

渲染输入若含 `{{...}}`(C-7 违规)MUST 拒绝该文件并报告,不产出半截产物。

## R-11 退役语义

`_AGENT_LINK_DIRS` 与 `ensure_per_file_agent_links()` 退役;其承载的语义(实例优先、失效清理、仅 `*.agent.md`、execution 层隔离)由 R-2/R-3/R-5/R-6 承接。退役顺序:先改写全部引用该函数的测试,再删函数;旧名登记按仓库 rename/retire 纪律处理。
