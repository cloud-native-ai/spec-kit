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

## 8. 预存缺陷修复记录（T003，2026-10-27，implement part 1b）

- **缺陷**: `scripts/python/probe-utils.py::load_probe_registry` 的非实体 catalog 可达性检查只按 `workspace_root / rel` 校验；真实客户端（`specify init` 布局）只有 `.specify/<rel>`，故任何客户帽项目里 `--action probe-inject`（armed-state 准备步，C-3 命名的动作）必然以 `non-entity catalog entry unreachable` 拒绝。框架仓自测不可见（catalog 路径在框架根都存在），正是 C-58 要抓的盲分支。
- **修复理由**: 引擎自身已有同 doctrine —— `_engine_script`（同文件）"framework-source face first, runtime face (.specify/) second — downstream projects only have the latter"。catalog 检查漏用了该 doctrine；Driver 裁决为纠正级唯一读法。修复 = 指针在 `workspace_root / rel` **或** `workspace_root / ".specify" / rel` 任一存在即可达，二者皆无仍报错。
- **负例**（新增确定性用例，全在 `tests/contract/test_probe_nonentity_catalog.py`）:
  1. 框架布局（`ROOT`）`errors=[]`（`test_catalog_reachable_in_framework_layout`）；
  2. 仅含 `.specify/scripts/...` + `.specify/shared/definitions/probe-definitions.md` 的临时客户端布局，catalog 指针经 `.specify/` 兜底可达、`errors=[]`（`test_catalog_reachable_via_specify_face_in_client_layout`）；
  3. 两个面都缺失时仍报 `non-entity catalog entry unreachable`（`test_catalog_unreachable_when_both_faces_missing`）。
- **影响面**: 仅 `load_probe_registry` 一处判断 + 其 `.specify/` 运行时镜像（`sync-mirrors.py --write` 再同步）；注册内容（`shared/definitions/probe-definitions.md`）未改；无新增动作/依赖/存储；`probes` JSON 输出面未动（DoD-4 探针注册面不被触碰）。
- **夹具侧纠正（in-passing，同属未提交的 T003 产物）**: `ClientProject.external_probe_count()` 与自检一处断言原先读 `external_objects` 键，而 `--action probes` 普通输出只有 `available/classes/objects`（该计数键只存在于 validate/inject 输出）——改为从 `objects` 列表按 `ext-` 前缀推导（C-9 机器可读输出原则不变）。修复引擎输出面属 plan 保护面之外的改动，未选。
- **验证**: 定向集 `pytest -q tests/contract/test_probe_nonentity_catalog.py tests/contract/test_probe_registry_umbrella.py tests/contract/test_probe_engine_action_sets.py tests/contract/test_feedback_probe_registry.py` → 45 passed；夹具自检 21/21 SELF-CHECK OK（含 arm/disarm 往返；派单预期的 13/13 基于夹具早期检查数，现行为 21 项全过）。
- 镜像: `sync-mirrors.py --check` 修复后全 ok（既录 loop-playbook.md DIFF 之外无新增）。
