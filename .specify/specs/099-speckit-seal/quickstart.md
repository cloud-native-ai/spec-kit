# Quickstart — `/speckit.seal` 走查（099-speckit-seal）

**Feature**: 099 Speckit Seal | **Date**: 2026-11-10 | **Plan**: [plan.md](plan.md)
**读者基线**: 按 `.specify/shared/guidelines/user-facing-comprehension.md` § 基准读者与覆盖协议 的全局基准读者；
本页首次出现处定义的术语：**封装（seal）**= 把一条 review 完成的 spec 固定为终态 `Sealed` 并留下回执；
**合并回写（merge-back）**= 把分片交付的同名输出件按声明顺序并回父级 spec；**合并清单**= 记录每次合并
归属与冲突的 `merge-manifest.json`。

> **执行状态说明（按例生效，不是文件级免责）**：S-2…S-8 中的引擎命令在 plan 阶段**尚不可执行**——引擎随
> 实现阶段的工作包 P2–P6 落地。每个示例块下方逐条列出它依赖的前提（premises）与将钉住它的契约测试；
> S-1 的检查命令已于 2026-11-10 实跑并粘贴真实输出。

---

## S-1 环境自检（已实跑，2026-11-10）

**S-1.1 镜像与命令副本零漂移**

```bash
python3 scripts/python/sync-mirrors.py --check; echo "sync exit=$?"
python3 scripts/python/regen-command-copies.py --check; echo "regen exit=$?"
```

实测输出（尾部）：`ok shared/ == .specify/shared/ (111 files, byte-identical)`、`sync exit=0`；
`OK: all per-tool command copies match the source templates.`、`regen exit=0`。

**S-1.2 测试入口可用**

```bash
bash scripts/bash/run-tests.sh tests/contract/test_status_gate_owner.py -q
```

实测输出：`32 passed in 6.17s`（并行模式，`mode=parallel workers=auto dist=load`）。

**S-1.3 074 当前闭包裁决（输入缺陷，实测 exit 2）**

```bash
python3 scripts/python/closure-acceptance-check.py --spec-dir .specify/specs/074-goal-team-sdd-unification --json; echo "exit=$?"
```

实测：`exit=2`，stderr 逐字为：

```text
closure-acceptance-check: input error: .../074-goal-team-sdd-unification/requirements.md:392 SC-001 carries 0 `**Path**` markers; exactly one is required (AS-01)
```
按 FR-007 / C-042，seal 会把这一形态报为 `closure-input-defect` 阻断，**不读作通过**。

---

## S-2 只读预览一次合并（`merge-plan`）

**前提**：引擎已落地（P3）。在 074 树上运行（只读，不改任何文件）：

```bash
python3 scripts/python/seal-utils.py --action merge-plan \
  --spec-dir .specify/specs/074-goal-team-sdd-unification --json
```

预期形态：退出 `1`（存在开放冲突）或 `0`（无冲突）；JSON 负载含分片集合（`074a-authorized-routing`、
`074b-nested-governance`，`order_basis: split-record`）、15 项输出件的动作分类、ID 映射表与冲突清单。
074 的已知合并冲突至少包含：STR 同号不同义（074b 本地 004/005/006）与出厂文档
`create-team/SKILL.md` 的分片本地 ID 引用。（"SC 行缺 `**Path**` 标记"不是合并冲突——它是闭包输入缺陷，
在 `seal` 阶段报 `closure-input-defect`；回合的处置是补标记后重跑，见 S-7。）

> **不可执行于 plan 阶段。** Premises：(a) `seal-utils.py` 存在且动作 `merge-plan` 已实现（P3）；
> (b) 引擎按 C-011 的封闭二形识别分片（074a/074b 的 `## Parent Mapping` 章节存在——本日实测存在）；
> (c) 拆分记录位于 `.specify/state/074-goal-team-sdd-unification.md` § 拆分记录（本日实测存在）。
> 将被 `tests/contract/test_seal_merge_plan.py` 钉住；074 只读片段由
> `tests/integration/test_seal_074_round.py` 钉住。

---

## S-3 在夹具树上执行合并并验证确定性（`merge-apply`）

**前提**：引擎已落地（P4）；夹具树 `tests/fixtures/seal/split-pair/`（两分片，各带 `## Parent Mapping`）。

```bash
mkdir -p .specify/.tmp
rm -rf .specify/.tmp/quickstart-seal
cp -r tests/fixtures/seal/split-pair .specify/.tmp/quickstart-seal
# 全部命令从仓库根执行：--repo 指向夹具根，--spec-dir 写仓库根相对路径
python3 scripts/python/seal-utils.py --action merge-apply --repo .specify/.tmp/quickstart-seal \
  --spec-dir .specify/.tmp/quickstart-seal/.specify/specs/099-fixture-parent --json
find .specify/.tmp/quickstart-seal -type f \( -name '*.md' -o -name '*.json' \) | sort | xargs sha256sum > .specify/.tmp/run1.sha
python3 scripts/python/seal-utils.py --action merge-apply --repo .specify/.tmp/quickstart-seal \
  --spec-dir .specify/.tmp/quickstart-seal/.specify/specs/099-fixture-parent --json
find .specify/.tmp/quickstart-seal -type f \( -name '*.md' -o -name '*.json' \) | sort | xargs sha256sum > .specify/.tmp/run2.sha
diff .specify/.tmp/run1.sha .specify/.tmp/run2.sha   # 期望：无输出（两次运行逐字节一致；重跑幂等）
```

（`merge-apply` 不要求 git 仓库；`dirty-spec-tree` 是 `seal` 的前置条件，在 S-7 的提交步骤里满足。）

> **不可执行于 plan 阶段。** Premises：(a) 引擎已落地（P4）；(b) 夹具树随 P3 落地且自带
> `## Parent Mapping`；(c) 引擎写面限于父 spec 目录 + 分片标注（C-023）。
> 将被 `tests/contract/test_seal_merge_apply.py` 与 `tests/integration/test_seal_merge_determinism.py` 钉住。
> **清理**：在仓库根执行 `rm -rf .specify/.tmp/quickstart-seal .specify/.tmp/run1.sha .specify/.tmp/run2.sha`
> （sanctioned 临时根，`.specify/.gitignore` 的 `.tmp/` 覆盖）。

---

## S-4 封装一条干净的单体 spec（`seal` 成功路径）

**前提**：一条 `Ready for Review` 的夹具 spec，review 干净、`code-review.md` 零 `blocking`、
父 `verification.md` 每条 SC 有 `SC-NNN_status=pass` 行、每条 SC 带行尾 `**Path**: final|supporting`。

```bash
python3 scripts/python/seal-utils.py --action seal --spec-dir .specify/specs/099-fixture-clean --json; echo "exit=$?"
```

期望：`exit=0`、`seal.md` 出现在父 spec 目录、注册表行与特性详情状态同批变为 `Sealed`；再次运行
返回 `exit=0` 且输出 `already-sealed`，`seal.md` 与状态面不再变化。

> **不可执行于 plan 阶段。** Premises：(a) `Sealed` 已进入全部 carrier 与消费面（P1）；
> (b) 闭包引擎对该夹具 exit 0（夹具自带的 `Path` 标记与状态行）；(c) 状态写入集恰为
> 注册表 + 详情 + `seal.md`（C-005）。将被 `tests/contract/test_seal_seal.py` 钉住。

---

## S-5 八类拒绝各点一次名（`seal` 失败路径）

逐个夹具运行（每个夹具只注入一种缺陷）：from 状态错误、P0 未处置（含只有驱动者豁免）、
验收状态行缺失、闭包引擎 exit 2、分片存在未决冲突、分片未闭合、脏 spec 树、状态面漂移。

```bash
python3 scripts/python/seal-utils.py --action seal --spec-dir <fixture> --json; echo "exit=$?"
```

期望：前七类 `exit=1`、状态不变、报告逐条点名全部未满足条件与修复路径；状态面漂移一类 `exit=2`
（`state-drift`）。「三缺一」夹具（三个条件满足一个不满足）MUST 拒绝。

> **不可执行于 plan 阶段。** Premises：夹具随 P5 落地；拒绝码封闭集按 C-042；拒绝零持久化（C-006）。
> 将被 `tests/contract/test_seal_seal.py` 的八类夹具钉住。

---

## S-6 归档准入查询（`archive-gate`）

```bash
python3 scripts/python/seal-utils.py --action archive-gate --spec-dir .specify/specs/<target> --json; echo "exit=$?"
```

期望：`Sealed` → `exit=0`；非 `Sealed` → `exit=1` 且 `pointer` 指向 `/speckit.seal`；遗留 `Completed`
且无用户裁定 → `exit=1`，理由具名；输入错误 → `exit=2`。

> **不可执行于 plan 阶段。** Premises：(a) 引擎已落地（P6）；(b) 准入判据只在 seal 引擎实现（C-030）；
> (c) `/speckit.sanitize` 归档 lane、docs lane 与 manage-features 归档指针在动手前调用本查询。将被 `tests/contract/test_seal_archive_gate.py` 钉住。

---

## S-7 074 真实回合（split → merge-back → seal）

按 FR-026/SC-006 的顺序执行：`merge-plan`（S-2）→ 逐条处置冲突 → 提交 → `merge-apply` → 提交 →
`seal`，被阻断时捕获 stdout 拒绝清单。

```bash
mkdir -p .specify/.tmp
python3 scripts/python/seal-utils.py --action merge-plan --spec-dir .specify/specs/074-goal-team-sdd-unification --json > .specify/.tmp/074-plan.json; echo "exit=$?"
# 处置 = 编辑输入 → 重跑 merge-plan 至该冲突不再复现（C-018 的 recheck-clean；canonical-map 由 074b 映射表自带）：
#   - 出厂文档 skills/internal/create-team/SKILL.md:99,101 → 逐字字面量或重指向 [[STR-007]]/[[STR-008]]/[[STR-009]]
#   - 父 requirements.md 的每条 SC 行尾补 **Path**: final（严格默认，逐条记录，MUST NOT 读作 exit 2 通过）
#   - 074b P0（F1）：需修复证据，或按 C-044 在 review.md code 小节与特征详情 Latest Review **两处**各记录
#     一条 `- **User waiver**:` 字面行（仅一处不计数），否则保持开放
#   - 57 行拆前记录：由 merge-apply 按 supersede 处置（不需手改）
python3 scripts/python/seal-utils.py --action merge-plan --spec-dir .specify/specs/074-goal-team-sdd-unification --json; echo "exit=$?"   # 期望 exit=0（0 open conflicts）
python3 scripts/python/seal-utils.py --action merge-apply --spec-dir .specify/specs/074-goal-team-sdd-unification --json; echo "exit=$?"
git add .specify/specs/074-goal-team-sdd-unification .specify/specs/074a-authorized-routing .specify/specs/074b-nested-governance skills/internal/create-team/SKILL.md
git commit -m "chore(074): merge back slices"
python3 scripts/python/seal-utils.py --action seal --spec-dir .specify/specs/074-goal-team-sdd-unification --json > .specify/specs/099-speckit-seal/test-evidence/074-round-$(date -u +%Y%m%d).txt 2>&1; echo "exit=$?"
```

期望终态（二值）：`Sealed`（`exit=0`），或与 FR-027 五项实测输入一一对应的具名阻断清单（`exit=1` 或
`state-drift` 的 `exit=2`）；阻断态重跑 MUST 清单一致。

> **不可执行于 plan 阶段。** Premises：(a) 五项输入缺陷的实测形态按 research R-9/R-10/R-12/R-17（本日实测）；
> (b) 074b 的 P0 豁免只有驱动者记录，除非回合内出现修复证据或用户以 `- **User waiver**:` 字面裁定（C-044）；
> (c) 合并产物提交后再跑 `seal`（C-039）。将被 `tests/integration/test_seal_074_round.py` 与回合记录
> `test-evidence/074-round-*.txt` 钉住。**清理**：回合产物是验收证据，不清理；临时 JSON 在
> `.specify/.tmp/`（已 gitignore）。

---

## S-8 阻断态的确定性重跑

在任一阻断夹具上连跑两次 `seal`，比较两次 stdout 拒绝清单（码、顺序、证据指针）：
期望逐字节一致（引擎不把时间戳写进 stdout 拒绝清单，见 `data-model.md` E12）；`merge-apply` 已完成且无变化的步骤零 diff。

> **不可执行于 plan 阶段。** Premises：拒绝清单顺序稳定（C-006/C-038）；引擎不读取返回时刻作排序键。
> 将被 `tests/integration/test_seal_074_round.py`（阻断态重跑）与 `test_seal_merge_determinism.py` 钉住。

---

## S-9 清理

S-3 与 S-7 的临时内容都在 `.specify/.tmp/`（gitignore 覆盖）；夹具复制树用
`rm -rf .specify/.tmp/quickstart-seal` 清除。074 回合的正式产物（`seal.md`、`merge-manifest.json`、
分片标注）是验收证据，MUST NOT 清理。
