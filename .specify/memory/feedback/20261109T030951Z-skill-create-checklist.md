---
id: "20261109T030951Z-skill-create-checklist"
unit_id: "skill:create-checklist"
unit_type: "skill"
run_id: "r20261109T023000Z-auto-closeout"
scope: "local"
probe: "skill-create-checklist-wrapup"
kind: "internal"
slice: "skills"
feature: "091-auto-git-closeout"
feature_id: "091"
partial: false
created: "2026-11-09T03:09:51Z"
summary: "create-checklist 阶段顺：模板/Methodology/create-checklist SKILL 三处口径一致，gate 集合可判定；reader face 与 requirements 面联动失效、run-determination 的两处接口形状是本阶段主要摩擦。"
---

## Review
create-checklist 阶段顺：模板/Methodology/create-checklist SKILL 三处口径一致，gate 集合可判定；reader face 与 requirements 面联动失效、run-determination 的两处接口形状是本阶段主要摩擦。

## Optimization Points
- 1) doc-consistency-check.py --faces reader 只在显式 --path 下判定，--spec-dir 形态直接返回 not-applicable，导致 expression-gates 为 checklist 阶段钉的 G-checklist-reader（blocking）在 spec 目录上永不触发；建议 engine 对 --spec-dir 递归判定各 spec 产物的 reader 声明，或让 gate 表改用 --path 形态。2) run-determination.py --names-current 期望的是 run-tests.sh --names-out 的 FAILED nodeid 列表文件（引擎侧 'a readable file'），--help 只写 'sorted FAILED-nodeid list from run-tests.sh --names-out'，未提示这是文件路径；误传会被判成 artifact_correctness=regressed。3) 模板 requirements-template.md 不含 Readers/Reading scenario 行，而 reader face 对 requirements.md 判定 fail（reader-declaration-missing），模板与 gate 互不匹配。4) pre-analyze-check.py 的 missing-path advisor 会对 spec 正文里任何反引号路径（哪怕只是引用既存裁决）开 advisory，checklist 引用 tasks 裁决即新增一条，需调用方回避写法而非引擎区分「引用」与「声明」。5) run-determination.py 同一 (unit_id, run_id) 二次 determine 静默返回 duplicate 且不覆盖，错了只能换 run_id 或留坏记录，没有 --redetermine。
