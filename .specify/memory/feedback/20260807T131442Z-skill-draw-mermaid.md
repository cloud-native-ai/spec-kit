---
id: "20260807T131442Z-skill-draw-mermaid"
unit_id: "skill:draw-mermaid"
unit_type: "skill"
run_id: "sandbox-20260807-draw-mermaid"
scope: "local"
feature: "viz-skill-arena-sandbox"
partial: false
created: "2026-08-07T13:14:42Z"
summary: "绘制 sandbox (wasm-e2b-k8s) 三张架构图：组件（五大子系统 hub-and-spoke + legend）、部署（C4Deployment：ate-api-server Deployment / atelet DaemonSet / valkey StatefulSet / ateom-wasmd worker Pod / atunnel / ateom-gvisor 伴生 "
---

## Review
绘制 sandbox (wasm-e2b-k8s) 三张架构图：组件（五大子系统 hub-and-spoke + legend）、部署（C4Deployment：ate-api-server Deployment / atelet DaemonSet / valkey StatefulSet / ateom-wasmd worker Pod / atunnel / ateom-gvisor 伴生 Pod）、Actor 序列（DNS→router→API→atelet→ateom-wasmd ColdBoot 恢复→atunnel 隧道，四阶段 + CAS critical + RunWorkload/CheckpointWorkload 两个 opt 分支）。复用 substrate 轮次的子系统词汇与 classDef 配色，远端 server 后端渲染成功，PNG+SVG+.mmd+HTML 四件套齐全，HTML 内嵌可复现信息，有效字号 ≥12px。语义完整覆盖架构描述全部要点（控制面卸载、快照模型 tar+ColdBoot、帧协议、epoch 超时、WASM_BOOTSTRAP_DIR）。

## Optimization Points
- ## 优化点
- 序列图的 sequence 子配置（actorFontSize/messageFontSize/noteFontSize）被 mermaid.ink 服务器忽略，统一渲染为 16px（与 substrate 轮次实测一致）；建议在 12-rendering-and-output.md 或 render-mermaid.sh 中固化「服务器忽略 sequence 子配置」这一认知，避免后续轮次重复调试。
- C4Deployment 在 3×N 网格下 15 条 Rel 边标签易与邻近容器混淆；可评估把 podcert-controller 的三条签发边收敛为一条「SPIFFE 全链路」边（详情外置 HTML），或改用 flowchart subgraph 部署近似以完全控制连线走向。
