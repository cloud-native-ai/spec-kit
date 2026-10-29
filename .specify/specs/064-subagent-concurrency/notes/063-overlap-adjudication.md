# Feature 063 ↔ 064 Overlap Adjudication（CLI 能力档案）

**Date**: 2026-10-20
**Basis**: 064 `requirements.md` FR-044（064 为 CLI 档案权威归属；逐条裁决保留/迁入/去重；禁止双 owner/静默复制）；只读检视 063 在途分支 `bcf27c77` 的 `requirements.md`（FR-044…FR-049）、`contracts/cli-profiles.md`（CP-01…CP-10）、`plan.md`、`tasks.md`。
**Constraint**: 本分支不包含 063 的提交，不修改 063 分支；本文件是 063 合并时的消费依据。063 合并时必须自登记并执行本裁决。

## 1. 总裁决

| 编号 | 主题 | 裁决 | 064 归宿 | 063 合并时动作 |
|------|------|------|----------|----------------|
| 063 FR-044 / CP-01 | 档案集合与落点 | **迁入 064** | FR-033 / CLP-01 | 删除本条款，改一行指针到 064 CLP-01 |
| 063 FR-045 / CP-02 | 必填维度（七维） | **合并去重（064 扩为八维）** | FR-034 / CLP-02 | 删除，指针到 064 CLP-02 |
| 063 CP-03 | known/unknown/provenance | **迁入 064** | FR-035 / CLP-03/14 | 删除，指针 |
| 063 FR-046 / CP-04 | SKILL.md H2 与单一 owner | **迁入 064（H2 名保留）** | FR-042 / CLP-06/07 | 删除，指针；063 不再修改 SKILL.md 该节 |
| 063 FR-047 / CP-05 | U2 派发前查档 | **迁入 064** | FR-037 / CLP-08 | 删除，指针 |
| 063 FR-047 / CP-06 | U4/U5 观测触发 | **迁入 064** | FR-038/039 / CLP-09/10 | 删除，指针 |
| 063 FR-047 / CP-07 | Probe + feedback | **迁入 064（Object id 变更）** | FR-040 / CLP-11/12 | 删除 `skill-sdd-loop-driver-wrapup` 注册设计；不注册任何 CLI-profile 专用 Object |
| 063 FR-048 / CP-08 | 行为不变 | **迁入 064** | FR-041 / CLP-13 | 删除，指针 |
| 063 CP-09 | 版本/缺陷生命周期 | **迁入 064** | FR-035 / CLP-14 | 删除，指针 |
| 063 FR-049 / CP-10 | 交付、镜像与契约测试 | **迁入 064** | FR-045 / CLP-16 | 删除其 CLI-profile 测试与契约文件，指针到 064 |
| 063 §3④ stream-json 默认 | 吞吐优化（输出形态） | **保留在 063** | 064 依赖引用（CLP-02/04 记录事实） | 保留；064 不复制 runner 实现 |
| 063 §3④ nohup 脱离 | 吞吐优化（本地脱离） | **保留在 063** | 064 依赖引用（LC-01/LC-17） | 保留；064 只定义生命周期/Registry 字段 |
| 063 E6 派发记录 / E8 状态脊字段 | 数据模型 | **保留在 063** | 064 扩展 `cli_observations` 与派发三字段（`data-model.md` E10） | 保留；064 引用其 owner 路径 |

**结论**: CLI 能力档案只有一个 owner（064）；063 保留其吞吐优化与 runner 实现，不再拥有档案契约、档案文件、Probe Object 或档案测试。两份分支合并后不得同时存在 `contracts/cli-profiles.md` 的两个版本。

## 2. 逐条差异与处置细节

1. **CP-01 的落点文件**: 063 指定 `references/cli/README.md` 为 schema owner。宪法 X 的保留名阻断严格范围只覆盖项目根与 `docs/`，但按其路径语义原则（目录索引用 `index.md`，不以嵌套 `README.md` 承担索引语义），064 统一为 `references/cli/index.md`，其余不受影响。063 合并时 MUST NOT 恢复 `README.md`。
2. **维度数**: 063 为七维（无独立 detach/信号/孤儿维度）；064 为八维（新增 detach 行为、信号/退出与孤儿检测）。064 的八维定义是唯一 roster；063 的七维文本删除，不保留副本。
3. **Probe Object**: 063 设计注册 `skill-sdd-loop-driver-wrapup`（`skill-wrapup`，unit `skill:sdd-loop-driver`，`wrap-up`）。064 注册 `skill-sdd-loop-driver-cli-profile`（同 class/unit/point）。同一 unit 只保留 064 的 Object；063 合并时不得再添加其 Object 行。主落点经 2026-10-20 实测通过 `probes --validate`；`custom:` unit 不匹配注册表 unit 正则、external 形态要求 `ext-` 前缀，二者不得作为 fallback 登记（analyze repair-1 裁定）。
4. **反馈标记**: 063 的 `STR-009` 与 064 的 `STR-001` 字面量相同（`cli-profile:`）；064 的共享字符串是唯一声明，063 合并时删除其 `STR-009` 行并在正文使用 064 的 `[[STR-001]]` 等价指针（跨规格引用以路径+字符串 ID 表示）。
5. **测试文件**: 063 规划 `tests/contract/test_sdd_loop_driver_efficiency.py` 内的 CP 测试与 `tests/unit/test_cli_profile_record.py`。064 规划 `tests/contract/test_sdd_loop_driver_cli_profiles.py`；063 合并时 MUST 移除其 CP 测试段落，不得保留第二套档案断言。063 的 `test_cli_profile_record.py` 若已实现，迁移为 064 的单元测试或删除；MUST NOT 双份。
6. **内容保全（NG-03）**: 063 的档案条款文本在本文件 §1 与 064 CLP 条款中均有等价承载；063 合并时以「删除 + 指针」方式收编，历史保留在 063 的提交历史与 064 的 `notes/` 记录中，不属于静默丢失。
7. **依赖方向与输出模式边界**: 064 引用 063 的 stream-json 默认与 nohup 实施作为已知依赖，但不依赖 063 分支代码存在；若 063 先合并，064 的 runner 修改需与之协调（同文件 `dispatch-recipes.md`），冲突处理以 064 的归属/生命周期字段为准、以 063 的 stream-json 派生为准。**输出模式的吞吐默认（stream-json）由 063 决定；064 档案只记录缓冲/事件等观测事实并在 U2 只读引用，档案更新不得改写该默认**（CLP-08）。

## 3. 验证清单（063 合并时执行）

1. `grep -rn "CLI Capability Profiles\|references/cli/" .specify/specs/074-sdd-loop-efficiency/` 只应命中指向 064 的指针行，不应有独立条款正文或第二套 CP 编号。
2. `.specify/specs/074-sdd-loop-efficiency/contracts/cli-profiles.md` 已删除（或替换为不超过 5 行的指针文件）。
3. `skills/external/sdd-loop-driver/references/cli/` 只由 064 引入；063 不新增/修改该目录。
4. `shared/definitions/probe-definitions.md` 中 `unit=skill:sdd-loop-driver` 的 Object 恰好 1 行，id 为 `skill-sdd-loop-driver-cli-profile`。
5. `tests/unit/test_cli_profile_record.py` 不存在或已迁移至 064 的测试文件；不存在两组档案断言。
6. `python3 .specify/scripts/python/probe-utils.py --action probes --validate` exit 0。

## 4. Branch verification record (implement, 2026-10-20)

Read-only inspection of `bcf27c77` (main worktree) and repository-wide residual scan on `064-subagent-concurrency`:

- `git show bcf27c77:.specify/specs/074-sdd-loop-efficiency/contracts/cli-profiles.md` exists on 063 only; this tree contains exactly one CLI-profile contract at `.specify/specs/064-subagent-concurrency/contracts/cli-profiles.md`.
- No `references/cli/README.md` exists in this tree; the schema owner is `references/cli/index.md`.
- No `tests/unit/test_cli_profile_record.py` exists in this tree.
- `shared/definitions/probe-definitions.md` contains exactly one object for `unit=skill:sdd-loop-driver`: `skill-sdd-loop-driver-cli-profile` (no `skill-sdd-loop-driver-wrapup`).
- Guard installed: `test_clp_17_no_063_duplicate_owner` performs the same repository-wide scan and is green.
- **Merge-time obligations (unchanged, recorded in §1–§3):** delete 063's provisional `contracts/cli-profiles.md` (or replace with a ≤5-line pointer), delete its CP tests / `test_cli_profile_record.py`, do not restore `references/cli/README.md`, do not register a second Probe Object for `skill:sdd-loop-driver`, and replace its `STR-009` literal with a pointer to 064 `STR-001`.
- The 063 worktree/branch was not modified.

## 5. Branch-aware guard (postreview repair, 2026-10-20)

The worktree-only guard could not see the unmerged 063 branch. `skills/external/sdd-loop-driver/scripts/check-063-overlap.py` now inspects the branch tree directly:

```bash
python3 skills/external/sdd-loop-driver/scripts/check-063-overlap.py --repo <repo>
# 063 absent -> branch-absent; present but unmerged -> pending-merge-obligation (paths);
# merged into HEAD with residual assets -> exit 3 dual-owner

python3 skills/external/sdd-loop-driver/scripts/check-063-overlap.py --repo <repo> --strict-premerge
# exit 3 while the provisional 063 assets still exist (use in the 063 merge checklist/CI)
```

`test_clp_17_no_063_duplicate_owner` executes the guard: the default invocation must exit 0 and disclose `pending-merge-obligation` with the 063 contract path; `--strict-premerge` must exit 3 in that state. This turns the merge-time obligation into an executable pre-merge check instead of a post-merge red test.
