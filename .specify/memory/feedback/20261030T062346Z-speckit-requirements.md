---
id: "20261030T062346Z-speckit-requirements"
unit_id: "/speckit.requirements"
unit_type: "command"
run_id: "r20261030T054502Z-078a"
scope: "local"
probe: "speckit-requirements-wrapup"
kind: "internal"
slice: "commands"
feature: "078-coaching-skills"
feature_id: "078"
partial: false
created: "2026-10-30T06:23:46Z"
summary: "requirements-fix（analyze 回环 1/1）只修 requirements 侧四条：M-01 把 FR-024/A9 的不改写边界从「.specify/specs/** 一律冻结」改为「本特性 078-coaching-skills 目录之外的既有记录」，并写明本特性自身产物可正常改写与重跑；M-02 把 SC-006 的计数集从 5/5 扩为 FR-018 的八个身份坐标（源"
---

## Review
requirements-fix（analyze 回环 1/1）只修 requirements 侧四条：M-01 把 FR-024/A9 的不改写边界从「.specify/specs/** 一律冻结」改为「本特性 078-coaching-skills 目录之外的既有记录」，并写明本特性自身产物可正常改写与重跑；M-02 把 SC-006 的计数集从 5/5 扩为 FR-018 的八个身份坐标（源目录 / frontmatter name / skill_id 与 Canonical ID/Path / 运行时 unit id / flow-class 行 / probe 行与 probe id / 路由行与路径 / description 触发词与调用形态），8/8，并保留「按坐标计数、STR-001 被 STR-003 包含不重复计」；H-02 把 SC-008 第三条从「blocking 计数前后相等」改为 FR-027/A11 同单位——git diff 新增行 0 命中 BLOCKING_PATTERNS，点名可执行判定并命令基线读数入证据；C-01 的 requirements 侧把 checklists/requirements.md 的封闭面锚点由 A11 改为 A10、允许差异集改为恰为 _OBSOLETE_SKILLS 一行。未新增 FR/SC 编号（renumber 未触发），plan/contracts/tasks 未改。重跑三门均 pass：validate-requirements status=ok 0 error/0 warning；decomposition decision=proceed fr_count=29 ≤ 30；pre-analyze decision=pass errors=0 advisories=50（全部 missing-path，实现前目标路径未创建属预期；审计面从 1 个文件扩到 13 个文件，故读数由早期的 2 变为 50）。新增 gate-newline-baseline.txt 记录 SC-008 新判定单位的基线：扫描面 added_lines=0、blocking_hits=0，总量基线 blocking=27（destructive 20 / governance_kept 7）、violations=0。测试预算 docs-only，status=not-run-docs-only。本阶段无异常、无就地修复。

## Optimization Points
- 1) [token-efficiency] requirements 阶段的 pre-analyze 读数随下游产物落盘而变（advisories 2 → 50，审计面 1 → 13 个文件）；同一条读数在跨阶段比较时无法区分「回归」与「审计面扩大」。引擎可在 verdict 行同时打印分母（advisories=N over F files），并让证据行自带文件数。2) 本轮三条 findings（C-01 / H-02 / M-02）同属一类：枚举或集合在 owner 之外被复述后漂移（封闭面、计量单位、坐标数）。analyze 可固定加一道「验收面枚举 vs owner 枚举」的成员与单位对账，把这三次分别发现变成一次机械判定。3) 证据文件在本轮被覆盖，中间失败读数不留痕；可在捕获文件里加 attempt 序号，使回环过程可审计。
