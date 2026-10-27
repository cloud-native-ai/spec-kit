# Pre-Change Measurements — Feature 072 client-self-improvement (implement part 1/8)

> 测量日期: 2026-10-27（UTC，implement Setup 阶段 T001，任何实现编辑之前）。
> 用途: 实现期每个"红先行 / 无新增失败 / 镜像无新增漂移"声称的日期化控制冻结。
> 对应锚: tasks.md § Measured Premises（生成期 HEAD `646e1bfe`）——本表为 implement 期复测值。

## 1. 工具链版本

| 工具 | 命令 | 实测输出 |
|------|------|----------|
| Python | `python3 --version` | `Python 3.11.11` |
| pytest | `python3 -m pytest --version` | `pytest 8.4.2` |
| bash | `bash --version` | `GNU bash, version 4.4.20(1)-release (x86_64-koji-linux-gnu)` |
| git | `git --version` | `git version 2.43.5` |

## 2. Git 快照

| 项 | 命令 | 实测输出 |
|----|------|----------|
| HEAD | `git rev-parse HEAD` | `fe089338082a3dbd2b49e14ba9912468252d6308`（analyze 072 收尾提交） |
| 工作树 | `git status --short` | 0 行（干净） |

注: tasks.md 生成期记录的 HEAD 为 `646e1bfe`；`fe089338` 是其后的 analyze 阶段收尾提交，tasks.md 内容未随该提交变化（本阶段复核一致）。

## 3. 镜像三作用域计数（`python3 scripts/python/sync-mirrors.py --check`）

| 作用域 | 结果 | 计数 |
|--------|------|------|
| `templates/` == `.specify/templates/` | ok | 22 files |
| `skills/internal/` == `.specify/skills/internal/` | ok | 136 files |
| `agents/` == `.specify/agents/templates/` | ok | 3 files |
| `scripts/` == `.specify/scripts/` | ok | 112 files |
| `shared/` == `.specify/shared/` | ok | 55 files |
| `.specify/skills/improve-skills/references/loop-playbook.md` | **DIFF** | 1 处（plan 既录漂移，判据 = 无**新增**） |

退出结论: `DRIFT detected`（仅既录一处）。

## 4. 命令副本再生成检查

- `python3 scripts/python/regen-command-copies.py --check` → `OK: all per-tool command copies match the source templates.`

## 5. 守护套件计数（def 级，实际文件名带 `test_` 前缀）

| 套件族 | 命令 | 实测计数 |
|--------|------|----------|
| 071 六套件 | `grep -c "def test_" tests/contract/test_{review_code_composition,code_review_skill_contract,coverage_receipt,status_gate_owner,review_feedback_boundary,review_docs_isomorphism}.py` 求和 | 31+39+20+32+30+9 = **161** |
| 表达式兼容（C-5 冻结哈希） | `grep -c 'def test_' tests/contract/test_expression_compatibility.py` | **16** |
| 071 P1 复审循环 | `grep -c 'def test_' tests/contract/test_review_p1_review_loop.py` | **10** |
| feedback/probe 契约族文件数 | `ls tests/contract/ \| grep -cE '^test_feedback_\|^test_probe_'` | **18** |

## 6. 冻结覆盖基线正文 delta

- `LC_ALL=C comm -13 <(grep -v '^#' .specify/specs/072-client-self-improvement/coverage-baseline.txt) <(python3 scripts/python/account-clause-coverage.py --freeze | grep -v '^#') | wc -l` → **0**（不重新冻结；冻结时机归 plan 阶段首次全树会计）。

## 7. E2 基线槽锚（T002，同一冻结窗口内）

- 命令: `bash scripts/bash/run-tests.sh --names-out .specify/specs/072-client-self-improvement/baseline-failed.txt`
- 结果: 6144 passed / **26 failed** / 1 skipped，rc=1（pytest 失败字母表）。
- 失败名单: `.specify/specs/072-client-self-improvement/baseline-failed.txt`（26 名）。
- 文档化预存失败 `tests/contract/test_clause_forms.py::test_the_four_md_forms_never_co_occur_in_one_file` 在列（plan.jsonl 既录）；其余 25 名为既有环境/基线失败，本特性判据 = 相对此名单**零新增**。
- 状态脊: `tmp/sdd-loop-072/state-spine.md` test-budget 块 seq=1 / slot=baseline（SPINE_WRITE_MODE=direct）。
