---
id: "20260805T171328Z-skill-improve-skills"
unit_id: "skill:improve-skills"
unit_type: "skill"
run_id: "improve-skills-fb-batch-12-apply-20260806"
scope: "local"
partial: false
created: "2026-08-05T17:13:28Z"
summary: "处理 draft/2026-08-05-profiles-feedback-batch-12(12 条)批量反馈:分拣出本仓库可落地 10 条,落地 3 个技能共 10 项改进——draw-plantuml(render-plantuml.sh 彩色标记循环陷阱修复并实测双轮渲染验证、PLANTUML_SERVER_FALLBACKS 公网回退+显式 UA 并实测 plantuml.com 回退、"
---

## Review
处理 draft/2026-08-05-profiles-feedback-batch-12(12 条)批量反馈:分拣出本仓库可落地 10 条,落地 3 个技能共 10 项改进——draw-plantuml(render-plantuml.sh 彩色标记循环陷阱修复并实测双轮渲染验证、PLANTUML_SERVER_FALLBACKS 公网回退+显式 UA 并实测 plantuml.com 回退、stereotype/颜色顺序与 ~ 转义与 frame 嵌套三条实测语法规则落 syntax-reference/04-deployment/12-rendering 文档);create-skills(Step 6 无契约套件项目的回退路径、Step 5 注册表插入锚点规则);improve-skills(Step 3 新增委托能力面/数据表/覆盖分级三条事实核查门,subagent GREEN 验证通过)。全量测试失败集与基线 diff 完全一致(零回归),sync-mirrors 镜像字节一致。

## Optimization Points
- findings.json 的证据结构(evidence[].{id,lane,evidenceState,summary,signals,evidenceRefs} + lanes 计数)未在 evidence-step.md 或 evidence-utils.py --help 中给出速查说明,消费者每次都要用 jq 试探键名(本次先猜 .findings 落空)。建议在 evidence-step.md 增加一段 findings.json shape 速查或让 --action latest 附 digest 摘要字段。
- 处理跨项目 feedback 打包(12 条、6 单元、含本仓库不存在的单元)时,先按"本仓库可落地 / 外仓 / 无优化点"三分法分拣再进入逐技能流程,避免了对外仓单元(dingtalk-follow-up、aliyun-workspace)做无效解析;该分拣步骤可作为 improve-skills 批量模式的第 0 步写入。
- 文档化语法断言前先实测(render-plantuml.sh 修复同法):本次实测证实 ~ 转义规则,但 frame-in-node 在当前服务器实际可渲染,与反馈的"语法错误"不一致,最终按版本敏感措辞落文档,避免了以偏概全。
