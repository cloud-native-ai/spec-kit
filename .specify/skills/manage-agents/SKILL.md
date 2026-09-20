---
name: manage-agents
description: 通用多 Agent 配置管理技能（跨平台）。分层信息披露：先判定平台（macOS/Linux），再判定意图（组件运维 / 异常诊断 / 装配配置），再装载部署方提供的 Agent 知识页。本技能是通用下层——不含任何机器特定路径；本机专用内容（接线拓扑、技能库归档、备份恢复、具体 Agent 知识页）由部署环境的配套前门技能承载。当用户提到 "agent 配置管理", "配置 agent", "配置AI工具", "切换模型", "切换provider", "统一环境变量", "AGENT_API_KEY", "agent 运维", "诊断 agent", "manage-agents", "config agent", "agent setup", "configure agent", "switch model", "install codex", "install claude", "四元组配置", "互斥配置", "unified env" 时使用。
skill_id: "<SKILL:./SKILL.md>"
---

# manage-agents — 通用多 Agent 配置管理

跨平台、跨 Agent 的通用配置管理下层技能：组件运维协议、异常诊断循环、
统一环境变量装配。**本技能不含任何机器特定内容**——具体 Agent 的知识页
（组件地图/配置地图/禁区/判读决策表）由部署环境的配套前门技能按
[references/agent-page-contract.md](references/agent-page-contract.md) 提供。

## 分层信息披露（严格按序，禁止跳层/全量装载）

**L0 — 平台判定**：

```bash
uname -s   # Darwin → macOS；Linux → linux
```

平台差异只影响「哪些 Agent 在场、有无注册表/db 动作」——由配套前门技能的
平台矩阵给出。

**L1 — 意图判定**（进入恰好一个意图页）：

| 意图 | 关键词特征 | 意图页 |
|------|-----------|--------|
| 组件运维（单 Agent） | 某 agent 的配置/进程/插件/重启 | [references/intents/agent-ops.md](references/intents/agent-ops.md) |
| 异常诊断（单 Agent） | 没反应、卡住、报错、排查、诊断 | [references/intents/agent-diagnose.md](references/intents/agent-diagnose.md) |
| 装配配置（单/多 CLI） | 配置 agent、切换模型/provider、统一环境变量、安装 CLI | [references/intents/agent-setup.md](references/intents/agent-setup.md) |

**L2 — Agent 知识页装载**：意图页要求时，从配套前门技能装载
`agents/<agent>.md`（一页一次；全量遍历是反模式）。找不到对应知识页时
先只读探测，沉淀后建页。

## 硬约束

1. **凭据值禁区**：任何 Agent 的凭据值一律不改、不打印、不入文档。
2. **诊断默认只读**：不重启、不删会话、不改配置；修复动作先说明再执行。
3. **变更先备份**：任何配置修改先 `cp <file> <file>.bak-<ts>`。
4. **机器特定内容不进本技能**：路径、拓扑、注册表接线属于配套前门技能；
   发现本技能里出现机器特定内容时，移回前门技能。

## Resources

| 目录 | 内容 |
|------|------|
| `references/intents/` | agent-ops / agent-diagnose / agent-setup |
| `references/setup/` | unified-variables / supported-tuples / available-tuples / permission-modes / usage-examples |
| `references/agent-page-contract.md` | Agent 知识页结构契约 |
| `scripts/` | config-agent.sh（统一环境变量装配） |

## Feedback

**Runtime-mode gate.** If `${SKILL_WORKDIR}/.specify/` does not exist, this skill is
running in standalone mode (a non–Spec Kit deployment, e.g. a global agent skills
directory) — skip this entire Feedback step: no engine call, no feedback entry.

At the end of a substantial run of this skill, perform an agent self-reflection step (never solicit feedback content from the user), following the canonical convention in `.specify/shared/workflow/feedback-step.md`:

1. **Gate on qualification & completion.** Only proceed if this run reached a meaningful wrap-up. Skip trivial/no-op runs; for an aborted run use the abort/partial rule below.
2. **Reflect (no user input).** Review this run against this skill's declared purpose and produce a short review plus ≥1 concrete, skill-specific optimization point. If the run was clean, use exactly: `No significant optimization points identified this run.`
3. **Scope guard.** Keep strictly to this skill's operation; do NOT produce a global/whole-project assessment (that is `/speckit.review`'s job). Entries are `scope: local`.
4. **Dedup guard.** Use a stable `run_id`; if a parent flow already recorded feedback for this same `(unit_id, run_id)`, the engine no-ops.
5. **Persist** via the engine:
   ```bash
   python3 "${SKILL_WORKDIR:-.}/.specify/scripts/python/feedback-utils.py" --action record \
     --unit-id "skill:manage-agents" --unit-type skill \
     --run-id "<stable-run-id>" --feature "<feature-key-if-any>" \
     --review "<review prose>" --points-file "<points file>"
   ```
   Probe attribution: the engine resolves the unit to its probe object automatically — the entry inherits kind/slice from the probe registry. External custom units record via `--unit-id custom:<owner>/<name> --unit-type custom-unit`; their entries stay host-project-local and never enter upstream packages.
6. **Consolidated submission prompt(非阻塞).** If the returned `should_prompt` is `true`, append ONE non-blocking line to the wrap-up report inviting submission (point the user to the `/speckit.feedback package` command — the user-facing path; never paste the raw `feedback-utils.py` engine call into the user-facing line); it MUST NOT block the wrap-up flow and MUST NOT trigger any 自动传输 (manual delivery only; `--action mark-submitted` runs only if the user initiates submission). Below threshold, do not prompt.

**Abort / partial-run rule.** If the run failed before wrap-up, either skip recording or record with `--partial` and a `## Review` beginning `**Partial run** — `.
