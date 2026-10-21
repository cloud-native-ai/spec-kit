---
id: "introspection-20261021T130154Z"
created: "2026-10-21T13:01:54Z"
status: "superseded"
scope_filter: "disposition=open --format json (5 entries; framework hat; 0 pending bundles)"
scope_entries: ["20261021T092729Z-speckit-clarify", "20261021T105335Z-skill-improve-skills", "20261021T111429Z-speckit-requirements", "20261021T111631Z-skill-improve-skills", "20261021T115006Z-speckit-clarify"]
supersedes: null
confirmed_at: "2026-10-21T13:13:14Z"
---

# Introspection Report: introspection-20261021T130154Z

范围：本地库 **5** 条 open 条目（全部 `kind: internal`；0 个待处理入站包）。本仓戴**框架帽子**——根级 `templates`、`skills`、`shared`、`scripts`、`src/specify_cli` 五源目录俱在；全部条目的分流恒为 `local-sink(<channel>)`，Path B 未被路由选择。

核验方式：本批 5 条中有 2 条由本会话写下，按客观化分析门把整批核验委派给 1 个新鲜上下文只读子代理；其对每个候选问题回读框架根级源并给出 `path:line` 证据，回报“未发现异常”。委派结论与本会话独立核验一致。未以 `.specify/` 镜像为权威。

覆盖核对：范围 **5** = 问题成员 **2** + Excluded **3**，恰好覆盖一次。分流分布：`direct-fix` 1（F-02）、`speckit-requirements` 1（F-01）。同一条目的次生根（拆分门）经 `git blame` 核验为**已具备**（`stage-prompts.md:79`，提交 `df0ae2db`，早于本轮 09:27Z 运行），属执行遗漏而非源缺口，不再单独开问题。

## Findings

### F-01: 父规格 FR 引用被 pre-analyze-check 一律判为 dangling，而 validate-requirements 又禁止切片复用父编号

- **根因**: `pre-analyze-check.py` 的 `check_references` 只把本地 `requirements.md` 中定义的 `FR-NNN` 视为已定义；`FR` 前缀被排除在契约条款的 `external-clause` advisory 分支之外，因此切片正文里的父规格 `#FR-NNN` 一律报 `dangling-id` error；同时 `validate-requirements.py` 的 `id-contiguous` 要求本地 FR 编号自 001 连续，切片不能复用父编号，只能把精确映射降级到 notes（066 的实际绕行）。
- **证据锚点**: `skills/external/sdd-loop-driver/scripts/pre-analyze-check.py:181-185,201-203`；`scripts/python/validate-requirements.py:119-146`；`.specify/specs/066-loop-state-awareness-a/notes/parent-fr-mapping.md:6-18`。
- **成员条目**: 20261021T111429Z-speckit-requirements(成立)
- **分流决定**: local-sink(speckit-requirements)
- **优化方案**: 为 `pre-analyze-check.py` 增加父规格输入（如 `--parent-requirements`）或声明式 `Parent FR` 映射段，把父 FR 引用降为 `external-fr` advisory（与 `external-clause` 同构），并同步 `efficiency-model.md` §6 与单测；次生根 token-efficiency：以既有 slice spec 为惯例样本时只读目标 heading/FR 摘录，不整篇注入上下文。
- **建议处置**: 20261021T111429Z-speckit-requirements:processed

### F-02: Feature bind-or-create 归属在 feature-integration.md 与 create-requirements/clarify 之间未收敛

- **根因**: `feature-integration.md` 仍把 bind-or-create 归 `/speckit.requirements`（标题 “requirements phase”、状态表 Notes “Feature binding only”），而 `create-requirements/SKILL.md` 明确本技能不绑定、推迟到 `/speckit.clarify`，`clarify-taxonomy.md` 的 Feature Linkage 又要求 clarify 提案绑定——三处对“谁绑定”未收敛；同一条目的拆分门点已由 `stage-prompts.md:79` 落实，属执行遗漏而非源缺口。
- **证据锚点**: `shared/workflow/feature-integration.md:33,64-70`；`skills/internal/create-requirements/SKILL.md:146-151`；`shared/constants/clarify-taxonomy.md:11-15,83-85`；`skills/external/sdd-loop-driver/references/stage-prompts.md:79`。
- **成员条目**: 20261021T092729Z-speckit-clarify(部分成立)
- **分流决定**: local-sink(direct-fix)
- **优化方案**: 把 `feature-integration.md` § Feature Binding Rules 改名为 “Feature Binding Rules (clarify checkpoint)”，说明 requirements 只初始化 `Related Feature: Need clarification`、由 clarify Mode A 应用 binding rules；状态表 requirements 行 Notes 改为 “Initializes Feature Linkage; binding deferred to `/speckit.clarify` Mode A”，不改变状态转换归属；同步 shared 镜像并跑 `test_review_p1_review_loop.py` 与 `test_neutrality_budget.py`；拆分门点无需改源。
- **建议处置**: 20261021T092729Z-speckit-clarify:processed

## Excluded

- 20261021T105335Z-skill-improve-skills — sdd-project-setup 改进的运行结果记录（契约/镜像绿）；carrier 复验属未来执行证据，不是待改缺陷。
- 20261021T111631Z-skill-improve-skills — sdd-loop-driver 改进的运行结果记录（契约/镜像绿，7 个陈旧镜像文件已在当轮收敛）；条目中“S0 缺口”为 U0 笔误，无待改框架缺陷。
- 20261021T115006Z-speckit-clarify — 唯一“优化点”是绑定 065 与五项裁决冻结的运行记录，无框架级缺陷。
