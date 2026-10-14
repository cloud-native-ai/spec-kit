---
id: "20261013T162355Z-speckit-feedback"
unit_id: "/speckit.feedback"
unit_type: "command"
run_id: "consume-20261013-batch3-bundles"
scope: "local"
probe: "speckit-feedback-wrapup"
kind: "internal"
slice: "commands"
disposition: "processed"
partial: false
created: "2026-10-13T16:23:55Z"
summary: "框架帽子判定正确(五源目录实测),Path B 未被选中亦未被请求;58 条物料(本地 32 + 入站 26,其中 12 条为自我投递副本已按本地计一次)由 4 个并行只读核验器对框架源取证,11 条异常全部上交无隐瞒;32 条 open 归零,24 行入 backlog,2 行按 owner 实测关闭。主要成本在两处本可避免的返工:inventory 首读被已知截断缺陷误导一次、报告骨架靠 ex"
disposition_reason: "consume-20261013-batch4 — P1 count-truncation(3rd round, existing row), P2 introspect-register section-marker hijack(new direct-fix row), P3 skeleton(F-11 row); all 3 verified against source this session"
---

## Review
框架帽子判定正确(五源目录实测),Path B 未被选中亦未被请求;58 条物料(本地 32 + 入站 26,其中 12 条为自我投递副本已按本地计一次)由 4 个并行只读核验器对框架源取证,11 条异常全部上交无隐瞒;32 条 open 归零,24 行入 backlog,2 行按 owner 实测关闭。主要成本在两处本可避免的返工:inventory 首读被已知截断缺陷误导一次、报告骨架靠 exit 2 反推两轮。

## Optimization Points
- 命令模板与技能正文的 inventory/A3 快照步仍不带 `--limit 0`:`--action list` 的 `count` 是截断后计数(`feedback-utils.py:857-858`,`--limit` 默认 5 在 `:2013`),本轮首次读得 5 而真实 open 为 32,若未复核即会对 5 条做自省并声称覆盖全量;这是该缺陷第三轮复发且第二次咬到编排者,owner 文件 `templates/commands/feedback.md` 与 `scripts/python/feedback-utils.py` 至今未动,`skills/internal/manage-feedback/references/path-a-digest.md` 亦未加防呆指针 —— 修复需先在 (a) 改引擎语义 与 (b) 补 `--limit 0`+明写 count 为截断后 之间裁定。
- `introspect-register` 的小节定位用 `body.find("## Findings")` 与 `body.find("## Excluded")` 的首次字面命中(`feedback-utils.py:567-572`),因此**正文中的行内代码里出现这两个小节标记字面量就会把解析锚点搬走** —— 本轮两次 exit 2 皆源于此(先是前言里以 code span 引用排除小节名,再是 F-11 方案里以 code span 引用两个小节名),而该约束既不在 `docs/reference/skills/feedback.md:155-169` 的三约束内、也无 `templates/` 骨架承载,只能靠 exit 2 反推;建议要么把引擎改为只匹配行首小节,要么在 schema owner 明写「正文 MUST NOT 出现小节标记字面量」。
- A3 报告无骨架模板导致两处自身缺陷要靠程序补算才发现:`scope_entries` 手写时重复了两个条目 id(触发 C-5 风险),排除区手写时把一条已归属 F-09 的条目误留作「占位行」,使成员∪排除与范围不闭合;`path-a-digest.md` 的 A3 步已声明 V-1 判据以引擎为准,但引擎只在落盘后才给判定 —— 与 F-11 同根,一处 `templates/introspection-report-template.md` 骨架 + 一行「先程序化算覆盖再落盘」即可消除。
