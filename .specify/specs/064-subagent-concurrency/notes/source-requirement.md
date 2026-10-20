# Feature 064 Brief — Subagent Concurrency, CLI Profiles, and Lifecycle Decoupling

## 1. Goal

Create a Spec Kit feature that makes the subagent-driven SDD mechanism safe and efficient when
multiple agents operate in the same environment and on the same codebase, and when the main
session and its subagents have independent lifecycles.

This is the authoritative input for Feature 064. The target is the Spec Kit framework itself
(`skills/external/sdd-loop-driver/`, `skills/internal/run-agent/`, shared definitions/workflows,
watcher/runner scripts, docs, and contract tests). Feature 063 (`sdd-loop-efficiency`) is a
related but distinct feature: 063 optimizes SDD-loop throughput (fast lane, test budget, plan
constraint, stream-json/nohup); 064 owns subagent concurrency/attribution, CLI capability
profiles, and lifecycle decoupling. CLI-profile scope may have been provisionally added to 063
during an in-flight repair; 064 is the authoritative home. The requirements/analyze stages MUST
record and resolve this cross-feature overlap rather than silently duplicating it.

## 2. Background and observed incident

- A Spec Kit session driving Feature 063 (`sdd-loop-efficiency`) performed a broad `ps` scan and
  inferred that a user message about a "600 s qodercli background-task limit" referred to a
  separate xuanji-robot implement process (PID 88306). It monitored that PID and relayed its
  `IMPLEMENT-DONE` as if it were the Spec Kit session's own progress.
- Root cause: no environment-level line registry, no line/run envelope on events, no
  line-scoped message ingress, and no prohibition on ambient process inference. Per-line state
  spines existed, but line attribution did not.
- A second, independent gap: multiple write agents in one repository share the working tree,
  Git index, runtime stores, mirrors, build caches, and test ports, so even correct attribution
  does not prevent workspace interference.
- Additional observed CLI behavior: qodercli in `-p` mode buffers output until exit; it exposes
  `BASH_DEFAULT_TIMEOUT_MS` / `BASH_MAX_TIMEOUT_MS` (positive override; default max is 600,000 ms);
  session/run logs live under `~/.qoder/logs/`; a detached runner is required to survive main
  session failure.

## 3. Required scope

### A. Same-environment line identity and non-cross-talk (prerequisite layer)

1. **Line Registry**: one environment-level registry mapping
   `line_id`, `run_id`, `project_dir`, `repo_root`, `branch`, `base_sha`, `driver_session`,
   `cli`, `runner_pid`/`qodercli_pid` (with start ticks), `prompt/status/log/heartbeat` paths,
   `owned_paths`, `stage`, `state`, `created_at`, `updated_at`.
   Registration at line start (U0.5), deregistration at line end (U6); atomic writes; stale-line
   detection and explicit cleanup.
2. **Line envelope**: every stage prompt, status, log, heartbeat, sentinel, watcher output, and
   monitor event carries `line_id` and `run_id`. Generic stage sentinels remain, but must be
   attributable. Define a machine-readable envelope (JSON or fixed key/value line).
3. **Message ingress**: a user message without a line/project identifier, while more than one
   line is active, MUST trigger exactly one clarification question. The driver MUST NOT infer a
   line from `ps`, `pgrep`, process names, cwd, or ambient shell state.
4. **Process attribution**: watchers/monitors only consume registered PIDs and verify PID start
   ticks, cwd, and branch against the registry. Broad `ps`/`pgrep` is forbidden for attribution.
   Foreign-line events are marked `foreign` and are neither acted on nor relayed as the current
   line's progress.
5. **Cross-line isolation tests**: same environment, two lines, identical generic sentinel and
   identical CLI command name; prove events do not cross; prove a no-line message asks once;
   prove a foreign monitor event cannot change the current line's state.

### B. Same-project workspace isolation (second layer)

1. **Worktree-per-line**: each write line gets its own `git worktree` and branch from the trunk;
   record `worktree_path`, `branch`, `base_sha`. One writer per worktree; no branch switches in
   the stage subagent.
2. **Ownership manifest**: each line declares `owned_paths` / `read_only_paths` /
   `forbidden_paths`; the coordinator rejects overlapping write ownership; overlapping lines are
   serialized or split.
3. **Runtime and mirror governance**: line-local runtime records (feedback/session/exec-quant);
   the integrator commits/archives them once; `sync-mirrors.py` / command-copy regeneration run
   once in the integration pass, never per line.
4. **Integration queue**: a single coordinator merges `ready_for_merge` lines in FIFO/topological
   order; rebase onto latest trunk, run the full gates, merge, update registry/mirrors, archive
   runtime records, remove the worktree. No force push; confirmation gates unchanged.
5. **Build/test isolation**: per-line caches/ports/temp databases or shared read-only caches;
   no global services; concurrency cap and resource reporting.
6. **Crash and re-entry**: worktree + state spine + registry are the recovery evidence; stale
   locks are investigated, never blindly deleted; re-entry uses a `--once` snapshot.

### C. CLI capability profiles (per subagent CLI, continuously updated)

1. One independent file per CLI under `skills/external/sdd-loop-driver/references/cli/<cli>.md`.
   At minimum qodercli; claude, codex, opencode, and hermes profiles must exist with known /
   unknown sections. Each profile covers:
   - invocation and key flags; supported output modes (`-p` buffered vs `--output-format
     stream-json`); prompt/permission modes;
   - background/timeout behavior (`BASH_DEFAULT_TIMEOUT_MS`, `BASH_MAX_TIMEOUT_MS`, 600,000 ms
     default max; positive override semantics; what 0/negative means);
   - sentinel reliability; buffering/visibility behavior; session/run log locations;
   - detach behavior (nohup/setsid/disown), signal/exit behavior, orphan detection;
   - known defects, version applicability, and the evidence that established each fact.
2. Profiles are consulted at dispatch (U2) and updated at U4/U5 when observed behavior differs.
   The update is continuous, not a one-time document.
3. **Probe + feedback point**: a stable marker `cli-profile:<cli>`; each observation that changes
   a profile MUST update the file and record a feedback entry through the existing feedback
   mechanism. Define the trigger points (at least: dispatch preflight, U4 independent
   verification, U5 stall handling). Do not duplicate feedback-store mechanics; reference the
   owner.
4. qodercli initial profile MUST include the observed facts: `-p` buffers until exit;
   `BASH_MAX_TIMEOUT_MS` positive override; default max 600,000 ms; stream-json support; session
   log paths; a detached runner is required to survive main-session failure.

### D. Main-session / subagent lifecycle decoupling

1. Stage subagents MUST run in a detached process group/session (nohup/setsid/disown), with
   stdio detached from the main session; main-session failure MUST NOT terminate them.
2. The runner writes the four-piece evidence (pid with start ticks, atomic status, log,
   heartbeat) and the line registry entry; the subagent's lifecycle is independent of the
   driver's model loop.
3. **Reattachment**: after main-session recovery, a driver MUST be able to reattach to a
   previously launched subagent using the Line Registry + state spine:
   - verify the registered PID (start ticks/cwd/branch), do a `--once` snapshot;
   - if running, resume monitoring without re-dispatch;
   - if done, continue at U4/U5;
   - if dead, follow the stall/retry procedure with preserved worktree and evidence.
4. Reattachment MUST NOT rely on conversation memory or ambient process scanning. The registry
   and state spine are the only recovery sources.
5. Define orphan/stale handling, duplicate-launch prevention, and cleanup after U6.
6. The lifecycle design must work in both local and remote topologies; remote uses ssh+su+nohup
   with the same registry fields.

## 4. Non-goals / boundaries

- No automatic push; all remote writes remain gated.
- No deletion of uncommitted work; worktree cleanup only after merge or explicit user action.
- No silent content loss in instruction/skill/doc migrations.
- No change to stage sentinel semantics or watcher verdict state machine beyond the attribution
  envelope; existing exit codes remain.
- No new long-running daemon or external service; use existing shell/Python/stdlib and the
  existing feedback/probe engines.
- Cross-machine/multi-user coordination is out of scope unless the line registry design requires
  a minimal remote field.

## 5. Success criteria (draft for requirements refinement)

- Two concurrent lines in one environment with identical sentinels never cross-attribute events;
  a no-line user message causes exactly one clarification.
- Two write lines on the same repository, with overlapping and disjoint path sets, produce no
  Git index corruption, no lost commits, and a deterministic integration queue outcome.
- A main-session kill leaves the stage subagent running; a new session reattaches via the
  registry/state spine and reports the correct stage outcome without re-dispatch.
- qodercli profile captures the observed timeout/buffering/session-log facts; a simulated
  behavior change updates the profile and records a `cli-profile:qodercli` feedback entry.
- Existing confirmation gates, no-push policy, and independent verification remain intact.
- Contract/integration tests cover the above, including a two-line simulation and a
  main-session crash/reattach simulation.

## 6. Relationship to Feature 063

- 063 is the SDD-loop throughput feature; 064 is the subagent runtime/concurrency feature.
- 063's in-flight repair may contain a provisional CLI-profile scope. 064 MUST treat its own
  CLI-profile requirements as authoritative, and the analyze stage MUST reconcile the overlap
  (move/retain with a recorded decision; no duplicate ownership).
- 064 may reuse 063's stream-json/nohup work as a dependency, but must define its own concurrency,
  registry, and reattachment behavior.
