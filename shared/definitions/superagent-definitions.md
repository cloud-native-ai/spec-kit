# Super Agent Definitions Reference

This file is the **single owner** of the **super agent** concept — the parent-side **relative** logical role that a dispatch edge assigns to its two endpoints. It owns the role definition and its set semantics, the edge predicate and its four closed violation kinds, role depth, the super↔sub protocol, the dispatch settlement contract (§ Termination: the closed settlement values, the per-value evidence requirement, the reactions, the version/legacy rule and the three settlement violation kinds), the closed `role-transition` injection, the state-sync/recovery mapping, the visualization mapping, the zero-second-mechanism boundary, and the terminology boundary. Every other surface reaches this page by pointer: `agent-definitions.md`, `subagent-definitions.md` and `framework-map.md` carry one pointer line / row each, and the dispatch and digest surfaces reference the model without restating it. The role acts on the existing three-layer Agent taxonomy owned by `agent-definitions.md` and adds no fourth layer, no entity type and no runtime.

## The Relative Role (相对角色)

A **role** is decided only by a dispatch edge. A directed edge `P → C` exists if and only if one dispatch by `P` produced one execution of `C`; one dispatch produces exactly one edge. On that edge `P` is the **super agent** — machine identifier `superagent` — and `C` is the **subagent** — machine identifier `subagent`. The classification MUST NOT be derived from executor type, model, tool list, prompt wording or a self-description; a face that classifies roles by entity type is defective.

Roles form a **set** on each executor, not a single label. An executor that parents at least one edge is a super agent; an executor that is a child on at least one edge is a subagent; an executor holding both members is a **dual-role** executor (双重角色) and stays fully a subagent on its parent edge. The machine marker `dual-role` appears only in role-set **output** (the judgement face's `role_set_marker` key): it is never a third role value, never a member of the role set, and never a carrier declaration value.

Carrier declarations use exactly the two role values `subagent` / `superagent`. The **dispatch-duty grant** is a separate declaration: a `dispatch_duty` field taking `granted` / `not-granted`. A grant is not a role claim and a role claim is not a grant; granted-but-not-yet-dispatched is legal.

The executor that directly holds the user session is a **root**: depth 0, and never a subagent.

## Role Edges (角色边)

An edge record has record kind `role-edge`. It is a **projection over existing carriers** — never a new store — with these fields: parent identity, child identity, dispatch-attempt identifier, the declared role for this edge, the independent dispatch-duty grant, the computed depth, the primary carrier source, and any conflict rows.

Identity resolves to existing labels: the child is the existing dispatch label (team / dispatch convention, `run-agent` label, or driver stage `<line_id>-<stage>`); the parent is its own dispatch label, and a root uses its existing run identity — status-spine `run_id`, else line-registry `line_id`, else the owner-declared root literal `root`. Parent-side dispatch records are the **primary carrier**: team run-report dispatch mapping tables, the driver's status spine line + stage, and the `run-agent` label; artifact triplets, status spines, the line registry and run reports cross-check only.

One dispatch produces exactly one edge, and one retry is a new attempt with a new label (old attempt artifacts are kept, never overwritten). When the same field of one edge disagrees between two carriers, the judgement face emits a `conflicts` row naming the field, **both paths** and the edge identity (`parent` / `child` / `attempt`) — never a silent pick.

The judgement face is the deterministic, read-only engine `scripts/python/role-edge-check.py`; its actions, exit codes and output schema are owned by the engine itself and pinned by `tests/contract/test_role_edge_engine.py`. The violation set is **closed at four kinds**:

| Kind | Predicate |
|------|-----------|
| `self-dispatch` | the resolved parent equals the resolved child |
| `dangling-parent` | the parent identity cannot be resolved from the existing records |
| `unbacked-role-claim` | an explicit recorded `superagent` role assertion (a carrier's declared-role field taking `superagent`) while the judgement finds no edge where that executor is the parent. A `dispatch_duty: granted` declaration is not a role claim and never triggers this kind; `dual-role` appears in no carrier |
| `depth-inconsistent` | a recorded `depth_position` disagrees with the computed depth, or a cycle makes depth unresolvable |

A fifth kind MUST NOT be emitted before this page is revised. The settlement contract in § Termination owns a separate closed three-kind violation set — `settlement-unrecorded`, `settlement-out-of-set`, `settlement-unbacked` — carried by this same page; the edge kinds and the settlement kinds never merge, and neither gains a kind before this page is revised.

## Role Depth (角色深度)

The root's depth is 0; an executor's depth is the shortest edge distance from a root, computed from the recorded edges and recheckable against the dispatch records. Role depth is unbounded — it describes the graph, and it is not an authorization rule.

Role depth is unbounded and descriptive; the SDD license-chain depth 2 is an authorization limit owned by `subagent-definitions.md` § Dispatch-Time Governance Obligation — the two axes are orthogonal and neither rewrites the other.

When an executor enters the SDD carrying chain, the three conditions, the three prohibitions, the virtual-cannot-host rule and the one-run-per-member cap apply unchanged, by pointer to the owner named above. A non-SDD fan-out consumes no license-chain depth, and this page MUST NOT be read as a second authorization rule.

## The super↔sub Protocol (super↔sub 协议)

**Downlink.** Every governed dispatch carries seven role fields in its existing payload channel: `parent_identity`, `child_label`, `role_declaration`, `dispatch_duty`, `depth_position`, `authority_ref`, `return_channel`. The four pre-existing injections keep their owners and travel by pointer: the fast-fail clause (`shared/guidelines/fast-fail.md` § 子代理派发注入), the concurrency obligation (`subagent-definitions.md` § The Concurrency Obligation), the reporting duty (`shared/guidelines/reporting-obligations.md`), and the re-anchoring anchor digest (`shared/definitions/re-anchoring-definitions.md`). The payload MUST NOT instruct the child to load any skill, MUST NOT reference a driver skill, and MUST NOT contain loop logic — the anti-nesting owner is `subagent-definitions.md` § Dispatch-Time Governance Obligation.

**Decision block (task-authority content, owner by pointer).** A dispatch that implements an already-recorded decision MAY carry a decision block as task-authority content inside this same payload. Its fields, the acknowledgement and the implementation receipt are owned by `shared/definitions/decision-definitions.md` § 传递与实施 and are referenced here, never restated; the block is never an eighth role field and changes none of the seven fields or four injections above.

**Uplink.** Every return carries the result or deliverable path, evidence pointer(s), an explicit anomaly line (stating "no anomaly" explicitly when none), the concurrency reading triple with its fields owned by `subagent-definitions.md` § The Concurrency Obligation, and the returning executor's identity. Missing any item makes the return incomplete: the parent MUST NOT consume the conclusion and MUST NOT backfill the missing fields.

**Message classes.** Edge messages are classified into one closed set of four tokens: `ack`, `answer`, `result`, `attention-escalation`. Unclassified progress MUST NOT travel up an edge; an executor's activity stays visible through the existing liveness carriers (artifact triplet and `watch-model.md`). This model adds no attention mechanism, channel or notification service.

**User-facing output.** User-facing output is not an edge message: only the root executor composes it, and its channel, boundary and envelope are owned by `shared/guidelines/user-facing-output.md`. A child's return is an input to that output, never the output itself, and a child does not write user-facing text.

**Waiting.** Waiting is bounded and observable through the existing watch model (`watch-model.md`); a human abort or redirect stays servable; slow versus stalled uses the existing thresholds.

**Attempts.** Each retry is a new dispatch attempt with a new label. The old attempt's artifacts are kept; a stale attempt's return is identified by the existing attribution values owned by `watch-model.md` § 11 and MUST NOT be consumed as the current result.

**Authorization.** What an edge may do is decided only by `sdd-route.py --action authorize` together with the recorded routing verdict and the team territory; message content never widens permission; a refusal produces the existing named refusal record; resume or retry re-validates before acting.

**Termination.** Edge end is written into the edge's existing carrier, so the parent can judge it; silent orphaning is a defect. The settlement value set, the per-value evidence requirement, the reactions, the version/legacy rule and the closed settlement violation kinds are owned by § Termination (终止与结算) and are reached only by pointer.

## Termination (终止与结算)

**Termination.** The settlement contract of a dispatch edge lives here. The parent derives exactly one settlement value per attempt it opened, from positive evidence only. This section is the single owner of that contract — the value set, the per-value evidence requirement, the settlement-time rules, the reactions, the version/legacy rule, the virtual/native boundaries and the settlement violation kinds. Every other surface (a skill, a command template, a report contract, an engine or a test) reaches these rules by pointer; **no other surface may carry a second value table, a second evidence matrix or a carrier-private judgment copy.** The judgment face is the read-only engine `scripts/python/role-edge-check.py` `--action settle`.

### Settlement Values (结算值, closed)

Exactly one closed set of seven settlement values applies to every attempt; a value outside it is never coerced. The three semantic classes are `terminal` (`completed`, `failed`, `anomaly`, `cancelled`, `silent-end`), `non-terminal` (`running`) and `detection-defect` (`unknown`).

| Value | Class | Positive evidence required | Readings that explicitly do not constitute it |
|-------|-------|---------------------------|-----------------------------------------------|
| `completed` | terminal | A success terminal record **and** an independent verification of the required deliverable/return; the independent-verification mechanism is one of the closed four — `u4` (driver product verification), `team-verification` (the team report's `## Verification`), `five-element` (a complete five-element uplink), `return-record` (the parent's verified declared-equivalent return) — with non-empty, resolvable evidence pointers | exit code 0 alone; a good-looking log tail; the parent's expectation; any mechanism outside the closed four; a success record with verification absent (that is `failed` (incomplete)) |
| `failed` | terminal | A non-zero terminal record; a named failure return; or exit 0 without the required completion evidence **and without an explicit anomaly signal** (the incomplete kind) | missing logs, no output or silence; a stopped-growing log; a wait that ran out; and exit 0 carrying an explicit anomaly signal, which settles `anomaly` instead |
| `anomaly` | terminal | An explicit anomaly signal together with terminal evidence — for example an exit-0 termination whose last non-empty log line starts with `ANOMALY:`, or an equivalent anomaly return; an exit-0 termination carrying an explicit anomaly signal settles `anomaly` here, and the incomplete branch of `failed` applies only when no anomaly marker is present | an intermediate anomaly line while the subject is still alive: that is `anomaly` observed, and the attempt stays `running` |
| `cancelled` | terminal | An explicit parent-side cancellation record produced under the existing destructive-action discipline | process death; an early exit; a dropped connection |
| `running` | non-terminal | A live check performed at settlement time: the pid alive (not a zombie, start ticks matching), a fresh heartbeat, a live log growing inside the `--live-window` window, or an open return channel | a stale reading; "it was alive last time"; a check that was not performed |
| `silent-end` | terminal (abnormal) | A start record **and** the execution subject gone **and** all four terminal evidences (`completed` / `failed` / `anomaly` / `cancelled`) absent. For process carriers, subject-gone means the recorded pid is absent — it disappeared, or it never appeared within `--start-grace` (or the attempt's `start_grace_s`). For pid-less carriers the same value's substitution applies: the declared wait deadline passed with no return and no live signal, where the deadline comes from `--wait-deadline` (or the attempt's `wait_deadline_s`) and "no live signal" means the settlement-time live check fails on every leg, its live-log leg measured over `--live-window` | "no output was seen"; "the process is not there" without a start record and the absence check; a deadline that has not yet passed; and a live subject — a live attempt is `running`, never `silent-end` |
| `unknown` | detection-defect | The unreadable/unparseable evidence pointer set (finding label `unreadable`), or a claimed attempt with no resolvable start record (finding label `start-record-missing`) | any inference of success, failure or still-running |

### Settlement-Time Rules (结算时刻规则)

- **`silent-end` is a named terminal state, not a fallback.** It MUST NOT be folded into `completed` or `failed`, and it MUST NOT be reported as still running. For a carrier without a pid, the no-pid branch above is the same value's substitution, not a second value. The declared wait deadline only triggers a settlement-time observation: evidence already present at that observation settles the attempt by that evidence, and only an observation that finds no return and no live signal settles `silent-end` — it MUST NOT be declared before the deadline. C1's post-deadline reclassification rides the watcher's existing `--deadline-grace` and adds no settlement-side parameter. A return arriving after the settlement is a late return under the attempts rule below, never a rewrite of the settled value.
- **`unknown` is a detection-defect state, never an ending.** It is produced only in the two readable cases of its value row, each with its finding label (`unreadable` / `start-record-missing`); it names the unreadable pointers or the missing start slot, is not an ending, and carries the same "do not claim success" reaction as `silent-end`.
- **Attempts and labels.** Each attempt has one unique label; a retry is a new dispatch attempt with a new label; the old attempt's artifacts are kept; a stale attempt's late return is never consumed as the current result.
- **Start record or `unknown`; the return channel is not liveness evidence.** Before or at dispatch, the parent records the attempt identity, carrier, parent identity, start time, the optional `wait_deadline_s` / `start_grace_s` and (for process carriers) the pid into the existing dispatch log directory (the judgment face's `--logs-dir` root) as the additive `<label>.attempt` record. C1 reuses its existing four-piece, and a C3 seat dispatched through C1/C2 reuses the same label's carrier start evidence, so neither writes a duplicate; the additive file is permitted additive evidence, not a new storage root. An attempt with no start record cannot prove it existed and settles `unknown` with the finding label `start-record-missing` — never `completed`. The return channel (including the seven-field `return_channel`) is a child-initiated uplink; its silence is neither liveness nor completion, so the parent settles from the attempt record plus live evidence or the deadline plus the carrier's terminal records — never by waiting for a return that may never come.
- **The parent settles before it reports.** The parent settles every attempt it opened before its own externally visible completion report; a report that leaves any attempt unsettled is incomplete and cannot claim success.

### Reactions (反应: report / retry / stop)

Exactly three reactions exist; silent repair is forbidden.

- **report** — a `silent-end` or `unknown` attempt is surfaced as an abnormal report (what was found, why it matters, the intermediate artifacts, optional dispositions) and is not re-dispatched as an ordinary failure without a named diagnosis or a user ruling.
- **retry** — a retry is a new attempt with a new label, and the old attempt's evidence is kept; the existing retry limits are unchanged.
- **stop** — stopping a live attempt records `running` + live evidence + the stop reason, never `silent-end`; stopping or terminating keeps the existing destructive-action discipline and adds no gate.

No silent repair: never fabricate a terminal record, never backfill a missing return field, never rewrite a `.status` line, report or evidence file, never delete evidence, and never consume a stale return. The engine has no kill, retry, delete, rewrite or push authority.

### Cancellation (取消)

`cancelled` comes only from a parent-side explicit cancellation record produced under the existing destructive-action discipline; process death, an early exit or a dropped connection MUST NOT be inferred as cancellation.

### Contract Version and Legacy (版本与旧记录)

Every new settlement-bearing record carries the additive field `settlement_version` (`1` in this page's first version); no existing line format changes. A record without the version declaration its shape requires is annotated `legacy` in settlement/audit output: it is never reported as compliant with this contract, it is never rewritten, and the annotation alone does not produce a failing exit code. Version-bearing is decided per claim shape — a claim file is version-bearing if and only if it carries `settlement_version`; a team-report row has no version slot, so the 7-column header is its version declaration and a 5-column-header row is version-less legacy by schema. A legacy record is exempt from all three settlement violations below (a 5-column row's absent cells are absent columns, not an unrecorded claim) while still deriving its value from its raw evidence; the single deterministic refusal is `unknown` (a detection defect, not a settlement judgment), which applies regardless of the version declaration. No pre-built rejection mechanism is added beyond that single refusal.

### Virtual and Native Boundaries (virtual 排除与 native 前台终结)

Virtual dispatch is excluded from background settlement: it cannot detach from the session, the parent is the executor, and no orphan edge exists — while unfinished virtual work MUST NOT be reported `completed`. When the host offers no background native form, the mode is foreground-terminal: the tool return is the termination event and no settlement edge is created.

### Observer (观察者可选)

An observer may record settlement facts (for example as journal entries), but it MUST NOT be the only settlement carrier — the settlement evidence stays with the carrier records named in § Carrier Evidence, and a line without an observer still settles. No probe class, handler binding or observer dependency is added.

### Carrier Evidence (C1…C6, closed)

Every background-detachable carrier exposes the evidence the judgment face reads; a carrier outside this list is outside the contract, and adding one is a revision of this page.

| ID | Carrier | Evidence the judgment face reads | Evidence-shape owner |
|----|---------|----------------------------------|----------------------|
| C1 | driver stage dispatch (fork) | the four-piece (`pid-`, `status-`, `log-`, `heartbeat-<line>-<stage>`), the stage sidecar/spine and the U4 verdict pointer | `skills/external/sdd-loop-driver/scripts/stage-runner.sh`; `watch-model.md` |
| C2 | external CLI subprocess | the `.live.log` / `.jsonl` / `.status` triplet plus the additive `<label>.attempt` / `<label>.end` and the optional parent-written `<label>.settlement` claim | `skills/internal/create-team/scripts/dispatch.sh` |
| C3 | team run seats | the seat's `<label>.attempt` (carrier `c3-team-seat`) or the same label's C1/C2 start evidence, plus the run report's mapping row and `## Verification` | `skills/internal/create-team/SKILL.md` § Report |
| C4 | native host subagent | `<label>.attempt` (carrier `c4-native`) plus the return record or the five-element uplink | `skills/internal/run-agent/SKILL.md` |
| C5 | virtual subagent | no settlement evidence — excluded (see the virtual boundary above) | `shared/definitions/subagent-definitions.md` § Three Execution Modes |
| C6 | direct external recipes | only through a compliant C1/C2 runner or the foreground-terminal form | `shared/workflow/external-dispatch-recipes.md` |

- **C1 verdict mapping.** The watcher's judgments map onto the settlement values: `DONE` → `completed` (a candidate the driver's U4 verification completes), `FAILED` → `failed`, `ANOMALY` → `anomaly`, `INCOMPLETE` → `failed` (incomplete), `DEAD` → `silent-end`, `NO_SIGNAL` → `silent-end`, `TIMEOUT` / `RUNNING` → `running` only when a settlement-time live check holds, else `silent-end` for a `TIMEOUT` whose subject is dead and which has no terminal record.

### Settlement Violations (结算违例, closed)

Exactly three settlement violation kinds exist, owned by this page; the judgment face emits no other kind.

| Kind | Predicate |
|------|-----------|
| `settlement-unrecorded` | a version-bearing claim slot exists with no value: a 7-column team-report row missing `end_state`/`evidence`, or a claim file carrying `settlement_version` with no `value` |
| `settlement-out-of-set` | a recorded value on a version-bearing record lies outside the closed seven |
| `settlement-unbacked` | a recorded value on a version-bearing record lacks its required positive evidence (`completed` without the closed-four verification; `running` without a settlement-time live check; `silent-end` without start record plus disappearance plus all four terminal evidences absent), or the claim disagrees with the value derived from the evidence |

A fourth settlement kind MUST NOT be emitted before this page is revised. The four edge violation kinds in § Role Edges are unchanged and separate. The settlement judgment face is the read-only engine `scripts/python/role-edge-check.py`, whose `--action settle` keeps the engine's exit codes: `0` every attempt judged (a correctly derived `silent-end` included), `1` settlement violations found, `2` `unknown` findings naming the unreadable pointers or the missing start slot — `unknown` is never represented as exit `0`.

## Role-Transition Injection (身份转变注入)

When a subagent is granted dispatch duty, its dispatch payload MUST physically carry the `role-transition` injection (身份转变注入): the stable identifier plus the nine pointer items below. Physical presence is mandatory because a standing instruction layer does not reach a child executor.

| # | Item id | Points at |
|---|---------|-----------|
| a | `role-activation-scope` | the superagent role activation and the dispatchable scope on this edge |
| b | `self-identity-parent-edge` | the executor's own identity and its parent edge |
| c | `downward-obligation-checklist` | the obligations it must inject into each of its own dispatches, by pointer |
| d | `concurrency-budget-ref` | the available concurrency budget and the existing slot/reserve facts, by pointer to their owners |
| e | `reporting-path` | the reporting path and the reporter / master-subordinate reporting duty, by pointer |
| f | `state-carriers-writer-boundary` | the existing state carriers it reads and writes and the writer boundary, including the visibility contract by pointer |
| g | `attention-classes-escalation` | the message classes above and the escalation rules, with the reporting owner by pointer |
| h | `depth-remaining-prohibitions` | remaining depth and the prohibitions that still bind it, by pointer to their owners |
| i | `aggregate-return-contract` | the aggregate return contract |

The list is closed — adding or removing an item is a contract change. Each item is carried as a pointer, never as rule text. The existing pre-dispatch self-check (`shared/guidelines/fast-fail.md` § 派发前自检) requires the `role-transition` identifier and each item-id slug; a missing identifier or slug is a payload-construction defect and is blocked before dispatch. The check form and its landing are existing — only the judged identifier is new.

The payload red lines are owned by `subagent-definitions.md` § Dispatch-Time Governance Obligation and referenced here: no full driver manual, no skill-load instruction, no driver-skill reference, no loop logic.

A dual-role executor keeps every upload duty of a subagent — gaining the superagent role reduces none of them. It returns **one** structured result to its parent: per-child attribution, per-child evidence paths, failures and anomalies surfaced; the aggregate does not replace the child evidence, and the parent can drill down.

## State Synchronization & Recovery (状态同步与恢复)

Edge state has a single writer per fact: the parent owns the edge record and the aggregate state; the child owns its own latest state (the artifact triplet's `.status` and its return). The parent records the edge and the received returns before its next externally visible action. No shared mutable aggregate is maintained; edge records land per entry, following the framework's Concurrent Development Safety discipline.

The parent derives child state only from the three existing fact layers:

| Layer | Carrier | Used for |
|-------|---------|----------|
| State layer | status spine / line-registry entry | identity, run / line ids, stage verdicts |
| Assignment layer | artifact triplet `.status`, return record, run report | edge state, attempt, result presence |
| Host-event layer | watch model pid / heartbeat / liveness | liveness, stale marking, interrupted / attention |

The parent MUST NOT derive state from conversation memory, child-session transcripts or process scans.

Recovery rebuilds the edges from those three layers and reports the real state: a child still judged to be running is marked `interrupted` / `attention`, never silently `running` or `completed`. Resume and re-entry re-validate authorization before acting, do not replay old messages, and do not re-dispatch completed children; an unverifiable resume stops with a named failure.

## Visualization & Tracking (状态跟踪与可视化)

`scripts/python/status-digest.py` remains the **only** digest renderer. Its role view adds `parent`, `roles`, `role_set_marker` (passed through from the judgement model, never re-derived) and `depth` beside the existing identity, state, recent activity, age and stale fields, in both the table and JSON outputs. The role model is computed once per digest run through the engine's importable interface, so the legacy line view and the role view share one carrier materialization. `nothing-running`, the omitted-count declaration on truncation and stale marking keep their existing semantics.

A fan-out of one parent to N children renders in the same digest read: the parent row plus one row per child. No dashboard, second parser or second renderer is introduced; liveness stays on the artifact triplets, and the dispatch mapping tables in team and driver run reports carry `label → role → dispatch_duty → workspace → parent` by pointer to their report-contract owners.

## Zero Second Mechanism (零第二机制)

This model adds no persistence root, registry, second renderer, dispatcher, scheduler, queue, transport or notification channel. Edge records are projections over the existing carriers named in § Role Edges; the role view is an extension of the existing digest, not a second visualization.

The judgement face is read-only: `scripts/python/role-edge-check.py` has zero write points, answers `--help` / `--version`, and rejects undeclared options before reading — the script interface contract is owned by `shared/definitions/script-interface-definitions.md`.

Owner rules are not copied here and keep their owners: concurrency (`subagent-definitions.md` § The Concurrency Obligation and the concurrency facts under `shared/declarations/facts/`), reporting (`shared/guidelines/reporting-obligations.md`), authorization (`sdd-route.py`), waiting and attribution (`watch-model.md`), the SDD dispatch-time governance and the anti-nesting red lines (`subagent-definitions.md` § Dispatch-Time Governance Obligation), the fast-fail injection (`shared/guidelines/fast-fail.md`), and the re-anchoring obligation (`shared/definitions/re-anchoring-definitions.md`).

Gaining the superagent role grants no new capacity: slots and reserves stay with the existing concurrency facts, and nesting does not amplify them. Suppressing unclassified progress inside an edge never reduces the human-facing reporting duty, which stays with its owner.

## Terminology Boundaries (术语边界)

| Term | Meaning | Where defined |
|------|---------|---------------|
| **super agent** | The parent-side relative logical role on a dispatch edge; prose form (two words) | here |
| **superagent** | The machine identifier of that role, used in carrier declarations and judgement output | here |
| **super-agent** | Glossary alias only; framework prose does not use it | `.specify/glossary.md` `Super Agent` entry |
| **subagent** | The child-side relative logical role; its execution modes, visibility contract and governance stay with the child-side owner | `shared/definitions/subagent-definitions.md` |
| **dual-role** | The output-only marker of the both-roles set state (`role_set_marker`); never a third role value and never a carrier declaration value | here |
| **role edge** | One dispatch's directed parent → child relation, record kind `role-edge` | here |
| **role-transition** | The stable identifier of the injection a dispatch-duty grant carries | here |

The role is **not a fourth layer**: it acts on the three-layer Agent taxonomy owned by `shared/definitions/agent-definitions.md`, and this page MUST NOT be read as a new entity type, a new Agent category or a new owner for subagent behaviour. The parent-side role is owned here; the child side stays with `subagent-definitions.md`.
