---
id: "20261008T135121Z-speckit-review"
unit_id: "/speckit.review"
unit_type: "command"
run_id: "review:20261008-spec054-roadmap"
scope: "local"
probe: "speckit-review-wrapup"
kind: "internal"
slice: "commands"
partial: false
created: "2026-10-08T13:51:21Z"
summary: "roadmap Now-tier 三项全部闭环:F1 选「补演示」路径——dogfood-executor 席位按新流程真实走完建队实例化→渲染触发(实跑 rendered 3)+ 按注册类型语义派发(run report §3 派发记录 + 席位任务 success),SC-002 以 Source 点名的证据形态(宿主目录清单+派发记录)重立 pass;F2 quickstart 全部命令逐字"
---

## Review
roadmap Now-tier 三项全部闭环:F1 选「补演示」路径——dogfood-executor 席位按新流程真实走完建队实例化→渲染触发(实跑 rendered 3)+ 按注册类型语义派发(run report §3 派发记录 + 席位任务 success),SC-002 以 Source 点名的证据形态(宿主目录清单+派发记录)重立 pass;F2 quickstart 全部命令逐字重跑零占位符;F4 从句引用纠正;同批 F6/F7/F8/F9/F10 补丁落地;F12 由用户本人的 7267c46a 提交顺带关闭。一条机制面发现如下(补记——run report §2 声称已入 feedback 而当时未记录,该不实声明随 b4f2b8cb 落盘,本条使其为真)。

## Optimization Points
- 1. [deploy-timeliness] 新 CLI 子命令从合入到宿主 PATH 生效之间存在发布窗口:本特性的 `specify render-agents --ai qoder` 已在本仓 src/ 落地并通过契约测试,但宿主 PATH 上的 `specify` 是安装态 0.0.22——SC-002 dogfood 演示实跑时命令报「No such command 'render-agents'」,只能以 in-tree 模块执行同一 typer 入口等价完成(两顶帽子:本仓的 .specify/ 是客户端运行时,装的是已发布的 CLI)。这不是缺陷而是发布时序事实,但**教给用户的触发命令在发布前对安装态 CLI 不可用**——templates/commands/agents.md 与 SKILL.md 教的 `specify render-agents` 要等下一版 specify-cli 发布 + 用户升级后才真正可达。机制侧建议:(a) create-team/improve-team 流程文的渲染触发步可补一句「若宿主 specify 版本低于该子命令引入版本,退回 `specify init --here --ai <tool>`(等价渲染,副作用面大)或先升级」;(b) 长期看 `_AGENT_METADATA_MAPPING`/子命令集的版本敏感教学面值得一个「capability floor」注记模式,避免下一次新子命令重蹈同一窗口。
