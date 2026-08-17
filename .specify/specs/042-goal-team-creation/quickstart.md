# Quickstart: 042-goal-team-creation

从零走一遍"定义 goal → 基于它创建团队(含分解与成组建队)→ 聚焦运行"。

**验证标注**:标 ✅ 的命令已在临时 repo root(`/tmp`,`--repo-root` 隔离)实际执行验证(2026-08-17);标 📌 的是本需求新增面,由契约测试钉住(`tests/contract/test_targets_check.py`、`test_focus_target_resolution.py`、`test_goal_team_creation.py`),实现合入后方可照抄执行。

## 0. 前置

```bash
.specify/scripts/bash/check-prerequisites.sh --json --paths-only   # ✅ 既有,取 REPO_ROOT
```

## 1. 先有一个已归档的 goal(既有面)

```bash
python3 scripts/python/goal-utils.py create improve-harness \
  --objective "spec-kit 框架自身的持续改进闭环运转良好" \
  --criterion "每月至少消化一批用户反馈" --json          # ✅ {"created": ".specify/goal/improve-harness/goal.md"}
python3 scripts/python/goal-utils.py targets improve-harness \
  --add "反馈处理链路的文档与脚本拆分完成" --json        # ✅ {"slug": "improve-harness", "added": "T-001"}
python3 scripts/python/goal-utils.py list --json         # ✅ archive 枚举,goal-based 分支的识别数据源
```

(也可完全不手工加 Target——留给第 3 步的分解提议。)

## 2. goal-based 创建:传入已定义 goal

对话命令:

```text
/speckit.team create 基于 improve-harness 这个 goal 组建团队
```

流程要点(契约 `goal-based-create`):`list` 枚举精确命中 `improve-harness` → 确认进入分支 → `parse_goal` 加载并复述 → 呈现四要素分析(维度/判据/既有 Target/可达成性)→ 用户裁决路径。传错名字会得到逐字前缀 `goal 未定义:` 的拒绝并指向 `/speckit.goal create`;终态 goal 直接拒绝(✅ 该两类拒绝复用既有 `list`/`parse_goal` 事实,无新命令)。

## 3. 分解提议与成组批准

分析判定"宽泛需分解"并被用户采纳后:

```bash
# 📌 干跑校验(新增,零写入;校验器与 --add 同源)
python3 scripts/python/goal-utils.py targets improve-harness --check "评测引擎的会话取证链路拆分完成"
# 期望 exit 0;步骤形语句/复述判据 → exit 2 并附原因

# 批准后逐条落盘(既有面,✅ 已验证)
python3 scripts/python/goal-utils.py targets improve-harness --add "评测引擎的会话取证链路拆分完成" --json
```

确认门禁以 `分解提议` 小节一次呈现全量(每条语句 + 理由 + `--check` verdict);单次批准 → 逐条 `--add`。中途中止:已落盘保留,重发起时既有 open Targets 自动成为复用基线,零重复授权。

## 4. 每 Target 一个团队

批准后成组创建(N teams : 1 Goal):每个团队 `goal_slug: improve-harness`、`focus_target: T-00n`(字段插在 `goal_slug` 之后)、slug 缺省 `improve-harness-t00n` 查重落盘;roster/pattern 以各 Target 语句走既有 `match-team-preset.py --goal "<语句>"` 派生(✅ 既有)。

territory 提议落盘前:

```bash
# 📌 两两不相交校验(新增薄脚本;判定文法 import 自 build-summary-input.py)
python3 skills/create-team/scripts/verify-territory-disjoint.py --input proposals.json --json
# 期望 exit 0;任何 overlap/undecidable → exit 4 列出争用区 → 改划重跑或移交 /speckit.goal coordinate
```

## 5. 聚焦运行

```text
/speckit.team run improve-harness-t003            # 无显式 --target
```

📌 解析顺序:显式 `--target` > `focus_target` > 无。上例解析为 `T-003`,确认门禁披露:

```text
本次 Target: T-003 — <语句>(open)(团队默认)
```

解析值走既有五项 preview 校验(悬空/终态/跨 goal/goal 终态一律拦截,终态复核二分无旁路);报告行 `**Target 指派**: T-003(<语句>)(团队默认)`;新台账条目由 Team Supervisor 写 `"target_ref": "T-003"`。未声明 `focus_target` 的团队照旧对 goal 整体运行,行为与引入前逐字节等价。

## 6. 冲突与重划

同 goal 下团队写域重叠或事后新增团队 → `/speckit.goal coordinate improve-harness`(既有,提议形,人批准写回各 team.md)。默认聚焦的 Target 转 `dropped` → run 被五查拦截,经 `improve-team` 重聚焦或 `/speckit.goal targets --set open --id T-00n` 重开,无终态执行旁路。
