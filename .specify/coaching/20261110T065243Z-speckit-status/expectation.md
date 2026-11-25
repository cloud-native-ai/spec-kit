## Run header

- run-id: 20261110T065243Z-speckit-status
- chain: /coaching-skills → /speckit.status（direct run；`<work>` 为空 = 无参执行）
- trainee: /speckit.status — command；canonical template `templates/commands/status.md`（运行期副本 `.qoder/commands/speckit.status.md`）
- subject: 无（Trainee 即对象；无 meta-skill 链）
- started-at: 2026-11-10T06:52:43Z

## Trainee

- identifier (verbatim): `/speckit.status`
- resolved-path: `templates/commands/status.md`（command 模板；生成副本为 alias）
- executor-kind: command（技能集中无同名 skill，双表扫描唯一命中）
- layer: n/a（command）
- subject-resolution: self
- failure-semantics: 输入错误 → exit 2；无活动线 → exit 3 显式 `nothing-running`（是正确答案而非失败）；输出必须逐字呈现脚本结果

## Outcome Correctness

| id | object | acceptance | allowed-deviation | derivation |
|---|---|---|---|---|
| OC-1 | stdout 上的当前态摘要渲染 + 报告的退出码 | stdout 非空且为脚本网格渲染（或显式 nothing-running 渲染）；exit ∈ {0,3} | tolerance=0 severity=high | status.md § Delegation（默认动作 digest）与 § Exit statuses |
| OC-2 | 摘要反映真实注册表（活动线可见） | 若注册表存在 `095-superagent-role`（state=active），摘要中出现该线 | tolerance=0 severity=medium | status.md § three actions（digest 回答「什么在运行」） |
| OC-3 | 输出逐字、未重渲染/改写 | 无自撰表格、无改写脚本行 | tolerance=0 severity=high | status.md § Delegation 末段（print verbatim；不得 paraphrase） |

## Process Efficiency

| id | steps | tool-calls | retries | critical-path | derivation |
|---|---|---|---|---|---|
| PE-1 | ~3-5 | Bash 1-2 轮（脚本调用）+ Wrap-up 引擎 3 轮 | 0 | 解析参数（空=digest）→ 调脚本 → 逐字打印 | status.md § Delegation + § Wrap-up |
| PE-2 | validation-gap | validation-gap | validation-gap | validation-gap | validation-gap |

## Assumptions

- 注册表解析到 `~/.local/state/spec-kit/lines`（无 `SPECIFY_LINE_REGISTRY_DIR` 覆盖）
- 仓库中存在至少一条活动线（095 运行中），因此预期 exit 0
- 执行者以项目根为 cwd

## Unknowns

- digest 的声明上限是否会把 095 线截断（`--cap` 缺省值）
- 实际退出码（0 vs 3）

## Forbidden Side Effects

- 本阶段不执行任何 Trainee 工具、脚本或命令
- 不写 Trainee 目录
- 无网络或外部调用
- 不创建 claim 标记（归 ../data-model.md § Optimization claim 与优化步）

## Trainee Failure Semantics

- 退出码 2（输入错误）即失败并上抛
- 退出码 3 = 显式 nothing-running，不是失败
- Wrap-up 记账（session/feedback/exec-quant 记录）是允许的写面；不得改写摘要输出
