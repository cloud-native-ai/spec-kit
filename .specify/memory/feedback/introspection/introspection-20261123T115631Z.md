---
id: "introspection-20261123T115631Z"
created: "2026-11-23T11:56:31Z"
status: "confirmed"
scope_filter: "disposition=open --limit 0 --format json (3 entries; framework hat; 30 inbound bundles digested separately as bundle material)"
scope_entries: ["20261116T163101Z-skill-manage-feedback", "20261116T163102Z-speckit-feedback", "20261122T050152Z-skill-manage-features"]
supersedes: ""
confirmed_at: "2026-11-23T12:27:54Z"
---

# Introspection Report: introspection-20261123T115631Z

范围:本地库 **3** 条 open 条目(全部 `kind: internal`,`external_count: 0`)。本仓戴**框架帽子**(root 实测 `templates`、`skills`、`shared`、`scripts`、`src/specify_cli` 五个源目录俱在),故不存在上行侧,分流恒为 `local-sink(...)`;Path B 未被选中,也未被显式请求。

**Bundle 物料不进入本报告成员**:本轮另有 30 个入站包(1 184 条 / 2 228 优化点),按 A2 大批量读纪律由 22 个并行只读核验组处理,结论经 A4 对账后写入 backlog;包内条目不属于本库索引(引擎 V-3),故 `scope_entries` 只含本库 3 条。

## Findings

### F-01: manage-features 全量注册表消费缺确定性投影,且证据车道未分 baseline / feature-specific

- **根因**: `skills/internal/manage-features/SKILL.md` 的 Actions 4–9 只规定「diff every registry row / 逐行对照」,没有要求按列投影消费(首列表格单元拆分、状态列投影),也没有确定性提取器;读取形态全靠代理自行决定,宽口径 ID 提取一次可产出 30 KB 结果,且同一审计工人可能重复同一宽匹配。同一技能的 Action 9 残留报告亦未区分「既有基线失败」与「特性自身失败」两条证据车道。
- **证据锚点**: `skills/internal/manage-features/SKILL.md:104-125`(Actions 4–9,无投影/extractor/证据车道条款);`:80-102`(Action 0–3,亦无读取形态约定)。
- **成员条目**: 20261122T050152Z-skill-manage-features(成立)
- **分流决定**: local-sink(improve-skills)
- **优化方案**: ① Action 1/4 增「注册表消费投影」条:全量 reconcile MUST 先以确定性提取器(或引擎动作)产出 ID/Name/Status 字段投影,禁止把表格整行/整格宽匹配注入;首列 markdown 链接按 `[ID](features/ID.md)` 拆分消费。② Action 9 的残留报告增两条证据车道:pre-existing baseline failures(须引 canonical runner 原始记录)与 feature-specific failures(须引特性审计原始记录),两者 MUST 分列,不得合并叙述。
- **建议处置**: 20261122T050152Z-skill-manage-features:processed

## Excluded

- 20261116T163101Z-skill-manage-feedback — clean-run 自记录(上一轮 171 条消化运行的渠道统计摘要),无优化点
- 20261116T163102Z-speckit-feedback — clean-run 自记录(框架帽子路由摘要),无优化点
