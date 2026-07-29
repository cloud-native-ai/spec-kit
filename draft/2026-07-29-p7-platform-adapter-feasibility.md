# P7 平台适配器迭代：复杂度与可行性调研

> 状态：**待审查（调研文档）**
> 日期：2026-07-29
> 承接：spec `034-evidence-infra` US7 交付物 `platform-adapter-survey.md`（T038，clarify Q3 定界：新适配器属后续独立迭代）
> 上游基线：`scripts/js/better-harness/` @ `b2e621d`（源码复制托管，D1）
> 调研方法：**源码探测**（引擎子集实际代码 + 行数实证）+ **本机 doctor/文件系统实测**，不依赖上游 roadmap 文档（FR-012 口径）。未观察项显式标注 Unobserved，不推断。

---

## 1. 结论速览

- 剩余 5 个自研平台（copilot / opencode / qwen / hermes / iflow）全部点亮约需 **2,000–3,500 行新代码 + 5 组 fixture 测试**；
- 按价值/成本排序，**前三步（claude 核实补齐 → opencode → qwen+iflow 合并迭代）以约 40% 成本覆盖最可能有真实落盘的平台**；
- 调研发现一个**先决缺陷**：doctor 的会话存储探测仅做目录存在性判定，会产生 `detected` 误报（本机 opencode 实例证实）——**建议 P7 第一个任务先修 doctor 三态探测**，否则后续定序建立在误报上；
- hermes / copilot 可行性未观察（无落盘、无格式资料），维持"探测到真实落盘前不投入"。

## 2. 成本基准（源码实证）

一个"平台点亮" = 会话适配器 + 资产 provider + 固定横切开销：

| 构件 | 实证基准（行数为在库实测） | 说明 |
| --- | --- | --- |
| 会话适配器 | **provider-runner 新模式 ≈ 469 行**（`platforms/claude.mjs`）；内联旧模式 1,997 行（qoder）/ 1,239 行（codex）/ 664 行（cursor） | 继承 `session-analysis/analyzer.mjs` 的 `SessionAnalyzer` 五虚方法（resolveScope / discoverSourceRoots / discoverSessions / readSession / normalizeEvent）；`provider-runner.mjs` 已托管 scope/source/warning 公共逻辑——**新适配器成本已被上游模式演进压缩至旧模式的约 1/4** |
| 资产 provider | 339–585 行（codex 339 / cursor 391 / claude 531 / qoder 585） | 注册进 `agent-customize/providers/index.mjs` 的 `PROVIDER_COLLECTORS` 分发表（全文件仅 19 行，扩展点干净） |
| 固定横切开销（每平台，不可省略） | — | ① 脱敏漏斗接入（不得绕过 privacy-safe-text / semantic-facets）② 能力缺口显式标注（仿 cursor `eventTimestampCoverage: "partial"`）③ 最小 fixture 测试 ④ **三处登记**：`analyzer.mjs loadPlatform` 显式分支（勘察确认非自动发现）+ `PROVIDER_COLLECTORS` + `evidence-utils.py PLATFORM_SESSION_STORES` ⑤ `UPSTREAM.md` 修改台账 ⑥ 双镜像同步（`diff -rq`） |

## 3. 逐平台评估（8 工具支持矩阵）

| 序 | 平台 | 会话存储实况（本机实测 2026-07-29，root 账号） | 复杂度 | 可行性 | 关键依据 |
| --- | --- | --- | --- | --- | --- |
| — | qoder | ✅ detected，`~/.qoder/projects/<slug>/transcript/*.jsonl` 真实数据 | 零（已完整） | 已可用 | 1,997 行完整适配器 + 585 行 provider 在库 |
| — | codex | 本机未落盘（`~/.codex/` 仅 config/hooks/tmp） | 零（已可用） | 已可用 | 双侧在库；模型/Hook 证据缺口按纪律标 Unobserved |
| 1 | claude | ⚠️ 本机 `~/.claude/projects` 无落盘（survey 快照曾 detected——见 §4 风险②） | **小**：双侧代码已存在（469 + 531 行），仅差 fixture 验证 + 缺口标注 | **高** | 上游已按 provider-runner 模式写好，属"核实补齐"而非新写 |
| 2 | opencode | ⚠️ doctor 判 detected 但为**误报**：`~/.local/share/opencode/` 仅空 `repos/` + `log/`，零会话文件（§4 风险①） | **中**：新写 ~450–700 行适配器 + ~350–500 行 provider | **高**：会话存储为本地 JSON、格式公开 | 需真实 opencode 使用环境产出 fixture |
| 3 | qwen | 未落盘（`~/.qwen/tmp` 空） | **中**：Gemini-CLI 系，存储格式类 JSON 日志，可低成本仿写 | **高**，但时间戳/工具事件粒度可能不全 → 需 partial 标注 | survey 判断 + 存储路径已入 doctor 表 |
| 4 | iflow | 未落盘（`~/.iflow/tmp`） | **中偏小**：与 qwen 同为 Gemini-CLI 系——**建议与 qwen 合并为一个迭代**（共享基类），边际成本约减半 | 高（随 qwen） | 同系工具存储结构高度相似 |
| 5 | hermes | 未落盘（`~/.hermes/sessions` 不存在），格式**未核实** | **中~大（Unobserved）** | **未观察**——按纪律不推断 | 无源码 / 无落盘 / 无公开格式资料三缺；先探测到真实落盘再投入 |
| 6 | copilot | 未落盘（`~/.copilot/` 仅 hooks） | 待定 | **最低**：CLI 会话持久化能力最弱 | 维持 survey 结论"探测到落盘前不投入" |

## 4. 调研新发现（survey 之外的增量结论）

1. **doctor 存在性探测有误报（先决缺陷）**：`PLATFORM_SESSION_STORES` 探测仅做 `Path.exists()`——本机 opencode 目录存在但零会话文件仍判 `detected`。建议给 doctor 加二级校验（目录内实际含会话文件才 `detected`，或输出 `detected / detected-empty / not-detected` 三态）。改动很小（`evidence-utils.py` 约 20 行 + 镜像），但决定后续全部定序决策的可信度。
2. **探测结果随用户/HOME 漂移**：本机（root）与 survey 快照（claude detected）不一致——doctor 定序必须在**目标使用环境**（实际开发者账号）下执行；survey 第 19 行的告诫应升格为操作前置条件。
3. **qwen + iflow 应合并迭代**：同为 Gemini-CLI 系，五虚方法实现可共享基类；survey 定序第 3、4 两项合并后总成本低于两次独立开发。
4. **资产 provider 是独立决策**：会话适配器价值在"观察到的执行"；资产 provider 价值取决于各工具配置面丰富度——opencode/qwen/iflow 配置资产较薄，可先只做会话适配器、资产泳道标 `unavailable`，符合 findings 合同的显式降级语义。

## 5. 建议的迭代切分（供后续 /speckit.requirements 参考）

| 迭代 | 内容 | 规模 | 前置条件 |
| --- | --- | --- | --- |
| P7-a | doctor 三态探测修正 + claude fixture 核实补齐 | 小 | 有 Claude 会话落盘的环境 |
| P7-b | opencode 会话适配器（provider-runner 模式） | 中 | 真实 opencode 使用产出 fixture |
| P7-c | qwen + iflow 合并迭代（共享 Gemini-CLI 系基类） | 中 | 任一工具真实落盘 |
| P7-d | hermes / copilot | 挂起 | doctor（修正后）探测到真实落盘才立项 |

每个迭代按 FR-012 约束执行：脱敏漏斗 + 缺口显式标注 + fixture 测试 + 三处登记 + UPSTREAM.md 台账 + 双镜像同步。

## 6. 证据清单

| 证据 | 路径 |
| --- | --- |
| US7 交付的探测报告 | `.specify/specs/034-evidence-infra/platform-adapter-survey.md` |
| 适配器接口（五虚方法 + loadPlatform 显式分发） | `scripts/js/better-harness/session-analysis/analyzer.mjs` |
| provider-runner 公共逻辑 | `scripts/js/better-harness/session-analysis/provider-runner.mjs` |
| 在库适配器/provider（行数基准） | `scripts/js/better-harness/session-analysis/platforms/*.mjs`、`agent-customize/providers/*.mjs` |
| doctor 探测实现与存储路径表 | `.specify/scripts/python/evidence-utils.py`（`PLATFORM_SESSION_STORES`） |
| 本机存储实测 | `~/.qoder/projects`（JSONL 实据）、`~/.local/share/opencode`（空目录误报实据）等，2026-07-29 root 账号快照 |
