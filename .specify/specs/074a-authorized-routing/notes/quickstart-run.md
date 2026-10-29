# Quickstart run record — slice 074a-authorized-routing

Owner of this file: the slice's implement-stage quickstart evidence. `quickstart.md` defines the
scenarios; this file carries the **real output** of each one on the date it became executable.

Discipline: a section is appended by the task row that can actually run its scenario. A scenario
that cannot be run is recorded as `not-evaluated` with its reason, never as achieved. Every block
below was copied from a run in this session; nothing is reconstructed from memory.

Part 2 of 5 (tasks T009–T016), 2026-10-29, `HEAD=acfc762ae` before this part's commits.

---

## S4 — Resolve effective authorization · EXECUTED 2026-10-29

`quickstart.md` S4 shows `python3 .specify/scripts/python/sdd-route.py --action authorize …`
against a real `.specify/teams/<slug>/team.md`. This repository has no such team definition, so the
example is executed against the slice's fixture team (three seats: one allowed, one forbidden, one
with no entry), whose construction is task T006's.

Command shape (identical for both seats; only `--seat` changes):

```console
$ python3 scripts/python/sdd-route.py --action authorize \
    --agent seat-allowed.agent.md --team fixture-team --seat seat-allowed --format json
```

Real output — **allowed seat**, exit `0`:

```json
{
  "action": "authorize",
  "agent_capability": "allowed",
  "seat_policy": "allowed",
  "effective": "allowed",
  "verdict": "allowed",
  "reason": "both halves allow SDD invocation: the agent definition declares the capability and the seat policy allows it",
  "failed_half": null,
  "team_slug": "fixture-team",
  "seat_slug": "seat-allowed",
  "supplying": {
    "agent": "declared",
    "seat": "declared"
  },
  "sources": {
    "agent": "/home/agent/tmp/spec-kit/074a-quickstart/project/.specify/agents/instances/seat-allowed.agent.md",
    "team": "/home/agent/tmp/spec-kit/074a-quickstart/project/.specify/teams/fixture-team/team.md"
  }
}
# RC=0
```

Real output — **forbidden seat**, exit `0` as well: a refusal is a produced verdict, carried by the
record's `verdict` / `reason` / `failed_half` fields, never by the process status:

```json
{
  "agent_capability": "allowed",
  "seat_policy": "forbidden",
  "effective": "forbidden",
  "verdict": "forbidden",
  "reason": "the seat half does not allow SDD invocation (absent map, absent entry for this seat, or explicit refusal)",
  "failed_half": "seat",
  "seat_slug": "seat-forbidden"
}
# RC=0   (elided to the fields the scenario is about; the full record carries the same
#         team_slug / supplying / sources members as the allowed case above)
```

Real output — **malformed `seats:` map** (flow style), exit `2`, the seat named:

```console
$ python3 scripts/python/sdd-route.py --action authorize \
    --agent seat-allowed.agent.md --team fixture-team --seat seat-allowed --format json
# (stdout empty)
sdd-route: /home/agent/tmp/spec-kit/074a-quickstart/flow/.specify/teams/fixture-team/team.md:
  'seats' is a flow-style map ('{ seat-allowed: { sdd-invocation: allowed } }'); only a block map
  keyed by seat slug is accepted (seat under resolution: 'seat-allowed')
# RC=2
```

**Reading**: the exit alphabet is exactly two-valued (C-8 / C-28) — `0` for both verdicts and `2`
only for malformed input — and a refusal names the failing half (`seat`) plus both source paths and
the seat slug, so the verdict is recheckable (C-14). The scratch root
(`~/tmp/spec-kit/074a-quickstart/`) was removed after the run, per
`.specify/shared/guidelines/temp-directory-discipline.md` §4.

**Pinning test**: `tests/contract/test_sdd_authorization.py` (11 cases). **Full log**:
`green-t016-demo.txt` (which is also the source of the S5 output below).

---

## S5 — Start a nested run and receive the handoff · EXECUTED (content face) 2026-10-29

`quickstart.md` S5 emits no shell command on purpose: `/speckit.*` and the SDD driver are chat
instructions, so there is no executable "start a nested run" CLI. The decidable face executed here is
the one C-41 / D-3 fixes — **the content face**: the entry precondition resolves **allowed** on the
authorized seat and **refused with the failing half named** on the forbidden seat, the assembled
handoff carries the whole closed field set, the stages reached stop at `review`, and a real
repository's `git log` / `git status` are identical before and after (zero merge, zero push).

Real output:

```console
BEFORE  git log --oneline: de7a434 nested run: artifact chain through review
BEFORE  git status --porcelain: (clean)
BEFORE  branch: main HEAD: de7a4342a207adb9de2d7b417ba5c6f8d65a0e75

allowed seat   -> effective: allowed failed_half: None
forbidden seat -> effective: forbidden failed_half: seat | reason: the seat half does not allow SDD
                  invocation (absent map, absent entry for this seat, or explicit refusal)

HANDOFF (seven closed fields, field-presence check):
{
  "outcome": "completed",
  "stages_reached": ["requirements", "clarify", "plan", "tasks", "checklist", "analyze", "implement", "review"],
  "artifact_paths": ["/home/agent/tmp/spec-kit/074a-quickstart/line/artifact.md"],
  "evidence_paths": ["/home/agent/tmp/spec-kit/074a-quickstart/project/.specify/agents/execution/20261029T000000Z-routing-verdict-d1.md"],
  "unresolved_findings": [],
  "anomaly_line": "未发现异常",
  "integration_identity": {
    "line_id": "074a-fixture-line",
    "branch": "main",
    "worktree_path": "/home/agent/tmp/spec-kit/074a-quickstart/line",
    "head_commit": "de7a4342a207adb9de2d7b417ba5c6f8d65a0e75"
  }
}
missing fields: []
stages_reached stops at review: review | 'merge' in stages: False

AFTER   git log --oneline: de7a434 nested run: artifact chain through review
AFTER   git status --porcelain: (clean)
AFTER   branch: main HEAD: de7a4342a207adb9de2d7b417ba5c6f8d65a0e75
zero merge / zero push (git log + status + branch + HEAD identical): True
```

(The `stages_reached` / `HANDOFF` blocks are rendered over several lines in this record; the run
printed `stages_reached` across eight lines and the JSON with two-space indentation. Field values,
verdicts and the git states are verbatim.)

**Reading**: the complete handoff carries all seven closed fields (C-34) — including the four-fact
integration identity with `main` named as the retained branch (C-36) — and the run's git state is
byte-identical before and after, which is what "zero merge and zero push" looks like when it is
measured rather than asserted (C-37 / C-41). The entry half is the engine's own verdict: the
authorized seat resolves `allowed`, the forbidden seat resolves `forbidden` with `failed_half=seat`.

**Pinning test**: `tests/contract/test_nested_sdd_invocation.py::test_nested_run_reaches_review_zero_merge_zero_push`
(the same shape is restated case by case across the module's 23 cases). **Full log**:
`green-t016-demo.txt`.
