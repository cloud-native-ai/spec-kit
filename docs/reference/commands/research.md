# /speckit.research

In-depth research and analysis in two modes. In **SDD mode** it backs the implementation plan, and its project study is the `study-code` skill applied to this project. In **standalone mode** it investigates any question through three study carriers — `study-code` (source code), `study-kb` (the project's own knowledge base), `study-online` (the web) — chosen per question.

## When to Use

- **SDD mode**: the requirements or plan has open questions that need evidence or repo context; the tech stack or approach has unknowns; `NEEDS CLARIFICATION` items need resolution.
- **Standalone mode**: any research question — how a repository's code works, what this project already decided/learned, or what the outside world says — with or without a feature in flight.

## Syntax

```text
/speckit.research [research topic or question] [--standalone] [--carriers code|kb|online[,…]]
```

- `[research topic or question]` — the technical uncertainty or exploration area (optional in SDD mode).
- `--standalone` — force standalone mode even when a feature spec resolves.
- `--carriers` — restrict the standalone carrier set; absent, the command decides from the question.

## Execution Flow

1. **Mode decision** — run `research-project.sh`. A payload naming an existing `FEATURE_SPEC` selects SDD mode; a failure or empty feature resolution selects standalone (the report states which signal decided). `--standalone` forces standalone.

2. **SDD mode — `research-feature` with the `study-code` carrier**:
   - Setup: locate the requirements spec, plan, specs directory, branch, and available documentation.
   - Load context: the requirements spec, the constitution, and the relevant docs from `AVAILABLE_DOCS`.
   - Information gathering:
     - **Own-project study**: a `study-code` invocation against this project (reuse `.specify/studies/<repo>-study/` when `target-commit.txt` matches HEAD; otherwise run the study), cited by evidence path.
     - **Feature interdependencies**: `.specify/features.md` and `.specify/features/` conflicts or reuse.
     - **Unknown resolution**: `NEEDS CLARIFICATION` markers and user questions.
     - **Technology selection**: best practices verified against the gathered context.
   - SDD research invokes **no other study carrier**: unknowns the project cannot answer stay under Open Questions & Risks — the standalone mode is their route.
   - Write/append `research.md` (merge-only), then report its path and key findings.

3. **Standalone mode — per-question carrier selection**:
   - Decompose the question into sub-questions and map each to the carrier that can answer it: code → `study-code`; project knowledge → `study-kb`; external world → `study-online`. Combine carriers only when the question genuinely spans domains.
   - Each carrier produces its own report (`.specify/studies/<repo>-study/docs/overview.md`, `.specify/studies/<slug>-kb/report.md`, `.specify/studies/<slug>-online/report.md`).
   - When one carrier fully answers, its own report is the deliverable; otherwise synthesize `report.md` under `.specify/studies/<question-slug>-research/`.
   - Standalone never writes `research.md` (that artifact belongs to SDD mode).

## Output Structure

SDD mode — `research.md`:

```markdown
# Research Findings: [Feature Name]

## Project Context Analysis
[Insights from the own-project study, project docs and feature memory]

## References
- [Study report sections and evidence paths]
- [Doc files and feature memory files referenced]

## Decisions & Rationale
### [Decision Topic]
- **Decision**: [what was chosen]
- **Rationale**: [why, citing references]
- **Alternatives considered**: [what else was evaluated]
- **Impact**: [how this affects the plan]

## Open Questions & Risks
- [Remaining unknowns requiring human input]
```

Standalone mode — `report.md`: question & decision, carrier coverage, findings with evidence pointers, conflicts, answer, gaps.

## Output Artifacts

| Mode | Artifact | Location |
|------|----------|----------|
| SDD | Research findings | `.specify/specs/<key>/research.md` |
| SDD | Own-project study (reused or produced) | `.specify/studies/<repo>-study/` |
| Standalone | Synthesis report | `.specify/studies/<question-slug>-research/report.md` |
| Standalone | Carrier reports | `.specify/studies/<repo>-study/`, `<slug>-kb/`, `<slug>-online/` |

## Prerequisites

- SDD mode: a resolvable feature spec (run after `/speckit.requirements`, before `/speckit.plan`).
- Standalone mode: none beyond the question itself; `study-kb` requires the `.specify/` knowledge layout, `study-online` requires network access.

## Next Steps

- SDD mode: proceed to [`/speckit.plan`](plan.md) (or re-run it) to encode research decisions into the technical plan.
- Standalone mode: the report feeds whatever comes next; there is no automatic command handoff.
