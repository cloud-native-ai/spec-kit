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

---

Part 3 of 5 (tasks T017–T021), 2026-10-29, `HEAD=186d6ce9b` before this part's commits.

## S1 — Route a feature-scale change · EXECUTED 2026-10-29

`quickstart.md` S1 runs the route action against a feature-scale change. The command below is
S1 verbatim, with the `.specify/` mirror path (the shipped copy, not the canonical source):

```console
$ python3 .specify/scripts/python/sdd-route.py --action route \
    --nature feature --traceability required \
    --blast-radius cross-cutting --reversibility hard \
    --complexity standard --format json
```

Real output, exit `0`:

```json
{
  "action": "route",
  "owner_document": "/storage/project/cloud-native-ai/spec-kit/.specify/shared/definitions/sdd-routing-definitions.md",
  "verdict": "sdd",
  "reason_code": "sdd-capability-or-contract-change",
  "triggered_conditions": [
    "nature-feature",
    "traceability-required",
    "blast-cross-cutting",
    "reversal-hard",
    "complexity-low",
    "bounded-correction-recorded"
  ],
  "inputs": {
    "change_nature": "feature",
    "traceability": "required",
    "blast_radius": "cross-cutting",
    "reversibility": "hard",
    "complexity": "standard"
  },
  "effective_blast_radius": "cross-cutting",
  "bounded_correction_rationale": null,
  "absent_inputs": [],
  "ambiguous_inputs": [],
  "actor": null,
  "recorded_at": null,
  "override": null
}
# RC=0
```

**Reading**: the expected shape from `quickstart.md` holds — verdict `sdd`, a reason code from the
owner's closed vocabulary (`sdd-capability-or-contract-change` is the first declared *sdd* row whose
condition held), and the five input values echoed back. The two `direct`-branch condition ids in
`triggered_conditions` are expected and documented in the owner's § Precedence: the carried set is
every triggered condition across the three branches, so a marginal direct condition that held but was
absorbed by the higher-precedence verdict still appears.

## S2 — Route a bounded maintenance change · EXECUTED 2026-10-29

```console
$ python3 .specify/scripts/python/sdd-route.py --action route \
    --nature maintenance --traceability not-required \
    --blast-radius local --reversibility reversible \
    --complexity standard --format json
```

Real output, exit `0`:

```json
{
  "action": "route",
  "owner_document": "/storage/project/cloud-native-ai/spec-kit/.specify/shared/definitions/sdd-routing-definitions.md",
  "verdict": "direct",
  "reason_code": "direct-conditions-all-hold",
  "triggered_conditions": [
    "nature-preserves",
    "traceability-not-required",
    "blast-local",
    "reversal-reversible",
    "complexity-low",
    "bounded-correction-recorded"
  ],
  "inputs": {
    "change_nature": "maintenance",
    "traceability": "not-required",
    "blast_radius": "local",
    "reversibility": "reversible",
    "complexity": "standard"
  },
  "effective_blast_radius": "local",
  "bounded_correction_rationale": null,
  "absent_inputs": [],
  "ambiguous_inputs": [],
  "actor": null,
  "recorded_at": null,
  "override": null
}
# RC=0
```

**Reading**: verdict `direct` with the record naming all six conditions that held (C-22 is an `all`
branch, so the record shows the whole conjoint set, not just one witness). The value literals used
here (`maintenance`, `not-required`, `local`, `reversible`, `standard`) are the owner document's
declared domain values — S2's own disclaimer said the example would be wrong if they differed, and
they do not.

## S3 — A missing input never falls through to direct · EXECUTED 2026-10-29

```console
$ python3 .specify/scripts/python/sdd-route.py --action route \
    --nature maintenance --traceability not-required \
    --blast-radius local --reversibility reversible --format json
```

Real output, exit `0` — the complexity tier was not declared, and every supplied value points at
direct:

```json
{
  "action": "route",
  "owner_document": "/storage/project/cloud-native-ai/spec-kit/.specify/shared/definitions/sdd-routing-definitions.md",
  "verdict": "adjudicate",
  "reason_code": "adjudicate-missing-input",
  "triggered_conditions": [
    "input-missing",
    "nature-preserves",
    "traceability-not-required",
    "blast-local",
    "reversal-reversible",
    "bounded-correction-recorded"
  ],
  "inputs": {
    "change_nature": "maintenance",
    "traceability": "not-required",
    "blast_radius": "local",
    "reversibility": "reversible",
    "complexity": null
  },
  "effective_blast_radius": "local",
  "bounded_correction_rationale": null,
  "absent_inputs": [
    "complexity"
  ],
  "ambiguous_inputs": [],
  "actor": null,
  "recorded_at": null,
  "override": null
}
# RC=0
```

The conflicting form from the same scenario — a feature-scale change paired with a bounded
definition correction:

```console
$ python3 .specify/scripts/python/sdd-route.py --action route \
    --nature feature --blast-radius local-bounded-definition-correction \
    --traceability not-required --reversibility reversible --complexity trivial \
    --rationale "只收紧一处定义措辞" --format json
# verdict: adjudicate / reason_code: adjudicate-conflicting-inputs
# triggered_conditions: input-conflicting, nature-feature, blast-cross-cutting, ...
# RC=0
```

**Reading**: both adjudicate forms exit `0` — an adjudication is a produced verdict, not an engine
failure (C-28) — and neither falls through to `direct` even though five of the six direct conditions
held in the first case. `absent_inputs` names the missing input rather than leaving the reader to
infer it.

## S1 / S2 / S3 — golden table judged row by row · EXECUTED 2026-10-29

The owner document's § Golden case table is the row set's single landing place; the golden action
parses it and judges every row. Two runs, byte-identical:

```console
$ python3 scripts/python/sdd-route.py --action golden --format json > notes/golden-run1.json   # RC=0
$ python3 scripts/python/sdd-route.py --action golden --format json > notes/golden-run2.json   # RC=0
$ cmp notes/golden-run1.json notes/golden-run2.json && echo identical
identical
$ sha256sum notes/golden-run1.json notes/golden-run2.json
7ad8419ee75bbdd9d33d57b5662003a22ab24553509ff15dc036bdbce97b8fe9  notes/golden-run1.json
7ad8419ee75bbdd9d33d57b5662003a22ab24553509ff15dc036bdbce97b8fe9  notes/golden-run2.json
```

Row-by-row check (`--action golden --format text`, exit `0`):

```text
ok   G1-feature-scale: sdd / sdd-capability-or-contract-change (expected sdd / sdd-capability-or-contract-change)
ok   G2-bounded-maintenance: direct / direct-conditions-all-hold (expected direct / direct-conditions-all-hold)
ok   G3-cross-cutting: sdd / sdd-cross-cutting-radius (expected sdd / sdd-cross-cutting-radius)
ok   G4-irreversible: sdd / sdd-hard-reversal (expected sdd / sdd-hard-reversal)
ok   G5-ambiguous-value: adjudicate / adjudicate-ambiguous-value (expected adjudicate / adjudicate-ambiguous-value)
ok   G6-conflicting: adjudicate / adjudicate-conflicting-inputs (expected adjudicate / adjudicate-conflicting-inputs)
ok   G7-bounded-definition-correction: direct / direct-conditions-all-hold (expected direct / direct-conditions-all-hold)
ok   G8-missing-input: adjudicate / adjudicate-missing-input (expected adjudicate / adjudicate-missing-input)
ok   G9-definition-class-default: sdd / sdd-cross-cutting-radius (expected sdd / sdd-cross-cutting-radius)
ok   G10-complexity-high: sdd / sdd-complexity-high (expected sdd / sdd-complexity-high)
ok   G11-traceability: sdd / sdd-traceability-required (expected sdd / sdd-traceability-required)
ok   G12-bounded-without-rationale: adjudicate / adjudicate-missing-input (expected adjudicate / adjudicate-missing-input)
ok   G13-all-sdd-conditions: sdd / sdd-capability-or-contract-change (expected sdd / sdd-capability-or-contract-change)
ok   G14-ambiguous-beats-conflict: adjudicate / adjudicate-ambiguous-value (expected adjudicate / adjudicate-ambiguous-value)
14 cases, all_match=True
```

**Ambiguous and conflicting rows return `adjudicate`, never `direct`** (the explicit re-check T021
asks for): G5 and G14 both land on `adjudicate / adjudicate-ambiguous-value`, G6 on
`adjudicate / adjudicate-conflicting-inputs`. G14 is the code-taking-order witness — it hits *both*
an ambiguous value and the conflict combination, and the record shows
`triggered_conditions: [input-ambiguous, input-conflicting, nature-feature, blast-cross-cutting, ...]`
while the reason code is the earlier declared row (`adjudicate-ambiguous-value`, row 2, taken ahead
of `adjudicate-conflicting-inputs`, row 3), so every triggered condition is carried and two
evaluations of the same inputs stay byte-identical (C-24).

**Pinning tests**: `tests/contract/test_sdd_routing_engine.py` (21 cases: determinism, precedence,
reason-code order, exit alphabet, zero writes, three owner-document mutation probes, golden row
judging, golden byte-identity). **Full logs**: `green-t021.txt`, `golden-run1.json`,
`golden-run2.json`, `golden-rows.txt`.

---

## Governance — pre-dispatch blocking records (US3) · EXECUTED 2026-10-29

`quickstart.md` carries no governance scenario (its S1–S7 are routing, authorization, nested run,
acceptance evidence and the three baselines), so this section is US3's own evidence and does not
reuse S6. Part 4 of 5 (tasks T022–T025), `HEAD=0dbe8897b` before this part's commits; the record below
was produced against the slice's disposable target project (`tests/fixtures/nested_sdd.py`,
`variant="block"`: one allowed seat, one forbidden seat, one seat with no roster entry).

**The four dispatch forms and the surface that decides each** (US3's independent test as
`test_sdd_invocation_governance.py::test_the_four_dispatch_forms_each_carry_their_rule`):

| Form | Decision | Decided by |
|------|----------|------------|
| authorized SDD assignment | dispatched, basis recorded | `sdd-route.py --action authorize` (two halves) + the duty's recorded `sdd` decision |
| prompt naming a driver without both halves | blocked before dispatch, failed condition named | the probe (`run-agent/SKILL.md`) on the engine's refusal |
| stage executor hosting a driver | refused — a stage executor is a leaf | owner site § Dispatch-Time Governance Obligation (`MUST NOT start or host any SDD run`) |
| SDD attempt inside a stage | refused — SDD-within-SDD recursion prohibited | same owner site |
| virtual-mode member hosting a run | refused — virtual execution occupies the orchestrating session | same owner site (`MUST NOT host an SDD run`) |

**Live blocking records (two declared halves, real output).** Command shape for every case:
`python3 <repo>/scripts/python/sdd-route.py --action authorize --agent <definition> --team
fixture-team --seat <seat> --format json`, run with the target project as working directory.

```console
$ cd <target-project> && python3 <repo>/scripts/python/sdd-route.py --action authorize \
    --agent <target-project>/.specify/agents/instances/seat-allowed.agent.md \
    --team fixture-team --seat seat-allowed --format json
# form 1 — authorized SDD assignment: dispatched, authorization basis recorded
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
  "supplying": {"agent": "declared", "seat": "declared"},
  "sources": {"agent": ".../agents/instances/seat-allowed.agent.md", "team": ".../teams/fixture-team/team.md"}
}
# RC=0

$ cd <target-project> && python3 <repo>/scripts/python/sdd-route.py --action authorize \
    --agent <target-project>/.specify/agents/instances/seat-allowed.agent.md \
    --team fixture-team --seat seat-forbidden --format json
# form 2a — the seat half refuses: BLOCKED before dispatch, condition = seat
{
  "action": "authorize",
  "agent_capability": "allowed",
  "seat_policy": "forbidden",
  "effective": "forbidden",
  "verdict": "forbidden",
  "reason": "the seat half does not allow SDD invocation (absent map, absent entry for this seat, or explicit refusal)",
  "failed_half": "seat",
  "team_slug": "fixture-team",
  "seat_slug": "seat-forbidden",
  "supplying": {"agent": "declared", "seat": "declared"},
  "sources": {"agent": ".../agents/instances/seat-allowed.agent.md", "team": ".../teams/fixture-team/team.md"}
}
# RC=0

$ cd <target-project> && python3 <repo>/scripts/python/sdd-route.py --action authorize \
    --agent <target-project>/.specify/agents/instances/seat-forbidden.agent.md \
    --team fixture-team --seat seat-allowed --format json
# form 2b — the agent half refuses (key absent ⇒ default deny): BLOCKED, condition = agent
{
  "action": "authorize",
  "agent_capability": "forbidden",
  "seat_policy": "allowed",
  "effective": "forbidden",
  "verdict": "forbidden",
  "reason": "the agent half does not allow SDD invocation (absent key or explicit refusal; the owner's absent-key default is deny)",
  "failed_half": "agent",
  "team_slug": "fixture-team",
  "seat_slug": "seat-allowed",
  "supplying": {"agent": "absent-key", "seat": "declared"},
  "sources": {"agent": ".../agents/instances/seat-forbidden.agent.md", "team": ".../teams/fixture-team/team.md"}
}
# RC=0
```

Two further cases, same command shape, field projection of the run (full payloads have the shape
above):

```console
# form 2c — the seat has no seats entry:    verdict=forbidden  failed_half="seat"   supplying.seat="absent-entry"  seat_slug=seat-absent    # RC=0
# form 2d — both halves refuse:             verdict=forbidden  failed_half="both"   reason="neither half allows SDD invocation: the agent definition and the seat policy both deny"  seat_slug=seat-forbidden  # RC=0
```

Every refusal is a **produced verdict**, not an error status (exit `0`), and every one names the
failed condition, the recipient's resolved values, both source paths and the seat slug — the field
set C-14 requires, and the reason no reader has to accept a bare "not authorized".

**Stage executor and virtual-mode refusals — declared, not engine-produced.** The engine above
returns `allowed` for the authorized seat, which is exactly why the leaf rule and the virtual-mode
rule cannot live in the engine action: they are conditions on the *dispatch* (chain position and
execution mode), read by the probe from the target project's state, not facts of the two declared
halves. This slice adds no new command, gate or scheduler to make them executable (C-16), so their
evidence is the declaration plus the executable case that pins it:

- `shared/definitions/subagent-definitions.md` § Dispatch-Time Governance Obligation —
  `a stage executor MUST NOT start or host any SDD run`; `a member executed in virtual mode MUST NOT
  host an SDD run` … `the dispatch is refused before it leaves and the reason is reported`; refusal
  record = `failed condition + recipient's resolved values + both source paths + seat slug`.
- `skills/internal/run-agent/SKILL.md` § Pre-dispatch probe (fail-closed) — `a stage executor stays a
  leaf: a dispatch prompt handed to it MUST NOT name a driver`, and `Rewording the prompt cannot
  repair a refusal`.
- Pinned by `test_sdd_invocation_governance.py::test_c15_stage_executors_and_unqualified_prompts_are_blocked_before_dispatch`,
  `::test_c12_virtual_mode_must_not_host_a_run`, `::test_c14_a_refusal_record_names_the_condition_and_the_resolved_values`
  (17 passed, `notes/green-t025.txt`).

**Structure face — the authorization surface added no machinery** (`git diff --name-status
0dbe8897b..HEAD`): six paths, and not one of them is a command template, a skill directory, a
registry, a ledger or a state file —

```console
M shared/definitions/subagent-definitions.md     # owner site amended in place
M skills/internal/run-agent/SKILL.md             # probe amended in place
A tests/contract/test_sdd_invocation_governance.py
M .specify/specs/074a-authorized-routing/tasks.md
M .specify/specs/074a-authorized-routing/notes/red-first-evidence.md
A .specify/specs/074a-authorized-routing/notes/red-t022.txt
# git diff --name-status 0dbe8897b..HEAD -- .specify/state/ .specify/memory/registers  → empty
```

The confirmation-gate count, the scheduler inventory and the registry set are therefore unchanged by
this part; the full baseline comparison is task T028's (part 5), and this line only states what this
part's own diff shows.
