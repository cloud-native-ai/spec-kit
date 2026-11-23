# Feature Detail: Research Command

**Feature ID**: 011  
**Name**: Research Command  
**Description**: Research projects through code, knowledge-base, and online studies.
**Status**: Completed  
**Created**: 2026-02-10  
**Last Updated**: 2026-11-22

## Overview

`/speckit.research` supports two modes. In an SDD run, `research-feature` creates or incrementally updates `research.md`, and project research uses `study-code`. In standalone mode, the command selects `study-code`, `study-kb`, or `study-online` according to the research question.

## Latest Review

2026-11-22 implementation audit: the former generic context-gathering text predated the three study carriers. The command now has an explicit SDD/standalone split, and the prerequisite script emits the feature path and documentation inventory as JSON.

## Key Changes

1. Generate or refresh implementation research through `research-feature` during SDD.
2. Use stripped, evidence-indexed source investigation through `study-code`.
3. Answer project-internal questions with `study-kb` and externally grounded questions with `study-online`.
4. Resolve feature context and available documents through deterministic prerequisite output.

## Implementation Notes

- Primary surfaces: `templates/commands/research.md`, `skills/internal/research-feature/SKILL.md`, `skills/external/study-code/`, `skills/internal/study-kb/`, and `skills/external/study-online/`.
- The standalone carriers are part of this feature's current capability and do not require separate registry rows.

## Future Evolution Suggestions

- Keep carrier selection and citation requirements aligned with newly added research sources.

## Related Files

- Feature Index: `.specify/features.md`
- Feature Detail: `.specify/features/011-research-command.md`
- Implementation: `templates/commands/research.md`, `skills/internal/research-feature/SKILL.md`
- Specification: none registered for this legacy command row.

## Status Tracking

- **Draft**: Concept defined.
- **Planned**: Specification and design approved.
- **Implemented**: Research workflow delivered and verified.
- **Blocked**: A final-path acceptance criterion fails.
- **Ready for Review**: Review evidence complete with no blocking code-review entry.
- **Sealed**: Canonical seal criteria met.
- **Completed** (legacy — current): Historical delivered status retained.
