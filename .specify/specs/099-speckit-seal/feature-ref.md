# Feature Reference — 099-speckit-seal

**Feature**: 099 Speckit Seal（`/speckit.seal`：按 review 封装 spec 与分片合并回写）
**Spec directory**: `.specify/specs/099-speckit-seal/`
**Binding**: `spec:099-speckit-seal`; `flow_class=execution`（注册声明，不是推断）
**Delivery surface**: 常量面 `templates/commands/seal.md` + internal 技能 `skills/internal/seal-artifact/` +
引擎 `scripts/python/seal-utils.py`；状态面 6 处 carrier；既有引擎 2 处消费面；074 回合产物。
**Authority**: `requirements.md`（28 FR / 9 SC / 3 STR / Clarifications / Assumptions）是意图 owner；
`contracts/` 是符合性 owner；`plan.md` 是设计 owner。本页只映射，不复述规则。

## Feature registration（本阶段）

- `.specify/features.md` 新增一行 **099**（插在 094 与 093 之间；Status `Planned`），特性计数 89 → 90；
  Last Updated `2026-11-10`。
- `.specify/features/099-speckit-seal.md` 新建（Overview / Key Changes / Plan Notes / Related Files，
  近邻文体见 plan § Disclosed Rulings 2）。
- 无既有 Feature 被合并/废弃/改名；074 不是被合并对象（它是本特性的**验收目标**，其注册行保持
  `Ready for Review` 直到回合给出二值终态）。

## Delivery map — FR → contract clause

条款 id 在 4 份契约间**全局连续**（C-001…C-045），文件归属：
`seal-engine` C-001…C-010 / `merge-back` C-011…C-023 / `status-sealed` C-024…C-031 /
`records-and-boundaries` C-032…C-045。

| FR | Clauses | FR | Clauses |
|----|---------|----|---------|
| FR-001 | C-024, C-025, C-029 | FR-015 | C-016 |
| FR-002 | C-026, C-033 | FR-016 | C-017 |
| FR-003 | C-027 | FR-017 | C-018 |
| FR-004 | C-028 | FR-018 | C-019, C-022, C-034 |
| FR-005 | C-007, C-031, C-042 | FR-019 | C-020, C-021, C-040 |
| FR-006 | C-040, C-042, C-044 | FR-020 | C-008, C-023, C-037 |
| FR-007 | C-042 | FR-021 | C-001, C-002, C-003, C-004, C-009, C-010, C-041 |
| FR-008 | C-042 | FR-022 | C-030, C-035 |
| FR-009 | C-002, C-005, C-006, C-038, C-042 | FR-023 | C-030 |
| FR-010 | C-005, C-007, C-032, C-033, C-039 | FR-024 | C-008, C-036 |
| FR-011 | C-011, C-012 | FR-025 | C-045 |
| FR-012 | C-013, C-021 | FR-026 | C-043 |
| FR-013 | C-014 | FR-027 | C-042, C-043, C-044 |
| FR-014 | C-015 | FR-028 | C-038, C-043 |

**This table is generated, not authored** — it is the deterministic export of the contracts' own citation
groups. Regenerate after any clause edit (run from the repo root; this exact snippet was executed at plan
time, 2026-11-10):

```bash
python3 - <<'EOF'
import sys, glob
sys.path.insert(0, 'scripts/python')
import clause_extract as ce
fr = {}
for f in sorted(glob.glob('.specify/specs/099-speckit-seal/contracts/*.md')):
    for cid, frs in ce.clause_citations(f).items():
        for x in frs:
            fr.setdefault(x, []).append(cid)
for x in sorted(fr):
    print(x, '->', ', '.join(sorted(set(fr[x]))))
EOF
```

Count: 28 FR / 28 present — 每条需求至少到达一条条款，无孤儿 FR。

## Measurement map — SC → red-first module

| SC | Path | 首红模块 |
|----|------|----------|
| SC-001 | final | `tests/contract/test_seal_seal.py` + `tests/contract/test_sealed_status_domain.py` |
| SC-002 | final | `tests/contract/test_seal_seal.py`（八类拒绝 + 三缺一变异） |
| SC-003 | final | `tests/integration/test_seal_merge_determinism.py` |
| SC-004 | final | `tests/contract/test_seal_merge_apply.py` |
| SC-005 | final | `tests/contract/test_seal_merge_plan.py` |
| SC-006 | final | `tests/integration/test_seal_074_round.py` + `test-evidence/074-round-*.txt` |
| SC-007 | supporting | `tests/contract/test_seal_archive_gate.py` |
| SC-008 | supporting | `tests/contract/test_seal_boundaries.py` + `tests/contract/test_sealed_status_domain.py` |
| SC-009 | supporting | `tests/contract/test_seal_concurrency_and_readonly.py` |

Tests Mode ON；取证形态按 `contracts/records-and-boundaries` C-045。

## Overlap adjudication（与相邻特性的文件级边界）

| 相邻面 | 关系 | 边界证据 |
|--------|------|----------|
| 074-goal-team-sdd-unification | **验收目标**，不是依赖 | 回合写面 = 父目录产物 + 两片 `requirements.md` 一行标注 + 经记录的出厂文档引用修正（C-023/C-017）；074 的注册状态在回合前不动（C-043） |
| 090/092 Non-Disposable | 复用其处置词汇与协议 | 57 行采用 `supersede`（C-022）；不新增处置写入器或台账（R-15） |
| `/speckit.review`（012/094 线） | review 记录的 owner | seal 只读（C-040），生成父级汇总视图属合并输出件的 `create/merge`（C-013） |
| `/speckit.sanitize` sanitize-materials | 归档 lane 的 owner | lane 在动 archive 前调用 `archive-gate`（C-030），不复制判定 |
| `/speckit.feature` manage-features | 注册表 reconcile 的 owner | seal 只写它拥有的那一条转移与记录（C-028/C-035） |
| `/speckit.goal` migrate-archive | goal/team 树迁移的 owner | seal 不迁移不删除（C-035） |
| 093 Concurrency by Default | 执行形态的 owner 事实 | 本 plan 的并发读数按 `shared/declarations/facts/effective-concurrency.yaml` 记录；不新增并发机制 |

无文件级重叠：本特性新增的测试模块名与既有模块不冲突；`tests/fixtures/seal/` 为新主题目录。

## Disclosed rulings

1. **条款编号全局连续**（C-001…C-045 跨 4 文件）：沿用 094 先例，避免 `feature-ref` 映射出现页面歧义；
   `clause_extract.py` 按「id 在单文件内唯一」判定可解析，本选择不违反语法 owner。
2. **散文「同一锚点」的窄解释**（plan § Disclosed Rulings 1，T-001）：映射单元文本差异 = 合法本地化；
   冲突只在映射层与共享字符串层。
3. **`Sealed` 加入 completion-claim 家族**（plan § Disclosed Rulings 3）：使 `Sealed + block` 可被检出。
4. **拒绝码与 `state-drift` 的分层**：拒绝码走 exit 1 的封闭集；`state-drift` 单独走 exit 2（C-031/C-042）。
5. **074 回合的「回合记录」承载**（plan § Disclosed Rulings 5）：manifest + stdout 捕获（+ 仅 `Sealed`
   时的 `seal.md`），不建第三份台账。
6. **冲突解决的封闭形式**（C-018）：`canonical-map`（分片映射表自带的重指向）/ `recheck-clean`（修复输入后
   重跑不再复现）/ `user-waiver`（C-044 字面行）——三者的证据都在现有产物内，不引入新的决议输入文件。
7. **拆前行的 supersede 目标**（C-022）：指向 `merge-manifest.json` 整文件（line 0），由
   `slices[].carrier_tasks` 列出真正的接手文件——拆分声明只有 FR 范围，逐行映射属于发明（C-016 禁止）。
8. **遗留 `Completed` 的归档路径**（C-030）：seal 不接受 `Completed` 为 from 状态，故其唯一可执行路径是按
   C-044 字面记录的用户裁定；FR-023 中「先被 seal」一项在本形态下不可达，按此披露。

## Stage evidence

- `test-evidence/plan-stage-checks.txt` — 本阶段的确定性检查读数（validate-decision-tensions、
  pre-analyze `--stage plan`、decomposition、mirror/regen 基线、074 闭包 exit 2、测试入口实跑）。
- `research.md` R-01…R-20 — 全部设计输入的文件级实测。
