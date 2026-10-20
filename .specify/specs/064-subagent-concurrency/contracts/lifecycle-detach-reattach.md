# Contract: Lifecycle Decoupling — Detach, Lease, Reservation, Reattach

**Feature**: 064
**Owning FR**: FR-046…FR-059
**实体**: `data-model.md` § E4/E5/E6/E10；决策 `research.md` § R8–R9
**Implementation surface**: `skills/external/sdd-loop-driver/scripts/line-registry.py`（lease/reservation/identity/classify-remote，接口清单 owner 为 `contracts/line-registry.md` § Engine Actions）+ `references/dispatch-recipes.md`（detach/runner）+ `references/stage-prompts.md`（重接线程序）+ `scripts/watch-target.sh`（`--once` 快照）

## A. Detach

- **LC-01（独立进程组/会话）**: 阶段子代理 MUST 在独立进程组/会话中运行；本地使用 `setsid`（可用时）+ `nohup`，远端使用 `ssh + su + nohup`；stdio MUST 与主会话脱离（重定向到日志或 `/dev/null`）；主会话终止信号 MUST NOT 传播到子代理（FR-046, FR-047）。
- **LC-02（主会话故障隔离）**: 主会话进程/会话终止 MUST NOT 终止已启动子代理；子代理生命周期独立于驱动的模型循环（FR-047）。
- **LC-03（四件套与登记）**: runner MUST 启动时写入 PID + start token、原子 status、log、heartbeat，并在 Registry 登记 `runner_pid`/`cli_pid` 及 token；CLI MUST 作为记录 PID 的子进程运行（后台启动 + `wait`），不得只记录 runner 外壳（FR-048）。
- **LC-04（派发前预占）**: 派发前 MUST 以 `(line_id, stage)` 的 `O_CREAT|O_EXCL` reservation 防重复启动；reservation 内容含 `run_id`、PID、时间戳（FR-048, FR-056）。reservation 的 `pid` 是 launch 方（launcher/runner 外壳）的启动身份；Registry 的 `runner_pid` 是执行侧 runner。launcher 先占位，runner 启动后更新 Registry，不重写 reservation。

## B. Lease & Identity

- **LC-05（驱动租约获取与续租）**: 会话接管一条 line MUST 先取得 `<line_id>.driver.lock` lease（`O_CREAT|O_EXCL`）；lease 由活会话持有时 MUST NOT 夺取（exit 3）。持有者 MUST 以 ≤ `ttl_seconds/3` 的周期调用 `lease-renew` 刷新心跳（缺省 TTL 600s → ≤200s），并在 U2 派发、U3 终止、U4 校验、U5 处置各续租一次；`lease-renew` 只允许持有者本人（FR-049, V-DL-1/2/4）。
- **LC-06（过期 lease 破除）**: 过期 lease MUST 先验证持有者证据（心跳/PID/token/状态脊），再经 `lease-break --reason --evidence-ref` 显式破除并写历史；若 PID 仍存活且 start token 匹配但心跳已过期（`suspected-alive`），MUST NOT 自动破除，只能追加 `--override` 并在历史中记录「PID 活 + 心跳过期」证据；MUST NOT 盲删（FR-049, V-DL-3）。
- **LC-07（身份校验）**: 取得 lease 后 MUST 校验登记 PID 的 start token；cwd MUST 在平台暴露进程 cwd 时校验（Linux `/proc/<pid>/cwd`），平台不暴露时（macOS）记录 `cwd_check=unsupported` 作为唯一允许的豁免；branch MUST 始终由 worktree `git rev-parse --abbrev-ref HEAD` 复核。校验结果按 `data-model.md` § E6/V-ID-1/2 分类（FR-050, V-ID-1）。
- **LC-08（快照先行）**: 身份校验通过后 MUST 先执行一次 `watch-target.sh --once` 快照，再决定去向；重接线 MUST NOT 依赖会话记忆、对话历史或宽泛进程扫描（FR-049, FR-050, V-ID-4）。
- **LC-09（远端校验）**: 远端 line 的身份校验经 ssh 在远端执行同一引擎；ssh 不可达 MUST NOT 判为死亡或身份不符（`identity=remote-unreachable` → `stalled`，reason=`remote-unreachable`），也不得触发重派（FR-050, FR-055, FR-058）。

## C. Snapshot Branches

- **LC-10（running）**: 快照判定 running 时 MUST 恢复监听，MUST NOT 重新派发该阶段；重复派发次数 0（FR-051, SC-005）。
- **LC-11（done）**: 快照判定已完成（哨兵 + 证据齐备）时 MUST 进入既有 U4/U5 校验/收尾路径，MUST NOT 重新派发（FR-052）。
- **LC-12（dead / mismatch）**: 快照判定死亡或身份不符时 MUST 按既有 U5 卡死/重试程序处置，保留 worktree 与证据；MUST NOT 盲目杀进程或删除工作树（FR-053, FR-061）。Registry 状态由 U5 显式置 `stalled`（不自动置 `stale`；`stale` 只经显式清理）；`identity=unknown` MUST NOT 映射为 dead，按 stalled/重新校验处置。
- **LC-13（orphan）**: 进程存活但无有效驱动/Registry/状态脊，或 Registry 缺失 → 显式识别、标记 `orphaned` 并上送。识别 MUST 只用线自有证据与已登记 PID；MUST NOT 用宽泛 `ps`/`pgrep` 发现 orphan；处置 MUST 留痕，MUST NOT 静默认领或静默终止该进程（FR-054, V-SR-5）。
- **LC-14（stale）**: Registry 指向的进程已死、PID 复用、cwd/branch 不符或证据超期 → 标记 `stale` 并上送；清理为显式动作；远端不可达记 `stalled` 而非 stale/dead（FR-055, V-LR-10）。

## D. Duplicate Launch & Closure

- **LC-15（重复启动）**: 已有活动 reservation 时，第二次启动 MUST 附着监听（同 `run_id` 且身份有效）或拒绝；MUST NOT 启动第二个同阶段进程。stale reservation MUST 先验证 PID/心跳/状态脊再显式破除（FR-056, V-SR-1/2/3）。
- **LC-16（U6 收尾）**: U6 MUST 在 `integration_result`（merged|failed）记录之后执行；只读线无集成步骤，阶段完成后直接 U6；写线在集成前显式放弃时以 `last_event=abandoned` 关闭。U6 MUST 注销 Registry 条目（`state=closed`、`closed_at`）、释放 reservation 与 lease、按保留策略归档证据；worktree 的移除只由集成序列在合并成功后执行（WI-14/FR-026），未合并（failed/显式放弃）时保留并置 `worktree_retained=true`（用户显式动作除外，FR-032）；MUST NOT 留下 `active` 残留（FR-057, SC-010）。
- **LC-17（本地/远端同构）**: 本地与远端使用同一 Registry 字段与身份校验规则；远端仅增加 `data-model.md` § E1/V-LR-8 定义的最小远端字段（字段枚举不在本条复述）；Registry 始终在驱动侧（FR-058, FR-065）。
- **LC-18（kill/reattach 验收）**: 主会话 kill 后子代理存活率 100%；新会话经 Registry + 状态脊重接线成功率 100%、重复派发 0；running/done/dead 三分支与证据一致率 100%（FR-059, SC-005/SC-010）。

## Reattach Sequence（操作程序）

```text
1. line-registry.py --action lease-acquire --line-id <id> --session <sess> --pid $$   # live holder → exit 3
2. line-registry.py --action verify-identity --line-id <id> [--probe-json <file>]     # remote: ssh probe first
3. bash watch-target.sh --once --line-id <id> --run-id <run> --label <id> \
        --pid-file … --status-file … --log … --sentinel <STAGE>-DONE --heartbeat … --meta …
4. branch:
   identity=ok      + verdict RUNNING  → 重入 watch window（零重派）
   identity=ok      + verdict DONE     → U4 独立校验 → U5/U6
   identity=dead/mismatch              → U5 卡死/重试程序（保留 worktree）
   identity=remote-unreachable         → stalled(remote-unreachable) + 连通性重试（零重派）
   reservation/orphan evidence         → orphan-check 调查，不盲派
5. 每 ≤ ttl/3 续租 lease；阶段推进点（U2/U3/U4/U5）各续租一次
6. U6 在 integration_result 之后关闭（state=closed）；merged 的 worktree 已由集成序列移除，failed/放弃保留
```

## Traceability

| Clause | FR/SC | Planned tests |
|--------|-------|---------------|
| LC-01…LC-04 | FR-046…FR-048 | `test_lifecycle_detach_reattach.py::test_lc_01_detached_survives_sighup`, `test_lc_03_four_piece_and_cli_pid`, `test_lc_04_reservation_exclusive` |
| LC-05…LC-09 | FR-049, FR-050, FR-058 | `test_lc_05_live_lease_refused`, `test_lc_06_expired_lease_break_with_evidence`, `test_lc_07_identity_mismatch`, `test_lc_09_remote_unreachable_not_dead` |
| LC-10…LC-14 | FR-051…FR-055, SC-005 | `tests/integration/test_session_kill_reattach.py`（running/done/dead 三分支） |
| LC-15…LC-17 | FR-056…FR-058, SC-010 | `test_lc_15_second_start_attaches_or_refuses`, `test_lc_16_u6_no_active_residue`, `test_lc_17_remote_fields_isomorphic` |
| LC-18 | FR-059, SC-005/SC-010 | `tests/integration/test_session_kill_reattach.py` + 变异演练（删除 detach → 红） |
