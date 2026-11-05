---
id: "20261105T064532Z-speckit-analyze"
unit_id: "/speckit.analyze"
unit_type: "command"
run_id: "r20261105T033420Z-082a-re"
scope: "local"
probe: "speckit-analyze-wrapup"
kind: "internal"
slice: "commands"
feature: "083-mechanism-policy-separation"
feature_id: "082"
partial: false
created: "2026-11-05T06:45:32Z"
summary: "082 的 analyze 读闸完成。确定性引擎侧：pre-analyze(--stage tasks) 判 pass、errors 0、advisories 123（全部为待建产物的 missing-path）；validate-tasks PASS 0/0；flow-class-check exit 0；check-prerequisites MODE C（tasks 可用）。但 valida"
---

## Review
082 的 analyze 读闸完成。确定性引擎侧：pre-analyze(--stage tasks) 判 pass、errors 0、advisories 123（全部为待建产物的 missing-path）；validate-tasks PASS 0/0；flow-class-check exit 0；check-prerequisites MODE C（tasks 可用）。但 validate-decision-tensions 以 spec 目录重跑后报 5 条 HIGH（dtr-anchor 1 + expected-sacrifice-unmapped 4），且 coverage-baseline.txt 缺失使子句覆盖恒为 0（account-clause-coverage: claimed 0 / baseline MISSING）——两者都落在 plan / tasks 的回落面，不是分析侧误报。checklist 上呈的四个 medium 全部复现：GM-01/GM-03/GM-04/GM-08/GM-11 的模块与条目计数三处互不相容；requirements 第 306 行的自相矛盾句；GM-12 裸串字面与需求侧 code span 形式；以及两项承载义务。另新发现：coaching/run 的零命中断言在 GM-12 合流点与 tasks T020/T027 之间模块路由不一致；SW-05 的 grep 作用域（SKILL.md 与 references/）窄于 GATE-6/T027 的 skills/**/SKILL.md，使 coaching-skills/references 与 run-skills/references 不被扫描；feature-ref 改写框架源（9）只枚举 7 个路径；fixture 目录序数在 D13/quickstart S13/S14 三处漂移。本单元流程侧无失效：读闸顺序（先引擎后语义）正确、证据指针逐条可回溯、只读边界守住（除 .specify/memory 记账外无写面）。

## Optimization Points
- **token-efficiency** — 首轮 validate-decision-tensions.py 以 plan.md 文件路径作 --spec，引擎返回 status=unreadable 而各标签均为 0 错误，极易被读作"干净"；改以 spec 目录重跑才拿到 5 条 HIGH。确定性引擎的入参形态（目录 vs 文件）应在首次调用前对齐 --help / manifest，而不是把一次试跑当探测。
- 本轮读数来自 10+ 个确定性引擎（pre-analyze / validate-tasks / validate-decision-tensions / account-clause-coverage / audit-test-budget / flow-class-check / check-prerequisites），语义比对留给阅读——这是本单元应然分工；但 checklist 已呈的 GM 计数漂移一类（"六个模块"对 5 行表、8 = 3+5 对实际 2+6）本可由 GM 表的行数断言脚本化，属可下放的确定性工作。
- artifact_correctness 轴为 not_evaluated (no_declared_checks)：analyze 单元未声明任何可机检核对项，导致每次 analyze 的产物正确性只能由人读背书；建议登记最小声明集（例如"findings 每行带可回溯证据指针"的格式断言）。
