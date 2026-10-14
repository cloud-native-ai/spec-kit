# Contract: run-team 行为平价对映表(contracts/run-team-parity.md)

义务对映真源(spec FR-010 / SC-003):左列取落盘时点 `templates/commands/team.md` 中 **run 语义的全部程序性义务**——主体为 § Run Mode(L71–84),含路由流中 run 直接承载的一条(team not found → 提示 create,L43);逐条映射到 run-team SKILL.md 的落点,强度列判定 equal/stricter。落盘后本表的义务真源由 team.md 移交 run-team SKILL.md;team.md 残留文本仅作引用。行为类条款——由评审强制与 B-3 对映核对承担,不声称测试覆盖。

| # | 义务(源锚:team.md § Run Mode) | run-team 落点 | 强度 |
|---|--------------------------------|---------------|------|
| P-1 | Load:`.specify/teams/<slug>/team.md`;无匹配 → "team not found" + 提示 create(源锚:路由流 L43,run 语义直接承载) | Workflow § 1 Load | equal |
| P-2 | Target 解析 + 五查预检:`goal-utils.py run-checks <slug> [--target] --json` 为唯一判定点;`not-evaluated` 永非 `ok`;`blocked` 即停;退出码 0/2/3/4/5;非法 focus_target → `source=input-error` 停(修经 improve-team),不静默忽略;解析顺序 显式 `--target` > `focus_target` > 无 | Workflow § 2 Preview(engine 调用形态逐字保留) | equal |
| P-3 | 目标重述在前:先 goal,后结构 | Workflow § 3 Restate | equal |
| P-4 | 渲染静态结构(Role × Stage × Type 矩阵)与动态结构(pattern、并行度/DAG/阈值/运行设置、执行流图) | Workflow § 4 Render | equal |
| P-5 | Present & execute:披露非门禁,呈现后直接执行;披露 summary 判定(refresh/suppressed;落 `.specify/goal/<goal-slug>/summary/`,非团队目录);Target 指派行逐字形态(`本次 Target: T-<nnn> — <statement>(open)` / `本次 Target: 无(对 goal 整体运行)` / `…(团队默认)`) | Workflow § 5 Present & Execute | equal |
| P-6 | 按 pattern 编排:并行前 territory 校验;serial 链 DAG 无环 + 逐交接验证;iteration 强制上限;continuous 单轮 + L2+ 独立校验者;成员派发模态与外部 CLI Visibility Contract 按 subagent-definitions;用户可随时中止 | Workflow § 6 Orchestrate + Boundaries | equal |
| P-7 | 报告契约:每次运行强制写 `.specify/teams/<slug>/runs/<UTC-timestamp>-report.md`(含 `## Verification`);Target 指派字段逐字(`**Target 指派**: T-<nnn>(<statement>)` / `无(goal 整体)`,团队默认路径追加 `(团队默认)`);台账新条目带 `"target_ref": "T-<nnn>"` | Workflow § 7 Report | equal |
| P-8 | `--target` 不变量:不改 Goal–Team 绑定、不改身份解析、不改 summary 送达目录——仅本次聚焦切片 | Constraints 节(逐字承接) | equal |
| P-9 | 输出纪律:中间产物居 git-ignored `.specify/teams/.work/<slug>/`;交付物只到声明的目标路径(真源 create-team SKILL.md → Run Workspace, Reports & Output Discipline) | Constraints 节(引用不复制) | equal |
| P-10 | continuous 循环例外门控:`skills/internal/create-team/references/operating-loops.md` + `templates/teams/project-cluster.md` 的分级门保持 | Constraints 节(引用) | equal |

**提取边界**:create/modify 语义不进 run-team(FR-012);create-team 的执行引擎引用关系不变(run-team 调用同一引擎与 references,不复制其内容)。
