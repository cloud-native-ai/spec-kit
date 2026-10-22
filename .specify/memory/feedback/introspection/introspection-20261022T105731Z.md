---
id: "introspection-20261022T105731Z"
created: "2026-10-22T10:57:31Z"
status: "confirmed"
scope_filter: "disposition=open --format json (4 entries; framework hat; 1 pending bundle)"
scope_entries: ["20261022T093747Z-skill-sdd-loop-driver", "20261022T100515Z-skill-sdd-loop-driver", "20261022T064104Z-speckit-requirements", "20261022T064746Z-speckit-clarify"]
supersedes: null
confirmed_at: "2026-10-22T11:42:49Z"
---

# Introspection Report: introspection-20261022T105731Z

范围：本地库 **4** 条 open 条目（`kind: internal`；框架帽子；1 个待处理入站包）。核验方式：逐条读取条目正文，回读 `sdd-loop-driver` 技能脚本/参考与相关引擎源，并与 067/068 两次运行的状态脊 Framework Observations 交叉核对；入站包的 20 条由三个只读核验代理对当前框架源逐项核验（见 digest 报告）。

覆盖核对：范围 **4** = 问题成员 **2** + Excluded **2**，恰好覆盖一次。

## Findings

### F-01: sdd-loop-driver 过程摩擦：分派预算、状态脊/台账、镜像纪律与门约束

- **根因**: `sdd-loop-driver` 的编排纪律与工具面未完全收敛——TDD 重段超出 120 回合预算；E2 台账需手写 JSON 围栏而提示词只给散文描述；`sync-mirrors --only` 是 scope 级会拖带继承漂移；plan 阶段门不检查契约条款形态；create-tasks 不生成 GATE-7 引用的 coverage 基线；创建分支脚本与「子代理不得切换分支」纪律冲突；`SPINE_WRITE_MODE=direct` 允许子代理改写驱动状态脊。
- **证据锚点**: `skills/external/sdd-loop-driver/references/efficiency-model.md`; `references/stage-prompts.md`; `scripts/python/audit-test-budget.py:4,63`; `scripts/python/sync-mirrors.py`; `scripts/bash/create-new-requirements.sh:265-270`; `scripts/bash/create-new-plan.sh:51`; `.specify/specs/068-exec-quant-feedback-channel/notes/post-merge-067.md`（同类过程摩擦记录）。
- **成员条目**: 20261022T100515Z-skill-sdd-loop-driver(成立), 20261022T093747Z-skill-sdd-loop-driver(成立)
- **分流决定**: local-sink(improve-skills)
- **优化方案**: (a) TDD 重段按「测试写作 / 实现」拆分至 ≤4 任务，或提升 implement 段回合预算；(b) E2 台账由 runner 自动写 JSON 围栏，提示词携带字面 `<-- test-budget:begin -->` 标记；(c) 镜像同步任务行使用文件级 `--only` 前缀；(d) plan 阶段门增加契约条款形态检查（`clause_extract`）；(e) create-tasks 生成 coverage 基线，或 GATE-7 改为自建基线；(f) 解决 `create-new-requirements.sh` / `create-new-plan.sh` 的切分支行为与派发纪律冲突（增加 `--no-branch` 或改由驱动建线）；(g) `SPINE_WRITE_MODE` 对驱动/子代理分离。次级路由：`improve-tools`（audit-test-budget 围栏）、`/speckit.requirements`（plan 门条款形态检查机制）。
- **建议处置**: 20261022T100515Z-skill-sdd-loop-driver:processed, 20261022T093747Z-skill-sdd-loop-driver:processed

## Excluded

- 20261022T064104Z-speckit-requirements — 无 actionable 优化点（clean-run；唯一一点为正向观察：checker 首轮 exit 0、清单全绿）；建议处置 ignored，理由 clean-run-no-points
- 20261022T064746Z-speckit-clarify — 0 优化点（pass）；建议处置 ignored，理由 clean-run-no-points
