# Quickstart run record — 104-agents-run (T033)

Date: 2026-11-24 · Branch `104-agents-run` · Tree: product slice committed at `8c39cdec0`
(evidence/verification files of this package are the only uncommitted paths at capture time).

Reading discipline: `/speckit.agents …` lines are **chat instructions**, not shell commands —
they cannot be executed by a shell. Every such example is pinned by a contract test (route b)
and carries its premises; only S-0 carries shell commands, and those were just executed with the
real output pasted below.

## S-0 — Prerequisites (executed now)

```console
$ python3 .specify/scripts/python/flow-class-check.py --action lookup --unit-id "spec:104-agents-run"
unit_id: spec:104-agents-run
flow_class: execution
flow_type: -
source: declaration
marker: null
basis: null
neutral: false
exit=0

$ python3 scripts/python/sync-mirrors.py --check
OK: all per-tool command copies match the source templates.
ok    templates/ == .specify/templates/ (23 files, byte-identical)
ok    skills/external/ == .specify/skills/ (394 files, byte-identical)
ok    skills/internal/ == .specify/skills/internal/ (139 files, byte-identical)
ok    agents/ == .specify/agents/templates/ (20 files, byte-identical)
ok    scripts/ == .specify/scripts/ (132 files, byte-identical)
projected[bash-version-guard] .specify/scripts/bash/check-prerequisites.sh <- scripts/bash/check-prerequisites.sh: ok
projected[bash-version-guard] .specify/scripts/bash/generate-instructions.sh <- scripts/bash/generate-instructions.sh: ok
projected[bash-version-guard] .specify/scripts/bash/run-tests.sh <- scripts/bash/run-tests.sh: ok
projected[python-version-bridge] .specify/scripts/python/script-interface-check.py <- scripts/python/script-interface-check.py: ok
projected[python-version-bridge] .specify/scripts/python/script_interface_cli.py <- scripts/python/script_interface_cli.py: ok
projected[python-version-bridge] .specify/scripts/python/sync-mirrors.py <- scripts/python/sync-mirrors.py: ok
ok    shared/ == .specify/shared/ (114 files, byte-identical)
exit=0

$ python3 scripts/python/regen-command-copies.py --check
OK: all per-tool command copies match the source templates.
exit=0
```

Telemetry note: `sync-mirrors.py --check` also prints the per-tool copy verdict as its first
line (the tool checks both generators' outputs); the per-pair rows below it are the six mirror
pairs. The expected results (exit 0, byte-identical pairs) were observed, not pre-written.

## S-1 … S-7 — chat instructions, pinned by tests (not shell-runnable)

| Scenario | Chat instruction (excerpt) | Pinning evidence |
|----------|---------------------------|------------------|
| S-1 one run with a task | `/speckit.agents run sdd-debt-governor 审计 src/ 下的技术债并输出清单` | `tests/contract/test_agents_run_command_contract.py` (C-01/C-06/C-08); `tests/contract/test_agents_run_skill_wiring.py` (C-11/C-12/C-15 text pins; runtime = behavior-class: `test-evidence/behavior-class-evidence.md`) |
| S-2 multiple runs under one superagent | two consecutive `run` invocations with different agents | `tests/contract/test_agents_run_skill_wiring.py` (C-16/C-17); `tests/contract/test_agents_run_multi_child_edges.py` (same-parent/two-label fixture → 2 edges, depth 1, no violations; label collapse red form) |
| S-3 missing task | `/speckit.agents run sdd-debt-governor` | `tests/contract/test_agents_run_command_contract.py` (C-07); skill input contract `missing task` stop |
| S-4 missing agent name / unknown agent | `/speckit.agents run` and `/speckit.agents run no-such-agent 做点什么` | `tests/contract/test_agents_run_command_contract.py` (C-04/C-10); `tests/contract/test_agents_run_skill_wiring.py::test_us5_not_found_reports_a_bounded_list_with_a_create_suggestion` and `::test_us5_corrupt_definition_is_named_and_never_merged_with_not_found` (data-model E2 text) |
| S-5 team intent not served | `/speckit.agents run 三个 agent 并行审计并汇总` | `tests/contract/test_agents_run_command_contract.py` (C-03/C-08 sample 5); skill § Team parameters conflict sentence |
| S-6 SDD-driver assignment vs ordinary run | conditional probe | `tests/contract/test_agents_run_skill_wiring.py` (C-18 applicability text; execution is behavior-class) |
| S-7 behavior-class route | — | `test-evidence/behavior-class-evidence.md`; `test-evidence/mutation-drill.md` |

## Teardown

No temporary resource was created: every command above is read-only (lookup) or a
check-mode generator that writes nothing; no background process, no container, no cluster.
Nothing to clean up.
