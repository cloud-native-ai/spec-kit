# Quickstart — 分片归档走查（100-seal-slice-archive）

**Feature**: 100-seal-slice-archive（bound Feature 099） | **Date**: 2026-11-11 | **Plan**: [plan.md](plan.md)
**读者基线**: 按 `.specify/shared/guidelines/user-facing-comprehension.md` § 基准读者与覆盖协议 的全局基准读者。本页首次出现处定义的术语：**分片归档（slice archive）**= 把已完成合并回写的分片目录整体移入父 spec 的 `slices/` 并留存清单；**归档清单**= 父 spec 根的 `archive-manifest.json`；**活引用**= 当前读者会照着导航的指针（必须直接指向存在路径）；**日期化记录**= 过去运行留下的测量与叙述（保持原字节，只经清单 `from → to` 映射解析）。

> **执行状态说明（按例生效，不是文件级免责）**：S-2…S-6 中的 `archive-plan` / `archive-apply` 命令在 plan 阶段**尚不可执行**——两个动作随实现阶段 P1–P4 落地。每个示例块下逐条列出它依赖的前提（premises）与将钉住它的契约测试；S-1 的检查命令已于 2026-11-11 实跑并粘贴真实输出。

---

## S-1 环境自检（已实跑，2026-11-11）

**S-1.1 flow-class 读取**

```bash
python3 .specify/scripts/python/flow-class-check.py --action lookup --unit-id "spec:100-seal-slice-archive"
```

实测输出（前六行）：

```text
unit_id: spec:100-seal-slice-archive
flow_class: execution
flow_type: -
source: declaration
marker: null
basis: null
```

**S-1.2 引擎当前调用面**

```bash
python3 scripts/python/seal-utils.py --help
```

实测输出（头部，verbatim）：

```text
usage: seal-utils.py [-h] --action {merge-plan,merge-apply,seal,archive-gate}
                     --spec-dir SPEC_DIR [--repo REPO]
                     [--feature-detail FEATURE_DETAIL]
                     [--feature-registry FEATURE_REGISTRY] [--json]
                     [--version]

Seal engine for /speckit.seal: merge-back, seal judgment and archive admission.
```

**Premises**: 本输出是**实现前**的读数；P1 落地后 `--action` 的 choices 变为 `{merge-plan,merge-apply,seal,archive-gate,archive-plan,archive-apply}`，帮助文本的动作描述追加归档动作。钉住方式：`tests/contract/test_seal_engine_contract.py` 的 C-001 断言（六动作 pin，P1 更新）。

**S-1.3 镜像与命令副本基线**

```bash
python3 scripts/python/sync-mirrors.py --check; echo "sync exit=$?"
python3 scripts/python/regen-command-copies.py --check; echo "regen exit=$?"
```

实测：`sync exit=2`，唯一漂移为 `.specify/templates/gitignore-specify-template`（既有、与本特性写面无关）；其余对全部 `ok`（`shared/` 113 文件、`scripts/` 129 文件、`skills/external` 429、`skills/internal` 136、`agents` 18）。`regen exit=0`，输出 `OK: all per-tool command copies match the source templates.`。因此本特性的判据是「触及的镜像对**零新增漂移**」，不是全局 exit 0。

**S-1.4 git 与钉住提交**

```bash
git rev-parse HEAD; git rev-parse --is-inside-work-tree
```

实测输出：

```text
9695d78c52fb5013ab092840e9eea3e56e55ec0b
true
```

---

## S-2 只读预览一次归档（`archive-plan`）

```bash
python3 scripts/python/seal-utils.py --action archive-plan \
  --spec-dir .specify/specs/074-goal-team-sdd-unification --repo . --json
```

预期形态：`verdict=ok`，具名结论 `would-archive`；负载包含分片集（2 片）、移动对、引用台账候选（`checks.live_rewrite` / `checks.dated_preserved` 计数）、`checks.unresolved_before=0`、`checks.unresolved_after=0`（plan 期按投影归档树复算）、`checks.unclassified=0` 与退出码 `0`。若任一前置不成立，`verdict=refused`（exit `1`）或 `error`（exit `2`），逐条点名**全部**未满足条件。

**Premises**: ① `archive-plan` 由 P3 实现并注册进 `ACTIONS`/`HANDLERS`；② `merge-manifest.json` 处于 `merge.status=merged`、零开放冲突（本日实测 R-07）；③ 074 的 2 个分片在源与目标中恰在一侧（当前都在源）；④ 引用分类按 `contracts/reference-classification.contract.md` 的封闭集判定。**Pinned by**: `tests/contract/test_seal_archive_plan.py::test_plan_reports_move_pairs_and_zero_unresolved`（P3）。

---

## S-3 执行归档（`archive-apply`）并在批次后提交

```bash
python3 scripts/python/seal-utils.py --action archive-apply \
  --spec-dir .specify/specs/074-goal-team-sdd-unification --repo . --json
git status --porcelain -- .specify/specs/074-goal-team-sdd-unification
git diff --name-status -M HEAD -- .specify/specs/074-goal-team-sdd-unification .specify/specs/074a-authorized-routing .specify/specs/074b-nested-governance
```

预期：exit `0`，具名结论 `archived`；两片位于 `.specify/specs/074-goal-team-sdd-unification/slices/<slug>/`；`git diff --name-status -M HEAD`（比较基 = apply 前提交；`git mv` 已暂存，索引写入不改变该读数）对每个被移动文件给出 `R` 重命名对、零 `D` 纯删除；父 spec 根出现 `archive-manifest.json`。随后按显式路径提交 archive 批次（父 spec 树、`register.md`、详情活区、`shared` 源/镜像、两个测试载体、归档清单），单行提交消息，`git add -A` 禁用。

**Premises**: ① `archive-apply` 由 P4 实现；② `archive-plan` 先行且无阻断；③ 工作树在父 spec 与分片范围内干净；④ 本仓库是 git 工作树（S-1.4）；⑤ 提及的两个测试载体路径存在（实测）。**Pinned by**: `tests/contract/test_seal_archive_apply.py::test_apply_is_a_pure_rename_batch` 与 `tests/integration/test_seal_archive_round.py::test_074_round_moves_both_slices`（P4/P7）。

---

## S-4 幂等重跑（`already-archived` 与零 diff）

```bash
python3 scripts/python/seal-utils.py --action archive-apply \
  --spec-dir .specify/specs/074-goal-team-sdd-unification --repo . --json
python3 scripts/python/seal-utils.py --action archive-plan \
  --spec-dir .specify/specs/074-goal-team-sdd-unification --repo . --json
git diff --stat -- .specify/specs/074-goal-team-sdd-unification
```

预期：apply exit `0` 且具名 `already-archived`；plan 报告同一 `already-archived` 结论、零待移动、零未解析；`git diff --stat` 零输出；不产生第二份清单。

**Premises**: ① S-3 已成功且其批次已提交；② 后到者读到先到者清单即收敛（无锁文件）；③ 归档后的分片发现走 `archive-manifest.json`（C-112）。**Pinned by**: `tests/integration/test_seal_archive_idempotency.py::test_second_apply_is_already_archived_with_zero_diff`（P4）。

---

## S-5 阻断态流程（封装阻断不阻断归档）

```bash
python3 scripts/python/seal-utils.py --action merge-apply \
  --spec-dir .specify/specs/<blocked-fixture> --repo . --json
python3 scripts/python/seal-utils.py --action archive-plan \
  --spec-dir .specify/specs/<blocked-fixture> --repo . --json
python3 scripts/python/seal-utils.py --action archive-apply \
  --spec-dir .specify/specs/<blocked-fixture> --repo . --json
python3 scripts/python/seal-utils.py --action seal \
  --spec-dir .specify/specs/<blocked-fixture> --repo . --json
```

预期：`merge-apply` 成功；`archive-plan`/`archive-apply` 正常执行；`seal` 仍给出与归档前相同的具名阻断清单（归档不改变封装结论）。`merge-apply` 被拒绝的夹具：`archive-plan` 不启动并点名上游阻断。

**Premises**: ① 夹具 `tests/fixtures/seal-archive/blocked-pair/` 由 P3 创建；② `merge-apply` 在夹具上的退出码由既有引擎产生（本特性不改合并语义）；③ `<blocked-fixture>` 为夹具 spec 目录占位符，不是本仓真实路径。**Pinned by**: `tests/integration/test_seal_archive_round.py::test_blocked_seal_still_archives` 与 `::test_merge_refusal_does_not_start_archive`（P7）。

---

## S-6 回滚走查（文档步骤 + 夹具）

版本化面（假设归档批次**尚未**提交；若已提交，用一条 `git revert <archive-commit>` 等效）：

```bash
# ① 逆移动（按清单 slices[] 的 order 顺序）
git mv .specify/specs/074-goal-team-sdd-unification/slices/074a-authorized-routing .specify/specs/074a-authorized-routing
git mv .specify/specs/074-goal-team-sdd-unification/slices/074b-nested-governance .specify/specs/074b-nested-governance
# ② 逐条 live-rewrite 载体 + merge-manifest.json 恢复归档前字节
git restore --source=<pinned_commit> --staged --worktree -- .specify/register.md .specify/features/074-goal-team-sdd-unification.md \
  .specify/specs/074-goal-team-sdd-unification/merge-manifest.json .specify/specs/074-goal-team-sdd-unification/tasks.md
# ③ 移除 apply 新建的归档清单（若已暂存，先从索引移除再删工作树文件）
git rm -f --cached .specify/specs/074-goal-team-sdd-unification/archive-manifest.json 2>/dev/null || true
rm .specify/specs/074-goal-team-sdd-unification/archive-manifest.json
# ④ 运行期面按清单 references.runtime[] 逐条把 after 逆写回 before
git status --porcelain -- .specify/specs/074-goal-team-sdd-unification .specify/register.md
git diff --exit-code <pinned_commit> -- .specify/specs/074-goal-team-sdd-unification .specify/specs/074a-authorized-routing .specify/specs/074b-nested-governance
```

完成判据：父 spec、分片与全部 live 载体相对 `pinned_commit` 的树零差异（路径集 = `<parent>` + 每个分片的 **`from`（源）路径**（逆移动后分片所在位置）+ `references.rows[].carrier` 去重后的 live 载体；`git diff --exit-code <pinned_commit> -- <该路径集>` 为空），且清单 `references.rows[]` 的 `before` / `after` 逐行核对成立；`git status` 相对回滚前无新增差异。

**Premises**: ① `pinned_commit` 取自归档清单（apply 前 HEAD）；② 步骤 ② 的路径清单来自清单的 `live-rewrite` 行，示例只列测量到的载体（`register.md`、详情活区、`merge-manifest.json`、父 `tasks.md`），其余载体（`plan.md`、`research.md`、`quickstart.md`、`verification.md`、`review.md`、`code-review.md`、`feature-ref.md`、`contracts/`、`shared` 源/镜像、两个测试载体）按同一形式逐条补入；③ 步骤 ④ 只适用于状态根可见的环境（本 worktree 全部 `absent`，该步为空操作）；④ 示例使用真实父 spec 路径，但**未执行**——夹具版本由 P7 的 rollback 测试执行并断言逐字节恢复。**Pinned by**: `tests/integration/test_seal_archive_rollback.py::test_rollback_restores_byte_identical_tree`（P7/P8）。

---

## 交付面速查

| 你会看到 | 位置 | 由谁写 |
|----------|------|--------|
| 归档清单 `archive-manifest.json` | 父 spec 根 | `archive-apply` |
| 分片归档位置 | `.specify/specs/<parent>/slices/<slug>/` | `archive-apply`（`git mv`） |
| 合并清单路径字段 | 父 spec 根 `merge-manifest.json` | `archive-apply`（只改路径值、重算摘要） |
| 计划/拒绝报告 | stdout（`--json` 单负载） | `archive-plan` / `archive-apply` |
| 回滚配方 | 本页 S-6 + `contracts/archive-actions.contract.md` C-110 | 文档面 |
