# Contract — Direction Audit (checkpoint protocol)

**Feature**: 090-re-anchoring | **Date**: 2026-11-09 | **Plan**: [plan.md](../plan.md)

The executable half of the discipline. The owner of the procedure is
`skills/external/sdd-loop-driver/references/checkpoint-protocol.md` § Direction audit; this page states the
propositions a guard may assert about it. `FR-004`…`FR-007`; `SC-002`, `SC-004`.

**C-1** — The audit is a mandatory fifth part

The protocol MUST head its part list `## The five parts (all mandatory)` and MUST carry `### 5. Direction audit`. A
checkpoint without part 5 is a defect, and the protocol MUST say so in its `## Rules` list.

**C-2** — The minimal shape carries the audit

The protocol's `## Minimal shape` block MUST carry `## 5. Direction audit` and MUST print a `reload tier:` line, so a
checkpoint written from the shape cannot silently drop the audit.

**C-3** — The audit's primary object is the rules

The protocol MUST state that the audit's primary object is the RULES, not the goal, and MUST give the reason: the
current and next action already carry the goal, while a dropped rule leaves no trace in them.

**C-4** — Question 1 asks the rules, and carries the named rule set

Q1 MUST ask which rules govern the step and whether each is still in force, and MUST name the rule set inline:
`unattended` / no approval request / U4 -> next stage / spine written before acting / `workspace-guard --check` /
fast-fail / the gate discipline / budget.

(FR-004)

**C-5** — The verdict is one of exactly three values

The verdict MUST be exactly one of `on-track`, `correction-applied`, `decision-needed`. Only `decision-needed` is
surfaced; the other two are recorded and the loop continues.

**C-6** — The verdict precedes the next action, not the goal restatement

The protocol MUST order the audit so that the rule verdict and the action it licenses are stated before any goal
statement, and MUST NOT ask the goal as a separate question (the goal is implicit in Q3: "is the next action the one
the plan or assignment names?").

**Status**: this ordering is *stated* in the protocol and is **not yet asserted by any test** (recorded gap,
`guard-tests.contract.md` C-7). Until C-7 lands, C-6 is a documentation proposition only, and no green check may be
cited as its evidence.

(FR-005)

**C-7** — The audit is a statement, never an approval request

The protocol MUST state that the audit MUST NOT end with a question to the user, and the driver `SKILL.md` MUST carry
the same prohibition in its Hard Requirements block (`MUST NOT 以征求用户「继续」收尾`).

(FR-007)

**C-8** — The reload is tiered and bounded

The protocol MUST define T0 / T1 / T2 with their triggers, and MUST forbid a full reload of every reference at every
step, with the reason stated (ceremony that buries the anchor).

(FR-006)

**C-9** — Repeated drift escalates

Two consecutive audits flagging the same drift MUST escalate as a recurring anomaly under the fast-fail growth rule.
The audit does not define its own severity scale.
