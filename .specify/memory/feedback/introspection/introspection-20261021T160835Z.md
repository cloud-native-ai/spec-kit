---
id: "introspection-20261021T160835Z"
created: "2026-10-21T16:08:35Z"
status: "confirmed"
scope_filter: "disposition=open --limit 0 --format json (5 entries; framework hat; 0 pending bundles)"
scope_entries: ["20261021T130319Z-speckit-plan", "20261021T132940Z-speckit-tasks", "20261021T134937Z-speckit-checklist", "20261021T135429Z-speckit-feedback", "20261021T155458Z-skill-git-utils"]
supersedes: null
confirmed_at: "2026-10-21T16:10:37Z"
---

# Introspection Report: introspection-20261021T160835Z

范围：本地库 **5** 条 open 条目（全部 `kind: internal`；0 个待处理入站包）。本仓戴**框架帽子**——根级 `templates`、`skills`、`shared`、`scripts`、`src/specify_cli` 五源目录俱在；全部分流恒为 `local-sink(<channel>)`。本次按上一轮教训使用 `--limit 0` 全量盘点，并与 `--action status`（108 条总量）交叉核对。

核验方式：小批量（≤20 条）逐条内联读取；对每个优化点回读框架根级源并给 `path:line` 证据。未以 `.specify/` 镜像为权威。

覆盖核对：范围 **5** = 问题成员 **3** + Excluded **2**，恰好覆盖一次。分流分布：`improve-skills` 2（F-01/F-02）；Excluded 2（已被治理决定/既有 backlog 覆盖）。

## 元观察（不属任何单一条目）

- **M-01（复发）**：`--action list --disposition open` 的默认 limit 仍为 5（`scripts/python/feedback-utils.py:1605`）；上一轮已以 backlog M-01 登记（`backlog.md:137`），本轮条目 `20261021T135429Z-speckit-feedback` 再次确认。无需重复建行。

## Findings

### F-01: Slice spec 目录解析与条款形态仍是单特性/单分支假设

- **根因**: `common.sh` 的 `get_feature_paths` 从当前分支前缀解析 `REQUIREMENTS_DIR`（`find_feature_dir_by_prefix`），`check-prerequisites.sh` 没有 `--spec-dir`/`--feature-dir` 覆盖；066 slice 在 065 分支下只能手工指定目录；`common.sh` 还硬依赖未导出的 `CWS_LIB_BASH_HOME`；plan 期未强制 canonical `C-N` 条款形态，066 使用 CLI/SNP/RUL/CMP 后条款覆盖只能由任务映射承担（F-05 复发）。
- **证据锚点**: `scripts/bash/common.sh:5,13-19,117-145`；`scripts/bash/check-prerequisites.sh:18-45,263-267`；`shared/definitions/contract-clause-definitions.md:13,42-43`；`scripts/python/clause_extract.py:46-56`。
- **成员条目**: 20261021T132940Z-speckit-tasks(成立), 20261021T134937Z-speckit-checklist(成立)
- **分流决定**: local-sink(improve-skills)
- **优化方案**: 为 `check-prerequisites.sh` 增加 `--spec-dir`/`--feature-dir` 显式覆盖（或 slice-aware 目录解析）；把 cws-lib-bash 改为可选并给出可移植 fallback；在 plan 期增加 canonical `C-N` 条款形态前置检查；补脚本与契约测试，并在 backlog 中标注 F-05/F-08 复发。
- **建议处置**: 20261021T132940Z-speckit-tasks:processed, 20261021T134937Z-speckit-checklist:processed

### F-02: git-utils 提交分组仍依赖人工路径前缀分类

- **根因**: 并行会话在同一分支留下混合工作树，git-utils 没有确定性的 changed-path 分组配方或助手；本次只能人工按路径前缀分成 4 组提交，虽成功但存在可避免的审查成本。
- **证据锚点**: `.specify/memory/feedback/20261021T155458Z-skill-git-utils.md:19-20`；`docs/git-workflow.md:10`（临时分支模型）。
- **成员条目**: 20261021T155458Z-skill-git-utils(部分成立)
- **分流决定**: local-sink(improve-skills)
- **优化方案**: 在 git-utils 增加一个确定性的 changed-path 分组助手/配方（按 top-level 前缀给出建议提交组），并说明混合工作树的审查顺序；属低优先级增强，无失败证据。
- **建议处置**: 20261021T155458Z-skill-git-utils:processed

## Excluded

- 20261021T130319Z-speckit-plan — 治理决定已记录：`.specify/memory/features/065.md` 与 `features.md:74` 明确用户裁定「拆三片、先 065a」，065a 为 active、066 为 historical；残留的 066 active-basis 表述属项目级清理，不是框架缺陷。
- 20261021T135429Z-speckit-feedback — 默认 limit=5 仍存在于 `scripts/python/feedback-utils.py:1605`；该缺陷已由上一轮 backlog M-01（`backlog.md:137`）登记，本轮为复发观察，不重复建行。
