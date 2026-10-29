# Specification-Driven Development（SDD）过程评审报告：Feature 064 Subagent 并发归属、CLI 能力档案与生命周期解耦

> **Audience**: spec-kit framework maintainers.
> **Purpose**: 识别 Feature 064 的 SDD 生命周期中暴露出的模板、命令提示词、自动化与工作流问题，并给出可执行的改进目标。
> **Problem-first**: 本报告不叙述 Feature 064 的业务价值；只记录过程缺口、证据声明与真实行为之间的差距。所有证据都在报告内引用；读者不需要打开源文件才能判断问题是否成立。
> **评审边界**: 不修改实现或上游产物；本报告是 review 阶段的唯一新增制品。

## 0. Portable Project Context（自包含快照）

| Field | Value |
|-------|-------|
| Requirement ID | 064 |
| Requirement Key | `064-subagent-concurrency` |
| Requirement Name | Subagent 并发归属、CLI 能力档案与生命周期解耦（Subagent Concurrency, CLI Profiles, and Lifecycle Decoupling） |
| Related Feature | 064（本特性自身；与 058/061/063 有引用关系） |
| Repository | `spec-kit`（`specify-cli` 0.0.22） |
| Repository URLs | `git@gitee.com:cloud-native-ai/spec-kit.git`、`git@github.com:cloud-native-ai/spec-kit.git`、`git@gitlab.alibaba-inc.com:cloud-native-ai/spec-kit.git`（均为 SSH；无 HTTPS web remote） |
| Reachability of COMMIT_SHA | **UNRESOLVABLE**：`git branch -r --contains HEAD` 输出为空，分支无 upstream；HEAD 未 push 到任何 remote。因此本报告使用绝对路径，并在需要时给出 `git show 26b19104:<path>` 的恢复指令，不伪造 `blob/` URL。 |
| Branch | `064-subagent-concurrency` |
| Commit SHA | `26b191046c7333dab0ee984f53dd613471882562`（short: `26b19104`） |
| Repo Root (absolute) | `/tmp/sdd-worktrees/spec-kit/064-subagent-concurrency`（worktree）；主仓库 `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit` |
| Review Date | 2026-10-20 |
| Reviewer (Agent) | Qoder CLI review session（新鲜上下文；未参与 064 的 requirements/plan/tasks/implement 产出） |
| Environment | macOS Darwin 25.6.0 / arm64；bash `/opt/homebrew/bin/bash`；系统 Python 3.9.6（无 pytest），pytest 9.1.1 位于 `/Users/liuqiming.lqm/project/profiles/.venv/bin/python3`；qodercli 1.1.73；git 2.54.0（Apple Git-157）；`setsid` 缺失，`nohup` 位于 `/usr/bin/nohup` |
| spec-kit Source Snapshot | 同仓库 @ `26b19104`（框架源与 `.specify/` 客户端运行时同树；两顶帽子已声明） |

### Artifact Inventory

| Artifact | Lines | Absolute Path | One-line Summary |
|----------|------:|---------------|-------------------|
| requirements.md | 364 | `/tmp/sdd-worktrees/spec-kit/064-subagent-concurrency/.specify/specs/064-subagent-concurrency/requirements.md` | 68 FR / 10 SC / 5 US / 8 实体 / 4 shared strings；含 clarify 与 analyze repair 裁决 |
| plan.md | 252 | `/tmp/sdd-worktrees/spec-kit/064-subagent-concurrency/.specify/specs/064-subagent-concurrency/plan.md` | 16/16 宪法检查、D-01…D-17、镜像义务、Same-Author 复核 |
| tasks.md | 386 | `/tmp/sdd-worktrees/spec-kit/064-subagent-concurrency/.specify/specs/064-subagent-concurrency/tasks.md` | 82 任务（T001–T082），全部 `[X]`；DoD/GATE-1…10 |
| data-model.md | 355 | `/tmp/sdd-worktrees/spec-kit/064-subagent-concurrency/.specify/specs/064-subagent-concurrency/data-model.md` | E1–E11、59 条 V 规则、状态迁移 |
| contracts/（6 文件） | 388 | `/tmp/sdd-worktrees/spec-kit/064-subagent-concurrency/.specify/specs/064-subagent-concurrency/contracts/` | LR 13 / EN 16 / WI 21 / LC 18 / CLP 17 / NG 13 = 98 条款 |
| research.md | 172 | `/tmp/sdd-worktrees/spec-kit/064-subagent-concurrency/.specify/specs/064-subagent-concurrency/research.md` | R1–R12 基线、qodercli 观测、两顶帽子 |
| quickstart.md | 213 | `/tmp/sdd-worktrees/spec-kit/064-subagent-concurrency/.specify/specs/064-subagent-concurrency/quickstart.md` | 6 场景（S1–S6）与已跑基线 |
| feature-ref.md | 74 | `/tmp/sdd-worktrees/spec-kit/064-subagent-concurrency/.specify/specs/064-subagent-concurrency/feature-ref.md` | 68/68 FR、10/10 SC 证据计划 |
| verification.md | 124 | `/tmp/sdd-worktrees/spec-kit/064-subagent-concurrency/.specify/specs/064-subagent-concurrency/verification.md` | implement 测试、SC、变异、GATE、analyze 收口台账 |
| checklists/concurrency.md | 332 | `/tmp/sdd-worktrees/spec-kit/064-subagent-concurrency/.specify/specs/064-subagent-concurrency/checklists/concurrency.md` | 40 项需求质量清单：16 PASS / 24 FAIL（dated record） |
| checklists/requirements.md | 40 | `/tmp/sdd-worktrees/spec-kit/064-subagent-concurrency/.specify/specs/064-subagent-concurrency/checklists/requirements.md` | plan 前通用完整性门 |
| notes/red-first-evidence.md | 46 | `/tmp/sdd-worktrees/spec-kit/064-subagent-concurrency/.specify/specs/064-subagent-concurrency/notes/red-first-evidence.md` | R1–R5 red 运行摘要（计数） |
| notes/quickstart-run.md | 170 | `/tmp/sdd-worktrees/spec-kit/064-subagent-concurrency/.specify/specs/064-subagent-concurrency/notes/quickstart-run.md` | S1–S6 的运行摘要与命令形状 |
| notes/063-overlap-adjudication.md | 56 | `/tmp/sdd-worktrees/spec-kit/064-subagent-concurrency/.specify/specs/064-subagent-concurrency/notes/063-overlap-adjudication.md` | 063→064 逐条裁决与合并义务 |
| notes/analyze-repair-1.md | 81 | `/tmp/sdd-worktrees/spec-kit/064-subagent-concurrency/.specify/specs/064-subagent-concurrency/notes/analyze-repair-1.md` | 3 HIGH + 6 MEDIUM 修复与延后项 |
| run state | 72 | `/tmp/sdd-064/state.md` | 断点、阶段、line registry、framework observations |

## 1. Process Execution Timeline

按时间顺序记录实际发生的 SDD 生命周期、与规定流程的偏差，以及需要后文解释的摩擦点。证据来自 `git log --format='%h %ci %s' ae0eebeb..HEAD` 与 `/tmp/sdd-064/state.md`。

| # | Step / Event | Evidence (commit SHA, file, or quoted excerpt) | Deviation from prescribed flow? |
|---|--------------|------------------------------------------------|---------------------------------|
| 1 | U0 入口与五类 preflight；手工双线 Registry（063 + 064） | `/tmp/sdd-064/state.md:3-34`；`run_id=064-subagent-concurrency-20261020T1129Z`；base `ae0eebeb` | 无；本地直驱拓扑，手工 Registry 是 Feature 064 尚未实现时的演示性前置 |
| 2 | requirements 完成（68 FR / 10 SC），提交 `1b10d0dd` | `git log`：2026-10-20 11:35:54；`requirements.md` | **有偏差**：`create-new-requirements.sh` 无条件 `git checkout -b`，与预创建 worktree/branch 冲突；规格目录手工创建，feedback 已记录（`state.md:46`） |
| 3 | clarify 完成（绑定新建 Feature 064；5 组裁决），提交 `45d2e6b6` | `git log`：2026-10-20 11:46:19；`requirements.md:344-352` | 无；但 wrap-up 的 compiled `run-determination.py` 缺 `--run-id/--complexity`，子代理显式补齐（`state.md:48`） |
| 4 | plan + 设计产物，提交 `33df56ea`；两顶帽子证据 `535ce680` | `git log`：12:10:11 / 12:11:39；`plan.md`、`data-model.md`、`contracts/`、`research.md` | 无；同作者门触发，两个 fresh-context 只读子代理复核，25 项发现全部修复（`plan.md:181-187`） |
| 5 | tasks 完成（82 任务），提交 `a36aafe4`；glossary 提交 `7e877a2b` | `git log`：12:21:47 / 12:23:29；`tasks.md` | 无；validate-tasks 0/0 |
| 6 | concurrency checklist 完成（40 项：16 PASS / 24 FAIL），提交 `a3344b9a`；validator 证据 `3fc69c6d` | `git log`：12:36:57 / 12:37:10；`checklists/concurrency.md:12-24` | 无；FAIL 是需求质量发现，不是执行异常；清单保持 dated record |
| 7 | analyze 首轮：0 CRITICAL / 3 HIGH / 25 MEDIUM / 2 LOW，Gate **NOT READY** | `/tmp/sdd-064/log-064-subagent-concurrency-analyze.log:8-11` | 无；3 HIGH = I-02 状态机、I-04 镜像基数、I-15 租约 cadence |
| 8 | repair-1：3 HIGH + 6 MEDIUM 修复，提交 `4fba836b`；SC-002 分母 `a1aac7e5` | `git log`：12:57:21 / 12:57:57；`notes/analyze-repair-1.md:7-31` | 无；未降低判据，checklist 24 FAIL 原样保留 |
| 9 | analyze 复核：0 CRITICAL / 0 HIGH / 18 MEDIUM / 4 LOW，Gate **READY** | `/tmp/sdd-064/log-064-subagent-concurrency-analyze-rerun.log:9-12` | 无；Resolved 12 / New 4 / Carried-over 18 |
| 10 | implement 开始；13:10 捕获 71 条 baseline failures；13:16 US1 `9e69f3de` | `git log`：13:16:38；`baseline-failed.txt` mtime 13:10:54 | **有偏差（已披露）**：plan/tasks 前提“pytest 不可用”被证伪；`/Users/liuqiming.lqm/project/profiles/.venv/bin/python3` 有 pytest 9.1.1（`notes/pre-change-measurements.md:18`） |
| 11 | US2 `ba785b0a`；US3 `a100d560`；US4 `c37d7614`；US5/Polish `30439f53`；DoD `64a5933c`；3.8 guard `26b19104` | `git log`：13:21:55 / 13:26:21 / 13:31:41 / 13:48:58 / 13:49:39 / 13:58:15 | 无；每个故事独立提交；但部分测试是文档/元测试（见 F5） |
| 12 | implement 收口：82/82 `[X]`，feature matrix 151 passed，full suite 4077/69（0 NEW，2 fixed） | `verification.md:25-32`；本次复跑确认 | 无；GATE-1…10 机械通过；但 GATE 只检查“存在/通过”，不检查“通过的是行为还是字符串”（见 F5/F10） |
| 13 | review 开始（本报告） | `/tmp/sdd-064/state.md:64-72` | 无；review 为新鲜上下文，未修改实现或上游产物 |

## 2. Findings Summary

| Severity | Count | Definition |
|----------|------:|------------|
| P0 | 1 | 阻塞 spec-kit 的正确使用，或制造静默损坏风险。下一个 spec 之前必须修复。 |
| P1 | 8 | 跨 spec 反复出现的摩擦或证据缺口；当前每个 spec writer 都在付这笔成本。 |
| P2 | 3 | 质量/可维护性问题；在多个 spec 上复利改善。 |

| Category | Count |
|----------|------:|
| Template | 0 |
| Command Prompt | 0 |
| Automation / Scripts | 5 |
| Workflow | 5 |
| Documentation | 2 |

**P0 validation status**: P0-01 已由独立的新鲜上下文只读验证代理复现并确认（verdict: **CONFIRM**）；验证代理还独立发现 `ownership-check` 自身的自动晋升路径（`line-registry.py:1269-1273`），该发现已并入 F1。本报告没有其他 P0 候选。

## 3. Findings（问题与改进目标）

### F1 — 晋升路径 fail-open：stale-cleanup 关闭持线者后，重叠 waiting 线可直接变为 active

- **Severity**: P0
- **Category**: Automation / Scripts
- **Location**: `/tmp/sdd-worktrees/spec-kit/064-subagent-concurrency/skills/external/sdd-loop-driver/scripts/line-registry.py:1203-1219`（`_ownership_conflicts`）、`:1269-1273`（`action_ownership_check` 的自动晋升）、`:1314-1343`（`action_promote_waiting`）、`:713-747`（`action_deregister`）；规格 `/tmp/sdd-worktrees/spec-kit/064-subagent-concurrency/.specify/specs/064-subagent-concurrency/requirements.md:215,359`；契约 `/tmp/sdd-worktrees/spec-kit/064-subagent-concurrency/.specify/specs/064-subagent-concurrency/contracts/workspace-isolation.md:18`；裁决记录 `/tmp/sdd-worktrees/spec-kit/064-subagent-concurrency/.specify/specs/064-subagent-concurrency/notes/analyze-repair-1.md:30`
- **Evidence**（verbatim quote）：

  ```python
  # line-registry.py:1210-1214
  if entry.get("state") in {"closed", "stale", "orphaned"}:
      continue
  other_manifest = _manifest_for_entry(ctx.reg, entry)
  if not other_manifest or other_manifest.get("released_at"):
      continue
  ```

  ```python
  # line-registry.py:1269-1273
  elif data.get("state") == "waiting" and data.get("waiting_reason") == "ownership-overlap":
      data["state"] = "active"
      for key in ("waiting_reason", "holder_line_id", "queued_at"):
          data.pop(key, None)
  ```

  ```python
  # line-registry.py:1314-1326
  require(entry.get("state") == "waiting", ...)
  manifest = _manifest_for_entry(ctx.reg, entry)
  if manifest is not None:
      conflicts, competitors = _ownership_conflicts(ctx, entry, manifest)
      if conflicts:
          ... return exit 3
  ...
  data["state"] = "active"   # line 1338
  ```

  规格原文（`requirements.md:215`）：`直到持线者完成集成合并并完成 U6 收尾，或显式放弃；持线者死亡 MUST NOT 自动释放归属`。`requirements.md:359` 的裁决原文：`stale 清理产生的 closed 不构成自动释放`。`notes/analyze-repair-1.md:30` 同样写明：`stale 清理产生的 closed 不等于显式释放，仍需 release-ownership`。

  本次复现（临时 registry；holder 与 waiter 的 manifest 分别为 `src/` 与 `src/a.py`）：

  ```text
  waiter state after overlap: waiting
  holder state after stale-cleanup: closed
  {"last_event": "promoted", "line_id": "wait-...", "state": "active", ...}
  promote_rc=0
  ```

  独立验证代理在第二个临时 registry 中复现了同一结果，并确认：`ownership-check` 本身也会把无冲突的 waiting 线直接改回 active（`:1269-1273`），因此漏洞不限于显式 `promote-waiting`。现有测试 `tests/contract/test_workspace_isolation_contract.py:135-153` 只覆盖显式 `release-ownership`；`:156-173` 只覆盖“持线者仍打开”的死亡场景，均未覆盖 stale-cleanup 关闭。

- **Why it's a problem**: 这是 fail-open 的串行化闸门。持线者可以因证据过期、身份不符、甚至只是错误调用 `deregister --reason stale-cleanup` 被关闭；waiter 随后晋升为 active，两条写线在逻辑上同时拥有重叠路径。`worktree-per-line` 只隔离物理文件，不阻止两个分支对同一路径的并发修改与后续集成冲突；这正是 FR-021/WI-06 要消除的静默损坏风险。P0 的定义是“制造静默损坏风险”，本项符合。
- **Proposed fix**: 在 `promote-waiting` 与 `ownership-check` 的自动晋升路径上，要求持线者满足以下任一条件才允许晋升：(a) `release-ownership` 历史记录存在且带 `evidence_ref`；(b) `integration_result.status=merged` 且该 line 已 U6 `closed`。stale-cleanup 不应直接写 `closed`；应先进入 `stale`，再经显式 `release-ownership` 或合并证据关闭。增加回归测试：overlap → waiting → holder `deregister --reason stale-cleanup` → `promote-waiting` 必须返回 exit 3，且 waiter 保持 waiting。
- **Validation**: CONFIRM（独立只读验证代理，已复现；见 §2 P0 validation status）。

### F2 — Watcher 没有真正消费 Registry 身份；macOS 上 start token 被忽略

- **Severity**: P1
- **Category**: Automation / Scripts
- **Location**: `/tmp/sdd-worktrees/spec-kit/064-subagent-concurrency/skills/external/sdd-loop-driver/scripts/watch-target.sh:123-150,250-274,305-320`；契约 `/tmp/sdd-worktrees/spec-kit/064-subagent-concurrency/.specify/specs/064-subagent-concurrency/contracts/line-envelope-and-ingress.md:16`（EN-07）；需求 `/tmp/sdd-worktrees/spec-kit/064-subagent-concurrency/.specify/specs/064-subagent-concurrency/requirements.md:204`（FR-013）；自测证据 `/tmp/sdd-worktrees/spec-kit/064-subagent-concurrency/.specify/specs/064-subagent-concurrency/verification.md:30`
- **Evidence**（verbatim quote）：

  ```bash
  # watch-target.sh:250-274
  is_alive() {
    ...
    if [ -r "/proc/$pid/stat" ]; then
      ...
      actual=$(awk '{print $22}' "/proc/$pid/stat" 2>/dev/null)
      if [ -n "$actual" ] && [ "$actual" != "$expected" ]; then
        PID_STATE="reused"
        return 1
      fi
    fi
    PID_STATE="alive"
    return 0
  }
  ```

  参数解析（`:123-150`）只有 `--pid-file`/`--status-file`/`--log`/`--heartbeat`/`--meta` 等文件选项，**没有** `--registry` 或 Registry 路径参数；`evaluate`（`:305-320`）直接读取调用方给出的文件，从不查询 Line Registry，也不复核 cwd/branch。契约 EN-07 的要求是：`watcher/monitor MUST 只消费 Registry 中登记且身份校验通过的 PID（start token；cwd/branch 在可用时）`（`line-envelope-and-ingress.md:16`）。

  本次探针（macOS，活进程的真实 `ps -p <pid> -o lstart=` 与 pid 文件中的 `start=1` 不同；status/meta 均为 own、sentinel=1）：

  ```text
  WATCH label=x verdict=DONE pid=alive heartbeat=fresh anomaly=no sentinel=yes rc=0 ... attribution=own
  real_start_token=二 10月/20 14:08:09 2026
  pid_file_start_token=1
  watcher_rc=0
  ```

  自测 `pid-reuse` 仍失败（`verification.md:30`：`18 passed, 4 failed — exactly the recorded baseline (pid-reuse, zombie, ...)`），而 `tests/integration/test_two_line_isolation.py:87-104` 的“PID reuse”用例实际使用 `pid=999999` 的死进程，并没有使用“活着的复用 PID + 错误 start token”。

- **Why it's a problem**: Feature 064 的 SC-001/FR-016 明确要求“PID 复用/死亡不产生假完成”。在目标平台 macOS 上，watcher 只在有 `/proc` 时校验 start token；没有 `/proc` 时 `expected` 被完全忽略，`kill -0` 成功即判 alive。上面探针证明，错误的 start token 仍能得到 `verdict=DONE ... attribution=own`。把 `pid-reuse` 失败当作“既有基线”接受，等于把本特性的核心验收项排除在证据之外。Registry 查询缺失还意味着 EN-07 的“只消费登记 PID”没有落地：watcher 信任调用方给的路径，而不是登记记录。
- **Proposed fix**: 为 `watch-target.sh` 增加 `--registry`（或复用 `SPECIFY_LINE_REGISTRY_DIR`），在 `evaluate` 前读取 `<line_id>.json` 并核对 `runner_pid`/`runner_start_token`/`worktree_path`/`branch`；macOS 使用 `ps -p <pid> -o lstart=` 作为 start token 回退（引擎的 `process_start_token` 已实现，可直接复用逻辑）。增加“活 PID + 错误 token → DEAD/mismatch”的测试，并把 `pid-reuse`/`zombie` 自测从基线失败改为该特性的 gate，否则 SC-001 只能标 Partial。
- **Why not P0**: 当前归属仍受 line-scoped 文件与 envelope 保护，跨线文件不会被 watcher 直接读取；风险集中在同一 line 的 PID 复用/证据过期，影响是假 RUNNING 或（在 stale status 下）假 DONE，未证明跨线静默损坏。因此定为 P1，但必须在下一个依赖 watcher 判定的 spec 前修复。

### F3 — 集成队列只有 plan/record，没有执行 merge 的代码；SC-004 的“合并结果重放差异 0”未被验证

- **Severity**: P1
- **Category**: Workflow
- **Location**: `/tmp/sdd-worktrees/spec-kit/064-subagent-concurrency/skills/external/sdd-loop-driver/scripts/line-registry.py:68-76`（ACTIONS）；`/tmp/sdd-worktrees/spec-kit/064-subagent-concurrency/tests/integration/test_worktree_integration_queue.py:96-166`；契约 `/tmp/sdd-worktrees/spec-kit/064-subagent-concurrency/.specify/specs/064-subagent-concurrency/contracts/workspace-isolation.md:29,41-60`（WI-14 / Integration Protocol）；验证声明 `/tmp/sdd-worktrees/spec-kit/064-subagent-concurrency/.specify/specs/064-subagent-concurrency/verification.md:41`
- **Evidence**（verbatim quote）：

  ```python
  # line-registry.py:68-76 — 没有任何 integrate/merge/rebase action
  ACTIONS = {
      "register", "update", "deregister", "list", "resolve-message",
      "verify-identity", "classify-remote", "reattach-brief",
      "lease-acquire", "lease-renew", "lease-release", "lease-break",
      "reserve", "reservation-status", "reservation-break",
      "orphan-check", "ownership-check", "release-ownership", "promote-waiting",
      "integration-enqueue", "integration-plan", "integration-record",
      "allocate-resources", "archive-runtime",
  }
  ```

  ```python
  # test_worktree_integration_queue.py:86-93 — 只是各自 commit，没有 merge
  c1 = _commit(wt1, "a/one.txt", "one", "line one")
  c2 = _commit(wt2, "b/two.txt", "two", "line two")
  fsck = subprocess.run(["git", "-C", str(repo), "fsck", "--no-dangling"], ...)
  assert fsck.returncode == 0
  all_commits = git(repo, "rev-list", "--all").stdout.split()
  assert c1 in all_commits and c2 in all_commits
  ```

  `test_runtime_archive_once_before_removal`（`:141-165`）只调用一次 `archive-runtime` 并断言一个文件；没有计数集成过程中是否调用了多次。`test_wi_11_mirrors_once`（`tests/contract/test_workspace_isolation_contract.py:236-240`）只是断言 dispatch-recipes 文本里出现“整批”。契约 WI-14 要求逐线执行 `rebase → 完整质量门 → 合并 → integration-record → archive-runtime → git worktree remove`（`workspace-isolation.md:29`），但没有任何执行体实现或测试这条链。

- **Why it's a problem**: SC-004 的验收原文是“同一输入的集成队列顺序与**合并结果**在重放中差异为 0”（`requirements.md:303`）。当前强制执行的是 `integration-plan` 的 JSON 相等；`git fsck` 和 commit membership 发生在 merge 之前，不能证明 merge 后不丢提交、不产生冲突、重放结果一致。`verification.md:41` 把“both commit SHAs in git rev-list; integration-plan replay byte-identical”写成 SC-004 Pass，属于证据层级降级：把“计划确定性”当成了“合并结果确定性”。
- **Proposed fix**: 二选一：(a) 在引擎或独立脚本中实现 integration executor，按 WI-14 顺序执行 rebase/merge/record/archive/remove，并用两个真实 worktree 做端到端重放，断言合并后的 tree hash 或 commit SHA 相等；(b) 明确把 SC-004 收窄为“队列计划确定性”，把“合并结果差异 0”标为未评估/Partial，并新增一个执行协议的脚本化测试。无论哪种，`archive-runtime` 与 `sync-mirrors` 的调用次数都应由执行器计数断言，而不是由文档字符串断言。

### F4 — Detach/reattach 的“存活”证据由测试夹具自造，未执行交付的 runner recipe

- **Severity**: P1
- **Category**: Workflow
- **Location**: `/tmp/sdd-worktrees/spec-kit/064-subagent-concurrency/tests/fixtures/line_fixtures.py:320-341`；`/tmp/sdd-worktrees/spec-kit/064-subagent-concurrency/tests/integration/test_session_kill_reattach.py:83-138`；`/tmp/sdd-worktrees/spec-kit/064-subagent-concurrency/skills/external/sdd-loop-driver/references/dispatch-recipes.md:229-257`；验证声明 `/tmp/sdd-worktrees/spec-kit/064-subagent-concurrency/.specify/specs/064-subagent-concurrency/verification.md:42,54`
- **Evidence**（verbatim quote）：

  ```python
  # line_fixtures.py:320-335
  driver = subprocess.Popen(
      ["bash", "-c", f'echo $$ > "{root / "driver.pid"}"; sleep 30'],
      start_new_session=True,
      ...
  )
  ...
  if selected == "detached":
      kwargs["start_new_session"] = True
      runner_proc = subprocess.Popen(["bash", str(runner)], **kwargs)
  ```

  ```python
  # test_session_kill_reattach.py:97-100
  kill_driver_group(stage)  # SIGHUP to the driver process group
  stage["driver"].wait(timeout=3)
  time.sleep(0.4)
  assert pid_alive(stage["runner"].pid), "detached runner must survive the driver kill"
  ```

  dispatch-recipes 的 detach 配方（`:241-245`）是 prose：

  ```text
  if command -v setsid >/dev/null 2>&1; then
    setsid nohup bash <runner> > <runner-log> 2>&1 < /dev/null &
  else
    nohup bash <runner> > <runner-log> 2>&1 < /dev/null &
    disown
  fi
  ```

  仓库的 `skills/external/sdd-loop-driver/scripts/` 只有 `line-registry.py` 与 `watch-target.sh`，没有可执行的 runner；测试里的 `runner` 是 pytest 在 `tmp_path` 动态生成的 `fake-runner.sh`，由 pytest 自己用 `start_new_session=True` 启动。SIGHUP 发给的是与 runner 无关的 `sleep 30` driver shell。

- **Why it's a problem**: FR-046/FR-047 的核心保证是“主会话故障不得终止子代理”。当前测试证明的是 pytest 夹具的 detach 行为，不是交付给驱动的 recipe。若 dispatch-recipes 的 `setsid/nohup/disown` 顺序、stdio 重定向或 `wait` 逻辑有误，测试仍然全绿。`verification.md:42` 的 SC-005 “detached runner survives driver SIGHUP”因此是夹具级证据，不是产品级证据；mutation drill 2（`SDD_RUNNER_MODE=foreground`）也只是切换夹具的启动方式。
- **Proposed fix**: 把 dispatch-recipes 的本地 detach 片段提取为可执行 runner 脚本（或提供 `scripts/run-stage.sh`），让集成测试通过文档给出的命令启动它，再 kill driver group；断言 runner 写入四件套、心跳继续、registry 的 `runner_pid`/`cli_pid` 正确。若短期不提供 runner，应把 SC-005 标为“protocol simulated”并把该缺口写进 verification，而不是 Pass。

### F5 — `151 passed` 中包含大量文档/元测试；它们不能作为行为覆盖

- **Severity**: P1
- **Category**: Workflow
- **Location**: `/tmp/sdd-worktrees/spec-kit/064-subagent-concurrency/tests/contract/test_line_envelope_contract.py:315-321`；`/tmp/sdd-worktrees/spec-kit/064-subagent-concurrency/tests/contract/test_workspace_isolation_contract.py:236-245,301-305,337-343`；`/tmp/sdd-worktrees/spec-kit/064-subagent-concurrency/tests/contract/test_lifecycle_detach_reattach.py:413-419`；`/tmp/sdd-worktrees/spec-kit/064-subagent-concurrency/tests/contract/test_line_envelope_contract.py:273-292`
- **Evidence**（verbatim quote）：

  ```python
  # test_line_envelope_contract.py:315-321
  def test_en_15_integration_delegate():
      integration = (... / "integration" / "test_two_line_isolation.py")
      text = integration.read_text(encoding="utf-8")
      for needle in ["PLAN-DONE", "foreign", "clarify", "attribution"]:
          assert needle in text
  ```

  ```python
  # test_workspace_isolation_contract.py:236-240
  def test_wi_11_mirrors_once():
      text = _docs()
      assert "sync-mirrors.py" in text
      assert "整批" in text or "每批" in text
      assert "MUST NOT 每 line" in text or "不得每 line" in text or "不在逐线序列" in text
  ```

  ```python
  # test_lifecycle_detach_reattach.py:413-419
  def test_lc_18_kill_reattach_delegate():
      integration = (... / "integration" / "test_session_kill_reattach.py")
      text = integration.read_text(encoding="utf-8")
      for needle in ["SIGHUP", "survive", "reattach", "reservation", "remote-unreachable"]:
          assert needle in text
  ```

  `test_en_13_clarification_non_blocking`（`test_line_envelope_contract.py:273-292`）在 `clarify` 之后由测试自己写 heartbeat、自己调用 `update`，然后断言 heartbeat mtime 和 `updated_at` 前进；没有任何并发执行体，因此它证明的是“测试自己的写入成功”，不是“其他 line 未被暂停”。

- **Why it's a problem**: 这些测试把“文档里写了 X”或“另一个测试文件包含字符串 X”当作行为证据。删除实现但保留文本时，它们仍然全绿；`test_en_13` 则把被验证的动作由测试自己完成。`verification.md` 的“151 passed”和 checklist/analyze 的若干“Closed”依赖这些测试，导致 green 的真实含义被高估。尤其是 F6/F7/F8 所涉的 FR，恰好是由这类测试承载。
- **Proposed fix**: 把测试分成两类并显式命名：`test_doc_*`（只验证文档契约）与 `test_behavior_*`（必须驱动代码/进程）。把 `*_delegate` 测试改为真正运行被引用的测试函数（例如通过 pytest marker/collect 计数），或删除；把 `test_en_13` 改为启动两个真实的 fake 监听器，在 clarify 期间观察第二个 line 的心跳到/状态推进。`verification.md` 的通过计数按“behavior / doc”分列，不再合并成一个 151。

### F6 — `stale` / `orphaned` 只存在于状态词表，从未被任何动作写入

- **Severity**: P1
- **Category**: Automation / Scripts
- **Location**: `/tmp/sdd-worktrees/spec-kit/064-subagent-concurrency/skills/external/sdd-loop-driver/scripts/line-registry.py:46,713-747,1916-1952`；数据模型 `/tmp/sdd-worktrees/spec-kit/064-subagent-concurrency/.specify/specs/064-subagent-concurrency/data-model.md:73-74`；契约 `/tmp/sdd-worktrees/spec-kit/064-subagent-concurrency/.specify/specs/064-subagent-concurrency/contracts/lifecycle-detach-reattach.md:28-29`；需求 `/tmp/sdd-worktrees/spec-kit/064-subagent-concurrency/.specify/specs/064-subagent-concurrency/requirements.md:254-255`；测试 `/tmp/sdd-worktrees/spec-kit/064-subagent-concurrency/tests/contract/test_line_registry_contract.py:187-206`、`tests/contract/test_lifecycle_detach_reattach.py:319-330`
- **Evidence**（verbatim quote）：

  ```python
  # line-registry.py:46
  STATE_VALUES = {"active", "waiting", "stalled", "completed", "orphaned", "stale", "closed"}
  ```

  ```python
  # line-registry.py:726 — deregister 直接 closed
  entry["state"] = "closed"
  entry["closed_at"] = now_iso()
  ```

  ```python
  # line-registry.py:1952 — orphan-check 只输出布尔，不写状态
  return emit({"line_id": line_id, "orphaned": orphaned, "evidence": evidence})
  ```

  数据模型的迁移（`data-model.md:73-74`）写明 `active --identity fail / evidence expired--> stale --explicit cleanup--> closed` 与 `active/waiting --line-owned evidence missing--> orphaned --explicit disposition--> closed`；`verification.md:81` 声称 I-07 “Closed — ... dead/mismatch → U5 → explicit stalled; stale only by explicit cleanup”。但代码中没有任何 `entry["state"] = "stale"` 或 `"orphaned"` 的赋值；`test_lr_10_stale_detection_explicit_cleanup` 在 `deregister --reason stale-cleanup` 后直接断言 `closed`，从未观察到 `stale`；`test_lc_13_orphan_check_uses_line_evidence` 只断言布尔 `orphaned`。

- **Why it's a problem**: FR-054/FR-055/LC-13/LC-14 要求显式识别、标记并上送 stale/orphaned；state 词表与数据模型把 `stale`/`orphaned` 当作可恢复处置的中间状态。实际实现把“识别”与“标记”合并成“直接关闭”，丢失了“先保留证据、再显式处置”的状态语义。这也直接削弱了 F1 的防线：没有 `stale` 中间态，持线者关闭后无法区分“合并后关闭”“显式放弃”“证据过期清理”。
- **Proposed fix**: 增加 `mark-stale` / `mark-orphaned`（或让 `deregister` 根据 `reason` 先进入对应中间态），要求 `closed` 只能从 `stale/orphaned` 经显式 `release-ownership`/处置动作到达；补测试：identity dead/mismatch → `stale`（不是直接 closed）、registry missing → `orphaned`、处置后 → `closed`。若决定不保留中间态，则从 state 词表与数据模型中删除 `stale/orphaned`，并修改 FR-054/055 的验收口径——不能继续两套说法并存。

### F7 — Lease 续租 cadence 只“报告”不“执行”；默认 watch window 超过 `ttl/3`

- **Severity**: P1
- **Category**: Automation / Scripts
- **Location**: `/tmp/sdd-worktrees/spec-kit/064-subagent-concurrency/skills/external/sdd-loop-driver/scripts/line-registry.py:1707-1737`；`/tmp/sdd-worktrees/spec-kit/064-subagent-concurrency/skills/external/sdd-loop-driver/scripts/watch-target.sh:106,119-121,466-474`；需求 `/tmp/sdd-worktrees/spec-kit/064-subagent-concurrency/.specify/specs/064-subagent-concurrency/requirements.md:249`（FR-049）；验证 `/tmp/sdd-worktrees/spec-kit/064-subagent-concurrency/.specify/specs/064-subagent-concurrency/verification.md:87`
- **Evidence**（verbatim quote）：

  ```python
  # line-registry.py:1717-1736
  previous = _iso_epoch(lease.get("heartbeat_at"))
  now = now_epoch()
  interval = int(now - previous) if previous is not None else None
  ttl = int(lease.get("ttl_seconds") or DEFAULT_TTL)
  max_interval = lease_max_interval(ttl)
  lease["heartbeat_at"] = now_iso(now)
  atomic_write_json(path, lease)
  cadence_ok = interval is not None and interval <= max_interval
  ...
  return emit(payload)
  ```

  ```bash
  # watch-target.sh:106,119-121
  WINDOW=300
  ...
  LEASE_RENEW_CMD=""
  LEASE_RENEW_INTERVAL=60
  ```

  `test_lc_05_live_lease_refused_and_cadence`（`:177-181`）在 acquire 后立刻 renew，`interval` 为 0，因此 `cadence_ok` 必然为 true；没有测试间隔 >200s 的情况。`verification.md:87` 声称 I-19 “Closed — lease renew cadence ≤ ttl/3; watch window ≤ ttl/3 or `--lease-renew-cmd` hook”。但默认 `WINDOW=300` 大于 200，`--lease-renew-cmd` 缺省为空；只有驱动主动传参才满足，代码不拒绝也不标记违规。

- **Why it's a problem**: I-15 是 analyze 的 3 个 HIGH 之一，其修复的核心是“活会话不得因心跳过期被合法夺取”。当前实现只把 `cadence_ok` 作为返回值，不写入 registry、不拒绝续租、不改变 lease 状态；默认 watch 窗口又允许 300s 不续租，违反 FR-049 的“MUST ≤ ttl_seconds/3”。这意味着 HIGH 的关闭是规范文本层的，运行时没有相应的控制点；一个 300s 的 watch 窗口足以让下一次续租间隔超过 200s。
- **Proposed fix**: 在 `lease-renew` 中把 `cadence_ok=false` 写入 lease 历史与 registry（`last_event=lease-cadence-violation`），或直接拒绝并返回 exit 3；把持有 lease 的 watch 默认窗口改为 `min(300, ttl/3)`（缺省 200s），或在 `watch-target.sh` 内部自动续租（不依赖调用方传 hook）。新增测试：模拟 heartbeat 300s 前 → renew 返回 `cadence_ok=false` 并被记录/拒绝；watch 窗口 > ttl/3 时显式失败。

### F8 — CLI 观测程序是 prose；SC-006 的 mismatch / no-fact 证据是手写 S5 摘要

- **Severity**: P1
- **Category**: Workflow
- **Location**: `/tmp/sdd-worktrees/spec-kit/064-subagent-concurrency/tests/contract/test_sdd_loop_driver_cli_profiles.py:142-159`；`/tmp/sdd-worktrees/spec-kit/064-subagent-concurrency/skills/external/sdd-loop-driver/references/cli/index.md:50-58`；`/tmp/sdd-worktrees/spec-kit/064-subagent-concurrency/skills/external/sdd-loop-driver/references/cli/qodercli.md:7-16,24-29`；`/tmp/sdd-worktrees/spec-kit/064-subagent-concurrency/.specify/specs/064-subagent-concurrency/notes/quickstart-run.md:100-123`；验证 `/tmp/sdd-worktrees/spec-kit/064-subagent-concurrency/.specify/specs/064-subagent-concurrency/verification.md:43`
- **Evidence**（verbatim quote）：

  ```python
  # test_clp_10_write_order_and_feedback_cardinality
  prompts = (... "stage-prompts.md").read_text(...)
  section = prompts.split("## CLI Capability Profiles", 1)[1].split("\n## ", 1)[0].lower()
  order = ["cli_observations", "provenance", "feedback"]
  positions = [section.find(word) for word in order]
  assert positions == sorted(positions), "write order must be spine → provenance → feedback"
  ```

  ```text
  # quickstart-run.md:102-117
  Command: `bash /tmp/run-s5.sh` (temp feedback workspace; profile copy for the simulated mismatch; ...)
  ...
  == S5.2 no new fact -> zero feedback ==
  count 0
  == S5.3 mismatch -> spine -> provenance -> exactly one feedback ==
  count 1
  ```

  qodercli 档案的 known 行（`qodercli.md:9-16`）把 `cli_version` 写成 `qodercli (version string not exposed by the CLI; host probe 2026-10-20)` / `qodercli (host probe)`，`evidence_ptr` 多数指向 `notes/source-requirement.md §2`（即 brief 快照），而不是一条可复查的观测命令或日志。

- **Why it's a problem**: FR-038/FR-039 要求 U2/U4/U5 的观测、写序、恰好一条反馈、无新事实零反馈；`test_clp_10` 只检查 `stage-prompts.md` 中三个词的先后顺序，`test_clp_11` 直接调用 `feedback-utils.py` 记录一条反馈；没有任何代码或提交的脚本执行“观测事件 → 状态脊 → provenance → feedback”的链路。S5 的 `/tmp/run-s5.sh` 不在仓库中，输出是手写摘要（`count 0`/`count 1`），无法从 HEAD 复现。SC-006 的“simulated `-p` mismatch → exactly 1”因此不是行为证据。known 行的版本/证据也不满足 FR-035 的“CLI version + 可复查证据指针”的强度。
- **Proposed fix**: 提交一个可执行的 S5 观测夹具（例如 `tests/fixtures/cli_observation.py` 或 `notes/run-s5.sh`），从档案副本、状态脊、feedback 引擎三者读取计数；用实际 `qodercli --version`（或记录“命令不可用”的探测输出）填充 `cli_version`，并把 `evidence_ptr` 指向命令/日志/提交，而不是 brief。把 `test_clp_10` 改为执行该夹具并断言“事件数=1 / 反馈数=1 / 无事件=0”，否则 SC-006 标 Partial。

### F9 — 063 唯一 owner 守卫只扫描当前 worktree，看不到 063 分支

- **Severity**: P2
- **Category**: Automation / Scripts
- **Location**: `/tmp/sdd-worktrees/spec-kit/064-subagent-concurrency/tests/contract/test_sdd_loop_driver_cli_profiles.py:247-260`；`/tmp/sdd-worktrees/spec-kit/064-subagent-concurrency/.specify/specs/064-subagent-concurrency/notes/063-overlap-adjudication.md:37-56`；063 分支 `bcf27c77`
- **Evidence**（verbatim quote）：

  ```python
  # test_clp_17_no_063_duplicate_owner
  spec_contracts = [
      path for path in (REPO_ROOT / ".specify" / "specs").glob("*/contracts/cli-profiles.md")
  ]
  assert spec_contracts == [REPO_ROOT / ".specify" / "specs" / "064-subagent-concurrency" /
                            "contracts" / "cli-profiles.md"], spec_contracts
  ```

  但 `git show bcf27c77:.specify/specs/075-sdd-loop-efficiency/contracts/cli-profiles.md` 仍然存在（本次只读检视确认），且 063 分支未合入 master（`git merge-base --is-ancestor bcf27c77 master` 返回 1）。`notes/063-overlap-adjudication.md:50-55` 明确把删除/指针动作列为“merge-time obligations”。

- **Why it's a problem**: 守卫的“repository-wide”只是当前 worktree 范围；它看不到 063 分支的 provisional contract、CP 测试和 Probe Object 设计。只有在 063 合并进包含 064 的分支后，守卫才会因两份 `contracts/cli-profiles.md` 或第二个 Probe Object 转红——这是**合并后**发现，不是合并前阻止。若合并者忽略 notes 的手工义务，双 owner 会短暂进入主线，违反 FR-044“MUST NOT 双 owner”。当前 063 分支没有实际的 `references/cli/` 文件或 Probe 行，所以运行时风险较低，但契约/规格层仍是双份。
- **Proposed fix**: 把守卫改为分支感知：在 CI/merge checklist 中对 063 的树执行同一 residual scan（`git grep`/`git ls-tree` 063 分支），或在 063 合并 PR 的模板中加入“删除 CP-01…CP-10 / `test_cli_profile_record.py` / `skill-sdd-loop-driver-wrapup`”的强制检查项。守卫的失败消息应直接指出 063 分支路径，而不是仅在合并后报“第二个 contract”。

### F10 — Closure ledger 把 22 项全部标为 Closed，但多项只有 prose/string 证据或仍有残留

- **Severity**: P1
- **Category**: Workflow
- **Location**: `/tmp/sdd-worktrees/spec-kit/064-subagent-concurrency/.specify/specs/064-subagent-concurrency/verification.md:72-99`；对照 `/tmp/sdd-worktrees/spec-kit/064-subagent-concurrency/.specify/specs/064-subagent-concurrency/checklists/concurrency.md:291-323`、`/tmp/sdd-064/log-064-subagent-concurrency-analyze-rerun.log:18-41`
- **Evidence**（verbatim quote）：

  ```text
  verification.md:74
  All 22 carried-over/new findings from the analyze rerun were closed during implement; none deferred.
  ```

  ```text
  verification.md:81
  I-07 | MEDIUM | **Closed** — LC-12: identity=unknown is never dead; dead/mismatch → U5 → explicit stalled; `stale` only by explicit cleanup
  ```

  ```text
  verification.md:87
  I-19 | MEDIUM | **Closed** — lease renew cadence ≤ ttl/3; watch window ≤ ttl/3 or `--lease-renew-cmd` hook (watcher implementation + self-test `lease-renew-hook` + docs)
  ```

  ```text
  verification.md:93
  G-01 | MEDIUM | **Closed** — EN-13 named assertion in `test_en_13_clarification_non_blocking` (heartbeat and other-line state keep advancing)
  ```

  ```text
  verification.md:96
  G-06 | MEDIUM | **Closed** — SC-004 comparison level named: plan JSON byte equality + ordered line list + commit SHA membership + fsck
  ```

  这些“Closed”对应的行为证据分别落在 F6（无 stale state）、F7（cadence 只报告）、F5（EN-13 自写心跳）、F3（只比较 plan）与本报告 F12（`at` 类型）上；`verification.md:88` 的 U-01 修复也没有消除 `data-model.md:7 vs :93` 的时间类型冲突。

- **Why it's a problem**: closure ledger 是下一个 maintainer 最先读的“是否真的关闭”的入口。把 doc/string 证据、返回布尔值、plan-only 比较写成“Closed”，会让后续修复失去触发点；同时 checklist 的 24 FAIL 仍是 dated record（不更新是合理的），但 verification 必须区分“需求文本已修”与“运行时行为已验证”。当前 All 22 closed 的表述掩盖了至少 5 项 Partial。
- **Proposed fix**: 为每条 closure 增加 `evidence_kind: behavior | doc-string | design-only` 与 `test` 列；只有 behavior 证据才能标 `Closed`，其余标 `Partial` 并写明未测面。优先把 F2/F3/F6/F7/F8 对应的项重新打开为 Partial/Open，重跑 analyze 确认 residual 数。对 checklist 24 FAIL，保留 dated record，但在 verification 中给出逐项 `addressed | not-addressed | superseded` 的映射，而不是笼统的 22/22。

#### F10.1 Closure audit（针对 analyze 3 HIGH 与 checklist 24 FAIL 的抽样复核）

| Item | Claimed status | Independent re-read | Verdict |
|------|----------------|---------------------|---------|
| analyze I-02 (HIGH) | Resolved | `data-model.md:70-73` 选定 `completed` 为唯一 pre-merge 状态；FR-006 六同步点、WI-06、LC-16、Integration Protocol 一致；`workspace-isolation.md:18` 已收紧 waiting 晋级 | **Resolved（规范/契约层）** |
| analyze I-04 (HIGH) | Resolved | FR-024/FR-026、US2 AS4、V-IQ-4、WI-14 已统一为“每线 Registry + 批次镜像”；但无 merge executor，运行时未验证（F3） | **Partial** |
| analyze I-15 (HIGH) | Resolved | FR-049/LC-05/V-DL-2/4 已写入 ≤ ttl/3 与 suspected-alive；但 `lease-renew` 只报告 cadence_ok、默认窗口 300s（F7） | **Partial** |
| CHK002 | 纠正类已关闭 | `run_history`、`profile_version`、`resources.active_count/cap` 已补；`data-model.md:7` 与 `:93` 的 `at` 类型仍冲突（F12） | **Partial** |
| CHK004 | 裁定类已关闭 | EN-16/watch-model/stage-prompts 用 prose 限制 legacy 为单活动线；watcher 不查 Registry，多线 legacy 仍无运行时闸门（F2/F5） | **Partial** |
| CHK006 | 纠正类已关闭 | `test_en_13` 由测试自己推进 heartbeat/update，未证明其他 line 未被暂停（F5） | **Partial** |
| CHK012 | 纠正类已关闭 | stale-cleanup 关闭后 waiter 仍可晋升；与裁决记录直接矛盾（F1） | **Open（P0）** |
| CHK017 | 纠正类已关闭 | E11 `active_count/cap` 已在 `test_wi_18_19_20_resources` 中真实断言 | **Pass** |
| CHK018 | 纠正类已关闭 | WI-21 已补第五项；integration test 覆盖 overlap/disjoint/fsck/replay/archive | **Pass**（但 merge 结果层面见 F3） |
| CHK022 | 纠正类已关闭 | `feedback_id` 回填、U4 buffering、多事件规则只在 `cli/index.md` prose；无行为夹具（F8） | **Partial** |
| CHK024 | 裁定类已关闭 | Probe Object `skill-sdd-loop-driver-cli-profile` 注册，`probes --validate` exit 0；单一落点实测通过 | **Pass** |
| CHK026 | 裁定类已关闭 | CP-07/CP-08 活引用已删；但 `test_clp_17` 只扫描当前 worktree，063 分支合约仍在（F9） | **Partial** |
| CHK030 | 裁定类已关闭 | FR-049 已量化；运行时 cadence 只报告、默认窗口超限（F7） | **Partial** |
| CHK031 | 裁定类已关闭 | `stale`/`orphaned` 状态从未被写入；identity 分支只输出 hint/boolean（F6） | **Open** |
| CHK036 | 纠正类已关闭 | `test_lr_12` N=12 + interleaved reader，真实并发读断言 | **Pass** |
| CHK037 | 纠正类已关闭 | SC-004 比较层级被定义为 plan JSON + ordered list + commit membership + fsck；未比较 merge 后的 tree/commit（F3） | **Partial** |
| CHK038 | 裁定类已关闭 | SC-003 的 stale-run/unattributed、SC-005 的 orphan/stalled/remote 有测试；但 PID reuse 在 macOS 仍红（F2） | **Partial** |
| CHK039 | 纠正类已关闭 | `feature-ref.md` 已补 SC-001/002/006 度量分量 | **Pass** |
| CHK040 | 裁定类/纠正类已关闭 | NG-03 只断言 notes/contract 中出现 CP 字符串；未证明每个迁移条款有等价承载（F5/F9） | **Partial** |

其余 checklist 项（CHK001/003/005/007/008/009/010/011/013/014/015/016/019/020/021/023/025/027/028/029/032/033/034/035）复读后为文本层已处理；本表只列会改变行为判断或仍有残留的项。结论：**3 HIGH 中 I-02 真正关闭，I-04/I-15 只在规范层关闭；24 FAIL 中至少 CHK012/CHK031 仍未关闭，CHK002/004/006/022/026/030/037/038/040 为 Partial。**“All 22 closed”不能作为当前事实。

### F11 — Red-first、mutation 与 quickstart 证据是摘要，关键产物已删除，无法从 HEAD 复现

- **Severity**: P2
- **Category**: Documentation
- **Location**: `/tmp/sdd-worktrees/spec-kit/064-subagent-concurrency/.specify/specs/064-subagent-concurrency/notes/red-first-evidence.md:5-46`；`/tmp/sdd-worktrees/spec-kit/064-subagent-concurrency/.specify/specs/064-subagent-concurrency/verification.md:49-55`；`/tmp/sdd-worktrees/spec-kit/064-subagent-concurrency/.specify/specs/064-subagent-concurrency/notes/quickstart-run.md:90-98,165-168`；`tasks.md` DoD-6
- **Evidence**（verbatim quote）：

  ```text
  red-first-evidence.md:9-10
  - Exit status: 1
  - Output (tail): `9 failed in 0.05s`; every failure is `AssertionError: engine missing: ...`
  ```

  ```text
  quickstart-run.md:90-92
  WATCH label=life-… verdict=RUNNING ...
  ...
  WATCH label=life-… verdict=DONE ...
  ```

  ```text
  verification.md:53
  | 1. Attribution filter removed (watcher copy) | `2 failed, 4 passed` ... | copy deleted → `6 passed` |
  ```

  mutation drill 的变异副本（`notes/mutation-watch-target.sh`、`notes/mutation-line-registry.py`）在记录中被删除；red-first 只保留 tail 计数，没有完整 stdout/stderr、没有失败断言原文、没有命令的完整输出文件；quickstart S4 使用 `life-…` 省略线号。DoD-6 要求“real command/output/exit evidence”，Single-Run Evidence 纪律要求执行时全量捕获。

- **Why it's a problem**: 读者无法从 HEAD 重新执行 red/mutation 演练，也无法判断 9/24/26/21/19 这些数字是否来自正确的失败原因（例如 fixture 错误 vs 真实缺失）。本次 review 能复跑 feature/full suite，但不能复现 red-first 和 mutation 的“红→绿”；这使 SC-008 的“变异演练”证据停留在自述层。quickstart 的省略号也让“真实输出”不可审计。
- **Proposed fix**: 在 `notes/` 下保存每次 red run 的完整 `stdout/stderr`（或 `.log` 文件）与精确命令；mutation drill 保存 patch/diff 的 sha256 与复现命令（副本可以删除，但 patch 必须可重放）；quickstart 输出不省略线号/run id，或提供可重跑脚本并保存完整日志。DoD/GATE 应检查这些文件存在，而不只是检查摘要表。

### F12 — 数据模型的 `at` 类型自相矛盾：文件声明 ISO-8601，E2 定义为 epoch seconds

- **Severity**: P2
- **Category**: Documentation
- **Location**: `/tmp/sdd-worktrees/spec-kit/064-subagent-concurrency/.specify/specs/064-subagent-concurrency/data-model.md:7,93`；相关契约 `/tmp/sdd-worktrees/spec-kit/064-subagent-concurrency/.specify/specs/064-subagent-concurrency/contracts/line-envelope-and-ingress.md:10`（EN-01）；测试夹具 `/tmp/sdd-worktrees/spec-kit/064-subagent-concurrency/tests/fixtures/line_fixtures.py:115-180`
- **Evidence**（verbatim quote）：

  ```text
  data-model.md:7
  约定：...；时间为 ISO-8601 UTC（`YYYY-MM-DDTHH:MM:SSZ`）；...

  data-model.md:93
  | `at` | epoch seconds | always |
  ```

  EN-01 要求每个事件携带 `at`，但没有规定类型；测试夹具与 watcher 都按 epoch 写入/解析（`write_status` 的 `at={int(time.time())}`；watcher 的 `V_AT="$now"`）。

- **Why it's a problem**: 同一份 data model 在同一文件内给出互斥的时间表示。实现选择了 epoch，测试也按 epoch；但按文件顶部的 ISO 约定阅读的 implementer 可能写 ISO，导致 watcher/engine 的时间比较失败或 `_iso_epoch` 解析失败。这是 checklist CHK002 / analyze U-01 的残留，verification 的 U-01 “Closed”没有覆盖它。
- **Proposed fix**: 明确 `at` 是 epoch seconds 的例外（在文件顶部加一句“除 E2 `at` 为 epoch seconds 外”），或把 `at` 统一为 ISO 并同步 watcher/engine/tests。二选一，不能保留两套约定。

## 4. What Worked — Preserve（Brief）

- 环境级 Line Registry 的真实引擎：per-line 原子替换（`os.link` + fsync + os.replace）、同线 flock、未知字段保留；`test_lr_12_concurrent_registration`（N=12 + interleaved reader）与 `test_lc_04_reservation_concurrent_single_winner`（6 进程单赢家）是真实并发测试，值得保留。
- 双线归属与入口：`test_two_line_isolation.py` 的 foreign/stale-run/unattributed 注入、PATH 桩 `ps`/`pgrep`/`pidof` 零调用、`resolve-message` 的 `clarify/ambiguous-stop/no-active/route` 决策表，直接覆盖了 063 事故的“进程扫描推断”根因。
- 非回归基线纪律：full suite 4077 passed / 69 failed，与 71 条 baseline 相比 **0 NEW / 2 fixed**；watcher self-test 18/4 与既有基线一致；confirmation gates 45/1（既有失败不变）；mirror pair 12 files clean；probe 114 objects / compile-embeds 74 units zero drift。
- 文本层追踪链完整：68 FR / 10 SC / 5 US / 98 契约条款 / 82 任务 / 11 测试文件的编号与映射可解析；`validate-requirements.py` 0/0、`validate-tasks.py` 0/0、`feature-ref.md` 68/68 与 10/10 的覆盖矩阵在文本层成立（行为层缺口见 F5/F10）。
- Analyze 门的修复纪律：3 HIGH 全部有 decision/correction 记录（`notes/analyze-repair-1.md`），复核 0 HIGH；同作者检测委托 fresh-context 只读子代理，25 项发现全部逐条修复，未降级判据。
- 063 重叠裁决：逐条 CP/FR 映射、删除/指针义务、Probe Object 唯一性、`test_clp_17` 守卫，至少把“双 owner”变成了显式可讨论的风险。
- Fast-fail 与诚实披露：`pytest unavailable` 前提被证伪后立即更正并全量使用 `SPECKIT_PYTHON`；`setsid` 缺失、baseline 失败、S5 手动模拟都在 verification 中披露，没有伪造 green。
- 安全边界：engine/watcher 无 `git push`；无 `shutil.rmtree`/`--force`；archive 只复制；失败集成保留 worktree；confirmation gates 未改。
- 本次 review 在交付前捕获了 P0-01；独立验证代理复现并确认，说明“实现 green ≠ 语义正确”的 review 层是必要的。

## 5. spec-kit / SDD Improvement Recommendations

### 5.1 Automation / Scripts

- **R-A1 关闭晋升 fail-open** — Target: `/tmp/sdd-worktrees/spec-kit/064-subagent-concurrency/skills/external/sdd-loop-driver/scripts/line-registry.py` 的 `action_promote_waiting` / `action_ownership_check` / `action_deregister`。Change: 晋升前要求 `release-ownership` 证据或 `integration_result.status=merged` + U6 closed；stale-cleanup 不直接写 `closed`；增加 stale-cleanup + overlapping waiter 的回归测试。Source: F1. Expected impact: 消除写-写重叠的静默损坏风险；让 FR-021/WI-06 可执行。
- **R-A2 Watcher 使用 Registry 身份与平台 start token** — Target: `/tmp/sdd-worktrees/spec-kit/064-subagent-concurrency/skills/external/sdd-loop-driver/scripts/watch-target.sh`。Change: 增加 `--registry`（或 `SPECIFY_LINE_REGISTRY_DIR`）并在 `evaluate` 前核对 registry 的 `runner_pid`/`runner_start_token`/`worktree_path`/`branch`；macOS fallback 到 `ps -p <pid> -o lstart=`；把 `pid-reuse`/`zombie` 从“基线失败”改为本特性 gate。Source: F2. Expected impact: EN-07/FR-013 真正落地，SC-001 的“PID 复用不产生假完成”可被证明。
- **R-A3 实现 stale/orphaned 状态** — Target: `line-registry.py` 的 `action_deregister`/`action_orphan_check`。Change: 增加 `mark-stale`/`mark-orphaned` 或按 reason 进入中间态；`closed` 只能由显式处置到达；补 identity dead/mismatch → stale、registry missing → orphaned 的测试。Source: F6. Expected impact: FR-054/055/LC-13/14 可验收，F1 的状态语义闭合。
- **R-A4 执行 lease cadence** — Target: `line-registry.py:lease-renew` + `watch-target.sh` 默认窗口。Change: `cadence_ok=false` 写入历史并拒绝/标记；默认 watch window ≤ `ttl/3` 或内部自动续租；补 >200s 间隔测试。Source: F7. Expected impact: analyze I-15 的 HIGH 修复进入运行时。
- **R-A5 063 分支感知守卫** — Target: `test_clp_17_no_063_duplicate_owner` + merge checklist。Change: 扫描 063 分支树或把 063 合并 PR 的删除项变成强制检查；在守卫失败消息中给出 063 路径。Source: F9. Expected impact: 双 owner 在合并前而不是合并后被阻止。

### 5.2 Workflow

- **R-W1 集成执行器或脚本化协议测试** — Target: `line-registry.py`/新增 `scripts/integrate-lines.sh` + `tests/integration/test_worktree_integration_queue.py`。Change: 按 WI-14 执行 rebase→gate→merge→record→archive→remove，断言合并后的 tree hash/commit SHA 重放一致，并计数 archive/mirror 调用。Source: F3. Expected impact: SC-004 的“合并结果差异 0”成为可验证事实。
- **R-W2 可执行 detach runner + 端到端测试** — Target: `skills/external/sdd-loop-driver/scripts/` + `dispatch-recipes.md`。Change: 把 setsid/nohup/disown 片段落为 runner 脚本；测试用文档命令启动它并 kill driver group；断言四件套/心跳/registry 身份。Source: F4. Expected impact: FR-046/047/SC-005 从“夹具模拟”升级为产品证据。
- **R-W3 区分 behavior test 与 doc test** — Target: `tests/contract/*` 的 `*_delegate`/`*_mirrors_once`/`*_crash_reentry` 等。Change: 文档检查改名为 `test_doc_*`；行为测试必须驱动代码/进程；`test_en_13` 改为真实双监听器；verification 分列 behavior/doc 计数。Source: F5. Expected impact: 151 passed 不再被误读为 151 个行为断言。
- **R-W4 CLI 观测夹具** — Target: `tests/fixtures/` 或 `notes/run-s5.sh` + `test_sdd_loop_driver_cli_profiles.py`。Change: 提交可执行 S5 脚本，真实执行 spine→provenance→feedback 并计数；known 行使用实际 CLI 版本与可复查证据。Source: F8. Expected impact: SC-006/FR-038/039 可复现。
- **R-W5 Closure ledger 区分证据类型** — Target: `verification.md` 的 §7 表 + `/speckit.implement` 的完成门模板。Change: 每条 closure 加 `evidence_kind`（behavior/doc-string/design-only）与具名测试；只有 behavior 才能写 Closed；其余写 Partial。Source: F10. Expected impact: 下一个 maintainer 不再把“文本已改”当成“行为已验证”。

### 5.3 Documentation

- **R-D1 全量捕获 red/mutation/quickstart 证据** — Target: `notes/red-first-evidence.md`、`notes/quickstart-run.md`、`verification.md` §5。Change: 保存完整 stdout/stderr、精确命令、mutation patch 的 sha256 与可重放指令；quickstart 不省略 line/run id。Source: F11. Expected impact: red→green 与变异演练可从 HEAD 复现。
- **R-D2 统一 `at` 的时间类型** — Target: `data-model.md` § E2 + `contracts/line-envelope-and-ingress.md` EN-01 + watcher/tests。Change: 声明 `at` 为 epoch 的显式例外，或统一改为 ISO 并同步三处。Source: F12. Expected impact: 消除 schema 歧义，避免实现漂移。

## 6. Priority Roadmap

| Priority | Recommendation | Target File / Subsystem | Source Finding(s) |
|----------|----------------|--------------------------|-------------------|
| P0 | 关闭晋升 fail-open（显式释放/合并证据 + 回归测试） | `line-registry.py` `promote-waiting`/`ownership-check`/`deregister` | F1 |
| P1 | Watcher 使用 Registry 身份与 macOS start token | `watch-target.sh` | F2 |
| P1 | 集成执行器或脚本化 merge protocol | `line-registry.py` / integration tests | F3 |
| P1 | 可执行 detach runner + 端到端 kill/reattach | `scripts/` + `dispatch-recipes.md` | F4 |
| P1 | 区分 behavior/doc tests；替换 meta grep | `tests/contract/*` | F5 |
| P1 | 实现 stale/orphaned 状态 | `line-registry.py` | F6 |
| P1 | 执行 lease cadence；默认窗口 ≤ ttl/3 | `line-registry.py` / `watch-target.sh` | F7 |
| P1 | CLI 观测夹具与真实版本证据 | `tests/fixtures` / `cli/*.md` | F8 |
| P1 | Closure ledger 证据分级 | `verification.md` §7 | F10 |
| P2 | 063 分支感知守卫 | `test_clp_17` / merge checklist | F9 |
| P2 | 全量捕获 red/mutation/quickstart | `notes/*` / `verification.md` §5 | F11 |
| P2 | 统一 `at` 类型 | `data-model.md` E2 / EN-01 | F12 |

## 7. Self-Containment Check

- [x] Every file path in this report is absolute, or accompanied by a `git show <sha>:<path>` recovery instruction. (Commit is unpushed; §0 states UNRESOLVABLE and uses absolute worktree paths.)
- [x] Every finding in Section 3 has a quoted excerpt that lets the reader judge the problem without opening the source file.
- [x] No bullet says “see attached”, “as discussed earlier”, or otherwise references context outside this document.
- [x] No placeholder tokens remain anywhere in the report.
- [x] Section 4 is short and bullet-only — no multi-paragraph narrative summaries leaked back in.
- [x] Section 5 recommendations each cite an exact target file in the spec-kit repo and at least one source finding ID.
- [x] P0 validation status is stated explicitly: P0-01 was confirmed by an independent fresh-context read-only validator; no other P0 candidates.

## 8. Feedback

Please share the contents of this document with the spec-kit framework developers.
