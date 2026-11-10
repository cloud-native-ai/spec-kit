# Review-repair r1 — dispositions（095-superagent-role，2026-11-10）

**Scope**: `.specify/specs/095-superagent-role/review.md` 的 P0/P1 findings 与 `.specify/specs/095-superagent-role/code-review.md` 的两条 `blocking` entries。
**Basis**: `/speckit.review` run `r20261110T055657Z-b095-review`（判定 `blocked`；`Implemented → Ready for Review` refused，`blocking-unresolved`）。
**Nature**: 修复实现与守卫；不重写 review 记录（下一轮代码段重写记录后才重新判定转移）。

| # | Review item | Disposition | Evidence |
|---|-------------|-------------|----------|
| 1 | **F1 (P0)** — implement 未落 `Planned → Implemented`，review 转移无合法源状态 | **fixed** — `.specify/features.md` 行 095 `Planned → Implemented`；`.specify/features/095-superagent-role.md` 补齐模板字段块（`**Feature ID**` / `**Name**` / `**Description**` / `**Status**: Implemented` / `**Created**` / `**Last Updated**`），`## Latest Review` 保留并追加 repair 说明；`verification.md` § Feature-list review 改为记录实际翻转（四条件复验）。闭合检查器显式载体路径恢复可用 | `test-evidence/review-repair-closure-acceptance.txt`（`claimed_status=Implemented`、四条件全 true、tasks 54 closed / 0 deferred、`verdict=accept`）；`verification.md` § Feature-list review |
| 2 | **Code blocking-1** — 18 守卫红；`last_completion` 从唯一可达 renderer 移除，`render_digest` 成为死代码 | **fixed** — `render_digest_table`（唯一可达 renderer）恢复 `last_completion` 汇总行；删除不可达 `render_digest`（第二渲染器缺陷消除）；18 守卫对齐重构后的声明面（表格/JSON，断言强度不降） | `test-evidence/review-repair-suite.txt`（41 passed, exit 0）；`test-evidence/review-repair-guards.txt`（105 passed）；`test-evidence/review-repair-mutation-drills.txt` |
| 3 | **Code blocking-2** — C-68 显式「no measurements」态被删，守卫被弱化 | **fixed** — 表渲染恢复 `store=no measurements` 显式汇总行；守卫**强化**：断言该态恰为一条 `store=` 汇总行（`len==1`）、不是逐行 marker、且两条 entry 行不变；红先演练（删除该行 → 测试红） | `test_efficiency_element.py` § C-68 三腿；`test-evidence/review-repair-mutation-drills.txt` Drill B |
| 4 | **P1 C-1** — digest 两次读取 registry；AST 调用点计数无行为载体 | **fixed** — `role-edge-check.py` 的 `read_carrier_inputs` 返回 `registry_payloads`（同一次读取的解析结果），`status-digest.py::read_state` 由该 materialization 派生 legacy 行（一次读取 + 双视图；materialization 不可用时保留单次兜底读取）；`test_status_digest_roles.py` 的 C-1 守卫改为**行为级**：进程内审计钩子观测真实读取，断言 registry 根 1 次扫描、每 entry 1 次打开 | `test-evidence/review-repair-guards.txt`；Drill A（seed 第二次读取 → `observed 2 reads` 红）；`scripts/python/status-digest.py`、`scripts/python/role-edge-check.py`（+ `.specify/` 镜像） |
| 5 | **P1 F2** — 重建基线吸收范围内红灯，「zero NEW」只覆盖特性包 | **fixed** — `notes/baseline-provenance.md` 新增逐模块守卫健康度与归因规则：仅在范围基线 `b3da3a26d` 也红才算 `inherited`；实测 17 条继承（范围前 master 侧重构 `9ac56bf10`/`fb5125eae`）、1 条由范围内 `c2f199955` 引入（拒绝归为 inherited）、1 条范围内修复。`verification.md` SC-009 同步（含本轮修复后全套件复测） | `notes/baseline-provenance.md` § Per-module guard health；`test-evidence/review-repair-baseline-module-health.txt`；`test-evidence/review-repair-closure-suite-comparison.txt`；`verification.md` SC-009 |
| 6 | **P1 F3** — 7 个跨线提交 + 1 个用户裁定使 delta 非特性作用域 | **fixed** — `verification.md` 新增「跨线提交（review F3）」段，逐条登记 `dddd09773`、`c2f199955`、`48d78d1a5`、`9c39b8e06`、`6d13938aa`、`57d364074`、`343ad1e1e`、`dd7cbbab4` 的出处类别与证据；行级提交守卫作为后续改进项记入状态脊 `FO-095-11`（不阻塞本线） | `verification.md` § 跨线提交；`.specify/state/095-superagent-role.md` § 框架观察 `FO-095-11` |
| 7 | **P1 F4** — loop-state 机器块停留在 analyze round 2 | **fixed** — 机器块推进为 `spine_state: active` / `stage: review-repair (round 1)` / `last_verdict` 覆盖 analyze r3/r4 放行、implement P1–P6 完成、review round-1 blocked、repair 进行中；人工 state 行与「当前阶段」同步；追加 review + review-repair 阶段记录 | `.specify/state/095-superagent-role.md` § loop-state / 当前阶段 / Stage Record — review round 1 + review-repair r1 |
| 8 | **F5** — T003 冻结基线重冻结被延后到 review 门 | **fixed** — 先把 tasks-frozen 基线复制到 dated archive（`notes/coverage-baseline-2026-11-10-tasks-frozen.txt`，642 行，`base-sha 2c8da54c0`，保住 analyze 引用），再在 implement pre-flight 位置重冻结 `coverage-baseline.txt`（642 行，`base-sha d54b1c012`）；`tasks.md` T003 `[~] → [X]`；`verification.md` `deferred_tasks=none` + Setup-package disposition 同步 | `tasks.md` T003；`coverage-baseline.txt`；`notes/coverage-baseline-2026-11-10-tasks-frozen.txt`；`test-evidence/review-repair-closure-acceptance.txt`（`tasks.closed=54`、`tasks.deferred=0`） |
| 9 | **P2 F6** — code-review 脚本步骤普查与技能正文矛盾（四步 vs 五步） | **fixed** — `git-delta-review.sh` 头部与 `--help` 的 `NON-INTERACTIVE PATH` 改为五步并具名 `capture` 为第 5 步；`--help` 的 `COMMANDS:` 增补 `capture` 条目；`.specify/skills/internal/code-review/scripts/git-delta-review.sh` 镜像同步；钉死四步的旧守卫 `test_us2_the_non_interactive_path_is_four_steps_read_as_four` 对齐为五步（`..._five_steps_read_as_five`） | `skills/internal/code-review/scripts/git-delta-review.sh` + 镜像；`tests/contract/test_code_review_skill_contract.py`（39 passed） |
| 10 | **P2** plan D-1 未指向 `dd7cbbab4` 对 `better-harness.md` 的修改 | **fixed** — `plan.md` D-1 追加 later user ruling 指针（`verification.log → verification.md`，constitution 1.19.1） | `plan.md` D-1 |
| 11 | **P2 F7**（重派发读到旧 status 判 DONE） | **not repaired this round（budget）** — 已在状态脊 `FO-095-05` 具名记录（含本轮实测与处置建议）；不阻塞本线，转入后续框架改进 | `.specify/state/095-superagent-role.md` § 框架观察 `FO-095-05`；review.md F7 |
| 12 | **P2 F8**（`watch-target.sh --window` 到期不返回 RUNNING） | **not repaired this round（budget）** — 已在状态脊 `FO-095-02` 具名记录（含实测 200s/340s 超时）；不阻塞本线 | `.specify/state/095-superagent-role.md` § 框架观察 `FO-095-02`；review.md F8 |

## 复跑读数（本轮）

| Suite | Command | Reading |
|-------|---------|---------|
| 受影响守卫（blocking-1/2） | `bash scripts/bash/run-tests.sh tests/unit/test_status_digest_unit.py tests/contract/test_efficiency_element.py -q` | exit 0 — **41 passed**（pre-repair: 18 failed / 23 passed） |
| 相关契约（C-1 / 引擎 / 087 digest / 零机制） | `… tests/contract/test_status_digest_roles.py tests/contract/test_role_edge_engine.py tests/contract/test_status_digest.py tests/contract/test_superagent_zero_mechanism.py -q` | exit 0 — **105 passed** |
| code-review 技能契约（F6） | `… tests/contract/test_code_review_skill_contract.py -q` | exit 0 — **39 passed** |
| Closure 全套件（T051 复跑） | `bash scripts/bash/run-tests.sh --names-out .specify/.tmp/095-repair2-names.txt` | exit 1 — **215 failed / 8415 passed / 2 skipped in 47.75s**；NEW vs 303 基线 = 2（均为既有环境归属，具名不声绿） |
| 闭合检查器（显式载体） | `closure-acceptance-check.py --spec-dir … --feature-detail … --feature-registry … --json` | exit 0 — `claimed_status=Implemented`、四条件 true、`verdict=accept` |

## 说明

- **review 记录不改写**：`review.md` 与 `code-review.md` 保持本轮 review 的原始记录；两条 `blocking` 条目的**成因**已修复并复测，但条目本身只在下一轮代码段重写记录时才被取代（`Implemented → Ready for Review` 需重新判定）。
- **归因更正（如实披露）**：review blocking-1 把 18 条红灯全部归因于范围内提交；实测 17 条在范围基线 `b3da3a26d` 即红（范围前 master 侧 digest 重构），1 条由范围内 `c2f199955` 引入。`notes/baseline-provenance.md` 与 `verification.md` SC-009 按实测记录，不沿用原归因。
- **只提交本修复产物**：会话态脏文件（agent 镜像、exec-quant/feedback/session 运行时记录、todo、`checkpoints/` 等）不提交、不还原。
- **镜像**：`status-digest.py`、`role-edge-check.py`、`git-delta-review.sh` 的 `.specify/` 副本已按文件级 `sync-mirrors.py --only` 同步，`diff -q` 逐对一致。
