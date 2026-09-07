---
id: "20260907T043622Z-skill-improve-skills"
unit_id: "skill:improve-skills"
unit_type: "skill"
run_id: "improve-skills-merge-skills-2026-09-07"
scope: "local"
probe: "skill-improve-skills-wrapup"
kind: "internal"
slice: "skills"
partial: false
created: "2026-09-07T04:36:22Z"
summary: "改进了从未真实执行过的新技能 merge-skills（创建于 2 小时前）。findings 泳道退化（10 条全为项目级，无一条指向该技能），因此改以「实跑技能自带脚本 + 挖创建会话记录」为执行窗口：对 coverage_probe.py 构造正/负/反向样本，实测出 4 个高危缺陷——①SKILL.md 与 reference 均声称覆盖「枚举值/状态码（READ/WRITE、201、42"
---

## Review
改进了从未真实执行过的新技能 merge-skills（创建于 2 小时前）。findings 泳道退化（10 条全为项目级，无一条指向该技能），因此改以「实跑技能自带脚本 + 挖创建会话记录」为执行窗口：对 coverage_probe.py 构造正/负/反向样本，实测出 4 个高危缺陷——①SKILL.md 与 reference 均声称覆盖「枚举值/状态码（READ/WRITE、201、422）」，但无任何 pattern 抽取该类，纯枚举源材料对空目标竟报 extracted:0 + coverage clean + exit 0；②源路径不存在/为空时同样报 exit 0「coverage clean」，把强制无损失门禁变成静默空转并授权下线删除；③文档允许的终态「每个残差都是已核实的误报」在脚本里不可达（任何 miss 恒 exit 3，无处登记），逼着要么篡改目标文档要么无视门禁；④Phase 5 只证源→目标，未覆盖 Phase 3 改写既有目标文档时目标自身丢内容。另修 3 处文档/接线缺口：下线清单漏了两个本仓库有契约强制的接线面（agent skills: 前置声明需改指目标而非删除，否则 test_declared_skills_resolve_to_installed 红；退役名需登记 _OBSOLETE_SKILLS，否则下次 specify init 复活）；Phase 8 误指 create-skills §Report（真实标题为 8. Report completion 且内容是创建向）；缺 Resources 表。验证：4 类 exit code 全部实测、创建会话原冒烟用例回归一致、反向样本仍 exit 0、49 项 skill_enablement+obsolete_assets 契约全绿、-k 'skill or runtime_mode' 14 项失败与 git worktree HEAD 基线逐字节一致（零回归）、镜像 --check 无漂移、形态门 exit 0。另派新 subagent 只读更新后的下线参考文档，独立说出两个新接线面并成功执行文档中新写的 pytest 选择器（收集 49 项），构成 GREEN 侧证据；RED 侧为创建会话首稿确实完全遗漏这两面。loop-playbook Step 3 的「运行时失败优先于既有 it works 断言」与「静默欠抽取即缺陷」两条在本轮直接命中，无需修改。

## Optimization Points
- **未执行过的新技能：Step 3 退化证据兜底给的候选来源太弱。** 本次目标 `merge-skills` 创建于 2 小时前、从未真实执行，`evidence-utils.py --action collect --target skill:merge-skills` 返回的 10 条 findings 全是项目级（Present/Exercised），无一条指向该技能。`loop-playbook.md ## Step 3` 的「退化证据兜底」此时把候选限定为「既有 sanctioned 检查 + 文件系统地面真值（死链、缺失引用文件）」——照此执行本轮几乎空转：死链、`py_compile`、镜像一致性在创建会话里已全部通过，再查一遍仍然全绿。真正产出 4 个高危缺陷的证据来自两处兜底未点名的来源：①**直接执行技能自带的脚本**（对 `coverage_probe.py` 构造正样本/负样本/反向样本，才发现「枚举+状态码类文档所声称覆盖的 token 类根本没有 pattern 抽取」与「源路径不存在时仍打印 coverage clean 并 exit 0」）；②**创建会话本身**（auto-memory 的 `task_summary_experience` 笔记 + host transcript 索引），从中读到创建时的冒烟测试是「只测正样本」，因此以错误的理由通过。建议：Step 3 兜底补两条——「目标从未执行时，**创建会话就是执行窗口**，经 auto-memory 任务总结与 host transcript 定位」；「文件系统地面真值不足以判定以脚本为核心的技能，MUST 实跑其 scripts/references 中的代码并构造负样本与反向样本」。
- token-efficiency：挖掘 host transcript 找某个程序的输出时，用 `MISSING` 作匹配标记命中了 Edit 工具自身的模板串「Please check for UNEXPECTED changes and MISSING modifications」，一次返回 14 段无关 diff 片段（约 7k 字符上下文）才察觉，随后改用锚定该程序自身输出形态的 `fact tokens extracted:` / `coverage_probe\.py` 重跑才拿到有效证据。建议把「transcript 挖掘的 pattern MUST 锚定目标程序的输出格式，并排除 harness 模板串（Edit/Write 的 MISSING/INDENT errors 等）」写入 Step 3 的证据采集细则——这是一次可避免的重复读取 + 原文转储。
- **Step 8 的干预台账写法与引擎契约不符，且仓库现存示例在教错。** `evidence-step.md` 给出的 schema 是 `targetFinding` = 基线 findings 中的证据条目 id、`expectedSignal` = `{signalKey, direction}`，而 `evidence-utils.py:785` 在 `targetFinding` 不匹配任何 `id` 时直接 `raise CliError`。实测仓库 6 份 `intervention.json` 中 3 份（含两份 improve-skills 自己历史轮次写的）用的是散文式 `targetFinding`/`expectedSignal`，`--action compare` 一旦运行就会抛错——这些台账永远拿不到 Outcome-supported/Unobserved 判定，等于死账。SKILL.md Step 8 只说「写 intervention.json（targetFinding / change / baselineRunId / expectedSignal）」，既未申明 id 与对象形态的硬约束，也没提醒「现存文件可能是错误范例」；照仓库最近示例模仿就会继续产出死账。建议 Step 8 就地补一句判据：`targetFinding` MUST 是基线 findings 里真实存在的 `id`，`expectedSignal` MUST 为 `{signalKey, direction}` 且 signalKey 取自基线 signals，写完用「该 id 是否在基线 evidence 列表中 + signalKey 是否存在」自检（本轮已按此写出可被引擎接受的台账）。
