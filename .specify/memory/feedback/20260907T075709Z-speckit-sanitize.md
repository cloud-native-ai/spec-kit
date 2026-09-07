---
id: "20260907T075709Z-speckit-sanitize"
unit_id: "/speckit.sanitize"
unit_type: "command"
run_id: "sanitize-2026-09-07"
scope: "local"
probe: "speckit-sanitize-wrapup"
kind: "internal"
slice: "commands"
partial: false
created: "2026-09-07T07:57:09Z"
summary: "运行达成命令目的:七阶段完整执行。Preflight 通过;Collect 零新增、刷新 757、语义候选 0(判定依据材料齐备,无待裁决);Judge 对 756 项 dead-reference 逐区裁决为不可行动——727 项在已完成特性的历史 spec 工件、20 项在 features.md 历史列/NNN 占位行(项目纪律禁止改写历史记录)、9 项在活文档但全部核实为提取器误报(枚举拼"
---

## Review
运行达成命令目的:七阶段完整执行。Preflight 通过;Collect 零新增、刷新 757、语义候选 0(判定依据材料齐备,无待裁决);Judge 对 756 项 dead-reference 逐区裁决为不可行动——727 项在已完成特性的历史 spec 工件、20 项在 features.md 历史列/NNN 占位行(项目纪律禁止改写历史记录)、9 项在活文档但全部核实为提取器误报(枚举拼接/子串/假想例/owner 一致的按需模式路径);Present 呈现台账摘要与分诊(无 docs/instructions/sync-mirrors 移交项);Confirm 单次批量呈现唯一 destructive 项,用户批准;Apply 中引擎拒绝删除非空目录(exit 2 零部分执行,防线正确),agent 依同一批准 rm -rf 精确目标并验证,会话技能列表 24 个 layout-int-* 垃圾条目即时消失;Wrap-up 记录门控证据与本条。台账状态:9ded7d0e4022 待下次 collect 自动收敛;756 项 repair 处置经本轮裁决语义不成立,建议引擎引入 dated-record 区排除或 waived 状态。

## Optimization Points
- **dead-reference 提取器五类误报无豁免机制,756 项每轮全量重标(台账噪音)。** 本轮实测误报类:①斜杠连接枚举被拼成路径(`instructions.md/memory/skills/agents/scripts/templates`、`create-docs/improve-docs`);②有效长路径的子串(`docs/reference/skills/feedback.md` 被抽出 `skills/feedback`);③散文示例路径(constitution `docs/team/overview.md` 是 path-is-semantic 原则的假想例);④owner 一致的按需模式路径(`.specify/goal/<slug>/`、`.specify/agents/instances/`、`.specify/memory/todo/`、`NNN` 占位行);⑤带尾标点的散文引用(`skills/tools.`)。加上 727 项落在已完成特性的历史 spec 工件(项目纪律:历史文件 MUST NOT be rewritten)与 features.md 历史列( dated record),引擎 disposition=repair 全部语义不成立。建议:扫描器排除 dated-record 区(specs/archive/history 历史工件、features.md 状态列),或引入 waived/acknowledged 状态供人工裁决后静默,否则台账永久携带 700+ 不可行动项、每次 collect 全量刷新。
- **引擎 apply 拒绝删除非空目录,confirmed destructive 目录项无法由引擎完成。** 本轮唯一 destructive 项(`.specify/skills/.migration-backups/`,24 个子目录)用户批准后 apply 返回 `refusing to delete non-empty directory` exit 2(零部分执行,防线正确);最终由 agent 以同一批准执行 rm -rf 完成。建议:对已确认计划中的目录目标支持递归删除,或在命令模板 Stage 6 明示 agent 兜底路径,避免每次非空目录项都走失败-兜底两跳。
- **`.migration-backups` 复发的根因在 sanitize 范围外,登记为观察。** 该目录 2026-08-20 经用户批准删除后,8/24–9/6 由外部迁移工具将测试生成的 layout-int-* 集成场景技能备份重新生成(仓内脚本零引用该目录;live layout-int-* 在全盘不存在,会话技能列表的 24 个垃圾条目实际加载自备份目录,删除后即时消失)。引擎 summary 建议登记 `_OBSOLETE_SKILLS`——语义不符:该 registry 收录"曾随包发布后退役的技能",`.migration-backups` 是外部工具的运行时残留且已 gitignore。复发源头(测试场景把技能写入真实工作区 + 外部迁移工具)属产品脚本/测试用例,按范围红线不评估不修改,仅在此登记。
- token-efficiency:首轮 collect 将原始 JSON(含 757 项 pendingTargets 全量列表)直接管道 head -200 输出,约 200 行台账原文进入上下文后才改为「重定向到文件 + python 摘要」的正确姿势;命令模板 Stage 2 可加一句提示(collect 输出 MUST 先落文件再取摘要),避免每次运行重复这笔可避免开销。
