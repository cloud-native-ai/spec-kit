---
id: "20261005T170700Z-skill-create-team"
unit_id: "skill:create-team"
unit_type: "skill"
run_id: "create-team-session-driven-self-improvement-20261006"
scope: "local"
probe: "skill-create-team-wrapup"
kind: "internal"
slice: "skills"
disposition: "processed"
partial: false
created: "2026-10-05T17:07:00Z"
summary: "create 模式一次完整走通:goal-based 分支(引擎精确匹配 + parse 复述 + 四要素分析)→ preset 匹配(confidence none,不复用)→ pattern 决策树(Q1 否 / Q2 否 / Q3 是 → serial,并明示误判 continuous 会强制 L1 停在报告态)→ roster(6 席,Type 按写目标判定:交付物是定义类文件,故按 co"
introspection_ref: "introspection-20261006T140432Z#F-03"
disposition_reason: "introspection:introspection-20261006T140432Z#F-03"
---

## Review
create 模式一次完整走通:goal-based 分支(引擎精确匹配 + parse 复述 + 四要素分析)→ preset 匹配(confidence none,不复用)→ pattern 决策树(Q1 否 / Q2 否 / Q3 是 → serial,并明示误判 continuous 会强制 L1 停在报告态)→ roster(6 席,Type 按写目标判定:交付物是定义类文件,故按 conceptual-model.md § 消解条款必含唯一 Meta supervisor 作为 canonical 落盘者,Worker 只产补丁到工作区)→ pattern config(serial DAG + file-path-only + per-handoff verification + 粒度声明 + summary every:1 交付到 goal 索引目录)→ 直接落盘不设停等 → 落盘后自校验 + territory verify。粒度纪律在本轮真实发挥了一次作用:按文件计数发现 skills/ 有 13687 文件,据此否掉了 skills/** 通配 write 范围,改为 non_path 登记开放集合 + 具名目录后续 modify 追加。D9 四项细节全部落到 team.md 的可执行位置(## Goal 小节的编号清单 + territory.non_path + 各成员 responsibility),而非仅作叙述。零写入 goal.md。

## Optimization Points
- **team.md 的结构不变量没有引擎校验,只能靠现场手写校验器。** schema 要求四个小节各一、`## Self-Improvement Contract` 恰好一次,但落盘前后没有任何程序步骤检查它。本轮 `## Dynamic Structure` 出现 2 次(某成员 responsibility 里写了字面量交叉引用「依据见 ## Dynamic Structure 的粒度声明」),是我临时写 python 数标题才发现的——一个「标题恰好一次」的契约测试在被守物坏掉时会红,而现场手写的一次性校验器下次不会有人再写。建议:create-team 带一个 `validate-team-md.py`,或让 tests/contract/ 覆盖 team.md 标题唯一性;顺带把「正文引用小节 MUST NOT 用字面量标题」写进 schema notes,因为这是最容易踩的形态。
- **容量制品缺口:6 席里 5 席回落到通用 stage 模板。** `.specify/agents/templates/` 只有 skill-verifier 与 structure-adjuster,故本轮 4 个 executor 席全部指向 agent-stage-executor-template、1 个 evaluator 席指向 agent-stage-evaluator-template,roster 的区分度全靠 responsibility 文本承载。对「改框架定义文件」这类工作没有可复用的具名容量。evaluator 席还额外要在 responsibility 里解释为什么不用 skill-verifier(其容量是审技能执行证据,窄于红线/镜像/契约三类判定)——这段解释每次建同类团队都要重写一遍。建议:若这类团队会复现,沉淀 framework-definition-author 与 framework-contract-verifier 两个容量制品。
- **territory 必须在 create 时声明,而落点要等设计才定,这条张力没有处置规则。** 本轮技能侧落点名要等 S1 契约才定,但 territory 是 create 时字段。实测 `skills/` 有 13687 个文件,以 `skills/**` 通配占位即不可交付(粒度纪律按文件计数校验会直接判超),故现场裁为:write 不含 `skills/**`,开放集合登记到 `non_path`(type: scope-set),并在粒度声明里写明「具名目录经 /speckit.team modify 追加,MUST NOT 以通配承接」。这条处置没有任何文档规定。建议 create-mode.md 补一条:设计期未定的落点走 non_path + 后续 modify,不得以大通配占位;并把「文件计数」这一步的样例命令写进粒度纪律(本轮是靠 `find <dir> -type f | wc -l` 才暴露 13687 这个数)。
- token-efficiency — 无原文转储:`skills/` 的 13687 文件用 `find | wc -l` 取数而非列举,`.specify/memory/evidence/` 的 106 文件全程未读(只作为 read 范围声明并写明 MUST 走摘要)。但 `create-mode.md`(131 行)与 agent-serial-orchestration-template.md(131 行)整篇读入,其中 iteration/continuous 相关内容与 Cross-Session Resume、Final Report 细节本次用不到,约六成是无效读入;定点读「Persisted team.md schema + Schema notes + 消解条款 + Stage granularity discipline」四节即可。
