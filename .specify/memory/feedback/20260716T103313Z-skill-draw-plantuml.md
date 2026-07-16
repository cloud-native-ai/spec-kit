---
id: "20260716T103313Z-skill-draw-plantuml"
unit_id: "skill:draw-plantuml"
unit_type: "skill"
run_id: "arc7-stability-verify-r3"
scope: "local"
feature: "draw-plantuml-optimizer"
partial: false
created: "2026-07-16T10:33:13Z"
summary: "从零生成「部署与治理拓扑」部署图，稳定性验证第3轮。严格套用两条确定性规则：保色配方(monochrome false + legend 内 <color:#..>)一次命中，渲染日志确认「Color markup detected — skipping monochrome」，SVG 含 6 组语义填充色 + 蓝/红着色边，稳定彩色不抖动；输入输出同 basename 触发脚本的碰撞保护(tem"
---

## Review
从零生成「部署与治理拓扑」部署图，稳定性验证第3轮。严格套用两条确定性规则：保色配方(monochrome false + legend 内 <color:#..>)一次命中，渲染日志确认「Color markup detected — skipping monochrome」，SVG 含 6 组语义填充色 + 蓝/红着色边，稳定彩色不抖动；输入输出同 basename 触发脚本的碰撞保护(temp copy)正常。band-by-plane 分带(声明式顶/运行+命令式底)正确成形，每带折 2×2 网格保证每行≤5、nodesep(42)≥ranksep(38)。3 轮迭代把宽高比从 2.0:1→(误)2.27:1→1.24:1(≈4:3 横向)。

## Optimization Points
- title: band-by-plane 折 2×N 后需左列锚定防对角漂移
- detail: >
- §4d/§4e 指导「每带折 2×N 网格 + nodesep≥ranksep」压 4:3，但实测：把两条带内子框各折成 2×2 后，
- 仅靠跨带真实边(op→cp) + 右侧隐藏边(etcd→agent 右对右) 会让下带整体漂到右下角、两带排成对角线，
- 宽高比反而从 2.0:1 恶化到 2.27:1。根因是无约束把下带左缘对齐到上带左缘。
- 修复：删右侧 right-to-right 隐藏边，改用「上带左列元素 -[hidden]down-> 下带左列元素」左对左锚定，
- 立即回落到竖直堆叠、1.24:1。建议 playbook §4d 补一句：band 竖直堆叠的隐藏主轴必须走左列对左列(或统一同侧)，
- 切勿右列对右列，否则折网格后易成对角。
- scope: local
