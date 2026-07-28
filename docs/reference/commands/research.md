# /speckit.research

Conduct in-depth research and analysis to support the implementation plan, resolving technical uncertainties and informing architectural decisions.

## When to Use

- When the requirements or plan has open questions that need evidence or context
- Before planning, if the tech stack or approach has significant unknowns
- When external data, technology comparisons, or project architecture understanding is needed
- To resolve `NEEDS CLARIFICATION` items in the spec or plan

## Syntax

```text
/speckit.research [research topic or question]
```

`[research topic or question]` is optional — specify the technical uncertainty or exploration area.

## Execution Flow

1. **Setup** — Runs `research-project.sh` to locate the requirements spec, plan, specs directory, branch, and available documentation.

2. **Load context**:
   - Reads the requirements specification (`FEATURE_SPEC`)
   - Reads the constitution
   - Reviews available project documentation (`AVAILABLE_DOCS`) from the setup output
   - Reads README and key docs relevant to the feature

3. **Information gathering & analysis**:
   - **Project architecture**: Understands how the new feature fits into the existing system
   - **Feature interdependencies**: Checks feature memory for conflicts or reuse opportunities
   - **Unknown resolution**: Addresses `NEEDS CLARIFICATION` items or questions from user input
   - **Technology selection**: Verifies best practices using the gathered context

4. **Generate/update `research.md`**:
   - If the file exists: **appends** new findings (does not overwrite valid research)
   - If the file doesn't exist: creates it with the standard structure

5. **Report** — Outputs the path of `research.md` and summarizes key findings.

## Output Structure

```markdown
# Research Findings: [Feature Name]

## Project Context Analysis
[Insights from project docs and feature memory]

## References
- [Doc files and feature memory files referenced]
- [External references from arguments]

## Decisions & Rationale
### [Decision Topic]
- **Decision**: [what was chosen]
- **Rationale**: [why, citing references]
- **Alternatives considered**: [what else was evaluated]
- **Impact**: [how this affects the plan]

## Open Questions & Risks
- [Remaining unknowns requiring human input]
```

## Output Artifacts

| Artifact | Location |
|----------|----------|
| Research findings | `.specify/specs/<key>/research.md` |

## Prerequisites

- Run when the plan/spec has open questions that require evidence or context

## Next Steps

- Proceed to [`/speckit.plan`](plan.md) (or re-run it) to encode research decisions into the technical plan
