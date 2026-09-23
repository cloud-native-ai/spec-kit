---
id: "20260914T180702Z-skill-draw-echarts"
unit_id: "skill:draw-echarts"
unit_type: "skill"
run_id: "viz-skill-arena-cycle3-drawer-echarts"
scope: "local"
probe: "skill-draw-echarts-wrapup"
kind: "internal"
slice: "skills"
feature: "viz-skill-arena"
disposition: "processed"
partial: false
created: "2026-09-14T18:07:02Z"
summary: "Cycle-3 arena draw: recreated target.png (three dashed zones 用户网络/Aone/ASO/阿里云, 21 rounded-rect nodes, 5 solid arrows) as a fixed-layout ECharts graph plus graphic zone layer, config-driven (config.js"
introspection_ref: "introspection-20260923T120035Z#F-18"
disposition_reason: "introspection:introspection-20260923T120035Z#F-18"
---

## Review
Cycle-3 arena draw: recreated target.png (three dashed zones 用户网络/Aone/ASO/阿里云, 21 rounded-rect nodes, 5 solid arrows) as a fixed-layout ECharts graph plus graphic zone layer, config-driven (config.json canonical + generated config.js), vendored echarts@5.6.0, verify-deliverable and check-layout clean, headless screenshot evidence incl. network-blocked identical offline render. Three non-obvious ECharts behaviors required pixel-level forensics: layout:'none' bounds-fits node coords to the series rect (misaligning graphic zones until corner anchors were added), link lineStyle rendered at 50% opacity, and roundRect symbol radius too pill-like for architecture boxes.

## Optimization Points
- ECharts graph `layout:'none'` does NOT treat node x/y as raw canvas pixels: it linearly fits the node-coordinate bounding box into the series rect (per axis). Fixed-layout architecture configs that must pixel-align graph nodes with a `graphic` zone layer therefore need four invisible 1x1 corner anchor nodes (canvas corners) so the bounds-fit becomes the identity map; without them nodes stretch/shift away from the zones. Add this to the graph/component-view recipe in references/echarts-guide.md and to pitfalls.md.
- Graph link `lineStyle` rendered at ~50% opacity despite an explicit near-black color (pixel forensics: stroke value 132 over #f7f9fa background = 50% of #111). Pin `opacity: 1` on link lineStyle when faithful solid strokes are required; document in the guide's graph recipe.
- The built-in `roundRect` symbol rounds far more than typical architecture-diagram boxes (pill-like); for faithful corner radius use a per-node generated `path://` rounded-rect symbol authored at exact pixel size (symbolSize equals path bbox so scale is 1).
- Render-evidence gotcha: macOS headless Chrome inner viewport height is ~88px less than `--window-size` height; a chart taller than that gets its bottom clipped in the screenshot PNG and can be misdiagnosed as a page/layout bug. Size evidence windows with ~100px headroom (or measure painted bbox before trusting a clip).
