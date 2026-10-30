---
id: "20261030T090012Z-speckit-review"
unit_id: "/speckit.review"
unit_type: "command"
run_id: "r20261030T085940Z-078a-repair"
scope: "local"
probe: "speckit-review-wrapup"
kind: "internal"
slice: "commands"
feature: "078-coaching-skills"
feature_id: "078"
partial: false
created: "2026-10-30T09:00:12Z"
summary: "record-only repair of the five P1 review findings: A10 now names the 20th hand-edited source (sanitize-utils LEGACY_SKILL_NAMES) with the allowed difference set unchanged; feature status and baseline "
---

## Review
record-only repair of the five P1 review findings: A10 now names the 20th hand-edited source (sanitize-utils LEGACY_SKILL_NAMES) with the allowed difference set unchanged; feature status and baseline are committed; 19 analyze residuals carry dispositions (2 fixed, 17 accepted-deferred); SC-001/SC-005 are partial with an explicit transport validation gap; closure will compare names with comm -13 baseline-failed.txt final-failed.txt. Validators pass (0 errors; 7 expected missing-path advisories per stage); targeted set 122 passed / 0 failed / new_failures 0. No implementation code changed.

## Optimization Points
- token-efficiency — 为定位 M-08…L-19 的 finding 正文，本轮先对主目录做了全量 grep（超时后被停止），随后改为仓内定向搜索与既有 evidence 指针；后续先查仓库内 owner 与证据文件，避免 home-wide scan。
- analyze 残留 finding 的正文未在 analyze 阶段落盘，review 修复轮只能按门禁行与既有 commit 重建 19 条处置；建议 review 阶段要求 analyze 把 9M/9L 正文写入 tracked evidence，再按 ID 逐条处置。
- A10 类封闭面声明应同时接受“注册表增长后被迫获得旧字面量的消费方”；本轮以 A10 单点修订加 guard 既有 OBSOLETE-ASSET-REGISTRY 剥离语义收口，未新增第二份手写枚举。
