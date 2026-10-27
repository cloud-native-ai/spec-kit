# /speckit.review

Critically review the SDD process for the current feature **and** the code delta it produced, and produce two self-contained, improvement-focused artifacts: a process review report for spec-kit maintainers and, when this feature slice delivers code, a code review record.

## When to Use

- After `/speckit.implement` completes — to evaluate the SDD process quality and, in the same run, review the code this feature committed
- When you want to identify friction, ambiguity, and improvement opportunities in the spec-kit workflow
- When you need a pre-merge verdict on this feature slice's committed code delta, with a coverage receipt proving how much of that delta was actually read
- To generate a portable report that can be shared with framework maintainers

## Syntax

```text
/speckit.review [review criteria or focus areas]
```

`[review criteria or focus areas]` is optional — specify quality dimensions or reporting preferences. It guides focus; it never selects one segment over the other.

## Composition — two segments, one fixed order

A single invocation runs exactly **two segments in a fixed order**. There is no parallel mode, no single merged report, and no parameter — `$ARGUMENTS` included — that selects one segment over the other.

1. **The process segment runs first, on every invocation.** No execution class or expression class exempts it, no argument exempts it, an absent code delta does not exempt it, and no earlier segment's outcome exempts it.
2. **The code segment runs second**, and its applicability is decided by an explicit triage before it starts.

The two conclusions are never merged: not into one severity system, not into one score, not through a mapping table or a conversion.

## Segments and their delegation

Each segment is delegated to its existing skill by runtime path. The command orchestrates and points; it inlines neither skill's methodology — no dimension list, no severity definitions, no receipt field list.

| Segment | Skill | Judgment object |
|---------|-------|-----------------|
| Process segment | `review-sdd-process` (`.specify/skills/internal/review-sdd-process/SKILL.md`) | the SDD process that produced the feature — process and tooling quality, never the feature's business merits, never the code it produced |
| Code segment | `code-review` (`.specify/skills/internal/code-review/SKILL.md`) | verifiable defects in this feature slice's committed code delta |

A process-segment abort does not suppress the code segment: the two judgment objects are independent, the abort is recorded as `not-evaluated` with its reason, and the command itself authors the minimal process report (carrying the code-segment subsection and the abort reason) so the verifiable carrier stays the single `review.md`.

## Review object — the committed delta

The code segment judges this feature slice's committed code delta, reviewed as the range `base..head` and recorded so any later reader can recompute it with `git diff base..head`. Base and head resolution belong to the skill's deterministic script — `skills/internal/code-review/scripts/git-delta-review.sh`, whose `base` step owns the ordered resolution tiers, the closed trunk order and the run-start-fixed head.

Uncommitted working-tree changes are **not** part of that object: when they exist, the run discloses the unreviewed scope on both carriers and issues no pass conclusion over it.

## Applicability triage — three closed values

Before the code segment starts, the run resolves its applicability to exactly one of three values:

| Value | When it applies | What it obliges |
|-------|-----------------|-----------------|
| `run` | this feature has a committed code delta containing at least one code path | the code segment runs and `code-review.md` is written |
| `not-applicable` | the feature produces no code deliverable, or has no committed code delta | a basis naming one of those two facts |
| `not-evaluated` | the environment or the base resolution prevents evaluation | a reason, with the reproducible command that failed |

There is no fourth state: an unspecified value, an empty value, or a silently dropped segment is a violation. A `pass` verdict can never be attached to a non-`run` triage. What counts as a code path is decided by the script's closed default set (overridable with an explicit `--code-paths`), never by the command. An empty delta is triaged before any coverage receipt runs, so an empty changed set is never reported as a clean review of nothing.

## Output artifacts — two files, one directory

| Artifact | Location | Written when |
|----------|----------|--------------|
| Process review report | `.specify/specs/<key>/review.md` | every invocation |
| Code review record | `.specify/specs/<key>/code-review.md` | the triage value is `run` only |

Neither file overwrites the other. `not-applicable` and `not-evaluated` create **no** record file — not even an empty one — and their verdict and reason live in the report's code subsection (`### 2.1`). When a run finds an existing `code-review.md`, it first archives it in the same directory as `code-review-<YYYYMMDDTHHMMSSZ>.md` (UTC, second resolution) and then writes the new record; `code-review.md` therefore always denotes the latest run, and every earlier run survives as its own archive file.

Both segment conclusions land on two verifiable carriers: the report's code subsection and the bound feature detail's existing `## Latest Review` entry. The closing summary may restate them, but it is a presentation, not a third carrier: it carries no obligation of its own, and where it disagrees the carriers govern.

## Severity vocabularies — two, never mapped

Each segment keeps its own vocabulary, and no run maps one onto the other: no numeric conversion, no mapping matrix and no unified score exists between them.

The process segment's vocabulary, defined by `review-sdd-process`:

| Severity | Meaning |
|----------|---------|
| P0 | Blocks correct use of spec-kit or creates silent corruption risk |
| P1 | Recurring friction across specs |
| P2 | Quality-of-life improvement |

The code segment's vocabulary is defined by `code-review` and runs from `blocking` to `praise`; its levels are defined there and are never relabelled, weighted or converted here. An `important` item never blocks the transition but MUST be answered; the levels below it never block either.

A code-segment finding keeps its locating form — severity plus file and optional line — inside `code-review.md`. It is never coined as a `REC-…` identifier and never registered in the register; that family stays with framework-targeted recommendations.

## Status transition — where the criteria live

This run judges exactly one status transition, `Implemented → Ready for Review`, and states no criterion of its own: the criteria — three conjunctive conditions, the third an existence test over the current `code-review.md` — are owned by `templates/feature-details-template.md` § Canonical Status State Machine, and the transition table in `.specify/shared/workflow/feature-integration.md` cites that owner instead of restating it.

The transition is judged **once**, after both segments have finished and both artifacts are on disk; the status MUST NOT flip before the code segment completes. A waiver is an explicit user ruling or there is none. Without one, an unattended run halts before the transition, names the failed condition and records `blocking-unresolved` as its refusal literal, leaving the status at `Implemented`.

## Coverage receipt — the only evidence of "the whole diff was read"

The code segment's "I read the whole delta" claim is evidence-bearing only through the coverage receipt: a delimited block inside `code-review.md` whose file set equals the delta's changed-file set, with a per-file verdict. The exit alphabet is closed at three — `0` when every file carries a verdict, `1` on a gap, `2` on a state it cannot evaluate — and a non-zero gap or skip count is surfaced outside the block as well. The receipt counts reviewed files; it is never test or compile coverage.

## Feedback boundary — friction only

A feedback entry records friction of the framework itself — a missing renderer, an ambiguous base, an insufficient non-interactive path, a receipt gap. A code defect found by the code segment MUST NOT be posted as a feedback entry: it stays in `code-review.md`, where its severity, file and line are meaningful. One run has **three** units — this command, `skill:review-sdd-process` and `skill:code-review` — each with its own `unit_id` under one run id, so none dedups or merges another. The closing step set is unchanged, this composition adds no side channel, and nothing is transmitted automatically.

## Key Characteristics

- **Composed, not merged** — two judgment objects, two artifacts, two vocabularies, one fixed order
- **Problem-first** — the process segment focuses on what to change, not on what each artifact contains
- **Evidence-backed** — process findings without quoted excerpts are dropped; code findings carry severity plus location
- **Honest about scope** — a non-`run` triage, an unread file and an excluded uncommitted change are all disclosed rather than glossed over

## Prerequisites

- Run after [`/speckit.implement`](implement.md) so there is a complete artifact chain to review
- The code segment needs git history for the feature slice; its script resolves the base itself and reports `not-evaluated` with the failing command when it cannot

## Next Steps

- Register every `REC-…` id coined in the report in `.specify/memory/register.md` in the same commit as the report
- Apply improvements to spec-kit templates, command prompts, and scripts
- Optionally iterate on [`/speckit.requirements`](requirements.md) or [`/speckit.plan`](plan.md) to fix current-spec findings
- Optionally run [`/speckit.analyze`](analyze.md) to validate consistency after revisions
