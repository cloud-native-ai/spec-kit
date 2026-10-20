# Contract: Workspace Isolation & Deterministic Integration（工作区隔离与确定性集成）

**Feature**: 064
**Owning FR**: FR-018…FR-032
**实体**: `data-model.md` § E3/E7/E8/E11；决策 `research.md` § R4–R7
**Implementation surface**: `skills/external/sdd-loop-driver/scripts/line-registry.py`（ownership/integration/archive/resources）+ `references/dispatch-recipes.md`（worktree 与集成程序）+ `references/stage-prompts.md`（并发隔离提示段）

## A. Worktree

- **WI-01（worktree-per-write-line）**: 每条写 line MUST 使用独立 `git worktree` 与专用分支 `line/<line_id>`，从 trunk（或当前集成分支）的 `base_sha` 创建。默认路径 `<repo_parent>/.spec-kit/worktrees/<repo-basename>/<line_id>`，可经入口参数覆盖；MUST 位于任一 line 的 worktree 之外。`worktree_path`/`branch`/`base_sha` MUST 记录在 Registry（FR-018）。
- **WI-02（单写者与分支纪律）**: 每个 worktree 同时只有一个写 line。阶段子代理 MUST NOT 切换分支、创建/删除 worktree、或改写其他 line 的 worktree；runner 与提示词不得包含 `git checkout`/`git switch`/`git worktree` 指令（FR-019）。
- **WI-03（路径冲突）**: worktree 目标路径已存在、或跨文件系统导致创建失败 → 显式失败并上送；MUST NOT 复用或删除其他 line 的 worktree（Edge Case）。

## B. Ownership

- **WI-04（Manifest 与投影）**: 每条 line MUST 声明 Ownership Manifest（`owned_paths`/`read_only_paths`/`forbidden_paths`/`integration_depends_on`）。Manifest 是路径集 owner；Registry 的 `owned_paths` 是可由 Manifest 再生的投影（FR-020, V-OM）。
- **WI-05（归一化与重叠）**: 路径 MUST 归一化（相对/绝对统一、符号链接解析、去尾分隔符）后比较；写-写重叠（相等或互相包含）MUST 在注册/派发前被拒绝或串行化。不同字符串写法的同一路径、嵌套前缀重叠均须命中（FR-020, FR-021, Edge Case）。
- **WI-06（串行化）**: 重叠 line MUST 按当前认领时间 FIFO（Manifest/条目的 `claimed_ns`，无则 `created_at` 的 epoch ns；同一时间戳以 `line_id` 字典序 tie-break）串行化；重新认领（`ownership-check`）刷新认领时间并排在既有等待者之后；后到 line `state=waiting`，持有等待票据（`waiting_reason`、`holder_line_id`、`queued_at`），直到持线者完成集成合并并完成 U6 收尾（`closed`）或经 `release-ownership --reason --evidence-ref` 显式释放。`ownership-check` MUST NOT 隐式晋升；`promote-waiting` MUST 校验持线者满足「带 evidence_ref 的 released 历史」或「`integration_result.status=merged` 且已 U6 `closed`」，否则 exit 3 且 waiting 保持不变（FR-021, FR-057, V-LR-13）。
- **WI-07（持线者死亡）**: 持线者死亡 MUST NOT 自动释放归属；`waiting` 保持，先保留并上送持线者 worktree/证据，再由显式 `release-ownership --reason --evidence-ref` 处置并留痕。`deregister --reason stale-cleanup` 只把条目标记为 `stale`（写 `stale_at`、保留 Manifest/reservation/worktree），MUST NOT 直接写 `closed`，MUST NOT 构成释放路径（FR-021, FR-055, Edge Case）。
- **WI-08（只读/禁止路径）**: 任何 line MUST NOT 写入另一活动 line 的 `read_only_paths` 或 `forbidden_paths`；命中按重叠处理（FR-021, V-OM-4）。

## C. Runtime, Mirrors, Integration

- **WI-09（运行时记录）**: line 本地运行时记录 MUST 写在各自 worktree 范围内；该 line 的阶段提交 MUST NOT 包含这些记录；MUST NOT 存在跨 line 共享的可写运行时路径。运行时记录路径集合的唯一枚举（含排除项及理由）是 `data-model.md` § E8 **Runtime-record path set** 与 **Excluded stores**，本条款只引用（FR-022, V-AR-4）。
- **WI-10（集成归档）**: 集成者 MUST 在移除 worktree 之前读取并归档各 line 的运行时记录（`archive-runtime` 输出清单 + 哈希）；同名冲突保留双方，禁止静默覆盖（FR-023, V-AR-1/2）。
- **WI-11（镜像一次）**: `sync-mirrors.py` 与 `regen-command-copies.py` MUST 只在集成过程执行一次（全部 line 合并完成后、最终集成提交之前），MUST NOT 每 line 执行（FR-024）。
- **WI-12（单一协调者）**: 合并 MUST 由单一集成协调者执行；不引入常驻服务（FR-025）。
- **WI-13（队列确定性）**: 队列顺序 MUST 确定：`ready_for_merge_at` FIFO，同一时间戳 `line_id` 字典序 tie-break；显式拓扑依赖（Manifest `integration_depends_on`）先于被依赖者，同层仍按 FIFO/tie-break；重放同一输入得到逐字相同顺序与结果（FR-025, V-IQ-1）。
- **WI-14（逐线步骤与失败保留）**: 对每条 queue 条目依次执行：rebase 到最新 trunk → 完整质量门 → 合并 → 更新该 line 的 Registry 条目（`integration-record`；`state` 保持 `completed`，`merge_ready=false`）→ 归档运行时记录 → 移除 worktree（仅 merged）。镜像同步与命令副本再生成不在此循环内，按 WI-11 在一次集成批次结束时统一执行（每线 Registry + 批次镜像；FR-024 是基数唯一 owner，FR-026 的逐线步骤不含镜像）。任一步失败 MUST 保留该 line 的 worktree 与证据并上送，继续下一条；失败不改变其他条目的相对顺序（FR-026, FR-024, V-IQ-4）。
- **WI-15（push 与确认门）**: 集成 MUST NOT force push，MUST NOT 绕过确认门；push 仍是显式授权动作（FR-027, FR-060）。
- **WI-16（清理）**: worktree 清理 MUST 只在合并成功或用户显式动作后以 `git worktree remove`（无 `--force`）执行；存在未提交/未合并工作时 MUST 保留并上送（FR-032, FR-061）。
- **WI-17（崩溃重入）**: 崩溃/重入 MUST 以 worktree + 状态脊 + Registry 为恢复证据；stale lock MUST 先验证持有者再处置；重入 MUST 先做一次 `--once` 快照（FR-030）。

## D. Build/Test Isolation

- **WI-18（独立资源）**: 每条 line MUST 获得独立端口块、缓存目录与临时目录（或只读共享缓存）；MUST NOT 写入共享路径；MUST NOT 启动全局服务（FR-028, V-RA-1/3）。
- **WI-19（并发上限）**: 并发上限 MUST 可配置并在派发前检查；超限 line 进入 `waiting`（`waiting_reason=concurrency-cap`）（FR-028, V-RA-2）。
- **WI-20（资源报告）**: 每条 line MUST 报告分配的端口、缓存/临时路径与上限使用情况，供协调者与收尾汇总消费（FR-029, V-RA-4）。
- **WI-21（双写线验收）**: 同仓库双写线（重叠与不相交各一组）模拟 MUST 证明：Git index 损坏次数 0、已提交工作丢失次数 0、写-写重叠在写入前被拒绝或串行化的比例 100%、同一输入的集成队列顺序与合并结果重放差异 0、运行时记录只归档一次且镜像/命令副本每批只执行一次（FR-031 五项、FR-023/FR-024, SC-004）。

## Integration Protocol（操作序列）

```text
1. line-registry.py --action integration-plan            # 输入 state=completed 且 merge_ready=true + depends_on，输出有序 order
2. for each entry in order:
   a. git -C <worktree> fetch/rebase onto latest trunk   # 无 force
   b. 运行完整质量门（058 既有阶段校验 + 本特性测试）
   c. 合并（缺省本地合并；push 需显式授权）
   d. line-registry.py --action integration-record --result merged --commit <sha>
      # state 保持 completed；merge_ready=false；integration_result 记录
   e. line-registry.py --action archive-runtime --worktree <wt> --dest <archive>
   f. git worktree remove <wt>                            # 仅 merged；无 --force；失败保留
3. once per batch（全部条目处置后）:
   g. sync-mirrors.py --write --only <touched pairs> + regen-command-copies.py
   h. 最终集成提交（含运行时归档清单与镜像更新）
4. 逐线 U6 收尾：deregister（state=closed，closed_at）       # 必须在步骤 d 的 integration_result 之后
   merged → worktree 已在 f 移除；failed/显式放弃 → worktree_retained=true
```

失败分支：b/c/e/f 任一步失败 → `integration-record --result failed --reason <…>`（`state` 保持 `completed`、`merge_ready=false`），保留 worktree 与证据，继续下一条；该 line 的 U6 不自动执行，等待显式重试或放弃。步骤 g 的镜像失败不回滚已合并 line，但必须在最终提交前重试或显式上送。

## Traceability

| Clause | FR/SC | Planned tests |
|--------|-------|---------------|
| WI-01…WI-03 | FR-018, FR-019 | `test_workspace_isolation_contract.py::test_wi_01_worktree_per_line`, `test_wi_02_branch_discipline`, `test_wi_03_target_occupied` |
| WI-04…WI-08 | FR-020, FR-021 | `test_wi_05_normalization_overlap`, `test_wi_06_fifo_serialization`, `test_wi_07_dead_holder_no_release` |
| WI-09…WI-11 | FR-022…FR-024 | `test_wi_09_runtime_not_committed`, `test_wi_10_archive_conflict_preserved`, `test_wi_11_mirrors_once` |
| WI-12…WI-17 | FR-025…FR-027, FR-030, FR-032 | `tests/integration/test_worktree_integration_queue.py`（确定性/重放/失败保留/git fsck） |
| WI-18…WI-20 | FR-028, FR-029 | `test_wi_18_resource_isolation`, `test_wi_19_concurrency_cap`, `test_wi_20_resource_report` |
| WI-21（双线验收） | FR-031, SC-004 | `tests/integration/test_worktree_integration_queue.py` 的重叠/不相交两组 fixture |
