# Line State — speckit-docs-expression

- line_id: `speckit-docs-expression`
- run_id: `r20261024T1208Z-docs-expression`
- project_dir: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit`
- repo_root: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit`
- worktree: `none（本地拓扑，单工作区）`
- base_sha: `b852f2eb`（069a 已合并 master）
- trunk: `master`
- topology: `local`
- state: `running`

## U0 入口声明

- 目标项目：spec-kit 框架源码仓（本地 `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit`）
- 终态权威文档：仓库 `AGENTS.md`、`CONTRIBUTING.md`、`README.md`、`.specify/memory/constitution.md`、`templates/commands/*`、`.qoder/commands/*`、`skills/internal/*`、`docs/`；输入材料为 `kangaroo-xuanji` Feature 001 的完成态与 `.specify/specs/001-arch-redesign/review.md`（10 条 P1 框架建议）。
- 特性切片：引入「执行（execution）」与「表达（expression）」二元概念（执行 = 默认 SDD 流程与动作类流程；表达 = 文字/沟通类流程，`speckit.docs`、`speckit.humanize` 归此类）；在二元模型上优化以文档开发为核心的 SDD；统一代码与文档的 SDD 方法论（代码 = 计算机语言写的文档，文档 = 人类语言写的代码）。
- 断点：U1 自动探测。初始事实：`master @ 76ce86a0`，工作树干净；`.specify/specs` 最大编号 `068`；本特性尚无 specs 目录。
- 阶段计划：requirements → clarify → plan → tasks → checklist → analyze → implement → review → 本地合并（全程本地原生子代理；不启动 qodercli）。
- U0.5 自检：目标/拓扑/权威/切片/断点已写入；尚未编辑目标仓产品文件、未加载维护技能、未派发 subagent；阶段计划已写出。

## 前置检查

- 本地拓扑；宿主具备原生子代理（Agent）。
- 目标仓为框架源码仓（self-hosting）：框架源在 `templates/`、`commands/`、`skills/`、`scripts/`、`src/`；`.specify/` 为客户端运行时，按 Two Hats 不得把框架级改动只落在 `.specify/` 镜像。
- 既有相关特性：`062-humanize-command`、`067-loop-efficiency-hardening`、`068-exec-quant-feedback-channel`；本特性须增量叠加，不重复已交付能力。
- 输入摩擦：Feature 001 review 的 REC-T1…REC-D1（10 P1 + 5 P2），以及实测“文档型 SDD 门禁链占约 70%”的时长结构。

## 当前阶段

- stage: `complete`
- attempts: `0`
- stage_started_at: `1792868012`
- stage_deadline_epoch: `1792871612`
- last_verdict: `CLOSED：069a（分类+文档门禁）与 069b（同构/迁移/度量）均合并 master；最终定向 278 passed；镜像/副本 OK；Feature 069 Implemented；未 push。已知：069a SC 2 partial/4 deferred；069b SC-004 unknown；F6 仪器插桩 deferred（REC-069b-08）`
- next_stage: `none（已收尾）`
- evidence_ptr: master `d8df8cad`；`.specify/specs/069a-*/review.md`；`.specify/specs/069b-*/review.md`
- commit: `d8df8cad`（069b merge；069a merge `b852f2eb`）
- gates: `target repo clean; next spec number expected 069; no spec dir for this slice yet`

## 隔离与纪律

- owned_paths（预计）：`.specify/specs/069-*/**`、`.specify/memory/**`、`templates/**`、`commands/**`、`skills/**`、`docs/**`、`tests/**`、`src/**`（实现阶段按 plan 收窄）。
- forbidden_paths：`docs/public/**`、`.git/**`、目标仓之外的其他仓库。
- 既有脏文件不提交、不还原；不 push；不进入下一阶段。

## 历史

- 2026-10-24T12:08Z U0/U1 起始：master `76ce86a0`，工作树干净；最大 spec 编号 068；本切片无现有 spec；进入 requirements。

## 拆分记录（2026-10-24，plan 入口门 split-required）

- measured: 41 FR / 13 SC（clarify 5183bd8f）；fr_ceiling=30；task_ceiling=40
- reasons:
  1. fr_count 41 > 30，按 efficiency-model §5.3 必须拆分；
  2. 两个关注面可独立验收：分类本体 + 文档型门禁（A/B/D/E）与同构映射 + 迁移/度量（C/F/G）。
- ceilings: 8–30 FR / 10–40 tasks per slice
- base_commit: 5183bd8f
- proposed_slices:
  - `069a-flow-classification-docs-gates`：FR-001–FR-017、FR-023–FR-032（27 FR）；分类本体/台账/门禁不变量/六面文档门禁/docs+humanize 成员；预估 10–20 tasks。
  - `069b-isomorphism-migration-metrics`：FR-018–FR-022、FR-033–FR-041（14 FR）；同构映射与边界/迁移兼容/分发/度量；预估 10–14 tasks。
- 备选（未采用）：三片 069a 分类本体+不变量（17）、069b 文档门禁+成员（10）、069c 同构+迁移+度量（14）；碎片更多、编排成本更高。
- 确认状态：confirmed-user（2026-10-24 选择「两片（推荐）」）
- 约束：切片按顺序逐条走完整链，禁止同线并行；切片各自独立 spec 目录与注册表绑定，Related Feature 仍为 069。

- 2026-10-24T23:45Z 069a CLOSED：review-fix A（1b5f4741）+ B（88561737）；合并 b852f2eb；069b 待启动。

- 2026-10-25T03:10Z CLOSED：069a merge b852f2eb；069b merge d8df8cad；278 定向测试通过；Feature 069 Implemented；未 push。
