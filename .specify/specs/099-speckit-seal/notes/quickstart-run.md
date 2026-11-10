# Quickstart 走查实录 — `/speckit.seal`（T047，GATE-4 smoke 证据）

**执行日期**: 2026-11-11（UTC 2026-11-10T17:5x）
**执行树**: worktree `099-speckit-seal`（分支 `099-speckit-seal`）
**执行方式**: 按 `quickstart.md` S-1…S-9 逐步实跑；每条命令、输出与退出码原样抄自本次运行的完整转录
（scratch：`.specify/.tmp/quickstart-transcript.txt`，gitignore 覆盖；本文件是归档面）。
**smoke 命令（GATE-4 三键之一）**:

```bash
bash scripts/bash/run-tests.sh tests/integration/test_seal_074_round.py -q
```

本次实测：`5 passed in 6.31s`，`exit=0`——该模块钉住 074 round 的 merge-plan → merge-apply → seal
全链路的形状与阻断态重跑一致性，是本特性主流程的端到端执行面。
`smoke_exit_code=0`、`smoke_evidence_path=.specify/specs/099-speckit-seal/notes/quickstart-run.md`。

---

## S-1 环境自检

### S-1.1 镜像与命令副本零漂移

```bash
python3 scripts/python/sync-mirrors.py --check; echo "sync exit=$?"
python3 scripts/python/regen-command-copies.py --check; echo "regen exit=$?"
```

实测（尾部）：

```text
ok    templates/ == .specify/templates/ (23 files, byte-identical)
ok    skills/external/ == .specify/skills/ (428 files, byte-identical)
ok    skills/internal/ == .specify/skills/internal/ (136 files, byte-identical)
ok    agents/ == .specify/agents/templates/ (17 files, byte-identical)
ok    scripts/ == .specify/scripts/ (127 files, byte-identical)
ok    shared/ == .specify/shared/ (111 files, byte-identical)
sync exit=0
OK: all per-tool command copies match the source templates.
regen exit=0
```

### S-1.2 测试入口可用

```bash
bash scripts/bash/run-tests.sh tests/contract/test_status_gate_owner.py -q
```

实测：`32 passed in 6.26s`，`exit=0`（并行模式 `workers=auto dist=load`）。

### S-1.3 074 闭包裁决（输入缺陷，实测 exit 2）

```bash
python3 scripts/python/closure-acceptance-check.py --spec-dir .specify/specs/074-goal-team-sdd-unification --json; echo "exit=$?"
```

实测：`exit=2`，stderr 逐字：

```text
closure-acceptance-check: input error: .../074-goal-team-sdd-unification/requirements.md carries no § Runtime Stack & Dependency Ownership
```

这是回合的 B2 具名阻断（074 早于 runtime-stack 门禁，闭包判定器 exit 2），**不读作通过**；
与 plan 阶段 S-1.3 的「SC 行缺 `**Path**` 标记」不同的原因是：回合已按 C-018 给父 requirements 的
8 条 SC 行补上 `**Path**: final`，Path 输入缺陷已 resolved，B2 保持阻断。

---

## S-2 只读预览一次合并（`merge-plan`，074 树）

```bash
python3 scripts/python/seal-utils.py --action merge-plan --spec-dir .specify/specs/074-goal-team-sdd-unification --json; echo "exit=$?"
```

实测：`exit=0`（`verdict=ok`，`conditions=[]`）。载荷要点：`plan.slices` = `074a-authorized-routing`（order 1）
→ `074b-nested-governance`（order 2）；`plan.conflicts` = 0；`plan.factory_doc_refs`、`plan.id_maps`、
`plan.checks` 齐备（重跑形态：回合已把冲突处置完毕，故本行为 0 冲突；冲突检出能力由 S-5 的
`conflict-open` 夹具与 P3 契约测试钉住）。只读：命令前后 `git status --porcelain` 对 074 三树为空。

---

## S-3 夹具树上的合并与确定性（`merge-apply`，重跑形态）

```bash
mkdir -p .specify/.tmp
rm -rf .specify/.tmp/quickstart-seal
cp -r tests/fixtures/seal/split-pair .specify/.tmp/quickstart-seal
python3 scripts/python/seal-utils.py --action merge-apply --repo .specify/.tmp/quickstart-seal \
  --spec-dir .specify/.tmp/quickstart-seal/.specify/specs/099-fixture-parent --json
find .specify/.tmp/quickstart-seal -type f \( -name '*.md' -o -name '*.json' \) | sort | xargs sha256sum > .specify/.tmp/run1.sha
python3 scripts/python/seal-utils.py --action merge-apply --repo .specify/.tmp/quickstart-seal \
  --spec-dir .specify/.tmp/quickstart-seal/.specify/specs/099-fixture-parent --json
find .specify/.tmp/quickstart-seal -type f \( -name '*.md' -o -name '*.json' \) | sort | xargs sha256sum > .specify/.tmp/run2.sha
diff .specify/.tmp/run1.sha .specify/.tmp/run2.sha; echo "exit=$?"
```

实测：

- 第一次：`exit=0`，`idempotent=false`，`writes` 16 条（父级 14 项输出件 + `merge-manifest.json` + 两片
  `requirements.md` 的分片标注行）；`checks`: `id_continuity=pass`、`open_rows=0`、`duplicate_ids=0`、
  `dangling_refs=0`、`dated_record_hashes_stable=true`。切片按声明顺序 `099a-fixture-alpha` → `099b-fixture-beta`。
- 第二次：`exit=0`，`idempotent=true`，`writes=[]`。
- `diff run1.sha run2.sha`：**无输出**，`exit=0`——两次运行逐字节一致（重跑幂等）。

---

## S-4 封装一条干净的单体 spec（成功路径）

夹具复制到 sanctioned 临时根后执行（`seal` 的 `dirty-spec-tree` 前置要求 git 仓库，复制树内 `git init` + 提交）：

```bash
cp -r tests/fixtures/seal/single-spec .specify/.tmp/quickstart-seal-clean
# git init/add/commit（user.name=qs, user.email=qs@example.com）
python3 scripts/python/seal-utils.py --action seal --repo .specify/.tmp/quickstart-seal-clean \
  --spec-dir .specify/.tmp/quickstart-seal-clean/.specify/specs/099-fixture-clean --json; echo "exit=$?"
```

实测：`exit=0`，`verdict=ok`，`seal.outcome=sealed`，`seal.writes` 3 条（注册表行、详情、`seal.md`）；
`seal.md` 落盘（1729 B）。状态对同批变为 `Sealed`（契约测试同判据）。
重跑同一命令：`exit=0`，`seal.outcome=already-sealed`，`writes=[]`，`seal.md` 不再变化。

---

## S-5 八类拒绝各点一次名（失败路径）

每个夹具只注入一种缺陷；均以 `shutil` 等价复制到 `.specify/.tmp/quickstart-seal-refusals/<case>/repo`，
`git init` + 提交后执行（`dirty-spec-tree` 在提交后追加一条未提交编辑）：

```bash
python3 scripts/python/seal-utils.py --action seal --repo <case>/repo \
  --spec-dir <case>/repo/.specify/specs/<slug> --json; echo "exit=$?"
```

| 夹具 | 目标 slug | exit | 具名码 | `seal.md` |
|------|-----------|------|--------|-----------|
| `from-status-invalid` | `099-fixture-clean` | 1 | `from-status-invalid` | 未生成（状态不变） |
| `p0-unresolved` | `099-fixture-clean` | 1 | `p0-unresolved` | 未生成 |
| `closure-refused` | `099-fixture-clean` | 1 | `closure-refused` | 未生成 |
| `closure-input-defect` | `099-fixture-clean` | 2 | `closure-input-defect` | 未生成 |
| `conflict-open` | `099-fixture-merged` | 1 | `conflict-open` | 未生成 |
| `slice-unclosed` | `099-fixture-clean` | 1 | `merge-incomplete` + `slice-unclosed` | 未生成 |
| `three-minus-one`（三缺一） | `099-fixture-clean` | 1 | `closure-refused` | 未生成 |
| `state-drift` | `099-fixture-clean` | 2 | `state-drift` | 未生成 |
| `dirty-spec-tree` | `099-fixture-clean` | 1 | `dirty-spec-tree` | 未生成 |

全部拒绝均为 `seal.outcome=refused|error`、`writes=0`、状态面字节不变——拒绝零持久化。

---

## S-6 归档准入查询（`archive-gate`）

```bash
python3 scripts/python/seal-utils.py --action archive-gate --spec-dir <target> --json; echo "exit=$?"
```

三个读数：

1. **`Sealed` 目标**（S-4 封装后的复制树）：`exit=0`，`gate={allowed:true, reason:"sealed", status:"Sealed",
   pointer:"seal.md"}`。
2. **非 `Sealed` 目标**（074，`Ready for Review`）：`exit=1`，`gate={allowed:false, reason:"not-sealed",
   pointer:"/speckit.seal"}`，`conditions` 点名 `not-sealed` 且修复指针指向 `/speckit.seal`。
3. **遗留 `Completed` 且无用户裁定**（复制树改状态后提交）：`exit=1`，
   `gate={allowed:false, reason:"legacy-completed-unruled", pointer:"/speckit.seal"}`。

---

## S-7 074 真实回合 — 重跑形态（split → merge-back → seal）

回合本体已在 P8 执行并留证（`test-evidence/074-round-20261110.txt`；P8b 修复引擎后的重跑记录
`test-evidence/074-round-rerun-20261111.txt`）。本次走查按 S-7 的**重跑形态**复验终态与确定性：

```bash
python3 scripts/python/seal-utils.py --action merge-plan --spec-dir .specify/specs/074-goal-team-sdd-unification --json
python3 scripts/python/seal-utils.py --action merge-apply --spec-dir .specify/specs/074-goal-team-sdd-unification --json
git status --porcelain -- .specify/specs/074-goal-team-sdd-unification .specify/specs/074a-authorized-routing .specify/specs/074b-nested-governance
python3 scripts/python/seal-utils.py --action seal --spec-dir .specify/specs/074-goal-team-sdd-unification --json   # ×2
```

实测：

- `merge-plan`：`exit=0`，`conflicts=0`。
- `merge-apply`：`exit=0`，`idempotent=true`，`writes=0`；`git status --porcelain` 对三树**空输出**（重跑零写）。
- `seal` ×2：均 `exit=2`，`verdict=error`，`seal.outcome=error`，`writes=0`，唯一引擎条件
  `closure-input-defect`（B2）。两次 stdout 载荷 `diff` 无输出（`exit=0`）——阻断态重跑逐字节一致（S-8）。
- 回合终态：**blocked（exit 2）**，具名阻断 = FR-027(d)（074b P0 F1 仅驱动者豁免）+ B2（runtime-stack
  输入缺陷）；FR-027(a)/(b)/(c)/(e) resolved、B1/B3/B4 resolved。与 P8b 裁定记录一致，非 `Sealed`。

---

## S-8 阻断态的确定性重跑

见 S-7 的 `diff <(seal run 1) <(seal run 2)`：无输出、`exit=0`。引擎不把时间戳写入 stdout 拒绝清单；
`merge-apply` 已完成且无变化的步骤零 diff（`writes=0` / `idempotent=true`）。

---

## S-9 清理

```bash
rm -rf .specify/.tmp/quickstart-seal .specify/.tmp/quickstart-seal-clean \
       .specify/.tmp/quickstart-seal-refusals .specify/.tmp/quickstart-seal-legacy
rm -f .specify/.tmp/run1.sha .specify/.tmp/run2.sha
ls -d .specify/.tmp/quickstart-seal*
```

实测：`ls` 对四个路径均报 `No such file or directory`（`exit=2`）——临时复制树已清除。
074 回合的正式产物（`seal.md` 不产生于阻断态；`merge-manifest.json`、分片标注）是验收证据，未清理。

---

## 附：与 quickstart.md 的一处执行差异（披露）

S-7 的原始命令把 `seal` 输出重定向到 `test-evidence/074-round-$(date -u +%Y%m%d).txt`。本次走查是
**重跑形态**，回合记录已由 `074-round-20261110.txt`（P8）与 `074-round-rerun-20261111.txt`（P8b）承载，
故本次输出落在 `.specify/.tmp/`（scratch）并把读数抄入本节，避免制造第三份同义回合记录。
其余步骤（含 S-3/S-4/S-5/S-6 的夹具复制）与 quickstart 逐条一致。
