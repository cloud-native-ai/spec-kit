# Quickstart — `/speckit.agents run`

Scenarios for the explicit run mode. `/speckit.agents …` lines are **chat instructions**, not shell commands; they cannot be executed by a shell. Every such example is therefore pinned by a contract test (route b) and carries its premises; only S-0 contains shell commands, and those were executed in this stage with the outputs pasted.

Reader baseline and reading scenario are those declared in `requirements.md` (framework maintainers and downstream maintainers judging syntax, role automaticity, multi-child identity and error paths).

## S-0 — Prerequisites (executed, output pasted)

Premises: run from the repository root of a Spec Kit project; `python3 >= 3.8`; the framework's `.specify/` runtime installed.

```console
$ python3 .specify/scripts/python/flow-class-check.py --action lookup --unit-id "spec:104-agents-run"
unit_id: spec:104-agents-run
flow_class: execution
flow_type: -
source: declaration
marker: null
basis: null
neutral: false
(exit 0)

$ python3 scripts/python/sync-mirrors.py --check
... (per-pair lines omitted)
ok    shared/ == .specify/shared/ (114 files, byte-identical)
(exit 0; all six pairs ok, six projected rows ok, per-tool copies OK)

$ python3 scripts/python/regen-command-copies.py --check
OK: all per-tool command copies match the source templates.
(exit 0)
```

Expected results were observed, not pre-written: the three commands returned exit 0 with the shown tails on 2026-11-24. If either generator reports drift, the fix is to regenerate (`--write` / no argument), never to hand-edit a copy.

## S-1 — One run with a task

```text
/speckit.agents run sdd-debt-governor 审计 src/ 下的技术债并输出清单
```

**Premises**: `sdd-debt-governor` resolves (a project instance under `.specify/agents/instances/` when present, else the shipped template `agents/sdd-debt-governor.agent.md`, which exists in this repo); `.specify/agents/execution/configs/_defaults.yaml` exists (seeded by `specify init`); the runtime supports subagents, or an external CLI carrier is configured.
**Expected**: the command routes to `run-agent`; the presentation shows the agent name/layer/description and the task, the role relation (this session = the edge's superagent/root, child label, return channel) and the effective config; one execution is dispatched; the return carries the five uplink elements or is reported incomplete.
**Pinning**: `agents-run-command.contract.md` C-01/C-06/C-08 (`tests/contract/test_agents_run_command_contract.py`); `agents-run-dispatch.contract.md` C-11/C-12/C-15 (`tests/contract/test_agents_run_skill_wiring.py` pins the text; the runtime behavior is behavior-class — review + mutation drill, not contract coverage).

## S-2 — Multiple runs under one superagent

```text
/speckit.agents run sdd-debt-governor 审计 src/ 下的技术债并输出清单
/speckit.agents run sdd-plan-executor 为 104-agents-run 起草 plan 切片
```

**Premises**: both names resolve; the session is a root (or already holds a parent identity from the status spine / line registry).
**Expected**: two independent edges with two different child labels; the second run starts a new dispatch attempt; the first attempt's artifacts are untouched. The existing visibility carriers show the parent row plus one row per child (truncation declares the omitted count).
**Pinning**: `agents-run-dispatch.contract.md` C-16/C-17; `data-model.md` E8 (parent row, one row per child, truncation declared); `tests/contract/test_agents_run_multi_child_edges.py` builds the same-parent/two-label fixture (dispatch records + triplets) and asserts two edges, depth 1, no violations; a mutation collapsing the labels turns it red.

## S-3 — Missing task

```text
/speckit.agents run sdd-debt-governor
```

**Premises**: `sdd-debt-governor` resolves.
**Expected**: the presentation shows the resolved agent (name, layer, description) and reports `missing task`; no dispatch happens; the no-argument listing behaviour is not executed.
**Pinning**: `agents-run-command.contract.md` C-07 (`tests/contract/test_agents_run_command_contract.py`).

## S-4 — Missing agent name, and an unknown agent

```text
/speckit.agents run
/speckit.agents run no-such-agent 做点什么
```

**Premises**: none.
**Expected**: the first reports `missing agent name`, the three capabilities and the usage, and dispatches nothing. The second reports `agent not found` with a bounded available list (omission count declared) and a create suggestion; a definition directory that exists while its `.agent.md` is missing/unreadable is reported as `定义损坏/不可读` with the named path, never as not-found.
**Pinning**: `agents-run-command.contract.md` C-04/C-10 (`tests/contract/test_agents_run_command_contract.py`); `data-model.md` E2.

## S-5 — A team intent is not served here

```text
/speckit.agents run 三个 agent 并行审计并汇总
```

**Premises**: none.
**Expected**: the request is recognized as a multi-agent/team intent and redirected to `/speckit.team`; run is not executed; `--target` carried by a run request is reported as a mode/parameter conflict.
**Pinning**: `agents-run-command.contract.md` C-03/C-08 sample 5 (`tests/contract/test_agents_run_command_contract.py`); `data-model.md` E1 (`--target` mode/parameter conflict).

## S-6 — SDD-driver assignment vs an ordinary run

Premises: for the SDD path, the recipient declares `sdd-invocation: allowed`, its seat policy declares the same, and the duty's routing decision is `sdd` (the narrowed predicate, owned by `subagent-definitions.md` § Dispatch-Time Governance Obligation).
**Expected**: an SDD-driver assignment runs `sdd-route.py --action authorize` before dispatch and dispatches only on the owner's allowed verdict; a normal run that names no SDD driver does **not** invoke the probe and is not blocked by a missing team/seat. A refusal names the failing half (`agent` / `seat` / `both`), the resolved values, both source paths and the seat slug.
**Pinning**: `agents-run-dispatch.contract.md` C-18 (`tests/contract/test_agents_run_skill_wiring.py` pins the applicability text; execution is behavior-class).

## S-7 — Behavior-class evidence route

The following clauses have no independent artifact to assert: presentation disclosure, payload content, return completeness, runtime label uniqueness, probe execution, and reading recording. Their evidence is the truth-source text (pinned for presence), the review pass, and the SC-006 mutation drill recorded in `test-evidence/`. Contract tests MUST NOT be described as covering them.
