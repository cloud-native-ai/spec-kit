# Contract: Reporter Seat and Roster Guard

**Feature**: 087 | **Covers**: FR-005, FR-006, FR-021
**Contract object**: (a) the Agent Template `agents/reporter.agent.md` and its mirror
`.specify/agents/templates/reporter.agent.md`; (b) the roster obligation stated in
`skills/internal/create-team/SKILL.md` + `references/create-mode.md`; (c) the deterministic guard
`skills/internal/create-team/scripts/validate-roster.py` and its mirror.

Clause ids are dense (`RS-01`…`RS-08`) and are cited verbatim by `/speckit.tasks`.

---

## C-14 · RS-01 — The reporting role is an Agent **Template** in the existing template store

The delivered file MUST be `agents/reporter.agent.md`, and its mirror MUST be
`.specify/agents/templates/reporter.agent.md` (the `agents/` → `.specify/agents/templates/` pair of
`scripts/python/sync-mirrors.py`). No new directory is created in either place (`requirements.md` A13, FR-005).

The frontmatter MUST carry the framework's neutral agent keys as its siblings do — at minimum `name`,
`description`, `user-invocable`, `model-tier`, `capability-tools`, `skills`, `run-turn-budget`, `display-color` —
with `user-invocable: false` (a seat is dispatched, not invoked by a user).

*Judged by*: `tests/contract/test_reporting_obligations.py` — file existence on both sides, byte equality, and the
key set.

## C-15 · RS-02 — The seat is a roster member row, not a new roster key

The obligation MUST be expressed as a row of the existing `members[]` list in the team schema
(`skills/internal/create-team/references/create-mode.md` § Team Schema) whose `role` is the literal `reporter`.
The schema MUST NOT gain a parallel `reporter:` block: roster membership has one expression point.

The row's two seat-specific keys are `reporting-territory` (`read` list + `write` list) and `reporting-cadence`
(an explicit duration or the literal `default`), plus `reporting-reason` where RS-05 applies.

*Judged by*: `tests/contract/test_roster_reporter_seat.py` — reads `references/create-mode.md`, asserts the schema
block carries `members[]`, asserts `role: reporter` is the discriminator, and asserts no top-level `reporter:` key
is introduced.

## C-16 · RS-03 — A missing seat is a NAMED defect

`skills/internal/create-team/scripts/validate-roster.py` MUST accept a team file path and MUST report a missing
reporter seat as a defect whose message **names the seat** (the literal `reporter` and the team slug) rather than
reporting a generic failure. A roster that carries a reporter row whose `agent` does not resolve to the shipped
template or to a seat instance referencing it is a **second** named defect, distinct from the missing-seat one.

Exit codes: `0` = the roster satisfies the obligation (seat present, or an RS-05 reason recorded); `1` = at least
one named defect; `2` = input error (file missing, frontmatter unparsable).

*Judged by*: `tests/contract/test_roster_reporter_seat.py` — three fixtures (compliant, missing-seat,
unresolvable-agent) with the exact expected defect name asserted.

## C-17 · RS-04 — The recorded reason is an accepted alternative, never a silent omission

When `reporting-reason` is present, the guard MUST judge the roster **conforming** and MUST echo the reason in its
output, so a reader can tell a recorded omission from a forgotten seat. The accepted values are the closed set
`all-lanes-in-session-single-interval` (FR-021's runtime-omission condition) and `host-cannot-host-reporter`. A
`reporting-reason` value outside that set is a named defect of its own.

*Judged by*: same test file — one fixture per value plus one out-of-domain fixture.

## C-18 · RS-05 — The runtime-omission condition is exactly FR-021's

`references/create-mode.md` MUST state the runtime-omission condition as two conjunctive facts — every lane is
executed by the current session, **and** the whole run is expected to finish inside one cadence interval — and MUST
state that under it the orchestrating session carries the reporting duty itself. Outside that condition a reporter
execution is required. The condition MUST NOT be widened by a per-team judgement.

*Judged by*: `tests/contract/test_roster_reporter_seat.py` asserts both conjuncts appear and that the "carries the
duty itself" consequence is stated.

## C-19 · RS-06 — The Template's authority is read + write-own-stream, and nothing else

`capability-tools` MUST contain only read-class tools (Read, Grep, Glob) plus the minimal write surface for the
reporter's own stream artifact, and MUST NOT contain any tool that dispatches an agent, launches a process,
authorizes, retries or terminates work. The body MUST state in one clause that the reporter observes and reports,
and that a reporter observed mutating anything outside its own stream artifact is a defect.

*Judged by*: `tests/contract/test_reporting_obligations.py` — a deny list over the `capability-tools` value
(`Agent`, `Task`, `Bash` launching a CLI, any dispatch wrapper) and the presence of the boundary clause.

## C-20 · RS-07 — The seat carries the dispatch-injection duties it is subject to

The Template body MUST reference, and MUST NOT restate: `shared/guidelines/fast-fail.md` § 子代理派发注入 (the
anomaly-return line) and `shared/guidelines/progress-reporting.md` § 子代理与委托（派发时注入） (the duty's own
injection into further dispatches). The reference is by path plus anchor; a copy of either clause inside the Template
is a defect.

*Judged by*: `tests/contract/test_reporting_obligations.py` — both anchors resolve to real sections and the Template
does not contain their clause text.

## C-21 · RS-08 — The guard is stdlib-only and is called from the create procedure

`skills/internal/create-team/scripts/validate-roster.py` MUST import only the standard library (it runs under the
plain `python3` a host provides, with no `pip install`), MUST be a single file, and MUST be invoked from a numbered
step of `references/create-mode.md` or of `SKILL.md` so the obligation is reachable without a separate command.

*Judged by*: `tests/contract/test_roster_reporter_seat.py` — an import audit over the file's `import` lines plus an
assertion that `create-mode.md` or `SKILL.md` names the script.
