# Quickstart 走查实录 — 分片归档（T048）

**执行日期**: 2026-11-11
**执行树**: worktree `100-seal-slice-archive`（分支 `100-seal-slice-archive` @ `f3bd72866`）
**执行方式**: 按 `quickstart.md` S-2…S-6 逐步实跑；每条命令、输出与退出码原样抄自本次运行的完整转录（转录文件：`.specify/.tmp/p8/quickstart-transcript.md`，位于 sanctioned 临时根）。JSON 负载在原文过长处保留投影（`action` / `verdict` / `outcome` / `exit_code` / `archive.checks` / `archive.manifest_digest` / 移动对），投影未改字段值；完整清单正文以 digest 钉住。

**回放树**: `tests/fixtures/seal-archive/clean-pair`、`blocked-pair` 复制到 `.specify/.tmp/p8/quickstart/` 下并 `git init` + 基线提交；真实 074 树直接读取（已归档态）。

---

## S-2 只读预览一次归档（`archive-plan`）

### S-2a 已归档的 074 真实树

```text
$ python3 scripts/python/seal-utils.py --action archive-plan \
    --spec-dir .specify/specs/074-goal-team-sdd-unification --repo . --json
EXIT=0
{
  "action": "archive-plan",
  "verdict": "ok",
  "outcome": "already-archived",
  "exit_code": 0,
  "archive.checks": {
    "live_rewrite": 249,
    "dated_preserved": 825,
    "unclassified": 0,
    "unresolved_before": 0,
    "unresolved_after": 0
  },
  "archive.moves": [],
  "archive.manifest_digest": "sha256:2e2b2f571947ccff2dc6ce379dd832c38d90b25c98a51615fc71ebab0f0406b6"
}
```

读解：074 树已由 P7 回合归档，plan 读回执并给出 `already-archived`、零待移动；计数与归档清单一致（249 / 825 / 0 / 0）。

### S-2b `clean-pair` 回放树（未归档态）

```text
$ python3 scripts/python/seal-utils.py --action archive-plan \
    --spec-dir <replay>/.specify/specs/100-fixture-parent --repo <replay> --json
EXIT=0
{
  "action": "archive-plan",
  "verdict": "ok",
  "outcome": "would-archive",
  "exit_code": 0,
  "archive.checks": {
    "live_rewrite": 2,
    "dated_preserved": 0,
    "unclassified": 0,
    "unresolved_before": 0,
    "unresolved_after": 0
  },
  "archive.moves": [
    {"slug": "100a-fixture-alpha", "from": ".specify/specs/100a-fixture-alpha",
     "to": ".specify/specs/100-fixture-parent/slices/100a-fixture-alpha", "file_count": 2},
    {"slug": "100b-fixture-beta", "from": ".specify/specs/100b-fixture-beta",
     "to": ".specify/specs/100-fixture-parent/slices/100b-fixture-beta", "file_count": 2}
  ],
  "archive.manifest_digest": "sha256:ea7824c704a8e34aaf46e085f574a5d396647009e57f1b6d43ab01c8bd849eae"
}
```

与 `quickstart.md` S-2 的预期形态一致：`would-archive`、两片移动对、未解析 0、未分类 0、退出码 0。

---

## S-3 执行归档（`archive-apply`）并在批次后提交

```text
$ python3 scripts/python/seal-utils.py --action archive-apply \
    --spec-dir <replay>/.specify/specs/100-fixture-parent --repo <replay> --json
EXIT=0
{
  "action": "archive-apply",
  "verdict": "ok",
  "outcome": "archived",
  "exit_code": 0,
  "archive.moves": [ 同 S-2b 的两条移动对 ]
}
```

提交前工作树（逐字）：

```text
$ git status --porcelain -- <parent> <切片 100a> <切片 100b>
 M .specify/specs/100-fixture-parent/merge-manifest.json
R  .specify/specs/100a-fixture-alpha/requirements.md -> .specify/specs/100-fixture-parent/slices/100a-fixture-alpha/requirements.md
R  .specify/specs/100a-fixture-alpha/tasks.md -> .specify/specs/100-fixture-parent/slices/100a-fixture-alpha/tasks.md
R  .specify/specs/100b-fixture-beta/requirements.md -> .specify/specs/100-fixture-parent/slices/100b-fixture-beta/requirements.md
R  .specify/specs/100b-fixture-beta/tasks.md -> .specify/specs/100-fixture-parent/slices/100b-fixture-beta/tasks.md
?? .specify/specs/100-fixture-parent/archive-manifest.json

$ git diff --name-status -M HEAD -- <parent> <切片 100a> <切片 100b>
M	.specify/specs/100-fixture-parent/merge-manifest.json
R100	.specify/specs/100a-fixture-alpha/requirements.md	.specify/specs/100-fixture-parent/slices/100a-fixture-alpha/requirements.md
R100	.specify/specs/100a-fixture-alpha/tasks.md	.specify/specs/100-fixture-parent/slices/100a-fixture-alpha/tasks.md
R100	.specify/specs/100b-fixture-beta/requirements.md	.specify/specs/100-fixture-parent/slices/100b-fixture-beta/requirements.md
R100	.specify/specs/100b-fixture-beta/tasks.md	.specify/specs/100-fixture-parent/slices/100b-fixture-beta/tasks.md
```

读解：每个被移动文件一条 `R100` 重命名对、零 `D` 纯删除；父 spec 根出现 `archive-manifest.json`；`merge-manifest.json` 只改路径形态值（M）。随后按显式路径提交 archive 批次（`git mv` 已暂存，`git add -A -- <parent>` 补清单与改写文件，`git add -A` 全仓禁用）：提交 exit 0。

---

## S-4 幂等重跑（`already-archived` 与零 diff）

```text
$ python3 scripts/python/seal-utils.py --action archive-apply ... --json
EXIT=0
{ "verdict": "ok", "outcome": "already-archived", "exit_code": 0, "archive.moves": [] }

$ python3 scripts/python/seal-utils.py --action archive-plan ... --json
EXIT=0
{ "verdict": "ok", "outcome": "already-archived", "exit_code": 0, "archive.moves": [] }

$ git diff --stat -- .specify/specs/100-fixture-parent
EXIT=0
（零输出）
```

读解：重跑 apply 与 plan 均读清单收敛为 `already-archived`、零待移动、零未解析；批次提交后重跑 `git diff --stat` 零输出，不产生第二份清单。

---

## S-5 阻断态流程（封装阻断不阻断归档）

```text
$ python3 scripts/python/seal-utils.py --action seal ... --json          # 归档前
EXIT=2   {"verdict": "error", "outcome": null}

$ python3 scripts/python/seal-utils.py --action merge-apply ... --json
EXIT=1   {"verdict": "refused", "outcome": null}

$ python3 scripts/python/seal-utils.py --action archive-plan ... --json
EXIT=0   {"verdict": "ok", "outcome": "would-archive"}

$ python3 scripts/python/seal-utils.py --action archive-apply ... --json
EXIT=0   {"verdict": "ok", "outcome": "archived"}

（提交 archive 批次：git add -A -- <parent> → commit，均 exit 0）

$ python3 scripts/python/seal-utils.py --action seal ... --json          # 归档后
EXIT=2   {"verdict": "error", "outcome": null}
```

阻断清单（归档前 / 归档后，按 `slices/` 载体前缀规范化后逐条相等，4 = 4）：

```text
['code-review-blocking', 'closure-input-defect', 'merge-incomplete', 'merge-incomplete']  (pre)
['code-review-blocking', 'closure-input-defect', 'merge-incomplete', 'merge-incomplete']  (post)
```

读解与偏差披露：

- `blocked-pair` 夹具是**合并已完成、封装具名阻断**的树，其 `merge-apply` 在已合并树上幂等拒绝（`refused`，exit 1）；归档触发读的是合并清单已记录的 settled 状态（`merge.status=merged`），因此 plan / apply 照常执行。上游 `merge-apply` 被拒绝时归档不启动的腿由 `tests/integration/test_seal_archive_round.py::test_merge_refusal_does_not_start_archive` 钉住（注入重复映射、无合并清单 → archive-plan exit 2 `merge-manifest-missing`），本次走查未再复制该夹具。
- 归档后 seal 的阻断清单与归档前一致（仅分片载体前缀从源路径变为 `slices/` 路径）；归档不改变封装结论。

---

## S-6 回滚走查（文档步骤 + 夹具）

在**独立的未提交回放树**（`clean-pair-rollback`）上执行：先 `archive-apply`（`archived`，批次未提交），再逐字执行 `quickstart.md` S-6 配方：

```text
# ① 逆移动（按清单 slices[] 的 order 顺序）
$ git mv -- <parent>/slices/100a-fixture-alpha .specify/specs/100a-fixture-alpha     EXIT=0
$ git mv -- <parent>/slices/100b-fixture-beta  .specify/specs/100b-fixture-beta      EXIT=0
# ② 逐条 live-rewrite 载体恢复归档前字节（本夹具 = merge-manifest.json；无 register/glossary 等）
$ git restore --source=<pinned_commit> --staged --worktree -- .specify/specs/100-fixture-parent/merge-manifest.json   EXIT=0
# ③ 移除 apply 新建的归档清单
$ rm <parent>/archive-manifest.json                                                  EXIT=0
# ④ 运行期面按 references.runtime[] 逆写（本回放树 0 条更新）
$ reverse 0 runtime update(s)
```

完成判据：

```text
$ git diff --exit-code <pinned_commit> -- <parent> <每片 from 源路径> <live 载体>
EXIT=0
$ git status --porcelain
EXIT=0（零输出）
```

读解：逆移动 + 原字节恢复 + 移除清单后，父 spec、两片源目录与全部 live 载体相对 `pinned_commit` 的树零差异，工作树干净。配方中的运行期步骤在本回放树为空操作（无更新行），与契约 C-309 的缺席非阻断一致。

---

## Teardown

- 三棵回放树与临时提交均在 `.specify/.tmp/p8/quickstart/`（`.gitignore` 覆盖的 sanctioned 临时根）；不进入版本库，由 house-keeping 回收。
- 真实 074 树只执行了只读 `archive-plan`（S-2a），未写入。
- 本走查未修改仓库内任何被跟踪文件。
