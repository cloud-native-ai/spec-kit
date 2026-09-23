---
id: "20260914T180923Z-skill-draw-plantuml"
unit_id: "skill:draw-plantuml"
unit_type: "skill"
run_id: "viz-skill-arena-cycle-3-drawer-plantuml"
scope: "local"
probe: "skill-draw-plantuml-wrapup"
kind: "internal"
slice: "skills"
disposition: "processed"
partial: false
created: "2026-09-14T18:09:23Z"
summary: "Cycle-3 复刻任务（三域部署拓扑 target.png）完成交付：puml/SVG/PNG/HTML 齐备，远端渲染一次通过校验（viewBox 11012、PNG 2750x1884、附录与磁盘 puml 逐字节一致）。主要成本花在渲染后端差异试错：服务器忽略 <style> 块、packageStyle rectangle 抑制 dashed、hidden 边 rank 语义与 2-环反"
introspection_ref: "introspection-20260923T120035Z#F-20"
disposition_reason: "introspection:introspection-20260923T120035Z#F-20"
---

## Review
Cycle-3 复刻任务（三域部署拓扑 target.png）完成交付：puml/SVG/PNG/HTML 齐备，远端渲染一次通过校验（viewBox 11012、PNG 2750x1884、附录与磁盘 puml 逐字节一致）。主要成本花在渲染后端差异试错：服务器忽略 <style> 块、packageStyle rectangle 抑制 dashed、hidden 边 rank 语义与 2-环反转，共 6 轮渲染才收敛到与源图匹配的布局。

## Optimization Points
- 复刻类任务先做「渲染后端能力探针」：本 cycle 实测远端 PlantUML 服务器完全忽略 <style> 块（LineStyle/RoundCorner 均无效），且 `skinparam packageStyle rectangle` 会使 `packageBorderStyle dashed` 失效；可行配方是「stereotype 矩形容器（rectangle <<zone>> + hide stereotypes）+  stereotype 级 skinparam（BorderStyle dashed / RoundCorner 0 / FontStyle plain）」。建议把该探针与配方写入 style.md / pitfalls，避免每轮重绘重复试错 4-5 次渲染。
- 隐藏边语义实测：`-[hidden]down-` 约束 rank（+1），`-[hidden]right-` 不约束 rank 仅定左右序；因此「撑满全高分区」需用无入边的不可见占位节点 + 中间占位链（phTop→phMid→sls）把占位钉在 rank 0，仅靠 right 锚点会被 dot 的边长最小化拉到 rank 1。建议纳入 large-diagram-playbook 的隐藏脚手架小节。
- 同节点对「可见边 + 反向 hidden 边」构成 2-环，dot 会随机反转导致扇形方向错乱；复刻扇形分发时应以「不可见左列锚点节点 + hidden down 链 + hidden right 列锚点」表达 rank 差，而非在可见边对上叠加反向 hidden 边。
