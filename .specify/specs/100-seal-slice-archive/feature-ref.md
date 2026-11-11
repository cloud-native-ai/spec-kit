# Feature Reference — 100-seal-slice-archive

**Feature**: 100-seal-slice-archive（`/speckit.seal` 的分片归档步骤）——**bound Feature 099 Speckit Seal**
**Spec directory**: `.specify/specs/100-seal-slice-archive/`
**Binding**: `spec:100-seal-slice-archive` → Feature **099**（`/speckit.clarify` Mode A under shared/workflow/feature-integration.md § Feature Binding Rules）；`flow_class=execution`（注册声明，不是推断）
**Delivery surface**: 既有三件产物内的增量 `templates/commands/seal.md` + `skills/internal/seal-artifact/SKILL.md` + `scripts/python/seal-utils.py`；2 份既有 owner 页 + 6 条 099 契约条款原地修订；3 份新契约页；074 回合产物与测试。
**Authority**: `requirements.md`（28 FR / 10 SC / 5 STR / 5 条 Clarifications）是意图 owner；`contracts/` 是符合性 owner；`plan.md` 是设计 owner。本页只映射，不复述规则。

## Feature registration（本阶段）

- **不新建 Feature 行**：binding 指向 **099**；`100-seal-slice-archive` 是同一命令/引擎/技能的 follow-up 规格。
- `.specify/features.md` 099 行与 `.specify/features/099-speckit-seal.md` 的 Last Updated 刷新为 2026-11-11（plan 阶段），状态**保持 `Ready for Review`**——既不推进到 `Sealed`（归 `/speckit.seal`），也不回退。
- 无既有 Feature 被合并/废弃/改名；074 是本特性的**验收目标**，其注册行状态保持 `Ready for Review`。

## Delivery map — FR → contract clause

条款 id 在本特性 3 份契约间全局分段：`archive-actions` **C-101…C-116**（16） / `archive-manifest` **C-201…C-212**（12） / `reference-classification` **C-301…C-312**（12），全文件合计 **40** 条、全 `md-bold-closed`。编号不复用 099 的 C-001…C-045，避免跨 feature 引用歧义。

| FR | Clauses |
|----|---------|
| FR-001 | C-102, C-107 |
| FR-002 | C-113 |
| FR-003 | C-106 |
| FR-004 | C-203 |
| FR-005 | C-109, C-201, C-202, C-203, C-207, C-208, C-209, C-212 |
| FR-006 | C-102 |
| FR-007 | C-103, C-104 |
| FR-008 | C-101, C-115 |
| FR-009 | C-103, C-108 |
| FR-010 | C-105 |
| FR-011 | C-110 |
| FR-012 | C-109, C-204, C-301, C-302, C-305, C-306 |
| FR-013 | C-303, C-308, C-310, C-311 |
| FR-014 | C-210, C-304, C-306, C-308 |
| FR-015 | C-210, C-301, C-307, C-312 |
| FR-016 | C-204, C-206 |
| FR-017 | C-205, C-309 |
| FR-018 | C-211 |
| FR-019 | C-112 |
| FR-020 | C-113 |
| FR-021 | C-101, C-114 |
| FR-022 | C-107, C-114 |
| FR-023 | C-113 |
| FR-024 | C-116 |
| FR-025 | C-116 |
| FR-026 | C-116 |
| FR-027 | C-105, C-111 |
| FR-028 | C-106 |

**This table is generated, not authored** — it is the deterministic export of the contracts' own citation groups (last FR/SC parenthetical group per clause). Regenerate after any clause edit (run from the repo root; this exact snippet was executed at plan time, 2026-11-11):

```bash
python3 - <<'EOF'
import sys
from pathlib import Path
from collections import defaultdict
sys.path.insert(0, 'scripts/python')
import clause_extract as ce
files = sorted(Path('.specify/specs/100-seal-slice-archive/contracts').glob('*.md'))
by_fr = defaultdict(list)
for f in files:
    for cid, frs in ce.clause_citations(f).items():
        for fr in frs:
            by_fr[fr].append(cid)
num = lambda x: int(x.split('-')[1])
for fr in sorted(by_fr, key=num):
    print(fr, ', '.join(sorted(by_fr[fr], key=num)))
EOF
```

Output at plan time: 28 lines, `FR-001`…`FR-028`, zero missing (the enumeration above).

## Measurement map — SC → red-first module

| SC | 首红模块 | 变异取证 |
|----|----------|----------|
| SC-001 | `tests/integration/test_seal_archive_round.py` | 归档前后文件数/sha256/相对路径集合；`git diff --name-status -M` 零纯删除；清单可复核 |
| SC-002 | `tests/integration/test_seal_archive_idempotency.py` | 重跑 `already-archived` 零 diff；内容变异使哈希检查转红 |
| SC-003 | `tests/contract/test_seal_archive_plan.py` | 活/日期化/未分类三类夹具；注入悬空引用与移除映射转红 |
| SC-004 | `tests/integration/test_seal_archive_round.py`（阻断态） + `tests/contract/test_seal_engine_contract.py` | 阻断态照常归档、merge 拒绝不启动；`COMMAND_BASELINE` 对照 |
| SC-005 | `tests/contract/test_seal_boundaries.py` | 写面静态审计；注入删除/状态写入转红 |
| SC-006 | `tests/integration/test_seal_archive_idempotency.py` | 两次 plan sha256 一致；排序变异转红 |
| SC-007 | `tests/contract/test_seal_archive_manifest.py` | 三组闭环算术；删行变异转红 |
| SC-008 | `tests/contract/test_seal_archive_apply.py` | 运行期存在/缺席两类夹具；缺席转阻断变异转红 |
| SC-009 | `tests/contract/test_seal_boundaries.py` + 并发夹具 | 单一机制静态审计；双写路径互异；聚合变异转红 |
| SC-010 | `tests/integration/test_seal_archive_round.py`（rollback） | 回滚前后树哈希对照；跳过步骤转红 |

## Delivery surface（供 `/speckit.tasks` 与 overlap-check 消费）

声明本特性的共享根交付路径（仓库根相对）：

```text
scripts/python/seal-utils.py
skills/internal/seal-artifact/SKILL.md
templates/commands/seal.md
shared/definitions/non-disposable-definitions.md
shared/definitions/framework-map.md
shared/definitions/sdd-routing-definitions.md
docs/reference/commands/seal.md
tests/contract/test_seal_engine_contract.py
tests/contract/test_seal_boundaries.py
tests/contract/test_seal_merge_apply.py
tests/contract/test_seal_archive_plan.py
tests/contract/test_seal_archive_apply.py
tests/contract/test_seal_archive_manifest.py
tests/contract/test_sdd_compat_containment.py
tests/contract/test_sdd_diffusion.py
tests/integration/test_seal_archive_round.py
tests/integration/test_seal_archive_idempotency.py
tests/integration/test_seal_074_round.py
tests/fixtures/seal-archive/
```

特性内部产物（`.specify/specs/100-seal-slice-archive/**`、`.specify/specs/099-speckit-seal/contracts/*.md` 的修订、`.specify/specs/074-goal-team-sdd-unification/**` 的回合产物）不进入共享根交付面。

## Overlap adjudication（与 Feature 099 的同一交付面）

本特性与 099 在多数路径上重叠，是**绑定关系下的原地增量**，不是并行写同一路径：099 已交付这些 owner 与引擎，本特性在同一 owner 上增加两个动作、三份契约页与 074 回合。归属裁决：每个重叠路径的 owner 不变（099 的契约 / non-disposable owner / seal 三件套），本特性只做被 099 C-019 明确延后的「分片后续处置」增量。plan 阶段 `overlap-check.py` 读数与逐路径裁决记录在 `test-evidence/plan-stage-checks.txt`。
